#!/usr/bin/env python3

import argparse
import json
import re
from dataclasses import asdict, dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

from scripts.bilingual_export.align import ParsedDocument, build_aligned_document, parse_markdown
from scripts.bilingual_export.discovery import ChapterPairAudit, build_pair_manifest


REPORT_HEADING = "# HTML Structural Validation Report"
STYLE_URL_RE = re.compile(r"url\(([^)]+)\)")


@dataclass(frozen=True)
class SideCounts:
    heading_count: int
    heading_levels: dict[str, int]
    table_count: int
    image_count: int
    data_uri_image_count: int


@dataclass(frozen=True)
class ChapterExpectation:
    english_file: str
    chinese_file: str
    pair_status: str
    alignment_status: str
    english: SideCounts
    chinese: SideCounts
    row_status_counts: dict[str, int]
    missing_markers: dict[str, int]
    warnings: list[str]
    html_output: str


@dataclass(frozen=True)
class HtmlSideCounts:
    heading_count: int
    heading_levels: dict[str, int]
    table_count: int
    image_count: int
    data_uri_image_count: int


@dataclass(frozen=True)
class HtmlObservation:
    english: HtmlSideCounts
    chinese: HtmlSideCounts
    row_status_counts: dict[str, int]
    missing_markers: dict[str, int]
    link_tag_count: int
    script_tag_count: int
    asset_dependencies: list[str]
    style_dependencies: list[str]


@dataclass(frozen=True)
class ChapterValidationResult:
    english_file: str
    chinese_file: str
    pair_status: str
    alignment_status: str
    html_path: str
    passed: bool
    checks: dict[str, bool]
    expected: ChapterExpectation
    actual: HtmlObservation
    issues: list[str]


@dataclass(frozen=True)
class ValidationReport:
    output_root: str
    manifest_path: str
    report_path: str
    chapter_count: int
    passed: bool
    failed_chapters: list[str]
    chapters: list[ChapterValidationResult]


class HtmlStructureParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=False)
        self._side_stack: list[str | None] = []
        self._tag_stack: list[str] = []
        self._style_depth = 0
        self.english_heading_levels: dict[str, int] = {}
        self.chinese_heading_levels: dict[str, int] = {}
        self.english_table_count = 0
        self.chinese_table_count = 0
        self.english_image_count = 0
        self.chinese_image_count = 0
        self.english_data_uri_image_count = 0
        self.chinese_data_uri_image_count = 0
        self.row_status_counts: dict[str, int] = {}
        self.missing_markers = {"en": 0, "zh": 0}
        self.link_tag_count = 0
        self.script_tag_count = 0
        self.asset_dependencies: list[str] = []
        self.style_dependencies: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_map = {name: value or "" for name, value in attrs}
        current_side = self._side_stack[-1] if self._side_stack else None
        next_side = current_side
        class_names = set(attr_map.get("class", "").split())
        if {"col", "col-en"}.issubset(class_names):
            next_side = "en"
        elif {"col", "col-zh"}.issubset(class_names):
            next_side = "zh"

        if tag == "style":
            self._style_depth += 1
        if tag == "div" and "row" in class_names and attr_map.get("data-status"):
            status = attr_map["data-status"]
            self.row_status_counts[status] = self.row_status_counts.get(status, 0) + 1
        if tag == "div" and "missing-marker" in class_names and attr_map.get("data-missing") in self.missing_markers:
            self.missing_markers[attr_map["data-missing"]] += 1

        if tag in {"h1", "h2", "h3", "h4", "h5", "h6"} and current_side in {"en", "zh"}:
            self._increment_heading(current_side, tag)
        elif tag == "table" and current_side in {"en", "zh"}:
            if current_side == "en":
                self.english_table_count += 1
            else:
                self.chinese_table_count += 1
        elif tag == "img":
            self._handle_image(current_side, attr_map)
        elif tag == "link":
            self.link_tag_count += 1
            href = attr_map.get("href")
            if href:
                self.asset_dependencies.append(f"link:{href}")
        elif tag == "script":
            self.script_tag_count += 1
            src = attr_map.get("src")
            if src:
                self.asset_dependencies.append(f"script:{src}")

        href = attr_map.get("href")
        if href and not href.startswith("#"):
            self.asset_dependencies.append(f"href:{href}")

        self._side_stack.append(next_side)
        self._tag_stack.append(tag)

    def handle_endtag(self, tag: str) -> None:
        if self._tag_stack:
            self._tag_stack.pop()
        if self._side_stack:
            self._side_stack.pop()
        if tag == "style" and self._style_depth > 0:
            self._style_depth -= 1

    def handle_data(self, data: str) -> None:
        if self._style_depth == 0:
            return
        for match in STYLE_URL_RE.finditer(data):
            candidate = match.group(1).strip().strip('"\'')
            if candidate and not candidate.startswith("data:"):
                self.style_dependencies.append(candidate)

    def _increment_heading(self, side: str, tag: str) -> None:
        target = self.english_heading_levels if side == "en" else self.chinese_heading_levels
        target[tag] = target.get(tag, 0) + 1

    def _handle_image(self, side: str | None, attrs: dict[str, str]) -> None:
        src = attrs.get("src", "")
        if side == "en":
            self.english_image_count += 1
            if src.startswith("data:image/"):
                self.english_data_uri_image_count += 1
        elif side == "zh":
            self.chinese_image_count += 1
            if src.startswith("data:image/"):
                self.chinese_data_uri_image_count += 1
        if src and not src.startswith("data:image/"):
            self.asset_dependencies.append(f"img:{src}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate generated bilingual HTML outputs structurally.")
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--json-output", type=Path, required=True)
    parser.add_argument("--report-output", type=Path, required=True)
    return parser.parse_args()


