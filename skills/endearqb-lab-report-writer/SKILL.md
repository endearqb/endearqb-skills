---
name: lab-report-writer
metadata:
  version: 2.2.1
description: |
  撰写期刊风格的实验报告，支持理工科实验课报告、科研论文级实验记录、工程项目技术报告、竞赛展示用报告等全场景。
  用户提供实验信息、数据、方法描述后，生成结构完整、排版专业的报告，并附带Python数据验证脚本对所有计算结论进行复核。
  
  触发条件（凡符合以下任一项，均应使用本skill）：
  - 用户说"帮我写实验报告"、"写一份实验记录"、"整理实验数据"、"写技术报告"
  - 用户提供了实验原始数据并想生成正式报告
  - 用户说"我有实验结果，帮我整理成报告"
  - 用户想把markdown或word报告转成HTML期刊风格
  - 任何涉及"实验"+"报告/记录/总结"的组合请求
  - 用户提到要生成包含数据图表、公式推导、误差分析的正式文档
  
  输出格式：优先HTML报告（期刊风格）；也可输出Markdown或Word（.docx）。
  如果用户提供了Markdown/Word报告，应提醒其可升级为HTML报告。
---

# Lab Report Writer — 期刊风格实验报告撰写 Skill

## 概览

本skill覆盖四类场景：理工科实验课、科研论文级记录、工程技术报告、竞赛展示报告。

核心流程：**信息采集 → 文献搜索 → Python自动验证 → 撰写结构化内容 → 生成HTML报告**

---

## 第一步：信息采集与场景识别

### 识别场景类型

| 场景 | 典型特征 | 报告侧重 |
|------|----------|----------|
| 实验课报告 | 有实验目的、操作步骤、数据表格 | 规范结构、误差分析、结论 |
| 科研记录 | 有假设、方法对比、统计分析 | 方法严谨性、数据可重复性 |
| 工程技术报告 | 有设计参数、测试标准、性能指标 | 工程可行性、指标达标情况 |
| 竞赛展示 | 有创新点、视觉冲击需求 | 清晰叙事、高质量图表 |

### 必须从用户处收集的信息

**最小信息集（必须有）：**
- 实验/项目标题
- 实验目的或研究问题
- 实验方法或操作步骤（文字描述即可）
- 主要结果（数据或文字描述）

**增强信息（有则收集）：**
- 原始数据表格（CSV、手工记录等）
- 计算公式和推导过程
- 参考文献列表
- 实验装置或流程图描述
- 误差来源分析
- 作者、机构、日期等元数据

### 信息不完整时的处理策略

- **数据缺失**：跳过图表，用文字表述结果，在报告中标注"[图表：数据待补充]"
- **公式缺失**：根据领域知识推断，并在报告中说明假设
- **参考文献缺失**：生成报告，提醒用户补充
- **元数据缺失**：使用占位符（如"[作者姓名]"、"[日期]"）

---

## 第一步（补）：生成前确认选项

完成信息采集、场景识别后，在开始任何生成之前，**必须调用 `ask_user_input` 工具**向用户确认以下四个选项。用自然语言简短说明即将生成报告，然后紧接着调用工具展示选项（不要用纯文字罗列问题）。

```
调用 ask_user_input，四个问题同时呈现：

问题1（single_select）：
  标题：文档模式
  选项：["长文档模式（分章节生成，推荐）", "单文件模式"]
  默认高亮：长文档模式

问题2（multi_select）：
  标题：可视化内容
  选项：["生成 SVG 流程图", "生成 Chart.js 图表"]
  默认全选

问题3（single_select）：
  标题：附加输出
  选项：["仅 HTML 报告", "HTML + Markdown 草稿"]
  默认高亮：仅 HTML 报告

问题4（single_select）：
  标题：报告色彩主题
  选项：["暖墨纸（默认）", "午夜藏青（深色）", "净白简约", "橄榄学报", "砖红工程", "石墨极简"]
  默认高亮：暖墨纸（默认）
```

根据用户回答设定以下工作变量，后续所有步骤依据这些变量执行：

| 变量 | 含义 | 默认值 |
|------|------|--------|
| `MODE_LONG` | 是否使用长文档分段模式 | `true` |
| `NEED_SVG` | 是否生成 SVG 流程图 | `true` |
| `NEED_CHART` | 是否生成 Chart.js 图表 | `true` |
| `NEED_MD` | 是否额外输出 Markdown 草稿 | `false` |
| `THEME` | 色彩主题名称 | `"暖墨纸"` |

