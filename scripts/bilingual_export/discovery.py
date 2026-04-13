#!/usr/bin/env python3

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path


CONTROL_ZH_FILES = {"termbase.md", "translation-guide.md"}
TOC_EN_NAME = "TC-Table-of-Contents.md"
TOC_ZH_NAME = "00-Contents.md"
IMAGE_RE = re.compile(r"!\[[^\]]*\]\([^\)]+\)")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*\S)\s*$")


@dataclass(frozen=True)
class SectionAudit:
    anchor: str
    level: int
    line_count: int
    block_count: int
    paragraph_blocks: int
    table_blocks: int
    image_blocks: int


@dataclass(frozen=True)
class FileAudit:
    path: str
    line_count: int
    heading_count: int
    image_count: int
    total_block_count: int
    section_count: int
    section_anchor_levels: tuple[int, ...]
    sections: tuple[SectionAudit, ...]


@dataclass(frozen=True)
class ChapterPairAudit:
    english_file: str
    chinese_file: str
    status: str
    warnings: tuple[str, ...]
    is_degraded: bool
    notes: tuple[str, ...]
    english: FileAudit
    chinese: FileAudit


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build bilingual chapter discovery manifest and source audit.")
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path(__file__).resolve().parents[2],
        help="Repository root containing FullText-en and FullText-zh-sense.",
    )
    parser.add_argument("--json-output", type=Path, help="Write the full pair manifest as JSON.")
    parser.add_argument(
        "--report-output",
        type=Path,
        help="Write a plain-text report for either all pairs or selected --chapter files.",
    )
    parser.add_argument(
        "--chapter",
        action="append",
        default=[],
        help="Limit the report to one or more English filenames, e.g. 09-Best-Explanation....md",
    )
    return parser.parse_args()


def discover_pairs(repo_root: Path) -> list[tuple[Path, Path]]:
    english_dir = repo_root / "FullText-en"
    chinese_dir = repo_root / "FullText-zh-sense"
    english_files = sorted(english_dir.glob("*.md"))
    chinese_files = {path.name: path for path in chinese_dir.glob("*.md") if path.name not in CONTROL_ZH_FILES}

    pairs: list[tuple[Path, Path]] = []
    for english_path in english_files:
        chinese_name = TOC_ZH_NAME if english_path.name == TOC_EN_NAME else english_path.name
        chinese_path = chinese_files.get(chinese_name)
        if chinese_path is None:
            raise FileNotFoundError(f"Missing Chinese pair for {english_path.name}: expected {chinese_name}")
        pairs.append((english_path, chinese_path))
    return pairs


def audit_pair(english_path: Path, chinese_path: Path) -> ChapterPairAudit:
    english_audit = audit_file(english_path)
    chinese_audit = audit_file(chinese_path)
    status, warnings, notes = classify_pair(english_audit, chinese_audit)
    return ChapterPairAudit(
        english_file=english_path.name,
        chinese_file=chinese_path.name,
        status=status,
        warnings=tuple(warnings),
        is_degraded=status in {"divergent", "incomplete"},
        notes=tuple(notes),
        english=english_audit,
        chinese=chinese_audit,
    )


def build_pair_manifest(repo_root: Path) -> list[ChapterPairAudit]:
    return [audit_pair(english_path, chinese_path) for english_path, chinese_path in discover_pairs(repo_root)]


def audit_file(path: Path) -> FileAudit:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    sections = tuple(split_sections(lines))
    section_anchor_levels = tuple(section.level for section in sections[1:])
    return FileAudit(
        path=str(path),
        line_count=len(lines),
        heading_count=sum(1 for line in lines if HEADING_RE.match(line)),
        image_count=len(IMAGE_RE.findall(text)),
        total_block_count=sum(section.block_count for section in sections),
        section_count=len(sections),
        section_anchor_levels=section_anchor_levels,
        sections=sections,
    )


def split_sections(lines: list[str]) -> list[SectionAudit]:
    sections: list[tuple[str, int, list[str]]] = []
    current_anchor = "__preamble__"
    current_level = 1
    current_lines: list[str] = []

    for line in lines:
        match = HEADING_RE.match(line)
        if match and len(match.group(1)) >= 2:
            sections.append((current_anchor, current_level, current_lines))
            current_anchor = match.group(2)
            current_level = len(match.group(1))
            current_lines = [line]
            continue
        current_lines.append(line)

    sections.append((current_anchor, current_level, current_lines))
    return [summarize_section(anchor, level, section_lines) for anchor, level, section_lines in sections]


