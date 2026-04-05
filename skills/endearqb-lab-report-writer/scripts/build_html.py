#!/usr/bin/env python3
"""
build_html.py - Lab Report HTML Assembler
==========================================
将分段生成的内容文件拼装为完整 HTML 报告。

流程：
  1. 读取正文 HTML 片段（支持单文件或多分段合并）
  2. 注入 SVG 流程图（扫描 data-svg-src 占位符，替换为 SVG 文件内容）
  3. 读取 assets/report.css  （样式，直接内嵌，不解析）
  4. 注入主题 CSS 覆盖       （--theme 参数，内置6套预置风格，可选）
  5. 读取 assets/report.js   （交互脚本，直接内嵌，不解析）
  6. 读取 charts-init.js     （图表初始化，Claude 生成，可选）
  7. 读取 verify-output.txt  （Python 验证摘要，可选）
  8. 拼装成完整 HTML 输出

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
用法 A（单文件，传统模式）：
  python build_html.py --body   report-body.html \
                       --output /mnt/user-data/outputs/report.html \
                       [--theme  dark] \
                       [--charts  charts-init.js] \
                       [--verify  verify-output.txt] \
                       [--svg-dir svgs/]

用法 B（多分段，按文件名排序自动合并）：
  python build_html.py --body-dir ./body-parts/ \
                       --output /mnt/user-data/outputs/report.html \
                       [--theme  olive] \
                       [--charts  charts-init.js] \
                       [--verify  verify-output.txt] \
                       [--svg-dir svgs/]

  body-parts/ 中的文件按文件名升序拼接，建议命名：
    body-01-header.html       封面 + 摘要 + 目录 + report-layout 开始标签
    body-02-intro.html        引言节
    body-03-theory.html       原理节
    body-04-methods.html      方法节（含 SVG 占位符）
    body-05-results.html      结果节（含 chart canvas 占位）
    body-06-analysis.html     分析节
    body-07-discussion.html   讨论节
    body-08-conclusion.html   结论节
    body-09-references.html   参考文献节
    body-10-footer.html       footer + 悬浮目录 + 移动导航 + 验证面板骨架 + 闭合标签

用法 C（多分段，手动指定顺序）：
  python build_html.py --body-parts body-01.html body-02.html body-03.html \
                       --output /mnt/user-data/outputs/report.html

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
主题参数 --theme：

可选值（省略或 default 时使用 report.css 内置默认风格，无额外开销）：
  default       暖墨纸（默认，无需此参数）
  dark          午夜藏青 Midnight Navy
  clean         净白简约 Clean White
  olive         橄榄学报 Olive Scholar
  engineering   砖红工程 Engineering Red
  graphite      石墨极简 Graphite Minimal

主题 CSS 以 <style> 块注入 <head>，优先级高于 report.css。
Claude 只需传 --theme 参数，无需读取或内联任何 CSS 内容。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SVG 注入机制：

在 HTML 片段中用占位符标记 SVG 插入位置：

  <figure data-svg-src="flowchart.svg">
    <figcaption>图 1. 实验流程图</figcaption>
  </figure>

build_html.py 会：
  1. 从 --svg-dir 目录（默认与 --body 同目录，或 --body-dir 目录）查找 flowchart.svg
  2. 读取 SVG 文件内容，去除 <?xml ...?> 声明行
  3. 将 SVG 内容注入到 <figure> 开始标签之后、<figcaption> 之前
  4. 移除 data-svg-src 属性

结果：
  <figure>
    <svg viewBox="..." ...>...</svg>
    <figcaption>图 1. 实验流程图</figcaption>
  </figure>

若 SVG 文件未找到，保留占位符并打印 [WARN]，不中断构建。
多个 SVG 文件用不同文件名区分（如 flowchart.svg、apparatus.svg）。

--assets 默认指向脚本所在目录的 ../assets/
--svg-dir 默认与正文文件同目录（单文件模式）或 --body-dir 目录（分段模式）
"""

