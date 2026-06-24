---
name: anti-ai-slop-swarm
description: |
  多智能体去 AI 味流水线。六个独立审稿透镜（事实、膨胀、结构、词汇、语气、节奏）并行诊断同一文本，
  编排者合并去重排优先级，重写者统一修改，红队校验者检查信息损失与过度去味。
  触发：用户说 多智能体/swarm 去 AI 味、分维度审稿再合并重写、先诊断再重写、并行审稿，
  或长文/高风险稿需要多遍严格去 slop。快速单遍去味用 anti-ai-slop。
  禁止针对 AI 检测器优化或虚构人类经历。
metadata:
  version: 1.1.0
  triggers:
    - 多智能体去 AI 味
    - swarm 去 slop
    - 分维度审稿
    - 并行审稿重写
    - 先诊断再重写
    - 独立子智能体审稿
    - de-slop swarm
    - multi-agent de-slop
---

# Anti AI Slop · Swarm 编排

## 环境适配

| 能力 | 有 subagent（Claude Code / Cowork） | 无 subagent（Claude.ai） |
|------|------|------|
| 审稿透镜启动 | 真并行，独立上下文 | 顺序模拟，逐个透镜读判，K=1 |
| 上下文隔离 | 子 Agent 物理隔离 | 流式读取纪律：一次只装一个透镜，判完释放 |
| 红队校验 | 独立子 Agent 不读诊断 | Orchestrator 切换视角自评，标 `[self-judged]` |

无 subagent 环境下隔离靠纪律近似，无法消除上下文污染；追求完整隔离建议使用 Claude Code 或 Cowork。

## 核心抽象：四位一体对齐

```
slop 类别组(A–F)  ↔  审稿透镜(audit lens)  ↔  dim{编号}/ 工作区  ↔  Auditor Worker
       评分定位到维度 → 维度反查到透镜 → 透镜定位到 dim → 重部署 Worker
```

只要这条映射成立，"红队给某维度判不合格 → 反查对应透镜的诊断 → 定向重写那部分"就自动闭环。

六个透镜固定对齐 base 技能的 slop 分类六组：

| dim | 透镜 | 对应 base 分类组 | 透镜文件 |
|-----|------|------------------|----------|
| dim01 | 事实与证据 | A（1–4） | `references/lens/A-facts.md` |
| dim02 | 内容膨胀 | B（5–10） | `references/lens/B-bloat.md` |
| dim03 | 结构模板 | C（11–16） | `references/lens/C-structure.md` |
| dim04 | 词汇句法 | D（17–22） | `references/lens/D-diction.md` |
| dim05 | 对话语气 | E（23–29） | `references/lens/E-tone.md` |
| dim06 | 节奏格式 | F（30–35） | `references/lens/F-rhythm.md` |

## Agent 角色（独立子智能体）

每个角色的完整指令在 `agents/` 下，是该子智能体的独立 skill 文档。部署某角色时，把对应文件作为它的系统指令。

| 角色 | 数量 | 任务 | 独立文档 |
|------|------|------|----------|
| **Orchestrator** | 1 | 锁原文、分透镜、合并去重定级、裁决、调红队、精炼、交付 | `agents/orchestrator.md` |
| **Auditor（审稿透镜）** | 6（A–F） | 各自独立诊断一组 slop，**只诊断不改写** | `agents/auditor.md` + 对应 `lens/` |
| **Fact-Verifier** | 0–1 | 用工具核验事实锚点（可选） | `agents/fact-verifier.md` |
| **Rewriter** | 1 | 按统一问题清单执行修改 | `agents/rewriter.md` |
| **Loss-Verifier（红队）** | 1 | 对照原文检查信息损失/事实改动/过度去味 | `agents/loss-verifier.md` |
| **Voice-Matcher** | 0–1 | 提取作者风格卡（voice-match 模式） | `agents/voice-matcher.md` |

**铁律：审稿者只诊断不改写。** 六个审稿者各改各的必然冲突；诊断与重写分离，让重写者在一份合并后的、已解决透镜间冲突的清单上一次改完。

## 模式

| 模式 | 跑哪些角色 | 用途 |
|------|-----------|------|
| `audit-only` | 6 Auditor + 合并 | 只出诊断报告，不改稿 |
| `full-deslop`（默认） | 6 Auditor → Rewriter → Loss-Verifier（+精炼） | 完整诊断+重写+校验 |
| `surgical` | 6 Auditor → Rewriter（只修高/硬失败） → Loss-Verifier | 最小修补，保结构文气 |
| `+fact` | 任意模式叠加 Fact-Verifier | 含精确数字/时效信息，需工具核验 |
| `+voice` | 任意模式叠加 Voice-Matcher | 用户提供作者样本，需匹配声音 |

## 7-Phase 生命周期（映射到去 slop）

```
Phase 1  选模式（audit-only/full-deslop/surgical[+fact][+voice]）+ 声明配置
   ▼
Phase 2  冻结 contract.md：原文 = 不可变事实锚点 + 问题清单 schema
         产出 style_guide.md：从原文/样本提取的体裁/受众/语体/受保护内容    ◄── 🔒 用户检查点
   ▼
Phase 3  原文写入 shared/source.md（只读）；建 dim01–dim06[+voice/fact dim]
   ▼
Phase 4  部署 6 Auditor（各读 source + 自己的 lens，独立诊断）→ 产出完整问题清单（full_issues）
   ▼
Phase 5  full_issues → 去重 → 密度合并 → 解决冲突 → 排序 → 按浮动上限截取本轮批次（batch）
         剩余问题存入 backlog
   ▼
Phase 6  audit-only 到此交付诊断报告；否则部署 Rewriter 按 batch 执行修改 → 重写稿
   ▼
Phase 7  Loss-Verifier 红队 → 6 维质量门评分 + MSR 过度去味检测 → 不达标且未到上限且上轮有改进
         → 定向重写（有界精炼，回 Phase 6）；达标/触顶/无改进 → 交付
   ▼
交付    报告本轮处理数 / backlog 剩余数；若未启用 +fact/+voice，提示可补充启用  ◄── 💬 用户检查点
         用户满意 → STOP
         用户要求继续 → 回 Phase 5（以当前重写稿为输入，从 backlog 截取下一批次）
         用户要求补跑 +fact/+voice → 回 Phase 4 仅补跑对应 Agent（以当前重写稿为输入）
           → 新诊断追加入 backlog → 回 Phase 5
```

