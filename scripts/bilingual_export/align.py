#!/usr/bin/env python3

import argparse
import re
from dataclasses import asdict, dataclass
from pathlib import Path

from scripts.bilingual_export.discovery import HEADING_RE, build_pair_manifest, is_table_line


PREAMBLE_ANCHOR = "__preamble__"
PARAGRAPH_MARKER_RE = re.compile(r"^(?:\*\*)?(\d+(?::\d+)?(?:[.–-]\d+(?::\d+)?)?|[A-Z])(?:\.|:|\))\b")
EXAMPLE_MARKER_RE = re.compile(r"^\*\*(?:Example|示例)\s+([0-9]+(?::[0-9]+)?)\*\*$")


@dataclass(frozen=True)
class Block:
    index: int
    block_type: str
    source_text: str
    content: str
    section_anchor: str
    section_level: int
    line_start: int
    line_end: int
    status: str = "source"


@dataclass(frozen=True)
class SectionBlocks:
    index: int
    anchor: str
    level: int
    blocks: tuple[Block, ...]
    status: str = "source"


@dataclass(frozen=True)
class ParsedDocument:
    path: str
    sections: tuple[SectionBlocks, ...]
    blocks: tuple[Block, ...]


@dataclass(frozen=True)
class AlignedRow:
    section_index: int
    section_anchor: str
    row_index: int
    status: str
    english_block: Block | None
    chinese_block: Block | None
    note: str = ""


@dataclass(frozen=True)
class AlignedSection:
    index: int
    anchor: str
    level: int
    status: str
    english_anchor: str | None
    chinese_anchor: str | None
    rows: tuple[AlignedRow, ...]


@dataclass(frozen=True)
class AlignedDocument:
    english_file: str
    chinese_file: str
    pair_status: str
    status: str
    warnings: tuple[str, ...]
    sections: tuple[AlignedSection, ...]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Parse and align bilingual markdown chapter blocks.")
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path(__file__).resolve().parents[2],
        help="Repository root containing FullText-en and FullText-zh-sense.",
    )
    parser.add_argument("--chapter", required=True, help="English markdown filename to align.")
    parser.add_argument("--report-output", type=Path, help="Write a plain-text alignment report.")
    return parser.parse_args()


def parse_markdown(path: Path) -> ParsedDocument:
    lines = path.read_text(encoding="utf-8").splitlines()
    section_anchors: list[str] = [PREAMBLE_ANCHOR]
    section_levels: list[int] = [1]
    section_blocks: list[list[Block]] = [[]]
    current_anchor = PREAMBLE_ANCHOR
    current_level = 1
    paragraph_lines: list[str] = []
    paragraph_start = 0
    block_index = 0

    def current_blocks() -> list[Block]:
        return section_blocks[-1]

    def add_block(block_type: str, block_lines: list[str], line_start: int, line_end: int) -> None:
        nonlocal block_index
        source_text = "\n".join(block_lines)
        block = Block(
            index=block_index,
            block_type=block_type,
            source_text=source_text,
            content=source_text.strip(),
            section_anchor=current_anchor,
            section_level=current_level,
            line_start=line_start,
            line_end=line_end,
        )
        current_blocks().append(block)
        block_index += 1

    def flush_paragraph(end_line: int) -> None:
        nonlocal paragraph_lines, paragraph_start
        if not paragraph_lines:
            return
        add_block("paragraph", paragraph_lines, paragraph_start, end_line)
        paragraph_lines = []
        paragraph_start = 0

    line_number = 1
    while line_number <= len(lines):
        line = lines[line_number - 1]
        stripped = line.strip()
        heading_match = HEADING_RE.match(line)

        if heading_match:
            flush_paragraph(line_number - 1)
            level = len(heading_match.group(1))
            anchor = heading_match.group(2)
            if level >= 2:
                current_anchor = anchor
                current_level = level
                section_anchors.append(current_anchor)
                section_levels.append(current_level)
                section_blocks.append([])
            add_block("heading", [line], line_number, line_number)
            line_number += 1
            continue

        if not stripped:
            flush_paragraph(line_number - 1)
            line_number += 1
            continue

        if stripped.startswith("![") and stripped.endswith(")"):
            flush_paragraph(line_number - 1)
            add_block("image", [line], line_number, line_number)
            line_number += 1
            continue

        if is_table_line(stripped):
            flush_paragraph(line_number - 1)
            table_lines = [line]
            table_start = line_number
            line_number += 1
            while line_number <= len(lines) and is_table_line(lines[line_number - 1].strip()):
                table_lines.append(lines[line_number - 1])
                line_number += 1
            add_block("table", table_lines, table_start, line_number - 1)
            continue

        if not paragraph_lines:
            paragraph_start = line_number
        paragraph_lines.append(line)
        line_number += 1

    flush_paragraph(len(lines))

    built_sections = tuple(
        SectionBlocks(
            index=index,
            anchor=section_anchors[index],
            level=section_levels[index],
            blocks=tuple(section_blocks[index]),
        )
        for index in range(len(section_anchors))
    )
    all_blocks = tuple(block for section in built_sections for block in section.blocks)
    return ParsedDocument(path=str(path), sections=built_sections, blocks=all_blocks)