import argparse, os, re, sys
from pathlib import Path


# ──────────────────────────────────────────────────────────────────────────────
# 内置主题 CSS（对应 references/style-constitution.md 预置风格库）
# Claude 只需传 --theme 参数，无需读取或内联任何 CSS。
# ──────────────────────────────────────────────────────────────────────────────
THEMES = {
    'default': '',   # 使用 report.css 内置默认暖墨纸，无额外 CSS

    'dark': """\
/* ===== 主题：午夜藏青 Midnight Navy ===== */
:root {
  --paper:     #0d1117;
  --page:      #161b22;
  --ink:       #e6edf3;
  --muted:     #7d8590;
  --line:      #30363d;
  --soft:      #1c2128;
  --soft-alt:  #1a2332;
  --soft-blue: #172033;
  --accent:    #c9a84c;
  --shadow:    0 18px 48px rgba(0,0,0,0.40);
}
body {
  background:
    radial-gradient(circle at top left, rgba(201,168,76,0.06), transparent 30%),
    linear-gradient(180deg, #090d13 0%, var(--paper) 100%);
  font-family: "Source Serif 4", Georgia, "Noto Serif SC", serif;
  line-height: 1.80;
}
/* 表格 */
th { background: #21262d; color: #e6edf3; }
td { border-bottom-color: #30363d; }
tbody tr:nth-child(even) td { background: #1c2128; }
/* 摘要、目录、引用块 */
.abstract { background: #1a2332; border-left-color: var(--accent); }
.toc { background: var(--soft); border-color: var(--line); }
blockquote { background: #1a2332; border-left-color: var(--accent); color: var(--muted); }
/* 公式、验证框 */
.formula { background: var(--soft-blue); border-color: #2d3748; }
.verification { background: #162118; border-color: #2d5a27; border-left-color: #3fb950; }
/* 提示框、图表容器 */
.callout { background: linear-gradient(180deg,#1a2a1a 0%,#162820 100%); border-left-color: #3f6b3a; }
.chart-container { background: #1c2128; border-color: var(--line); }
/* 元数据卡片 */
.meta-card { background: linear-gradient(180deg,#1c2128 0%,#161b22 100%); border-color: var(--line); }
/* 验证面板 */
.verify-panel-header { background: var(--soft); }
.verify-panel-header:hover { background: var(--soft-alt); }
.verify-section-label { background: var(--soft); }
/* 链接 */
a { color: var(--accent); }""",

    'clean': """\
/* ===== 主题：净白简约 Clean White ===== */
:root {
  --paper:     #f8f9fa;
  --page:      #ffffff;
  --ink:       #212529;
  --muted:     #6c757d;
  --line:      #dee2e6;
  --soft:      #f1f3f5;
  --soft-alt:  #e8f4fd;
  --soft-blue: #ebf5fb;
  --accent:    #1a6eb5;
  --shadow:    0 8px 32px rgba(0,0,0,0.08);
}
body {
  background: var(--paper);
  font-family: "Lora", Georgia, "Noto Serif SC", serif;
  line-height: 1.78;
}
.page { border: none; border-top: 3px solid var(--accent); }
/* 表格 */
th { background: #1a6eb5; color: #ffffff; }
td { border-bottom-color: #dee2e6; }
tbody tr:nth-child(even) td { background: #f8f9fa; }
/* 摘要、目录、引用块 */
.abstract { background: #f0f7ff; border-left-color: #1a6eb5; }
.toc { background: #f8f9fa; border-color: var(--line); }
blockquote { background: #ebf5fb; border-left-color: #1a6eb5; color: var(--muted); }
/* 公式、验证框 */
.formula { background: #ebf5fb; border-color: #b8d8f0; }
.verification { background: #f0fff4; border-color: #c3e6cb; border-left-color: #28a745; }
/* 提示框、图表、元数据卡片 */
.callout { background: linear-gradient(180deg,#e8f4fd 0%,#f0f7ff 100%); border-left-color: #1a6eb5; }
.chart-container { background: #f8f9fa; border-color: var(--line); }
.meta-card { background: linear-gradient(180deg,#f1f3f5 0%,#e9ecef 100%); border-color: var(--line); }
/* 验证面板 */
.verify-panel-header { background: var(--soft); }
.verify-panel-header:hover { background: var(--soft-alt); }
.verify-section-label { background: var(--soft); }
/* 链接 */
a { color: #1a6eb5; }""",

    'olive': """\
/* ===== 主题：橄榄学报 Olive Scholar ===== */
:root {
  --paper:     #f7f5ef;
  --page:      #fefdfb;
  --ink:       #2c2a1e;
  --muted:     #6b6550;
  --line:      #ccc9b4;
  --soft:      #eeeade;
  --soft-alt:  #edf0e5;
  --soft-blue: #edf2e8;
  --accent:    #4a6741;
  --shadow:    0 16px 44px rgba(44,42,30,0.11);
}
body {
  background:
    radial-gradient(circle at top left, rgba(74,103,65,0.07), transparent 30%),
    linear-gradient(180deg, #efede4 0%, var(--paper) 100%);
  font-family: Georgia, "Noto Serif SC", serif;
  line-height: 1.84;
}
/* 表格 */
th { background: #3d5735; color: #f5f3ec; }
td { border-bottom-color: #ddd8c4; }
tbody tr:nth-child(even) td { background: #f3f1e8; }
/* 摘要、目录、引用块 */
.abstract { background: #edf0e5; border-left-color: #4a6741; }
.toc { background: #f4f2ea; border-color: var(--line); }
blockquote { background: #edf0e5; border-left-color: #4a6741; color: var(--muted); }
/* 公式、验证框 */
.formula { background: #edf2e8; border-color: #c4cebc; }
.verification { background: #f0f5ee; border-color: #b8ccb4; border-left-color: #4a6741; }
/* 提示框、图表、元数据卡片 */
.callout { background: linear-gradient(180deg,#edf0e5 0%,#f4f6ef 100%); border-left-color: #4a6741; }
.chart-container { background: #f7f5ef; border-color: var(--line); }
.meta-card { background: linear-gradient(180deg,#eeead8 0%,#e8e4d0 100%); border-color: var(--line); }
/* 验证面板 */
.verify-panel-header { background: var(--soft); }
.verify-panel-header:hover { background: var(--soft-alt); }
.verify-section-label { background: var(--soft); }
/* 链接 */
a { color: #4a6741; }""",

    'engineering': """\
/* ===== 主题：砖红工程 Engineering Red ===== */
:root {
  --paper:     #f9f7f5;
  --page:      #ffffff;
  --ink:       #1c1c1e;
  --muted:     #636366;
  --line:      #d1cbc3;
  --soft:      #f4eeea;
  --soft-alt:  #fdf1ee;
  --soft-blue: #f5f5f7;
  --accent:    #9b2335;
  --shadow:    0 12px 40px rgba(28,28,30,0.10);
}
body {
  background:
    radial-gradient(circle at top left, rgba(155,35,53,0.05), transparent 30%),
    linear-gradient(180deg, #f2efec 0%, var(--paper) 100%);
  font-family: Georgia, "Noto Serif SC", serif;
  line-height: 1.80;
}
/* 表格 */
th { background: #7a1a28; color: #fff8f8; }
td { border-bottom-color: #d1cbc3; }
tbody tr:nth-child(even) td { background: #faf8f6; }
/* 摘要、目录、引用块 */
.abstract { background: #fdf1ee; border-left-color: #9b2335; }
.toc { background: #faf7f5; border-color: var(--line); }
blockquote { background: #fdf1ee; border-left-color: #9b2335; color: var(--muted); }
/* 公式、验证框 */
.formula { background: #f5f5f7; border-color: #d1cbc3; }
.verification { background: #f0fff4; border-color: #c3e6cb; border-left-color: #28a745; }
/* 提示框、图表、元数据卡片 */
.callout { background: linear-gradient(180deg,#fdf1ee 0%,#fdf8f7 100%); border-left-color: #9b2335; }
.chart-container { background: #faf8f6; border-color: var(--line); }
.meta-card { background: linear-gradient(180deg,#f4eeea 0%,#eee8e4 100%); border-color: var(--line); }
/* 验证面板 */
.verify-panel-header { background: var(--soft); }
.verify-panel-header:hover { background: var(--soft-alt); }
.verify-section-label { background: var(--soft); }
/* 链接 */
a { color: #9b2335; }""",

    'graphite': """\
/* ===== 主题：石墨极简 Graphite Minimal ===== */
:root {
  --paper:     #f5f5f5;
  --page:      #ffffff;
  --ink:       #1a1a1a;
  --muted:     #666666;
  --line:      #cccccc;
  --soft:      #ebebeb;
  --soft-alt:  #f0f0f0;
  --soft-blue: #f0f0f4;
  --accent:    #333333;
  --shadow:    0 8px 28px rgba(0,0,0,0.08);
}
body {
  background: var(--paper);
  font-family: Georgia, "Noto Serif SC", serif;
  line-height: 1.80;
}
.page { border: 1px solid var(--line); }
/* 表格 */
th { background: #2a2a2a; color: #f5f5f5; }
td { border-bottom-color: #cccccc; }
tbody tr:nth-child(even) td { background: #f5f5f5; }
/* 摘要、目录、引用块 */
.abstract { background: #f0f0f0; border-left-color: #1a1a1a; }
.toc { background: #f5f5f5; border-color: #cccccc; }
blockquote { background: #f0f0f0; border-left-color: #666; color: var(--muted); }
/* 公式、验证框 */
.formula { background: #f0f0f4; border-color: #cccccc; }
.verification { background: #f8f8f8; border-color: #cccccc; border-left-color: #555555; }
/* 提示框、图表、元数据卡片 */
.callout { background: #f0f0f0; border-left-color: #666; }
.chart-container { background: #f8f8f8; border-color: #cccccc; }
.meta-card { background: linear-gradient(180deg,#ebebeb 0%,#e5e5e5 100%); border-color: #cccccc; }
/* 验证面板 */
.verify-panel-header { background: var(--soft); }
.verify-panel-header:hover { background: var(--soft-alt); }
.verify-section-label { background: var(--soft); }
/* 链接 */
a { color: #333333; text-decoration: underline; }""",
}

