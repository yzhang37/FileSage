# Rules Draft

规则系统还未实现。这份文档定义预期方向，避免后续随意扩展。

## 设计目标

- 规则可读。
- 规则可测试。
- 规则有优先级。
- 每次命中规则都能输出原因。
- 冲突行为明确。

## 草案格式

```yaml
version: 1
defaults:
  recursive: false
  include_hidden: false
  conflict: rename

rules:
  - name: Screenshots
    when:
      name_matches: "^Screenshot"
      extension_in: [".png", ".jpg", ".jpeg"]
    then:
      category: Images/Screenshots

  - name: PDFs
    when:
      extension_in: [".pdf"]
    then:
      category: Documents/PDF

  - name: Old archives
    when:
      extension_in: [".zip", ".tar", ".gz"]
      older_than_days: 30
    then:
      category: Archives/Old
```

## 规则优先级

建议采用从上到下优先匹配：

1. 用户规则。
2. 项目内置高置信规则。
3. 通用扩展名分类。
4. `Other`。

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

AI 分类只能产生建议，不能绕过 dry-run 和确认流程。

建议输出：

- 建议类别。
- 置信度。
- 理由。
- 可替代类别。

