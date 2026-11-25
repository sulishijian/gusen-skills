# 谷神技能库

用于集中存放和维护 Codex 技能，按业务系统组织。

## 目录结构

```text
skills/
├── wms/                       # 仓储管理系统
│   └── example-skill/
│       ├── SKILL.md
│       ├── scripts/
│       ├── references/
│       └── assets/
└── tms/                       # 运输管理系统
```

## 收录技能

把每个技能放在 `skills/<系统名>/<技能名>/` 下。新增系统时，在 `skills/` 下创建以小写系统简称命名的目录。

每个技能目录包含 `SKILL.md`，在文件顶部的 YAML 元数据中填写 `name` 和 `description`。按需添加 `scripts/`、`references/` 和 `assets/`。

## 同步到 GitHub

新增或更新技能后，提交对应目录并推送。

```sh
git add skills/wms/example-skill
git commit -m "Add WMS example skill"
git push
```

提交前检查技能文件，避免将令牌、密码或个人配置写入仓库。
