#!/usr/bin/env python3

import argparse
import importlib
import re
from pathlib import Path
from typing import Any

from scripts.bilingual_export.align import AlignedDocument, AlignedRow, Block, build_aligned_document
from scripts.bilingual_export.image_utils import extract_image_refs, resolve_images

Document = importlib.import_module("docx").Document
WD_ALIGN_PARAGRAPH = importlib.import_module("docx.enum.text").WD_ALIGN_PARAGRAPH
OxmlElement = importlib.import_module("docx.oxml").OxmlElement
qn = importlib.import_module("docx.oxml.ns").qn
Inches = importlib.import_module("docx.shared").Inches
DocxDocument = Any

PLACEHOLDER_LABELS = {
    "en": "Missing English Content",
    "zh": "Missing Chinese Content",
}

NOTICE_LABELS = {
    "missing-zh-section": "No aligned Chinese section for this English block.",
    "missing-en-section": "No aligned English section for this Chinese block.",
    "trailing-en-block": "English content continues beyond the aligned Chinese text.",
    "trailing-zh-block": "Chinese content continues beyond the aligned English text.",
    "extra-en-paragraph": "Extra English paragraph with no direct Chinese match.",
    "extra-zh-paragraph": "Extra Chinese paragraph with no direct English match.",
    "merged-en-tail-paragraph": "English tail paragraph merged into the previous matched row.",
    "merged-zh-tail-paragraph": "Chinese tail paragraph merged into the previous matched row.",
}

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
TABLE_SEPARATOR_RE = re.compile(r"^\|[\s:\-\|]+\|$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render aligned bilingual chapter to DOCX.")
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--chapter", required=True, help="English markdown filename.")
    parser.add_argument("--output", type=Path, required=True, help="Output DOCX file path.")
    return parser.parse_args()


def set_table_borders_none(table) -> None:
    table_element = table._tbl
    table_pr = table_element.tblPr
    if table_pr is None:
        table_pr = OxmlElement("w:tblPr")
        table_element.insert(0, table_pr)
    borders = table_pr.find(qn("w:tblBorders"))
    if borders is None:
        borders = OxmlElement("w:tblBorders")
        table_pr.append(borders)
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        edge_element = borders.find(qn(f"w:{edge}"))
        if edge_element is None:
            edge_element = OxmlElement(f"w:{edge}")
            borders.append(edge_element)
        edge_element.set(qn("w:val"), "nil")


def first_paragraph(cell):
    return cell.paragraphs[0] if cell.paragraphs else cell.add_paragraph()


def add_notice(cell, text: str) -> None:
    paragraph = first_paragraph(cell) if not cell.text and len(cell.paragraphs) == 1 else cell.add_paragraph()
    run = paragraph.add_run(f"[Alignment notice] {text}")
    run.bold = True


def add_missing_placeholder(cell, side: str, note: str) -> None:
    label = PLACEHOLDER_LABELS[side]
    message = notice_message(note, f"No aligned {language_name(side)} block.")
    paragraph = first_paragraph(cell)
    run = paragraph.add_run(f"[{label}] {message}")
    run.bold = True


def language_name(side: str) -> str:
    return "English" if side == "en" else "Chinese"


def notice_message(note: str, fallback: str) -> str:
    if note in NOTICE_LABELS:
        return NOTICE_LABELS[note]
    if note.startswith("type-mismatch:"):
        mismatch = note.split(":", 1)[1]
        return f"Aligned row contains different block types ({mismatch})."
    return fallback


def write_multiline_text(paragraph, text: str) -> None:
    lines = text.splitlines() or [text]
    for index, line in enumerate(lines):
        if index:
            paragraph.add_run().add_break()
        paragraph.add_run(line)


def render_heading(cell, block: Block) -> None:
    match = HEADING_RE.match(block.content)
    text = block.content
    level = 1
    if match:
        level = len(match.group(1))
        text = match.group(2)
    paragraph = first_paragraph(cell) if not cell.text and len(cell.paragraphs) == 1 else cell.add_paragraph()
    paragraph.style = f"Heading {min(level, 6)}"
    write_multiline_text(paragraph, text)


def render_paragraph(cell, block: Block) -> None:
    paragraph = first_paragraph(cell) if not cell.text and len(cell.paragraphs) == 1 else cell.add_paragraph()
    write_multiline_text(paragraph, block.content)