THEME_ALIASES = {
    '暖墨纸': 'default', '默认': 'default',
    '午夜藏青': 'dark',  '极夜深色': 'dark',   'midnight': 'dark',
    '净白简约': 'clean', 'white': 'clean',
    '橄榄学报': 'olive',
    '砖红工程': 'engineering', 'red': 'engineering',
    '石墨极简': 'graphite', '石墨': 'graphite',
}


def parse_args():
    p = argparse.ArgumentParser(description='Assemble lab report HTML')
    grp = p.add_mutually_exclusive_group(required=True)
    grp.add_argument('--body',       help='单个正文 HTML 片段文件（传统模式）')
    grp.add_argument('--body-dir',   help='目录，按文件名升序合并其中所有 *.html')
    grp.add_argument('--body-parts', nargs='+', metavar='FILE',
                     help='手动指定多个正文 HTML 片段，按参数顺序合并')
    p.add_argument('--output',  default='report.html', help='输出文件路径')
    p.add_argument('--theme',   default='default',
                   help='色彩主题：default/dark/clean/olive/engineering/graphite（默认 default）')
    p.add_argument('--charts',  default=None, help='Chart.js 初始化脚本（可选）')
    p.add_argument('--verify',  default=None, help='Python 验证摘要文本（可选）')
    p.add_argument('--title',   default=None, help='报告标题（页面 <title> 用）')
    p.add_argument('--assets',  default=None, help='assets/ 目录路径，默认自动推断')
    p.add_argument('--svg-dir', default=None,
                   help='SVG 文件所在目录，默认与正文文件同目录')
    return p.parse_args()


