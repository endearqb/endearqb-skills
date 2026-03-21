# 报告风格宪法（Style Constitution）

本文件定义实验报告HTML的设计语言系统。**默认风格**的完整实现记录在此；**自定义风格**须依照本宪法的约束框架替换相应层级的变量，保持结构规则不变。

---

## 一、设计语言解析：默认风格「暖墨纸」

默认风格的核心意象是**印刷在高质量道林纸上的学术期刊**。它用克制的暗青色点睛，用衬线字体传递严肃感，用温暖的米白消除屏幕冷感。

### 1.1 色彩层次（五层模型）

默认风格只用五个语义色槽，每层职责严格分离：

```
层级 1  底层背景（body background）
        #f6f4ee → #fbfaf6  线性渐变，带左上角淡青晕
        → 制造"纸张放在桌面上"的纵深感

层级 2  纸张（.page 卡片背景）
        #ffffff  纯白
        → 与底层形成轻微对比，强化"一张纸"的感知

层级 3  墨色系（文字与线条）
        --ink:   #1f2328   主文字、表头背景、重边框
        --muted: #5c6570   次要文字（图注、页脚、meta）
        --line:  #d7d0c3   分隔线、细边框
        → 三档灰度构成信息层级，无一为纯黑

层级 4  柔色填充（背景块）
        --soft:      #f5f1e7   暖米（悬停、TOC高亮背景）
        --soft-alt:  #eef4f1   冷米绿（callout背景）
        --soft-blue: #f3f6fb   淡蓝（公式块背景）
        → 三种微饱和色区分内容类型，互不冲突

层级 5  强调色（accent，全文唯一彩色）
        --accent: #2f4f4f   暗青绿
        → 用于：section标题小字、TOC active、链接、
                 悬浮目录高亮边、编辑按钮、callout左边框
        → 原则：只有一种强调色，绝不再引入第二彩色
```

### 1.2 字体系统（双轨制）

```
衬线轨（正文内容）：
  Georgia, "Noto Serif SC", "Songti SC", "STSong", serif
  用于：body、h1-h4、摘要、正文段落
  line-height: 1.82   → 比常规1.6更宽松，减少长文阅读疲劳
  text-align: justify → 两端对齐，期刊排版规范

无衬线轨（元数据/标签/UI）：
  "Helvetica Neue", Arial, sans-serif
  用于：journal-bar、meta-card标签、section小标题、
        TOC、页脚、编辑器UI、图注
  letter-spacing: 0.08–0.14em  → 稀字距，制造标签感
  text-transform: uppercase     → 全大写强化分类标签属性
```

### 1.3 结构规则（不随风格变化）

以下规则是**宪法级固定条款**，任何风格都不能改变：

```
① .page 最大宽度：980px，保持期刊单栏版面比例
② 悬浮目录：1280px 以上显示，宽度固定 200px，不压缩正文
③ 响应式三档：1280px+ / 860px / 600px，各自触发不同收窄策略
④ 层次靠线条/粗细，不靠颜色区分（无彩色背景章节块）
⑤ 强调色限一种，全文统一
⑥ 表头用 --ink 深色背景 + 白色文字（信息密度高时易区分）
⑦ 验证框配色固定：绿色系（pass）/ 橙色系（warn），不随主题变
⑧ 打印时去背景、去阴影、去编辑器UI（@media print 必须保留）
```

### 1.4 阴影哲学

```css
/* 默认：大偏移、大模糊、极低透明度 → "悬浮纸张"效果 */
--shadow: 0 18px 48px rgba(31,35,40,0.10);

/* 禁止：小偏移高透明度 → 会变成"网页卡片"质感，失去纸感 */
/* 禁止：多层叠加阴影 → 过度设计 */
```

---

## 二、风格宪法框架

### 2.1 四个可变层（允许替换）

自定义风格时，只替换以下四层，结构和JS逻辑一律不动：

