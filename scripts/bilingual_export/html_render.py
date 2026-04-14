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

def _render_inline_math(latex: str) -> str:
    r"""Convert a snippet of LaTeX math to lightweight HTML.

    Handles the subset used in this textbook:
      - \\rightarrow  ->  Unicode arrow
      - \\underline{...} -> <u>...</u>
      - \\ (escaped space) -> space
      - bare letters/words -> <em>...</em>

    This function receives the *content between* dollar signs, never the
    dollar signs themselves.
    """
    s = latex.strip()
    # Step 1: LaTeX command replacements
    s = s.replace('\\rightarrow', '→')
    s = s.replace('\\leftarrow', '←')
    s = s.replace('\\leftrightarrow', '↔')
    s = s.replace('\\ ', ' ')
    # Step 2: \underline{...} → <u>...</u>
    s = re.sub(r'\\underline\{([^}]*)\}', r'<u>\1</u>', s)
    # Step 3: Italicize alphabetic tokens outside HTML tags
    parts = re.split(r'(<[^>]+>)', s)
    result = []
    for part in parts:
        if part.startswith('<') and part.endswith('>'):
            result.append(part)
        else:
            result.append(re.sub(r'\b([a-zA-Z]+)\b', r'<em>\1</em>', part))
    return ''.join(result)


_math_stash_counter: int = 0
_math_stash_pending: dict[int, str] = {}


def _preprocess_inline_math(text: str) -> str:
    r"""Replace $...$ inline math with placeholder tokens before markdown-it.

    markdown-it CommonMark does not support $...$ math syntax, so we stash
    the content in sentinel tokens that survive markdown-it's rendering.
    Post-processing will convert them to proper HTML.
    """
    global _math_stash_counter, _math_stash_pending

    def _stash(m):
        global _math_stash_counter
        latex = m.group(1)
        idx = _math_stash_counter
        _math_stash_counter += 1
        _math_stash_pending[idx] = latex
        return f'INLINEMATH{idx}END'

    return re.sub(r'(?<!\$)\$(?!\$)([^$\n]+?)\$(?!\$)', _stash, text)


def _postprocess_inline_math(rendered: str) -> str:
    """Convert INLINEMATH<n>END sentinels back to rendered HTML."""
    global _math_stash_counter, _math_stash_pending
    for idx, latex in _math_stash_pending.items():
        html = _render_inline_math(latex)
        rendered = rendered.replace(f'INLINEMATH{idx}END', html)
    _math_stash_counter = 0
    _math_stash_pending = {}
    return rendered


def _preprocess_footnote_defs(text: str) -> str:
    """Convert footnote definitions [^N]: ... to placeholder tokens before markdown-it.

    markdown-it in CommonMark mode treats [^N]: as a link reference definition and
    silently discards it (since ^N is not a valid link label).  By converting to a
    plain-text sentinel *before* rendering we prevent the content from being eaten.
    """
    return re.sub(r'^\[\^(\d+)\]:\s*(.*)$', r'FNDEF\1END \2', text, flags=re.MULTILINE)


def _postprocess_footnote_defs(rendered: str) -> str:
    """Convert sentinel tokens back to proper footnote definition HTML."""
    return re.sub(
        r'FNDEF(\d+)END',
        r'<a id="fn\1"></a><sup class="footnote-label">[\1]</sup> ',
        rendered,
    )


def render_markdown_text(text: str) -> str:
    """Render markdown block to HTML, preserving &#43; but escaping raw HTML like <EF>."""
    preprocessed = _preprocess_inline_math(text)
    preprocessed = _preprocess_footnote_defs(preprocessed)
    rendered = md_parser.render(preprocessed)
    rendered = _postprocess_inline_math(rendered)
    rendered = _postprocess_footnote_defs(rendered)
    rendered = re.sub(r'&amp;(#\d+|[a-zA-Z]+);', r'&\1;', rendered)
    # Process footnote references
    rendered = re.sub(r'\[\^(\d+)\]', r'<sup class="footnote-ref"><a href="#fn\1">[\1]</a></sup>', rendered)
    
    return rendered

def render_markdown_inline(text: str) -> str:
    """Render markdown inline to HTML, preserving &#43; but escaping raw HTML like <EF>."""
    preprocessed = _preprocess_inline_math(text)
    rendered = md_parser.renderInline(preprocessed)
    rendered = _postprocess_inline_math(rendered)
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

