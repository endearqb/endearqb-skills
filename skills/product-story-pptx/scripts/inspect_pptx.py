#!/usr/bin/env python3
"""inspect_pptx.py — 生成后的结构检查。

用法:
    python scripts/inspect_pptx.py out/deck.pptx
    python scripts/inspect_pptx.py out/deck.pptx --json

退出码:
    0  0 ERROR（WARN 需逐条判断）
    1  有 ERROR
    2  文件无法打开

检查项:
    E01 越界        形状超出画布（容差 0.03 in）
    E02 占位残留    空占位符；或文字含 "Click to add" / "单击此处" / "Lorem" / "TODO" / "{{" / "缺图："
    W03 疑似溢出    按字号与框宽估算的所需高度 > 框高 × 1.15
    W04 字号过小    < 12pt WARN；< 9pt ERROR（页脚 10pt 属正常，按位置放行；
                    形状名含 _MOCK 的“界面示意”矢量 UI 标签豁免——它们相当于
                    图表图片内的坐标轴文字，按设计稿字号放行，仍会汇总计数）
    W05 低分辩率    图片有效 ppi < 110 WARN；< 72 ERROR
    W06 文字框重叠  两个文字框相交面积 > 较小者的 20%
    W07 纯文字页    连续 ≥ 3 页没有图片 / 图表 / 形状
    I08 字体清单    实际写入的 latin / ea 字体名；用于对照渲染机器是否安装
    E09 UI 外壳      可编辑 UI 的 shell / titlebar / join / divider 完整且内嵌
    W10 UI 一致性    重复 UI 实例的圆角、标题栏高度与 inset 保持一致
"""
from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys

try:
    from pptx import Presentation
    from pptx.enum.shapes import MSO_SHAPE_TYPE
    from pptx.oxml.ns import qn
except ImportError:  # pragma: no cover
    print("缺少依赖: pip install python-pptx", file=sys.stderr)
    sys.exit(2)

EMU_PER_IN = 914400
CJK_RE = re.compile(r"[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\uff66-\uff9f]")
PLACEHOLDER_RE = re.compile(r"(Click to add|单击此处|Lorem ipsum|TODO|\{\{|缺图：|待替换)", re.IGNORECASE)
UI_ROLE_RE = re.compile(r"^PST_UI_MOCK_([A-Z0-9_]+)::(.+)$")


class Report:
    def __init__(self) -> None:
        self.items: list[dict] = []
        self.info: dict = {}

    def add(self, level: str, code: str, slide: int | None, msg: str) -> None:
        self.items.append({"level": level, "code": code, "slide": slide, "msg": msg})

    def count(self, level: str) -> int:
        return sum(1 for i in self.items if i["level"] == level)

    def print(self) -> None:
        for it in self.items:
            where = f"slide {it['slide']:>2}" if it["slide"] is not None else "deck    "
            print(f"[{it['level']}] {it['code']} {where}  {it['msg']}")
        fonts = self.info.get("fonts", {})
        print(f"\n字体: latin={sorted(fonts.get('latin', []))}  ea={sorted(fonts.get('ea', []))}")
        print(f"{self.count('ERROR')} ERROR, {self.count('WARN')} WARN")


# ---------------------------------------------------------------------------
def _units(text: str) -> float:
    return sum(1.0 if CJK_RE.match(c) else (0.3 if c.isspace() else 0.55) for c in text)


def est_height_in(text: str, w_in: float, size_pt: float, ls: float = 1.15) -> float:
    em = size_pt / 72
    per_line = max(1.0, (w_in - 0.1) / em)
    lines = sum(max(1, math.ceil(_units(p) / per_line)) for p in text.split("\n"))
    return lines * size_pt * ls / 72


def shape_rect(sh) -> tuple[float, float, float, float]:
    return (sh.left / EMU_PER_IN, sh.top / EMU_PER_IN, sh.width / EMU_PER_IN, sh.height / EMU_PER_IN)


def overlap_ratio(a, b) -> float:
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    ix = max(0.0, min(ax + aw, bx + bw) - max(ax, bx))
    iy = max(0.0, min(ay + ah, by + bh) - max(ay, by))
    inter = ix * iy
    small = min(aw * ah, bw * bh) or 1e-9
    return inter / small


def text_runs(sh):
    if not sh.has_text_frame:
        return
    for p in sh.text_frame.paragraphs:
        for r in p.runs:
            yield p, r


def _theme_effect_idx(shape) -> str | None:
    nodes = shape._element.xpath("./p:style/a:effectRef")
    return nodes[0].get("idx") if nodes else None


