# HTML 报告构建指南（架构 / 分段 / 拼装 / 主题）

生成 HTML 报告时读本文件。结构骨架另见 `html-template.md`。

## 架构：内容与模板分离

统一走**分段生成 → 脚本拼装**流程。CSS/JS 在 `assets/`，由 `build_html.py` 直接读取，**不经过对话 token**。

```
lab-report-writer/
├── assets/  report.css（样式/响应式/深色/编辑器） + report.js（目录/验证面板/编辑器交互）
├── scripts/ build_html.py（合并分段 + 注入 SVG + 注入验证数据）
└── references/ html-template.md（结构参考，不参与构建）

工作目录（临时文件）：
body-parts/ 各章节 HTML 片段（或单文件 report-body.html）+ flowchart.svg 等
charts-init.js（仅有图表时） / verify-output.txt（仅有数据时）
```

## 阶段一：生成内容文件

### 单文件 vs 分段

| 情形 | 策略 |
|------|------|
| 短报告（≤5 章节，量小） | 单文件 `report-body.html` |
| 长报告（>5 章节，或引言/讨论丰富） | 分段，每章一个片段存入 `body-parts/` |

**分段原则**：每个片段是纯 HTML（无 `<html>/<head>/<body>`），逐个生成暂存；脚本按文件名升序直接拼接，无需包裹容器。封面/摘要/目录/布局开头放 `body-01-header.html`，footer/悬浮目录/移动导航/验证面板骨架放最后一段。

**推荐分段方案**：

```
body-01-header.html      封面+摘要+目录 + <div class="report-layout"><main class="page">
body-02-intro.html       引言
body-03-theory.html      实验原理
body-04-methods.html     实验方法（含 SVG 流程图占位）
body-05-results.html     实验结果（含图表 canvas 占位）
body-06-analysis.html    数据处理与分析
body-07-discussion.html  讨论
body-08-conclusion.html  结论
body-09-references.html  参考文献
body-10-footer.html      </main> footer+悬浮目录+移动导航+验证面板骨架 </div>
```

> ⚠️ `body-01` 必须含 `<div class="report-layout"><main class="page">` 开始标签；末段必须含闭合 `</main></div>`。

### 四类内容文件

- **① 正文 HTML 片段**：直接写 HTML（不经 Markdown）。完整骨架见 `html-template.md`。关键约定：`<section id>` 与目录 `href` 一一对应；`<canvas id="chartN">` 与 `charts-init.js` 一致；SVG 用 `<figure data-svg-src="xxx.svg">` 占位；验证面板骨架放末段。
- **② `charts-init.js`**：仅有图表时生成。模板见 `swd-chartjs-examples.md`。
- **③ `verify-output.txt`**：`auto_verify.py` 的输出，`--verify` 注入面板。
- **④ `flowchart.svg` 等**：SVG 独立文件，与正文同目录。详见 `svg-flowchart-template.md`。

## 阶段二：运行拼装脚本

```bash
# 单文件
python scripts/build_html.py --body report-body.html \
  --output /mnt/user-data/outputs/report.html [--charts charts-init.js] [--verify verify-output.txt]

# 分段（长报告推荐）
python scripts/build_html.py --body-dir body-parts/ \
  --output /mnt/user-data/outputs/report.html [--charts charts-init.js] [--verify verify-output.txt]
```

可选参数：`--theme <值>`（非默认主题）、`--svg-dir <目录>`（SVG 不在正文同目录时）、`--editable`（启用浏览器内编辑）、`--no-verify-panel`（无数据时不渲染面板）。SVG 默认在正文同目录自动查找。

脚本逻辑极简：`<html head> + report.css + 主题CSS + body_html + charts-init.js + report.js`，无格式转换。

## 阶段三：输出

```bash
present_files /mnt/user-data/outputs/report.html
```

## 主题注入

`assets/report.css` 含默认暖墨纸风格、响应式断点（1280/1024/768/480/360）、系统深色模式、打印优化。色彩主题全部由 `--theme` 参数控制，Claude **无需读取或内联任何 CSS**。

| 用户选项 | `--theme` 值 | | 用户选项 | `--theme` 值 |
|---|---|---|---|---|
| 暖墨纸（默认） | `default`/省略 | | 橄榄学报 | `olive` |
| 午夜藏青（深色） | `dark` | | 砖红工程 | `engineering` |
| 净白简约 | `clean` | | 石墨极简 | `graphite` |

- `THEME=default` → 省略 `--theme`
- `THEME≠default` → 加 `--theme <值>`，脚本自动注入对应 CSS 块（优先级高于 report.css）
- 仅当用户要求**自定义**非预置风格时，才需读取 `style-constitution.md`

## 输出格式

| 格式 | 生成方式 | 何时 |
|------|----------|------|
| HTML | 上述三阶段 | 默认 |
| Markdown | 直接生成 | 用户要纯文本草稿 |
| Word (.docx) | 读取 docx skill | 用户要可编辑 Word |

若用户提供 Markdown/Word，提示可转为期刊风格 HTML 版本。
