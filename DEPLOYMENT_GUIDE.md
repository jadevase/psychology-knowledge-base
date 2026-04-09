# 🚀 心理学知识库 GitHub 部署指南

本指南将帮助你把心理学知识库部署到 GitHub，实现线上访问和自动同步。

---

## 📋 准备工作

### 必需条件

- ✅ 拥有 GitHub 账号（如果没有，请前往 [github.com](https://github.com) 注册）
- ✅ 安装 Git（可选，用于本地管理）
- ✅ 本知识库的完整文件

### 预计用时

- 初次部署：15-20 分钟
- 日常使用：无需操作，自动同步

---

## 步骤一：创建 GitHub 仓库

### 1.1 登录 GitHub

访问 [github.com](https://github.com) 并登录你的账号。

### 1.2 创建新仓库

1. 点击右上角 **+** → **New repository**
2. 填写仓库信息：
   - **Repository name**: `psychology-knowledge-base`
   - **Description**: `心理咨询师考试自学知识库 - 180 天系统化学习路径`
   - **Visibility**: 选择 **Public**（公开，推荐）或 Private（私有）
   - **Initialize this repository with**: 暂时不勾选任何选项
3. 点击 **Create repository**

### 1.3 记录仓库 URL

创建成功后，你会看到类似这样的 URL：
```
https://github.com/yourusername/psychology-knowledge-base
```

---

## 步骤二：上传知识库文件

### 方式 A：通过网页上传（推荐新手）

适合首次部署，简单直观。

#### 2.A.1 上传文件

1. 在仓库页面，点击 **uploading an existing file**
2. 将本地 `psychology-knowledge-base/` 目录下的所有文件拖拽到上传区域
   - ✅ 必需文件：`README.md`, `index.json`, `daily-lessons/`, `practice-questions/`
   - ✅ 配置文件：`.github/workflows/`, `.gitignore`, `LICENSE`
   - ✅ 文档文件：`USER_GUIDE.md`, `learning-plan.md`
3. 等待上传完成

#### 2.A.2 提交更改

1. 在 **Commit changes** 区域填写：
   - Commit message: `Initial commit: 心理学知识库基础结构`
2. 点击 **Commit changes**

### 方式 B：通过 Git 命令行上传（推荐开发者）

适合有 Git 经验的用户，便于后续管理。

#### 2.B.1 初始化本地 Git 仓库

```bash
# 进入知识库目录
cd psychology-knowledge-base

# 初始化 Git 仓库
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit: 心理学知识库基础结构"
```

#### 2.B.2 关联远程仓库并推送

```bash
# 添加远程仓库（替换为你的仓库 URL）
git remote add origin https://github.com/yourusername/psychology-knowledge-base.git

# 推送到 GitHub
git branch -M main
git push -u origin main
```

---

## 步骤三：配置 GitHub Actions 自动同步

### 3.1 启用 GitHub Actions

1. 进入你的仓库页面
2. 点击 **Actions** 标签
3. 如果是第一次使用，会看到欢迎页面
4. 点击 **I understand my workflows, go ahead and enable them**

### 3.2 验证工作流

1. 在 **Actions** 页面，你应该能看到 **Daily Psychology Lesson Sync** 工作流
2. 工作流状态应该是绿色的 ✓（如果已触发）或灰色（等待下次执行）
3. 可以手动触发测试：
   - 点击工作流名称
   - 点击 **Run workflow** 按钮
   - 选择分支（main）
   - 点击 **Run workflow**

### 3.3 查看执行日志

1. 在工作流页面，点击具体的运行记录
2. 展开各个步骤查看详细日志
3. 确认没有错误（所有步骤显示绿色 ✓）

---

## 步骤四：配置 GitHub Pages 在线浏览

### 4.1 启用 GitHub Pages

#### 方式 A：使用 GitHub Actions 部署（推荐）

已在仓库中配置了自动部署工作流 `pages-deploy.yml`，它会在每次推送时自动部署到 GitHub Pages。

#### 方式 B：手动配置 Pages

1. 进入仓库 **Settings** → **Pages**
2. 在 **Source** 下选择：
   - Branch: `main`
   - Folder: `/docs`
3. 点击 **Save**

### 4.2 访问你的网站

部署成功后（约 1-2 分钟），你会看到类似这样的 URL：

```
https://yourusername.github.io/psychology-knowledge-base/
```

或

```
https://yourusername.github.io/psychology-knowledge-base/docs/
```

点击即可在线浏览知识库内容！

### 4.3 自定义域名（可选）

如果想使用自己的域名：

1. Settings → Pages → Custom domain
2. 输入你的域名（如 `psychology.yourdomain.com`）
3. 按照提示配置 DNS 解析

---

## 步骤五：验证部署成功

### ✅ 检查清单

- [ ] GitHub 仓库已创建，文件已上传
- [ ] README.md 能正常预览
- [ ] GitHub Actions 工作流已启用
- [ ] 手动触发工作流执行成功
- [ ] GitHub Pages 网站可访问
- [ ] index.json 中的进度数据正确显示

### 测试方法

1. **查看仓库页面**
   ```
   https://github.com/yourusername/psychology-knowledge-base
   ```

2. **查看 Actions 执行**
   ```
   https://github.com/yourusername/psychology-knowledge-base/actions
   ```

3. **访问 Pages 网站**
   ```
   https://yourusername.github.io/psychology-knowledge-base/
   ```

---

## 日常使用流程

### 自动同步（推荐）

配置完成后，每天会自动执行：

```
每天 17:30 (北京时间)
    ↓
GitHub Actions 触发
    ↓
生成当日学习内容
    ↓
自动提交到仓库
    ↓
GitHub Pages 自动更新
    ↓
你在钉钉收到学习推送
```

**你只需要：**
- ✅ 每天下午 5 点查看钉钉推送
- ✅ 打开 GitHub Pages 网站开始学习
- ✅ 完成练习题

### 手动同步（如需补学）

如果需要手动生成某一天的内容：

#### 方式 A：使用 GitHub Actions

1. Actions → Daily Psychology Lesson Sync → Run workflow
2. 在弹窗中添加参数（如果需要指定天数）
3. 点击运行

#### 方式 B：本地生成后推送

```bash
# 本地运行同步脚本
python sync_simple.py 5  # 生成第 5 天内容

# 提交并推送
git add .
git commit -m "feat: 手动生成第 5 天学习内容"
git push origin main
```

---

## 常见问题解答

### Q1: GitHub Actions 没有自动执行？

**A:** 检查以下几点：
1. Actions 是否已启用（首次使用需要手动确认）
2. 查看仓库 Settings → Actions → General，确保 Actions 未被禁用
3. 检查 cron 表达式时区是否正确（UTC 时间 9:30 = 北京时间 17:30）

### Q2: GitHub Pages 显示 404？

**A:** 可能的原因：
1. 部署尚未完成，等待 1-2 分钟
2. 配置的路径不正确，确认 Source 设置为 `main` branch + `/docs` folder
3. `docs/index.html` 文件不存在，检查文件是否上传

### Q3: 如何修改学习进度？

**A:** 直接编辑 `index.json` 文件：
```json
{
  "current_day": 10,  // 修改这里
  "total_lessons": 10  // 修改这里
}
```
然后提交更改即可。

### Q4: 可以离线学习吗？

**A:** 可以！有两种方式：
1. **克隆仓库到本地**：`git clone https://github.com/yourusername/psychology-knowledge-base.git`
2. **下载 ZIP**：仓库页面 → Code → Download ZIP

### Q5: 如何分享给我的朋友？

**A:** 
1. 分享 GitHub 仓库链接
2. 分享 GitHub Pages 网站链接
3. 邀请他们 Watch 或 Star 你的仓库

---

## 高级配置（可选）

### 添加钉钉机器人集成

如果想让 GitHub 更新时自动通知钉钉：

1. 在钉钉创建机器人 Webhook
2. 在 GitHub Actions 中添加钉钉通知步骤：

```yaml
- name: Notify DingTalk
  run: |
    curl 'https://oapi.dingtalk.com/robot/send?access_token=YOUR_TOKEN' \
      -H 'Content-Type: application/json' \
      -d '{
        "msgtype": "markdown",
        "markdown": {
          "title": "今日学习内容已更新",
          "text": "## 今日学习已就绪\n\n第${{ steps.progress.outputs.next_day }}天学习内容已生成，快去查看吧！\n\n[立即学习](https://yourusername.github.io/psychology-knowledge-base/)"
        }
      }'
```

### 添加学习统计图表

可以使用 GitHub Insights 或第三方工具（如 Wakatime）追踪学习时间。

---

## 下一步计划

完成 GitHub 部署后，你可以：

1. ✅ **开始第二步：钉钉集成**
   - 将知识库导入钉钉文档
   - 配置 AI 助理进行问答
   
2. 📊 **增强功能**
   - 添加学习打卡功能
   - 创建学习社区
   - 分享学习心得

3. 🎯 **专注学习**
   - 按照 180 天计划稳步前进
   - 每天完成学习内容和练习
   - 定期复习和总结

---

## 获取帮助

遇到问题？

- 📖 查看 [USER_GUIDE.md](USER_GUIDE.md) 了解使用方法
- 💬 在 GitHub Issues 中提问
- 📧 联系作者：朱湛锋

---

**祝你部署顺利，学习进步！** 🎉