def find_assets_dir(hint=None):
    if hint and Path(hint).is_dir():
        return Path(hint)
    candidate = Path(__file__).parent.parent / 'assets'
    if candidate.is_dir():
        return candidate
    raise FileNotFoundError(
        f'assets/ not found at {candidate}. '
        'Run this script from inside the lab-report-writer skill directory.'
    )


def read_file(path, label='file'):
    p = Path(path)
    if not p.exists():
        print(f'[WARN] {label} not found: {p}', file=sys.stderr)
        return ''
    return p.read_text(encoding='utf-8')


def load_body(args):
    """Load and concatenate body HTML; return (html_text, default_svg_dir)."""
    if args.body:
        return read_file(args.body, '正文 HTML'), Path(args.body).parent

    if args.body_dir:
        d = Path(args.body_dir)
        if not d.is_dir():
            print(f'[ERROR] --body-dir does not exist: {d}', file=sys.stderr)
            sys.exit(1)
        parts = sorted(d.glob('*.html'))
        if not parts:
            print(f'[WARN] No *.html files found in {d}', file=sys.stderr)
            return '', d
        print(f'[build_html] Merging {len(parts)} segment(s) from {d}:')
        chunks = []
        for f in parts:
            print(f'  + {f.name}')
            chunks.append(f.read_text(encoding='utf-8'))
        return '\n'.join(chunks), d

    if args.body_parts:
        chunks = []
        for fp in args.body_parts:
            print(f'  + {Path(fp).name}')
            chunks.append(read_file(fp, fp))
        return '\n'.join(chunks), Path(args.body_parts[0]).parent

    return '', Path('.')


