#!/usr/bin/env python3
"""Validate a Her Gallery JSON manifest and its local media references."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


THEMES = {
    "moonlit-letter",
    "summer-film",
    "forest-specimen",
    "cosmic-stage",
}
LAYOUTS = {"classic-card", "romantic-stage", "editorial-scroll"}
IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".avif"}
VIDEO_SUFFIXES = {".mp4", ".mov", ".webm"}
AUDIO_SUFFIXES = {".mp3", ".m4a", ".ogg", ".wav"}
MEDIA_SUFFIXES = IMAGE_SUFFIXES | VIDEO_SUFFIXES | AUDIO_SUFFIXES
PHOTO_MOTIONS = {"none", "slow-zoom", "drift-left", "drift-right", "breathe"}
PRESET_BACKGROUNDS = {
    "star-meadow": "star-meadow.jpg",
    "sunlit-valley": "sunlit-valley.jpg",
    "teal-sky": "teal-sky.jpg",
}


def load_manifest(manifest_path: Path) -> dict:
    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"找不到清单：{manifest_path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"JSON 格式错误（第 {exc.lineno} 行）：{exc.msg}") from exc
    if not isinstance(data, dict):
        raise ValueError("清单顶层必须是 JSON 对象。")
    return data


def validate_manifest(data: dict, manifest_path: Path) -> tuple[list[str], list[str], int]:
    errors: list[str] = []
    warnings: list[str] = []
    total_bytes = 0

    for field in ("slug", "displayName", "title", "preface", "chapters", "dedication"):
        if field not in data:
            errors.append(f"缺少必填字段：{field}")

    slug = data.get("slug")
    if not isinstance(slug, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
        errors.append("slug 只能包含小写字母、数字和单个连字符。")

    theme = data.get("theme", "moonlit-letter")
    if theme not in THEMES:
        errors.append(f"未知主题：{theme}。可选：{', '.join(sorted(THEMES))}")
    layout = data.get("layout", "classic-card")
    if layout not in LAYOUTS:
        errors.append(f"未知展示模式：{layout}。可选：{', '.join(sorted(LAYOUTS))}")

    chapters = data.get("chapters")
    if not isinstance(chapters, list) or not 1 <= len(chapters) <= 12:
        errors.append("chapters 必须包含 1–12 个章节。")
        chapters = []

    media_paths: list[tuple[str, str, set[str] | None]] = []
    background = data.get("background")
    if background:
        if isinstance(background, str) and background.startswith("preset:"):
            preset = background.removeprefix("preset:")
            if preset not in PRESET_BACKGROUNDS:
                errors.append(f"未知背景预设：{preset}。可选：{', '.join(sorted(PRESET_BACKGROUNDS))}")
            else:
                preset_path = Path(__file__).resolve().parent.parent / "assets" / "backgrounds" / PRESET_BACKGROUNDS[preset]
                media_paths.append(("background", str(preset_path), IMAGE_SUFFIXES))
        else:
            media_paths.append(("background", background, IMAGE_SUFFIXES))
    background_meta = data.get("backgroundMeta")
    if background_meta:
        if not isinstance(background_meta, dict):
            errors.append("backgroundMeta 必须是对象。")
        elif background_meta.get("origin") == "public-library":
            for field in ("title", "creator", "license", "licenseUrl", "sourceUrl", "attribution"):
                if not background_meta.get(field):
                    errors.append(f"公开背景缺少 backgroundMeta.{field}。")
    music = data.get("music")
    if music:
        if not isinstance(music, dict) or not music.get("src"):
            errors.append("music 必须是包含 src 的对象。")
        else:
            media_paths.append(("music.src", music["src"], AUDIO_SUFFIXES))
            origin = music.get("origin")
            if origin not in {"user-provided", "public-library"}:
                errors.append("music.origin 必须是 user-provided 或 public-library。")
            if origin == "public-library":
                for field in ("title", "creator", "license", "licenseUrl", "sourceUrl", "attribution"):
                    if not music.get(field):
                        errors.append(f"公开音乐缺少 music.{field}。")

    media_count = 0
    for chapter_index, chapter in enumerate(chapters, start=1):
        prefix = f"chapters[{chapter_index - 1}]"
        if not isinstance(chapter, dict):
            errors.append(f"{prefix} 必须是对象。")
            continue
        if not chapter.get("title"):
            errors.append(f"{prefix}.title 不能为空。")
        if not chapter.get("text"):
            warnings.append(f"{prefix}.text 为空；请确认是否有意只展示媒体。")
        media = chapter.get("media", [])
        if not isinstance(media, list):
            errors.append(f"{prefix}.media 必须是数组。")
            continue
        for media_index, item in enumerate(media):
            item_prefix = f"{prefix}.media[{media_index}]"
            if not isinstance(item, dict) or not item.get("src"):
                errors.append(f"{item_prefix} 必须是包含 src 的对象。")
                continue
            media_count += 1
            media_paths.append((f"{item_prefix}.src", item["src"], IMAGE_SUFFIXES | VIDEO_SUFFIXES))
            suffix = Path(item["src"]).suffix.lower()
            if suffix in IMAGE_SUFFIXES and "alt" not in item:
                warnings.append(f"{item_prefix} 缺少 alt 描述。")
            motion = item.get("motion", "none")
            if motion not in PHOTO_MOTIONS:
                errors.append(f"{item_prefix}.motion 无效：{motion}。")
            elif suffix in VIDEO_SUFFIXES and motion != "none":
                warnings.append(f"{item_prefix}.motion 只对静态照片生效。")
            crop_scale = item.get("cropScale", 1)
            if isinstance(crop_scale, bool) or not isinstance(crop_scale, (int, float)) or not 1 <= crop_scale <= 2.5:
                errors.append(f"{item_prefix}.cropScale 必须是 1–2.5 之间的数字。")
            crop_y = item.get("cropY", "0%")
            if not isinstance(crop_y, str) or not re.fullmatch(r"-?(?:\d+(?:\.\d+)?|\.\d+)%", crop_y):
                errors.append(f"{item_prefix}.cropY 必须是百分比字符串，例如 -8% 或 5%。")
            else:
                crop_y_value = float(crop_y.removesuffix("%"))
                if not -50 <= crop_y_value <= 50:
                    errors.append(f"{item_prefix}.cropY 必须在 -50% 到 50% 之间。")
            duration = item.get("duration", 6.5)
            if isinstance(duration, bool) or not isinstance(duration, (int, float)) or not 2 <= duration <= 30:
                errors.append(f"{item_prefix}.duration 必须是 2–30 之间的秒数。")

    if media_count == 0:
        warnings.append("展览没有章节媒体。")

    root = manifest_path.parent
    seen: set[Path] = set()
    for field, raw_path, expected_suffixes in media_paths:
        if not isinstance(raw_path, str) or raw_path.startswith(("data:", "http://", "https://")):
            if isinstance(raw_path, str) and raw_path.startswith(("http://", "https://")):
                errors.append(f"{field} 使用了网络地址；离线产物只接受本地文件。")
            continue
        resolved = (root / raw_path).resolve()
        if resolved.suffix.lower() not in MEDIA_SUFFIXES:
            warnings.append(f"{field} 的格式可能不受支持：{resolved.suffix or '无扩展名'}")
        elif expected_suffixes is not None and resolved.suffix.lower() not in expected_suffixes:
            expected = "、".join(sorted(suffix.lstrip(".").upper() for suffix in expected_suffixes))
            errors.append(f"{field} 的文件类型不合适；此处接受：{expected}。")
        if not resolved.is_file():
            errors.append(f"{field} 找不到文件：{raw_path}")
        elif resolved not in seen:
            total_bytes += resolved.stat().st_size
            seen.add(resolved)

    if total_bytes > 100 * 1024 * 1024:
        warnings.append("素材超过 100 MB；生成后的 HTML 会更大，建议先压缩视频。")
    elif total_bytes > 25 * 1024 * 1024:
        warnings.append("素材超过 25 MB；部分聊天工具或邮箱可能无法发送生成文件。")

    return errors, warnings, total_bytes


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    args = parser.parse_args()

    try:
        manifest = load_manifest(args.manifest)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    errors, warnings, total_bytes = validate_manifest(manifest, args.manifest.resolve())
    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    print(f"素材体积：{total_bytes / 1024 / 1024:.1f} MB")
    if errors:
        print(f"校验失败：{len(errors)} 个错误，{len(warnings)} 个提醒。", file=sys.stderr)
        return 1
    print(f"校验通过：{len(warnings)} 个提醒。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