```
可变层 A  配色系统（CSS变量）
          替换 :root 中的 10 个变量

可变层 B  字体系统（font-family + line-height）
          替换 body 字体声明，可引入 Google Fonts

可变层 C  背景纹理（body background）
          替换 body 的 background 属性

可变层 D  强调色衍生（accent相关颜色）
          --accent 变了，body background 中的 rgba 晕也要同步调整
```

### 2.2 变量替换模板

生成自定义风格时，复制此块替换 :root：

```css
:root {
  /* === 可变层 A：配色 === */
  --paper:     [底层背景色，略深于 --page];
  --page:      [纸张/卡片背景色];
  --ink:       [主文字色，建议深色，对比度 ≥ 4.5:1];
  --muted:     [次要文字色，比 --ink 浅 30-40%];
  --line:      [分隔线色，比 --paper 深一档，低饱和];
  --soft:      [暖色填充，用于悬停/TOC高亮，与 --paper 同色温];
  --soft-alt:  [冷色填充，callout 背景，与 --accent 同色系但极淡];
  --soft-blue: [公式块背景，可改为与主题配套的极淡色];
  --accent:    [唯一强调色，整份报告只有这一个彩色];
  --shadow:    [卡片阴影，保持低透明度];

  /* === 可变层 B：字体（可选替换）=== */
  /* 若引入 Google Fonts，在 <head> 加 <link> 后修改此处 */
}

body {
  /* === 可变层 C：背景纹理 === */
  background: [替换为新背景];

  /* === 可变层 B：字体 === */
  font-family: [替换字体栈];
  line-height: [建议保持 1.7–1.9 之间];
}
```

### 2.3 强调色衍生规则

替换 `--accent` 后，以下位置必须同步更新，确保风格一致：

| 位置 | 当前默认值 | 替换规则 |
|------|-----------|---------|
| `body` background 晕 | `rgba(47,79,79,0.08)` | 改为 `rgba(accent的RGB, 0.08)` |
| `.callout` 左边框 | `#3f6b68` | 改为 accent 的稍深版本 |
| `.callout` 背景 | `#edf4f1 → #f7fbfa` | 改为 accent 的极淡渐变 |
| `.float-toc a.active` border | `var(--accent)` | 自动继承，无需改 |
| 编辑按钮背景 | `var(--accent)` | 自动继承，无需改 |

---

## 三、预置风格库

每个预置风格提供完整的「可变层 A+B+C+D」替换值，可直接使用。

---

### 风格 01：暖墨纸（默认）Warm Ink Paper

**意象**：高质量道林纸期刊。沉稳、克制、学术。  
**适用场景**：理工科实验课、科研记录、工程技术报告。

```css
:root {
  --paper:     #fbfaf6;
  --page:      #ffffff;
  --ink:       #1f2328;
  --muted:     #5c6570;
  --line:      #d7d0c3;
  --soft:      #f5f1e7;
  --soft-alt:  #eef4f1;
  --soft-blue: #f3f6fb;
  --accent:    #2f4f4f;
  --shadow:    0 18px 48px rgba(31,35,40,0.10);
}
body {
  background:
    radial-gradient(circle at top left, rgba(47,79,79,0.08), transparent 30%),
    linear-gradient(180deg, #f6f4ee 0%, var(--paper) 100%);
  font-family: Georgia, "Noto Serif SC", "Songti SC", "STSong", serif;
  line-height: 1.82;
}
/* callout 衍生色 */
.callout { background: linear-gradient(180deg,#edf4f1 0%,#f7fbfa 100%); border-left-color: #3f6b68; }
```

---

### 风格 02：午夜藏青 Midnight Navy

**意象**：深色背景，藏青主调，金色点睛。精英感、高密度信息。  
**适用场景**：竞赛展示报告、科研论文级记录、汇报型技术文档。

