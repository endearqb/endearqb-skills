# SVG流程图模板与规范

## 触发条件

**仅在以下情况绘制SVG流程图：**
- 用户描述了实验步骤或操作流程（≥ 3个步骤）
- 用户明确要求画流程图
- 实验涉及复杂的多阶段工序

**不绘制的情况：**
- 用户只有文字描述但没有明确步骤
- 用户没有提供流程信息

---

## ⚠️ 箭头方向核心机制（必读，不可忽略）

### `orient="auto"` 的工作原理

SVG `<marker>` 的 `orient="auto"` 会将 marker 的**本地 +x 轴**旋转对齐到连线的行进方向。

**关键推论：箭头尖必须指向 marker 本地坐标的 +x 方向**（即 path 中 x 坐标最大的顶点为尖端）。

```
正确 ✅：尖端在 +x 方向（x 最大处）
  <path d="M0,0 L0,6 L9,3 z"/>
  解释：顶点分别在 (0,0)、(0,6)、(9,3)
        x 最大的顶点是 (9,3) → 箭头尖在此 → 指向 +x → 朝向连线终点 ✓

错误 ❌：尖端在 -x 方向（x 最小处）
  <path d="M9,0 L9,6 L0,3 z"/>
  解释：x 最小的顶点是 (0,3) → 箭头尖在此 → 指向 -x → 箭头反向 ✗
```

### 配套 `refX` 设置

`refX` 决定 marker 的哪个点对齐到连线终点：
- **`refX="9"`（推荐）**：将箭头尖（x=9 处）对齐到终点，箭头不超出节点边缘
- **`refX="8"`**：箭头尖略微缩入连线内（适合线段末端有间距时）

```xml
<!-- 标准箭头 marker 写法 -->
<marker id="arr" markerWidth="10" markerHeight="7"
        refX="9" refY="3.5" orient="auto">
  <path d="M0,0 L0,7 L10,3.5 z" fill="#2f4f4f"/>
</marker>
```

### 常见错误排查

| 症状 | 原因 | 修复方法 |
|------|------|---------|
| 箭头反向（指向起点） | path 尖端在 x 最小处 | 翻转 path，确保 x 最大顶点为尖端 |
| 箭头偏离连线 | `refY` 不等于箭头高度的一半 | 设 `refY = markerHeight / 2` |
| 箭头悬空不贴终点 | `refX` 过小 | 将 `refX` 设为箭头尖的 x 坐标值 |
| 水平箭头正常，垂直反向 | `orient` 未设为 `"auto"` | 检查 `orient="auto"` 是否存在 |

---

## 配色规范（通过 CSS 变量跟随页面主题）

SVG 内嵌到 HTML 后，可直接读取页面 `:root` 上的 CSS 变量。**所有颜色必须使用变量，禁止硬编码色值。**

```
--svg-node-bg      通用步骤框背景（暖白）
--svg-node-alt     关键步骤/成功路径框背景（淡绿调）
--svg-node-data    数据采集步骤框背景（淡蓝调）
--svg-node-warn    注意/风险步骤框背景（淡红调）
--svg-diamond-bg   判断菱形背景（淡黄调）
--svg-diamond-stroke 判断菱形边框
--svg-stroke       节点通用边框色
--svg-arrow        箭头与连线色
--svg-start-bg     开始节点实心背景（= accent）
--svg-end-bg       结束节点实心背景（深色）
--svg-text         主文字色
--svg-text-sub     副文字/说明文字色
--svg-start-text   开始/结束节点上的文字色（白或亮色）
```

各变量默认值定义在 `report.css` 的 `:root` 中，每套主题在 `build_html.py` 的主题 CSS 块里覆盖对应值。

---

## 垂直流程图模板（4步）

适合：线性实验流程