def summarize_section(anchor: str, level: int, lines: list[str]) -> SectionAudit:
    paragraph_blocks = 0
    table_blocks = 0
    image_blocks = 0
    paragraph_open = False
    table_open = False

    for line in lines:
        stripped = line.strip()
        if not stripped:
            paragraph_open = False
            table_open = False
            continue
        if IMAGE_RE.fullmatch(stripped):
            image_blocks += 1
            paragraph_open = False
            table_open = False
            continue
        if is_table_line(stripped):
            if not table_open:
                table_blocks += 1
                table_open = True
            paragraph_open = False
            continue
        table_open = False
        if not paragraph_open:
            paragraph_blocks += 1
            paragraph_open = True

    return SectionAudit(
        anchor=anchor,
        level=level,
        line_count=len(lines),
        block_count=paragraph_blocks + table_blocks + image_blocks,
        paragraph_blocks=paragraph_blocks,
        table_blocks=table_blocks,
        image_blocks=image_blocks,
    )


def is_table_line(stripped_line: str) -> bool:
    return stripped_line.startswith("|") and stripped_line.count("|") >= 2


def classify_pair(english: FileAudit, chinese: FileAudit) -> tuple[str, list[str], list[str]]:
    warnings: list[str] = []
    notes: list[str] = []
    english_levels = english.section_anchor_levels
    chinese_levels = chinese.section_anchor_levels

    if english.image_count != chinese.image_count:
        warnings.append(f"image-count-asymmetry: en={english.image_count}, zh={chinese.image_count}")

    if english_levels == chinese_levels:
        if english.line_count == chinese.line_count and english.total_block_count == chinese.total_block_count:
            status = "exact"
        else:
            status = "wrapping-drift"
            notes.append("Heading anchors align; line/block differences look like translation expansion or paragraph wrapping.")
    elif is_prefix(chinese_levels, english_levels):
        status = "incomplete"
        missing = len(english_levels) - len(chinese_levels)
        notes.append(f"Chinese file ends after a matched section prefix and is missing {missing} trailing section(s).")
    elif is_prefix(english_levels, chinese_levels):
        status = "divergent"
        notes.append("Chinese file contains extra anchored sections beyond the English source.")
    else:
        status = "divergent"
        notes.append("Section anchor sequence diverges before the end of either file.")

    return status, warnings, notes


def is_prefix(candidate: tuple[int, ...], full: tuple[int, ...]) -> bool:
    return len(candidate) < len(full) and full[: len(candidate)] == candidate


def manifest_to_serializable(manifest: list[ChapterPairAudit]) -> list[dict[str, object]]:
    return [asdict(item) for item in manifest]


def write_manifest_json(manifest: list[ChapterPairAudit], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(manifest_to_serializable(manifest), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def build_text_report(manifest: list[ChapterPairAudit], english_filenames: list[str] | None = None) -> str:
    selected = manifest
    if english_filenames:
        wanted = set(english_filenames)
        selected = [item for item in manifest if item.english_file in wanted]

    lines: list[str] = []
    for item in selected:
        lines.append(f"{item.english_file} -> {item.chinese_file}")
        lines.append(f"  status: {item.status}")
        lines.append(
            "  counts: "
            f"en(lines={item.english.line_count}, headings={item.english.heading_count}, images={item.english.image_count}, blocks={item.english.total_block_count}) | "
            f"zh(lines={item.chinese.line_count}, headings={item.chinese.heading_count}, images={item.chinese.image_count}, blocks={item.chinese.total_block_count})"
        )
        lines.append(
            "  section-anchor-levels: "
            f"en={list(item.english.section_anchor_levels)} | zh={list(item.chinese.section_anchor_levels)}"
        )
        if item.warnings:
            lines.append(f"  warnings: {', '.join(item.warnings)}")
        if item.notes:
            lines.append(f"  notes: {' | '.join(item.notes)}")
        lines.append("  per-section:")
        max_sections = max(len(item.english.sections), len(item.chinese.sections))
        for index in range(max_sections):
            english_section = item.english.sections[index] if index < len(item.english.sections) else None
            chinese_section = item.chinese.sections[index] if index < len(item.chinese.sections) else None
            lines.append(
                "    "
                + format_section_pair(index, english_section, chinese_section)
            )
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def format_section_pair(index: int, english_section: SectionAudit | None, chinese_section: SectionAudit | None) -> str:
    english_text = format_section(english_section)
    chinese_text = format_section(chinese_section)
    return f"[{index}] en={english_text} || zh={chinese_text}"


def format_section(section: SectionAudit | None) -> str:
    if section is None:
        return "<missing>"
    return (
        f"{section.anchor!r} lvl={section.level} lines={section.line_count} blocks={section.block_count} "
        f"(p={section.paragraph_blocks}, t={section.table_blocks}, i={section.image_blocks})"
    )


def write_text_report(manifest: list[ChapterPairAudit], output_path: Path, english_filenames: list[str] | None = None) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(build_text_report(manifest, english_filenames), encoding="utf-8")


def main() -> None:
    args = parse_args()
    manifest = build_pair_manifest(args.repo_root)
    if args.json_output:
        write_manifest_json(manifest, args.json_output)
    if args.report_output:
        write_text_report(manifest, args.report_output, args.chapter)
    if not args.json_output and not args.report_output:
        print(json.dumps(manifest_to_serializable(manifest), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