def _inspect_ui_instances(instances: dict, rep: Report) -> None:
    signatures = []
    required = {"SHELL", "TOPBAR", "TOPBAR_JOIN", "DIVIDER"}
    for (slide_no, instance), roles in sorted(instances.items()):
        missing = required - set(roles)
        if missing:
            rep.add("ERROR", "E09", slide_no, f"UI {instance} 缺少组件: {sorted(missing)}")
            continue
        shell, topbar, divider = roles["SHELL"], roles["TOPBAR"], roles["DIVIDER"]
        sx, sy, sw, sh = shape_rect(shell)
        tx, ty, tw, th = shape_rect(topbar)
        dx, dy, dw, dh = shape_rect(divider)
        tol = 0.035
        if tx < sx - tol or ty < sy - tol or tx + tw > sx + sw + tol or ty + th > sy + sh + tol:
            rep.add("ERROR", "E09", slide_no, f"UI {instance} 标题栏未完全嵌入 shell")
        if abs(dy - (sy + 0.50)) > 0.08 or dx < sx - tol or dx + dw > sx + sw + tol:
            rep.add("WARN", "W10", slide_no, f"UI {instance} 分隔线与标题栏边界不一致")
        effect = _theme_effect_idx(topbar)
        if effect not in (None, "0"):
            rep.add("ERROR", "E09", slide_no, f"UI {instance} 标题栏仍继承主题 effectRef={effect}，会像悬浮条")
        try:
            adjustment = float(shell.adjustments[0])
            corner_in = adjustment * min(sw, sh)
        except Exception:  # noqa: BLE001
            corner_in = 0.0
        if not 0.08 <= corner_in <= 0.30:
            rep.add("WARN", "W10", slide_no, f"UI {instance} shell 圆角约 {corner_in:.2f}in，桌面窗口建议 0.08–0.30in")
        signatures.append({
            "slide": slide_no, "instance": instance, "corner": corner_in,
            "titlebar_h": th, "inset_x": tx - sx, "inset_y": ty - sy,
        })
    if len(signatures) > 1:
        base = signatures[0]
        for sig in signatures[1:]:
            diffs = []
            if abs(sig["corner"] - base["corner"]) > 0.04:
                diffs.append("圆角")
            if abs(sig["titlebar_h"] - base["titlebar_h"]) > 0.04:
                diffs.append("标题栏高度")
            if abs(sig["inset_x"] - base["inset_x"]) > 0.03 or abs(sig["inset_y"] - base["inset_y"]) > 0.03:
                diffs.append("inset")
            if diffs:
                rep.add("WARN", "W10", sig["slide"],
                        f"UI {sig['instance']} 与 slide {base['slide']} 公共外壳不一致: {', '.join(diffs)}")


