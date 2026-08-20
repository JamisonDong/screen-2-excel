# screen-2-excel

把表格截图一键转成 Excel。完全本地运行，基于 [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) 的 PP-StructureV3 表格识别管线，**不调用任何大模型 API，不需要联网（仅首次运行需下载模型）**。

## 原理

截图 → PP-StructureV3（版面分析 + 表格结构识别 + 单元格 OCR）→ HTML 表格 → openpyxl → `.xlsx`

支持合并单元格（colspan/rowspan）还原、单元格内多行文本、中英文混排、数字自动转数值。

## 安装

支持 macOS（Intel/Apple Silicon）和 Windows x64。要求 Python 3.10–3.13（paddlepaddle 暂不支持 3.14）。推荐用 [uv](https://docs.astral.sh/uv/) 管理环境：

macOS / Linux:

```bash
git clone git@github.com:JamisonDong/screen-2-excel.git
cd screen-2-excel
uv venv --python 3.12 .venv && uv pip install -e .
# 或者 pip: python3.12 -m venv .venv && .venv/bin/pip install -e .
```

Windows (PowerShell):

```powershell
git clone git@github.com:JamisonDong/screen-2-excel.git
cd screen-2-excel
uv venv --python 3.12 .venv; uv pip install -e .
# 或者 pip: py -3.12 -m venv .venv; .venv\Scripts\pip install -e .
```

依赖体积：Python 包约 700 MB；首次运行时模型自动下载到 `~/.paddlex`（Windows 为 `C:\Users\<你>\.paddlex`），已默认关闭公式/印章/图表/文档方向等无关子管线，仅需约 1 GB，下载后可离线使用。

## 用法

macOS / Linux 下命令前缀为 `.venv/bin/screen2excel`，Windows 下为 `.venv\Scripts\screen2excel`，以下略写为 `screen2excel`：

```bash
# 单张截图
screen2excel table.png -o result.xlsx

# 多张截图 → 一个 xlsx 的多个 sheet
screen2excel 1.png 2.png -o result.xlsx

# 直接读系统剪贴板里的截图（支持 macOS / Windows）
screen2excel --clipboard -o result.xlsx
```

## 许可

MIT
