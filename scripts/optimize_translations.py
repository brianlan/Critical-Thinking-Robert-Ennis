import argparse
import dataclasses
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from loguru import logger

from scripts.bilingual_export.align import build_aligned_document, AlignedRow, AlignedDocument, AlignedSection


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
    parser.add_argument("--startover", action="store_true", default=False)

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


def count_written_sections(output: Path) -> int:
    """Count how many sections have been written by counting top-level headings."""
    if not output.exists():
        return 0
    return sum(1 for line in open(output, encoding="utf-8") if line.startswith("# "))


def build_section_markdown(section: AlignedSection, lang="chinese") -> str:
    parts = [row.chinese_block.content for row in section.rows if row.chinese_block] if lang == "chinese" \
        else [row.english_block.content for row in section.rows if row.english_block]
    return "\n\n".join(parts) + "\n\n" if parts else ""


def optimize_doc(doc: AlignedDocument, output: Path, num_workers: int = 0, lang="chinese") -> None:
    n_done = count_written_sections(output)
    with open(output, "a", encoding="utf-8") as f:
        for section in doc.sections:
            if section.index < n_done:
                continue
            logger.info("Section {}/{}: {}", section.index + 1, len(doc.sections), section.anchor)

            rows = list(section.rows)
            if num_workers > 0:
                optimized = dict(zip(rows, ThreadPoolExecutor(max_workers=num_workers).map(optimize_row, rows)))
            else:
                optimized = {row: optimize_row(row) for row in rows}

            optimized_section = dataclasses.replace(section, rows=tuple(optimized[row] for row in section.rows))
            f.write(build_section_markdown(optimized_section, lang))
            f.flush()


def main(args) -> None:
    if args.startover and args.output.exists():
        args.output.unlink()

    doc = build_aligned_document(args.repo_root, args.chapter_filename)
    optimize_doc(doc, output=args.output, num_workers=args.num_workers)


if __name__ == "__main__":
    main(parse_args())
