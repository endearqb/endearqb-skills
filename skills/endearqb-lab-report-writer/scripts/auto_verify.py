#!/usr/bin/env python3
"""
实验报告数据自动验证脚本
auto_verify.py

功能：
- 自动读取CSV、TSV、或粘贴的表格数据
- 智能识别列名关键词，匹配计算模式
- 输出统计摘要 + 计算验证结果
- 验证深度根据数据量自动调节

用法：
  python auto_verify.py <数据文件路径>
  python auto_verify.py <数据文件路径> --claims "产率=74.35,均值=0.684"
  python auto_verify.py --stdin   （从标准输入读取粘贴的表格）
"""

import sys
import math
import argparse
import statistics
import re
from pathlib import Path

# ---- 尝试导入 pandas；不可用时降级为内置csv ----
try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False
    import csv as _csv


# ==============================================================
# 数据读取层
# ==============================================================

def read_data(source: str) -> dict:
    """
    读取数据源，返回 {列名: [数值列表]} 字典。
    source: 文件路径，或字符串形式的内联表格
    """
    if source == "--stdin":
        raw = sys.stdin.read()
        return _parse_text_table(raw)
    
    path = Path(source)
    if not path.exists():
        # 当作内联文本处理
        return _parse_text_table(source)
    
    if HAS_PANDAS:
        return _read_with_pandas(path)
    else:
        return _read_with_builtin_csv(path)


def _read_with_pandas(path: Path) -> dict:
    # 自动检测分隔符
    for sep in [',', '\t', ';', r'\s+']:
        try:
            df = pd.read_csv(path, sep=sep, engine='python')
            if df.shape[1] > 1:
                break
        except Exception:
            continue
    
    result = {}
    for col in df.columns:
        vals = pd.to_numeric(df[col], errors='coerce').dropna().tolist()
        if vals:
            result[col] = vals
    return result


def _read_with_builtin_csv(path: Path) -> dict:
    result = {}
    with open(path, newline='', encoding='utf-8-sig') as f:
        # 嗅探分隔符
        sample = f.read(2048)
        f.seek(0)
        dialect = _csv.Sniffer().sniff(sample, delimiters=',\t;')
        reader = _csv.DictReader(f, dialect=dialect)
        for row in reader:
            for key, val in row.items():
                try:
                    result.setdefault(key, []).append(float(val))
                except (ValueError, TypeError):
                    pass
    return result


def _parse_text_table(text: str) -> dict:
    """解析粘贴的Markdown表格或空格分隔表格"""
    lines = [l.strip() for l in text.strip().splitlines() if l.strip()]
    # 去掉Markdown表格分隔行（---|---）
    lines = [l for l in lines if not re.match(r'^[\|\s\-:]+$', l)]
    if not lines:
        return {}
    
    # 解析表头
    header_line = lines[0]
    if '|' in header_line:
        headers = [h.strip() for h in header_line.strip('|').split('|')]
    else:
        headers = header_line.split()
    
    result = {h: [] for h in headers if h}
    
    for line in lines[1:]:
        if '|' in line:
            cells = [c.strip() for c in line.strip('|').split('|')]
        else:
            cells = line.split()
        
        for h, cell in zip(headers, cells):
            if not h:
                continue
            try:
                result[h].append(float(cell.replace('%', '').replace(',', '')))
            except (ValueError, TypeError):
                pass
    
    return {k: v for k, v in result.items() if v}


# ==============================================================
# 统计摘要
# ==============================================================

def summarize(data: dict, mode: str) -> list[str]:
    lines = []
    lines.append("【统计摘要】")
    for col, vals in data.items():
        n = len(vals)
        if n == 0:
            continue
        mean = statistics.mean(vals)
        mn, mx = min(vals), max(vals)
        lines.append(f"  列: {col!r}  (n={n})")
        lines.append(f"    均值={mean:.4g}  最小={mn:.4g}  最大={mx:.4g}")
        if n >= 2:
            std = statistics.stdev(vals)
            rsd = std / mean * 100 if mean != 0 else float('inf')
            lines.append(f"    标准差={std:.4g}  RSD={rsd:.2f}%")
        if mode == "deep" and n >= 3:
            med = statistics.median(vals)
            lines.append(f"    中位数={med:.4g}")
    return lines


