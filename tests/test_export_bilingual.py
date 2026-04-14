#!/usr/bin/env python3

import json
import subprocess
import sys
from pathlib import Path

from scripts.export_bilingual import build_report, run_export


REPO_ROOT = Path(__file__).resolve().parents[1]
TOC_FILE = "TC-Table-of-Contents.md"
CH02_FILE = "02-Argument-Analysis-Identifying-Conclusions-and-Reasons.md"
SUBSET = [TOC_FILE, CH02_FILE]


def _run_subset(tmp_path: Path, **kwargs) -> list[dict]:
    return run_export(
        repo_root=REPO_ROOT,
        output_root=tmp_path,
        chapter_filter=SUBSET,
        skip_html=kwargs.get("skip_html", False),
        skip_word=kwargs.get("skip_word", False),
    )


def test_subset_produces_two_entries(tmp_path: Path) -> None:
    entries = _run_subset(tmp_path)
    assert len(entries) == 2
    names = {e["english_file"] for e in entries}
    assert names == {TOC_FILE, CH02_FILE}


def test_subset_html_files_exist(tmp_path: Path) -> None:
    entries = _run_subset(tmp_path)
    html_dir = tmp_path / "html"
    assert html_dir.is_dir()
    for entry in entries:
        assert entry["html_output"] is not None
        assert Path(entry["html_output"]).exists()
        assert entry["html_bytes"] > 0


def test_subset_word_files_exist(tmp_path: Path) -> None:
    entries = _run_subset(tmp_path)
    word_dir = tmp_path / "word"
    assert word_dir.is_dir()
    for entry in entries:
        assert entry["word_output"] is not None
        assert Path(entry["word_output"]).exists()
        assert entry["word_bytes"] > 0


def test_subset_html_is_standalone(tmp_path: Path) -> None:
    entries = _run_subset(tmp_path)
    for entry in entries:
        html_content = Path(entry["html_output"]).read_text(encoding="utf-8")
        assert "<style>" in html_content
        assert "data:image/" in html_content or "img" not in html_content.lower() or entry["english_file"] == TOC_FILE


def test_subset_html_has_bilingual_rows(tmp_path: Path) -> None:
    entries = _run_subset(tmp_path)
    for entry in entries:
        html_content = Path(entry["html_output"]).read_text(encoding="utf-8")
        assert 'class="col col-en"' in html_content
        assert 'class="col col-zh"' in html_content


def test_skip_html_no_html_files(tmp_path: Path) -> None:
    entries = _run_subset(tmp_path, skip_html=True)
    html_dir = tmp_path / "html"
    assert not html_dir.exists() or not list(html_dir.iterdir())
    for entry in entries:
        assert entry["html_output"] is None
        assert entry["html_bytes"] == 0


def test_skip_word_no_word_files(tmp_path: Path) -> None:
    entries = _run_subset(tmp_path, skip_word=True)
    word_dir = tmp_path / "word"
    assert not word_dir.exists() or not list(word_dir.iterdir())
    for entry in entries:
        assert entry["word_output"] is None
        assert entry["word_bytes"] == 0


def test_entries_contain_required_fields(tmp_path: Path) -> None:
    entries = _run_subset(tmp_path)
    required_keys = {
        "english_file", "chinese_file", "pair_status", "alignment_status",
        "html_output", "word_output", "html_bytes", "word_bytes", "warnings",
    }
    for entry in entries:
        assert required_keys.issubset(entry.keys()), f"Missing keys in {entry['english_file']}"


def test_toc_pairing_in_entries(tmp_path: Path) -> None:
    entries = _run_subset(tmp_path)
    toc_entry = next(e for e in entries if e["english_file"] == TOC_FILE)
    assert toc_entry["chinese_file"] == "00-Contents.md"


def test_ch02_pairing_in_entries(tmp_path: Path) -> None:
    entries = _run_subset(tmp_path)
    ch02 = next(e for e in entries if e["english_file"] == CH02_FILE)
    assert ch02["chinese_file"] == CH02_FILE


def test_report_contains_status_sections(tmp_path: Path) -> None:
    entries = _run_subset(tmp_path)
    report = build_report(entries)
    assert "# Bilingual Export Report" in report
    assert "Total chapters: 2" in report
    assert "## Per-Chapter Details" in report
    assert TOC_FILE in report
    assert CH02_FILE in report


def test_report_lists_pair_status(tmp_path: Path) -> None:
    entries = _run_subset(tmp_path)
    report = build_report(entries)
    for entry in entries:
        assert entry["pair_status"] in report


def test_report_categorizes_chapters(tmp_path: Path) -> None:
    entries = _run_subset(tmp_path)
    report = build_report(entries)
    assert "Exact Match" in report or "Wrapping Drift" in report