# ---------------------------------------------------------------------------
def inspect(path: str) -> Report:
    rep = Report()
    prs = Presentation(path)
    W, H = prs.slide_width / EMU_PER_IN, prs.slide_height / EMU_PER_IN
    tol = 0.03
    if abs((W / H) - (16 / 9)) > 0.01:
        rep.add("WARN", "W00", None, f"画布比例 {W:.3f}:{H:.3f} 不是 16:9")
    fonts_latin, fonts_ea = set(), set()
    text_only_streak = 0
    mock_labels = []
    ui_instances: dict[tuple[int, str], dict[str, object]] = {}

    for idx, slide in enumerate(prs.slides, start=1):
        text_boxes = []
        has_visual = False

        for sh in slide.shapes:
            x, y, w, h = shape_rect(sh)
            ui_match = UI_ROLE_RE.match(sh.name)
            if ui_match:
                role, instance = ui_match.groups()
                ui_instances.setdefault((idx, instance), {})[role] = sh

            # E01 越界
            if x < -tol or y < -tol or x + w > W + tol or y + h > H + tol:
                rep.add("ERROR", "E01", idx, f"「{sh.name}」越界: x={x:.2f} y={y:.2f} w={w:.2f} h={h:.2f}")

            # 视觉元素
            if sh.shape_type in (MSO_SHAPE_TYPE.PICTURE, MSO_SHAPE_TYPE.AUTO_SHAPE, MSO_SHAPE_TYPE.GROUP,
                                 MSO_SHAPE_TYPE.CHART) and not (sh.has_text_frame and sh.text_frame.text.strip()
                                                               and sh.shape_type != MSO_SHAPE_TYPE.PICTURE and w * h < 1.0):
                has_visual = True

            # E02 占位符
            if sh.is_placeholder and not (sh.has_text_frame and sh.text_frame.text.strip()):
                rep.add("ERROR", "E02", idx, f"空占位符「{sh.name}」")

            # W05 图片分辨率
            if sh.shape_type == MSO_SHAPE_TYPE.PICTURE and sh.name != "PST_SCRIM":
                try:
                    px_w, px_h = sh.image.size
                    ppi_x = px_w / w if w else 0
                    ppi_y = px_h / h if h else 0
                    ppi = min(ppi_x, ppi_y)
                    if ppi < 72:
                        rep.add("ERROR", "W05", idx, f"图片「{sh.name}」有效 {ppi:.0f} ppi < 72，会明显发糊")
                    elif ppi < 110:
                        rep.add("WARN", "W05", idx, f"图片「{sh.name}」有效 {ppi:.0f} ppi < 110")
                except Exception:  # noqa: BLE001
                    pass

            if not sh.has_text_frame:
                continue
            text = sh.text_frame.text.strip()
            if not text:
                continue

            # E02 占位文字
            if PLACEHOLDER_RE.search(text):
                rep.add("ERROR", "E02", idx, f"占位文字残留：「{text[:40]}」")

            sizes = []
            for p, r in text_runs(sh):
                if r.font.size is not None:
                    sizes.append(r.font.size.pt)
                rPr = r._r.find(qn("a:rPr"))
                if rPr is not None:
                    lat = rPr.find(qn("a:latin"))
                    ea = rPr.find(qn("a:ea"))
                    if lat is not None and lat.get("typeface"):
                        fonts_latin.add(lat.get("typeface"))
                    if ea is not None and ea.get("typeface"):
                        fonts_ea.add(ea.get("typeface"))
            if not sizes:
                continue
            smin, smax = min(sizes), max(sizes)
            is_footer = y > H - 0.6 or sh.name.startswith("PST_FOOTER_")
            # 形状名含 _MOCK 的是“界面示意”矢量 UI 标签：与图表图片内的坐标轴
            # 文字同类，按设计稿字号放行，不计入 W04。
            is_mock = "_MOCK" in sh.name
            if is_mock:
                mock_labels.append(text[:12])

            # W04 字号
            if not is_mock:
                if smin < 9:
                    rep.add("ERROR", "W04", idx, f"字号 {smin:.0f}pt < 9pt：「{text[:30]}」")
                elif smin < 12 and not is_footer:
                    rep.add("WARN", "W04", idx, f"字号 {smin:.0f}pt < 12pt：「{text[:30]}」")

            # W03 溢出估算（用最大字号保守估）
            need = est_height_in(text, w, smax)
            if text.strip() not in {"“", "”"} and need > h * 1.15 and h > 0.2:
                rep.add("WARN", "W03", idx, f"疑似溢出：需要约 {need:.2f}in，框高 {h:.2f}in：「{text[:30]}」")

            text_boxes.append({"rect": (x, y, w, h), "text": text, "name": sh.name})

        # W06 重叠
        for i in range(len(text_boxes)):
            for j in range(i + 1, len(text_boxes)):
                a, b = text_boxes[i], text_boxes[j]
                # 装饰性大引号允许压住引言区域；流程标签都在各自节点内，名称用于排除误报。
                if a["text"].strip() in {"“", "”"} or b["text"].strip() in {"“", "”"}:
                    continue
                if a["name"].startswith("PST_FLOW_") and b["name"].startswith("PST_FLOW_"):
                    continue
                r = overlap_ratio(a["rect"], b["rect"])
                if r > 0.2:
                    rep.add("WARN", "W06", idx,
                            f"文字框重叠 {r:.0%}：「{a['text'][:20]}」×「{b['text'][:20]}」")

        # W07 纯文字页
        text_only_streak = 0 if has_visual else text_only_streak + 1
        if text_only_streak == 3:
            rep.add("WARN", "W07", idx, "连续 3 页没有图片 / 图表 / 形状：观众会开始看手机")

    rep.info["fonts"] = {"latin": sorted(fonts_latin), "ea": sorted(fonts_ea)}
    rep.info["slides"] = len(prs.slides)
    rep.info["canvas_in"] = [round(W, 3), round(H, 3)]
    _inspect_ui_instances(ui_instances, rep)
    if ui_instances:
        rep.info["ui_mockup_instances"] = len(ui_instances)
    if mock_labels:
        rep.info["mock_ui_labels_exempted_from_W04"] = len(mock_labels)
    return rep


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pptx")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    if not os.path.isfile(args.pptx):
        print(f"文件不存在: {args.pptx}", file=sys.stderr)
        return 2
    try:
        rep = inspect(args.pptx)
    except Exception as e:  # noqa: BLE001
        print(f"无法打开: {e}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps({"items": rep.items, "info": rep.info}, ensure_ascii=False, indent=2))
    else:
        rep.print()
    return 1 if rep.count("ERROR") else 0


if __name__ == "__main__":
    sys.exit(main())
