"""PaddleOCR PP-StructureV3 表格识别：图片 → HTML 表格列表。"""

from __future__ import annotations

import tempfile
from pathlib import Path

_pipeline = None


def _get_pipeline():
    """懒加载 PPStructureV3（首次会下载模型，进程内只初始化一次）。

    截图转表格只需要 版面分析 + 表格识别 + OCR，关闭公式/印章/图表/文档方向
    等无关子管线，显著减少模型下载量和推理耗时。
    """
    global _pipeline
    if _pipeline is None:
        from paddleocr import PPStructureV3

        _pipeline = PPStructureV3(
            use_doc_orientation_classify=False,
            use_doc_unwarping=False,
            use_textline_orientation=False,
            use_formula_recognition=False,
            use_seal_recognition=False,
            use_chart_recognition=False,
        )
    return _pipeline


def _extract_table_htmls(result) -> list[str]:
    """从 PPStructureV3 单页结果中提取所有表格的 HTML。"""
    htmls: list[str] = []
    try:
        data = result.json
        if isinstance(data, dict):
            data = data.get("res", data)
        for block in data.get("parsing_res_list", []) or []:
            label = block.get("block_label", "")
            content = block.get("block_content", "")
            if "table" in label and "<table" in content:
                htmls.append(content)
    except Exception:
        pass
    return htmls


def _extract_via_save(result) -> list[str]:
    """兜底：用 save_to_html 落盘再读回。"""
    htmls: list[str] = []
    try:
        with tempfile.TemporaryDirectory() as tmp:
            result.save_to_html(tmp)
            for p in sorted(Path(tmp).rglob("*.html")):
                text = p.read_text(encoding="utf-8", errors="ignore")
                if "<table" in text:
                    htmls.append(text)
    except Exception:
        pass
    return htmls


def image_to_table_htmls(image_path: str) -> list[str]:
    """识别一张截图，返回其中所有表格的 HTML（通常只有 1 个）。"""
    pipeline = _get_pipeline()
    htmls: list[str] = []
    for result in pipeline.predict(input=image_path):
        htmls.extend(_extract_table_htmls(result))
    if not htmls:
        for result in pipeline.predict(input=image_path):
            htmls.extend(_extract_via_save(result))
    return htmls
