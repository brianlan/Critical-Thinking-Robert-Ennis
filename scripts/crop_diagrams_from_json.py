#!/usr/bin/env python3

import argparse
import json
import re
from pathlib import Path

from PIL import Image


PAGE_RE = re.compile(r"page_(\d+)")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate diagram crops from a JSON bbox file.")
    parser.add_argument("json_file", type=Path, help="Path to the JSON file produced by extract_diagram_bboxes.py")
    parser.add_argument("output_dir", type=Path, help="Directory where cropped images will be saved")
    return parser.parse_args()


def extract_page_num(image_path: Path) -> str:
    match = PAGE_RE.search(image_path.stem)
    if not match:
        raise ValueError(f"Could not extract page number from image path: {image_path}")
    return match.group(1)


def resolve_image_path(raw_path: str, json_file: Path) -> Path:
    image_path = Path(raw_path)
    if image_path.is_absolute() and image_path.exists():
        return image_path
    if image_path.exists():
        return image_path

    candidate = json_file.parent / image_path
    if candidate.exists():
        return candidate

    raise FileNotFoundError(f"Image path from JSON does not exist: {raw_path}")


def normalize_box(box: list[int], width: int, height: int) -> tuple[int, int, int, int]:
    if len(box) != 4:
        raise ValueError(f"Expected bbox with 4 integers, got: {box}")

    x1, y1, x2, y2 = [int(value) for value in box]
    x1 = max(0, min(width, x1))
    y1 = max(0, min(height, y1))
    x2 = max(0, min(width, x2))
    y2 = max(0, min(height, y2))

    if x2 <= x1 or y2 <= y1:
        raise ValueError(f"Invalid bbox after clamping: {[x1, y1, x2, y2]}")

    return x1, y1, x2, y2


def main() -> None:
    args = parse_args()
    data = json.loads(args.json_file.read_text(encoding="utf-8"))

    if not isinstance(data, dict):
        raise ValueError("JSON root must be an object mapping image paths to bbox lists")

    for raw_image_path, boxes in data.items():
        image_path = resolve_image_path(raw_image_path, args.json_file)
        page_num = extract_page_num(image_path)
        page_dir = args.output_dir / f"page_{page_num}"
        page_dir.mkdir(parents=True, exist_ok=True)

        with Image.open(image_path) as image:
            width, height = image.size

            for diagram_id, box in enumerate(boxes, start=1):
                x1, y1, x2, y2 = normalize_box(box, width, height)
                crop = image.crop((x1, y1, x2, y2))
                output_path = page_dir / (
                    f"page_{page_num}_diagram_{diagram_id}_loc_{x1}_{y1}_{x2}_{y2}.png"
                )
                crop.save(output_path)
                print(output_path)


if __name__ == "__main__":
    main()
