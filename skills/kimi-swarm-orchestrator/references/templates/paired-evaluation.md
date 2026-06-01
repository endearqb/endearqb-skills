# 模板：Paired-Evaluation（配对评估）

## 适用场景
需评估某 Agent/技能表现，有明确评估维度和基线参照。典型场景：技能优化、A/B 测试、质量评估、基准测试。

## 不适用场景
无明确评估标准、无可参照基线、纯主观评价。

## Agent 需求

| 角色 | 数量 | 职责 |
|------|------|------|
| Orchestrator | 1 | 定义标准、汇总分析、决策修订 |
| Subject A | 1 | 待评估对象（方案 A） |
| Subject B | 1 | 基线对象（方案 B） |
| Evaluator | 1 | 盲评对比两者产出 |

## 流程图

```
Orchestrator: Define Eval Dimensions -> Prepare Same Input
  -> Subject A (dim01/, with Skill/Approach A)   --
  -> Subject B (dim02/, with Baseline B)           |-- Parallel Execution
  -> Evaluator (dim03/): Blind Compare A vs B    --
  -> Orchestrator: Analyze Result
       -> Improve? -> Yes: Revise Skill (loop back)
                     -> No:  Final Skill Locked
```

## Phase 分解

| Phase | 执行者 | 输入 | 输出 | Gate |
|-------|--------|------|------|------|
| P1-Define | Orchestrator | 评估目标 + 维度建议 | 评估标准文档 | 标准完整 |
| P2-Prepare | Orchestrator | 评估标准 | 标准化测试输入集 | 输入一致 |
| P3-Execute-A | Subject A | 测试输入 + 方案 A | dim01/ 内 A 的产出 | 产出完整 |
| P4-Execute-B | Subject B | 测试输入 + 方案 B | dim02/ 内 B 的产出 | 产出完整 |
| P5-Evaluate | Evaluator | A/B 产出(匿名) | dim03/ 内各维度评分 + 评语 | **Quality Gate** |
| P6-Analyze | Orchestrator | 评分结果 | 改进建议清单 | 方向明确 |
| P7-Revise | Orchestrator | 改进建议 + 原方案 | 修订后方案 | 修订有效 |
| P8-Finalize | Orchestrator | 修订方案 | output/ 内最终定版方案 | **Quality Gate** |

## 具体示例

**示例 A：技能优化** —— 定义正确性/简洁性/可读性/性能四维度，准备 10 道题让 Skill v1 与基线分别解答，盲评后分析修订，锁定 v2 技能。

**示例 B：架构方案 A/B 对比** —— 定义可扩展性/维护成本/性能/安全性四维度，两方案实现相同业务场景后盲评，取优势设计混合方案锁定最终架构。

## 变体
| 变体 | 说明 |
|------|------|
| **Multi-Paired** | 多对 A/B 同时评估 |
| **Self-Evaluation** | Subject 自己评估自己 |
| **Human-in-Loop** | 人工作为 Evaluator |
