#!/usr/bin/env python3

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.bilingual_export.align import build_aligned_document
from scripts.bilingual_export.discovery import build_pair_manifest
from scripts.bilingual_export.html_render import render_html
from scripts.bilingual_export.word_render import render_docx


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Batch export bilingual chapters to HTML and Word with manifest and report.",
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Repository root containing FullText-en and FullText-zh-sense.",
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        required=True,
        help="Root output directory; html/ and word/ subdirs will be created here.",
    )
    parser.add_argument(
        "--chapter",
        action="append",
        default=[],
        help="Limit to one or more English filenames (repeatable). Default: all 17.",
    )
    parser.add_argument(
        "--skip-html",
        action="store_true",
        help="Skip HTML rendering.",
    )
    parser.add_argument(
        "--skip-word",
        action="store_true",
        help="Skip Word rendering.",
    )
    return parser.parse_args()


def run_export(
    repo_root: Path,
    output_root: Path,
    chapter_filter: list[str] | None,
    skip_html: bool,
    skip_word: bool,
) -> list[dict]:
    html_dir = output_root / "html"
    word_dir = output_root / "word"

    manifest = build_pair_manifest(repo_root)
    if chapter_filter:
        wanted = set(chapter_filter)
        manifest = [item for item in manifest if item.english_file in wanted]

    entries: list[dict] = []
    for pair in manifest:
        doc = build_aligned_document(repo_root, pair.english_file)

        html_path: Path | None = None
        word_path: Path | None = None
        html_bytes: int = 0
        word_bytes: int = 0
        warnings: list[str] = list(doc.warnings)

        if not skip_html:
            html_path = html_dir / pair.english_file.replace(".md", ".html")
            html_dir.mkdir(parents=True, exist_ok=True)
            html_content = render_html(doc, repo_root)
            html_path.write_text(html_content, encoding="utf-8")
            html_bytes = html_path.stat().st_size

        if not skip_word:
            word_path = word_dir / pair.english_file.replace(".md", ".docx")
            word_dir.mkdir(parents=True, exist_ok=True)
            render_docx(doc, repo_root, word_path)
            word_bytes = word_path.stat().st_size

        if doc.status in ("incomplete", "degraded") and pair.status not in ("incomplete",):
            warnings.append(f"alignment-status: {doc.status}")

        entries.append({
            "english_file": pair.english_file,
            "chinese_file": pair.chinese_file,
            "pair_status": pair.status,
            "alignment_status": doc.status,
            "html_output": str(html_path) if html_path else None,
            "word_output": str(word_path) if word_path else None,
            "html_bytes": html_bytes,
            "word_bytes": word_bytes,
            "warnings": warnings,
        })

    return entries


def build_report(entries: list[dict]) -> str:
    exact = [e for e in entries if e["pair_status"] == "exact"]
    wrapping = [e for e in entries if e["pair_status"] == "wrapping-drift"]
    divergent = [e for e in entries if e["pair_status"] in ("divergent", "incomplete")]
    image_asym = [e for e in entries if any("image-count-asymmetry" in w for w in e["warnings"])]

    lines: list[str] = []
    lines.append("# Bilingual Export Report")
    lines.append("")
    lines.append(f"Total chapters: {len(entries)}")
    lines.append(f"Exact match: {len(exact)}")
    lines.append(f"Wrapping drift: {len(wrapping)}")
    lines.append(f"Divergent / Incomplete: {len(divergent)}")
    lines.append(f"Image asymmetry: {len(image_asym)}")
    lines.append("")

    if exact:
        lines.append("## Exact Match")
        for e in exact:
            lines.append(f"- {e['english_file']}")
        lines.append("")

    if wrapping:
        lines.append("## Wrapping Drift")
        for e in wrapping:
            lines.append(f"- {e['english_file']}")
        lines.append("")

    if divergent:
        lines.append("## Divergent / Incomplete")
        for e in divergent:
            lines.append(f"- {e['english_file']} (status: {e['pair_status']}, alignment: {e['alignment_status']})")
        lines.append("")

    if image_asym:
        lines.append("## Image Asymmetry")
        for e in image_asym:
            asym_warnings = [w for w in e["warnings"] if "image-count-asymmetry" in w]
            lines.append(f"- {e['english_file']}: {', '.join(asym_warnings)}")
        lines.append("")

    lines.append("## Per-Chapter Details")
    lines.append("")
    for e in entries:
        lines.append(f"### {e['english_file']}")
        lines.append(f"- Chinese: {e['chinese_file']}")
        lines.append(f"- Pair status: {e['pair_status']}")
        lines.append(f"- Alignment status: {e['alignment_status']}")
        if e["html_output"]:
            lines.append(f"- HTML: {e['html_output']} ({e['html_bytes']} bytes)")
        if e["word_output"]:
            lines.append(f"- Word: {e['word_output']} ({e['word_bytes']} bytes)")
        if e["warnings"]:
            lines.append(f"- Warnings: {', '.join(e['warnings'])}")
        lines.append("")

    return "\n".join(lines)


def main() -> None:
    args = parse_args()
    entries = run_export(
        repo_root=args.repo_root,
        output_root=args.output_root,
        chapter_filter=args.chapter or None,
        skip_html=args.skip_html,
        skip_word=args.skip_word,
    )

    manifest_path = args.output_root / "manifest.json"
    args.output_root.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(entries, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    report = build_report(entries)
    report_path = args.output_root / "report.md"
    report_path.write_text(report, encoding="utf-8")

    print(f"Export complete: {len(entries)} chapters", file=sys.stderr)
    print(f"  Manifest: {manifest_path}", file=sys.stderr)
    print(f"  Report:   {report_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
