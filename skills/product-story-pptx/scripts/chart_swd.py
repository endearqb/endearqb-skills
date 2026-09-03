#!/usr/bin/env python3
"""chart_swd.py — Storytelling with Data 风格图表 → PNG。

被 build_deck.py 调用:
    from chart_swd import render_chart, build_palette
    render_chart(chart, palette, "out.png", width_in=11.7, height_in=4.6, fonts=fonts, cfg=tokens["chart"])

独立调试:
    python scripts/chart_swd.py chart.yaml out.png [--theme ink]
    # chart.yaml 可以是一个 chart 块，也可以是含 chart 键的整页 slide

支持 kind: bar | hbar | line | slope | dot
不支持: pie / donut / 3D / 双轴 —— 这不是缺功能，是规则。

原则 → 实现:
    消除杂乱     无网格；只留基线；不画图例框；不描边
    聚焦注意力   highlight 用强调色，其余一律 neutral 灰；高亮类别的刻度文字同色加粗
    直接标注     数值写在柱/点旁边，line/slope 在线端写系列名 + 数值
    诚实的轴     柱状图必从 0 起；line 的 y 轴保留少量刻度
    来源         source 写在左下角；is_example 时右上角有「示例数据」角标
"""
from __future__ import annotations

import argparse
import math
import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib import font_manager  # noqa: E402
from matplotlib.ticker import MaxNLocator  # noqa: E402

SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEFAULT_CFG = {
    "dpi": 220, "font_size": 11, "label_size": 11, "annotation_size": 11, "source_size": 8.5,
    "bar_width": 0.62, "line_width": 2.4, "line_width_muted": 1.6, "marker_size": 6,
    "example_badge": "示例数据",
}


# ---------------------------------------------------------------------------
# palette / fonts
# ---------------------------------------------------------------------------
def build_palette(theme: dict, cfg: dict | None = None) -> dict:
    """从 design-tokens 的一套 theme 生成图表调色。"""
    cfg = {**DEFAULT_CFG, **(cfg or {})}
    return {
        "bg": theme["background"],
        "text": theme["text"],
        "muted": theme["text_muted"],
        "neutral": theme[cfg.get("neutral_key", "neutral_data")],
        "highlight": theme[cfg.get("highlight_key", "accent")],
        "highlight2": theme[cfg.get("highlight2_key", "accent_soft")],
        "baseline": theme[cfg.get("baseline_key", "rule")],
    }


def setup_fonts(fonts: dict | None) -> None:
    """为 Matplotlib 选择真正覆盖中日韩字形的首选字体。"""
    fonts = fonts or {}
    installed = {f.name for f in font_manager.fontManager.ttflist}
    cjk_candidates = [
        fonts.get("font_cjk"), fonts.get("fallback_cjk"),
        "Noto Sans CJK SC", "Noto Sans CJK JP", "Noto Sans CJK TC", "Noto Sans CJK KR",
        "Source Han Sans SC", "Source Han Sans CN", "PingFang SC", "Hiragino Sans GB",
        "WenQuanYi Micro Hei",
    ]
    latin_candidates = [fonts.get("font_latin"), fonts.get("fallback_latin"), "Inter", "Arial", "DejaVu Sans"]
    chain = []
    for name in cjk_candidates + latin_candidates:
        if name and name in installed and name not in chain:
            chain.append(name)
    if not chain:
        chain = ["DejaVu Sans"]
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = chain
    plt.rcParams["axes.unicode_minus"] = False


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
def fmt(v, unit: str = "") -> str:
    if v is None:
        return ""
    if isinstance(v, (int,)) or (isinstance(v, float) and float(v).is_integer()):
        s = f"{int(v):,}"
    else:
        s = f"{v:,.1f}"
    unit = unit or ""
    return f"{s}{unit}" if unit in ("%", "x", "×") or not unit else f"{s} {unit}"