def build_aligned_document(repo_root: Path, english_filename: str) -> AlignedDocument:
    pair = next((item for item in build_pair_manifest(repo_root) if item.english_file == english_filename), None)
    if pair is None:
        raise KeyError(f"Unknown chapter: {english_filename}")

    english_doc = parse_markdown(Path(pair.english.path))
    chinese_doc = parse_markdown(Path(pair.chinese.path))
    aligned_sections = align_sections(english_doc.sections, chinese_doc.sections)
    document_status = summarize_document_status(pair.status, aligned_sections)
    return AlignedDocument(
        english_file=pair.english_file,
        chinese_file=pair.chinese_file,
        pair_status=pair.status,
        status=document_status,
        warnings=pair.warnings,
        sections=aligned_sections,
    )


def align_sections(
    english_sections: tuple[SectionBlocks, ...],
    chinese_sections: tuple[SectionBlocks, ...],
) -> tuple[AlignedSection, ...]:
    sections: list[AlignedSection] = []
    limit = max(len(english_sections), len(chinese_sections))
    for index in range(limit):
        english_section = english_sections[index] if index < len(english_sections) else None
        chinese_section = chinese_sections[index] if index < len(chinese_sections) else None
        if english_section is not None:
            anchor = english_section.anchor
            level = english_section.level
        elif chinese_section is not None:
            anchor = chinese_section.anchor
            level = chinese_section.level
        else:
            continue
        rows = align_section_rows(index, anchor, english_section, chinese_section)
        status = summarize_section_status(english_section, chinese_section, rows)
        sections.append(
            AlignedSection(
                index=index,
                anchor=anchor,
                level=level,
                status=status,
                english_anchor=None if english_section is None else english_section.anchor,
                chinese_anchor=None if chinese_section is None else chinese_section.anchor,
                rows=rows,
            )
        )
    return tuple(sections)


