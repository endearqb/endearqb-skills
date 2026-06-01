# 模板：Adaptive-Routing（自适应路由）

## 适用场景
无法预先完全规划，需根据中间结果动态决策路径。典型场景：复杂问题诊断、动态任务分配。

## 不适用场景
路径完全确定无分支、需严格可重现流程。

## Agent 需求

| 角色 | 数量 | 职责 |
|------|------|------|
| Orchestrator | 1 | 路由决策、状态管理 |
| Router | 1（可复用 Orchestrator） | 根据条件选择路径 |
| Worker A/B/C | 2-N | 各分支路径执行者 |

## 流程图

```
Orchestrator: Initial Assessment + Classify
  -> Cond A -> Worker A (dim01/, Path Alpha)    --
  -> Cond B -> Worker B (dim02/, Path Beta)       |-- Execute Selected Path
  -> Cond C -> Worker C (dim03/, Path Gamma)    --
  -> Orchestrator: Merge/Route
       -> Done? -> No:  Re-Route to another Worker（受 max_reroutes 上限约束）
                   -> Yes: Deliver (output/)
```

## 终止条件与上限（有界 ReAct）

本模板是 ReAct 式"评估→重路由"自我发现回路，**必须有界**，遵守 SKILL.md `Refinement Loop` 的护栏：

1. **重路由上限** `max_reroutes`：默认 2，绝对不超过 3。达到上限仍未解决 → 输出当前最佳结论 + 标注未解决项，停止。
2. **收敛判据**：每次重路由前，必须能说明"为什么换这条路径会更接近目标"。给不出理由 → 停止，按现状交付。
3. **无进展即停**：若一次重路由后与目标的差距没有缩小，不再换路径，回到表现最好的那条路径的结果交付。
4. **状态记录**：每次评估与重路由写入 `{任务根}/refine_log.md`（评估结论、选定路径、理由）。

## Phase 分解

| Phase | 执行者 | 输入 | 输出 | Gate |
|-------|--------|------|------|------|
| P1-Assess | Orchestrator | 任务描述 + 上下文 | 初始评估报告 | 信息充分 |
| P2-Classify | Router | 评估报告 + 路由规则 | 选定路径 + 理由 | 分类准确 |
| P3-Execute | 对应 Worker | 路径任务 | dim{编号}/ 内路径执行结果 | 执行完成 |
| P4-Evaluate | Orchestrator | 路径结果 + 完成标准 | 完成判断 + 下一步决策 | 继续/结束 |
| P5-ReRoute | Router | 新路径选择 | 路由到对应 Worker（新 dim 目录） | 路径合理 |
| P6-Deliver | Orchestrator | 所有路径结果 | output/ 内最终交付物 | **Quality Gate** |

## 具体示例

**示例 A：智能问题诊断** —— 评估故障后分类：网络问题 dim01/、配置问题 dim02/、代码问题 dim03/，沿路径诊断，未解决则重路由，最终输出结论。

**示例 B：动态内容生成** —— 评估需求后分类：简单信息走图文、复杂演示走视频、数据密集走信息图，不满意则切换路径，最终输出内容产物。

## 变体
| 变体 | 说明 |
|------|------|
| **Hierarchical Routing** | 多层路由决策 |
| **Probabilistic Routing** | 基于概率选择路径 |
| **Feedback Routing** | 用户反馈驱动路由 |