def validate_output_root(repo_root: Path, output_root: Path) -> ValidationReport:
    manifest_path = output_root / "manifest.json"
    report_path = output_root / "report.md"
    manifest_entries = json.loads(manifest_path.read_text(encoding="utf-8"))
    canonical_report = report_path.read_text(encoding="utf-8")
    pair_manifest = {item.english_file: item for item in build_pair_manifest(repo_root)}

    chapters: list[ChapterValidationResult] = []
    for entry in manifest_entries:
        chapters.append(
            validate_chapter(
                repo_root=repo_root,
                entry=entry,
                source_pair=pair_manifest[entry["english_file"]],
                canonical_report=canonical_report,
            )
        )

    failed = [chapter.english_file for chapter in chapters if not chapter.passed]
    return ValidationReport(
        output_root=str(output_root),
        manifest_path=str(manifest_path),
        report_path=str(report_path),
        chapter_count=len(chapters),
        passed=not failed,
        failed_chapters=failed,
        chapters=chapters,
    )


def validate_chapter(repo_root: Path, entry: dict[str, Any], source_pair: ChapterPairAudit, canonical_report: str) -> ChapterValidationResult:
    english_file = str(entry["english_file"])
    chinese_file = str(entry["chinese_file"])
    html_path = repo_root / str(entry["html_output"])
    expected = build_expectation(repo_root, entry, source_pair)
    actual = inspect_html(html_path)

    checks: dict[str, bool] = {}
    issues: list[str] = []

    checks["manifest_report_agree"] = report_contains_expected_lines(entry, canonical_report)
    checks["english_heading_count"] = actual.english.heading_count == expected.english.heading_count
    checks["chinese_heading_count"] = actual.chinese.heading_count == expected.chinese.heading_count
    checks["english_table_count"] = actual.english.table_count == expected.english.table_count
    checks["chinese_table_count"] = actual.chinese.table_count == expected.chinese.table_count
    checks["english_image_count"] = actual.english.image_count == expected.english.image_count
    checks["chinese_image_count"] = actual.chinese.image_count == expected.chinese.image_count
    checks["english_data_uri_count"] = actual.english.data_uri_image_count == expected.english.image_count
    checks["chinese_data_uri_count"] = actual.chinese.data_uri_image_count == expected.chinese.image_count
    checks["row_status_counts"] = actual.row_status_counts == expected.row_status_counts
    checks["missing_markers"] = actual.missing_markers == expected.missing_markers
    checks["no_link_tags"] = actual.link_tag_count == 0
    checks["no_script_tags"] = actual.script_tag_count == 0
    checks["no_external_assets"] = not actual.asset_dependencies and not actual.style_dependencies

    if not checks["manifest_report_agree"]:
        issues.append("report.md does not contain the expected canonical status lines")
    _maybe_add_issue(issues, checks["english_heading_count"], f"English headings expected {expected.english.heading_count}, got {actual.english.heading_count}")
    _maybe_add_issue(issues, checks["chinese_heading_count"], f"Chinese headings expected {expected.chinese.heading_count}, got {actual.chinese.heading_count}")
    _maybe_add_issue(issues, checks["english_table_count"], f"English tables expected {expected.english.table_count}, got {actual.english.table_count}")
    _maybe_add_issue(issues, checks["chinese_table_count"], f"Chinese tables expected {expected.chinese.table_count}, got {actual.chinese.table_count}")
    _maybe_add_issue(issues, checks["english_image_count"], f"English images expected {expected.english.image_count}, got {actual.english.image_count}")
    _maybe_add_issue(issues, checks["chinese_image_count"], f"Chinese images expected {expected.chinese.image_count}, got {actual.chinese.image_count}")
    _maybe_add_issue(issues, checks["english_data_uri_count"], f"English data URI images expected {expected.english.image_count}, got {actual.english.data_uri_image_count}")
    _maybe_add_issue(issues, checks["chinese_data_uri_count"], f"Chinese data URI images expected {expected.chinese.image_count}, got {actual.chinese.data_uri_image_count}")
    _maybe_add_issue(issues, checks["row_status_counts"], f"Row statuses expected {expected.row_status_counts}, got {actual.row_status_counts}")
    _maybe_add_issue(issues, checks["missing_markers"], f"Missing markers expected {expected.missing_markers}, got {actual.missing_markers}")
    _maybe_add_issue(issues, checks["no_link_tags"], f"Found {actual.link_tag_count} <link> tag(s)")
    _maybe_add_issue(issues, checks["no_script_tags"], f"Found {actual.script_tag_count} <script> tag(s)")
    if not checks["no_external_assets"]:
        problems = actual.asset_dependencies + actual.style_dependencies
        issues.append("Standalone asset dependency violation: " + ", ".join(problems))

    return ChapterValidationResult(
        english_file=english_file,
        chinese_file=chinese_file,
        pair_status=str(entry["pair_status"]),
        alignment_status=str(entry["alignment_status"]),
        html_path=str(html_path),
        passed=all(checks.values()),
        checks=checks,
        expected=expected,
        actual=actual,
        issues=issues,
    )


