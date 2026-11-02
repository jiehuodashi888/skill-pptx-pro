<!-- ppt-master-schema: design-spec/v1 -->
# AI at Work - Design Spec

## I. Project Information
| Item | Value |
| --- | --- |
| Project Name | AI at Work |
| Canvas Format | PPT 16:9, 1280 × 720 |
| Page Count | 8 |
| Primary Language | zh-CN |
| Target Audience | 办公团队成员 |
| Communication Intent | 解释可复用的草稿与核验流程，并推动小范围试用 |
| Desired Audience Outcome | 能选择一个任务，写清要求并核验输出 |
| Core Message / Ask / Action | 把重复工作交给草稿流程，把判断留给人 |
| Delivery Context | 8 分钟现场分享，兼顾会后阅读 |
| Artifact Afterlife | 可编辑、可复用的工作参考 |
| Reading Mode | balanced |
| Content Strategy | 按原创案例材料组织，不添加外部统计 |
| Design Style | 清爽专业，排版随页面任务变化 |
| AI Image Acquisition Path | not applicable |
| Generation Mode | continuous |
| Spec Refinement | disabled |
| Speaker Notes | enabled — workflow default |
| Custom Animations | disabled — agent-selected test policy |
| Narration Audio | disabled — agent-selected test policy |
| Created Date | 2026-11-02 |

## II. Canvas Specification
| Property | Value |
| --- | --- |
| Format | PPT 16:9 |
| Dimensions | 1280 × 720 |
| viewBox | `0 0 1280 720` |
| Margins | 64 px |
| Content Area | x 64–1216, y 56–640 |

## III. Visual Theme
### Theme Style
- **Mode**: custom
- **Mode Behavior**: 先选择任务，再解释流程，通过提示词示例练习，最后核验并安排试用。
- **Visual style**: custom
- **Visual Style Behavior**: 浅底深蓝正文，以蓝色标记重点，使用大标题、细分隔线和开放版面；对照页成对排列，流程页按阅读顺序排列。
- **Theme**: 可编辑的办公参考，以数字章节标记维持跨页识别。
- **Tone**: 清楚、务实

### Color Scheme
| Role | HEX | Purpose |
| --- | --- | --- |
| Background | #F7F9FC | 页面背景 |
| Secondary background | #EAF0FC | 示例区域 |
| Primary | #172B4D | 标题 |
| Accent | #2463EB | 重点 |
| Secondary accent | #FFFFFF | 深色区文字 |
| Body text | #172B4D | 正文 |
| Secondary text | #53657D | 注释 |
| Divider | #C7D3E3 | 分隔线 |

## IV. Typography System
### Font Plan
| Role | Character (Reference) | Primary | English if non-English | Fallback tail |
| --- | --- | --- | --- | --- |
| Title | bold sans | Microsoft YaHei | Arial | sans-serif |
| Body | neutral sans | Microsoft YaHei | Arial | sans-serif |
- **Title stack**: Microsoft YaHei, Arial
- **Body stack**: Microsoft YaHei, Arial

### Font Size Hierarchy
| Purpose | Anchor Size (px) |
| --- | ---: |
| Body | 28 |
| Title | 44 |
| Subtitle | 34 |
| Annotation | 20 |
| Display | 64 |
| Index | 24 |

## V. Layout Principles
### Deck-wide Direction
- **Hierarchy direction**: 标题说明主题，正文给出可操作内容，注释明确示例边界。
- **Composition tendency**: 根据主张、顺序、对照和清单选择不同构图。
- **Cross-page continuity**: 蓝色章节标记与深蓝标题，封面和结尾降低信息密度。
- **Spacing posture**: dense 内容页与 anchor 首尾交替。
- **Spacing anchors**: page margin 64; block gap 24; column gutter 48; corner radius 0; body leading 44 px.

## VI. Icon Usage Specification
- **Primary bundled library**: none
| Icon Path | Suitable Scenarios |
| --- | --- |

## VIII. Image Resource List
| Filename | Dimensions | Ratio | Purpose | Type | Image pattern | Crop Policy | Acquire Via | Status | Reference | text_policy | page_role |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

## IX. Content Outline
### Part 1: 工作方法

