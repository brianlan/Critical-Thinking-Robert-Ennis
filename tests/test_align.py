#!/usr/bin/env python3

from pathlib import Path

from scripts.bilingual_export.align import build_aligned_document, parse_markdown


REPO_ROOT = Path(__file__).resolve().parents[1]
CHAPTER_02 = "02-Argument-Analysis-Identifying-Conclusions-and-Reasons.md"
CHAPTER_06 = "06-Deduction-Propositional-Logic.md"
CHAPTER_09 = "09-Best-Explanation-and-Causal-Inference-Argument-and-Writing-Strategy.md"


def all_rows(document):
    return [row for section in document.sections for row in section.rows]


def test_parser_preserves_atomic_tables_images_and_plus_marker() -> None:
    chapter_02 = parse_markdown(REPO_ROOT / "FullText-en" / CHAPTER_02)
    chapter_09 = parse_markdown(REPO_ROOT / "FullText-en" / CHAPTER_09)

    assert any(block.block_type == "table" for block in chapter_02.blocks)
    assert any(block.block_type == "image" for block in chapter_02.blocks)
    assert any("&#43;" in block.source_text for block in chapter_09.blocks)


def test_chapter_02_aligns_cleanly() -> None:
    document = build_aligned_document(REPO_ROOT, CHAPTER_02)

    assert document.pair_status in {"exact", "wrapping-drift"}
    assert document.status == "matched"
    assert all(row.status == "matched" for row in all_rows(document))


def test_chapter_09_emits_unmatched_english_tail() -> None:
    document = build_aligned_document(REPO_ROOT, CHAPTER_09)
    rows = all_rows(document)

    assert document.pair_status == "incomplete"
    assert document.status == "incomplete"
    assert any(row.status == "unmatched-en" for row in rows)
    assert any(section.status == "unmatched-en" for section in document.sections)


def test_chapter_06_absorbs_wrapping_drift_without_section_tail_failure() -> None:
    document = build_aligned_document(REPO_ROOT, CHAPTER_06)
    rows = all_rows(document)

    assert document.pair_status == "wrapping-drift"
    assert document.status == "matched"
    assert all(section.status != "unmatched-en" for section in document.sections)
    assert all(section.status != "unmatched-zh" for section in document.sections)
    assert any(row.status == "matched" for row in rows)
    assert all(row.status == "matched" for row in rows)