def build_expectation(repo_root: Path, entry: dict[str, Any], source_pair: ChapterPairAudit) -> ChapterExpectation:
    english_doc = parse_markdown(Path(source_pair.english.path))
    chinese_doc = parse_markdown(Path(source_pair.chinese.path))
    aligned_doc = build_aligned_document(repo_root, str(entry["english_file"]))

    row_status_counts: dict[str, int] = {}
    missing_markers = {"en": 0, "zh": 0}
    for section in aligned_doc.sections:
        for row in section.rows:
            row_status_counts[row.status] = row_status_counts.get(row.status, 0) + 1
            if row.status in {"unmatched-en", "unmatched-zh"}:
                if row.english_block is None:
                    missing_markers["en"] += 1
                if row.chinese_block is None:
                    missing_markers["zh"] += 1

    return ChapterExpectation(
        english_file=str(entry["english_file"]),
        chinese_file=str(entry["chinese_file"]),
        pair_status=str(entry["pair_status"]),
        alignment_status=str(entry["alignment_status"]),
        english=summarize_source_side(english_doc),
        chinese=summarize_source_side(chinese_doc),
        row_status_counts=row_status_counts,
        missing_markers=missing_markers,
        warnings=[str(item) for item in list(entry.get("warnings", []))],
        html_output=str(entry["html_output"]),
    )


