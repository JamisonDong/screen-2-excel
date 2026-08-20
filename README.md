# screen-2-excel

把表格截图一键转成 Excel（`.xlsx`）。

基于 [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) 的 PP-StructureV3 表格识别管线，**纯本地运行：不调用大模型、不需要 API Key、识别过程零网络请求，截图数据不出本机**。

## 特性

- 表格结构识别 + 单元格 OCR 一体化，支持中英文混排
- 合并单元格（colspan/rowspan）还原、单元格内多行文本合并
- 数字列自动转为数值（千分位逗号自动处理）
- 自动裁剪识别产生的空尾列，表头加粗、列宽自适应
- 多张截图 → 一个 xlsx 的多个 sheet
- 可直接读取系统剪贴板里的截图（macOS / Windows）

## 原理

```
截图 → PP-StructureV3（版面分析 + 表格结构识别 + 单元格 OCR）→ HTML 表格 → openpyxl → .xlsx
```

已默认关闭公式/印章/图表/文档方向矫正等与截图表格无关的子管线，减少模型体积与耗时。

## 安装

支持 macOS（Intel / Apple Silicon）和 Windows x64。要求 Python 3.10–3.13（paddlepaddle 暂不支持 3.14）。推荐用 [uv](https://docs.astral.sh/uv/) 管理环境。

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

依赖体积：Python 包约 700 MB；首次运行时模型自动下载到 `~/.paddlex`（Windows 为 `C:\Users\<你>\.paddlex`），约 1 GB，下载一次后永久离线可用。

## 用法

macOS / Linux 下命令前缀为 `.venv/bin/screen2excel`，Windows 下为 `.venv\Scripts\screen2excel`，以下略写为 `screen2excel`：

```bash
# 单张截图
screen2excel table.png -o result.xlsx

# 多张截图 → 一个 xlsx 的多个 sheet（sheet 名取文件名）
screen2excel 1.png 2.png -o result.xlsx

# 直接读系统剪贴板里的截图（macOS / Windows）
screen2excel --clipboard -o result.xlsx
```

## 离线部署

识别本身完全离线。要在无网机器上运行，只需在一台有网机器上安装并运行一次（触发模型下载），然后把模型目录整体拷到目标机器同一位置：

- macOS / Linux：`~/.paddlex`
- Windows：`C:\Users\<用户名>\.paddlex`

## 常见问题

**识别有错字怎么办？**
OCR 存在固有精度边界（例如 `v4` 识别成 `y4`），生成的 xlsx 建议人工过一遍。截图越清晰、分辨率越高，效果越好。

**极宽的截图效果如何？**
内部会把超长边缩放到 4000px 以内再识别，宽表格可以正常工作；若遇到漏字，可尝试把截图拆成左右两半分别转换。

**提示找不到表格？**
确认截图里是带明确行列结构的表格；纯文字段落不会被识别为表格，该图片会被跳过并输出警告。

## 许可

MIT
