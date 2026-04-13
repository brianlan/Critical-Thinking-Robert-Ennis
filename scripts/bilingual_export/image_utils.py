#!/usr/bin/env python3
"""Image resolution, embedding, and asymmetry utilities for bilingual export.

This module provides renderer-agnostic helpers for:
- Resolving source-relative image paths to filesystem paths
- Reading image bytes and converting to data URIs
- Detecting image-reference asymmetry between EN/ZH pairs
- Extracting image metadata from markdown source text

Raw-content edge cases (&#43;, footnote markers, inline emphasis) are never
touched by these utilities -- they pass through unchanged.
"""

import base64
import re
from dataclasses import dataclass
from pathlib import Path

from scripts.bilingual_export.discovery import IMAGE_RE

# MIME type mapping for common image formats
MIME_MAP: dict[str, str] = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".svg": "image/svg+xml",
    ".webp": "image/webp",
    ".bmp": "image/bmp",
    ".tiff": "image/tiff",
    ".tif": "image/tiff",
}

# Regex to extract the path from markdown image syntax ![alt](path)
IMAGE_PATH_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")


@dataclass(frozen=True)
class ImageRef:
    """A single image reference extracted from markdown source text."""

    alt_text: str
    relative_path: str
    line_number: int


@dataclass(frozen=True)
class ResolvedImage:
    """A resolved image ready for embedding in a rendered document."""

    alt_text: str
    relative_path: str
    absolute_path: str
    data_uri: str
    mime_type: str
    size_bytes: int


@dataclass(frozen=True)
class ImageAsymmetry:
    """Records an image present on one side but missing on the other."""

    en_relative_path: str
    en_alt_text: str
    zh_missing: bool  # True when ZH lacks this image
    en_missing: bool  # True when EN lacks this image


@dataclass(frozen=True)
class ImageAsymmetryReport:
    """Summary of image asymmetry for one chapter pair."""

    english_file: str
    chinese_file: str
    en_image_count: int
    zh_image_count: int
    asymmetries: tuple[ImageAsymmetry, ...]


def resolve_image_path(raw_path: str, context_path: Path, repo_root: Path) -> Path:
    """Resolve a markdown image path relative to its source file context.

    Resolution order (mirrors crop_diagrams_from_json.py style):
    1. If absolute and exists, use as-is.
    2. If relative to context_path parent and exists, use that.
    3. If relative to repo_root and exists, use that.
    4. Raise FileNotFoundError with the tried paths.
    """
    image_path = Path(raw_path)
    if image_path.is_absolute() and image_path.exists():
        return image_path

    # Try relative to the markdown file's directory
    candidate = context_path.parent / image_path
    if candidate.exists():
        return candidate

    # Try relative to repo root (standard for this repo's image layout)
    candidate = repo_root / image_path
    if candidate.exists():
        return candidate

    raise FileNotFoundError(
        f"Cannot resolve image path: {raw_path} "
        f"(tried: {context_path.parent / image_path}, {repo_root / image_path})"
    )


def guess_mime_type(path: Path) -> str:
    """Guess MIME type from file extension. Defaults to application/octet-stream."""
    return MIME_MAP.get(path.suffix.lower(), "application/octet-stream")


def image_to_data_uri(image_path: Path) -> tuple[str, str, int]:
    """Convert an image file to a data URI string.

    Returns (data_uri, mime_type, size_bytes).
    """
    data = image_path.read_bytes()
    mime_type = guess_mime_type(image_path)
    b64 = base64.b64encode(data).decode("ascii")
    data_uri = f"data:{mime_type};base64,{b64}"
    return data_uri, mime_type, len(data)


def extract_image_refs(markdown_text: str) -> list[ImageRef]:
    """Extract all image references from markdown text with line numbers.

    Does NOT modify the text in any way. Returns ImageRef objects that carry
    the raw relative path and alt text exactly as written in the source.
    """
    refs: list[ImageRef] = []
    for line_number, line in enumerate(markdown_text.splitlines(), start=1):
        for match in IMAGE_PATH_RE.finditer(line):
            relative_path = match.group(1)
            # Extract alt text from the full image match
            full_match = IMAGE_RE.search(line[match.start():])
            if full_match:
                inner = full_match.group(0)
                alt_match = re.match(r"!\[([^\]]*)\]", inner)
                alt_text = alt_match.group(1) if alt_match else ""
            else:
                alt_text = ""
            refs.append(ImageRef(
                alt_text=alt_text,
                relative_path=relative_path,
                line_number=line_number,
            ))
    return refs


def resolve_images(
    refs: list[ImageRef],
    context_path: Path,
    repo_root: Path,
) -> list[ResolvedImage]:
    """Resolve a list of image references to ResolvedImage objects with data URIs.

    Raises FileNotFoundError if any image cannot be found on disk.
    """
    resolved: list[ResolvedImage] = []
    for ref in refs:
        abs_path = resolve_image_path(ref.relative_path, context_path, repo_root)
        data_uri, mime_type, size_bytes = image_to_data_uri(abs_path)
        resolved.append(ResolvedImage(
            alt_text=ref.alt_text,
            relative_path=ref.relative_path,
            absolute_path=str(abs_path),
            data_uri=data_uri,
            mime_type=mime_type,
            size_bytes=size_bytes,
        ))
    return resolved


def build_asymmetry_report(
    english_file: str,
    chinese_file: str,
    en_refs: list[ImageRef],
    zh_refs: list[ImageRef],
) -> ImageAsymmetryReport:
    """Build an image asymmetry report comparing EN and ZH image references.

    The report is based on image paths (not alt text), since the same diagram
    file is typically referenced from both sides. For chapters where ZH omits
    image references entirely, all EN images appear as ZH-missing asymmetries.
    """
    zh_paths = {ref.relative_path for ref in zh_refs}
    en_paths = {ref.relative_path for ref in en_refs}
    asymmetries: list[ImageAsymmetry] = []

    # EN images missing from ZH
    for ref in en_refs:
        if ref.relative_path not in zh_paths:
            asymmetries.append(ImageAsymmetry(
                en_relative_path=ref.relative_path,
                en_alt_text=ref.alt_text,
                zh_missing=True,
                en_missing=False,
            ))

    # ZH images missing from EN (rare but possible)
    for ref in zh_refs:
        if ref.relative_path not in en_paths:
            asymmetries.append(ImageAsymmetry(
                en_relative_path=ref.relative_path,
                en_alt_text="",
                zh_missing=False,
                en_missing=True,
            ))

    return ImageAsymmetryReport(
        english_file=english_file,
        chinese_file=chinese_file,
        en_image_count=len(en_refs),
        zh_image_count=len(zh_refs),
        asymmetries=tuple(asymmetries),
    )


def has_image_asymmetry(report: ImageAsymmetryReport) -> bool:
    """Return True if there is any image asymmetry between the pair."""
    return len(report.asymmetries) > 0