def render_block(block: Block | None, repo_root: Path, file_name: str, side: str, row_status: str, heading_id: str | None = None) -> str:
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
            id_attr = f' id="{heading_id}"' if heading_id else ''
            return f"<h{level}{id_attr}>{render_markdown_inline(text)}</h{level}>"
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
        "blockquote { margin: 0.8rem 0; padding: 0.6rem 1.2rem; border-left: 4px solid #a0a0a0; background: #f5f5f5; color: #555; }",
        "blockquote p { margin: 0; }",
        "/* Sidebar TOC */",
        "#toc-sidebar { position: fixed; top: 0; left: 0; height: 100vh; z-index: 1000; display: flex; align-items: stretch; transform: translateX(-292px); transition: transform 0.25s ease; }",
        "#toc-sidebar.open { transform: translateX(0); }",
        "#toc-content { width: 280px; max-width: 280px; background: #fafafa; border-right: 1px solid #ddd; padding: 1.5rem 1rem; overflow-y: auto; font-size: 0.85rem; box-shadow: 2px 0 8px rgba(0,0,0,0.05); }",
        "#toc-content h3 { margin: 0 0 0.8rem 0; font-size: 1rem; color: #333; border-bottom: 1px solid #ddd; padding-bottom: 0.5rem; }",
        "#toc-list { list-style: none; padding: 0; margin: 0; }",
        "#toc-list li { margin-bottom: 0.3rem; }",
        "#toc-list a { color: #555; text-decoration: none; display: block; padding: 0.2rem 0.4rem; border-radius: 3px; }",
        "#toc-list a:hover { background: #e8e8e8; color: #222; }",
        "#toc-tab { writing-mode: vertical-rl; text-orientation: mixed; background: #555; color: #fff; padding: 1rem 0.13rem; cursor: pointer; font-size: 0.9rem; letter-spacing: 2px; border-radius: 0 4px 4px 0; user-select: none; align-self: flex-end; margin-bottom: 2rem; opacity: 0.2; transition: opacity 0.2s ease; }",
        "#toc-tab:hover { background: #333; opacity: 0.7; }",
        "</style>",
        "</head>",
        "<body>"
    ]
    
    # Initialize heading counter and TOC entries collection
    heading_counter = 0
    toc_entries = []  # list of (level, text, id)
    
    for section in document.sections:
        for row in section.rows:
            is_divergent = row.status in ("unmatched-en", "unmatched-zh")
            classes = ["row", f"status-{row.status}"]
            if is_divergent:
                classes.append("divergent-tail")
                
            html.append(f'<div class="{" ".join(classes)}" data-status="{row.status}" data-row-index="{row.row_index}">')
            
            # Detect heading for TOC
            heading_id = None
            if row.english_block and row.english_block.block_type == "heading":
                heading_id = f"heading-{heading_counter}"
                # Extract heading text for TOC
                heading_content = row.english_block.content
                m = re.match(r"^(#{1,6})\s+(.*)$", heading_content)
                if m:
                    heading_text = m.group(2)
                    heading_level = len(m.group(1))
                else:
                    heading_text = heading_content
                    heading_level = 3
                toc_entries.append((heading_level, heading_text, heading_id))
                heading_counter += 1
            
            # Left column (EN)
            html.append('  <div class="col col-en">')
            en_html = render_block(row.english_block, repo_root, document.english_file, "en", row.status, heading_id=heading_id)
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

    # Build TOC sidebar HTML
    toc_items = []
    for level, text, hid in toc_entries:
        indent = (level - 1) * 1.0  # rem per level
        clean_text = render_markdown_inline(text)
        toc_items.append(f'<li style="margin-left:{indent}rem"><a href="#{hid}">{clean_text}</a></li>')

    html.append(f'''<div id="toc-sidebar">
  <div id="toc-content">
    <h3>Table of Contents</h3>
    <ul id="toc-list">
      {"".join(toc_items)}
    </ul>
  </div>
  <div id="toc-tab" onclick="toggleToc()">≫</div>
</div>''')

    # Add sidebar JS
    html.append('''<script>
function toggleToc() {
  var sidebar = document.getElementById('toc-sidebar');
  sidebar.classList.toggle('open');
  var tab = document.getElementById('toc-tab');
  tab.textContent = sidebar.classList.contains('open') ? '≪' : '≫';
}
document.addEventListener('DOMContentLoaded', function() {
  var links = document.querySelectorAll('#toc-list a');
  links.forEach(function(link) {
    link.addEventListener('click', function(e) {
      e.preventDefault();
      var target = document.getElementById(this.getAttribute('href').substring(1));
      if (target) {
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });
});
</script>''')

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
