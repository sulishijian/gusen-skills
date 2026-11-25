# 谷神技能库

用于集中存放和维护 Codex 技能。

## 收录技能

把每个技能放在 `skills/<技能名>/` 下。目录内包含 `SKILL.md`，在文件顶部的 YAML 元数据中填写 `name` 和 `description`。技能需要的脚本、参考资料和静态资源可以放在同一目录。

```text
skills/
└── example-skill/
    ├── SKILL.md
    ├── scripts/
    ├── references/
    └── assets/
```

## 同步到 GitHub

新增或更新技能后，提交对应目录并推送。

```sh
git add skills/example-skill
git commit -m "Add example-skill"
git push
```

提交前检查技能文件，避免将令牌、密码或个人配置写入仓库。
