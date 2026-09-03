#!/usr/bin/env python3
"""lint_deck.py — 生成前校验 deck spec。

用法:
    python scripts/lint_deck.py spec.yaml            # 人读输出
    python scripts/lint_deck.py spec.yaml --json     # 机器可读

退出码:
    0  无 FAIL（WARN 需逐条判断，不能默认忽略）
    1  有 FAIL
    2  文件不存在 / YAML 语法错误 / 顶层结构错误

规则编号（与 SKILL.md「硬规则」对应）:
    L00 schema            字段存在、枚举合法、energy 是 1–5 整数
    L01 action title      长度上限；疑似"话题标签"的短标题 WARN
    L02 type↔bleed        兼容表见 assets/layout-registry.yaml
    L03 energy 曲线       开场 ≥3；前 30% 有低谷 ≤2；末两页有 5；无连续 3 页相同；max−min ≥2
    L04 bleed 预算        full+color-block ≤ 40%；无连续 3 页 full；≥3 种模式含 none
    L05 压图页            full/overlay 必须有图、有 scrim、叠字上限、图宽 ≥ 1920
    L06 图表连续          连续 chart/big_number ≤ 2，随后必须是换气页
    L07 图表规则          kind 合法；source 必填；highlight ≤ 2；示例数据须标注；数据长度一致
    L08 流程图            3–7 步；恰好一个 highlight；label 长度
    L09 文字上限          body / bullets
    L10 图片              需要图的页有 image，且文件存在
    L11 主题              theme 存在于 design-tokens
    L12 版式单调          连续 3 页相同 type+bleed → WARN
    L13 结尾              第一页/最后一页类型与 CTA
    L14 叙事上下文        deck.big_idea / audience / desired_action 必填
    L15 主题篇幅预算      按 slides[].topics 校验 min_share / max_share
    L16 版本 lineage      initial / iteration、父 manifest 与回归页
    L17 可编辑 UI         ui_mockup 字段与桌面窗口约束
    L18 条目配图          media_bars 一对一图片映射与高亮
"""
from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys

try:
    import yaml
except ImportError:  # pragma: no cover
    print("缺少依赖: pip install pyyaml", file=sys.stderr)
    sys.exit(2)

SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(SKILL_ROOT, "assets")

VALID_TYPES = [
    "cover", "section", "statement", "quote", "feature_hero", "split",
    "bullets", "compare", "flow", "chart", "big_number", "gallery", "closing",
    "media_bars",
]
VALID_BLEEDS = [
    "none", "full", "partial-left", "partial-right", "half", "edge",
    "half-top", "half-bottom", "overlay", "color-block",
]
VALID_SCRIMS = ["none", "dark", "light", "gradient"]
VALID_FOCUS = ["center", "top", "bottom", "left", "right"]
CHART_KINDS = ["bar", "hbar", "line", "slope", "dot"]
IMAGE_REQUIRED_BLEEDS = [
    "full", "overlay", "partial-left", "partial-right", "half", "half-top", "half-bottom", "edge",
]
ON_IMAGE_BLEEDS = ["full", "overlay"]
UI_MOCKUP_BLEEDS = ["half", "partial-left", "partial-right", "half-top", "half-bottom"]

CJK_RE = re.compile(r"[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\uff66-\uff9f]")

# 常见"话题标签"式标题：只有名词，没有结论
TOPIC_LABEL_RE = re.compile(
    r"^(市场规模|产品介绍|功能介绍|团队介绍|竞品分析|商业模式|路线图|总结|"
    r"背景|现状|方案|架构|数据|案例|Agenda|Overview|Introduction|Roadmap|Summary|"
    r"Features?|Team|Market|Solution|Architecture|Thank ?you|谢谢|Q&A)$",
    re.IGNORECASE,
)