```css
/* Google Fonts（在 <head> 添加）：
   <link href="https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,opsz,wght@0,8..60,300..900;1,8..60,300..900&display=swap" rel="stylesheet"> */

:root {
  --paper:     #0d1117;
  --page:      #161b22;
  --ink:       #e6edf3;
  --muted:     #7d8590;
  --line:      #30363d;
  --soft:      #1c2128;
  --soft-alt:  #1a2332;
  --soft-blue: #172033;
  --accent:    #c9a84c;   /* 金色 */
  --shadow:    0 18px 48px rgba(0,0,0,0.40);
}
body {
  background:
    radial-gradient(circle at top left, rgba(201,168,76,0.06), transparent 30%),
    linear-gradient(180deg, #090d13 0%, var(--paper) 100%);
  font-family: "Source Serif 4", Georgia, "Noto Serif SC", serif;
  line-height: 1.80;
}
/* 深色模式下特殊调整 */
th { background: #21262d; color: #e6edf3; }
tbody tr:nth-child(even) td { background: #1c2128; }
.abstract { background: #1a2332; border-left-color: var(--accent); }
.formula { background: var(--soft-blue); border-color: #2d3748; }
.verification { background: #162118; border-color: #2d5a27; border-left-color: #3fb950; }
.callout { background: linear-gradient(180deg,#1a2a1a 0%,#162820 100%); border-left-color: #3f6b3a; }
.toc { background: var(--soft); border-color: var(--line); }
.chart-container { background: #1c2128; border-color: var(--line); }
a { color: var(--accent); }
```

---

### 风格 03：净白简约 Clean White

**意象**：极简主义，无纹理纯白，蓝色强调。现代、清晰、国际化。  
**适用场景**：工程项目技术报告、英文报告、跨学科展示。

```css
/* Google Fonts：
   <link href="https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400..700;1,400..700&display=swap" rel="stylesheet"> */

:root {
  --paper:     #f8f9fa;
  --page:      #ffffff;
  --ink:       #212529;
  --muted:     #6c757d;
  --line:      #dee2e6;
  --soft:      #f1f3f5;
  --soft-alt:  #e8f4fd;
  --soft-blue: #ebf5fb;
  --accent:    #1a6eb5;   /* 深宝蓝 */
  --shadow:    0 8px 32px rgba(0,0,0,0.08);
}
body {
  background: var(--paper);   /* 无渐变，极简纯色 */
  font-family: "Lora", Georgia, "Noto Serif SC", serif;
  line-height: 1.78;
}
.page { border: none; border-top: 3px solid var(--accent); }
.callout { background: linear-gradient(180deg,#e8f4fd 0%,#f0f7ff 100%); border-left-color: #1a6eb5; }
.abstract { background: #f0f7ff; border-left-color: var(--ink); }
```

---

### 风格 04：橄榄学报 Olive Scholar

**意象**：橄榄绿调，复古学院气息，近似自然科学期刊。  
**适用场景**：生物、化学、环境类实验报告，科研记录。

```css
:root {
  --paper:     #f7f5ef;
  --page:      #fefdfb;
  --ink:       #2c2a1e;
  --muted:     #6b6550;
  --line:      #ccc9b4;
  --soft:      #eeeade;
  --soft-alt:  #edf0e5;
  --soft-blue: #edf2e8;
  --accent:    #4a6741;   /* 橄榄绿 */
  --shadow:    0 16px 44px rgba(44,42,30,0.11);
}
body {
  background:
    radial-gradient(circle at top left, rgba(74,103,65,0.07), transparent 30%),
    linear-gradient(180deg, #efede4 0%, var(--paper) 100%);
  font-family: Georgia, "Noto Serif SC", serif;
  line-height: 1.84;
}
.callout { background: linear-gradient(180deg,#edf0e5 0%,#f4f6ef 100%); border-left-color: #4a6741; }
tbody tr:nth-child(even) td { background: #f3f1e8; }
td { border-bottom-color: #ddd8c4; }
```

---

### 风格 05：砖红工程 Engineering Red

**意象**：工业感，砖红主调，钢铁灰配色。严肃、精准。  
**适用场景**：机械、电气、土木、材料类工程技术报告。