**变量对后续步骤的影响：**
- `MODE_LONG=false` → 阶段一用单文件 `report-body.html`，`build_html.py` 用 `--body`
- `NEED_SVG=false` → 跳过 SVG 生成，方法节中不写 `data-svg-src` 占位符
- `NEED_CHART=false` → 跳过 `charts-init.js`，结果节中不写 `<canvas>` 占位
- `NEED_MD=true` → 阶段三额外输出一份 `.md` 文件并一同 `present_files`
- `THEME` → 非默认时，在 `build_html.py` 命令中添加 `--theme <值>` 参数（Agent 无需读取或写入任何 CSS）

### 主题名称映射

| 用户选项 | `--theme` 参数值 |
|---------|----------------|
| 暖墨纸（默认） | `default`（或省略） |
| 午夜藏青（深色） | `dark` |
| 净白简约 | `clean` |
| 橄榄学报 | `olive` |
| 砖红工程 | `engineering` |
| 石墨极简 | `graphite` |

### 主题注入规则

主题 CSS 完全由 `build_html.py` 处理，Agent **不需要**读取 `style-constitution.md`，也不需要内联任何 CSS。

- **`THEME=default`**：`build_html.py` 调用时省略 `--theme` 参数（或传 `--theme default`）。
- **`THEME≠default`**：在 `build_html.py` 调用命令中添加 `--theme <值>` 参数即可。

```bash
# 示例：橄榄学报主题
python scripts/build_html.py \
  --body-dir /outputs/XXXX报告名/body-parts/ \
  --output /outputs/XXXX报告名/report.html \
  --theme olive \
  [--charts charts-init.js] \
  [--verify verify-output.txt]
```

脚本会自动将对应主题的 CSS 块注入 `<head>` 中的独立 `<style>` 标签，优先级高于 `report.css`，无需 Agent 参与任何 CSS 处理。

> 如果用户在信息采集阶段就已明确指定了主题（在 `ask_user_input` 之前），则 `ask_user_input` 中第四个问题的默认高亮选项改为对应主题。

---

## 第二步：Python数据自动验证

### 触发判断

| 情形 | 操作 |
|------|------|
| 用户上传CSV文件 | 调用 `scripts/auto_verify.py` 自动解析并验证 |
| 用户粘贴表格数据（Markdown表格/空格分隔/逗号分隔） | 写入临时CSV，同上处理 |
| 用户提供了具体数值和公式 | 生成专项验证脚本并运行 |
| 用户只有文字描述、无任何数值 | 跳过Python验证，在报告中注明 |

### 自动验证流程（CSV/表格数据）

```
Step 1  读取数据
        用 pandas 解析，自动检测分隔符（csv/tsv/空格）
        打印列名、行数、数据类型、缺失值情况

Step 2  统计摘要
        对每列数值列计算：均值、标准差、最小值、最大值、中位数
        对比用户报告中声明的统计结果（如有）

Step 3  推断计算关系
        扫描列名关键词，匹配已知计算模式（见下方）
        若识别到公式关系，自动执行计算验证

Step 4  误差核查
        对比用户声明值 vs 脚本计算值，标记偏差 > 1% 的项

Step 5  输出验证摘要
        格式化为可直接粘贴到HTML报告「数据验证」节的文本
```

### 列名关键词→计算模式映射

脚本自动识别以下模式（不区分中英文大小写）：

| 关键词组合 | 自动触发的验证 |
|-----------|--------------|
| `质量/mass` + `产率/yield` | 产率 = m产品 / m理论 × 100% |
| `时间/time` + `浓度/concentration` | 速率 = ΔC/Δt；一阶/零阶拟合 |
| `电压/voltage` + `电流/current` | 功率 P = UI；电阻 R = U/I |
| `力/force` + `位移/displacement` | 功 W = F·d；弹性系数 |
| `温度/temperature` + `速率/rate` | Arrhenius拟合（lnk vs 1/T） |
| `重复/repeat` 多列 | 均值±标准差；RSD；置信区间 |
| `理论/theoretical` + `实验/experimental` | 相对误差 = \|实-理\|/理 × 100% |

若无法匹配，脚本仅输出统计摘要，不强行推断计算关系。

### 验证深度自动判断