def _numeric_values(values):
    vals = [v for v in values if isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v)]
    if not vals:
        raise ValueError("图表序列没有可绘制的数值")
    return vals


def _despine(ax, keep=("bottom",), color="#CCCCCC"):
    for side in ("top", "right", "left", "bottom"):
        sp = ax.spines[side]
        if side in keep:
            sp.set_color(color)
            sp.set_linewidth(1.0)
        else:
            sp.set_visible(False)


def _color_for(name, highlight: list, p: dict) -> str:
    if highlight and name == highlight[0]:
        return p["highlight"]
    if len(highlight) > 1 and name == highlight[1]:
        return p["highlight2"]
    return p["neutral"]


def _style_ticklabels(labels, highlight: list, p: dict) -> None:
    for lab in labels:
        txt = lab.get_text()
        if txt in highlight:
            lab.set_color(p["highlight"] if txt == highlight[0] else p["highlight2"])
            lab.set_fontweight("bold")
        else:
            lab.set_color(p["muted"])


# ---------------------------------------------------------------------------
# kinds
# ---------------------------------------------------------------------------
def _bar(ax, chart, p, cfg):
    cats = chart["data"]["categories"]
    vals = chart["data"]["series"][0]["values"]
    hl = chart.get("highlight") or []
    unit = chart.get("unit", "")
    colors = [_color_for(c, hl, p) for c in cats]
    x = range(len(cats))
    ax.bar(x, vals, width=cfg["bar_width"], color=colors, edgecolor="none", zorder=3)
    vmax = max(_numeric_values(vals)) or 1
    for xi, v in zip(x, vals):
        if v is None:
            continue
        ax.text(xi, v + vmax * 0.02, fmt(v, unit), ha="center", va="bottom",
                fontsize=cfg["label_size"], color=p["text"] if cats[xi] in hl else p["muted"],
                fontweight="bold" if cats[xi] in hl else "normal")
    ax.set_xticks(list(x))
    ax.set_xticklabels(cats, fontsize=cfg["font_size"])
    ax.set_ylim(0, vmax * 1.18)
    ax.yaxis.set_visible(False)
    ax.tick_params(axis="x", length=0, pad=8)
    _despine(ax, keep=("bottom",), color=p["baseline"])
    _style_ticklabels(ax.get_xticklabels(), hl, p)


def _hbar(ax, chart, p, cfg):
    cats = chart["data"]["categories"]
    vals = chart["data"]["series"][0]["values"]
    hl = chart.get("highlight") or []
    unit = chart.get("unit", "")
    colors = [_color_for(c, hl, p) for c in cats]
    y = list(range(len(cats)))
    ax.barh(y, vals, height=cfg["bar_width"], color=colors, edgecolor="none", zorder=3)
    ax.invert_yaxis()  # 第一个类别在最上
    vmax = max(_numeric_values(vals)) or 1
    for yi, v in zip(y, vals):
        if v is None:
            continue
        ax.text(v + vmax * 0.015, yi, fmt(v, unit), ha="left", va="center",
                fontsize=cfg["label_size"], color=p["text"] if cats[yi] in hl else p["muted"],
                fontweight="bold" if cats[yi] in hl else "normal")
    ax.set_yticks(y)
    ax.set_yticklabels(cats, fontsize=cfg["font_size"])
    ax.set_xlim(0, vmax * 1.22)
    ax.xaxis.set_visible(False)
    ax.tick_params(axis="y", length=0, pad=10)
    _despine(ax, keep=("left",), color=p["baseline"])
    _style_ticklabels(ax.get_yticklabels(), hl, p)


