# Commit skill — Conventional Commits

## 触发条件
用户说「帮我 commit」「生成 commit」「写 commit message」「commit 一下」时使用本 skill。

---

## 第一步：分析当前改动

```bash
git diff --cached --stat
git diff --cached
git status
```

暂存区为空时再查工作区：`git diff --stat`

---

## 第二步：决定暂存范围

一个 commit 只做一件事，不要把 feat + fix 混在一起。

改动涉及多个不相关功能时，分多次 commit：

```bash
git add src/auth/login.py tests/test_login.py  # 指定文件
git add -p                                      # 交互式，复杂改动推荐
git add -A                                      # 仅当改动确实只做一件事
```

---

## 第三步：构造 commit message

格式：

```
<type>(<scope>): <description>

[body]

[footer]
```

### Type

| Type       | 场景                              |
|------------|-----------------------------------|
| feat       | 新功能                            |
| fix        | Bug 修复                          |
| refactor   | 重构（不改功能，不修 bug）        |
| perf       | 性能优化                          |
| test       | 新增或修改测试                    |
| docs       | 文档或注释                        |
| style      | 格式（空格缩进，不影响逻辑）      |
| chore      | 构建脚本、依赖更新                |
| ci         | CI/CD 配置                        |
| revert     | 回滚                              |
| build      | 构建系统或外部依赖                |

### 标题规范

- 动词开头，祈使句（英文原形：add 不是 added）
- 不超过 72 字符，结尾不加句号
- Breaking change 在 type 后加 !，如 feat!

### Body

解释为什么，而不是做了什么（代码本身说明做了什么）。

### Footer

```
Closes #123
BREAKING CHANGE: 说明影响范围和迁移方式
```

---

## 第四步：直接执行，不等确认

```bash
git commit -m "type(scope): description" -m "body（如有）"
```

message 较长时：

```bash
git commit -F - << 'MSG'
feat(auth): add OAuth2 login with GitHub

支持用户通过 GitHub 账号一键登录，减少注册摩擦。

Closes #88
MSG
```

---

## 第五步：告知结果

```
已提交：<标题>
hash：<前 7 位>
改动：<N> 个文件

推送：git push origin <当前分支>
```

---

## 典型示例

简单新功能：
```bash
git add src/api/user.py
git commit -m "feat(api): add GET /users/:id endpoint"
```

Bug 修复带说明：
```bash
git add src/auth/token.py
git commit -m "fix(auth): prevent token reuse after logout" \
           -m "退出后将 token 加入黑名单，Closes #102"
```

Breaking change：
```bash
git commit -m "feat!(api): remove deprecated v1 endpoints" \
           -m "BREAKING CHANGE: /api/v1/* 已移除，请迁移至 /api/v2/*"
```

多个无关改动，拆分提交：
```bash
git add src/utils/date.py
git commit -m "fix(utils): correct timezone offset in date formatter"

git add src/components/DatePicker.vue
git commit -m "feat(ui): add date range picker component"
```

---

## 禁止事项

- 不生成 Auto-save、WIP、temp、fix bug 等无意义 message
- 不无脑 git add -A，先检查 diff 再决定范围
- 发现暂存区有敏感信息（密钥、密码），先提醒用户加 .gitignore 再 commit
