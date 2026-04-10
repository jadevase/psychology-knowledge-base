# 🚀 快速参考卡片

## 每日同步流程

### 1️⃣ 学习完成后运行脚本
```bash
cd psychology-knowledge-base
python sync_to_knowledge_base.py
```

### 2️⃣ 查看生成的文件
- 📖 完整版：`daily-lessons/day-XXX-full.md`
- 📝 简版：`daily-lessons/day-XXX.md`
- ✍️ 习题：`practice-questions/day-XXX-questions.md`

### 3️⃣ 提交到 GitHub（可选）
```bash
git add .
git commit -m "chore: add Day XXX lessons"
git push
```

---

## 常用命令速查

| 任务 | 命令 |
|------|------|
| 同步下一天 | `python sync_to_knowledge_base.py` |
| 同步指定天数 | `python sync_to_knowledge_base.py 5` |
| 扫描现有课程 | `python scan_existing_lessons.py` |
| 查看帮助 | 阅读 `SYNC_GUIDE.md` |

---

## 文件位置速查

```
📁 psychology-knowledge-base/
├── 📖 daily-lessons/          # 每日课程
│   ├── day-001-full.md       # 完整版
│   └── day-001.md            # 简版
├── ✍️ practice-questions/     # 习题练习
│   └── day-001-questions.md
├── 🌐 index.html             # 网页导航
├── 📊 index.json             # 数据索引
└── 📚 SYNC_GUIDE.md          # 详细指南
```

---

## 学习阶段速查

| 阶段 | 天数 | 主题 |
|------|------|------|
| 1️⃣ | 1-30 | 基础心理学 |
| 2️⃣ | 31-60 | 发展心理学 |
| 3️⃣ | 61-90 | 社会心理学 |
| 4️⃣ | 91-120 | 咨询心理学 |
| 5️⃣ | 121-150 | 心理诊断与测量 |
| 6️⃣ | 151-180 | 操作技能 |

---

## 故障排除

| 问题 | 解决方案 |
|------|----------|
| 索引错误 | `python scan_existing_lessons.py` |
| HTML 未更新 | 删除 `index.html` 后重新运行 |
| 路径错误 | 确保在 `psychology-knowledge-base` 目录运行 |

---

## 在线访问

### GitHub 仓库
https://github.com/jadevase/psychology-knowledge-base

### 访问方式
1. **直接浏览**: 打开 `index.html` 查看导航
2. **GitHub Pages**: 部署后访问静态网站（需配置）

---

## 💡 提示

- ✅ 每天学习后立即同步
- ✅ 定期推送到 GitHub 备份
- ✅ 使用简版快速复习
- ✅ 结合习题巩固知识

---

**打印此卡片作为桌面参考！** 📌
