import re
from pathlib import Path

from scripts.bilingual_export.align import build_aligned_document
from scripts.bilingual_export.html_render import render_html

REPO_ROOT = Path(__file__).resolve().parents[1]

def test_chapter_02_html_render():
    doc = build_aligned_document(REPO_ROOT, "02-Argument-Analysis-Identifying-Conclusions-and-Reasons.md")
    html = render_html(doc, REPO_ROOT)
    
    evidence_path = REPO_ROOT / ".sisyphus/evidence/task-5-html-standalone.txt"
    evidence_path.parent.mkdir(parents=True, exist_ok=True)
    evidence_path.write_text(html, encoding="utf-8")
    
    assert "<!DOCTYPE html>" in html
    assert '<html lang="en">' in html
    assert '<style>' in html
    assert '</style>' in html
    
    assert "<link rel=" not in html
    assert "<script" not in html
    
    assert "@media (max-width: 768px)" in html
    assert "flex-direction: column" in html
    
    assert '<div class="row ' in html
    assert '<div class="col col-en">' in html
    assert '<div class="col col-zh">' in html
    
    assert "<h1>CHAPTER 2 Argument Analysis: Identifying Conclusions and Reasons</h1>" in html
    assert "<h2>The Murder Trial</h2>" in html
    assert "<h3>Criteria (or Cues) for Identifying Conclusions</h3>" in html
    
    assert "<em>F</em>" in html
    assert "<em>FRISCO</em>" in html
    assert "*F*" not in html
    
    images = re.findall(r'<img src="data:image/[a-zA-Z\+]+;base64,[^"]+"', html)
    assert len(images) == 84, f"Expected 84 embedded base64 images in Chapter 02, found {len(images)}"

def test_chapter_09_html_render():
    doc = build_aligned_document(REPO_ROOT, "09-Best-Explanation-and-Causal-Inference-Argument-and-Writing-Strategy.md")
    html = render_html(doc, REPO_ROOT)
    
    evidence_path = REPO_ROOT / ".sisyphus/evidence/task-5-html-incomplete.txt"
    evidence_path.write_text(html, encoding="utf-8")
    
    # Ch09 is now fully matched — verify no missing content markers
    assert 'data-missing="zh"' not in html
    assert '[Missing Chinese Content]' not in html
    
    assert '&#43;' in html
    assert '&amp;#43;' not in html

    assert '&lt;EF&gt;' in html
    assert '<EF>' not in html
    
    assert '[^' not in html
    assert '<sup class="footnote-ref">' in html
    assert '<a id="fn' in html

def test_chapter_05_no_image_leaks():
    doc = build_aligned_document(REPO_ROOT, "05-Deduction-Class-Logic.md")
    html = render_html(doc, REPO_ROOT)
    
    leaked_images = re.findall(r'<img[^>]+src="(?!data:image)[^"]+"', html)
    assert not leaked_images, f"Found leaked non-data image sources: {leaked_images}"
    
    data_images = re.findall(r'<img[^>]+src="data:image/[a-zA-Z\+]+;base64,[^"]+"', html)
    assert len(data_images) > 50, f"Expected many embedded images in Chapter 05, found {len(data_images)}"
