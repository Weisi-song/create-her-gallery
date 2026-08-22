#!/usr/bin/env python3
"""Build a self-contained offline Her Gallery HTML from a JSON manifest."""

from __future__ import annotations

import argparse
import base64
import copy
import json
import mimetypes
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from validate_gallery import PRESET_BACKGROUNDS, THEMES, load_manifest, validate_manifest


MIME_OVERRIDES = {
    ".mov": "video/quicktime",
    ".m4a": "audio/mp4",
    ".avif": "image/avif",
}


def prepare_browser_video(file_path: Path, temp_root: Path) -> Path:
    """Remux MOV into MP4, transcoding only when the video codec requires it."""
    if file_path.suffix.lower() != ".mov":
        return file_path
    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        raise RuntimeError("处理 MOV 需要 ffmpeg 和 ffprobe；请先安装后重新生成。")

    probe = subprocess.run(
        [
            "ffprobe", "-v", "error", "-select_streams", "v:0",
            "-show_entries", "stream=codec_name", "-of", "default=nw=1:nk=1",
            str(file_path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    codec = probe.stdout.strip().lower()
    output_path = temp_root / f"{file_path.stem}-{abs(hash(file_path))}.mp4"
    command = [
        "ffmpeg", "-v", "error", "-y", "-i", str(file_path),
        "-map", "0:v:0", "-map", "0:a?",
    ]
    if codec == "h264":
        command += ["-c:v", "copy", "-c:a", "aac"]
    else:
        command += ["-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac"]
    command += ["-movflags", "+faststart", str(output_path)]
    subprocess.run(command, check=True, capture_output=True)
    return output_path


def file_to_data_url(file_path: Path, temp_root: Path) -> str:
    file_path = prepare_browser_video(file_path, temp_root)
    mime = MIME_OVERRIDES.get(file_path.suffix.lower())
    if not mime:
        mime = mimetypes.guess_type(file_path.name)[0] or "application/octet-stream"
    encoded = base64.b64encode(file_path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def embed_media(data: dict, manifest_path: Path, temp_root: Path) -> dict:
    embedded = copy.deepcopy(data)
    root = manifest_path.parent

    cache: dict[Path, str] = {}

    def replace(raw_path: str) -> str:
        if raw_path.startswith("data:"):
            return raw_path
        if raw_path.startswith("preset:"):
            preset = raw_path.removeprefix("preset:")
            resolved = Path(__file__).resolve().parent.parent / "assets" / "backgrounds" / PRESET_BACKGROUNDS[preset]
        else:
            resolved = (root / raw_path).resolve()
        if resolved not in cache:
            cache[resolved] = file_to_data_url(resolved, temp_root)
        return cache[resolved]

    if embedded.get("background"):
        embedded["background"] = replace(embedded["background"])
    if embedded.get("music", {}).get("src"):
        embedded["music"]["src"] = replace(embedded["music"]["src"])
    for chapter in embedded.get("chapters", []):
        for item in chapter.get("media", []):
            item["src"] = replace(item["src"])
    return embedded


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", nargs="?", type=Path)
    parser.add_argument("--output", "-o", type=Path)
    parser.add_argument("--list-themes", action="store_true")
    parser.add_argument("--list-backgrounds", action="store_true")
    args = parser.parse_args()

    if args.list_themes:
        print("\n".join(sorted(THEMES)))
        return 0
    if args.list_backgrounds:
        print("\n".join(sorted(PRESET_BACKGROUNDS)))
        return 0
    if not args.manifest:
        parser.error("manifest is required unless a list option is used")

    manifest_path = args.manifest.resolve()
    try:
        data = load_manifest(manifest_path)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    errors, warnings, total_bytes = validate_manifest(data, manifest_path)
    for warning in warnings:
        print(f"WARNING: {warning}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    template_names = {
        "classic-card": "classic.html",
        "romantic-stage": "romantic.html",
        "editorial-scroll": "index.html",
    }
    template_name = template_names[data.get("layout", "classic-card")]
    template_path = Path(__file__).resolve().parent.parent / "assets" / "gallery-template" / template_name
    template = template_path.read_text(encoding="utf-8")
    try:
        with tempfile.TemporaryDirectory(prefix="her-gallery-") as temp_dir:
            embedded = embed_media(data, manifest_path, Path(temp_dir))
            payload = json.dumps(embedded, ensure_ascii=False, separators=(",", ":"))
            payload = payload.replace("</script", "<\\/script")
            html = template.replace("__GALLERY_DATA__", payload)
    except (RuntimeError, subprocess.CalledProcessError) as exc:
        print(f"ERROR: 媒体转换失败：{exc}", file=sys.stderr)
        return 1
    if "__GALLERY_DATA__" in html:
        print("ERROR: 模板数据占位符没有被完整替换。", file=sys.stderr)
        return 1

    output_path = args.output or Path(f"{data['slug']}.html")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")
    output_mb = output_path.stat().st_size / 1024 / 1024
    print(f"已生成：{output_path.resolve()}")
    print(f"素材：{total_bytes / 1024 / 1024:.1f} MB；HTML：{output_mb:.1f} MB")
    if output_mb > 100:
        print("WARNING: HTML 超过 100 MB；建议在征得用户同意后压缩视频，再重新生成。")
    elif output_mb > 25:
        print("WARNING: HTML 超过 25 MB；部分聊天工具或邮箱可能无法发送。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
