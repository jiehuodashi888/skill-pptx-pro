# Personal PPT 0.3

可迁移的个人 PPT 技能，基于 MIT 许可的 PPT Master 6.8.0。个人入口为 `skills/personal-ppt/SKILL.md`，引擎为同级 `skills/ppt-master`。

## 内容

- `skills/personal-ppt`：个人配置、依赖诊断、安装打包、原生渲染与交付检查。
- `skills/ppt-master`：固定版本上游引擎，保留许可和来源。
- `examples/ai-work`：八页实际制作样稿、源材料、设计方案、可编辑 PPTX、逐页预览与检查记录。
- `manifest.json`：源码发布包文件校验清单，只覆盖源码包，不覆盖额外示例和本说明。
- `specs/`：已经确认、可复用的规格与设计决策；新对话从这里和历史记录恢复上下文。
- `PROJECT_HISTORY.md`：已完成工作、未验证边界和下一轮建议。

从 [个人技能说明](skills/personal-ppt/README_CN.md) 开始。正式制作使用任务级 `spec.md` 与 SDD 检查，规则见 [Specs 与 SDD](skills/personal-ppt/references/spec-sdd.md)。完整工作流和内网迁移步骤见 [制作与交付](skills/personal-ppt/references/production.md)，实际验收见 [样稿记录](examples/ai-work/制作与验收记录.md)。

用途可扩展，风格可复用；默认仅使用本地资料。公司品牌、模板和历史业务材料应保存在独立私有资料包。不要把模型密钥、公司参考材料或浏览器运行环境提交到公共仓库。

此版本已实际验证 Windows PowerPoint 的八页中文样稿生成与视觉检查。GLM + OpenCode 内网兼容性仍需在目标环境实跑。基线已同步至 GitHub；仓库级演进记录见 `PROJECT_HISTORY.md`。