```svg
<svg width="560" height="316" viewBox="0 0 560 316" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arr" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <path d="M0,0 L0,7 L10,3.5 z" fill="var(--svg-arrow)"/>
    </marker>
  </defs>

  <!-- 步骤1：节点垂直中心 y=48（20+56/2） -->
  <rect x="160" y="20" width="240" height="56" rx="8" fill="var(--svg-node-bg)" stroke="var(--svg-stroke)" stroke-width="1.5"/>
  <text x="280" y="38" text-anchor="middle" dominant-baseline="central" font-size="15" font-family="Georgia,serif" fill="var(--svg-text)">[步骤1标题]</text>
  <text x="280" y="58" text-anchor="middle" dominant-baseline="central" font-size="12" font-family="Arial,sans-serif" fill="var(--svg-text-sub)">[说明文字]</text>

  <!-- 箭头1→2 -->
  <line x1="280" y1="76" x2="280" y2="100" stroke="var(--svg-arrow)" stroke-width="2" marker-end="url(#arr)"/>

  <!-- 步骤2：节点垂直中心 y=128（100+56/2） -->
  <rect x="160" y="100" width="240" height="56" rx="8" fill="var(--svg-node-alt)" stroke="var(--svg-stroke)" stroke-width="1.5"/>
  <text x="280" y="118" text-anchor="middle" dominant-baseline="central" font-size="15" font-family="Georgia,serif" fill="var(--svg-text)">[步骤2标题]</text>
  <text x="280" y="138" text-anchor="middle" dominant-baseline="central" font-size="12" font-family="Arial,sans-serif" fill="var(--svg-text-sub)">[说明文字]</text>

  <!-- 箭头2→3 -->
  <line x1="280" y1="156" x2="280" y2="180" stroke="var(--svg-arrow)" stroke-width="2" marker-end="url(#arr)"/>

  <!-- 步骤3：节点垂直中心 y=208（180+56/2） -->
  <rect x="160" y="180" width="240" height="56" rx="8" fill="var(--svg-node-data)" stroke="var(--svg-stroke)" stroke-width="1.5"/>
  <text x="280" y="198" text-anchor="middle" dominant-baseline="central" font-size="15" font-family="Georgia,serif" fill="var(--svg-text)">[步骤3标题]</text>
  <text x="280" y="218" text-anchor="middle" dominant-baseline="central" font-size="12" font-family="Arial,sans-serif" fill="var(--svg-text-sub)">[说明文字]</text>

  <!-- 箭头3→4 -->
  <line x1="280" y1="236" x2="280" y2="260" stroke="var(--svg-arrow)" stroke-width="2" marker-end="url(#arr)"/>

  <!-- 步骤4：节点垂直中心 y=288（260+56/2） -->
  <rect x="160" y="260" width="240" height="56" rx="8" fill="var(--svg-node-bg)" stroke="var(--svg-stroke)" stroke-width="1.5"/>
  <text x="280" y="278" text-anchor="middle" dominant-baseline="central" font-size="15" font-family="Georgia,serif" fill="var(--svg-text)">[步骤4标题]</text>
  <text x="280" y="298" text-anchor="middle" dominant-baseline="central" font-size="12" font-family="Arial,sans-serif" fill="var(--svg-text-sub)">[说明文字]</text>
</svg>
```

---

## 水平流程图模板（3步）

适合：简单线性流程，横向展示

```svg
<svg width="880" height="160" viewBox="0 0 880 160" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arr-h" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <path d="M0,0 L0,7 L10,3.5 z" fill="var(--svg-arrow)"/>
    </marker>
  </defs>

  <!-- 步骤1：节点垂直中心 y=80（40+80/2） -->
  <rect x="30" y="40" width="220" height="80" rx="8" fill="var(--svg-node-bg)" stroke="var(--svg-stroke)" stroke-width="1.5"/>
  <text x="140" y="72" text-anchor="middle" dominant-baseline="central" font-size="16" font-family="Georgia,serif" fill="var(--svg-text)">[步骤1]</text>
  <text x="140" y="96" text-anchor="middle" dominant-baseline="central" font-size="12" font-family="Arial,sans-serif" fill="var(--svg-text-sub)">[说明]</text>

  <!-- 箭头 -->
  <line x1="250" y1="80" x2="330" y2="80" stroke="var(--svg-arrow)" stroke-width="2.5" marker-end="url(#arr-h)"/>
  <text x="290" y="68" text-anchor="middle" font-size="11" font-family="Arial,sans-serif" fill="var(--svg-arrow)">[条件]</text>

  <!-- 步骤2：节点垂直中心 y=80（40+80/2） -->
  <rect x="330" y="40" width="220" height="80" rx="8" fill="var(--svg-node-alt)" stroke="var(--svg-stroke)" stroke-width="1.5"/>
  <text x="440" y="72" text-anchor="middle" dominant-baseline="central" font-size="16" font-family="Georgia,serif" fill="var(--svg-text)">[步骤2]</text>
  <text x="440" y="96" text-anchor="middle" dominant-baseline="central" font-size="12" font-family="Arial,sans-serif" fill="var(--svg-text-sub)">[说明]</text>

  <!-- 箭头 -->
  <line x1="550" y1="80" x2="630" y2="80" stroke="var(--svg-arrow)" stroke-width="2.5" marker-end="url(#arr-h)"/>

  <!-- 步骤3：节点垂直中心 y=80（40+80/2） -->
  <rect x="630" y="40" width="220" height="80" rx="8" fill="var(--svg-node-data)" stroke="var(--svg-stroke)" stroke-width="1.5"/>
  <text x="740" y="72" text-anchor="middle" dominant-baseline="central" font-size="16" font-family="Georgia,serif" fill="var(--svg-text)">[步骤3]</text>
  <text x="740" y="96" text-anchor="middle" dominant-baseline="central" font-size="12" font-family="Arial,sans-serif" fill="var(--svg-text-sub)">[说明]</text>
</svg>
```

