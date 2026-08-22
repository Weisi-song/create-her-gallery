#!/usr/bin/env python3
"""Stack an original photo above its cartoon animation in a 3-second MP4."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def even_positive(value: str) -> int:
    number = int(value)
    if number <= 0 or number % 2:
        raise argparse.ArgumentTypeError("尺寸必须是大于 0 的偶数。")
    return number


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("original", type=Path, help="原始照片")
    parser.add_argument("animation", type=Path, help="卡通化后的短动画")
    parser.add_argument("--output", "-o", required=True, type=Path, help="合成 MP4")
    parser.add_argument("--width", type=even_positive, default=720)
    parser.add_argument("--height", type=even_positive, default=1080)
    parser.add_argument("--duration", type=float, default=3.0)
    parser.add_argument("--animation-start", type=float, default=0.0, help="卡通动画的起始秒数")
    parser.add_argument("--fit", choices=("contain", "cover"), default="contain", help="完整留边或裁切铺满")
    parser.add_argument("--focus-y", type=float, default=0.0, help="cover 裁切焦点：-50 顶部，0 中间，50 底部")
    parser.add_argument("--background", default="0x20332d", help="留白填充色，使用 FFmpeg 颜色格式")
    args = parser.parse_args()

    if not shutil.which("ffmpeg"):
        print("ERROR: 需要安装 ffmpeg 才能合成上下画面。", file=sys.stderr)
        return 1
    if not args.original.is_file():
        print(f"ERROR: 找不到原图：{args.original}", file=sys.stderr)
        return 1
    if not args.animation.is_file():
        print(f"ERROR: 找不到卡通动画：{args.animation}", file=sys.stderr)
        return 1
    if not 0.5 <= args.duration <= 30:
        print("ERROR: duration 必须在 0.5–30 秒之间。", file=sys.stderr)
        return 1
    if args.animation_start < 0:
        print("ERROR: animation-start 不能小于 0。", file=sys.stderr)
        return 1
    if not -50 <= args.focus_y <= 50:
        print("ERROR: focus-y 必须在 -50 到 50 之间。", file=sys.stderr)
        return 1

    panel_height = args.height // 2
    if args.fit == "cover":
        focus_ratio = (args.focus_y + 50) / 100
        fit = (
            f"scale={args.width}:{panel_height}:force_original_aspect_ratio=increase,"
            f"crop={args.width}:{panel_height}:(iw-ow)/2:(ih-oh)*{focus_ratio:.4f},setsar=1"
        )
    else:
        fit = (
            f"scale={args.width}:{panel_height}:force_original_aspect_ratio=decrease,"
            f"pad={args.width}:{panel_height}:(ow-iw)/2:(oh-ih)/2:color={args.background},"
            "setsar=1"
        )
    filter_graph = f"[0:v]{fit}[top];[1:v]{fit}[bottom];[top][bottom]vstack=inputs=2,format=yuv420p[out]"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    command = [
        "ffmpeg", "-v", "error", "-y",
        "-loop", "1", "-framerate", "30", "-i", str(args.original),
        "-stream_loop", "-1", "-ss", str(args.animation_start), "-i", str(args.animation),
        "-filter_complex", filter_graph,
        "-map", "[out]", "-an", "-t", str(args.duration), "-r", "30",
        "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-movflags", "+faststart", str(args.output),
    ]
    try:
        subprocess.run(command, check=True, capture_output=True)
    except subprocess.CalledProcessError as exc:
        detail = exc.stderr.decode("utf-8", errors="replace").strip()
        print(f"ERROR: 合成失败：{detail or exc}", file=sys.stderr)
        return 1

    print(f"已生成上下对照动画：{args.output.resolve()}")
    print(f"画面：{args.width}×{args.height}；时长：{args.duration:.1f} 秒；适配：{args.fit}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