```css
:root {
  --paper:     #f9f7f5;
  --page:      #ffffff;
  --ink:       #1c1c1e;
  --muted:     #636366;
  --line:      #d1cbc3;
  --soft:      #f4eeea;
  --soft-alt:  #fdf1ee;
  --soft-blue: #f5f5f7;
  --accent:    #9b2335;   /* 砖红 */
  --shadow:    0 12px 40px rgba(28,28,30,0.10);
}
body {
  background:
    radial-gradient(circle at top left, rgba(155,35,53,0.05), transparent 30%),
    linear-gradient(180deg, #f2efec 0%, var(--paper) 100%);
  font-family: Georgia, "Noto Serif SC", serif;
  line-height: 1.80;
}
.callout { background: linear-gradient(180deg,#fdf1ee 0%,#fdf8f7 100%); border-left-color: #9b2335; }
tbody tr:nth-child(even) td { background: #faf8f6; }
```

---

### 风格 06：石墨极简 Graphite Minimal

**意象**：冷灰调，极度克制，接近黑白印刷感。  
**适用场景**：答辩稿、正式提交文档、需要打印为黑白的场合。

```css
:root {
  --paper:     #f5f5f5;
  --page:      #ffffff;
  --ink:       #1a1a1a;
  --muted:     #666666;
  --line:      #cccccc;
  --soft:      #ebebeb;
  --soft-alt:  #f0f0f0;
  --soft-blue: #f0f0f4;
  --accent:    #333333;   /* 深灰作为强调色，近乎黑白 */
  --shadow:    0 8px 28px rgba(0,0,0,0.08);
}
body {
  background: var(--paper);
  font-family: Georgia, "Noto Serif SC", serif;
  line-height: 1.80;
}
/* 极简模式：去除所有装饰性渐变 */
.page { border: 1px solid var(--line); }
.abstract { background: #f5f5f5; border-left-color: var(--ink); }
.callout { background: #f0f0f0; border-left-color: #666; }
```

---

### 风格 07：琥珀审查 Amber Review

**意象**：琥珀橙主调，带斜纹警告纹理，传递"请注意、待核查"的视觉信号。  
**适用场景**：**数据存在重大偏差（>20%）时自动启用**；也适用于草稿审阅版、同行评议版、数据待确认版本。  
**触发规则**：当 Python 验证发现任意一项偏差 > 20% 时，**必须**自动切换至本风格，无需用户指定。

```css
:root {
  --paper:     #fdf8f0;
  --page:      #fffdf8;
  --ink:       #1c1a14;
  --muted:     #6b6248;
  --line:      #e0d4b8;
  --soft:      #faf2de;
  --soft-alt:  #fef9ec;
  --soft-blue: #fdf4e0;
  --accent:    #b45309;   /* 琥珀橙：唯一强调色 */
  --shadow:    0 18px 52px rgba(180,83,9,0.10);

  /* 警告专属语义色（本风格独有，其他风格不使用）*/
  --warn-bg:      #fff7ed;
  --warn-border:  #f59e0b;
  --warn-text:    #92400e;
  --warn-stripe:  repeating-linear-gradient(
                    -45deg,
                    transparent, transparent 8px,
                    rgba(245,158,11,0.06) 8px,
                    rgba(245,158,11,0.06) 16px
                  );
}
body {
  background:
    radial-gradient(circle at top left, rgba(180,83,9,0.07), transparent 28%),
    linear-gradient(180deg, #f9f1e4 0%, var(--paper) 100%);
  font-family: Georgia, "Noto Serif SC", serif;
  line-height: 1.82;
}

/* 页面顶部橙色警示线 */
.page {
  border: 1px solid rgba(180,83,9,0.12);
  border-top: 4px solid var(--warn-border);
}

/* 衍生色 */
.abstract  { background: var(--soft-alt); border-left-color: var(--accent); }
.callout   { background: linear-gradient(180deg,#fef9ec 0%,#fdf5e0 100%); border-left-color: var(--accent); }
.meta-card { background: linear-gradient(180deg,#fef9ec 0%,#faf2dc 100%); border-color: var(--warn-border); }
.toc       { background: var(--soft); }
th         { background: #78350f; }
tbody tr:nth-child(even) td { background: #fdf8f0; }
td         { border-bottom-color: #e8dccc; }
```