def summarize_source_side(document: ParsedDocument) -> SideCounts:
    heading_levels: dict[str, int] = {}
    table_count = 0
    image_count = 0
    for block in document.blocks:
        if block.block_type == "heading":
            level = f"h{len(block.content.split()[0])}"
            heading_levels[level] = heading_levels.get(level, 0) + 1
        elif block.block_type == "table":
            table_count += 1
        image_count += len(re.findall(r"!\[[^\]]*\]\([^\)]+\)", block.content))

    return SideCounts(
        heading_count=sum(heading_levels.values()),
        heading_levels=heading_levels,
        table_count=table_count,
        image_count=image_count,
        data_uri_image_count=image_count,
    )


def inspect_html(html_path: Path) -> HtmlObservation:
    parser = HtmlStructureParser()
    html_text = html_path.read_text(encoding="utf-8")
    parser.feed(html_text)
    parser.close()

    return HtmlObservation(
        english=HtmlSideCounts(
            heading_count=sum(parser.english_heading_levels.values()),
            heading_levels=dict(sorted(parser.english_heading_levels.items())),
            table_count=parser.english_table_count,
            image_count=parser.english_image_count,
            data_uri_image_count=parser.english_data_uri_image_count,
        ),
        chinese=HtmlSideCounts(
            heading_count=sum(parser.chinese_heading_levels.values()),
            heading_levels=dict(sorted(parser.chinese_heading_levels.items())),
            table_count=parser.chinese_table_count,
            image_count=parser.chinese_image_count,
            data_uri_image_count=parser.chinese_data_uri_image_count,
        ),
        row_status_counts=dict(sorted(parser.row_status_counts.items())),
        missing_markers=parser.missing_markers,
        link_tag_count=parser.link_tag_count,
        script_tag_count=parser.script_tag_count,
        asset_dependencies=sorted(set(filter_disallowed_assets(parser.asset_dependencies))),
        style_dependencies=sorted(set(filter_disallowed_assets(parser.style_dependencies))),
    )


def filter_disallowed_assets(values: list[str]) -> list[str]:
    disallowed: list[str] = []
    for value in values:
        payload = value.split(":", 1)[1] if ":" in value else value
        candidate = payload.strip().strip('"\'')
        if not candidate or candidate.startswith("#") or candidate.startswith("data:"):
            continue
        if candidate.startswith("http://") or candidate.startswith("https://"):
            disallowed.append(value)
            continue
        if candidate.startswith("/") or candidate.startswith("./") or candidate.startswith("../"):
            disallowed.append(value)
            continue
        if "://" not in candidate and not candidate.startswith("mailto:"):
            disallowed.append(value)
    return disallowed


def report_contains_expected_lines(entry: dict[str, Any], report_text: str) -> bool:
    english_file = str(entry["english_file"])
    chinese_file = str(entry["chinese_file"])
    pair_status = str(entry["pair_status"])
    alignment_status = str(entry["alignment_status"])
    html_output = str(entry["html_output"])
    html_bytes = int(str(entry["html_bytes"]))

    required_lines = [
        f"### {english_file}",
        f"- Chinese: {chinese_file}",
        f"- Pair status: {pair_status}",
        f"- Alignment status: {alignment_status}",
        f"- HTML: {html_output} ({html_bytes} bytes)",
    ]
    if pair_status in {"divergent", "incomplete"}:
        required_lines.append(f"- {english_file} (status: {pair_status}, alignment: {alignment_status})")
    return all(line in report_text for line in required_lines)


