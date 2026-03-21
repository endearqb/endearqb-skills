#!/usr/bin/env python3
"""
实验报告数据验证脚本模板
Lab Report Data Verification Script

使用方法：
1. 将用户提供的数据填入 USER_DATA 区域
2. 在 EXPECTED_VALUES 区域填入用户报告中的计算结果
3. 在 CALCULATIONS 区域写计算逻辑
4. 运行脚本，输出验证摘要

验证深度自动判断：
- 数据点 < 10个：轻量模式（仅输出结果对比）
- 数据点 10-50个：中度模式（输出中间步骤）
- 数据点 > 50个：深度模式（统计分析 + 可选图表数据）
"""

import math
import statistics
from typing import Any

# ============================================================
# 工具函数
# ============================================================

def check(label: str, user_val: float, calc_val: float, 
          tol_pct: float = 1.0, unit: str = "") -> dict:
    """
    比较用户值与计算值，返回验证结果。
    tol_pct: 允许误差百分比（默认1%）
    """
    if calc_val == 0:
        err_pct = 0.0 if user_val == 0 else float('inf')
    else:
        err_pct = abs(user_val - calc_val) / abs(calc_val) * 100
    
    status = "✓" if err_pct <= tol_pct else "✗"
    verdict = "吻合" if err_pct <= tol_pct else f"偏差超出{tol_pct}%容差"
    
    return {
        "label": label,
        "user_val": user_val,
        "calc_val": calc_val,
        "err_pct": err_pct,
        "status": status,
        "verdict": verdict,
        "unit": unit
    }


def print_result(r: dict):
    u = r['unit']
    print(f"  {r['status']} {r['label']}")
    print(f"      用户值: {r['user_val']:.4g} {u}")
    print(f"      计算值: {r['calc_val']:.4g} {u}")
    print(f"      误差:   {r['err_pct']:.3f}%  → {r['verdict']}")
    print()


def print_step(step_name: str, formula: str, result: Any, unit: str = ""):
    """输出计算中间步骤（中度/深度模式使用）"""
    print(f"  [{step_name}]")
    print(f"    公式: {formula}")
    print(f"    结果: {result:.4g} {unit}" if isinstance(result, (int, float)) else f"    结果: {result}")
    print()


def auto_mode(n_datapoints: int) -> str:
    if n_datapoints < 10:
        return "light"
    elif n_datapoints <= 50:
        return "medium"
    else:
        return "deep"


# ============================================================
# ↓↓↓ 根据用户提供的实验数据填写以下区域 ↓↓↓
# ============================================================

# --- 原始数据 ---
USER_DATA = {
    # 示例：
    # "temperature": [20, 30, 40, 50, 60],   # °C
    # "reaction_rate": [0.12, 0.24, 0.45, 0.89, 1.72],  # mol/L/s
    # "mass_sample": 5.234,   # g
    # "mass_product": 3.891,  # g
}

# --- 用户报告中声明的计算结果（待验证）---
EXPECTED_VALUES = {
    # 示例：
    # "yield_pct": 74.35,      # 产率 %
    # "mean_rate": 0.684,      # 平均反应速率
    # "activation_energy": 52.3,  # kJ/mol
}

# --- 报告元信息 ---
REPORT_META = {
    "title": "[实验标题]",
    "author": "[作者]",
    "date": "[日期]",
}


# ============================================================
# ↓↓↓ 在此编写计算逻辑 ↓↓↓
# ============================================================

def run_calculations(mode: str) -> list:
    """
    执行计算并返回验证结果列表。
    根据mode决定输出详细程度。
    """
    results = []
    
    # ---- 示例计算1：产率 ----
    # if "mass_sample" in USER_DATA and "mass_product" in USER_DATA:
    #     m_s = USER_DATA["mass_sample"]
    #     m_p = USER_DATA["mass_product"]
    #     
    #     if mode in ("medium", "deep"):
    #         print("  【中间步骤：产率计算】")
    #         print_step("原料质量", "已知", m_s, "g")
    #         print_step("产品质量", "已知", m_p, "g")
    #     
    #     calc_yield = m_p / m_s * 100
    #     
    #     if mode in ("medium", "deep"):
    #         print_step("理论产率", "m_product / m_sample × 100%", calc_yield, "%")
    #     
    #     if "yield_pct" in EXPECTED_VALUES:
    #         results.append(check("产率", EXPECTED_VALUES["yield_pct"], calc_yield, unit="%"))
    
    # ---- 示例计算2：平均值 ----
    # if "reaction_rate" in USER_DATA:
    #     rates = USER_DATA["reaction_rate"]
    #     mean_r = statistics.mean(rates)
    #     std_r  = statistics.stdev(rates) if len(rates) > 1 else 0
    #     
    #     if mode in ("medium", "deep"):
    #         print_step("均值", f"mean({rates})", mean_r, "mol/L/s")
    #         print_step("标准差", f"std({rates})", std_r, "mol/L/s")
    #     
    #     if "mean_rate" in EXPECTED_VALUES:
    #         results.append(check("平均反应速率", EXPECTED_VALUES["mean_rate"], mean_r, unit="mol/L/s"))
    
    # ---- 在此添加更多计算 ----
    
    return results


# ============================================================
# 主程序（不需要修改）
# ============================================================

def main():
    n_pts = sum(len(v) if isinstance(v, list) else 1 for v in USER_DATA.values())
    mode = auto_mode(n_pts)
    
    print("=" * 50)
    print(f"  实验报告数据验证")
    print(f"  {REPORT_META.get('title', '')}")
    print(f"  数据点数: {n_pts}  |  验证模式: {mode.upper()}")
    print("=" * 50)
    print()
    
    if not USER_DATA:
        print("  [跳过] 未提供数值数据，无需运行Python验证。")
        return
    
    if mode in ("medium", "deep"):
        print("【中间步骤输出】")
        print()
    
    results = run_calculations(mode)
    
    print("=" * 50)
    print("  验证摘要")
    print("=" * 50)
    
    if not results:
        print("  [提示] 未配置待验证项，请在EXPECTED_VALUES和run_calculations中补充。")
        return
    
    passed = [r for r in results if r["status"] == "✓"]
    failed = [r for r in results if r["status"] == "✗"]
    
    for r in results:
        print_result(r)
    
    print(f"  总计: {len(results)} 项  |  通过: {len(passed)}  |  偏差: {len(failed)}")
    print()
    
    if failed:
        print("  ⚠ 以下计算项存在偏差，请在报告中说明原因：")
        for r in failed:
            print(f"    - {r['label']}: 用户值={r['user_val']}, 计算值={r['calc_val']:.4g}, 误差={r['err_pct']:.2f}%")
    else:
        print("  ✅ 所有验证项均在容差范围内，数据可信。")
    
    print()
    print("  [将此摘要复制到HTML报告的「数据验证」小节]")


if __name__ == "__main__":
    main()
