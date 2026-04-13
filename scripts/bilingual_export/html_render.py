#!/usr/bin/env python3

import argparse
import re
from pathlib import Path
from typing import TextIO

from markdown_it import MarkdownIt

from scripts.bilingual_export.align import AlignedDocument, AlignedRow, Block, build_aligned_document
from scripts.bilingual_export.image_utils import extract_image_refs, resolve_images

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render aligned bilingual chapter to HTML.")
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--chapter", required=True, help="English markdown filename.")
    parser.add_argument("--output", type=Path, help="Output HTML file path.")
    return parser.parse_args()

md_parser = MarkdownIt('commonmark', {'html': False})
md_parser.disable('entity')

def render_markdown_text(text: str) -> str:
    """Render markdown block to HTML, preserving &#43; but escaping raw HTML like <EF>."""
    rendered = md_parser.render(text)
    rendered = re.sub(r'&amp;(#\d+|[a-zA-Z]+);', r'&\1;', rendered)
    
    # Process footnote definitions
    rendered = re.sub(r'\[\^(\d+)\]:\s*', r'<a id="fn\1"></a><sup class="footnote-label">[\1]</sup> ', rendered)
    # Process footnote references
    rendered = re.sub(r'\[\^(\d+)\]', r'<sup class="footnote-ref"><a href="#fn\1">[\1]</a></sup>', rendered)
    
    return rendered

def render_markdown_inline(text: str) -> str:
    """Render markdown inline to HTML, preserving &#43; but escaping raw HTML like <EF>."""
    rendered = md_parser.renderInline(text)
    rendered = re.sub(r'&amp;(#\d+|[a-zA-Z]+);', r'&\1;', rendered)
    
    # Process footnote definitions (just in case they appear inline)
    rendered = re.sub(r'\[\^(\d+)\]:\s*', r'<a id="fn\1"></a><sup class="footnote-label">[\1]</sup> ', rendered)
    # Process footnote references
    rendered = re.sub(r'\[\^(\d+)\]', r'<sup class="footnote-ref"><a href="#fn\1">[\1]</a></sup>', rendered)
    
    return rendered

def safe_escape(text: str) -> str:
    """Escape < and > for HTML but preserve HTML entities like &#43;."""
    escaped = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
    return re.sub(r'&amp;(#\d+|[a-zA-Z]+);', r'&\1;', escaped)

def render_table(content: str) -> str:
    lines = content.splitlines()
    if not lines:
        return ""
    html_lines = ["<table>"]
    
    # Check if it has a header separator
    has_header = len(lines) > 1 and re.match(r'^\|[\s\-\|]+\|$', lines[1].strip())
    
    if has_header:
        html_lines.append("  <thead>")
        html_lines.append("    <tr>")
        headers = [c.strip() for c in lines[0].strip().strip('|').split('|')]
        for h in headers:
            html_lines.append(f"      <th>{render_markdown_inline(h)}</th>")
        html_lines.append("    </tr>")
        html_lines.append("  </thead>")
        html_lines.append("  <tbody>")
        for line in lines[2:]:
            line_str = line.strip()
            if not line_str or line_str.startswith('<!--'):
                continue
            html_lines.append("    <tr>")
            cells = [c.strip() for c in line_str.strip('|').split('|')]
            for c in cells:
                html_lines.append(f"      <td>{render_markdown_inline(c)}</td>")
            html_lines.append("    </tr>")
    else:
        html_lines.append("  <tbody>")
        for line in lines:
            line_str = line.strip()
            if not line_str or line_str.startswith('<!--'):
                continue
            html_lines.append("    <tr>")
            cells = [c.strip() for c in line_str.strip('|').split('|')]
            for c in cells:
                html_lines.append(f"      <td>{render_markdown_inline(c)}</td>")
            html_lines.append("    </tr>")
            
    html_lines.append("  </tbody>")
    html_lines.append("</table>")
    return "\n".join(html_lines)

