# Contributing to smartgate-workflows

感谢贡献！本仓库是纯内容型项目（YAML + Markdown），**不需要修改任何业务代码**。

## 添加新 workflow

1. 复制 `_template/` 下的文件到 `workflows/<your-workflow-name>/`
2. 填写 `SKILL.md`（必须含 Purpose / When to use / When NOT to use / Returns / Composes with 五节）
3. 填写 `pipeline.yaml`（见 `schema/pipeline.schema.json`）
4. 至少添加一个 `examples/*.md` 具体案例
5. 更新 [ROUTING.md](ROUTING.md)，说明与现有 workflow 的边界

## Primitive 白名单

`pipeline.yaml` 中 `steps[].tool` **只能是**以下 7 个 primitive：

- `smart_fetch`
- `smart_search`
- `smart_context_gate`
- `smart_dedup`
- `smart_budget_guard`
- `smart_memory`
- `smart_pipe`

**不接受**在本仓库定义新 primitive。如有需求，请至 [smartgate-sdk](https://github.com/smartgate-network/smartgate-sdk) 提 issue。

## Pull Request 要求

- [ ] 已更新 [ROUTING.md](ROUTING.md)
- [ ] 已提供至少一个 `examples/*.md`
- [ ] `pipeline.yaml` 通过 schema 校验（CI 自动运行）
- [ ] 未引入 7 个 primitive 之外的新 tool

## 本地校验

```bash
pip install jsonschema pyyaml
python tests/validate.py
```

与 GitHub Actions 使用同一脚本。
