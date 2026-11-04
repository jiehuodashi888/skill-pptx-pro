# 0001 — Personal PPT 基线

Status: accepted

## 目标

建立一套可迁移的个人 PPT 基础能力：通用生成、按用途选择内容结构、按视觉风格
重新设计，并能在未来带入公司内网持续演进。

## 已确认决定

- 使用 MIT 许可的 PPT Master 6.8.0（固定 commit `5e8856b`）作为同级底层引擎；
  个人扩展不修改其已跟踪源码。
- 个人入口为 `skills/personal-ppt`，用途 profile 与视觉 style 分离。
- 初始 profile：`general`、`report`、`learning-sharing`、`technical-solution`、
  `retrospective`；初始 style：`clean`、`editorial`。
- 默认闭环使用本地资料，不自动访问外网、上传材料或配置模型服务。
- 每个正式交付使用 job 内 `spec.md` 走 SDD：规格审阅并批准后才生成；完成后保留
  渲染、结构审计和逐页视觉检查证据。

## 边界

- 公司历史 PPT、品牌资产、模板和模型配置只放内网私有资料包。
- GLM + OpenCode 的实际兼容性尚未验证，必须在目标环境试跑。
- 原生数据图表、动画、外部图像、模板严格保真分别需要按具体任务验证。

## 验收证据

`examples/ai-work` 保存了一个八页中文通用样稿：已生成可编辑 PPTX、PowerPoint
逐页 PNG、PPTX 审计记录与人工逐页视觉结论。它验证的是本地 Windows 环境下的基础
链路，不代表任意公司模板或内网环境已经通过。