def render_block(block: Block | None, repo_root: Path, file_name: str, side: str, row_status: str) -> str:
    if block is None:
        is_divergent = row_status in ("unmatched-en", "unmatched-zh")
        if is_divergent:
            # We must emit a visible marker and a deterministic machine-readable hook
            side_name = "English" if side == "en" else "Chinese"
            return f'<div class="missing-marker missing-{side}" data-missing="{side}">[Missing {side_name} Content]</div>'
        return ""

    content = block.content
    
    # Process image references globally for the block (paragraphs, tables, lists, etc.)
    refs = extract_image_refs(content)
    if refs:
        folder = "FullText-en" if side == "en" else "FullText-zh-sense"
        context_path = repo_root / folder / file_name
        try:
            resolved = resolve_images(refs, context_path, repo_root)
            for ref, res in zip(refs, resolved):
                content = content.replace(f"]({ref.relative_path})", f"]({res.data_uri})")
        except FileNotFoundError as e:
            return f'<div class="error">Image not found: {safe_escape(str(e))}</div>'
    
    if block.block_type == "heading":
        m = re.match(r"^(#{1,6})\s+(.*)$", content)
        if m:
            level = len(m.group(1))
            text = m.group(2)
            return f"<h{level}>{render_markdown_inline(text)}</h{level}>"
        return f"<h3>{render_markdown_inline(content)}</h3>"
        
    elif block.block_type == "paragraph" or block.block_type == "image":
        return render_markdown_text(content)
        
    elif block.block_type == "table":
        return render_table(content)
        
    else:
        return f"<pre>{render_markdown_inline(content)}</pre>"

def render_html(document: AlignedDocument, repo_root: Path) -> str:
    html = [
        "<!DOCTYPE html>",
        '<html lang="en">',
        "<head>",
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
        f"<title>{safe_escape(document.english_file)}</title>",
        "<style>",
        "body { font-family: system-ui, -apple-system, sans-serif; line-height: 1.5; margin: 0; padding: 2rem; color: #333; }",
        ".row { display: flex; gap: 2rem; margin-bottom: 1rem; border-bottom: 1px solid #eee; padding-bottom: 1rem; }",
        ".col { flex: 1; min-width: 0; }",
        "@media (max-width: 768px) { .row { flex-direction: column; gap: 1rem; } }",
        "img { max-width: 100%; height: auto; display: block; margin: 1rem 0; }",
        "table { border-collapse: collapse; width: 100%; margin-bottom: 1rem; }",
        "th, td { border: 1px solid #ccc; padding: 0.5rem; text-align: left; }",
        "th { background: #f9f9f9; }",
        "pre { white-space: pre-wrap; word-wrap: break-word; background: #f4f4f4; padding: 1rem; overflow-x: auto; }",
        ".missing-marker { color: #d32f2f; font-weight: bold; border: 1px dashed #d32f2f; padding: 1rem; text-align: center; background: #ffebee; margin-top: 1rem; }",
        ".divergent-tail { border-left: 4px solid orange; padding-left: 1rem; }",
        "</style>",
        "</head>",
        "<body>"
    ]
    
    for section in document.sections:
        for row in section.rows:
            is_divergent = row.status in ("unmatched-en", "unmatched-zh")
            classes = ["row", f"status-{row.status}"]
            if is_divergent:
                classes.append("divergent-tail")
                
            html.append(f'<div class="{" ".join(classes)}" data-status="{row.status}" data-row-index="{row.row_index}">')
            
            # Left column (EN)
            html.append('  <div class="col col-en">')
            en_html = render_block(row.english_block, repo_root, document.english_file, "en", row.status)
            if en_html:
                html.append("    " + en_html)
            html.append('  </div>')
            
            # Right column (ZH)
            html.append('  <div class="col col-zh">')
            zh_html = render_block(row.chinese_block, repo_root, document.chinese_file, "zh", row.status)
            if zh_html:
                html.append("    " + zh_html)
            html.append('  </div>')
            
            html.append("</div>")

    html.append("</body>")
    html.append("</html>")
    return "\n".join(html) + "\n"

def main() -> None:
    args = parse_args()
    document = build_aligned_document(args.repo_root, args.chapter)
    output_html = render_html(document, args.repo_root)
    
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output_html, encoding="utf-8")
    else:
        print(output_html, end="")

if __name__ == "__main__":
    main()