---

## 带判断分支的流程图模板

适合：含条件判断的实验流程（如：合格/不合格分支）

```svg
<svg width="600" height="460" viewBox="0 0 600 460" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arr-b" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <path d="M0,0 L0,7 L10,3.5 z" fill="var(--svg-arrow)"/>
    </marker>
  </defs>

  <!-- 开始：节点垂直中心 y=45（20+50/2） -->
  <rect x="200" y="20" width="200" height="50" rx="25" fill="var(--svg-start-bg)" stroke="none"/>
  <text x="300" y="45" text-anchor="middle" dominant-baseline="central" font-size="15" font-family="Georgia,serif" fill="var(--svg-start-text)">开始</text>

  <line x1="300" y1="70" x2="300" y2="110" stroke="var(--svg-arrow)" stroke-width="2" marker-end="url(#arr-b)"/>

  <!-- 步骤框：节点垂直中心 y=137.5（110+55/2） -->
  <rect x="180" y="110" width="240" height="55" rx="8" fill="var(--svg-node-bg)" stroke="var(--svg-stroke)" stroke-width="1.5"/>
  <text x="300" y="137" text-anchor="middle" dominant-baseline="central" font-size="14" font-family="Georgia,serif" fill="var(--svg-text)">[操作步骤]</text>

  <line x1="300" y1="165" x2="300" y2="205" stroke="var(--svg-arrow)" stroke-width="2" marker-end="url(#arr-b)"/>

  <!-- 判断菱形 -->
  <polygon points="300,205 400,255 300,305 200,255" fill="var(--svg-diamond-bg)" stroke="var(--svg-diamond-stroke)" stroke-width="1.5"/>
  <text x="300" y="255" text-anchor="middle" dominant-baseline="central" font-size="13" font-family="Arial,sans-serif" fill="var(--svg-text)">[判断条件]？</text>

  <!-- 是→右 -->
  <line x1="400" y1="255" x2="480" y2="255" stroke="var(--svg-arrow)" stroke-width="2" marker-end="url(#arr-b)"/>
  <text x="440" y="245" text-anchor="middle" font-size="12" fill="var(--svg-arrow)">是</text>
  <rect x="480" y="225" width="100" height="60" rx="8" fill="var(--svg-node-alt)" stroke="var(--svg-stroke)" stroke-width="1.5"/>
  <text x="530" y="255" text-anchor="middle" dominant-baseline="central" font-size="12" font-family="Arial,sans-serif" fill="var(--svg-text)">[处理A]</text>

  <!-- 否→下 -->
  <line x1="300" y1="305" x2="300" y2="345" stroke="var(--svg-arrow)" stroke-width="2" marker-end="url(#arr-b)"/>
  <text x="316" y="330" font-size="12" fill="var(--svg-arrow)">否</text>
  <rect x="180" y="345" width="240" height="55" rx="8" fill="var(--svg-node-warn)" stroke="var(--svg-stroke)" stroke-width="1.5"/>
  <text x="300" y="372" text-anchor="middle" dominant-baseline="central" font-size="14" font-family="Georgia,serif" fill="var(--svg-text)">[处理B / 重做]</text>

  <!-- 结束：节点垂直中心 y=435（420+30/2） -->
  <line x1="300" y1="400" x2="300" y2="420" stroke="var(--svg-arrow)" stroke-width="2" marker-end="url(#arr-b)"/>
  <rect x="200" y="420" width="200" height="30" rx="15" fill="var(--svg-end-bg)" stroke="none"/>
  <text x="300" y="435" text-anchor="middle" dominant-baseline="central" font-size="14" font-family="Georgia,serif" fill="var(--svg-start-text)">结束</text>
</svg>
```

