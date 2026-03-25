# report-body.html 结构参考

生成 `report-body.html` 时照此骨架写。CSS 和 JS 由 `build_html.py` 从 `assets/` 自动注入，**此文件不含样式代码**。

---

## 完整骨架

```html
<!-- 布局容器：正文 + 宽屏悬浮目录并排 -->
<div class="report-layout">
<main class="page">

  <!-- ① 期刊顶栏 -->
  <div class="journal-bar">
    <div>[课程名称] Lab Report</div>
    <div>Report Date: [日期]</div>
  </div>

  <!-- ② 封面（两栏：左标题 / 右元数据卡片） -->
  <section class="cover">
    <div>
      <h1>[实验报告标题]</h1>
      <p class="subtitle">[副标题或实验编号]</p>
    </div>
    <aside class="meta-card">
      <h2>Report Info</h2>
      <dl>
        <dt>作者</dt>   <dd>[姓名]</dd>
        <dt>学号</dt>   <dd>[学号]</dd>
        <dt>指导教师</dt><dd>[教师]</dd>
        <dt>实验日期</dt><dd>[日期]</dd>
        <dt>提交日期</dt><dd>[日期]</dd>
        <dt>课程</dt>   <dd>[课程名]</dd>
      </dl>
    </aside>
  </section>

  <!-- ③ 摘要 -->
  <section class="abstract">
    <h2>Abstract</h2>
    <p>[摘要，150–300字：目的、方法、主要结果、结论]</p>
    <p class="keywords"><strong>关键词：</strong>[词1]；[词2]；[词3]</p>
  </section>

  <!-- ④ 内联目录（inline，页内显示） -->
  <nav class="toc">
    <h2>Contents</h2>
    <ol>
      <li><a href="#intro">1. 引言</a></li>
      <li><a href="#theory">2. 实验原理</a></li>
      <li><a href="#methods">3. 实验装置与方法</a></li>
      <li><a href="#results">4. 实验结果</a></li>
      <li><a href="#analysis">5. 数据处理与分析</a></li>
      <li><a href="#discussion">6. 讨论</a></li>
      <li><a href="#conclusion">7. 结论</a></li>
      <li><a href="#references">参考文献</a></li>
    </ol>
  </nav>

  <div class="divider"></div>

  <!-- ⑤ 正文各节
       规则：
         - section id 必须与目录 href 和 float-toc href 一一对应
         - h2 必须加 class="section-title"
         - 引言/原理/讨论节含 web_search 来源引用上标
  -->

  <section id="intro">
    <h2 class="section-title">1. 引言</h2>
    <p>[背景、研究意义、实验目的。含引用上标 <sup><a href="#ref-1">[1]</a></sup>]</p>
  </section>

  <section id="theory">
    <h2 class="section-title">2. 实验原理</h2>
    <p>[理论基础]</p>
    <!-- 公式块 -->
    <div class="formula">η = (m_实 / m_理) × 100%</div>
    <!-- 或 MathJax 行内公式：$\eta = \frac{m_实}{m_理} \times 100\%$ -->
  </section>

  <section id="methods">
    <h2 class="section-title">3. 实验装置与方法</h2>
    <h3>3.1 实验装置</h3>
    <p>[仪器和试剂列表]</p>
    <h3>3.2 实验步骤</h3>
    <p>[步骤描述]</p>
    <!-- SVG 流程图（若有，直接内嵌） -->
    <figure>
      <svg viewBox="0 0 600 300" xmlns="http://www.w3.org/2000/svg">
        <!-- 参照 svg-flowchart-template.md 绘制 -->
      </svg>
      <figcaption>图 1. 实验流程图</figcaption>
    </figure>
  </section>

  <section id="results">
    <h2 class="section-title">4. 实验结果</h2>

    <!-- 数据表格 -->
    <div class="table-wrap">
      <table>
        <thead><tr><th>参数</th><th>数值</th><th>单位</th></tr></thead>
        <tbody>
          <tr><td>[参数名]</td><td>[值]</td><td>[单位]</td></tr>
        </tbody>
      </table>
    </div>

    <!-- Chart.js 图表（canvas id 须与 charts-init.js 中保持一致） -->
    <figure>
      <div class="chart-container">
        <canvas id="chart1"></canvas>
      </div>
      <figcaption>图 2. [描述性图题，说明核心发现，如"处理组效率比对照组高23%"]</figcaption>
    </figure>
  </section>

  <section id="analysis">
    <h2 class="section-title">5. 数据处理与分析</h2>
    <h3>5.1 计算过程</h3>
    <p>[推导步骤，含中间值]</p>
    <h3>5.2 误差分析</h3>
    <p>[误差来源与量化分析。验证详情见右下角验证面板，正文不重复。]</p>
  </section>

  <section id="discussion">
    <h2 class="section-title">6. 讨论</h2>
    <p>[结果解读、与预期/文献对比、改进建议]</p>
    <!-- 若验证发现偏差 > 5%，在此补充偏差分析段落 -->
  </section>

  <section id="conclusion">
    <h2 class="section-title">7. 结论</h2>
    <p>[简洁总结主要发现和意义，与实验目的对应]</p>
  </section>

  <!-- ⑥ 参考文献（GB/T 7714-2015，详见 gbt7714-reference-guide.md） -->
  <section id="references" class="references">
    <h2>参考文献</h2>
    <ol>
      <li id="ref-1">张三, 李四. 某化学反应动力学研究[J]. 化学学报, 2020, 78(5): 412–419.
        <a href="https://doi.org/10.xxxx/xxxxx" target="_blank">https://doi.org/10.xxxx/xxxxx</a></li>
      <li id="ref-2">Smith A, Jones B. Kinetics of reaction X[J]. <em>J. Chem. Phys.</em>, 2019, 150(3): 034501.
        <a href="https://doi.org/10.xxxx/xxxxx" target="_blank">https://doi.org/10.xxxx/xxxxx</a></li>
    </ol>
  </section>

  <!-- ⑦ 页脚 -->
  <footer class="footer">
    <span>[课程/机构名称] — 实验报告</span>
    <span>生成日期：[日期]</span>
  </footer>

</main>

<!-- ⑧ 宽屏悬浮目录（≥1280px 显示在正文右侧）
     条目 href 和文字必须与 ④ 内联目录保持完全一致 -->
<nav class="float-toc" id="floatToc" aria-label="文章目录">
  <p class="float-toc-label">目录</p>
  <ol>
    <li><a href="#intro">1. 引言</a></li>
    <li><a href="#theory">2. 实验原理</a></li>
    <li><a href="#methods">3. 实验装置与方法</a></li>
    <li><a href="#results">4. 实验结果</a></li>
    <li><a href="#analysis">5. 数据处理与分析</a></li>
    <li class="sub"><a href="#analysis">5.1 计算过程</a></li>
    <li class="sub"><a href="#analysis">5.2 误差分析</a></li>
    <li><a href="#discussion">6. 讨论</a></li>
    <li><a href="#conclusion">7. 结论</a></li>
    <li><a href="#references">参考文献</a></li>
  </ol>
</nav>

</div><!-- /.report-layout -->

<!-- ⑨ 移动端浮动导航（≤1024px 替代悬浮目录） -->
<div class="mobile-nav-overlay" id="mobileNavOverlay"></div>
<nav class="mobile-nav-menu" id="mobileNavMenu" aria-label="快速导航">
  <div class="mobile-nav-label">目录</div>
  <ol>
    <li><a href="#intro">1. 引言</a></li>
    <li><a href="#theory">2. 实验原理</a></li>
    <li><a href="#methods">3. 实验装置与方法</a></li>
    <li><a href="#results">4. 实验结果</a></li>
    <li><a href="#analysis">5. 数据处理与分析</a></li>
    <li class="sub"><a href="#analysis">5.1 计算过程</a></li>
    <li class="sub"><a href="#analysis">5.2 误差分析</a></li>
    <li><a href="#discussion">6. 讨论</a></li>
    <li><a href="#conclusion">7. 结论</a></li>
    <li><a href="#references">参考文献</a></li>
  </ol>
</nav>
<button class="mobile-nav-btn" id="mobileNavBtn" aria-label="打开目录" aria-expanded="false"></button>

<!-- ⑩ 验证面板（build_html.py 自动注入 verifyStatsContent / verifyCalcContent）
     复制此结构不要修改 id，脚本依赖这些 id -->
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

---

## 关键规则速查

| 元素 | 规则 |
|------|------|
| `section id` | 必须与 `.toc a[href]`、`.float-toc a[href]`、`.mobile-nav-menu a[href]` 三处完全一致 |
| `h2` 正文标题 | 必须加 `class="section-title"` |
| 数据表格 | 必须包在 `<div class="table-wrap">` 内（触摸横滚） |
| 图表 canvas | `id` 须与 `charts-init.js` 中 `getElementById` 调用一致 |
| SVG 流程图 | 直接内嵌在 `<figure>` 中，不保存为单独文件 |
| 验证面板 | 复制骨架中的 ⑩ 原样粘贴，不修改任何 `id` |
| CSS / JS | **不要**在 `report-body.html` 中写 `<style>` 或 `<script>`，统一由 `build_html.py` 注入 |

---

## 场景裁剪

| 场景 | meta-card 字段 | journal-bar 左侧 | 可省略的节 |
|------|---------------|-----------------|-----------|
| 实验课报告 | 作者、学号、指导教师、实验日期、提交日期、课程 | [课程名] Lab Report | — |
| 科研记录 | 作者、单位、项目编号、实验日期、版本 | [课题组] Research Record | — |
| 工程报告 | 编制人、审核人、项目编号、日期、密级 | [项目名] Technical Report | 「实验原理」→「设计依据」 |
| 竞赛展示 | 团队、参赛编号、赛事名称、日期 | [赛事名] Competition Report | 压缩 Methods，突出 Results |
