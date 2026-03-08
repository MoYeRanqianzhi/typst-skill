# Known Issues

## 上游资料不一致

- 中文蓝皮书存在 `0.11`、`0.12.0`、`0.13.1` 相关内容残留，不能直接视为当前官方基线。
- 蓝皮书在 CLI、包分发、Universe 生态方面不如官方文档完整。

## 索引系统现状

- 当前 Skill 同时维护 `reference/generated/` 综合索引与 `reference/08-generated/` 轻量官方 inventory。
- 若两个索引结果与原始源码不一致，必须回查 `typst/` 原始文件并以其为准。

## 自动索引的边界

- `refresh_typst_knowledge.py` 主要覆盖官方库 API、分组页与版本快照。
- `build_reference.py` 覆盖面更大，但依赖本地缓存与源码解析逻辑，仍不应替代原始上游源码。

## 仓库管理策略

- 根仓库仅跟踪 Skill 与 `docs/`，`typst/` 与 `The Raindrop-Blue Book/` 作为本地上游快照来源，不纳入本项目版本管理。
