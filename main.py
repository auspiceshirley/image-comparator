#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import hashlib
from pathlib import Path
from PIL import Image, UnidentifiedImageError
import imagehash


def get_sha256(file_path):
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def get_image_info(img_path):
    try:
        with Image.open(img_path) as img:
            return {
                "size": img.size,
                "mode": img.mode,
                "format": img.format,
                "width": img.width,
                "height": img.height,
            }
    except Exception as e:
        return {"error": str(e)}


def compare_two_images(img1_path, img2_path):
    print("=" * 70)
    print("Image Perceptual Hash Comparison Tool")
    print("=" * 70)

    paths = [Path(img1_path), Path(img2_path)]

    for i, p in enumerate(paths, 1):
        if not p.exists():
            print(f"Error: Image {i} does not exist → {p}")
            return

    print(f"\nImage 1: {paths[0].name}")
    print(f"Path: {paths[0]}")
    info1 = get_image_info(paths[0])
    if "error" not in info1:
        print(
            f"Size: {info1['size'][0]}x{info1['size'][1]} | Format: {info1['format']} | Mode: {info1['mode']}"
        )
    print(f"SHA256: {get_sha256(paths[0])}")

    print(f"\nImage 2: {paths[1].name}")
    print(f"Path: {paths[1]}")
    info2 = get_image_info(paths[1])
    if "error" not in info2:
        print(
            f"Size: {info2['size'][0]}x{info2['size'][1]} | Format: {info2['format']} | Mode: {info2['mode']}"
        )
    print(f"SHA256: {get_sha256(paths[1])}")

    print("\n" + "-" * 70)
    print("Computing perceptual hashes...")
    print("-" * 70)

    try:
        img1 = Image.open(paths[0])
        img2 = Image.open(paths[1])
    except UnidentifiedImageError:
        print(
            "Error: Cannot identify image format. Please confirm it is a valid image file."
        )
        return
    except Exception as e:
        print(f"Failed to open image: {e}")
        return

    hash_methods = {
        "Average Hash": imagehash.average_hash,
        "Perceptual Hash (pHash)": imagehash.phash,
        "Difference Hash (dHash)": imagehash.dhash,
        "Wavelet Hash (wHash)": imagehash.whash,
    }

    results = []

    for name, func in hash_methods.items():
        try:
            h1 = func(img1)
            h2 = func(img2)
            distance = h1 - h2
            results.append((name, str(h1), str(h2), distance))

            status = "Identical" if distance == 0 else f"Distance {distance}"
            print(f"{name:25} | Distance: {distance:3d}  | {status}")
        except Exception as e:
            print(f"{name:25} | Calculation failed: {e}")

    print("\n" + "=" * 70)
    print("Final Conclusion")

    zero_count = sum(1 for r in results if r[3] == 0)
    low_count = sum(1 for r in results if 0 < r[3] <= 5)

    if zero_count >= 3:
        print(
            "Very high probability it is the same image (only compression or slight encoding adjustments)"
        )
    elif zero_count >= 2 or low_count >= 3:
        print("Highly similar, very likely different versions of the same image")
    elif low_count >= 2:
        print("Possibly the same image, but with slight differences")
    else:
        print("Significant difference in image content, not the same image")

    print("=" * 70)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Image Comparator")
    parser.add_argument("image1", help="Path to the first image")
    parser.add_argument("image2", help="Path to the second image")

    args = parser.parse_args()
    compare_two_images(args.image1, args.image2)