### 追加轮次规则

Phase 5 的浮动上限使每轮只处理优先级最高的一批问题，backlog 中的低优先级问题留待后续。交付时必须告知用户：

> 本轮处理了 X 个问题，backlog 中还有 Y 个未处理。如需进一步去味，我可以继续执行下一轮。
> [若未启用 +fact] 本轮未启用事实核验（+fact），如需核验文中数字/时效信息，可补充启用。
> [若未启用 +voice] 本轮未启用声音匹配（+voice），如有作者样本需匹配风格，可补充启用。

用户确认继续时，按以下规则回到 Phase 5：

- **输入文本更新**：以上轮重写稿（而非原始原文）作为 Rewriter 和 Loss-Verifier 的工作文本。
- **backlog 按序截取**：从 backlog 头部按同样的浮动上限截取下一批次；已被前轮附带修复的问题由 Rewriter 跳过。
- **补跑 +fact/+voice**：用户在交付检查点要求启用时，回到 Phase 4 仅部署对应 Agent（不重跑 6 个 Auditor）。Fact-Verifier 以当前重写稿为输入核验事实；Voice-Matcher 从用户提供的作者样本提取风格卡。新产出的诊断追加入 backlog 参与后续 Phase 5 排序，不覆盖已有诊断。
- **MSR 按轮独立计算**：每轮的修改句比只统计本轮 batch 引起的变动，不累加历史轮次。
- **contract 事实锚点不变**：所有轮次共享同一份 Phase 2 锁定的事实锚点，不因文本迭代而松动。
- **backlog 耗尽即止**：backlog 为空时流程终止，不再重新审稿。

## 硬约束

- **承重墙**：Orchestrator 不在自身上下文堆积所有透镜全文；需读全文深判时下放或流式逐个读。
- **有界回路**：单轮内精炼必须同时满足迭代上限（默认 2、上限 3）、收敛判据（6 维达标）、无改进即停。跨轮由用户驱动，backlog 耗尽即止。
- **单次裁决**：合并问题清单读一遍、排一次、定即止。
- **契约不可变**：Phase 2 锁定的事实锚点在所有轮次中不变，不因文本迭代而松动。
- **dim 隔离**：审稿者不读其他 dim，红队不读审稿诊断。
- **用户检查点**：Phase 2 默认等确认；交付时报告本轮处理数、backlog 剩余数及 +fact/+voice 启用状态，由用户决定继续、补跑或终止。

## 领域规则

- **原文即 Fact Anchors**：contract 的事实锚点段 = 原文全部数字、日期、人名、产品名、引文、立场、限制。所有子智能体只读不改。
- **审稿只诊断不改写**（见上铁律）。
- **收敛判据 = 浮动上限 + 密度合并 + 6 维质量门 + MSR 安全阀**：合并阶段先做密度合并（同类型 ≥3 次 → 系统性问题，提级），再按浮动上限 `min(max(ceil(字数/1000)×3, 5), 20)` 截取本轮 batch，剩余入 backlog。不追求每类归零（过度去味禁区）。MSR 按轮独立计算，full-deslop/surgical 模式下单轮 MSR > 45% 触发回退。
- **去 slop 不是新模板**：破折号、被动、副词、三项列表、设问、第一人称只有在高密度/无功能时才处理；审稿者按"严重程度"四级分级，红队按 6 维评分，都不把语境相关写法当硬错误。

## 参考文件索引（按需加载）

- 子智能体指令 → `agents/`（六份独立文档，见上表）
- 六个透镜的判据 → `references/lens/A-facts.md` … `F-rhythm.md`（各审稿者只读自己那片）
- 问题清单字段 / digest 格式 / 合并去重与冲突解决规则 → `references/issue-schema.md`
- 6 维质量门评分与收敛判据 → `references/quality-gate.md`

## Quick Start

```
1. Phase 1: 选模式 + 声明配置（mode, max_parallel, refine, checkpoint）
2. Phase 2: 冻结 contract.md（原文=事实锚点 + 问题清单 schema）+ style_guide.md → 🔒 检查点
3. Phase 3: source.md 入 shared/（只读）+ mkdir dim01–dim06
4. Phase 4: 部署 6 Auditor（按 agents/auditor.md + 各 lens 文件）→ full_issues [+fact/voice]
5. Phase 5: full_issues → 去重 → 密度合并 → 解决冲突 → 排序 → 截取 batch，剩余入 backlog
6. Phase 6: audit-only 交付诊断；否则 Rewriter 按 batch 执行
7. Phase 7: Loss-Verifier 红队 → quality-gate 评分 + MSR 检测 → [精炼] → 交付
8. 报告本轮处理数 / backlog 剩余数；若未启用 +fact/+voice 则提示 → 用户审核
   → 满意 → STOP
   → 继续 → 以当前重写稿为输入，回 Phase 5 截取下一批次
   → 补跑 +fact/+voice → 回 Phase 4 仅跑对应 Agent → 新诊断入 backlog → 回 Phase 5
```