# ==============================================================
# 关键词→计算模式匹配
# ==============================================================

PATTERNS = [
    {
        "name": "产率/收率",
        "keys_need": [
            (r"(实验|actual|experiment|product|产品|产物)", "actual"),
            (r"(理论|theoretical|theory|理论量)", "theoretical"),
        ],
        "formula": "产率 = actual / theoretical × 100%",
        "compute": lambda d: (d["actual"] / d["theoretical"] * 100)
                   if d["theoretical"] != 0 else None,
        "unit": "%",
        "result_key": "yield",
    },
    {
        "name": "相对误差",
        "keys_need": [
            (r"(实验|measured|实测|experiment)", "measured"),
            (r"(理论|standard|真值|theoretical|reference)", "ref"),
        ],
        "formula": "相对误差 = |measured − ref| / ref × 100%",
        "compute": lambda d: abs(d["measured"] - d["ref"]) / abs(d["ref"]) * 100
                   if d["ref"] != 0 else None,
        "unit": "%",
        "result_key": "rel_error",
    },
    {
        "name": "欧姆定律 (R = U/I)",
        "keys_need": [
            (r"(电压|voltage|U[_\s]|V[_\s])", "U"),
            (r"(电流|current|I[_\s]|A[_\s])", "I"),
        ],
        "formula": "R = U / I",
        "compute": lambda d: d["U"] / d["I"] if d["I"] != 0 else None,
        "unit": "Ω",
        "result_key": "resistance",
    },
    {
        "name": "功率 (P = UI)",
        "keys_need": [
            (r"(电压|voltage|U[_\s])", "U"),
            (r"(电流|current|I[_\s])", "I"),
        ],
        "formula": "P = U × I",
        "compute": lambda d: d["U"] * d["I"],
        "unit": "W",
        "result_key": "power",
    },
    {
        "name": "速率 (ΔC/Δt)",
        "keys_need": [
            (r"(浓度|concentration|conc|C[_\s])", "C"),
            (r"(时间|time|t[_\s])", "t"),
        ],
        "formula": "速率 = ΔC / Δt（相邻点差分均值）",
        "compute": lambda d: statistics.mean(
            [abs(d["C"][i+1] - d["C"][i]) / abs(d["t"][i+1] - d["t"][i])
             for i in range(len(d["C"]) - 1)
             if d["t"][i+1] != d["t"][i]]
        ) if isinstance(d["C"], list) and len(d["C"]) > 1 else None,
        "unit": "单位/s",
        "result_key": "rate",
        "uses_series": True,
    },
]


def match_patterns(data: dict) -> list[dict]:
    """尝试将列名与计算模式匹配，返回匹配到的模式+数据字典列表"""
    matched = []
    col_names = list(data.keys())
    
    for pat in PATTERNS:
        binding = {}
        ok = True
        for regex, alias in pat["keys_need"]:
            found = None
            for col in col_names:
                if re.search(regex, col, re.IGNORECASE):
                    found = col
                    break
            if found is None:
                ok = False
                break
            vals = data[found]
            if pat.get("uses_series"):
                binding[alias] = vals
            else:
                # 对序列取均值作为代表值
                binding[alias] = statistics.mean(vals) if isinstance(vals, list) else vals
        
        if ok:
            matched.append({"pattern": pat, "binding": binding})
    
    return matched


# ==============================================================
# 用户声明值解析
# ==============================================================

def parse_claims(claims_str: str) -> dict:
    """
    解析 --claims "产率=74.35,均值=0.684" 为字典
    """
    if not claims_str:
        return {}
    result = {}
    for item in claims_str.split(','):
        if '=' in item:
            k, v = item.split('=', 1)
            try:
                result[k.strip()] = float(v.strip())
            except ValueError:
                pass
    return result


# ==============================================================
# 验证结果对比
# ==============================================================