def _line(ax, chart, p, cfg):
    cats = chart["data"]["categories"]
    series = chart["data"]["series"]
    hl = chart.get("highlight") or []
    unit = chart.get("unit", "")
    x = list(range(len(cats)))
    # 先画灰的，再画高亮的，保证高亮在上层
    ordered = sorted(series, key=lambda s: 1 if s["name"] in hl else 0)
    for s in ordered:
        is_hl = s["name"] in hl
        color = _color_for(s["name"], hl, p)
        lw = cfg["line_width"] if is_hl else cfg["line_width_muted"]
        ax.plot(x, s["values"], color=color, linewidth=lw, zorder=4 if is_hl else 3,
                solid_capstyle="round")
        valid_indices = [i for i, v in enumerate(s["values"]) if isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v)]
        if not valid_indices:
            continue
        last_i = valid_indices[-1]
        last_v = s["values"][last_i]
        if is_hl:
            ax.plot([last_i], [last_v], "o", color=color, markersize=cfg["marker_size"], zorder=5)
        ax.text(last_i + 0.15, last_v, f"{s['name']}  {fmt(last_v, unit)}", ha="left", va="center",
                fontsize=cfg["label_size"], color=color if is_hl else p["muted"],
                fontweight="bold" if is_hl else "normal")
    ax.set_xticks(x)
    ax.set_xticklabels(cats, fontsize=cfg["font_size"], color=p["muted"])
    ax.set_xlim(-0.2, len(cats) - 1 + 2.2)  # 右侧给标签留空
    ax.yaxis.set_major_locator(MaxNLocator(4))
    ax.tick_params(axis="y", labelsize=cfg["font_size"] - 1, colors=p["muted"], length=0)
    ax.tick_params(axis="x", length=0, pad=8)
    _despine(ax, keep=("bottom",), color=p["baseline"])
    ax.yaxis.grid(False)


def _slope(ax, chart, p, cfg):
    cats = chart["data"]["categories"]
    series = chart["data"]["series"]
    hl = chart.get("highlight") or []
    unit = chart.get("unit", "")
    ordered = sorted(series, key=lambda s: 1 if s["name"] in hl else 0)
    for s in ordered:
        a, b = s["values"][0], s["values"][1]
        is_hl = s["name"] in hl
        color = _color_for(s["name"], hl, p)
        lw = cfg["line_width"] if is_hl else cfg["line_width_muted"]
        ax.plot([0, 1], [a, b], color=color, linewidth=lw, marker="o",
                markersize=cfg["marker_size"] if is_hl else cfg["marker_size"] - 2, zorder=4 if is_hl else 3)
        ax.text(-0.04, a, f"{s['name']}  {fmt(a, unit)}", ha="right", va="center",
                fontsize=cfg["label_size"], color=color if is_hl else p["muted"],
                fontweight="bold" if is_hl else "normal")
        ax.text(1.04, b, fmt(b, unit), ha="left", va="center",
                fontsize=cfg["label_size"], color=color if is_hl else p["muted"],
                fontweight="bold" if is_hl else "normal")
    ax.set_xlim(-0.6, 1.4)
    ax.set_xticks([0, 1])
    ax.set_xticklabels(cats, fontsize=cfg["font_size"], color=p["muted"])
    ax.yaxis.set_visible(False)
    ax.tick_params(axis="x", length=0, pad=10)
    _despine(ax, keep=(), color=p["baseline"])
    for xi in (0, 1):
        ax.axvline(xi, color=p["baseline"], linewidth=1, zorder=1)


def _dot(ax, chart, p, cfg):
    cats = chart["data"]["categories"]
    vals = chart["data"]["series"][0]["values"]
    hl = chart.get("highlight") or []
    unit = chart.get("unit", "")
    y = list(range(len(cats)))
    vmax = max(_numeric_values(vals)) or 1
    for yi, (c, v) in enumerate(zip(cats, vals)):
        color = _color_for(c, hl, p)
        is_hl = c in hl
        ax.plot([0, v], [yi, yi], color=p["baseline"], linewidth=1, zorder=2)
        ax.plot([v], [yi], "o", color=color, markersize=cfg["marker_size"] + (4 if is_hl else 0), zorder=4)
        ax.text(v + vmax * 0.02, yi, fmt(v, unit), ha="left", va="center",
                fontsize=cfg["label_size"], color=p["text"] if is_hl else p["muted"],
                fontweight="bold" if is_hl else "normal")
    ax.invert_yaxis()
    ax.set_yticks(y)
    ax.set_yticklabels(cats, fontsize=cfg["font_size"])
    ax.set_xlim(0, vmax * 1.22)
    ax.xaxis.set_visible(False)
    ax.tick_params(axis="y", length=0, pad=10)
    _despine(ax, keep=(), color=p["baseline"])
    _style_ticklabels(ax.get_yticklabels(), hl, p)