#### 警告风格专属 HTML 组件（本风格独有，其他风格不需要）

生成琥珀审查风格报告时，必须额外添加以下三类组件：

**① 全局数据警告横幅**（插入在 `.journal-bar` 之后，封面之前）

```html
<!-- journal-bar 中 DOI 位置改为警告标记 -->
<div class="journal-bar">
  <div>[期刊/机构名称]</div>
  <div style="color:#b45309;font-weight:700;">⚠ 数据待核查版本 · Data Under Review</div>
</div>

<div class="data-alert-banner">
  <div class="banner-icon">⚠️</div>
  <div class="banner-body">
    <p class="banner-title">本报告存在需核查的数据问题，请读者注意</p>
    <p class="banner-desc">经自动化数据校验，发现以下问题，在原作者确认修正前请谨慎引用相关数据：</p>
    <ul class="banner-items">
      <!-- 每个 >20% 偏差项各一条 li -->
      <li><strong>[严重程度]：</strong>[具体偏差描述]</li>
    </ul>
  </div>
</div>
```

**② 行内数据徽章**（标注在含存疑数据的句子末尾）

```html
<!-- 通过验证 -->
<span class="badge-ok">✓ 校验通过</span>

<!-- 存疑 -->
<span class="badge-warn">⚠ 数据存疑</span>
```

**③ 斜纹警告框**（替换普通 `.warn-box`，用于标注具体偏差数据段落）

```html
<div class="warn-box">
  <p>⚠ <strong>数据存疑 — [字段名]</strong>：[偏差描述，包含计算值 vs 声称值，偏差倍数]。
  此数据在确认前不建议引用。</p>
</div>
```

#### 琥珀审查风格专属 CSS

以下 CSS 须追加到报告 `<style>` 块末尾（其他风格不需要）：

```css
/* 全局警告横幅 */
.data-alert-banner {
  margin: 0 0 28px;
  padding: 14px 20px;
  background: var(--warn-stripe), #fff7ed;
  border: 2px solid var(--warn-border);
  border-radius: 6px;
  display: flex; align-items: flex-start; gap: 14px;
}
.data-alert-banner .banner-icon  { font-size: 22px; flex-shrink: 0; line-height: 1; margin-top: 2px; }
.data-alert-banner .banner-body  { flex: 1; }
.data-alert-banner .banner-title { font: 700 14px/1.4 "Helvetica Neue",Arial,sans-serif; color: #92400e; margin: 0 0 5px; }
.data-alert-banner .banner-desc  { font-size: 13.5px; color: #78350f; margin: 0; line-height: 1.6; }
.data-alert-banner .banner-items { margin: 8px 0 0; padding: 0 0 0 16px; font-size: 13px; color: #92400e; }
.data-alert-banner .banner-items li { margin: 4px 0; }

/* 斜纹警告框 */
.warn-box {
  margin: 22px 0;
  padding: 18px 20px;
  background: var(--warn-stripe), var(--warn-bg);
  border: 1.5px solid var(--warn-border);
  border-left: 5px solid var(--warn-border);
  border-radius: 0 6px 6px 0;
}
.warn-box p       { margin: 0; font-size: 14px; color: var(--warn-text); }
.warn-box strong  { color: #78350f; }

/* 行内徽章 */
.badge-warn {
  display: inline-block;
  font: 700 11px/1 "Helvetica Neue",Arial,sans-serif;
  padding: 2px 7px; border-radius: 10px;
  background: #fef3c7; color: #92400e;
  border: 1px solid #fbbf24; vertical-align: middle; margin-left: 4px;
}
.badge-ok {
  display: inline-block;
  font: 700 11px/1 "Helvetica Neue",Arial,sans-serif;
  padding: 2px 7px; border-radius: 10px;
  background: #dcfce7; color: #166534;
  border: 1px solid #86efac; vertical-align: middle; margin-left: 4px;
}
```

