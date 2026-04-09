# 🚀 快速部署指南

**为你的 GitHub 账户（jadevase）定制**

---

## ⚡ 5 分钟完成部署

### 方式一：使用自动脚本（推荐）

#### 1️⃣ 运行部署脚本

在文件资源管理器中打开 `psychology-knowledge-base` 文件夹，双击运行：

```
setup-git.bat
```

脚本会自动完成以下操作：
- ✅ 配置 Git 用户信息
- ✅ 添加所有文件到仓库
- ✅ 提交初始版本
- ✅ 配置远程仓库地址
- ✅ 推送到 GitHub

#### 2️⃣ 输入 GitHub 凭据

当脚本提示时，输入：
- **用户名**: `jadevase`
- **密码**: 你的 GitHub 密码或**个人访问令牌**（推荐）

> 💡 **重要**：GitHub 从 2021 年起要求使用个人访问令牌（Personal Access Token）而非密码。
> 
> [如何生成个人访问令牌 →](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)

#### 3️⃣ 验证推送成功

看到以下提示表示成功：

```
✅ 部署成功！
========================================

你的知识库已上传到：
https://github.com/jadevase/psychology-knowledge-base
```

---

### 方式二：手动命令行部署

如果你更喜欢手动操作，请按以下步骤：

#### 1️⃣ 打开终端

在 `psychology-knowledge-base` 文件夹中右键 → "在终端中打开" 或使用 VS Code：

```bash
cd psychology-knowledge-base
```

#### 2️⃣ 初始化并配置 Git

```bash
# Git 已经初始化，跳过这步

# 配置用户信息
git config user.name "jadevase"
git config user.email "jadevase@users.noreply.github.com"

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit: 心理学知识库"

# 重命名分支为 main
git branch -M main

# 添加远程仓库
git remote add origin https://github.com/jadevase/psychology-knowledge-base.git

# 推送
git push -u origin main
```

---

## 🔧 后续配置

### 1️⃣ 启用 GitHub Actions

上传成功后，立即访问：

```
https://github.com/jadevase/psychology-knowledge-base/actions
```

点击 **"I understand my workflows, go ahead and enable them"**

这将激活每日自动同步功能（每天 17:30 自动生成新内容）。

### 2️⃣ 配置 GitHub Pages

访问：

```
https://github.com/jadevase/psychology-knowledge-base/settings/pages
```

按以下配置：
- **Source**: Deploy from a branch
- **Branch**: `main`
- **Folder**: `/docs`
- 点击 **Save**

等待约 1-2 分钟，页面会显示你的网站地址：

```
https://jadevase.github.io/psychology-knowledge-base/
```

### 3️⃣ 验证部署

访问以下链接确认一切正常：

| 检查项 | 链接 |
|--------|------|
| GitHub 仓库 | https://github.com/jadevase/psychology-knowledge-base |
| GitHub Actions | https://github.com/jadevase/psychology-knowledge-base/actions |
| 在线首页 | https://jadevase.github.io/psychology-knowledge-base/ |
| 第 1 天课程 | https://github.com/jadevase/psychology-knowledge-base/blob/main/daily-lessons/day-001.md |

---

## 🎯 部署完成后

### 每日自动流程

```
每天 17:00 → 钉钉推送学习内容
    ↓
每天 17:30 → GitHub Actions 自动同步
    ↓
自动生成新课程 → 提交到仓库 → 触发 Pages 更新
    ↓
你的网站自动显示最新内容 ✨
```

### 你可以

- ✅ 在手机/平板上随时访问知识库
- ✅ 分享链接给学习伙伴
- ✅ 查看完整的学习历史记录
- ✅ 通过 Issues 做笔记和问答

---

## ❓ 常见问题

### Q1: 推送时提示 "Permission denied"

**原因**：未配置正确的 GitHub 凭据

**解决方案**：
1. 生成个人访问令牌：https://github.com/settings/tokens
2. 权限勾选：`repo` (Full control of private repositories)
3. 复制令牌（只显示一次！）
4. 推送时使用令牌作为密码

### Q2: Git 命令找不到

**原因**：未安装 Git

**解决方案**：
1. 下载：https://git-scm.com/download/win
2. 安装后重启终端
3. 重新运行 `setup-git.bat`

### Q3: Actions 没有自动运行

**解决方案**：
1. 访问仓库的 Actions 标签
2. 点击 "Enable workflows"
3. 手动触发一次：Actions → Daily Sync → Run workflow

### Q4: Pages 页面显示 404

**原因**：Pages 尚未部署完成

**解决方案**：
1. 等待 2-3 分钟
2. 检查 Actions 中的 Pages 部署状态
3. 确认配置为 `main` 分支 + `/docs` 文件夹

---

## 📞 需要帮助？

如果遇到其他问题：

1. 查看完整文档：`DEPLOYMENT_GUIDE.md`
2. 检查 Git 状态：`git status`
3. 查看推送日志：`git log`

---

**祝你部署顺利！** 🎉

有任何问题随时告诉我。
