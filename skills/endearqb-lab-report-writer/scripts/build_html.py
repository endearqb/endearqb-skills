#!/usr/bin/env python3
"""
build_html.py - Lab Report HTML Assembler
==========================================
将分段生成的内容文件拼装为完整 HTML 报告。

流程：
  1. 读取正文 HTML 片段（支持单文件或多分段合并）
  2. 注入 SVG 流程图（扫描 data-svg-src 占位符，替换为 SVG 文件内容）
  3. 读取 assets/report.css  （样式，直接内嵌，不解析）
  4. 读取 assets/report.js   （交互脚本，直接内嵌，不解析）
  5. 读取 charts-init.js     （图表初始化，Claude 生成，可选）
  6. 读取 verify-output.txt  （Python 验证摘要，可选）
  7. 拼装成完整 HTML 输出

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
用法 A（单文件，传统模式）：
  python build_html.py --body   report-body.html \
                       --output /mnt/user-data/outputs/report.html \
                       [--charts  charts-init.js] \
                       [--verify  verify-output.txt] \
                       [--svg-dir svgs/]

用法 B（多分段，按文件名排序自动合并）：
  python build_html.py --body-dir ./body-parts/ \
                       --output /mnt/user-data/outputs/report.html \
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


def parse_args():
    p = argparse.ArgumentParser(description='Assemble lab report HTML')
    grp = p.add_mutually_exclusive_group(required=True)
    grp.add_argument('--body',       help='单个正文 HTML 片段文件（传统模式）')
    grp.add_argument('--body-dir',   help='目录，按文件名升序合并其中所有 *.html')
    grp.add_argument('--body-parts', nargs='+', metavar='FILE',
                     help='手动指定多个正文 HTML 片段，按参数顺序合并')
    p.add_argument('--output',  default='report.html', help='输出文件路径')
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


def assemble(body_html, css, js, charts_js, verify_text, title):
    body_html = slot_verify(body_html, verify_text)

    if not title:
        m = re.search(r'<h1[^>]*>(.*?)</h1>', body_html)
        title = re.sub(r'<[^>]+>', '', m.group(1)).strip() if m else '实验报告'

    charts_block = f'<script>\n{charts_js}\n</script>' if charts_js.strip() else ''

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
    charts_js   = read_file(args.charts,  '图表脚本') if args.charts else ''
    verify_text = read_file(args.verify,  '验证摘要') if args.verify else ''

    print(f'[build_html] assets={assets_dir}, svg_dir={svg_dir}')
    html = assemble(body_html, css, js, charts_js, verify_text, args.title)

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding='utf-8')
    print(f'[build_html] ✓ {out}  ({out.stat().st_size/1024:.1f} KB)')


if __name__ == '__main__':
    main()