- 数据点 < 10：轻量（仅统计摘要 + 结果对比）
- 数据点 10–50：中度（统计摘要 + 中间步骤 + 偏差标注）
- 数据点 > 50：深度（中度 + 相关性分析 + 输出图表数据供Chart.js使用）

### 验证脚本

完整自动脚本 → 参见 `scripts/auto_verify.py`

### 验证摘要放置规则

#### HTML 报告（默认）

将脚本输出嵌入右下角**悬浮折叠面板**（`#verifyPanel`），**正文不设数据验证章节**。

面板内容分三区渲染（详见 `references/html-template.md` 验证面板段落）：
1. **统计摘要区**：各列均值、标准差、RSD、最大/最小值
2. **计算验证区**：每个匹配模式的公式、计算值、用户声明值、偏差百分比、✓/✗
3. **偏差汇总区**：仅在有 ✗ 项时显示，列出所有偏差项及建议

面板行为：
- 有偏差（含 ✗）时：面板边框变橙，**自动展开**，并在面板底部显示偏差汇总
- 全部通过（仅 ✓）时：面板默认折叠，徽章显示「N/N 通过」
- 键盘快捷键：`V` 键切换展开/折叠

#### Markdown 报告

在参考文献之后追加 `## 附录：数据验证` 章节，原样嵌入脚本输出的纯文本块。

---

### ⚠ 数据冲突处理原则（宪法级规定，不可违反）

当 Python 验证发现用户提供的数值与计算结果存在偏差时：

```
✅ 正确做法：
   1. 报告正文（Results、Analysis节）始终忠实呈现用户提供的原始数据和结论
   2. 验证面板中如实标注偏差（✗ 项）
   3. 若偏差 > 5%，在「讨论」节自动补充一段措辞，例如：
      「本实验中[指标名]的实测值（X.XX）与理论计算值（Y.YY）存在约Z%的偏差，
       可能来源于[误差分析]，建议实验者核查原始记录。」
   4. 偏差说明措辞用「可能」「建议核查」等不确定语气，不替用户下定论

❌ 禁止做法：
   - 用计算值替换用户提供的数值写入报告正文
   - 在未告知用户的情况下修正任何数据
   - 忽略偏差、不在面板和讨论中体现
   - 因数据存在偏差而拒绝生成报告
```

**偏差严重程度分级**：

| 偏差幅度 | 处理方式 |
|---------|---------|
| < 1% | 视为数值舍入误差，验证面板标 ✓，正文无需特殊处理 |
| 1–5% | 验证面板标 ✗，讨论节加一句可能原因 |
| 5–20% | 验证面板标 ✗ 并橙色警示，讨论节专门分析，建议核查 |
| > 20% | 验证面板标 ✗ 并橙色警示，在正式生成报告**前**主动告知用户偏差情况，询问是否继续 |

---

## 第三步：文献搜索与引文标注

### 搜索触发原则

在撰写以下章节时，**必须**进行网络文献搜索：
- 引言（背景知识、研究现状）
- 实验原理（理论依据、公式来源）
- 讨论（与已有研究对比、机理解释）

**搜索策略：**

```
1. 优先搜索数据库/权威来源：
   - 中文：CNKI、万方、维普、国家标准全文库
   - 英文：PubMed、Web of Science、Google Scholar、ACS/RSC/Elsevier期刊
   - 标准文献：GB/T、ISO、ASTM（用 site:std.samr.gov.cn 或 standards.org）
   - 教材/专著：Google Books

2. 搜索关键词构建规则：
   - 中文优先：[实验主题] + [核心概念] + "原理"/"机制"/"方法"
   - 英文补充：[topic] + [concept] + "mechanism" / "review" / "standard method"
   - 针对公式：搜索公式名称（如"Arrhenius equation derivation"）

3. 每个引用点：搜索2-3个候选，选择最权威、最具体的来源
   - 期刊论文 > 教材 > 综述 > 网页
   - 优先选有DOI的来源

4. 无法找到合适文献时：
   - 在正文中不加上标注
   - 不虚构文献信息
   - 可注明"[此处建议查阅相关教材]"
```

### GB/T 7714-2015 引文格式

**正文内引用标注：**
```html
<!-- 上标数字引用，可点击跳转 -->
<sup><a href="#ref-1">[1]</a></sup>

<!-- 多文献同时引用 -->
<sup><a href="#ref-1">[1]</a><a href="#ref-2">[2]</a></sup>
```

**参考文献列表格式（严格遵守GB/T 7714-2015）：**