---

## 四、自定义风格生成流程

当用户在 prompt 中提到使用非默认风格时，按以下流程生成：

### Step 1：识别风格意图

用户描述 → 匹配预置库或自行创作：

| 用户说 | 对应动作 |
|--------|---------|
| "深色/暗色风格" | 使用「午夜藏青」或基于其框架调整 |
| "简洁/极简/白色" | 使用「净白简约」 |
| "学院/复古/自然科学" | 使用「橄榄学报」 |
| "工程/机械/电气" | 使用「砖红工程」 |
| "黑白/打印/答辩" | 使用「石墨极简」 |
| "暖色/米色/默认" | 使用「暖墨纸」（默认） |
| **数据偏差 > 20%（自动触发）** | **使用「琥珀审查」** |
| 指定具体颜色/风格名 | 基于宪法框架自行创作新风格 |

### Step 2：应用变量替换

1. 复制「暖墨纸」的完整 CSS 作为基础
2. 用目标风格的 `:root` 变量块替换 `:root`
3. 用目标风格的 `body { background: ... }` 替换 body 背景
4. 检查「强调色衍生规则」，补充 `.callout`、`.abstract`、`.verification` 等衍生色
5. 深色风格额外检查：`th`、`tbody even`、`a`、`.toc`、`.chart-container`

### Step 3：宪法合规检查

生成后逐项确认：
- [ ] `--accent` 只有一种颜色，无第二彩色
- [ ] 深色模式下 `--ink` 对 `--page` 对比度 ≥ 4.5:1
- [ ] `.verification` 的绿色/橙色系保留（固定宪法条款）
- [ ] `@media print` 规则完整保留
- [ ] 悬浮目录 `.float-toc` 的 `--accent` 相关颜色已同步

### Step 4：Chart.js 配色同步

图表颜色需与风格同步：

```javascript
// 主色系列（从 --accent 派生）
const CHART_PRIMARY = getComputedStyle(document.documentElement)
  .getPropertyValue('--accent').trim();

// 深色背景风格下，网格线颜色需改淡
const CHART_GRID = 风格是深色 ? 'rgba(255,255,255,0.08)' : '#f0ece2';
```

---

## 五、新风格创作规范

当没有预置风格匹配用户需求时，从头创作新风格，须遵守：

### 色彩创作约束

```
① --ink 的亮度（L in HSL）：
     浅色背景风格：L ≤ 20%（确保深色文字）
     深色背景风格：L ≥ 80%（确保浅色文字）

② --accent 的饱和度：S = 30–70%（太低无感知，太高刺眼）

③ --paper 与 --page 的亮度差：ΔL = 2–6%（对比但不跳跃）

④ --soft / --soft-alt / --soft-blue 必须是 --accent 同色温的极淡版，
   饱和度 < 15%，亮度 > 90%（浅色）或 < 20%（深色）

⑤ --line 的饱和度 < 20%，是中性过渡色，不能有明显彩色感
```

### 禁止项

```
✗ 引入两种强调色
✗ body 背景使用纯白（失去纸感）或纯黑（太压抑）
✗ 彩色表格行（even row 只能用极淡的 --soft 衍生色）
✗ 彩色边框（除 .callout 左边框外，所有边框用 --line）
✗ 字体使用系统无衬线字体（Arial、system-ui）作为正文主字体
✗ 去掉 .abstract 的左边框（是结构标识，不是装饰）
```

### 深色风格额外规范

```
• body background：避免纯黑（#000），用 #090d13–#111827 之间的深蓝黑
• 阴影透明度提高至 0.30–0.45（深底需要更强阴影才有卡片感）
• --soft-blue 等填充色改为比 --page 再深一档的颜色（而非更淡）
• 链接颜色改为 --accent（深色背景下蓝色链接对比度往往不足）
• 图表网格线改为 rgba(255,255,255,0.06–0.10)
```