def test_full_manifest_json_written(tmp_path: Path) -> None:
    from scripts.export_bilingual import main
    import argparse

    output_root = tmp_path / "full_run"
    entries = run_export(REPO_ROOT, output_root, chapter_filter=None, skip_html=False, skip_word=False)
    manifest_path = output_root / "manifest.json"
    manifest_path.write_text(json.dumps(entries, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    loaded = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert len(loaded) == 17


def test_full_manifest_toc_pairing(tmp_path: Path) -> None:
    entries = run_export(REPO_ROOT, tmp_path, chapter_filter=None, skip_html=True, skip_word=True)
    toc = next(e for e in entries if e["english_file"] == TOC_FILE)
    assert toc["chinese_file"] == "00-Contents.md"


def test_full_manifest_ch09_incomplete(tmp_path: Path) -> None:
    entries = run_export(REPO_ROOT, tmp_path, chapter_filter=None, skip_html=True, skip_word=True)
    ch09 = next(
        e for e in entries
        if e["english_file"] == "09-Best-Explanation-and-Causal-Inference-Argument-and-Writing-Strategy.md"
    )
    # Ch09 was fixed (duplicate section removed) — now exact
    assert ch09["pair_status"] == "exact"


def test_full_manifest_ch11_image_asymmetry(tmp_path: Path) -> None:
    entries = run_export(REPO_ROOT, tmp_path, chapter_filter=None, skip_html=True, skip_word=True)
    ch11 = next(e for e in entries if e["english_file"] == "11-Making-Value-Judgments.md")
    assert any("image-count-asymmetry" in w for w in ch11["warnings"])


def test_report_full_run_categorization(tmp_path: Path) -> None:
    entries = run_export(REPO_ROOT, tmp_path, chapter_filter=None, skip_html=True, skip_word=True)
    report = build_report(entries)
    assert "Total chapters: 17" in report
    assert "Divergent / Incomplete" in report
    assert "09-Best-Explanation" in report
    assert "Image Asymmetry" in report


def test_html_ch02_has_images(tmp_path: Path) -> None:
    run_export(REPO_ROOT, tmp_path, chapter_filter=[CH02_FILE], skip_html=False, skip_word=True)
    html_path = tmp_path / "html" / "02-Argument-Analysis-Identifying-Conclusions-and-Reasons.html"
    assert html_path.exists()
    content = html_path.read_text(encoding="utf-8")
    assert "data:image/" in content


def test_word_ch02_has_images(tmp_path: Path) -> None:
    run_export(REPO_ROOT, tmp_path, chapter_filter=[CH02_FILE], skip_html=True, skip_word=False)
    word_path = tmp_path / "word" / "02-Argument-Analysis-Identifying-Conclusions-and-Reasons.docx"
    assert word_path.exists()
    import zipfile
    with zipfile.ZipFile(str(word_path)) as zf:
        names = zf.namelist()
        media_files = [n for n in names if n.startswith("word/media/")]
        assert len(media_files) > 0, f"Expected images in docx, got: {names}"


def test_word_ch09_divergent_marker(tmp_path: Path) -> None:
    run_export(
        REPO_ROOT, tmp_path,
        chapter_filter=["09-Best-Explanation-and-Causal-Inference-Argument-and-Writing-Strategy.md"],
        skip_html=True, skip_word=False,
    )
    word_path = tmp_path / "word" / "09-Best-Explanation-and-Causal-Inference-Argument-and-Writing-Strategy.docx"
    assert word_path.exists()
    # Ch09 is now fully matched — no alignment notice expected
    import zipfile
    with zipfile.ZipFile(str(word_path)) as zf:
        doc_xml = zf.read("word/document.xml").decode("utf-8")
        assert "Alignment notice" not in doc_xml


# --- Real CLI invocation tests (subprocess) ---

PYTHON = sys.executable
SCRIPT = str(REPO_ROOT / "scripts" / "export_bilingual.py")


def test_cli_help_succeeds() -> None:
    result = subprocess.run(
        [PYTHON, SCRIPT, "--help"],
        capture_output=True, text=True, timeout=30,
    )
    assert result.returncode == 0, f"stderr: {result.stderr}"
    assert "output-root" in result.stdout
    assert "chapter" in result.stdout


def test_cli_subset_run_produces_all_outputs(tmp_path: Path) -> None:
    output_root = tmp_path / "cli_subset"
    result = subprocess.run(
        [
            PYTHON, SCRIPT,
            "--output-root", str(output_root),
            "--chapter", TOC_FILE,
            "--chapter", CH02_FILE,
        ],
        capture_output=True, text=True, timeout=120,
    )
    assert result.returncode == 0, f"stderr: {result.stderr}"
    assert "Export complete: 2 chapters" in result.stderr

    manifest_path = output_root / "manifest.json"
    report_path = output_root / "report.md"
    assert manifest_path.exists()
    assert report_path.exists()

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert len(manifest) == 2
    names = {e["english_file"] for e in manifest}
    assert names == {TOC_FILE, CH02_FILE}

    html_dir = output_root / "html"
    word_dir = output_root / "word"
    assert html_dir.is_dir()
    assert word_dir.is_dir()
    assert len(list(html_dir.glob("*.html"))) == 2
    assert len(list(word_dir.glob("*.docx"))) == 2


def test_cli_skip_html_no_html_dir(tmp_path: Path) -> None:
    output_root = tmp_path / "cli_skip_html"
    result = subprocess.run(
        [
            PYTHON, SCRIPT,
            "--output-root", str(output_root),
            "--chapter", TOC_FILE,
            "--skip-html",
        ],
        capture_output=True, text=True, timeout=60,
    )
    assert result.returncode == 0, f"stderr: {result.stderr}"
    assert not (output_root / "html").exists()


def test_cli_skip_word_no_word_dir(tmp_path: Path) -> None:
    output_root = tmp_path / "cli_skip_word"
    result = subprocess.run(
        [
            PYTHON, SCRIPT,
            "--output-root", str(output_root),
            "--chapter", TOC_FILE,
            "--skip-word",
        ],
        capture_output=True, text=True, timeout=60,
    )
    assert result.returncode == 0, f"stderr: {result.stderr}"
    assert not (output_root / "word").exists()
