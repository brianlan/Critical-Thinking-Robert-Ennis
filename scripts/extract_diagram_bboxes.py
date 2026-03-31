#!/usr/bin/env python3

import argparse
import json
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont


def gap(a1: int, a2: int, b1: int, b2: int) -> int:
    return max(0, max(a1 - b2, b1 - a2))


def union(boxes: list[list[int]]) -> list[int]:
    return [
        min(box[0] for box in boxes),
        min(box[1] for box in boxes),
        max(box[2] for box in boxes),
        max(box[3] for box in boxes),
    ]


def vertical_overlap_ratio(a: list[int], b: list[int]) -> float:
    overlap = max(0, min(a[3], b[3]) - max(a[1], b[1]))
    return overlap / max(1, min(a[3] - a[1], b[3] - b[1]))


def box_center_y(box: list[int]) -> float:
    return (box[1] + box[3]) / 2.0


def is_horizontal_line(box: list[int]) -> bool:
    return (box[2] - box[0]) >= 200 and (box[3] - box[1]) <= 12


def is_vertical_line(box: list[int]) -> bool:
    return (box[3] - box[1]) >= 200 and (box[2] - box[0]) <= 20


def find_band(row_sums: np.ndarray, y1: int, y2: int, blank_threshold: int, blank_run: int) -> tuple[int, int]:
    top = 0
    run = 0
    for y in range(max(0, y1 - 1), -1, -1):
        if row_sums[y] <= blank_threshold:
            run += 1
            if run >= blank_run:
                top = y + blank_run
                break
        else:
            run = 0

    bottom = len(row_sums) - 1
    run = 0
    for y in range(min(len(row_sums) - 1, y2), len(row_sums)):
        if row_sums[y] <= blank_threshold:
            run += 1
            if run >= blank_run:
                bottom = y - blank_run
                break
        else:
            run = 0

    return top, bottom


def detect_diagram_bboxes(
    image_path: Path,
    threshold: int,
    fill_threshold: float,
    blank_threshold: int,
    blank_run: int,
    label_gap_x: int,
    label_gap_y: int,
    final_pad_x: int,
    final_pad_y: int,
) -> list[list[int]]:
    gray = np.array(Image.open(image_path).convert("L"))
    height, width = gray.shape
    mask = (gray < threshold).astype("uint8")
    row_sums = mask.sum(axis=1)

    component_count, _, stats, _ = cv2.connectedComponentsWithStats(mask, connectivity=8)
    components = []
    for label in range(1, component_count):
        x, y, w, h, area = stats[label]
        if area < 8:
            continue
        components.append(
            {
                "id": label,
                "box": [int(x), int(y), int(x + w), int(y + h)],
                "w": int(w),
                "h": int(h),
                "area": int(area),
                "fill": float(area / (w * h)),
            }
        )

    anchors = []
    for component in components:
        x1, y1, x2, y2 = component["box"]
        w = component["w"]
        h = component["h"]
        long_line = (w >= 200 and h <= 12) or (h >= 200 and w <= 20)

        if w > 0.7 * width and h <= 15 and y1 < 180:
            continue

        if (
            component["fill"] <= fill_threshold
            and (component["area"] >= 80 or w >= 40 or h >= 40)
        ) or long_line:
            anchors.append(component)

    groups = []
    used_anchor_ids = set()
    for anchor in anchors:
        if anchor["id"] in used_anchor_ids:
            continue

        group = [anchor]
        used_anchor_ids.add(anchor["id"])
        changed = True
        while changed:
            changed = False
            group_box = union([item["box"] for item in group])
            for other in anchors:
                if other["id"] in used_anchor_ids:
                    continue
                if (
                    gap(group_box[0], group_box[2], other["box"][0], other["box"][2]) <= 25
                    and gap(group_box[1], group_box[3], other["box"][1], other["box"][3]) <= 25
                ):
                    group.append(other)
                    used_anchor_ids.add(other["id"])
                    changed = True
        groups.append(group)

    candidate_boxes = []
    for group in groups:
        core_box = union([item["box"] for item in group])
        core_w = core_box[2] - core_box[0]
        core_h = core_box[3] - core_box[1]

        if core_w * core_h < 1200 and not (core_h >= 150 or core_w >= 300):
            continue
        if core_h < 80 and core_w > 500 and not (is_horizontal_line(core_box) or is_vertical_line(core_box)):
            continue

        band_top, band_bottom = find_band(row_sums, core_box[1], core_box[3], blank_threshold, blank_run)
        group_ids = {item["id"] for item in group}

        changed = True
        while changed:
            changed = False
            current_box = union([item["box"] for item in group])
            for component in components:
                if component["id"] in group_ids:
                    continue

                box = component["box"]
                if box[3] < band_top or box[1] > band_bottom:
                    continue

                x_gap = gap(current_box[0], current_box[2], box[0], box[2])
                y_gap = gap(current_box[1], current_box[3], box[1], box[3])
                same_row = (
                    vertical_overlap_ratio(current_box, box) >= 0.35
                    or abs(box_center_y(current_box) - box_center_y(box)) <= 35
                )

                if (
                    x_gap <= label_gap_x
                    and y_gap <= label_gap_y
                    and same_row
                ):
                    if component["w"] > 420 and component["h"] < 50:
                        continue
                    group.append(component)
                    group_ids.add(component["id"])
                    changed = True

        candidate_boxes.append(union([item["box"] for item in group]))

    changed = True
    while changed:
        changed = False
        merged_boxes = []
        used = [False] * len(candidate_boxes)
        for index, left in enumerate(candidate_boxes):
            if used[index]:
                continue

            current = left
            used[index] = True

            for other_index, right in enumerate(candidate_boxes[index + 1 :], start=index + 1):
                if used[other_index]:
                    continue

                x_gap = gap(current[0], current[2], right[0], right[2])
                y_gap = gap(current[1], current[3], right[1], right[3])
                should_merge = False

                if vertical_overlap_ratio(current, right) >= 0.55 and x_gap <= 180:
                    should_merge = True
                elif (
                    (is_vertical_line(current) and is_horizontal_line(right))
                    or (is_horizontal_line(current) and is_vertical_line(right))
                ) and x_gap == 0 and y_gap <= 120:
                    should_merge = True

                if should_merge:
                    current = union([current, right])
                    used[other_index] = True
                    changed = True

            merged_boxes.append(current)

        candidate_boxes = merged_boxes

    final_boxes = []
    for box in sorted(candidate_boxes, key=lambda item: (item[1], item[0])):
        w = box[2] - box[0]
        h = box[3] - box[1]
        fill = float(mask[box[1] : box[3], box[0] : box[2]].sum() / max(1, w * h))

        if h < 20 or w < 20:
            continue
        if h < 80 and w > 500:
            continue
        if fill > 0.15 and w > 120 and h < 120:
            continue
        if looks_like_annotated_text_block(mask, box):
            continue

        padded_box = [
            max(0, int(box[0] - final_pad_x)),
            max(0, int(box[1] - final_pad_y)),
            min(width, int(box[2] + final_pad_x)),
            min(height, int(box[3] + final_pad_y)),
        ]

        final_boxes.append(padded_box)

    return final_boxes


