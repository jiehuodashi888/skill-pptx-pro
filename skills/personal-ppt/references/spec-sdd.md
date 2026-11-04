# Specs 与 SDD 工作流

本技能用“每个交付任务一份规格”的方式执行规格驱动开发（SDD）。规格不替代
`request.json`：前者说明要做什么、如何验收；后者固定已选择的 profile、style 与
本地资料哈希。二者和最终检查记录共同构成可复现的交付链路。

## 什么时候使用

每次新建 PPT、较大幅度重做现有 PPT、提炼公司模板，或新增 profile/style 时使用。
小的错字或单页微调可以记录在该任务的“Decisions and open questions”中，不必创建
新的规格。

## 流程

1. 选择 profile 和 style，并用 `init` 创建 job。
2. 执行 `spec-init`，生成 job 内的 `spec.md`。补全它：目标、听众、事实来源、逐页
   叙事、视觉约束、验收标准、开放问题与交付检查。
3. 与需求方审阅。确认后将 `Status: draft` 改为 `Status: approved`。若范围、受众、
   来源或模板发生实质变化，改回 `draft` 并记录理由。
4. 执行 `sdd-check`。只有输出 `ready_to_generate: true` 时才进入引擎生成阶段。
5. 依据规格制作、渲染、结构审计并逐页视觉检查。把实际结果和未解决问题写入 job
   的交付记录；更新 `request.json` 的状态时保留其最初的配置和资料哈希。
6. 把通用、已验证的学习沉淀到私有资料包（profile/style）或仓库 `specs/` 中。公司
   内容、模板和事实资料留在内网私有位置。

## 命令

```sh
python personal.py init --profile report --style clean --title "Q2 汇报" \
  --source /local/facts.md --output /local/jobs/q2-report
python personal.py spec-init --job /local/jobs/q2-report
# 编辑 /local/jobs/q2-report/spec.md，并在审阅后设为 Status: approved
python personal.py sdd-check --job /local/jobs/q2-report
```

`sdd-check` 会验证状态、必需章节和模板中尚未填写的关键字段，不能判断内容是否真实、
充分或已经获得业务批准。事实真实性、品牌授权和逐页视觉质量仍需人工负责。

## 规格的最小质量线

- 每页必须能回答“这页要让谁理解或决定什么”。
- 事实、假设与待补资料必须区分；没有本地来源的事实不得伪装为已核验。
- “风格”与“模板路径”分开记录。风格可指导重设计，模板路径才表示需要使用的文件。
- 验收标准要可观察，例如页数、目标受众、数据可编辑性、必要备注与视觉检查，而不是
  “看起来专业”。
- 交付前把 PowerPoint 渲染、PPTX 审计和每页视觉结论写入记录。