---

## 步骤框间距计算

每个步骤框高度 56px，步骤框间距 24px（箭头区域），顶部和底部各留 20px，则：

```
垂直 N 步流程图总高 H = 20 + N×56 + (N-1)×24 + 20
                      = N×80 − 4
```

| N | 高度 H |
|---|--------|
| 2 | 156 |
| 3 | 236 |
| 4 | 316 |
| 5 | 396 |
| 6 | 476 |
| 7 | 556 |

> ⚠️ 旧写法 `N×80+20` 漏掉底部留白，末节点底边会贴住 viewBox 边缘，stroke 可能被裁切。务必用新公式。

---

## 步骤数量适配

| 步骤数 | 建议布局 | SVG尺寸参考 |
|--------|----------|------------|
| 2–4步 | 垂直或水平 | `560 × (N×80−4)` 或 880×160 |
| 5–7步 | 垂直 | `560 × (N×80−4)` |
| 8步以上 | 分组水平+垂直混合，或拆成多个子流程图 | — |
| 含分支 | 带菱形判断节点 | 按内容手动测量 |

---

## ⚠ SVG `<text>` 内禁止嵌套 HTML 标签

SVG `<text>` 元素内**严禁**嵌套任何 HTML 标签（如 `<strong>`、`<sub>`、`<em>`）。浏览器遇到这类标签会将其"提升"出 SVG，导致文字渲染在页面正文流而非图形内部。

| 需求 | 错误写法 | 正确写法 |
|------|---------|---------|
| 粗体 | `<text><strong>步骤</strong></text>` | `<text font-weight="bold">步骤</text>` 或 `<tspan font-weight="bold">步骤</tspan>` |
| 下标 | `<text>H<sub>2</sub>O</text>` | `<text>H<tspan baseline-shift="sub" font-size="0.75em">2</tspan>O</text>` |
| 斜体/强调 | `<text><em>x</em></text>` | `<text font-style="italic">x</text>` 或 `<tspan font-style="italic">x</tspan>` |

---

## SVG 独立文件 + 注入机制

SVG **不内嵌在正文 HTML 片段中**，而是单独保存为 `.svg` 文件，由 `build_html.py` 在拼装时自动注入。

**① Claude 生成 SVG 文件**（如 `flowchart.svg`、`apparatus.svg`），保存在与正文同一目录：

```
body-parts/
  body-04-methods.html     ← 只含占位符，不含 SVG 代码
  flowchart.svg            ← 独立 SVG 文件
  apparatus.svg            ← 若有多图，用不同文件名
```

**② 正文 HTML 片段用 `data-svg-src` 属性标记注入位置**：

```html
<section id="methods">
  <h2 class="section-title">3. 实验装置与方法</h2>
  <p>实验采用...</p>
  <figure data-svg-src="flowchart.svg">
    <figcaption>图 1. 实验流程图</figcaption>
  </figure>
  <figure data-svg-src="apparatus.svg">
    <figcaption>图 2. 实验装置示意图</figcaption>
  </figure>
</section>
```

**③ `build_html.py` 自动完成注入**（默认在正文同目录查找）：

```bash
# SVG 与 body-parts/ 同目录，自动找到
python scripts/build_html.py --body-dir body-parts/ --output report.html
# SVG 在单独目录时用 --svg-dir 指定
python scripts/build_html.py --body-dir body-parts/ --svg-dir svgs/ --output report.html
```

> ⚠️ SVG 文件不要包含 `<?xml ...?>` 声明行（脚本会自动去除）。若文件未找到，占位符原样保留并打印 `[WARN]`，不中断构建。