```
期刊论文：
[序号] 作者1, 作者2. 题名[J]. 刊名, 年份, 卷(期): 起止页码. DOI或URL.

专著/教材：
[序号] 作者. 书名[M]. 版次. 出版地: 出版社, 年份: 起止页码.

标准文献：
[序号] 标准代号. 标准名称[S]. 发布机构, 年份.

网络资源（数据库条目等）：
[序号] 作者/机构. 题名[EB/OL]. [引用日期]. URL.
```

**HTML中的参考文献节渲染：**
```html
<section id="references" class="references">
  <h2>参考文献</h2>
  <ol>
    <li id="ref-1">
      张三, 李四. 某化学反应动力学研究[J]. 化学学报, 2020, 78(5): 412-419.
      <a href="https://doi.org/10.xxxx/xxxxx" target="_blank">https://doi.org/10.xxxx/xxxxx</a>
    </li>
    <li id="ref-2">
      Smith A, Jones B. Kinetics of reaction X[J]. <em>J. Chem. Phys.</em>, 2019, 150(3): 034501.
      <a href="https://doi.org/10.xxxx/xxxxx" target="_blank">https://doi.org/10.xxxx/xxxxx</a>
    </li>
  </ol>
</section>
```

### 引文质量检查

生成报告前检查：
- [ ] 每处引用均能通过URL访问（或有明确DOI）
- [ ] 作者、刊名、年份、卷期页码字段完整
- [ ] 文献类型标识符正确（[J]期刊/[M]专著/[S]标准/[EB/OL]网络）
- [ ] 正文引用编号与参考文献列表编号一一对应
- [ ] 无虚构文献信息

---

## 第四步：报告结构

### 标准结构（可根据场景裁剪）

```
1. 封面区（标题、副标题、作者、机构、日期）
2. Abstract / 摘要（150-300字）
3. 目录（自动生成）
4. 引言 / Introduction
5. 实验原理 / Theory（含公式）
6. 实验装置与方法 / Methods
   - 流程图（SVG，若用户提供了步骤描述）
7. 实验结果 / Results
   - 数据表格
   - 图表（Chart.js，仅当有数据时）
8. 数据处理与分析 / Analysis
   - 计算过程
   - 误差分析
9. 讨论 / Discussion
10. 结论 / Conclusion
11. 参考文献 / References
12. 附录（可选）
    - Markdown 格式：必须追加「附录：数据验证」节（嵌入脚本输出纯文本）
    - HTML 格式：无此附录，数据验证见右下角悬浮面板
```

**场景裁剪原则：**
- 实验课报告：保留全部章节，突出误差分析
- 科研记录：在Methods中增加"统计方法"小节
- 工程报告：将"实验原理"改为"设计依据"，增加"指标达标分析"
- 竞赛展示：压缩Methods，突出Results和Discussion，图表优先

---

## 第五步：可视化规范

### 数据可视化原则（基于Storytelling with Data）

1. **选图优先级**：散点图（关系）> 折线图（趋势）> 柱状图（对比）> 饼图（占比，慎用）
2. **去除图表垃圾**：无网格线（或极淡）、无边框、无不必要图例
3. **数据墨水比最大化**：每个像素都应服务于数据
4. **颜色使用**：
   - 主色系与HTML报告配色一致（`--accent: #2f4f4f`，暗绿色系）
   - 强调色用于最重要的数据系列
   - 其余系列用低饱和度灰色或浅色
   - 严禁彩虹配色
5. **图表标题**：描述性标题（"处理组效率比对照组高23%"），而非轴标签式（"效率对比"）
6. **标注优于图例**：直接在数据点旁标注系列名称

### Chart.js配置模板

```javascript
// 遵循SWD原则的Chart.js基础配置
const swdDefaults = {
  plugins: {
    legend: { display: false },  // 用直接标注替代图例
    tooltip: { callbacks: { /* 自定义 */ } }
  },
  scales: {
    x: { grid: { display: false }, border: { display: false } },
    y: { grid: { color: '#f0ece2', lineWidth: 1 }, border: { display: false } }
  },
  elements: {
    line: { tension: 0.3, borderWidth: 2 },
    point: { radius: 4, hoverRadius: 6 }
  }
};
```

### SVG流程图规范

