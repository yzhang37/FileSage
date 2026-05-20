# Rules And Policy Draft

规则系统还未实现。这份文档定义 File Organization Runtime 的 policy 方向，避免后续把规则降级成简单的“按扩展名分类”。

规则不是 UI 的临时状态。自然语言 advisor 生成的规则草案、高级 settings 手写的规则、workflow 模板和用户 review decisions 最终都要进入同一个 runtime policy。

## 设计目标

- 规则可读。
- 规则可测试。
- 规则有优先级。
- 每次命中规则都能输出原因。
- 冲突行为明确。
- 规则能表达 equal / similar / unknown / needs_more_analysis。
- 规则能表达容器 traversal policy。
- 规则能表达风险等级和确认要求。
- 规则能引用用户偏好和 review decisions。
- 规则可导出、可回滚、可在报告中引用。

## 两种入口

### 自然语言入口

基础用户可以说：

```text
这些照片看起来一样就算相似，但不要自动删除。
ISO 只做报告，不要递归展开。
同 hash 文件可以算完全重复。
这个项目文件夹里的 zip 只比较清单。
```

AI 把这些话转换成规则草案，用户确认后进入 policy。

### 高级 settings 入口

高级用户可以直接写：

```yaml
policies:
  - name: Exact duplicate by hash
    when:
      same_content_hash: true
    then:
      relation: equal
      confidence: 1.0

  - name: Similar image by perceptual hash
    when:
      media_type: image
      phash_distance_lte: 8
    then:
      relation: similar
      action: report_only

  - name: ISO as atomic
    when:
      extension_in: [".iso"]
    then:
      traversal: atomic
      action: report_only
      risk: medium
```

两种入口必须编译到同一个 runtime policy。

## 草案格式

```yaml
version: 1
defaults:
  recursive: false
  include_hidden: false
  conflict: rename
  uncertainty: explicit
  destructive_actions: require_confirmation

policies:
  - name: Exact duplicates
    when:
      same_content_hash: true
    then:
      relation: equal
      evidence: content_hash
      confidence: 1.0

  - name: Similar archives by manifest
    when:
      container_type_in: ["zip", "tar"]
      same_manifest_fingerprint: true
      close_size_ratio_lte: 0.03
    then:
      relation: similar
      evidence: archive_manifest
      action: report_only

  - name: Installer images
    when:
      extension_in: [".iso"]
      ai_label_in: ["windows_installer", "game_installer", "software_installer"]
    then:
      traversal: manifest
      relation: needs_more_analysis
      action: require_review
      risk: high
```

## 规则优先级

建议采用从上到下优先匹配：

1. 用户显式 settings。
2. 用户确认过的 review decisions。
3. 自然语言 advisor 生成并被确认的规则。
4. 项目内置高置信规则。
5. workflow 模板。
6. 通用 fallback。

如果规则冲突，runtime 必须报告冲突并解释采用了哪条规则。

## 不确定性协议

规则不能用 best effort 掩盖不确定性。

可用状态：

- `equal`
- `similar`
- `different`
- `unknown`
- `needs_more_analysis`
- `require_confirmation`

当证据不足时：

```yaml
then:
  relation: unknown
  reason: insufficient_evidence
  next: ask_user
```

当需要更深分析时：

```yaml
then:
  relation: needs_more_analysis
  next: recursive_manifest_scan
  estimated_cost: medium
```

## 冲突策略

默认策略是 `rename`：

```text
report.pdf
report (1).pdf
report (2).pdf
```

未来可选策略：

- `skip`: 保留原位置。
- `rename`: 生成唯一目标名。
- `replace`: 仅在明确开启且 journal 可回滚时允许。

## AI 分类边界

AI 只能产生建议或规则草案，不能绕过 runtime、dry-run、journal 和确认流程。

建议输出：

- 建议类别。
- 置信度。
- 理由。
- 可替代类别。
- 对应规则草案。
- 影响范围。
- 风险等级。
- 是否需要用户确认。

## Review Decisions

用户 review decision 是“懂你”的核心材料。

示例：

```yaml
review_decision:
  id: rd_001
  user_decision: similar
  scope: "*.jpg, *.png"
  rationale: "visual match is enough for photo grouping, but do not auto-delete"
  generated_policy:
    when:
      media_type: image
      visual_similarity_gte: 0.94
    then:
      relation: similar
      action: report_only
```

review decisions 必须可查看、可编辑、可撤销。
