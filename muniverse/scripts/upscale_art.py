#!/usr/bin/env python3
from __future__ import annotations

"""Upscale card art using Real-ESRGAN.

Reads raw images from assets/art/raw/, upscales each 4x using
realesrgan-ncnn-vulkan, and writes the results to assets/art/.

Requires: realesrgan-ncnn-vulkan binary in PATH.
  Download from https://github.com/xinntao/Real-ESRGAN-ncnn-vulkan/releases

Usage:
    python scripts/upscale_art.py              # upscale all raw images
    python scripts/upscale_art.py --ids hp-001  # upscale specific card(s)
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "assets" / "art" / "raw"
ART_DIR = BASE_DIR / "assets" / "art"

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}


def find_raw_images(ids: list[str] | None = None) -> list[Path]:
    """Find raw images to upscale, optionally filtered by card IDs."""
    images = []
    for path in sorted(RAW_DIR.iterdir()):
        if path.suffix.lower() not in IMAGE_EXTENSIONS:
            continue
        if ids and path.stem not in ids:
            continue
        images.append(path)
    return images


def get_dimensions(path: Path) -> tuple[int, int]:
    with Image.open(path) as img:
        return img.size


def find_binary() -> str | None:
    """Find realesrgan-ncnn-vulkan in PATH."""
    return shutil.which("realesrgan-ncnn-vulkan")


def run_upscale(binary: str, input_path: Path, output_path: Path) -> bool:
    """Run Real-ESRGAN 4x upscale. Returns True on success."""
    # Models dir is alongside the binary
    models_dir = Path(binary).parent / "models"
    cmd = [
        binary,
        "-i", str(input_path),
        "-o", str(output_path),
        "-n", "realesrgan-x4plus",
        "-s", "4",
    ]
    if models_dir.exists():
        cmd += ["-m", str(models_dir)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0


def main():
    parser = argparse.ArgumentParser(
        description="Upscale raw card art with Real-ESRGAN (4x)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--ids",
        nargs="*",
        help="Card IDs to upscale (default: all images in raw/)",
    )
    args = parser.parse_args()

    # Check binary
    binary = find_binary()
    if not binary:
        print("Error: realesrgan-ncnn-vulkan not found in PATH.\n")
        print("Install it:")
        print("  https://github.com/xinntao/Real-ESRGAN-ncnn-vulkan/releases")
        sys.exit(1)

    # Check raw dir exists
    if not RAW_DIR.exists():
        print(f"Error: raw image directory not found: {RAW_DIR}")
        print("Save downloaded art images there before running this script.")
        sys.exit(1)

    images = find_raw_images(args.ids)

    if not images:
        print("No images found in raw/ to upscale.")
        return

    print(f"Found {len(images)} image(s) to upscale:\n")
    for img in images:
        w, h = get_dimensions(img)
        print(f"  {img.name}: {w}×{h}px")

    print()

    upscaled = 0
    failed = 0
    for raw_path in images:
        out_path = ART_DIR / f"{raw_path.stem}.png"
        w, h = get_dimensions(raw_path)

        print(f"  {raw_path.name} (4x)...", end=" ", flush=True)

        if run_upscale(binary, raw_path, out_path):
            new_w, new_h = get_dimensions(out_path)
            print(f"{w}×{h} → {new_w}×{new_h}px → {out_path.name} ✓")
            upscaled += 1
        else:
            out_path.unlink(missing_ok=True)
            print("failed ✗")
            failed += 1

    print(f"\nUpscaled {upscaled}/{len(images)} image(s) to {ART_DIR.relative_to(BASE_DIR)}/")
    if failed > 0:
        print(f"{failed} failed.")


if __name__ == "__main__":
    main()