- 仅当用户描述了实验步骤/流程时才绘制
- 颜色用报告配色变量：`#f4f1e8`（暖白）、`#eef3f0`（淡绿）、`#2f4f4f`（墨绿）
- 字体：Georgia（中文：Noto Serif SC）
- 箭头颜色：`#2f4f4f`
- 每个步骤方框：`rx="12"` 圆角，`stroke="#283239"` 边框
- 详细模板参见 `references/svg-flowchart-template.md`

#### SVG 独立文件 + 注入机制

SVG **不内嵌在正文 HTML 片段中**，而是单独保存为 `.svg` 文件，由 `build_html.py` 在拼装时自动注入。

**① Agent 生成 SVG 文件**（如 `flowchart.svg`、`apparatus.svg`），保存在与正文同一目录：
```
body-parts/
  body-04-methods.html     ← 只含占位符，不含 SVG 代码
  flowchart.svg            ← 独立 SVG 文件
  apparatus.svg            ← 若有多图，用不同文件名
```

**② 正文 HTML 片段中用 `data-svg-src` 属性标记注入位置**：
```html
<!-- body-04-methods.html -->
<section id="methods">
  <h2 class="section-title">3. 实验装置与方法</h2>
  <p>实验采用...</p>

  <!-- SVG 占位符：data-svg-src 指向文件名，figcaption 正常写 -->
  <figure data-svg-src="flowchart.svg">
    <figcaption>图 1. 实验流程图</figcaption>
  </figure>

  <!-- 若有第二张 SVG -->
  <figure data-svg-src="apparatus.svg">
    <figcaption>图 2. 实验装置示意图</figcaption>
  </figure>
</section>
```

**③ `build_html.py` 自动完成注入**，无需额外参数（默认在正文同目录查找）：
```bash
# SVG 与 body-parts/ 在同一目录，自动找到
python scripts/build_html.py --body-dir /outputs/XXXX报告名/body-parts/ --output /outputs/XXXX报告名/report.html

# 若 SVG 在单独目录，用 --svg-dir 指定
python scripts/build_html.py --body-dir /outputs/XXXX报告名/body-parts/ --svg-dir /outputs/XXXX报告名/svgs/ --output /outputs/XXXX报告名/report.html
```

注入后效果：
```html
<figure>
  <svg viewBox="0 0 600 300" xmlns="http://www.w3.org/2000/svg">
    <!-- SVG 内容直接内嵌 -->
  </svg>
  <figcaption>图 1. 实验流程图</figcaption>
</figure>
```

> ⚠️ SVG 文件不要包含 `<?xml ...?>` 声明行（脚本会自动去除）。若文件未找到，占位符原样保留并打印 `[WARN]`，不中断构建。

---

## 第六步：HTML生成策略

### 架构：内容与模板分离

所有报告统一使用**分段生成 → 脚本拼装**流程。CSS 和 JS 存放在 `assets/` 目录，由 `build_html.py` 直接读取，**完全不经过对话 token**。

```
lab-report-writer/
├── assets/
│   ├── report.css        ← 完整样式（含响应式、深色模式、编辑器）
│   └── report.js         ← 所有交互（目录高亮、验证面板、内联编辑器）
├── scripts/
│   └── build_html.py     ← 拼接器：合并分段 + 注入 SVG + 注入验证数据
└── references/
    └── html-template.md  ← 给 Agent 读的结构参考（不参与构建）

工作目录（Agent 生成的临时文件）：
/outputs/XXXX报告名/body-parts/               ← 各章节 HTML 片段（或单文件 report-body.html）
  body-01-header.html
  body-04-methods.html    ← 含 data-svg-src 占位符，不含 SVG 代码
  ...
  flowchart.svg           ← SVG 独立文件，与 body-parts/ 同目录
  apparatus.svg
charts-init.js            ← Chart.js 初始化（仅有图表时）
verify-output.txt         ← Python 验证摘要（仅有数据时）
```

### 生成流程（固定，三个阶段）

#### 阶段一：依次生成并保存内容文件

**① 报告正文 HTML 片段** — Agent 直接生成 HTML，不经 Markdown 转换。

##### 单文件 vs 分段生成

| 情形 | 策略 | 文件命名 |
|------|------|---------|
| 短报告（≤ 5 章节，内容量小） | **单文件**：直接生成 `report-body.html` | `report-body.html` |
| 长报告（> 5 章节，或引言/讨论等节内容丰富） | **分段生成**：每章一个 HTML 片段，存入 `/outputs/XXXX报告名/body-parts/` 目录 | `body-01-header.html`、`body-02-intro.html`… |

