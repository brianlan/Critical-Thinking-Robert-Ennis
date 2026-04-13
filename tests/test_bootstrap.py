#!/usr/bin/env python3


def test_import_bilingual_export_package():
    import scripts.bilingual_export  # noqa: F401


def test_import_discovery_module():
    from scripts.bilingual_export import discovery  # noqa: F401


def test_import_align_module():
    from scripts.bilingual_export import align  # noqa: F401


def test_import_html_render_module():
    from scripts.bilingual_export import html_render  # noqa: F401


def test_import_word_render_module():
    from scripts.bilingual_export import word_render  # noqa: F401
