#!/usr/bin/env python3
"""Convert a user-provided or downloaded BGM track to a compact browser-safe MP3."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", "-o", required=True, type=Path)
    parser.add_argument("--bitrate", default="160k")
    args = parser.parse_args()

    if not shutil.which("ffmpeg"):
        print("ERROR: 需要安装 ffmpeg 才能准备背景音乐。", file=sys.stderr)
        return 1
    if not args.input.is_file():
        print(f"ERROR: 找不到音频：{args.input}", file=sys.stderr)
        return 1
    if args.output.suffix.lower() != ".mp3":
        print("ERROR: 输出文件必须使用 .mp3 扩展名。", file=sys.stderr)
        return 1
    if args.input.resolve() == args.output.resolve():
        print("ERROR: 输入和输出不能是同一个文件。", file=sys.stderr)
        return 1

    args.output.parent.mkdir(parents=True, exist_ok=True)
    command = [
        "ffmpeg", "-v", "error", "-y", "-i", str(args.input), "-vn",
        "-af", "loudnorm=I=-23:LRA=7:TP=-2",
        "-c:a", "libmp3lame", "-b:a", args.bitrate, "-ar", "44100",
        str(args.output),
    ]
    try:
        subprocess.run(command, check=True, capture_output=True)
    except subprocess.CalledProcessError as exc:
        detail = exc.stderr.decode("utf-8", errors="replace").strip()
        print(f"ERROR: 音频处理失败：{detail or exc}", file=sys.stderr)
        return 1

    size_mb = args.output.stat().st_size / 1024 / 1024
    print(f"已生成背景音乐：{args.output.resolve()}")
    print(f"格式：MP3 / 44.1 kHz / {args.bitrate}；体积：{size_mb:.1f} MB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