#### Slide 01 - 团队如何用 AI 提升日常工作效率
- **Audience move**: 从抽象兴趣到理解草稿与判断的分工。
- **Relationships**: 草稿流程与人工判断的分工 contrast。
- **Composition**: 大标题和简短主张。
- **Title**: 团队如何用 AI 提升日常工作效率
- **Core message**: 把重复工作交给草稿流程，把判断留给人。
- **Content**: 通用工作方法；选择任务、明确要求、核验结果。
- **Cover impact**: 把判断留给人；主张作为醒目副标题。

#### Slide 02 - 适合先尝试的任务
- **Audience move**: 从泛化应用到能选择低风险任务。
- **Relationships**: 材料归纳、初稿整理、格式转换 membership；无参考答案的判断 contrast。
- **Composition**: 三行任务清单与底部边界说明。
- **Title**: 适合先尝试的任务
- **Core message**: 优先选择有材料、有标准、可复核的工作。
- **Content**: 材料归纳：整理已有信息；初稿整理：形成可修改的草稿；格式转换：按要求重排。无参考答案的判断需要谨慎。数据仅在获准环境使用。

#### Slide 03 - 一次完整的协作流程
- **Audience move**: 从单次问答到掌握可核验的工作顺序。
- **Relationships**: 明确任务、提供材料、生成草稿、人工核验、保存方法 order；核验不通过返回调整要求 link。
- **Composition**: 横向编号步骤加下方复核反馈说明。
- **Title**: 一次完整的协作流程
- **Core message**: 核验通过后才能交付。
- **Content**: 明确任务；提供材料；生成草稿；人工核验；保存可复用方法。核验不通过就调整要求并重新生成。

#### Slide 04 - 一条可执行的提示词
- **Audience move**: 从随口提问到写出结构明确的请求。
- **Relationships**: 任务、材料、输出格式、约束和验收标准 membership。
- **Composition**: 左侧组成要素，右侧完整示例。
- **Title**: 一条可执行的提示词
- **Core message**: 把用途、依据和完成标准写清楚。
- **Content**: 把给定会议记录整理为待办清单。仅使用记录中的事实。列出事项、负责人、截止时间。缺失信息标为待确认。检查每个事项是否能追溯到原文。

#### Slide 05 - 同一任务的两种表达
- **Audience move**: 从知道要素到看出模糊请求的缺口。
- **Relationships**: 模糊请求与明确请求 contrast。
- **Composition**: 成对对照，右侧更大。
- **Title**: 同一任务的两种表达
- **Core message**: 明确用途、表头和事实边界，更方便检查结果。
- **Content**: 模糊：帮我总结会议。明确：按待办用途整理，列出事项、负责人、截止时间，只用记录事实，缺失项待确认。示例对照，不是效果测评。

#### Slide 06 - 交付前的四项核验
- **Audience move**: 从接受草稿到逐项检查交付质量。
- **Relationships**: 数字、依据、未知、格式 membership。
- **Composition**: 四项编号与简短核验动作。
- **Title**: 交付前的四项核验
- **Core message**: 使用者对最终交付负责。
- **Content**: 数字对应原文；结论有依据；遗漏和未知明确标出；格式可直接使用。未通过时回到材料和要求修订。

#### Slide 07 - 两周试用安排
- **Audience move**: 从理解方法到能组织小范围试用。
- **Relationships**: 第一周记录原流程、第二周比较结果 order。
- **Composition**: 两阶段顺序与底部评价维度。
- **Title**: 两周试用安排
- **Core message**: 先保证质量，再比较耗时和返工。
- **Content**: 第一周选择一个重复任务，保留原流程记录；第二周比较耗时、返工和结果可用性。只有通过质量检查的输出才纳入比较。
- **Data class**: scenario — 两周为建议安排，不是实测结果。

#### Slide 08 - 从一个重复任务开始
- **Audience move**: 从计划到明确下一次尝试需要保留的记录。
- **Relationships**: 输入、提示词、核验记录、最终版本 membership。
- **Composition**: 大号行动标题与记录要素。
- **Title**: 从一个重复任务开始
- **Core message**: 保存可复用方法，每次使用仍需检查。
- **Content**: 保留输入、提示词、核验记录和最终版本。下一次复用时仍需检查。
- **Closing impact**: 选一个任务，完成一次可核验的交付。

## X. Speaker Notes Requirements
- **Generation**: enabled
- **Filename**: match each SVG filename under notes/
- **Content**: 解释本页，不添加效果统计；说明原创案例和建议安排。
- **Total duration**: 8 minutes
- **Notes style**: conversational
- **Presentation purpose**: 解释工作流程并支持小范围试用