def parse_markdown_table(content: str) -> tuple[list[list[str]], bool]:
    rows: list[list[str]] = []
    lines = [line.strip() for line in content.splitlines() if line.strip() and not line.strip().startswith("<!--")]
    has_header = len(lines) > 1 and TABLE_SEPARATOR_RE.match(lines[1]) is not None
    for index, line in enumerate(lines):
        if has_header and index == 1:
            continue
        rows.append([cell.strip() for cell in line.strip("|").split("|")])
    return rows, has_header


def render_table_block(cell, block: Block) -> None:
    rows, has_header = parse_markdown_table(block.content)
    if not rows:
        render_paragraph(cell, block)
        return
    column_count = max(len(row) for row in rows)
    table = cell.add_table(rows=len(rows), cols=column_count)
    table.style = "Table Grid"
    for row_index, row in enumerate(rows):
        for column_index in range(column_count):
            value = row[column_index] if column_index < len(row) else ""
            nested_cell = table.cell(row_index, column_index)
            nested_cell.text = value
            if has_header and row_index == 0:
                for paragraph in nested_cell.paragraphs:
                    for run in paragraph.runs:
                        run.bold = True


def render_image_block(cell, block: Block, repo_root: Path, file_name: str, side: str) -> None:
    refs = extract_image_refs(block.content)
    if not refs:
        render_paragraph(cell, block)
        return
    folder = "FullText-en" if side == "en" else "FullText-zh-sense"
    context_path = repo_root / folder / file_name
    try:
        resolved = resolve_images(refs, context_path, repo_root)
    except FileNotFoundError as exc:
        paragraph = first_paragraph(cell) if not cell.text and len(cell.paragraphs) == 1 else cell.add_paragraph()
        run = paragraph.add_run(f"[Image not found] {exc}")
        run.bold = True
        return
    for image in resolved:
        paragraph = first_paragraph(cell) if not cell.text and len(cell.paragraphs) == 1 else cell.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = paragraph.add_run()
        run.add_picture(image.absolute_path, width=Inches(3.0))
        if image.alt_text:
            caption = cell.add_paragraph()
            caption.alignment = WD_ALIGN_PARAGRAPH.CENTER
            caption.add_run(image.alt_text)


def render_block(cell, block: Block, repo_root: Path, file_name: str, side: str) -> None:
    if block.block_type == "heading":
        render_heading(cell, block)
        return
    if block.block_type == "paragraph":
        render_paragraph(cell, block)
        return
    if block.block_type == "table":
        render_table_block(cell, block)
        return
    if block.block_type == "image":
        render_image_block(cell, block, repo_root, file_name, side)
        return
    render_paragraph(cell, block)


def render_row_cells(row: AlignedRow, en_cell, zh_cell, repo_root: Path, document: AlignedDocument) -> None:
    if row.english_block is None:
        add_missing_placeholder(en_cell, "en", row.note)
    else:
        if row.status != "matched":
            add_notice(en_cell, notice_message(row.note, "This English block does not align cleanly."))
        render_block(en_cell, row.english_block, repo_root, document.english_file, "en")

    if row.chinese_block is None:
        add_missing_placeholder(zh_cell, "zh", row.note)
    else:
        if row.status != "matched":
            add_notice(zh_cell, notice_message(row.note, "This Chinese block does not align cleanly."))
        render_block(zh_cell, row.chinese_block, repo_root, document.chinese_file, "zh")


def build_docx(document: AlignedDocument, repo_root: Path) -> DocxDocument:
    doc = Document()
    table = doc.add_table(rows=0, cols=2)
    table.autofit = True
    set_table_borders_none(table)

    for section in document.sections:
        for row in section.rows:
            docx_row = table.add_row()
            left_cell = docx_row.cells[0]
            right_cell = docx_row.cells[1]
            left_cell.width = Inches(3.25)
            right_cell.width = Inches(3.25)
            render_row_cells(row, left_cell, right_cell, repo_root, document)

    return doc


def render_docx(document: AlignedDocument, repo_root: Path, output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    doc = build_docx(document, repo_root)
    doc.save(output_path)
    return output_path


def main() -> None:
    args = parse_args()
    document = build_aligned_document(args.repo_root, args.chapter)
    render_docx(document, args.repo_root, args.output)


if __name__ == "__main__":
    main()
