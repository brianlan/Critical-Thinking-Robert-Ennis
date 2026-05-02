import argparse
import dataclasses
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from loguru import logger

from scripts.bilingual_export.align import build_aligned_document, AlignedRow, AlignedDocument


def parent_ensured_path(path: str | Path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    return Path(path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="desc")
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path(__file__).resolve().parents[2],
        help="Repository root containing FullText-en and FullText-zh-sense.",
    )
    parser.add_argument("--chapter-filename", type=str, help="file name of the chapter to be optimized.")
    parser.add_argument("-o", "--output", type=parent_ensured_path, help="Optimized Chinese translation output path.")
    parser.add_argument("--num-workers", type=int, default=0)
    parser.add_argument("-v", "--verbose", action="store_true", help="Show detailed progress")

    return parser.parse_args()


def optimize_row(row: AlignedRow) -> AlignedRow:
    prompt = f"英文原文：{row.english_block} 现有翻译：{row.chinese_block}"
    result = subprocess.run(
        ["opencode", "run", "--agent", "snippet-translation-coordinator", prompt],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        logger.error("opencode failed: {}", result.stderr.strip())
        return row

    match = re.search(r"<translation>(.*?)</translation>", result.stdout, re.DOTALL)
    if not match:
        logger.warning("No <translation> tag found in output, keeping original")
        return row

    optimized = match.group(1).strip()
    original = row.chinese_block
    optimized_block = dataclasses.replace(original, content=optimized) if original else None
    return dataclasses.replace(row, chinese_block=optimized_block)


def optimize_doc(doc: AlignedDocument, num_workers: int = 0) -> AlignedDocument:
    rows = [row for section in doc.sections for row in section.rows]

    if num_workers > 0:
        optimized = dict(zip(rows, ThreadPoolExecutor(max_workers=num_workers).map(optimize_row, rows)))
    else:
        optimized = {row: optimize_row(row) for row in rows}

    sections = tuple(
        dataclasses.replace(section, rows=tuple(optimized[row] for row in section.rows)) for section in doc.sections
    )
    return dataclasses.replace(doc, sections=sections)


def build_markdown_content(doc: AlignedDocument, lang="chinese") -> str:
    parts: list[str] = []
    for section in doc.sections:
        for row in section.rows:
            block = row.chinese_block if lang == "chinese" else row.english_block
            if block:
                parts.append(block.content)
    return "\n\n".join(parts) + "\n"


def write_file(content: str, save_path: Path) -> None:
    save_path.parent.mkdir(parents=True, exist_ok=True)
    save_path.write_text(content, encoding="utf-8")


def main(args) -> None:
    doc = build_aligned_document(args.repo_root, args.chapter_filename)
    optimized_doc = optimize_doc(doc, num_workers=args.num_workers)
    chinese_text = build_markdown_content(optimized_doc, lang="chinese")
    write_file(chinese_text, args.output)


if __name__ == "__main__":
    main(parse_args())