def strip_xml_declaration(svg_text):
    """Remove <?xml ...?> processing instruction if present."""
    return re.sub(r'<\?xml[^?]*\?>\s*', '', svg_text, flags=re.IGNORECASE).strip()


def inject_svgs(body_html, svg_dir):
    """
    Replace <figure data-svg-src="NAME.svg"> placeholders with actual SVG content.

    Pattern matched:
      <figure data-svg-src="NAME.svg" ...>
        ...optional whitespace / figcaption...
      </figure>

    The SVG is injected immediately after the opening <figure> tag.
    data-svg-src attribute is removed from the figure tag.
    """
    def replacer(m):
        full_tag   = m.group(0)
        svg_name   = m.group(1)
        inner      = m.group(2)   # content between <figure ...> and </figure>

        svg_path = svg_dir / svg_name
        if not svg_path.exists():
            print(f'[WARN] SVG file not found, placeholder kept: {svg_path}',
                  file=sys.stderr)
            return full_tag   # keep original, don't break the build

        svg_text = strip_xml_declaration(svg_path.read_text(encoding='utf-8'))
        print(f'[build_html] Injecting SVG: {svg_name} ({len(svg_text)} chars)')

        # Remove data-svg-src from the figure opening tag
        clean_open = re.sub(r'\s*data-svg-src="[^"]*"', '', m.group(3))
        return f'{clean_open}\n{svg_text}\n{inner}</figure>'

    # Match <figure ... data-svg-src="..."> ... </figure>
    # Group 1: svg filename, Group 2: inner content, Group 3: opening tag
    pattern = re.compile(
        r'(<figure[^>]*\s+data-svg-src="([^"]+)"[^>]*>)(.*?)</figure>',
        re.DOTALL
    )

    def _replacer(m):
        opening_tag = m.group(1)
        svg_name    = m.group(2)
        inner       = m.group(3)

        svg_path = svg_dir / svg_name
        if not svg_path.exists():
            print(f'[WARN] SVG not found, placeholder kept: {svg_path}',
                  file=sys.stderr)
            return m.group(0)

        svg_text = strip_xml_declaration(svg_path.read_text(encoding='utf-8'))
        print(f'[build_html] Injecting SVG: {svg_name} ({len(svg_text)} chars)')

        clean_tag = re.sub(r'\s*data-svg-src="[^"]*"', '', opening_tag)
        return f'{clean_tag}\n{svg_text}\n{inner}</figure>'

    return pattern.sub(_replacer, body_html)


