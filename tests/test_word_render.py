#!/usr/bin/env python3

from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZipFile

from scripts.bilingual_export.align import build_aligned_document
from scripts.bilingual_export.word_render import render_docx


REPO_ROOT = Path(__file__).resolve().parents[1]
CHAPTER_02 = "02-Argument-Analysis-Identifying-Conclusions-and-Reasons.md"
CHAPTER_09 = "09-Best-Explanation-and-Causal-Inference-Argument-and-Writing-Strategy.md"
CHAPTER_11 = "11-Making-Value-Judgments.md"
WORD_NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}


def all_rows(document):
    return [row for section in document.sections for row in section.rows]


def read_docx_parts(path: Path) -> tuple[str, str, list[str]]:
    with ZipFile(path) as archive:
        document_xml = archive.read("word/document.xml").decode("utf-8")
        rels_xml = archive.read("word/_rels/document.xml.rels").decode("utf-8")
        media_files = sorted(name for name in archive.namelist() if name.startswith("word/media/"))
    return document_xml, rels_xml, media_files


def first_table_row_count(document_xml: str) -> int:
    root = ET.fromstring(document_xml)
    table = root.find(".//w:tbl", WORD_NS)
    assert table is not None
    return len(table.findall("./w:tr", WORD_NS))


def test_chapter_02_docx_structure_and_images(tmp_path: Path) -> None:
    document = build_aligned_document(REPO_ROOT, CHAPTER_02)
    output_path = tmp_path / "chapter-02.docx"
    render_docx(document, REPO_ROOT, output_path)

    document_xml, rels_xml, media_files = read_docx_parts(output_path)
    evidence_path = REPO_ROOT / ".sisyphus/evidence/task-6-docx-structure.txt"
    evidence_path.parent.mkdir(parents=True, exist_ok=True)
    evidence_path.write_text(
        "\n".join(
            [
                f"chapter={CHAPTER_02}",
                f"aligned_rows={len(all_rows(document))}",
                f"outer_table_rows={first_table_row_count(document_xml)}",
                f"media_count={len(media_files)}",
                f"image_rel_count={rels_xml.count('Type=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships/image\"')}",
                f"contains_en_title={'CHAPTER 2 Argument Analysis: Identifying Conclusions and Reasons' in document_xml}",
                f"contains_zh_title={'第 2 章 论证分析：确定结论和理由' in document_xml}",
                "media_files:",
                *media_files[:20],
            ]
        ) + "\n",
        encoding="utf-8",
    )

    assert output_path.exists()
    assert first_table_row_count(document_xml) == len(all_rows(document))
    assert "CHAPTER 2 Argument Analysis: Identifying Conclusions and Reasons" in document_xml
    assert "第 2 章 论证分析：确定结论和理由" in document_xml
    assert "谋杀案审判" in document_xml
    assert len(media_files) >= 42
    assert "relationships/image" in rels_xml


def test_chapter_09_docx_contains_visible_incomplete_markers(tmp_path: Path) -> None:
    document = build_aligned_document(REPO_ROOT, CHAPTER_09)
    output_path = tmp_path / "chapter-09.docx"
    render_docx(document, REPO_ROOT, output_path)

    document_xml, rels_xml, media_files = read_docx_parts(output_path)
    evidence_path = REPO_ROOT / ".sisyphus/evidence/task-6-docx-incomplete.txt"
    evidence_path.write_text(
        "\n".join(
            [
                f"chapter={CHAPTER_09}",
                f"aligned_rows={len(all_rows(document))}",
                f"outer_table_rows={first_table_row_count(document_xml)}",
                f"media_count={len(media_files)}",
                f"image_rel_count={rels_xml.count('Type=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships/image\"')}",
                f"missing_chinese_count={document_xml.count('[Missing Chinese Content]')}",
                f"alignment_notice_count={document_xml.count('[Alignment notice]')}",
            ]
        ) + "\n",
        encoding="utf-8",
    )

    assert first_table_row_count(document_xml) == len(all_rows(document))
    # Ch09 is now fully matched — no missing content markers
    assert "[Missing Chinese Content]" not in document_xml
    assert "[Alignment notice]" not in document_xml
    assert "第 9 章 最佳解释与因果推理：论证与写作策略" in document_xml
    assert len(media_files) >= 1
    assert "relationships/image" in rels_xml


def test_chapter_11_en_image_rows_keep_image_and_label_missing_zh(tmp_path: Path) -> None:
    document = build_aligned_document(REPO_ROOT, CHAPTER_11)
    output_path = tmp_path / "chapter-11.docx"
    render_docx(document, REPO_ROOT, output_path)

    document_xml, rels_xml, media_files = read_docx_parts(output_path)

    assert "CHAPTER 11 Making Value Judgments" in document_xml
    assert "第 11 章 作出价值判断" in document_xml
    assert "[Missing Chinese Content]" in document_xml
    assert "Chinese content continues beyond the aligned English text." in document_xml or "English content continues beyond the aligned Chinese text." in document_xml
    assert len(media_files) >= 2
    assert rels_xml.count("relationships/image") >= 2