# ---------------------------------------------------------------------------
# 加载
# ---------------------------------------------------------------------------
def load_yaml(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise ValueError(f"{path} 顶层必须是映射（dict）")
    return data


def load_registry() -> dict:
    return load_yaml(os.path.join(ASSETS_DIR, "layout-registry.yaml"))


def load_tokens() -> dict:
    return load_yaml(os.path.join(ASSETS_DIR, "design-tokens.yaml"))


# ---------------------------------------------------------------------------
# 文本度量
# ---------------------------------------------------------------------------
def has_cjk(s: str) -> bool:
    return bool(CJK_RE.search(s or ""))


def text_len(s: str) -> tuple[int, str]:
    """返回 (长度, 单位)。含 CJK 按字符数（去空格）；否则按词数。"""
    s = (s or "").strip()
    if not s:
        return 0, "字"
    if has_cjk(s):
        return len(re.sub(r"\s+", "", s)), "字"
    return len(s.split()), "词"


def over_limit(s: str, cjk_limit: int, word_limit: int) -> tuple[bool, int, int, str]:
    n, unit = text_len(s)
    limit = cjk_limit if unit == "字" else word_limit
    return n > limit, n, limit, unit


# ---------------------------------------------------------------------------
# 报告
# ---------------------------------------------------------------------------
def _sparkline(values: list[int]) -> str:
    blocks = "▁▂▃▄▅"
    return "".join(blocks[max(1, min(5, int(v))) - 1] for v in values)


class Report:
    def __init__(self) -> None:
        self.items: list[dict] = []
        self.energy_sequence: list[int] = []
        self.bleed_sequence: list[str] = []
        self.topic_budget_results: list[dict] = []

    def fail(self, rule: str, slide: int | None, msg: str) -> None:
        self.items.append({"level": "FAIL", "rule": rule, "slide": slide, "msg": msg})

    def warn(self, rule: str, slide: int | None, msg: str) -> None:
        self.items.append({"level": "WARN", "rule": rule, "slide": slide, "msg": msg})

    @property
    def fails(self) -> list[dict]:
        return [i for i in self.items if i["level"] == "FAIL"]

    @property
    def warns(self) -> list[dict]:
        return [i for i in self.items if i["level"] == "WARN"]

    def print(self) -> None:
        if not self.items:
            print("✔ lint 通过：0 FAIL, 0 WARN")
            return
        for it in self.items:
            where = f"slide {it['slide']:>2}" if it["slide"] is not None else "deck    "
            print(f"[{it['level']}] {it['rule']} {where}  {it['msg']}")
        if self.energy_sequence:
            print(f"\nenergy: {' '.join(map(str, self.energy_sequence))}  {_sparkline(self.energy_sequence)}")
        if self.bleed_sequence:
            print("bleed:  " + " | ".join(self.bleed_sequence))
        print(f"\n{len(self.fails)} FAIL, {len(self.warns)} WARN")


# ---------------------------------------------------------------------------
# 单页校验
# ---------------------------------------------------------------------------
def _lint_slide(i: int, s: dict, spec: dict, reg: dict, tokens: dict, rep: Report,
                spec_dir: str) -> None:
    limits = reg["text_limits"]
    t = s.get("type")
    bleed = s.get("bleed", "none")

    # L00 schema
    if t not in VALID_TYPES:
        rep.fail("L00", i, f"type 非法: {t!r}；可选 {VALID_TYPES}")
        return
    if bleed not in VALID_BLEEDS:
        rep.fail("L00", i, f"bleed 非法: {bleed!r}；可选 {VALID_BLEEDS}")
        return
    energy = s.get("energy")
    if not isinstance(energy, int) or isinstance(energy, bool) or not 1 <= energy <= 5:
        rep.fail("L00", i, f"energy 必须是 1–5 的整数，当前 {energy!r}")
    if not (s.get("mood") or "").strip():
        rep.fail("L00", i, "缺少 mood（一两个词的情绪标签）")
    if s.get("scrim") not in (None, *VALID_SCRIMS):
        rep.fail("L00", i, f"scrim 非法: {s.get('scrim')!r}")
    if s.get("image_focus") not in (None, *VALID_FOCUS):
        rep.fail("L00", i, f"image_focus 非法: {s.get('image_focus')!r}")
    topics = s.get("topics") or []
    if not isinstance(topics, list) or any(not str(topic).strip() for topic in topics):
        rep.fail("L15", i, "topics 必须是非空字符串列表")

    # L01 action title
    title = (s.get("title") or "").strip()
    if not title:
        rep.fail("L01", i, "缺少 title（action title）")
    else:
        over, n, limit, unit = over_limit(title, limits["title_cjk"], limits["title_words"])
        if over:
            rep.fail("L01", i, f"title {n}{unit} > {limit}{unit}：「{title}」")
        if TOPIC_LABEL_RE.match(title) or (text_len(title)[0] <= 3 and t not in ("section", "cover")):
            rep.warn("L01", i, f"title 像话题标签而不是结论：「{title}」——改成一句有主张的话")

    # L02 type ↔ bleed
    allowed = reg["types"][t]["bleeds"]
    if bleed not in allowed:
        rep.fail("L02", i, f"type={t} 不允许 bleed={bleed}；可选 {allowed}")

    # L05 / L10 图片
    image = s.get("image")
    ui_mockup = s.get("ui_mockup")
    needs_image = bleed in IMAGE_REQUIRED_BLEEDS
    if image and ui_mockup:
        rep.fail("L17", i, "image 与 ui_mockup 只能选一个")
    if needs_image and not image and not ui_mockup:
        rep.fail("L10", i, f"bleed={bleed} 必须有 image；支持的界面页也可用 ui_mockup")
    if ui_mockup:
        _lint_ui_mockup(i, s, bleed, rep)
    if image:
        path = os.path.join(spec_dir, spec["deck"].get("assets_dir", "./assets"), image)
        if not os.path.isfile(path):
            rep.fail("L10", i, f"图片不存在: {path}")
        elif bleed in ON_IMAGE_BLEEDS:
            _check_image_width(i, path, 1920, rep)

    if bleed in ON_IMAGE_BLEEDS:
        scrim = s.get("scrim") or reg["bleed_modes"][bleed].get("scrim_default")
        if scrim in (None, "none"):
            rep.fail("L05", i, f"bleed={bleed} 必须有 scrim（dark / light / gradient）")
        combined = " ".join(x for x in [title, s.get("body") or ""] if x)
        over, n, limit, unit = over_limit(combined, limits["overlay_cjk"], limits["overlay_words"])
        if over:
            rep.fail("L05", i, f"压图页 title+body 共 {n}{unit} > {limit}{unit}，删字或改用 half / partial")

    # L09 文字上限
    body = s.get("body")
    if body:
        over, n, limit, unit = over_limit(body, limits["body_cjk"], limits["body_words"])
        if over:
            rep.fail("L09", i, f"body {n}{unit} > {limit}{unit}")
    bullets = s.get("bullets") or []
    if bullets:
        if not isinstance(bullets, list):
            rep.fail("L00", i, "bullets 必须是列表")
        else:
            if len(bullets) > limits["bullets_max"]:
                rep.fail("L09", i, f"bullets {len(bullets)} 条 > {limits['bullets_max']}")
            for b in bullets:
                over, n, limit, unit = over_limit(str(b), limits["bullet_cjk"], limits["bullet_words"])
                if over:
                    rep.fail("L09", i, f"bullet {n}{unit} > {limit}{unit}：「{b}」")
    if body and bullets and t in ("feature_hero", "split"):
        rep.warn("L09", i, f"{t} 页 body 与 bullets 同时出现，通常只留一个")

    # type 专用
    if t == "quote":
        if not (s.get("quote") or "").strip():
            rep.fail("L00", i, "quote 页缺少 quote 字段")
        if not (s.get("attribution") or "").strip():
            rep.warn("L00", i, "quote 页缺少 attribution（署名）")
    if t == "compare":
        for side in ("left", "right"):
            blk = s.get(side)
            if not isinstance(blk, dict) or not blk.get("title"):
                rep.fail("L00", i, f"compare 页缺少 {side}.title")
            elif len(blk.get("bullets") or []) > limits["bullets_max"]:
                rep.fail("L09", i, f"compare.{side} bullets > {limits['bullets_max']}")
    if t == "gallery":
        imgs = s.get("images") or []
        if not 2 <= len(imgs) <= 4:
            rep.fail("L00", i, f"gallery 需要 2–4 张图，当前 {len(imgs)}")
        for im in imgs:
            p = os.path.join(spec_dir, spec["deck"].get("assets_dir", "./assets"), im)
            if not os.path.isfile(p):
                rep.fail("L10", i, f"图片不存在: {p}")
    if t == "flow":
        _lint_flow(i, s, limits, spec, spec_dir, rep)
    if t == "chart":
        _lint_chart(i, s, rep)
    if t == "big_number":
        if not str(s.get("number") or "").strip():
            rep.fail("L00", i, "big_number 页缺少 number")
        if not (s.get("source") or "").strip():
            rep.fail("L07", i, "big_number 页缺少 source")
        if s.get("is_example") and "示例" not in (title + (s.get("source") or "")):
            rep.fail("L07", i, "is_example=true 时 title 或 source 必须含「示例」")
    if t == "media_bars":
        _lint_media_bars(i, s, spec, spec_dir, rep)


def _lint_ui_mockup(i: int, s: dict, bleed: str, rep: Report) -> None:
    ui = s.get("ui_mockup")
    if not isinstance(ui, dict):
        rep.fail("L17", i, "ui_mockup 必须是映射")
        return
    if bleed not in UI_MOCKUP_BLEEDS:
        rep.fail("L17", i, f"ui_mockup 不支持 bleed={bleed}；可选 {UI_MOCKUP_BLEEDS}")
    if s.get("type") not in ("feature_hero", "split"):
        rep.fail("L17", i, "ui_mockup 当前只用于 feature_hero / split")
    if not str(ui.get("title") or "").strip():
        rep.fail("L17", i, "ui_mockup.title 必填")
    if ui.get("theme", "light") not in ("light", "dark"):
        rep.fail("L17", i, "ui_mockup.theme 只支持 light / dark")
    if ui.get("badge") and "示意" not in str(ui["badge"]):
        rep.warn("L17", i, "ui_mockup.badge 建议明确含“示意”，避免被误认为真实截图")
    for field, maximum in (("sidebar", 5), ("kpis", 3), ("items", 4)):
        value = ui.get(field) or []
        if not isinstance(value, list):
            rep.fail("L17", i, f"ui_mockup.{field} 必须是列表")
        elif len(value) > maximum:
            rep.fail("L17", i, f"ui_mockup.{field} 最多 {maximum} 项，当前 {len(value)}")
    for field in ("kpis", "items"):
        for item in ui.get(field) or []:
            if not isinstance(item, dict) or not str(item.get("label") or "").strip():
                rep.fail("L17", i, f"ui_mockup.{field} 每项必须有 label")


def _lint_media_bars(i: int, s: dict, spec: dict, spec_dir: str, rep: Report) -> None:
    items = s.get("items")
    if not isinstance(items, list) or not 3 <= len(items) <= 5:
        rep.fail("L18", i, f"media_bars 需要 3–5 个 items，当前 {len(items) if isinstance(items, list) else 0}")
        return
    ratio = s.get("bar_width_ratio", 0.60)
    if isinstance(ratio, bool) or not isinstance(ratio, (int, float)) or not 0.45 <= ratio <= 0.72:
        rep.fail("L18", i, "bar_width_ratio 必须在 0.45–0.72 之间")
    if s.get("media_side", "alternating") not in ("aligned", "alternating"):
        rep.fail("L18", i, "media_side 只支持 aligned / alternating")
    highlights = 0
    for item in items:
        if not isinstance(item, dict) or not str(item.get("label") or "").strip():
            rep.fail("L18", i, "media_bars 每项必须有 label")
            continue
        if item.get("highlight"):
            highlights += 1
        image = item.get("image")
        if not image:
            rep.fail("L18", i, f"条目「{item.get('label')}」缺少一对一 image")
            continue
        path = os.path.join(spec_dir, spec["deck"].get("assets_dir", "./assets"), image)
        if not os.path.isfile(path):
            rep.fail("L10", i, f"条目配图不存在: {path}")
    if highlights > 1:
        rep.fail("L18", i, f"media_bars 有 {highlights} 个 highlight，最多一个")


def _check_image_width(i: int, path: str, min_w: int, rep: Report) -> None:
    try:
        from PIL import Image
    except ImportError:
        rep.warn("L05", i, "未安装 Pillow，跳过图片分辨率检查")
        return
    try:
        with Image.open(path) as im:
            w, h = im.size
    except Exception as e:  # noqa: BLE001
        rep.fail("L05", i, f"图片无法打开: {path} ({e})")
        return
    if w < min_w:
        rep.fail("L05", i, f"压图页图片宽 {w}px < {min_w}px，会糊；换图或改 half / partial")
    elif w < 2400:
        rep.warn("L05", i, f"图片宽 {w}px，投影放大后偏软，能换更大的就换")


def _lint_flow(i: int, s: dict, limits: dict, spec: dict, spec_dir: str, rep: Report) -> None:
    steps = s.get("steps")
    if not isinstance(steps, list):
        rep.fail("L08", i, "flow 页缺少 steps 列表")
        return
    n = len(steps)
    if not limits["flow_steps_min"] <= n <= limits["flow_steps_max"]:
        rep.fail("L08", i, f"flow 步数 {n}，需要 {limits['flow_steps_min']}–{limits['flow_steps_max']}；多了就拆页")
    hl = [st for st in steps if isinstance(st, dict) and st.get("highlight")]
    if len(hl) == 0:
        rep.fail("L08", i, "flow 必须有且只能有一个 highlight 节点")
    elif len(hl) > 1:
        rep.fail("L08", i, f"flow 有 {len(hl)} 个 highlight，只能一个")
    for st in steps:
        if not isinstance(st, dict) or not st.get("label"):
            rep.fail("L08", i, "flow 每一步都要有 label")
            continue
        if "\n" in str(st["label"]) or "\r" in str(st["label"]):
            rep.fail("L08", i, f"flow label 不允许手工换行：「{st['label']}」")
        over, m, limit, unit = over_limit(st["label"], limits["flow_label_cjk"], limits["flow_label_words"])
        if over:
            rep.fail("L08", i, f"flow label {m}{unit} > {limit}{unit}：「{st['label']}」")
        if "\n" in str(st.get("desc") or "") or "\r" in str(st.get("desc") or ""):
            rep.fail("L08", i, f"flow desc 必须保持单行：「{st.get('desc')}」")
    if s.get("direction") not in (None, "horizontal", "vertical"):
        rep.fail("L00", i, f"flow.direction 非法: {s.get('direction')!r}")
    if s.get("style") not in (None, "cards", "chevron", "layers"):
        rep.fail("L00", i, f"flow.style 非法: {s.get('style')!r}")
    images = s.get("images") or []
    if images:
        if not isinstance(images, list) or not 1 <= len(images) <= 3:
            rep.fail("L08", i, "flow.images 必须是 1–3 张图片的列表")
        elif s.get("direction") != "vertical" or s.get("style") != "layers":
            rep.fail("L08", i, "flow 多图增强只支持 direction=vertical + style=layers")
        else:
            for image in images:
                path = os.path.join(spec_dir, spec["deck"].get("assets_dir", "./assets"), image)
                if not os.path.isfile(path):
                    rep.fail("L10", i, f"flow 配图不存在: {path}")


def _lint_chart(i: int, s: dict, rep: Report) -> None:
    c = s.get("chart")
    if not isinstance(c, dict):
        rep.fail("L07", i, "chart 页缺少 chart 块")
        return
    kind = c.get("kind")
    if kind not in CHART_KINDS:
        rep.fail("L07", i, f"chart.kind 非法: {kind!r}；只允许 {CHART_KINDS}（饼图/环图/3D/双轴一律不用）")
    if not (c.get("source") or "").strip():
        rep.fail("L07", i, "chart.source 必填")
    data = c.get("data") or {}
    cats = data.get("categories") or []
    series = data.get("series") or []
    if not cats or not series:
        rep.fail("L07", i, "chart.data 需要 categories 与至少一个 series")
    else:
        if len(series) > 3:
            rep.fail("L07", i, f"chart 有 {len(series)} 个 series > 3；拆成多页")
        for se in series:
            vals = se.get("values") if isinstance(se, dict) else None
            if not isinstance(se, dict) or not (se.get("name") or "").strip():
                rep.fail("L07", i, "每个 chart series 都必须有 name")
                continue
            if not isinstance(vals, list) or len(vals) != len(cats):
                rep.fail("L07", i, f"series「{se.get('name')}」values 长度须等于 categories 长度 {len(cats)}")
                continue
            bad = [v for v in vals if v is not None and (isinstance(v, bool) or not isinstance(v, (int, float)))]
            if bad:
                rep.fail("L07", i, f"series「{se.get('name')}」含非数值: {bad[:3]}")
            elif kind in ("bar", "hbar") and any((v is not None and v < 0) for v in vals):
                rep.warn("L07", i, "柱状图出现负值：确认是否应改用 dot / line")
    if kind == "slope" and len(cats) != 2:
        rep.fail("L07", i, "slope 图 categories 必须恰好 2 个（起点 / 终点）")
    if kind in ("bar", "hbar", "dot") and len(series) > 1:
        rep.warn("L07", i, f"{kind} 有 {len(series)} 个 series，一图只讲一件事；考虑拆页或改 line/slope")
    if kind in ("bar", "hbar") and len(cats) > 8:
        rep.warn("L07", i, f"柱状图 {len(cats)} 个类别，考虑合并「其他」")
    hl = c.get("highlight") or []
    if not hl:
        rep.warn("L07", i, "chart 没有 highlight：这张图想让观众看哪一个？")
    elif len(hl) > 2:
        rep.fail("L07", i, f"highlight {len(hl)} 个 > 2")
    else:
        names = cats if kind in ("bar", "hbar", "dot") else [se.get("name") for se in series if isinstance(se, dict)]
        for h in hl:
            if h not in names:
                rep.fail("L07", i, f"highlight「{h}」不在 {'categories' if kind in ('bar','hbar','dot') else 'series.name'} 里")
    if c.get("is_example"):
        blob = (s.get("title") or "") + (c.get("source") or "")
        if "示例" not in blob:
            rep.fail("L07", i, "is_example=true 时 title 或 source 必须含「示例」")


def _lint_lineage(deck: dict, slides: list, spec_dir: str, rep: Report) -> None:
    lineage = deck.get("lineage")
    if lineage is None:
        return
    if not isinstance(lineage, dict):
        rep.fail("L16", None, "deck.lineage 必须是映射")
        return
    mode = lineage.get("mode", "initial")
    if mode not in ("initial", "iteration"):
        rep.fail("L16", None, "lineage.mode 只支持 initial / iteration")
    if not str(lineage.get("version") or "").strip():
        rep.fail("L16", None, "lineage.version 必填")
    if mode == "iteration":
        parent = lineage.get("parent_manifest")
        if not parent:
            rep.fail("L16", None, "iteration 必须提供 lineage.parent_manifest")
        else:
            path = parent if os.path.isabs(parent) else os.path.join(spec_dir, parent)
            if not os.path.isfile(path):
                rep.fail("L16", None, f"父 manifest 不存在: {path}")
        if not str(lineage.get("change_summary") or "").strip():
            rep.fail("L16", None, "iteration 必须提供 lineage.change_summary")
        pages = lineage.get("regression_pages")
        if not isinstance(pages, list) or not pages:
            rep.fail("L16", None, "iteration 必须列出 lineage.regression_pages")
        else:
            bad = [p for p in pages if isinstance(p, bool) or not isinstance(p, int) or not 1 <= p <= len(slides)]
            if bad:
                rep.fail("L16", None, f"regression_pages 含非法页码: {bad}")
        components = lineage.get("affected_components") or []
        if not isinstance(components, list):
            rep.fail("L16", None, "lineage.affected_components 必须是列表")


def _lint_topic_budgets(deck: dict, slides: list, rep: Report) -> None:
    budgets = deck.get("topic_budgets")
    if budgets is None:
        return
    if not isinstance(budgets, list):
        rep.fail("L15", None, "deck.topic_budgets 必须是列表")
        return
    total = len(slides)
    for budget in budgets:
        if not isinstance(budget, dict) or not str(budget.get("topic") or "").strip():
            rep.fail("L15", None, "每个 topic_budget 必须有 topic")
            continue
        topic = str(budget["topic"])
        lo, hi = budget.get("min_share"), budget.get("max_share")
        for key, value in (("min_share", lo), ("max_share", hi)):
            if value is not None and (isinstance(value, bool) or not isinstance(value, (int, float)) or not 0 <= value <= 1):
                rep.fail("L15", None, f"{topic}.{key} 必须在 0–1 之间")
        if lo is not None and hi is not None and isinstance(lo, (int, float)) and isinstance(hi, (int, float)) and lo > hi:
            rep.fail("L15", None, f"{topic}.min_share 不能大于 max_share")
        tagged = sum(1 for slide in slides if topic in (slide.get("topics") or []))
        share = tagged / total
        rep.topic_budget_results.append({"topic": topic, "slides": tagged, "total": total, "share": share})
        if lo is not None and isinstance(lo, (int, float)) and share < lo:
            rep.fail("L15", None, f"topic={topic} 占 {tagged}/{total}={share:.1%} < min_share {lo:.1%}")
        if hi is not None and isinstance(hi, (int, float)) and share > hi:
            rep.fail("L15", None, f"topic={topic} 占 {tagged}/{total}={share:.1%} > max_share {hi:.1%}")


# ---------------------------------------------------------------------------
# 整体校验
# ---------------------------------------------------------------------------
def lint(spec: dict, reg: dict, tokens: dict, spec_path: str = "spec.yaml") -> Report:
    rep = Report()
    spec_dir = os.path.dirname(os.path.abspath(spec_path))

    deck = spec.get("deck")
    slides = spec.get("slides")
    if not isinstance(deck, dict):
        rep.fail("L00", None, "缺少 deck 块")
        return rep
    if not isinstance(slides, list) or not slides:
        rep.fail("L00", None, "slides 必须是非空列表")
        return rep
    if not (deck.get("title") or "").strip():
        rep.fail("L00", None, "deck.title 必填")
    for field, meaning in (("big_idea", "整份 deck 的核心主张"),
                           ("audience", "目标受众"),
                           ("desired_action", "观众看完后的行动")):
        if not str(deck.get(field) or "").strip():
            rep.fail("L14", None, f"deck.{field} 必填（{meaning}）")
    language = str(deck.get("language", "zh")).lower()
    if language not in ("zh", "en"):
        rep.fail("L00", None, f"deck.language 只支持 zh / en，当前 {language!r}")
    spec_dir = os.path.dirname(os.path.abspath(spec_path))
    _lint_lineage(deck, slides, spec_dir, rep)
    _lint_topic_budgets(deck, slides, rep)

    # L11 主题
    theme = deck.get("theme")
    if theme not in tokens["themes"]:
        rep.fail("L11", None, f"theme={theme!r} 不存在；可选 {list(tokens['themes'])}")
    brand = deck.get("brand") or {}
    for k, v in brand.items():
        if k in ("accent", "color_block") and not re.fullmatch(r"#[0-9A-Fa-f]{6}", str(v)):
            rep.fail("L11", None, f"brand.{k} 必须是 #RRGGBB，当前 {v!r}")

    for i, s in enumerate(slides, start=1):
        if not isinstance(s, dict):
            rep.fail("L00", i, "每一页必须是映射")
            continue
        _lint_slide(i, s, spec, reg, tokens, rep, spec_dir)

    if rep.fails:  # schema 都不过，曲线检查没意义
        return rep

    n = len(slides)
    r = reg["rhythm"]
    energies = [s["energy"] for s in slides]
    bleeds = [s.get("bleed", "none") for s in slides]
    types = [s["type"] for s in slides]
    rep.energy_sequence = energies
    rep.bleed_sequence = bleeds

    # L03 energy 曲线
    if energies[0] < r["opening_min_energy"]:
        rep.fail("L03", 1, f"开场 energy {energies[0]} < {r['opening_min_energy']}")
    first_dip_window = max(1, math.ceil(n * r["first_dip_within"]))
    if not any(e <= r["dip_max_energy"] for e in energies[:first_dip_window]):
        rep.fail("L03", None, f"前 {first_dip_window} 页没有低谷（energy ≤ {r['dip_max_energy']}）：观众没感到问题，就不会在意方案")
    if r["peak_energy"] not in energies[-r["peak_in_last_n"]:]:
        rep.fail("L03", None, f"最后 {r['peak_in_last_n']} 页没有 energy {r['peak_energy']}：结尾要停在高点")
    streak = 1
    for k in range(1, n):
        streak = streak + 1 if energies[k] == energies[k - 1] else 1
        if streak > r["max_same_streak"]:
            rep.fail("L03", k + 1, f"连续 {streak} 页 energy 相同（{energies[k]}）：插入 statement / 换成 feature_hero 拉开")
    if max(energies) - min(energies) < r["min_range"]:
        rep.fail("L03", None, f"energy 跨度 {max(energies) - min(energies)} < {r['min_range']}：整份 deck 太平")
    for k, (energy, bleed, slide_type) in enumerate(zip(energies, bleeds, types), start=1):
        if energy == 5 and bleed not in ("full", "overlay", "color-block"):
            rep.warn("L03", k, f"energy=5 但 bleed={bleed}；峰值通常需要更强的视觉释放")
        if energy <= 2 and bleed in ("full", "overlay") and slide_type not in ("quote",):
            rep.warn("L03", k, f"energy={energy} 却使用 {bleed}；低谷页通常应更安静、更留白")
    for k in range(1, n):
        if energies[k] == 5 and min(energies[max(0, k - 2):k]) >= 4:
            rep.warn("L03", k + 1, "峰值前缺少明显低谷；先收紧再释放，反差会更强")

    # L04 bleed 预算
    heavy = sum(1 for b in bleeds if b in ("full", "color-block"))
    if heavy / n > r["bleed_budget"]:
        rep.fail("L04", None, f"full + color-block 共 {heavy}/{n} = {heavy / n:.0%} > {r['bleed_budget']:.0%}")
    streak = 0
    for k, b in enumerate(bleeds):
        streak = streak + 1 if b == "full" else 0
        if streak > r["max_full_streak"]:
            rep.fail("L04", k + 1, f"连续 {streak} 页 full bleed：满屏大图连着放就不再是峰值")
    variety = set(bleeds)
    if len(variety) < r["min_bleed_variety"] or "none" not in variety:
        rep.fail("L04", None, f"bleed 模式只有 {sorted(variety)}，需要 ≥ {r['min_bleed_variety']} 种且包含 none")

    # L06 图表连续
    streak = 0
    for k, t in enumerate(types):
        if t in ("chart", "big_number"):
            streak += 1
            if streak > r["max_chart_streak"]:
                rep.fail("L06", k + 1, f"连续 {streak} 页图表：中间放一页 {r['breath_types']} 换气")
        else:
            if streak == r["max_chart_streak"] and t not in r["breath_types"]:
                rep.warn("L06", k + 1, f"两页图表之后接 {t}，建议用 {r['breath_types']} 之一换气")
            streak = 0

    # L12 版式单调
    combo = [f"{t}/{b}" for t, b in zip(types, bleeds)]
    streak = 1
    for k in range(1, n):
        streak = streak + 1 if combo[k] == combo[k - 1] else 1
        if streak == 3:
            rep.warn("L12", k + 1, f"连续 3 页 {combo[k]}：换一种版式或 bleed")

    # L13 结尾
    if types[-1] != "closing":
        rep.warn("L13", n, f"最后一页是 {types[-1]}，通常应为 closing（含 CTA）")
    else:
        closing = slides[-1]
        if not (closing.get("body") or closing.get("cta")):
            rep.warn("L13", n, "closing 页没有 body/cta；把下一步行动写清楚")
    if types[0] != "cover":
        rep.warn("L13", 1, f"第一页是 {types[0]}，通常应为 cover")

    return rep


# ---------------------------------------------------------------------------
def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("spec")
    ap.add_argument("--json", action="store_true", help="以 JSON 输出")
    args = ap.parse_args(argv)

    if not os.path.isfile(args.spec):
        print(f"文件不存在: {args.spec}", file=sys.stderr)
        return 2
    try:
        spec = load_yaml(args.spec)
        reg = load_registry()
        tokens = load_tokens()
    except Exception as e:  # noqa: BLE001
        print(f"YAML 读取失败: {e}", file=sys.stderr)
        return 2

    rep = lint(spec, reg, tokens, args.spec)
    if args.json:
        print(json.dumps({
            "passed": not rep.fails,
            "fails": rep.fails,
            "warns": rep.warns,
            "energy_sequence": rep.energy_sequence,
            "bleed_sequence": rep.bleed_sequence,
            "topic_budget_results": rep.topic_budget_results,
        }, ensure_ascii=False, indent=2))
    else:
        rep.print()
    return 1 if rep.fails else 0


if __name__ == "__main__":
    sys.exit(main())
