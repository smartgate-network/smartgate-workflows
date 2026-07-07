# smartgate-workflows

SmartGate 生态下的**场景化 workflow 集合**——用 YAML + Markdown 声明式描述真实用户场景（如「调研竞品」），欢迎社区贡献。

## Workflows

| Workflow | 说明 |
|----------|------|
| [research-agent](workflows/research-agent/) | 无明确 URL 时的多源调研：搜索 → 批量抓取 → 去重 → 压缩 |
| [deep-reading](workflows/deep-reading/) | 已知单个 URL 的精读：抓取 → 压缩 |
| [remember-and-recall](workflows/remember-and-recall/) | 团队长期记忆的存取（add / search / get / delete） |
| [usage-report](workflows/usage-report/) | 查询团队 token 额度与使用记录（管理类，不生产内容） |

## 这不是运行时代码

本仓库只包含 workflow **声明**（`SKILL.md` + `pipeline.yaml`）。实际执行需配合：

- [smartgate-mcp](https://github.com/smartgate-network/smartgate-mcp) — MCP 工具网关
- smartgate-cli —（规划中）读取本仓库并调用 `smart_pipe`

### 运行时契约

| `template` | Loader 行为 | yaml `steps` 角色 |
|------------|-------------|-------------------|
| `read` / `research` / `remember` | `smart_pipe(template=…, params…)` | 文档 + CI 校验 |
| `custom` | `smart_pipe(steps=yaml.steps, …)` | 可执行契约 |

详见各 workflow 的 `pipeline.yaml`。

## 目录结构

```
smartgate-workflows/
├── workflows/          # 各场景 workflow
├── schema/             # pipeline.yaml / SKILL.md JSON Schema
├── _template/          # 新 workflow 模板
├── tests/fixtures/     # primitive 响应结构示例
└── .github/            # CI 与 PR 模板
```

## 贡献

请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。新增 workflow 从 `_template/` 复制，并更新 [ROUTING.md](ROUTING.md)。

## License

[MIT](LICENSE)
