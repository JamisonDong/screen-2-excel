# screen-2-excel

把表格截图一键转成 Excel（`.xlsx`）。

基于 [RapidTable](https://github.com/RapidAI/RapidTable)（SLANet_plus 表格结构识别，ONNX Runtime 推理）+ RapidOCR 中文识别，**纯本地运行：不调用大模型、不需要 API Key、识别过程零网络请求，截图数据不出本机**。

## 特性

- 表格结构识别 + 单元格 OCR 一体化，支持中英文混排
- 合并单元格（colspan/rowspan）还原、单元格内多行文本合并
- 数字列自动转为数值（千分位逗号自动处理）
- 自动裁剪识别产生的空尾列，表头加粗、列宽自适应
- 多张截图 → 一个 xlsx 的多个 sheet
- 可直接读取系统剪贴板里的截图（macOS / Windows）

## 原理

```
截图 → RapidTable（SLANet_plus 表格结构识别 + RapidOCR 单元格文字识别，ONNX Runtime）→ HTML 表格 → openpyxl → .xlsx
```

识别模型（SLANet_plus 约 7 MB + RapidOCR 默认中文模型）随 Python 包内置，**首次使用无需下载模型，装完即可离线使用**。注意：整图按一个表格处理，适合"整张截图就是一个表格"的场景；截图里表格占比很小或有多张表时，建议先裁切。

## 安装

支持 macOS（Intel / Apple Silicon）和 Windows x64。推荐 Python 3.10–3.13，用 [uv](https://docs.astral.sh/uv/) 管理环境。

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

全部依赖（含模型）约 200 MB，无大型模型下载步骤。

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

识别模型随 Python 包内置，无额外模型目录。离线机器只需把项目 clone 和依赖安装好（可用 `uv pip download` / `pip download` 在有网机器上打包 wheel 再拷贝安装），之后即可完全离线运行。

## 常见问题

**识别有错字怎么办？**
OCR 存在固有精度边界（例如 `v4` 识别成 `y4`），生成的 xlsx 建议人工过一遍。截图越清晰、分辨率越高，效果越好。

**极宽的截图效果如何？**
内部会把超长边缩放到 4000px 以内再识别，宽表格可以正常工作；若遇到漏字，可尝试把截图拆成左右两半分别转换。

**提示找不到表格？**
确认截图里是带明确行列结构的表格；纯文字段落不会被识别为表格，该图片会被跳过并输出警告。

## 许可

MIT
