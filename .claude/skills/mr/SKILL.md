# MR Description Skill — Conventional Commits

## 触发条件
用户说「帮我写 MR」「生成 MR 描述」「写 merge request」「write MR」时使用本 skill。

---

## 第一步：收集信息

在写 MR 之前，先运行以下命令获取上下文：

```bash
# 获取当前分支与目标分支的 diff 摘要
git log origin/main..HEAD --oneline

# 获取文件变更列表
git diff origin/main..HEAD --stat

# 获取详细 diff（用于理解改动意图）
git diff origin/main..HEAD
```

如果用户已经提供了改动描述，跳过此步骤。

---

## 第二步：判断 commit type

根据改动内容，从下表选择 **一个** type：

| Type       | 使用场景                                      |
|------------|-----------------------------------------------|
| `feat`     | 新功能、新接口、新页面                        |
| `fix`      | Bug 修复                                      |
| `refactor` | 重构（不影响功能，不修 bug）                  |
| `perf`     | 性能优化                                      |
| `test`     | 新增或修改测试                                |
| `docs`     | 文档变更（README、注释、changelog）           |
| `style`    | 格式调整（空格、缩进、分号，不影响逻辑）      |
| `chore`    | 构建脚本、依赖更新、CI 配置                   |
| `ci`       | CI/CD 流水线配置                              |
| `revert`   | 回滚某次提交                                  |
| `build`    | 影响构建系统或外部依赖（webpack、npm 等）     |

**Breaking change**：若改动不向后兼容，在 type 后加 `!`，如 `feat!`，并在 footer 写 `BREAKING CHANGE: <说明>`。

---

## 第三步：输出 MR 模板

严格按照以下格式输出，**不要**省略任何 section，没有内容的 section 写 `N/A`。

---

```
## [type](scope): <简短描述，动词开头，不超过 72 字符，不加句号>

### 背景 / 动机
<!-- 为什么要做这个改动？解决了什么问题？ -->


### 改动内容
<!-- 做了什么，怎么做的。使用列表，每条以动词开头 -->
- 


### Breaking Changes
<!-- 是否有不向后兼容的改动？有则说明影响范围和迁移方式 -->
N/A

### 测试
<!-- 如何验证改动是正确的？单测 / 集成测试 / 手动测试步骤 -->
- [ ] 单元测试已通过
- [ ] 本地手动验证


### 截图 / 录屏
<!-- UI 改动必填，其余可选 -->
N/A

### 关联 Issue / Ticket
<!-- 填写关联的 issue 编号，格式：Closes #123 或 Refs #123 -->


### Checklist
- [ ] 代码已自审
- [ ] 文档已更新（如需要）
- [ ] 无调试代码残留
- [ ] 涉及数据库变更已附迁移脚本
```

---

## 标题规范（重要）

标题格式：`type(scope): description`

- `type`：见上表
- `scope`（可选）：改动模块，如 `auth`、`api`、`ui`、`db`
- `description`：
  - 使用**祈使句**（英文用动词原形，中文用动词开头）
  - 不超过 72 个字符
  - 结尾不加句号
  - 英文全小写

**示例标题：**
```
feat(auth): add OAuth2 login with GitHub
fix(api): handle null pointer in user endpoint
refactor(db): extract query builder to separate module
perf(search): replace linear scan with inverted index
chore: upgrade dependencies to latest stable
feat!: remove deprecated v1 API endpoints
```

---

## 输出语言规则

- 标题（title）：**与代码库主要语言一致**（英文代码库用英文，中文项目用中文均可）
- 正文（body）：**与用户对话语言一致**
- 若用户未说明，默认英文标题 + 中文正文

---

## 示例输出

**输入**：新增了一个用户登录接口，支持用户名密码和手机验证码两种方式。

**输出**：

```
## feat(auth): add login API supporting password and SMS OTP

### 背景 / 动机
当前系统缺少统一的登录入口，前端需要分别调用两套接口。本次将登录逻辑收拢至单一接口，统一鉴权流程。

### 改动内容
- 新增 `POST /api/v1/auth/login` 接口，支持 `password` 和 `sms_otp` 两种认证方式
- 实现 `SmsOtpAuthenticator` 类，封装短信验证码校验逻辑
- 为登录接口添加速率限制（60 次/分钟/IP）
- 新增单元测试覆盖两种认证路径及异常场景

### Breaking Changes
N/A

### 测试
- [x] 单元测试已通过（覆盖率 > 85%）
- [x] Postman 手动测试两种登录方式
- [ ] 待 QA 回归

### 截图 / 录屏
N/A

### 关联 Issue / Ticket
Closes #42

### Checklist
- [x] 代码已自审
- [x] API 文档已更新（Swagger）
- [x] 无调试代码残留
- [ ] 涉及数据库变更已附迁移脚本
```
