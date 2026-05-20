# Positioning

## 核心定位

File Organizer 是一个证据驱动、懂用户偏好的智能文件整理高级顾问。

它确实是智能整理文件，但不是“AI 猜一个分类，然后 best effort 搬文件”。它的整理方式是：

```text
理解用户判断标准
-> 分析文件关系
-> 解释证据和风险
-> 生成专业报告
-> 生成安全整理方案
-> 用户或 agent 确认后执行
```

一句话给普通用户：

> AI 整理文件前，先帮你的文件夹做一次安全体检。看清哪些真的重复，哪些只是相似，哪些不能乱动，然后再安全整理。

一句话给高级用户和 agent：

> A preference-aware file organization advisor and runtime that turns file evidence, similarity, risk, and user policy into safe plans.

## 不是产品降级

这个定位不是把产品降级成小工具，而是把产品身份说清楚：

- 它仍然是智能文件整理。
- 它的高级之处是像顾问一样懂用户的整理哲学。
- 它先给证据和判断边界，再给整理动作。
- 它可以服务普通用户，也可以服务 power user、developer、archivist、data hoarder 和 AI agent。

不要把项目叙事写成“只是开源 infra”或“只是安全层”。底层确实可以作为 agent safety layer，但用户看到的产品应该是一个懂你的智能整理顾问。

## 两层“懂你”

### 基础用户：你讲清楚，AI 就会懂

基础用户不需要理解 `manifest`、`traversal policy`、`recursive fingerprint`、`similarity predicate`。

他们可以用自然语言表达偏好：

```text
这些照片只要看起来一样就算相似。
安装镜像不要乱删，只给我报告。
同一个项目的 zip，即使时间不同也先放一起给我看。
PDF 如果内容一样但文件名不同，算重复。
这个文件夹不要深入分析。
```

AI 的职责是把这些话翻译成可见、可改、可撤销的规则草案，而不是直接替用户执行含糊的操作。

### 高级用户：直接配置精确规则

高级用户可以在 settings 里直接编辑判断标准：

```text
image_similarity >= 0.92
archive_compare = manifest_only
iso_traversal = atomic
same_hash => equal
same_manifest + close_size => similar
risk_level >= 3 => require_confirmation
```

这些规则和自然语言生成的规则进入同一个 runtime，由同一套机制执行、解释和审计。

## 三层产品入口

### 第一层：普通用户

普通用户看到的是安全体检报告：

```text
扫描完成：

- 发现 12 组完全重复文件
- 发现 5 组高度相似文件
- 发现 3 个高风险整理项，不建议自动处理
- 发现 4 个压缩包疑似同一项目的不同版本
- 没有移动、删除、改名任何文件
```

按钮应该简单：

```text
查看原因
生成整理建议
导出报告
交给 Claude / ChatGPT 继续处理
```

### 第二层：进阶用户

进阶用户可以修正规则和 workflow：

```text
这些 ZIP 属于同一个项目。
这个文件夹不要递归分析。
这些 JPG 和 PNG 可以算相似。
这些 ISO 不要自动处理。
```

系统把这些决定写入 preference / policy，而不是只在一次对话中临时记住。

### 第三层：专家和 AI Agent

专家、开发者和 agent 使用 CLI / JSON / API：

```text
analyze
compare
report
safe-plan
```

这一层暴露：

- equal / similar / different / unknown / needs_more_analysis
- evidence
- confidence
- risk level
- traversal policy
- fingerprint
- journal
- safe plan

## 不做 best effort

项目口径里不要使用“best effort organize”作为目标。

规则：

- 证据不足就输出 `unknown` 或 `needs_more_analysis`。
- 风险高就明确标记风险。
- 需要用户偏好就停下来问。
- 无法证明的建议不能伪装成确定结论。
- 每个建议都要引用证据、规则和用户偏好来源。

“懂你的 AI”不是说 AI 可以大胆猜，而是它知道什么时候该解释、什么时候该确认、什么时候不能动。

## 与普通 AI sorter 的区别

普通 AI sorter 常见流程：

```text
AI 看文件
-> 猜分类或命名
-> 用户 review
-> 移动或重命名
-> undo
```

File Organizer 的流程：

```text
读取文件宇宙
-> 比较 equal / similar / version / container relation
-> 解释证据、风险和成本
-> 学习用户偏好
-> 生成报告
-> 生成安全整理方案
-> 用户或 agent 决定是否执行
```

它不是和 AI agent 抢“对话和执行”的入口。它应该成为 Claude、ChatGPT、Codex、本地 agent 在操作文件前可以调用的证据层、风险层和计划层。

## 近期产品判断

v0.1 不需要做完整消费级 App，也不需要先追求普通用户增长。

v0.1 应该证明这件事：

```text
1. exact duplicate analysis
2. similar candidate detection
3. ZIP/tar manifest comparison
4. evidence report
5. safe plan
6. agent-friendly JSON output
```

做完后只看三个问题：

1. 它能不能生成普通 AI sorter 生成不了的专业证据报告？
2. 它能不能让 Codex / Claude Code / 本地 agent 调用后少犯错？
3. 有没有 data hoarder / developer / archivist / power user 觉得它有用？

如果答案是 yes，就继续扩展。