**分段生成的原则**：
- 每个片段独立保存，Agent 逐个生成后暂存，不需要在单次输出中完成全部内容
- 每个片段都是纯 HTML 片段（不含 `<html>/<head>/<body>` 标签）
- 片段之间**无需**任何包裹容器，`build_html.py` 会按文件名升序直接拼接
- **封面/摘要/目录/布局开头**放在 `body-01-header.html`，**footer/悬浮目录/移动导航/验证面板骨架**放在最后一个片段（如 `body-10-footer.html`），中间各节按顺序编号

**推荐分段方案**（长报告）：
```
body-parts/
  body-01-header.html      封面 + 摘要 + 目录 + <div class="report-layout"><main class="page">
  body-02-intro.html       1. 引言节
  body-03-theory.html      2. 实验原理节
  body-04-methods.html     3. 实验方法节（含 SVG 流程图）
  body-05-results.html     4. 实验结果节（含图表 canvas 占位）
  body-06-analysis.html    5. 数据处理与分析节
  body-07-discussion.html  6. 讨论节
  body-08-conclusion.html  7. 结论节
  body-09-references.html  参考文献节
  body-10-footer.html      </main> footer + 悬浮目录 + 移动导航 + 验证面板骨架 + </div>
```

> ⚠️ **注意**：`body-01-header.html` 必须包含 `<div class="report-layout">` 和 `<main class="page">` 的**开始标签**；`body-10-footer.html` 必须包含对应的**闭合标签** `</main></div>`，以确保整体 DOM 结构完整。

**① `report-body.html`（单文件模式）** 或 **`body-parts/body-NN-*.html`（分段模式）**

结构约定（必须遵守，脚本靠这些 id/class 注入内容）：

```html
<!-- 布局容器 -->
<div class="report-layout">
<main class="page">

  <!-- 期刊顶栏 -->
  <div class="journal-bar">
    <div>[课程/机构]</div>
    <div>Report Date: [日期]</div>
  </div>

  <!-- 封面 -->
  <section class="cover">
    <div>
      <h1>[标题]</h1>
      <p class="subtitle">[副标题]</p>
    </div>
    <aside class="meta-card">
      <h2>Report Info</h2>
      <dl>
        <dt>作者</dt><dd>[姓名]</dd>
        <dt>日期</dt><dd>[日期]</dd>
        <!-- 按场景增减字段 -->
      </dl>
    </aside>
  </section>

  <!-- 摘要 -->
  <section class="abstract">
    <h2>Abstract</h2>
    <p>[摘要内容]</p>
    <p class="keywords"><strong>关键词：</strong>[词1]；[词2]</p>
  </section>

  <!-- 目录（inline，与正文同侧） -->
  <nav class="toc"><h2>Contents</h2><ol>
    <li><a href="#intro">1. 引言</a></li>
    <!-- ... -->
  </ol></nav>

  <div class="divider"></div>

  <!-- 正文各节：id 必须与目录 href 一致 -->
  <section id="intro">
    <h2 class="section-title">1. 引言</h2>
    <p>...</p>
  </section>

  <!-- SVG 流程图插入位置（若有） -->
  <section id="methods">
    <h2 class="section-title">3. 实验装置与方法</h2>
    <figure>
      <!-- flowchart.svg 内容直接粘贴至此 -->
      <figcaption>图 1. 实验流程图</figcaption>
    </figure>
  </section>

  <!-- 图表占位（canvas id 供 charts-init.js 初始化） -->
  <section id="results">
    <h2 class="section-title">4. 实验结果</h2>
    <figure>
      <div class="chart-container"><canvas id="chart1"></canvas></div>
      <figcaption>图 2. [描述性图题]</figcaption>
    </figure>
  </section>

  <!-- 参考文献 -->
  <section id="references" class="references">
    <h2>参考文献</h2>
    <ol>
      <li id="ref-1">...</li>
    </ol>
  </section>

  <footer class="footer">
    <span>[课程/机构]</span><span>生成日期：[日期]</span>
  </footer>

</main>

<!-- 宽屏悬浮目录（与目录 href 保持一致） -->
<nav class="float-toc" id="floatToc" aria-label="文章目录">
  <p class="float-toc-label">目录</p>
  <ol><!-- 与 inline toc 相同条目 --></ol>
</nav>
</div>

<!-- 移动端导航 -->
<div class="mobile-nav-overlay" id="mobileNavOverlay"></div>
<nav class="mobile-nav-menu" id="mobileNavMenu" aria-label="快速导航">
  <div class="mobile-nav-label">目录</div>
  <ol><!-- 同上 --></ol>
</nav>
<button class="mobile-nav-btn" id="mobileNavBtn" aria-label="打开目录" aria-expanded="false"></button>

<!-- 验证面板（build_html.py 注入验证内容到 pre 元素） -->
<aside id="verifyPanel" class="verify-panel" aria-label="数据验证摘要">
  <button class="verify-panel-header" id="verifyToggle" aria-expanded="false">
    <span class="verify-panel-icon">🔬</span>
    <span class="verify-panel-title">验证摘要</span>
    <span class="verify-panel-badge" id="verifyBadge"></span>
    <span class="verify-panel-chevron">▲</span>
  </button>
  <div class="verify-panel-body" id="verifyBody">
    <div class="verify-section" id="verifyStats">
      <div class="verify-section-label">📊 统计摘要</div>
      <pre class="verify-pre" id="verifyStatsContent">[暂无统计数据]</pre>
    </div>
    <div class="verify-section" id="verifyCalc">
      <div class="verify-section-label">🧮 计算验证</div>
      <pre class="verify-pre" id="verifyCalcContent">[暂无计算验证数据]</pre>
    </div>
    <div class="verify-section verify-warn-section" id="verifyWarnSection" style="display:none">
      <div class="verify-section-label">⚠ 偏差汇总</div>
      <pre class="verify-pre" id="verifyWarnContent"></pre>
      <p class="verify-note" id="verifyNote"></p>
    </div>
  </div>
</aside>
```

