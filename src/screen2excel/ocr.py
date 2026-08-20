"""表格识别引擎：截图 → HTML 表格列表。

使用 RapidTable（SLANet_plus，ONNX Runtime 本地推理）+ RapidOCR（中文 OCR）。
模型随 wheel 包内置，首次使用无需下载大型模型。
"""

from __future__ import annotations

_engine = None


def _get_engine():
    """懒加载 RapidTable（进程内只初始化一次）。"""
    global _engine
    if _engine is None:
        from rapid_table import ModelType, RapidTable, RapidTableInput

        _engine = RapidTable(RapidTableInput(model_type=ModelType.SLANETPLUS))
    return _engine


def image_to_table_htmls(image_path: str) -> list[str]:
    """识别一张截图，返回其中表格的 HTML（整图按单个表格处理）。"""
    engine = _get_engine()
    output = engine(image_path)
    htmls = [h for h in (output.pred_htmls or []) if h and "<table" in h]
    return htmls
