"""Tests for optional Markdown dependency handling in legacy output layer."""

import builtins

from layers.output_layer import OutputLayer


def test_html_preview_falls_back_when_markdown_package_is_missing(monkeypatch):
    original_import = builtins.__import__

    def fake_import(name, *args, **kwargs):
        if name == "markdown":
            raise ImportError("markdown missing in test")
        return original_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", fake_import)

    html_preview = OutputLayer().generate_html_preview("# 标题\n\n- **风险**：测试")

    assert "<h1>标题</h1>" in html_preview
    assert "<strong>风险</strong>" in html_preview
