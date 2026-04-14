import json
from pathlib import Path

from scripts.bilingual_export.html_validate import render_report, validate_output_root


REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_ROOT = REPO_ROOT / "FullText-en-zh-sense"


def test_full_html_validation_passes() -> None:
    report = validate_output_root(REPO_ROOT, OUTPUT_ROOT)
    assert report.chapter_count == 17
    assert report.passed
    assert not report.failed_chapters


def test_chapter_02_validation_confirms_heading_and_image_parity() -> None:
    report = validate_output_root(REPO_ROOT, OUTPUT_ROOT)
    chapter = next(item for item in report.chapters if item.english_file.startswith("02-"))
    assert chapter.passed
    assert chapter.expected.english.heading_count == chapter.actual.english.heading_count
    assert chapter.expected.chinese.heading_count == chapter.actual.chinese.heading_count
    assert chapter.expected.english.image_count == 42
    assert chapter.expected.chinese.image_count == 42
    assert chapter.actual.english.data_uri_image_count == 42
    assert chapter.actual.chinese.data_uri_image_count == 42


def test_chapter_09_validation_confirms_incomplete_markers_and_report_agreement() -> None:
    report = validate_output_root(REPO_ROOT, OUTPUT_ROOT)
    chapter = next(item for item in report.chapters if item.english_file.startswith("09-"))
    assert chapter.passed
    # Ch09 was fixed (duplicate section removed) — no longer incomplete
    assert chapter.pair_status == "exact"
    assert chapter.alignment_status == "matched"
    assert chapter.checks["manifest_report_agree"]
    assert chapter.actual.missing_markers["zh"] == 0
    assert chapter.expected.missing_markers == chapter.actual.missing_markers


def test_rendered_validation_report_mentions_required_chapters() -> None:
    report = validate_output_root(REPO_ROOT, OUTPUT_ROOT)
    rendered = render_report(report)
    assert "# HTML Structural Validation Report" in rendered
    assert "02-Argument-Analysis-Identifying-Conclusions-and-Reasons.md" in rendered
    assert "09-Best-Explanation-and-Causal-Inference-Argument-and-Writing-Strategy.md" in rendered


def test_validation_report_is_json_serializable() -> None:
    report = validate_output_root(REPO_ROOT, OUTPUT_ROOT)
    payload = json.loads(json.dumps(report, default=lambda value: value.__dict__, ensure_ascii=False))
    assert payload["chapter_count"] == 17
