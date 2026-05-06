# Contributing

感谢参与 File Organizer。这个项目处理用户文件，因此贡献时请优先考虑安全性、可预览性和可回滚性。

## 本地开发

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
PYTHONPATH=src python3 -m unittest discover -s tests
```

## 提交前检查

```bash
PYTHONPATH=src python3 -m unittest discover -s tests
python3 -m compileall src tests
```

## 贡献原则

- 优先补测试，再改行为。
- 所有真实文件移动能力都必须支持 dry-run。
- 不覆盖、不删除、不猜测用户意图。
- 新增规则或分类能力时，写清楚优先级和冲突行为。
- 文档和代码一起改，避免文档漂移。

## 分支建议

```text
feature/rule-engine
feature/journal
fix/conflict-destination
docs/product-spec
```

