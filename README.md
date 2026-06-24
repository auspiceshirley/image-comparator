# Image Comparator

A command-line tool for detecting whether **two images are the same content** (especially suitable for determining images that have undergone platform compression or minor editing).

This tool uses **Perceptual Hashing** technology to overcome the problem that traditional hashes completely fail after image compression, making it ideal for verifying whether images on platforms like X/Twitter, WeChat, Weibo, etc. are from the same source.

## Features

- Supports cross-validation with 4 common perceptual hash methods (Average Hash, pHash, dHash, wHash)
- Automatically calculates SHA256 for comparison
- Outputs basic image information (size, format, etc.)
- Clear final conclusion and explanation
- Simple and easy to use, supports command-line arguments

## Installation and Usage

```bash
# 1. Clone this repository
# 2. Use uv to create a virtual environment and install dependencies
uv venv
uv pip install -r requirements.txt
```

### Usage

```bash
uv run main.py "path/to/image1" "path/to/image2"
```

## Principle Overview

- **Traditional Hash**: If the file binary differs, the hash is completely different and cannot handle compression.
- **Perceptual Hash**: Simulates human visual perception, extracts structural features of the image. Even if the image is compressed, slightly cropped, or re-encoded, the hash values will still be very close.
- **Hamming Distance**: Used to measure the difference between two hash values. The smaller the distance, the more similar the image content (0 means almost identical).

## Notes

- Applicable to common formats such as JPEG, PNG
- Minor cropping, watermark removal, and platform compression have minimal impact on results
- This tool is for reference only; final judgment should be combined with visual observation and other evidence such as timelines

## Use Cases

- Verify whether social platform images have been copied/reused
- Content creators protect original evidence
- Learning and testing image similarity technology