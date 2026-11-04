# 项目历史与当前状态

最后更新：2026-11-04

## 项目目的

这是一个可迁移的个人 PPT Skill：以 PPT Master 为生成引擎，提供用途 profile、视觉
style、离线优先的任务准备、渲染与审计工具。后续目标是在公司内网基于 GLM + OpenCode
接入历史 PPT、品牌规则和不同类别的私有模板包。

## 已完成

- 引入并固定 PPT Master 6.8.0（MIT，commit `5e8856b`），作为 `skills/ppt-master`。
- 建立 `skills/personal-ppt` 个人入口；profile 与 style 解耦，支持私有资料包扩展。
- 提供五类初始 profile：通用、汇报、学习分享、技术方案、复盘总结；两类 style：
  clean 与 editorial。
- 提供环境诊断、离线安装、源码发布、PowerPoint 原生渲染和 PPTX 审计脚本。
- 完成一套八页中文通用样稿，包含可编辑文字、形状、备注、逐页预览及人工视觉检查。
- 引入任务级 `spec.md` 与 SDD 检查：规格批准后才进入生成，交付记录保留验证结论。
- 本地基线已提交并同步到 GitHub `jiehuodashi888/skill-pptx-pro` 的 `main`。

## 当前结构

- `skills/personal-ppt/`：个人工作流、配置与脚本。
- `skills/ppt-master/`：固定上游引擎，保持其许可与来源。
- `specs/`：仓库级、已确认的可复用规格和决策。
- `examples/ai-work/`：已验证样稿与证据。
- 每个未来 job：`request.json` 固化选择和资料哈希，`spec.md` 固化需求与验收，输出目录
  保留 PPTX、渲染图和检查记录。

## 尚未验证或未实现

- 公司内网的 GLM + OpenCode 真机工作流。
- 从公司历史 PPT 自动提炼风格、品牌和模板并由业务人员确认。
- 公司私有 profile/style/模板包及其评测样本。
- PowerPoint 原生数据图表、复杂动画、外部图像、严格模板保真。
- 非 Windows/无 PowerPoint 环境的最终渲染等价性。

## 下一轮推荐工作

1. 在目标内网安装源码包和批准的离线依赖，运行 `doctor` 与一份无敏感资料的试做任务。
2. 收集已授权的历史 PPT，先提取候选风格与版式，再做小样供业务确认。
3. 为每个稳定业务类别建立私有 profile/style，并用代表性任务建立验收样本。
4. 把已确认的决策更新到 `specs/`，把本文件的“已完成 / 尚未验证”同步更新。

## 新对话如何接续

先阅读本文件、`specs/0001-personal-ppt-baseline.md`、
`skills/personal-ppt/SKILL.md` 与 `skills/personal-ppt/references/spec-sdd.md`。然后根据
具体任务选择或新增 private pack 中的 profile/style，创建 job，填写并批准 `spec.md`，
再执行生成与验收。