def annotate_image(image_path: Path, boxes: list[list[int]], output_path: Path) -> None:
    image = Image.open(image_path).convert("RGB")
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()

    for index, box in enumerate(boxes, start=1):
        x1, y1, x2, y2 = box
        draw.rectangle((x1, y1, x2, y2), outline=(255, 0, 0), width=4)

        label = str(index)
        text_bbox = draw.textbbox((0, 0), label, font=font)
        text_w = text_bbox[2] - text_bbox[0]
        text_h = text_bbox[3] - text_bbox[1]
        label_x = x1
        label_y = max(0, y1 - text_h - 8)
        draw.rectangle((label_x, label_y, label_x + text_w + 10, label_y + text_h + 6), fill=(255, 0, 0))
        draw.text((label_x + 5, label_y + 3), label, fill=(255, 255, 255), font=font)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(output_path)


def looks_like_annotated_text_block(mask: np.ndarray, box: list[int]) -> bool:
    x1, y1, x2, y2 = box
    crop = mask[y1:y2, x1:x2]
    h, w = crop.shape
    if w < 400 or h < 120 or h > 360:
        return False

    fill = float(crop.mean())
    row_frac = crop.mean(axis=1)
    col_frac = crop.mean(axis=0)
    strong_row_ratio = float((row_frac > 0.12).sum() / max(1, h))
    wide_col_ratio = float((col_frac > 0.08).sum() / max(1, w))

    return fill > 0.15 and strong_row_ratio > 0.25 and wide_col_ratio > 0.85


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Extract diagram/graph bounding boxes from scanned page images.")
    parser.add_argument("images", nargs="+", type=Path, help="Page image paths")
    parser.add_argument("--threshold", type=int, default=220, help="Foreground threshold on grayscale image")
    parser.add_argument("--fill-threshold", type=float, default=0.28, help="Max fill ratio for graphic anchors")
    parser.add_argument("--blank-threshold", type=int, default=6, help="Blank-row threshold used for band detection")
    parser.add_argument("--blank-run", type=int, default=10, help="Consecutive blank rows required for a band boundary")
    parser.add_argument("--label-gap-x", type=int, default=420, help="Max horizontal gap when absorbing nearby labels/marks")
    parser.add_argument("--label-gap-y", type=int, default=50, help="Max vertical gap when absorbing nearby labels/marks")
    parser.add_argument("--final-pad-x", type=int, default=0, help="Final horizontal padding added to each detected box")
    parser.add_argument("--final-pad-y", type=int, default=18, help="Final vertical padding added to each detected box")
    parser.add_argument("--annotate-dir", type=Path, help="Directory for saving page images with boxes drawn on top")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of plain text")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    results = {}
    for image_path in args.images:
        boxes = detect_diagram_bboxes(
            image_path=image_path,
            threshold=args.threshold,
            fill_threshold=args.fill_threshold,
            blank_threshold=args.blank_threshold,
            blank_run=args.blank_run,
            label_gap_x=args.label_gap_x,
            label_gap_y=args.label_gap_y,
            final_pad_x=args.final_pad_x,
            final_pad_y=args.final_pad_y,
        )
        results[str(image_path)] = boxes

        if args.annotate_dir:
            annotate_image(image_path, boxes, args.annotate_dir / image_path.name)

    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=True))
        return

    for image_path, boxes in results.items():
        print(image_path)
        for box in boxes:
            print(f"  {box}")


if __name__ == "__main__":
    main()
