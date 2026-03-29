# endearqb-skills

[English](README.md) | [简体中文](README.zh-CN.md)

这是一个用于存放可复用 Agent Skills 的开源仓库。

## 仓库说明

当前仓库包含：

- `endearqb-lab-report-writer`：用于实验/报告类内容撰写与校验的技能，附带参考资料与校验脚本。
- `endearqb-frontend-dataviz`：用于前端数据可视化工作的技能，包含图表示例、配色方案、图标等参考资料。
- `endearqb-community-profiler`：用于群聊记录分析的技能，可生成成员画像、识别核心贡献者、评估社区健康度、总结聊天内容。
- `endearqb-wechat-file-organizer`：用于整理 Windows 微信文件存储目录的技能，支持自动检测目录、重复文件分析、移入回收站去重，以及按月份和类型分类整理。

## 目录结构

```text
skills/
  endearqb-lab-report-writer/
  endearqb-frontend-dataviz/
  endearqb-community-profiler/
  endearqb-wechat-file-organizer/
```

每个 skill 目录通常包含：

- `SKILL.md`：技能说明
- `references/`：参考资料
- `scripts/`：辅助脚本

## 使用方式

克隆本仓库后，可将各个 skill 目录作为本地技能包，在 Agent Skills 工作流中直接使用。

## 许可证

本项目采用 MIT License 开源，详见 `LICENSE` 文件。

## English README

英文说明见 `README.md`。
