#!/usr/bin/env python3
"""
build_html.py — Lab Report HTML Assembler
==========================================
将分段生成的内容文件拼装为完整 HTML 报告。

流程：
  1. 读取 report-body.html  （Claude 生成的报告正文片段）
  2. 读取 assets/report.css  （样式，直接内嵌，不解析）
  3. 读取 assets/report.js   （交互脚本，直接内嵌，不解析）
  4. 读取 charts-init.js     （图表初始化，Claude 生成，可选）
  5. 读取 verify-output.txt  （Python 验证摘要，可选）
  6. 拼装成完整 HTML 输出

用法：
  python build_html.py --body   report-body.html \
                       --output /mnt/user-data/outputs/report.html \
                       [--charts  charts-init.js] \
                       [--verify  verify-output.txt] \
                       [--title   "报告标题"]

--assets 默认指向脚本所在目录的 ../assets/
"""

import argparse, os, re, sys
from pathlib import Path
from datetime import datetime


def parse_args():
    p = argparse.ArgumentParser(description='Assemble lab report HTML')
    p.add_argument('--body',   required=True, help='报告正文 HTML 片段（Claude 生成）')
    p.add_argument('--output', default='report.html', help='输出文件路径')
    p.add_argument('--charts', default=None, help='Chart.js 初始化脚本（可选）')
    p.add_argument('--verify', default=None, help='Python 验证摘要文本（可选）')
    p.add_argument('--title',  default=None, help='报告标题（页面 <title> 用）')
    p.add_argument('--assets', default=None, help='assets/ 目录路径，默认自动推断')
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


def escape(text):
    return text.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')


def slot_verify(body_html, verify_text):
    """Fill verifyStatsContent / verifyCalcContent placeholders in body_html."""
    if not verify_text.strip():
        return body_html

    # Split verify-output.txt by section markers from auto_verify.py
    stats_text = calc_text = ''
    parts = re.split(r'【计算验证】', verify_text, maxsplit=1)
    stats_text = re.sub(r'【统计摘要】\s*', '', parts[0]).strip()
    if len(parts) > 1:
        calc_text = re.split(r'【偏差汇总】', parts[1], maxsplit=1)[0].strip()

    def replace_pre(content, element_id):
        return re.sub(
            r'(<pre[^>]*id="' + element_id + r'"[^>]*>)[^<]*(</pre>)',
            lambda m: m.group(1) + '\n' + escape(content) + '\n' + m.group(2),
            body_html
        )

    if stats_text:
        body_html = replace_pre(stats_text, 'verifyStatsContent')
    if calc_text:
        body_html = replace_pre(calc_text, 'verifyCalcContent')
    return body_html


def assemble(body_html, css, js, charts_js, verify_text, title):
    body_html = slot_verify(body_html, verify_text)

    # Extract title from first h1 if not given
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

    body_html   = read_file(args.body,   '正文 HTML')
    assets_dir  = find_assets_dir(args.assets)
    css         = read_file(assets_dir / 'report.css', 'report.css')
    js          = read_file(assets_dir / 'report.js',  'report.js')
    charts_js   = read_file(args.charts,  '图表脚本') if args.charts else ''
    verify_text = read_file(args.verify,  '验证摘要') if args.verify else ''

    print(f'[build_html] body={args.body}, assets={assets_dir}')
    html = assemble(body_html, css, js, charts_js, verify_text, args.title)

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding='utf-8')
    print(f'[build_html] ✓ {out}  ({out.stat().st_size/1024:.1f} KB)')


if __name__ == '__main__':
    main()