**② `charts-init.js`** — 仅当有图表时生成，内含 Chart.js 初始化代码：

```javascript
// SWD原则配置；canvas id 与 report-body.html 中保持一致
const isMobile = window.matchMedia('(max-width: 768px)').matches;
const ctx1 = document.getElementById('chart1');
if (ctx1) {
  new Chart(ctx1, {
    type: 'line',
    data: {
      labels: [/* x轴标签 */],
      datasets: [{ data: [/* 数据 */], borderColor: '#2f4f4f', borderWidth: 2, tension: 0.3 }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: !isMobile,
      plugins: { legend: { display: false } },
      scales: {
        x: { grid: { display: false }, border: { display: false } },
        y: { grid: { color: '#f0ece2' }, border: { display: false } }
      }
    }
  });
}
```

**③ `verify-output.txt`** — 运行 `auto_verify.py` 后的输出，格式：
```
【统计摘要】
...
【计算验证】
...
```

**④ `flowchart.svg` / `apparatus.svg` 等** — SVG 流程图独立文件，保存在与正文片段**同一目录**。正文 HTML 只写 `data-svg-src` 占位符，`build_html.py` 在拼装时自动注入。详见「SVG独立文件+注入机制」一节。

#### 阶段二：运行拼装脚本

**单文件模式**：
```bash
python scripts/build_html.py \
  --body    report-body.html \
  --output  /outputs/XXXX报告名/report.html \
  [--charts charts-init.js] \
  [--verify verify-output.txt]
# SVG 自动在 report-body.html 同目录查找
```

**分段模式**（推荐长报告使用）：
```bash
python scripts/build_html.py \
  --body-dir /outputs/XXXX报告名/body-parts/ \
  --output   /outputs/XXXX报告名/report.html \
  [--charts  charts-init.js] \
  [--verify  verify-output.txt]
# SVG 自动在 body-parts/ 目录查找；若在别处用 --svg-dir 指定
```

脚本做的事极其简单：`<html head> + assets/report.css + body_html（含多段拼接）+ charts-init.js + assets/report.js`，无任何格式转换逻辑。

#### 阶段三：输出文件

```bash
present_files /outputs/XXXX报告名/report.html
```

### 风格说明

`assets/report.css` 已包含：
- 默认暖墨纸风格（`:root` CSS 变量）
- 响应式断点（1280 / 1024 / 768 / 480 / 360px）
- 系统深色模式自动适配（`@media prefers-color-scheme: dark`）
- 打印优化

**色彩主题**：由 `build_html.py` 的 `--theme` 参数控制（详见「第一步（补）」主题注入规则）。Agent 无需读取 `references/style-constitution.md`，除非用户要求**自定义**非预置的风格。