def align_section_rows(
    section_index: int,
    section_anchor: str,
    english_section: SectionBlocks | None,
    chinese_section: SectionBlocks | None,
) -> tuple[AlignedRow, ...]:
    if english_section is None:
        assert chinese_section is not None
        return tuple(
            AlignedRow(section_index, section_anchor, row_index, "unmatched-zh", None, block, "extra-zh-section")
            for row_index, block in enumerate(chinese_section.blocks)
        )
    if chinese_section is None:
        return tuple(
            AlignedRow(section_index, section_anchor, row_index, "unmatched-en", block, None, "missing-zh-section")
            for row_index, block in enumerate(english_section.blocks)
        )

    rows: list[AlignedRow] = []
    en_index = 0
    zh_index = 0
    row_index = 0
    english_blocks = english_section.blocks
    chinese_blocks = chinese_section.blocks

    while en_index < len(english_blocks) and zh_index < len(chinese_blocks):
        english_block = english_blocks[en_index]
        chinese_block = chinese_blocks[zh_index]
        if should_skip_extra_paragraph(english_blocks, en_index, chinese_blocks, zh_index, side="zh"):
            rows.append(
                AlignedRow(
                    section_index,
                    section_anchor,
                    row_index,
                    "degraded",
                    None,
                    chinese_block,
                    "extra-zh-paragraph",
                )
            )
            zh_index += 1
            row_index += 1
            continue

        if should_skip_extra_paragraph(english_blocks, en_index, chinese_blocks, zh_index, side="en"):
            rows.append(
                AlignedRow(
                    section_index,
                    section_anchor,
                    row_index,
                    "degraded",
                    english_block,
                    None,
                    "extra-en-paragraph",
                )
            )
            en_index += 1
            row_index += 1
            continue

        if english_block.block_type == chinese_block.block_type:
            rows.append(AlignedRow(section_index, section_anchor, row_index, "matched", english_block, chinese_block))
            en_index += 1
            zh_index += 1
            row_index += 1
            continue

        if english_block.block_type == "paragraph" and can_skip_extra_paragraph(english_blocks, en_index, chinese_block.block_type):
            rows.append(
                AlignedRow(
                    section_index,
                    section_anchor,
                    row_index,
                    "degraded",
                    english_block,
                    None,
                    "extra-en-paragraph",
                )
            )
            en_index += 1
            row_index += 1
            continue

        if chinese_block.block_type == "paragraph" and can_skip_extra_paragraph(chinese_blocks, zh_index, english_block.block_type):
            rows.append(
                AlignedRow(
                    section_index,
                    section_anchor,
                    row_index,
                    "degraded",
                    None,
                    chinese_block,
                    "extra-zh-paragraph",
                )
            )
            zh_index += 1
            row_index += 1
            continue

        rows.append(
            AlignedRow(
                section_index,
                section_anchor,
                row_index,
                "degraded",
                english_block,
                chinese_block,
                f"type-mismatch:{english_block.block_type}->{chinese_block.block_type}",
            )
        )
        en_index += 1
        zh_index += 1
        row_index += 1

    if can_merge_tail_paragraph(rows, english_blocks, en_index, chinese_blocks, zh_index, side="en"):
        last_row = rows.pop()
        assert last_row.english_block is not None
        merged_english = merge_blocks((last_row.english_block, english_blocks[en_index]))
        rows.append(
            AlignedRow(
                section_index,
                section_anchor,
                last_row.row_index,
                "matched",
                merged_english,
                last_row.chinese_block,
                "merged-en-tail-paragraph",
            )
        )
        en_index += 1

    if can_merge_tail_paragraph(rows, english_blocks, en_index, chinese_blocks, zh_index, side="zh"):
        last_row = rows.pop()
        assert last_row.chinese_block is not None
        merged_chinese = merge_blocks((last_row.chinese_block, chinese_blocks[zh_index]))
        rows.append(
            AlignedRow(
                section_index,
                section_anchor,
                last_row.row_index,
                "matched",
                last_row.english_block,
                merged_chinese,
                "merged-zh-tail-paragraph",
            )
        )
        zh_index += 1

    while en_index < len(english_blocks):
        rows.append(
            AlignedRow(
                section_index,
                section_anchor,
                row_index,
                "unmatched-en",
                english_blocks[en_index],
                None,
                "trailing-en-block",
            )
        )
        en_index += 1
        row_index += 1

    while zh_index < len(chinese_blocks):
        rows.append(
            AlignedRow(
                section_index,
                section_anchor,
                row_index,
                "unmatched-zh",
                None,
                chinese_blocks[zh_index],
                "trailing-zh-block",
            )
        )
        zh_index += 1
        row_index += 1

    return tuple(rows)


def can_skip_extra_paragraph(blocks: tuple[Block, ...], index: int, expected_type: str) -> bool:
    return index + 1 < len(blocks) and blocks[index + 1].block_type == expected_type


def can_merge_tail_paragraph(
    rows: list[AlignedRow],
    english_blocks: tuple[Block, ...],
    en_index: int,
    chinese_blocks: tuple[Block, ...],
    zh_index: int,
    side: str,
) -> bool:
    if not rows or rows[-1].status != "matched":
        return False
    if side == "en":
        return (
            en_index == len(english_blocks) - 1
            and zh_index == len(chinese_blocks)
            and english_blocks[en_index].block_type == "paragraph"
            and rows[-1].english_block is not None
            and rows[-1].english_block.block_type == "paragraph"
        )
    return (
        zh_index == len(chinese_blocks) - 1
        and en_index == len(english_blocks)
        and chinese_blocks[zh_index].block_type == "paragraph"
        and rows[-1].chinese_block is not None
        and rows[-1].chinese_block.block_type == "paragraph"
    )


