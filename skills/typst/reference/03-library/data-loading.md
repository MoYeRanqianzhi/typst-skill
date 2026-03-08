# Data Loading

## 用途

- 处理外部数据读取、结构化数据解析与输入桥接。

## 权威来源

- `typst/docs/reference/library/data-loading.md`
- `typst/crates/typst-library/src/loading/**`
- `typst/crates/typst-cli/src/args.rs`

## 重点对象

- `read`
- `json`、`csv`、`yaml`、`xml`、`toml`、`cbor`
- `sys.inputs`

## 使用建议

- 小型配置优先用 `sys.inputs`。
- 可复用或结构化数据优先用 JSON / YAML / CSV / TOML。
- 二进制或紧凑交换格式优先考虑 `bytes` 与 `cbor`。
- 需要稳定调试时，把数据文件与 Typst 文档一起放在明确 root 下。
