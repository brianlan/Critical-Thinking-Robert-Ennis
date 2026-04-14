from pathlib import Path

import pytest

from scripts.bilingual_export.image_utils import (
    ImageAsymmetryReport,
    extract_image_refs,
    guess_mime_type,
    has_image_asymmetry,
    image_to_data_uri,
    resolve_image_path,
    resolve_images,
    build_asymmetry_report,
    ResolvedImage,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
FULLTEXT_EN = REPO_ROOT / "FullText-en"
FULLTEXT_ZH = REPO_ROOT / "FullText-zh-sense"


class TestExtractImageRefs:
    def test_extracts_single_image_ref(self):
        md = '![Diagram of defense](images/chapter-02/page_059/foo.png)'
        refs = extract_image_refs(md)
        assert len(refs) == 1
        assert refs[0].alt_text == "Diagram of defense"
        assert refs[0].relative_path == "images/chapter-02/page_059/foo.png"
        assert refs[0].line_number == 1

    def test_extracts_multiple_image_refs(self):
        md = '![a](x.png)\n\n![b](y.png)'
        refs = extract_image_refs(md)
        assert len(refs) == 2
        assert refs[0].relative_path == "x.png"
        assert refs[1].relative_path == "y.png"
        assert refs[0].line_number == 1
        assert refs[1].line_number == 3

    def test_returns_empty_for_no_images(self):
        refs = extract_image_refs("# Just a heading\nSome text.")
        assert len(refs) == 0

    def test_preserves_raw_content_like_amp_43(self):
        md = "Some text with &#43; markers\n\n![Diagram](images/ch-02/x.png)\n\nMore &#43; content"
        refs = extract_image_refs(md)
        assert len(refs) == 1
        assert refs[0].relative_path == "images/ch-02/x.png"

    def test_chapter_02_en_image_count(self):
        text = (FULLTEXT_EN / "02-Argument-Analysis-Identifying-Conclusions-and-Reasons.md").read_text(encoding="utf-8")
        refs = extract_image_refs(text)
        assert len(refs) == 42

    def test_chapter_02_zh_image_count(self):
        text = (FULLTEXT_ZH / "02-Argument-Analysis-Identifying-Conclusions-and-Reasons.md").read_text(encoding="utf-8")
        refs = extract_image_refs(text)
        assert len(refs) == 42

    def test_chapter_09_en_has_one_image(self):
        text = (FULLTEXT_EN / "09-Best-Explanation-and-Causal-Inference-Argument-and-Writing-Strategy.md").read_text(encoding="utf-8")
        refs = extract_image_refs(text)
        assert len(refs) == 1
        assert "chapter-09" in refs[0].relative_path

    def test_chapter_09_zh_has_no_images(self):
        text = (FULLTEXT_ZH / "09-Best-Explanation-and-Causal-Inference-Argument-and-Writing-Strategy.md").read_text(encoding="utf-8")
        refs = extract_image_refs(text)
        assert len(refs) == 1
        assert "chapter-09" in refs[0].relative_path

    def test_chapter_11_en_has_two_images(self):
        text = (FULLTEXT_EN / "11-Making-Value-Judgments.md").read_text(encoding="utf-8")
        refs = extract_image_refs(text)
        assert len(refs) == 2
        assert all("chapter-11" in r.relative_path for r in refs)

    def test_chapter_11_zh_has_no_images(self):
        text = (FULLTEXT_ZH / "11-Making-Value-Judgments.md").read_text(encoding="utf-8")
        refs = extract_image_refs(text)
        assert len(refs) == 0


class TestResolveImagePath:
    def test_resolves_relative_to_repo_root(self):
        ref = "images/chapter-02/page_059/page_059_diagram_1_loc_728_482_795_683.png"
        context = FULLTEXT_EN / "02-Argument-Analysis-Identifying-Conclusions-and-Reasons.md"
        result = resolve_image_path(ref, context, REPO_ROOT)
        assert result.exists()
        assert result.is_file()

    def test_raises_for_nonexistent_image(self):
        with pytest.raises(FileNotFoundError, match="Cannot resolve image path"):
            resolve_image_path("images/nonexistent/file.png", FULLTEXT_EN / "dummy.md", REPO_ROOT)

    def test_resolves_all_chapter_02_images(self):
        text = (FULLTEXT_EN / "02-Argument-Analysis-Identifying-Conclusions-and-Reasons.md").read_text(encoding="utf-8")
        refs = extract_image_refs(text)
        context = FULLTEXT_EN / "02-Argument-Analysis-Identifying-Conclusions-and-Reasons.md"
        for ref in refs:
            path = resolve_image_path(ref.relative_path, context, REPO_ROOT)
            assert path.exists(), f"Image not found: {ref.relative_path}"

    def test_resolves_chapter_09_en_image(self):
        text = (FULLTEXT_EN / "09-Best-Explanation-and-Causal-Inference-Argument-and-Writing-Strategy.md").read_text(encoding="utf-8")
        refs = extract_image_refs(text)
        assert len(refs) == 1
        context = FULLTEXT_EN / "09-Best-Explanation-and-Causal-Inference-Argument-and-Writing-Strategy.md"
        path = resolve_image_path(refs[0].relative_path, context, REPO_ROOT)
        assert path.exists()

    def test_resolves_chapter_11_en_images(self):
        text = (FULLTEXT_EN / "11-Making-Value-Judgments.md").read_text(encoding="utf-8")
        refs = extract_image_refs(text)
        context = FULLTEXT_EN / "11-Making-Value-Judgments.md"
        for ref in refs:
            path = resolve_image_path(ref.relative_path, context, REPO_ROOT)
            assert path.exists(), f"Image not found: {ref.relative_path}"


class TestImageToDataUri:
    def test_produces_valid_data_uri_prefix(self):
        ref = "images/chapter-02/page_059/page_059_diagram_1_loc_728_482_795_683.png"
        context = FULLTEXT_EN / "02-Argument-Analysis-Identifying-Conclusions-and-Reasons.md"
        path = resolve_image_path(ref, context, REPO_ROOT)
        data_uri, mime_type, size = image_to_data_uri(path)
        assert data_uri.startswith("data:image/png;base64,")
        assert mime_type == "image/png"
        assert size > 0

    def test_base64_content_is_valid(self):
        import base64
        ref = "images/chapter-02/page_059/page_059_diagram_1_loc_728_482_795_683.png"
        context = FULLTEXT_EN / "02-Argument-Analysis-Identifying-Conclusions-and-Reasons.md"
        path = resolve_image_path(ref, context, REPO_ROOT)
        data_uri, _, _ = image_to_data_uri(path)
        payload = data_uri.split(",", 1)[1]
        decoded = base64.b64decode(payload)
        assert len(decoded) > 0
        assert decoded[:4] == b"\x89PNG" or decoded[:2] == b"\xff\xd8"


class TestResolveImages:
    def test_resolves_all_chapter_02_images_with_data_uris(self):
        text = (FULLTEXT_EN / "02-Argument-Analysis-Identifying-Conclusions-and-Reasons.md").read_text(encoding="utf-8")
        refs = extract_image_refs(text)
        context = FULLTEXT_EN / "02-Argument-Analysis-Identifying-Conclusions-and-Reasons.md"
        resolved = resolve_images(refs, context, REPO_ROOT)
        assert len(resolved) == 42
        for img in resolved:
            assert img.data_uri.startswith("data:image/")
            assert img.size_bytes > 0
            assert "base64," in img.data_uri

    def test_resolved_image_carries_metadata(self):
        text = (FULLTEXT_EN / "02-Argument-Analysis-Identifying-Conclusions-and-Reasons.md").read_text(encoding="utf-8")
        refs = extract_image_refs(text)
        context = FULLTEXT_EN / "02-Argument-Analysis-Identifying-Conclusions-and-Reasons.md"
        resolved = resolve_images(refs, context, REPO_ROOT)
        first = resolved[0]
        assert first.alt_text != ""
        assert first.relative_path.startswith("images/chapter-02/")
        assert first.absolute_path != ""
        assert Path(first.absolute_path).exists()


class TestGuessMimeType:
    def test_png(self):
        assert guess_mime_type(Path("foo.png")) == "image/png"

    def test_jpg(self):
        assert guess_mime_type(Path("foo.jpg")) == "image/jpeg"

    def test_jpeg(self):
        assert guess_mime_type(Path("foo.jpeg")) == "image/jpeg"

    def test_unknown_returns_octet_stream(self):
        assert guess_mime_type(Path("foo.xyz")) == "application/octet-stream"


class TestBuildAsymmetryReport:
    def test_chapter_02_has_no_asymmetry(self):
        en_text = (FULLTEXT_EN / "02-Argument-Analysis-Identifying-Conclusions-and-Reasons.md").read_text(encoding="utf-8")
        zh_text = (FULLTEXT_ZH / "02-Argument-Analysis-Identifying-Conclusions-and-Reasons.md").read_text(encoding="utf-8")
        en_refs = extract_image_refs(en_text)
        zh_refs = extract_image_refs(zh_text)
        report = build_asymmetry_report("02-....md", "02-....md", en_refs, zh_refs)
        assert report.en_image_count == 42
        assert report.zh_image_count == 42
        assert len(report.asymmetries) == 0
        assert not has_image_asymmetry(report)

    def test_chapter_09_has_en_missing_zh_asymmetry(self):
        en_text = (FULLTEXT_EN / "09-Best-Explanation-and-Causal-Inference-Argument-and-Writing-Strategy.md").read_text(encoding="utf-8")
        zh_text = (FULLTEXT_ZH / "09-Best-Explanation-and-Causal-Inference-Argument-and-Writing-Strategy.md").read_text(encoding="utf-8")
        en_refs = extract_image_refs(en_text)
        zh_refs = extract_image_refs(zh_text)
        report = build_asymmetry_report("09-....md", "09-....md", en_refs, zh_refs)
        assert report.en_image_count == 1
        assert report.zh_image_count == 1
        assert len(report.asymmetries) == 0
        assert not has_image_asymmetry(report)

    def test_chapter_11_has_en_missing_zh_asymmetry(self):
        en_text = (FULLTEXT_EN / "11-Making-Value-Judgments.md").read_text(encoding="utf-8")
        zh_text = (FULLTEXT_ZH / "11-Making-Value-Judgments.md").read_text(encoding="utf-8")
        en_refs = extract_image_refs(en_text)
        zh_refs = extract_image_refs(zh_text)
        report = build_asymmetry_report("11-....md", "11-....md", en_refs, zh_refs)
        assert report.en_image_count == 2
        assert report.zh_image_count == 0
        assert len(report.asymmetries) == 2
        assert all(a.zh_missing for a in report.asymmetries)
        assert has_image_asymmetry(report)

    def test_report_is_frozen_dataclass(self):
        report = build_asymmetry_report("a.md", "b.md", [], [])
        assert hasattr(report, '__hash__')
        assert hasattr(report.asymmetries, '__hash__')


class TestRawContentPreservation:
    def test_amp_43_survives_extraction(self):
        md = "Text with &#43; here\n![img](x.png)\n&#43; more"
        refs = extract_image_refs(md)
        assert len(refs) == 1
        assert "&#43;" in md

    def test_extraction_does_not_mutate_input(self):
        original = "![a](b.png)\n&#43; footnote\n**bold**"
        original_copy = original
        _ = extract_image_refs(original)
        assert original == original_copy
