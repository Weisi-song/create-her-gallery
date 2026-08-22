#!/usr/bin/env python3
"""Export cartoon stills and prompts, or check returned image-to-video clips."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path


IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp", ".avif"}
ID_PATTERN = re.compile(r"[a-zA-Z0-9][a-zA-Z0-9_-]*")


def load_jobs(path: Path) -> tuple[dict, list[dict]]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"无法读取任务清单：{exc}") from exc
    items = data.get("items") if isinstance(data, dict) else None
    if not isinstance(items, list) or not items:
        raise ValueError("items 必须是非空数组。")
    seen: set[str] = set()
    for index, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"第 {index} 项必须是对象。")
        item_id = item.get("id")
        if not isinstance(item_id, str) or not ID_PATTERN.fullmatch(item_id):
            raise ValueError(f"第 {index} 项 id 无效；只使用字母、数字、下划线或连字符。")
        if item_id in seen:
            raise ValueError(f"id 重复：{item_id}")
        if not isinstance(item.get("prompt"), str) or not item["prompt"].strip():
            raise ValueError(f"{item_id} 缺少 prompt。")
        seen.add(item_id)
    return data, items


def prepare(jobs_path: Path, output: Path) -> int:
    data, items = load_jobs(jobs_path)
    if output.exists() and any(output.iterdir()):
        raise ValueError(f"输出目录不是空目录：{output}")
    output.mkdir(parents=True, exist_ok=True)
    package_items: list[dict] = []
    sections = [
        "# 图生视频任务包",
        "",
        "逐张上传卡通图片，粘贴对应提示词，并按指定文件名返回 MP4。不要上传原始照片。",
        "",
        f"统一画风：{data.get('style', '沿用已确认的卡通画风')}",
        f"目标时长：{data.get('duration', 3)} 秒",
        f"共同限制：{data.get('sharedConstraints', '保持人物、构图与背景稳定；不要添加文字或水印。')}",
    ]
    for item in items:
        source = (jobs_path.parent / item.get("cartoon", "")).resolve()
        if source.suffix.lower() not in IMAGE_SUFFIXES or not source.is_file():
            raise ValueError(f"{item['id']} 找不到受支持的卡通图片：{item.get('cartoon', '')}")
        image_name = f"{item['id']}{source.suffix.lower()}"
        return_name = f"{item['id']}.mp4"
        shutil.copy2(source, output / image_name)
        package_items.append({
            "id": item["id"],
            "image": image_name,
            "returnAs": return_name,
            "prompt": item["prompt"].strip(),
        })
        sections.extend([
            "",
            f"## {item['id']}",
            "",
            f"- 上传图片：`{image_name}`",
            f"- 返回文件名：`{return_name}`",
            f"- 提示词：{item['prompt'].strip()}",
        ])
    safe_manifest = {
        "duration": data.get("duration", 3),
        "style": data.get("style", ""),
        "sharedConstraints": data.get("sharedConstraints", ""),
        "items": package_items,
    }
    (output / "handoff.json").write_text(
        json.dumps(safe_manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (output / "prompts.md").write_text("\n".join(sections) + "\n", encoding="utf-8")
    print(f"已导出 {len(items)} 个任务：{output.resolve()}")
    print("外发包不含原始照片或本地 original 路径。")
    return 0


def probe_duration(path: Path) -> float:
    if not shutil.which("ffprobe"):
        raise ValueError("需要 ffprobe 检查返回视频。")
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(path)],
        check=False, capture_output=True, text=True,
    )
    try:
        return float(result.stdout.strip())
    except ValueError as exc:
        raise ValueError(f"无法读取视频：{path.name}") from exc


def check(jobs_path: Path, returned_dir: Path) -> int:
    _, items = load_jobs(jobs_path)
    errors = 0
    for item in items:
        video = returned_dir / f"{item['id']}.mp4"
        if not video.is_file():
            print(f"ERROR: 缺少 {video.name}", file=sys.stderr)
            errors += 1
            continue
        try:
            duration = probe_duration(video)
        except ValueError as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            errors += 1
            continue
        if duration < 2.9:
            print(f"ERROR: {video.name} 只有 {duration:.2f} 秒，无法截取完整三秒。", file=sys.stderr)
            errors += 1
        else:
            note = "；请选择稳定的三秒片段" if duration > 3.2 else ""
            print(f"OK: {video.name} · {duration:.2f} 秒{note}")
    if errors:
        print(f"检查失败：{errors} 个问题。", file=sys.stderr)
        return 1
    print(f"检查通过：{len(items)} 个视频均已返回；下一步进行人工审片和上下合成。")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    prepare_parser = subparsers.add_parser("prepare", help="导出卡通图与逐张提示词")
    prepare_parser.add_argument("jobs", type=Path)
    prepare_parser.add_argument("--output", required=True, type=Path)
    check_parser = subparsers.add_parser("check", help="检查用户返回的 MP4")
    check_parser.add_argument("jobs", type=Path)
    check_parser.add_argument("--returned-dir", required=True, type=Path)
    args = parser.parse_args()
    try:
        if args.command == "prepare":
            return prepare(args.jobs.resolve(), args.output.resolve())
        return check(args.jobs.resolve(), args.returned_dir.resolve())
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
