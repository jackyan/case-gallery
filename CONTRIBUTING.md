# 贡献指南

感谢你想为本项目做出贡献！为了保证代码质量和协作效率，请遵循以下规范。

## 开发流程

1.  **Fork** 本仓库。
2.  创建一个新的分支进行开发：
    ```bash
    git checkout -b feature/your-feature-name
    # 或
    git checkout -b fix/your-bug-fix
    ```
3.  在本地环境中进行开发和测试。
4.  提交代码并推送到你的远程仓库。
5.  提交 **Pull Request (PR)** 到 `main` 分支。

## 代码规范

### Python
*   遵循 **PEP 8** 编码规范。
*   使用 `isort` 排序导入语句。
*   使用有意义的变量名和函数名。
*   为复杂的函数添加 Docstrings。

### HTML/CSS/JS
*   HTML 结构保持语义化。
*   CSS 尽量使用定义好的 CSS 变量（`var(--primary-color)` 等）。
*   JS 使用 ES6+ 语法。

## 提交信息规范 (Commit Messages)

请使用清晰、描述性的提交信息。推荐格式：

```
<Type>: <Subject>

<Body> (可选)
```

**Type 类型**:
*   `feat`: 新功能
*   `fix`: 修复 Bug
*   `docs`: 文档变更
*   `style`: 代码格式调整（不影响逻辑）
*   `refactor`: 重构
*   `test`: 测试用例
*   `chore`: 构建过程或辅助工具的变动

**示例**:
```
feat: 添加早餐投票功能
fix: 修复词云API返回空数据的问题
docs: 更新部署文档
```

## 问题反馈 (Issues)

如果你发现了 Bug 或有新的想法，欢迎提交 Issue。
*   **Bug**: 请提供复现步骤、环境信息和错误日志。
*   **Feature Request**: 请详细描述新功能的场景和价值。

感谢你的贡献！