def merge_blocks(blocks: tuple[Block, ...]) -> Block:
    first = blocks[0]
    last = blocks[-1]
    source_text = "\n\n".join(block.source_text for block in blocks)
    return Block(
        index=first.index,
        block_type=first.block_type,
        source_text=source_text,
        content=source_text.strip(),
        section_anchor=first.section_anchor,
        section_level=first.section_level,
        line_start=first.line_start,
        line_end=last.line_end,
        status="merged",
    )


def should_skip_extra_paragraph(
    english_blocks: tuple[Block, ...],
    en_index: int,
    chinese_blocks: tuple[Block, ...],
    zh_index: int,
    side: str,
) -> bool:
    english_block = english_blocks[en_index]
    chinese_block = chinese_blocks[zh_index]
    if english_block.block_type != "paragraph" or chinese_block.block_type != "paragraph":
        return False

    english_marker = paragraph_marker(english_block)
    chinese_marker = paragraph_marker(chinese_block)
    if english_marker == chinese_marker:
        return False

    if side == "zh" and zh_index + 1 < len(chinese_blocks):
        return chinese_blocks[zh_index + 1].block_type == "paragraph" and paragraph_marker(chinese_blocks[zh_index + 1]) == english_marker
    if side == "en" and en_index + 1 < len(english_blocks):
        return english_blocks[en_index + 1].block_type == "paragraph" and paragraph_marker(english_blocks[en_index + 1]) == chinese_marker
    return False


def paragraph_marker(block: Block) -> str | None:
    stripped = block.content.strip()
    if not stripped:
        return None
    example_match = EXAMPLE_MARKER_RE.match(stripped)
    if example_match:
        return f"example:{example_match.group(1)}"
    marker_match = PARAGRAPH_MARKER_RE.match(stripped)
    if marker_match:
        return f"marker:{marker_match.group(1)}"
    return None


def summarize_section_status(
    english_section: SectionBlocks | None,
    chinese_section: SectionBlocks | None,
    rows: tuple[AlignedRow, ...],
) -> str:
    if english_section is None:
        return "unmatched-zh"
    if chinese_section is None:
        return "unmatched-en"
    if any(row.status != "matched" for row in rows):
        return "degraded"
    return "matched"


def summarize_document_status(pair_status: str, sections: tuple[AlignedSection, ...]) -> str:
    if any(section.status in {"unmatched-en", "unmatched-zh"} for section in sections):
        return "incomplete" if pair_status == "incomplete" else "degraded"
    if any(section.status == "degraded" for section in sections):
        return "wrapping-drift" if pair_status == "wrapping-drift" else "degraded"
    return "matched"


def build_text_report(document: AlignedDocument) -> str:
    lines = [
        f"{document.english_file} -> {document.chinese_file}",
        f"pair-status: {document.pair_status}",
        f"alignment-status: {document.status}",
    ]
    if document.warnings:
        lines.append(f"warnings: {', '.join(document.warnings)}")
    for section in document.sections:
        lines.append(
            f"section[{section.index}] anchor={section.anchor!r} lvl={section.level} status={section.status} "
            f"en={section.english_anchor!r} zh={section.chinese_anchor!r}"
        )
        for row in section.rows:
            lines.append(
                "  row[{row}] {status} en={en} zh={zh}{note}".format(
                    row=row.row_index,
                    status=row.status,
                    en=format_block(row.english_block),
                    zh=format_block(row.chinese_block),
                    note="" if not row.note else f" note={row.note}",
                )
            )
    return "\n".join(lines) + "\n"


def format_block(block: Block | None) -> str:
    if block is None:
        return "<missing>"
    preview = block.source_text.replace("\n", " ")
    if len(preview) > 70:
        preview = preview[:67] + "..."
    return f"{block.block_type}@{block.line_start}-{block.line_end}:{preview!r}"


def write_text_report(document: AlignedDocument, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(build_text_report(document), encoding="utf-8")


def aligned_document_to_dict(document: AlignedDocument) -> dict[str, object]:
    return asdict(document)


def main() -> None:
    args = parse_args()
    document = build_aligned_document(args.repo_root, args.chapter)
    if args.report_output:
        write_text_report(document, args.report_output)
    else:
        print(build_text_report(document), end="")


if __name__ == "__main__":
    main()