def _maybe_add_issue(issues: list[str], check_passed: bool, message: str) -> None:
    if not check_passed:
        issues.append(message)


def render_report(report: ValidationReport) -> str:
    lines = [REPORT_HEADING, "", f"Output root: {report.output_root}", f"Manifest: {report.manifest_path}", f"Canonical report: {report.report_path}", f"Chapters checked: {report.chapter_count}", f"Overall status: {'PASS' if report.passed else 'FAIL'}", ""]
    if report.failed_chapters:
        lines.append("## Failed Chapters")
        for chapter in report.failed_chapters:
            lines.append(f"- {chapter}")
        lines.append("")

    lines.append("## Per-Chapter Summary")
    for chapter in report.chapters:
        lines.append(
            f"- {chapter.english_file}: {'PASS' if chapter.passed else 'FAIL'} | "
            f"pair={chapter.pair_status} alignment={chapter.alignment_status} | "
            f"headings en/zh={chapter.actual.english.heading_count}/{chapter.actual.chinese.heading_count} | "
            f"tables en/zh={chapter.actual.english.table_count}/{chapter.actual.chinese.table_count} | "
            f"images en/zh={chapter.actual.english.image_count}/{chapter.actual.chinese.image_count} | "
            f"missing en/zh={chapter.actual.missing_markers['en']}/{chapter.actual.missing_markers['zh']}"
        )
    lines.append("")

    lines.append("## Detailed Findings")
    lines.append("")
    for chapter in report.chapters:
        lines.append(f"### {chapter.english_file}")
        lines.append(f"- Result: {'PASS' if chapter.passed else 'FAIL'}")
        lines.append(f"- Pair/alignment: {chapter.pair_status} / {chapter.alignment_status}")
        lines.append(
            f"- Headings EN expected/actual: {chapter.expected.english.heading_count} / {chapter.actual.english.heading_count}; "
            f"ZH expected/actual: {chapter.expected.chinese.heading_count} / {chapter.actual.chinese.heading_count}"
        )
        lines.append(
            f"- Tables EN expected/actual: {chapter.expected.english.table_count} / {chapter.actual.english.table_count}; "
            f"ZH expected/actual: {chapter.expected.chinese.table_count} / {chapter.actual.chinese.table_count}"
        )
        lines.append(
            f"- Images EN expected/actual: {chapter.expected.english.image_count} / {chapter.actual.english.image_count}; "
            f"ZH expected/actual: {chapter.expected.chinese.image_count} / {chapter.actual.chinese.image_count}"
        )
        lines.append(
            f"- Data-URI images EN/ZH actual: {chapter.actual.english.data_uri_image_count} / {chapter.actual.chinese.data_uri_image_count}"
        )
        lines.append(
            f"- Row statuses expected/actual: {chapter.expected.row_status_counts} / {chapter.actual.row_status_counts}"
        )
        lines.append(
            f"- Missing markers expected/actual: {chapter.expected.missing_markers} / {chapter.actual.missing_markers}"
        )
        lines.append(
            f"- Standalone asset dependencies: {'none' if not (chapter.actual.asset_dependencies or chapter.actual.style_dependencies) else ', '.join(chapter.actual.asset_dependencies + chapter.actual.style_dependencies)}"
        )
        if chapter.expected.warnings:
            lines.append(f"- Manifest warnings: {', '.join(chapter.expected.warnings)}")
        if chapter.issues:
            lines.append(f"- Issues: {'; '.join(chapter.issues)}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def write_report(report: ValidationReport, json_output: Path, report_output: Path) -> None:
    json_output.parent.mkdir(parents=True, exist_ok=True)
    report_output.parent.mkdir(parents=True, exist_ok=True)
    json_output.write_text(json.dumps(asdict(report), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    report_output.write_text(render_report(report), encoding="utf-8")


def main() -> None:
    args = parse_args()
    report = validate_output_root(args.repo_root, args.output_root)
    write_report(report, args.json_output, args.report_output)


if __name__ == "__main__":
    main()
