#!/usr/bin/env python3

from pathlib import Path

from scripts.bilingual_export.discovery import ChapterPairAudit, build_pair_manifest


REPO_ROOT = Path(__file__).resolve().parents[1]


def manifest_by_english_name() -> dict[str, ChapterPairAudit]:
    manifest = build_pair_manifest(REPO_ROOT)
    return {item.english_file: item for item in manifest}


def test_pair_manifest_has_expected_count() -> None:
    manifest = build_pair_manifest(REPO_ROOT)
    assert len(manifest) == 17


def test_toc_pairing_is_explicit() -> None:
    manifest = manifest_by_english_name()
    toc = manifest["TC-Table-of-Contents.md"]
    assert toc.chinese_file == "00-Contents.md"


def test_control_docs_are_excluded_from_manifest() -> None:
    manifest = build_pair_manifest(REPO_ROOT)
    chinese_names = {item.chinese_file for item in manifest}
    assert "termbase.md" not in chinese_names
    assert "translation-guide.md" not in chinese_names


def test_chapter_09_is_flagged_incomplete() -> None:
    manifest = manifest_by_english_name()
    chapter = manifest["09-Best-Explanation-and-Causal-Inference-Argument-and-Writing-Strategy.md"]
    assert chapter.status == "incomplete"
    assert chapter.is_degraded is True


def test_chapter_11_reports_image_asymmetry() -> None:
    manifest = manifest_by_english_name()
    chapter = manifest["11-Making-Value-Judgments.md"]
    assert any("image-count-asymmetry" in warning for warning in chapter.warnings)
    assert chapter.english.image_count == 2
    assert chapter.chinese.image_count == 0


def test_wrapping_drift_detected_for_healthy_chapter() -> None:
    manifest = manifest_by_english_name()
    chapter = manifest["06-Deduction-Propositional-Logic.md"]
    assert chapter.status == "wrapping-drift"
    assert chapter.is_degraded is False
    assert chapter.english.section_anchor_levels == chapter.chinese.section_anchor_levels
    assert chapter.english.line_count != chapter.chinese.line_count