def escape(text):
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def slot_verify(body_html, verify_text):
    """Fill verifyStatsContent / verifyCalcContent placeholders in body_html."""
    if not verify_text.strip():
        return body_html

    stats_text = calc_text = ''
    parts = re.split(r'【计算验证】', verify_text, maxsplit=1)
    stats_text = re.sub(r'【统计摘要】\s*', '', parts[0]).strip()
    if len(parts) > 1:
        calc_text = re.split(r'【偏差汇总】', parts[1], maxsplit=1)[0].strip()

    def replace_pre(html, element_id, content):
        return re.sub(
            r'(<pre[^>]*id="' + element_id + r'"[^>]*>)[^<]*(</pre>)',
            lambda m: m.group(1) + '\n' + escape(content) + '\n' + m.group(2),
            html
        )

    if stats_text:
        body_html = replace_pre(body_html, 'verifyStatsContent', stats_text)
    if calc_text:
        body_html = replace_pre(body_html, 'verifyCalcContent', calc_text)
    return body_html


def get_theme_css(theme_key):
    """Resolve theme key/alias to CSS string. Returns '' for default/unknown."""
    key = THEME_ALIASES.get(theme_key, theme_key).lower()
    if key not in THEMES:
        print(f'[WARN] Unknown theme "{theme_key}", falling back to default.', file=sys.stderr)
        return ''
    css = THEMES[key]
    if css:
        print(f'[build_html] Theme: {theme_key} ({key})')
    return css


def assemble(body_html, css, theme_css, js, charts_js, verify_text, title):
    body_html = slot_verify(body_html, verify_text)

    if not title:
        m = re.search(r'<h1[^>]*>(.*?)</h1>', body_html)
        title = re.sub(r'<[^>]+>', '', m.group(1)).strip() if m else '实验报告'

    charts_block = f'<script>\n{charts_js}\n</script>' if charts_js.strip() else ''
    theme_block  = f'<style>\n{theme_css}\n</style>' if theme_css.strip() else ''

    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=1.0, viewport-fit=cover">
<meta name="theme-color" content="#2f4f4f">
<title>{escape(title)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600;700&display=swap" rel="stylesheet">
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
<script>window.MathJax = {{tex:{{inlineMath:[['$','$'],['\\\\(','\\\\)']]}},svg:{{fontCache:'global'}}}};</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js" async></script>
<style>
{css}
</style>
{theme_block}
</head>
<body>

{body_html}

{charts_block}
<script>
{js}
</script>
</body>
</html>'''


def main():
    args = parse_args()

    body_html, default_svg_dir = load_body(args)

    # Determine SVG directory
    svg_dir = Path(args.svg_dir) if args.svg_dir else default_svg_dir
    if not svg_dir.is_dir():
        print(f'[WARN] --svg-dir does not exist: {svg_dir}', file=sys.stderr)
        svg_dir = Path('.')

    # Inject SVGs before assembling
    body_html = inject_svgs(body_html, svg_dir)

    assets_dir  = find_assets_dir(args.assets)
    css         = read_file(assets_dir / 'report.css', 'report.css')
    js          = read_file(assets_dir / 'report.js',  'report.js')
    theme_css   = get_theme_css(args.theme)
    charts_js   = read_file(args.charts,  '图表脚本') if args.charts else ''
    verify_text = read_file(args.verify,  '验证摘要') if args.verify else ''

    print(f'[build_html] assets={assets_dir}, svg_dir={svg_dir}')
    html = assemble(body_html, css, theme_css, js, charts_js, verify_text, args.title)

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding='utf-8')
    print(f'[build_html] ✓ {out}  ({out.stat().st_size/1024:.1f} KB)')


if __name__ == '__main__':
    main()