| 输出格式 | 生成方式 | 何时使用 |
|----------|----------|----------|
| HTML | 上述三阶段流程 | 默认，所有报告 |
| Markdown | 直接生成 | 用户明确要求纯文本草稿 |
| Word (.docx) | 读取 docx skill | 用户要求可编辑 Word 文档 |

若用户提供 Markdown/Word，提示："可以将这份报告转换为期刊风格 HTML 版本，是否需要？"

---

## 执行检查清单

生成报告前，逐项确认：

**阶段零：确认**
- [ ] 已调用 `ask_user_input` 工具展示四个确认选项（文档模式 / 可视化内容 / 附加输出 / 色彩主题）
- [ ] 已根据用户回答设定 `MODE_LONG` / `NEED_SVG` / `NEED_CHART` / `NEED_MD` / `THEME`
- [ ] `THEME≠default` → `build_html.py` 命令已加 `--theme <值>`（无需读取 CSS 文件）

**阶段一：内容生成**
- [ ] 场景类型已识别，章节结构已裁剪
- [ ] 必须信息已收集，缺失项已用占位符处理
- [ ] 判断报告长度：≤5章节→单文件 `report-body.html`；>5章节或内容量大→分段生成至 `/outputs/XXXX报告名/body-parts/`
- [ ] 单文件：`report-body.html` 含 `.report-layout`、`.page`、`.float-toc`、移动端导航、验证面板骨架
- [ ] 分段：`body-01-header.html` 含布局开始标签，最后一个片段含闭合标签及全部悬浮元素
- [ ] 所有 `section id` 与目录 `a[href]` 一一对应（跨分段也需对应）
- [ ] 有CSV/表格数据 → 已运行 `auto_verify.py`，输出保存为 `verify-output.txt`
- [ ] 有数值+公式（无CSV）→ 已生成并运行专项验证脚本，输出同格式保存
- [ ] 正文 Analysis 节**无**「数据验证」子章节
- [ ] 正文 Results/Analysis 节未出现任何用计算值替换原始数据的情况
- [ ] 有图表 → 已生成 `charts-init.js`，canvas id 与正文 `<canvas id="...">` 一致
- [ ] SVG 流程图（若有）已单独保存为 `.svg` 文件（如 `flowchart.svg`），与正文片段同目录；对应 `<figure>` 使用 `data-svg-src` 占位符，**不内嵌 SVG 代码**
- [ ] 偏差 > 20% → 已在生成报告前告知用户并确认继续
- [ ] 偏差 > 5% → 「讨论」节已补充偏差分析段落
- [ ] 引言、原理、讨论各节已通过 web_search 搜索权威文献
- [ ] 所有引用均有可访问URL或DOI，无虚构文献
- [ ] 参考文献按 GB/T 7714-2015 格式排列，含链接

**阶段二：拼装**
- [ ] 已运行 `build_html.py`（单文件用 `--body`，分段用 `--body-dir /outputs/XXXX报告名/body-parts/`）
- [ ] 脚本输出无 `[WARN]`（assets/report.css 和 report.js 均已找到）

**阶段三：输出**
- [ ] 已调用 `present_files` 向用户提供 HTML 文件下载

---

## 参考文件索引

| 文件 | 内容 | 何时读取 |
|------|------|----------|
| `references/html-template.md` | HTML结构参考骨架 | 生成 `report-body.html` 时参照结构 |
| `references/style-constitution.md` | 风格宪法框架 + 6套预置风格 | 用户指定非默认风格时 |
| `references/svg-flowchart-template.md` | SVG流程图模板和规范（含 `orient="auto"` 箭头方向核心机制） | 需要绘制流程图时 |
| `references/swd-chartjs-examples.md` | SWD原则Chart.js示例 | 生成 `charts-init.js` 时参照 |
| `references/gbt7714-reference-guide.md` | GB/T 7714格式详细规范与示例 | 撰写参考文献节时 |
| `assets/report.css` | 完整CSS（样式/响应式/深色模式/编辑器） | 由 `build_html.py` 自动读取，Agent不需读 |
| `assets/report.js` | 所有交互JS（目录/验证面板/内联编辑器） | 由 `build_html.py` 自动读取，Agent不需读 |
| `scripts/auto_verify.py` | CSV/表格数据自动验证脚本 | 有CSV或粘贴表格数据时 |
| `scripts/verify_data.py` | 手动填写的验证脚本模板 | 有数值+公式但无CSV时 |
| `scripts/build_html.py` | HTML拼装脚本 | 阶段二运行 |

---