def verify_value(label: str, calc_val: float,
                 user_claims: dict, tol: float = 1.0) -> dict:
    """在user_claims中查找与label最接近的键并对比"""
    matched_key = None
    for k in user_claims:
        if k in label or label in k or \
           re.search(re.escape(k), label, re.IGNORECASE):
            matched_key = k
            break
    
    if matched_key is None:
        return {"status": "—", "label": label, "calc_val": calc_val,
                "user_val": None, "err_pct": None}
    
    user_val = user_claims[matched_key]
    if calc_val == 0:
        err_pct = 0.0 if user_val == 0 else float('inf')
    else:
        err_pct = abs(user_val - calc_val) / abs(calc_val) * 100
    
    status = "✓" if err_pct <= tol else "✗"
    return {"status": status, "label": label,
            "calc_val": calc_val, "user_val": user_val,
            "err_pct": err_pct}


# ==============================================================
# 主程序
# ==============================================================

def main():
    parser = argparse.ArgumentParser(description="实验报告数据自动验证")
    parser.add_argument("source", nargs='?', default="--stdin",
                        help="CSV文件路径，或 --stdin 从标准输入读取")
    parser.add_argument("--claims", default="",
                        help='用户声明的计算结果，格式："产率=74.35,均值=0.684"')
    parser.add_argument("--tol", type=float, default=1.0,
                        help="误差容差百分比，默认1.0")
    args = parser.parse_args()

    # 1. 读取数据
    try:
        data = read_data(args.source)
    except Exception as e:
        print(f"[错误] 读取数据失败: {e}")
        sys.exit(1)

    if not data:
        print("[跳过] 未检测到数值数据，无需运行验证。")
        sys.exit(0)

    # 2. 确定验证模式
    n_pts = sum(len(v) for v in data.values())
    mode = "light" if n_pts < 10 else ("medium" if n_pts <= 50 else "deep")

    # 3. 解析用户声明值
    user_claims = parse_claims(args.claims)

    # 4. 打印标题
    print("=" * 50)
    print(f"  数据验证摘要 | 模式: {mode.upper()} | 数据点: {n_pts}")
    print(f"  列: {', '.join(data.keys())}")
    print("=" * 50)
    print()

    # 5. 统计摘要
    for line in summarize(data, mode):
        print(line)
    print()

    # 6. 计算模式匹配
    matched = match_patterns(data)
    results = []

    if matched:
        print("【计算验证】")
        for m in matched:
            pat = m["pattern"]
            binding = m["binding"]
            try:
                calc_val = pat["compute"](binding)
            except Exception:
                calc_val = None

            if calc_val is None:
                print(f"  [{pat['name']}] 计算失败（分母为零或数据不足）")
                continue

            label = f"{pat['name']} ({pat['formula']})"
            print(f"  [{pat['name']}]")
            print(f"    公式: {pat['formula']}")
            print(f"    计算值: {calc_val:.4g} {pat['unit']}")

            r = verify_value(pat["name"], calc_val, user_claims, args.tol)
            if r["user_val"] is not None:
                verdict = "吻合" if r["err_pct"] <= args.tol else f"偏差 {r['err_pct']:.2f}%，请在报告中说明"
                print(f"    用户声明值: {r['user_val']:.4g}  误差: {r['err_pct']:.2f}%  {r['status']} → {verdict}")
            results.append(r)
            print()
    else:
        print("【计算验证】")
        print("  未识别到已知计算模式，仅输出统计摘要。")
        print("  如需验证特定公式，请手动在 verify_data.py 中配置。")
        print()

    # 7. 最终摘要
    print("-" * 50)
    verified = [r for r in results if r["user_val"] is not None]
    passed   = [r for r in verified if r["status"] == "✓"]
    failed   = [r for r in verified if r["status"] == "✗"]

    if verified:
        print(f"  验证项合计: {len(verified)}  |  通过: {len(passed)}  |  存在偏差: {len(failed)}")
    if failed:
        print()
        print("  ⚠ 以下项存在偏差，建议在报告讨论中说明原因：")
        for r in failed:
            print(f"    - {r['label']}: 计算值={r['calc_val']:.4g}, 用户声明值={r['user_val']:.4g}, 误差={r['err_pct']:.2f}%")
    elif verified:
        print("  ✅ 所有验证项均在容差范围内。")

    print("=" * 50)
    print("  [将以上摘要复制到HTML报告的「数据验证」小节]")
    print()


if __name__ == "__main__":
    main()
