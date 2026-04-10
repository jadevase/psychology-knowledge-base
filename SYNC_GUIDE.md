# 知识库同步脚本使用说明

## 📋 功能概述

`sync_to_knowledge_base.py` 是心理学知识库的自动同步脚本，用于生成和管理每日学习内容。

### 主要功能

1. ✅ **双版本生成**：同时生成完整版（约 25,000 字）和简版（核心要点）课程
2. ✅ **习题配套**：为每门课程生成 10 道选择题及详细解析
3. ✅ **索引更新**：自动更新 `index.json` 索引文件
4. ✅ **网页导航**：自动更新 `index.html`，实现 GitHub 网页访问导航
5. ✅ **阶段管理**：根据学习进度自动分配到对应阶段（基础心理学、发展心理学等）

## 🚀 使用方法

### 基本用法

```bash
# 同步下一天（基于当前进度自动计算）
python sync_to_knowledge_base.py

# 同步指定天数
python sync_to_knowledge_base.py 2

# 批量同步（例如同步第 5-10 天）
for i in {5..10}; do python sync_to_knowledge_base.py $i; done
```

### Windows 批处理

```batch
REM 同步第 2 天
python sync_to_knowledge_base.py 2

REM 批量同步多个天数
for /L %i in (2,1,10) do python sync_to_knowledge_base.py %i
```

## 📁 输出文件

每次运行脚本会生成以下文件：

```
psychology-knowledge-base/
├── daily-lessons/
│   ├── day-001-full.md       # 完整版课程
│   ├── day-001.md            # 简版课程
│   ├── day-002-full.md
│   └── day-002.md
├── practice-questions/
│   ├── day-001-questions.md
│   ├── day-002-questions.md
│   └── ...
├── index.json                # 结构化索引（自动更新）
└── index.html                # 网页导航（自动更新）
```

## 🔄 完整工作流

### 每日学习流程

1. **运行同步脚本**（每天学习后）
   ```bash
   python sync_to_knowledge_base.py
   ```

2. **查看生成的内容**
   - 完整课程：`daily-lessons/day-XXX-full.md`
   - 简版课程：`daily-lessons/day-XXX.md`
   - 习题练习：`practice-questions/day-XXX-questions.md`

3. **提交到 Git**（可选，如需同步到 GitHub）
   ```bash
   git add .
   git commit -m "chore: add Day XXX lessons"
   git push
   ```

4. **访问网页导航**
   - 在 GitHub 仓库中打开 `index.html`
   - 或通过 GitHub Pages 访问（如果已部署）

## 📊 学习阶段

脚本会自动将课程分配到对应的学习阶段：

| 阶段 | 天数范围 | 主题 |
|------|----------|------|
| 第一阶段 | Day 1-30 | 基础心理学 |
| 第二阶段 | Day 31-60 | 发展心理学 |
| 第三阶段 | Day 61-90 | 社会心理学 |
| 第四阶段 | Day 91-120 | 咨询心理学 |
| 第五阶段 | Day 121-150 | 心理诊断与测量 |
| 第六阶段 | Day 151-180 | 操作技能与综合应用 |

## 🔧 自定义配置

### 修改学习计划

编辑 `index.json` 中的 `studyPlan.stages` 部分：

```json
{
  "studyPlan": {
    "stages": [
      {
        "id": "stage-01",
        "name": "基础心理学",
        "days": "1-30",
        "topics": ["心理学概述", "感觉与知觉", ...]
      }
    ]
  }
}
```

### 调整内容生成器

在 `sync_to_knowledge_base.py` 中修改各阶段的内容生成方法：

- `_generate_basic_psychology_full()`: 基础心理学内容
- `_generate_developmental_psychology_full()`: 发展心理学内容
- `_generate_social_psychology_full()`: 社会心理学内容
- 等等...

## 🛠️ 故障排除

### 问题：索引文件错误

**症状**: `KeyError: 'stages'`

**解决方案**: 运行扫描脚本重建索引
```bash
python scan_existing_lessons.py
```

### 问题：HTML 导航未更新

**症状**: `index.html` 中没有显示最新课程

**解决方案**: 
1. 检查 `index.json` 是否包含最新课程记录
2. 重新运行同步脚本
3. 手动删除 `index.html` 后重新运行

### 问题：文件路径错误

**症状**: 生成的文件路径不正确

**解决方案**: 确保在正确的目录运行脚本
```bash
cd psychology-knowledge-base
python sync_to_knowledge_base.py
```

## 📝 最佳实践

1. **每天同步**: 建议每天学习后立即运行脚本，保持进度更新
2. **定期备份**: 定期将知识库推送到 GitHub 进行备份
3. **检查内容**: 生成的内容是模板，需要根据实际学习材料填充详细内容
4. **使用简版复习**: 利用简版课程进行快速复习和考前冲刺
5. **结合习题**: 完成课程后立即做习题，巩固知识点

## 🎯 示例输出

运行脚本后的典型输出：

```
============================================================
开始同步 Day 002 的学习内容
============================================================

步骤 1: 生成完整课程内容...
步骤 2: 生成简版课程内容...
步骤 3: 生成配套习题...
步骤 4: 保存到知识库...
✓ 已保存完整课程：...\daily-lessons\day-002-full.md
✓ 已保存简版课程：...\daily-lessons\day-002.md
✓ 已保存习题：...\practice-questions\day-002-questions.md
步骤 5: 更新索引文件...
✓ 已更新索引文件：...\index.json
步骤 6: 更新网页导航...
✓ 已更新导航页面：...\index.html

============================================================
✓ Day 002 同步完成！
============================================================

同步完成！🎉
```

## 📞 支持

如有问题或建议，请：
1. 查看本指南
2. 检查 `index.json` 配置
3. 联系知识库维护者

---

**最后更新**: 2026-04-10  
**版本**: 2.0