KINDS = {"bar": _bar, "hbar": _hbar, "line": _line, "slope": _slope, "dot": _dot}


# ---------------------------------------------------------------------------
# entry
# ---------------------------------------------------------------------------
def render_chart(chart: dict, palette: dict, out_path: str, width_in: float, height_in: float,
                 fonts: dict | None = None, cfg: dict | None = None, language: str = "zh") -> str:
    """渲染一张图，返回 PNG 路径。宽高用英寸，与 pptx 里的放置框一致，避免二次缩放。"""
    cfg = {**DEFAULT_CFG, **(cfg or {})}
    kind = chart.get("kind")
    if kind not in KINDS:
        raise ValueError(f"不支持的 chart.kind: {kind!r}；只允许 {list(KINDS)}")
    setup_fonts(fonts)
    p = palette

    fig, ax = plt.subplots(figsize=(width_in, height_in), dpi=cfg["dpi"])
    fig.patch.set_facecolor(p["bg"])
    ax.set_facecolor(p["bg"])
    ax.grid(False)

    KINDS[kind](ax, chart, p, cfg)

    # 图内注释：一句话，说这张图想让人看到的那件事
    ann = chart.get("annotation")
    if ann:
        ax.text(0.0, 1.06, ann, transform=ax.transAxes, ha="left", va="bottom",
                fontsize=cfg["annotation_size"], color=p["text"])

    # 来源
    src = chart.get("source")
    if src:
        source_prefix = "Source: " if str(language).lower().startswith("en") else "来源："
        fig.text(0.012, 0.018, f"{source_prefix}{src}", ha="left", va="bottom",
                 fontsize=cfg["source_size"], color=p["muted"])

    # 示例数据角标
    if chart.get("is_example"):
        fig.text(0.99, 0.975, cfg["example_badge"], ha="right", va="top",
                 fontsize=cfg["source_size"] + 0.5, color=p["muted"],
                 bbox=dict(boxstyle="round,pad=0.35", facecolor="none", edgecolor=p["muted"], linewidth=0.8))

    left = 0.18 if kind in ("hbar", "dot") else (0.22 if kind == "slope" else 0.06)
    fig.subplots_adjust(left=left, right=0.97, top=0.86, bottom=0.2)
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    fig.savefig(out_path, dpi=cfg["dpi"], facecolor=p["bg"])
    plt.close(fig)
    return out_path


def main(argv=None) -> int:
    import yaml

    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("chart_yaml")
    ap.add_argument("out_png")
    ap.add_argument("--theme", default="ink")
    ap.add_argument("--size", default="11.7x4.6", help="宽x高（英寸）")
    ap.add_argument("--language", choices=["zh", "en"], default="zh")
    args = ap.parse_args(argv)

    with open(args.chart_yaml, encoding="utf-8") as f:
        node = yaml.safe_load(f)
    chart = node.get("chart", node)
    with open(os.path.join(SKILL_ROOT, "assets", "design-tokens.yaml"), encoding="utf-8") as f:
        tokens = yaml.safe_load(f)
    theme = tokens["themes"][args.theme]
    w, h = (float(x) for x in args.size.lower().split("x"))
    out = render_chart(chart, build_palette(theme, tokens.get("chart")), args.out_png, w, h,
                       fonts=tokens["typography"], cfg=tokens.get("chart"), language=args.language)
    print(f"→ {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
