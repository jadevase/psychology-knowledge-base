# GitHub Actions 工作流说明

本目录包含两个自动化工作流，用于实现心理学知识库的完全自动化管理。

---

## 📋 工作流列表

### 1️⃣ daily-sync.yml - 每日自动同步

**触发时间**: 每天 UTC 9:30（北京时间 17:30）

**功能**:
- 自动生成当天的学习内容
- 生成配套的练习题
- 更新索引文件 `index.json`
- 自动提交到仓库

**工作流程**:
```yaml
每天 17:30 → 触发工作流
    ↓
运行 Python 同步脚本
    ↓
生成 daily-lessons/day-XXX.md
生成 practice-questions/day-XXX-questions.md
    ↓
更新 index.json (current_day + 1)
    ↓
Git 提交更改
    ↓
推送到 main 分支
    ↓
触发 Pages 部署工作流
```

**自定义配置**:

如果你想修改同步时间，编辑 `.github/workflows/daily-sync.yml`:

```yaml
schedule:
  # 当前：每天北京时间 17:30
  - cron: '30 9 * * *'
  
  # 改为其他时间（UTC 时间）：
  # 每天早上 8:00 → cron: '0 0 * * *'
  # 每天晚上 10:00 → cron: '0 14 * * *'
```

---

### 2️⃣ pages-deploy.yml - GitHub Pages 自动部署

**触发条件**: 每次推送到 `main` 分支

**功能**:
- 自动部署 `/docs` 文件夹到 GitHub Pages
- 生成静态网站
- 提供在线访问链接

**工作流程**:
```yaml
push to main → 触发工作流
    ↓
构建 Pages 站点
    ↓
部署到 gh-pages 分支
    ↓
发布到 https://jadevase.github.io/psychology-knowledge-base/
```

---

## 🔧 高级配置

### 手动触发同步

如果需要立即生成某一天的内容（不等待定时任务）：

1. 访问：https://github.com/jadevase/psychology-knowledge-base/actions
2. 选择 "Daily Sync" 工作流
3. 点击 "Run workflow"
4. 在输入框中填写要生成的天数（例如：`5`）
5. 点击 "Run workflow"

### 禁用自动同步

如果暂时不需要自动同步：

1. 访问：https://github.com/jadevase/psychology-knowledge-base/actions
2. 点击右上角的三个点 ⋯
3. 选择 "Disable workflow"

### 查看执行日志

每次工作流执行后都会生成详细日志：

1. 访问 Actions 标签
2. 点击具体的运行记录
3. 展开各个步骤查看详细输出

---

## 📊 监控和维护

### 检查同步状态

```bash
# 查看最近一次同步
git log --oneline -n 5

# 查看当前学习进度
cat index.json | jq '.current_day'
```

### 故障排查

如果自动同步失败：

1. **检查 Actions 日志**
   - 访问仓库的 Actions 标签
   - 找到失败的运行记录
   - 查看错误信息

2. **常见问题**
   - Python 依赖缺失 → 检查 `requirements.txt`
   - Git 配置问题 → 检查工作流中的用户配置
   - 文件冲突 → 检查是否有未提交的更改

3. **手动修复**
   - 在本地运行同步脚本测试
   - 手动提交修复后的文件
   - 重新启用工作流

---

## 🎯 最佳实践

### 1. 定期备份

虽然代码托管在 GitHub，仍建议定期备份到本地或其他云存储。

### 2. 使用 Issue 追踪

为每个学习阶段创建 Issue：
- 记录学习心得
- 标记难点和重点
- 与其他学习者讨论

### 3. 版本标签

每完成一个学习阶段，创建版本标签：

```bash
git tag -a v1.0-stage1 -m "完成基础心理学阶段"
git push origin v1.0-stage1
```

### 4. 贡献指南

如果想邀请他人共同维护：

1. 创建 `CONTRIBUTING.md` 文件
2. 说明如何提交 PR
3. 定义代码规范和内容标准

---

## 📚 相关文档

- `DEPLOYMENT_GUIDE.md` - 完整部署指南
- `QUICK_START.md` - 快速开始（针对 jadevase 用户）
- `USER_GUIDE.md` - 知识库使用指南
- `learning-plan.md` - 6 个月学习计划

---

**祝你学习愉快！** 📖✨
