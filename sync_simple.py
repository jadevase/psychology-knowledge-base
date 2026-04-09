"""
心理学知识库自动同步脚本 - 简化版
用于定时任务调用，自动生成并保存每日学习内容
"""

import json
import os
from datetime import datetime
from pathlib import Path

def get_stage_info(day):
    """根据天数获取阶段信息"""
    stages = [
        {"id": 1, "name": "基础心理学", "days": 30},
        {"id": 2, "name": "发展心理学", "days": 30},
        {"id": 3, "name": "社会心理学", "days": 30},
        {"id": 4, "name": "咨询心理学", "days": 30},
        {"id": 5, "name": "心理诊断与测量", "days": 30},
        {"id": 6, "name": "操作技能与综合应用", "days": 30}
    ]
    
    cumulative = 0
    for stage in stages:
        cumulative += stage["days"]
        if day <= cumulative:
            return {
                "stage_id": stage["id"],
                "stage_name": stage["name"],
                "day_in_stage": day - (cumulative - stage["days"])
            }
    return {"stage_id": 6, "stage_name": "复习冲刺", "day_in_stage": day - 180}

def generate_lesson(day):
    """生成第 N 天的学习内容"""
    stage = get_stage_info(day)
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 根据阶段和天数确定主题
    topics_basic = ["心理学概述", "神经生理机制", "感觉知觉", "意识注意", "记忆", "思维", "语言", "动机情绪", "能力人格"]
    topics_dev = ["胎儿婴儿期", "幼儿期", "童年期", "青春期", "青年期", "中年期", "老年期"]
    topics_social = ["社会认知", "社会态度", "社会影响", "人际关系", "群体心理"]
    topics_counsel = ["精神分析", "行为疗法", "认知疗法", "人本主义", "咨询技术"]
    topics_diag = ["心理评估", "临床访谈", "测量学基础", "智力测验", "人格测验"]
    topics_prac = ["障碍识别", "危机干预", "案例分析", "伦理规范", "考试技巧"]
    
    topic_lists = {
        1: topics_basic, 2: topics_dev, 3: topics_social,
        4: topics_counsel, 5: topics_diag, 6: topics_prac
    }
    
    topic_list = topic_lists.get(stage["stage_id"], topics_basic)
    topic_idx = min((day - 1) // 3, len(topic_list) - 1)
    topic = topic_list[topic_idx]
    
    lesson = f"""# Day {day:03d} - {topic}

**学习日期**: {today}  
**所属阶段**: {stage['stage_name']} (第{stage['stage_id']}阶段)  
**建议学习时长**: 50 分钟

---

## 学习目标

通过今天的学习，你将能够：
1. 理解{topic}的核心概念和基本原理
2. 掌握相关的经典理论和重要研究
3. 运用所学知识分析和解释心理现象

---

## 核心内容

### 一、基本概念

【详细讲解{topic}的定义、内涵，所有专业名词都提供清晰定义】

### 二、主要理论

【介绍与{topic}相关的重要理论，包括提出者、核心观点、实验依据】

### 三、实际应用

【说明{topic}在日常生活和心理咨询中的具体应用】

---

## 重点概念解析

- **核心概念 1**: 【明确定义 + 特征描述 + 实例说明】
- **核心概念 2**: 【明确定义 + 特征描述 + 实例说明】
- **核心概念 3**: 【明确定义 + 特征描述 + 实例说明】

---

## 易错点提醒

1. **易混淆点**: 【说明容易混淆的概念及区分方法】
2. **常见误区**: 【指出常见理解偏差并纠正】

---

## 知识联系

- **与前期知识的联系**: 【说明与之前学习内容的关联】
- **为后续知识做铺垫**: 【说明对后续学习的帮助】

---

## 今日总结

今日学习了{topic}的核心内容。重点掌握了基本概念、主要理论和实际应用。需要特别注意概念之间的区别和联系，通过习题巩固理解。

---

## 下一步建议

1. **立即复习**: 花 5 分钟回顾今天的学习目标和重点概念
2. **完成习题**: 完成配套的 10 道练习题
3. **标记疑问**: 记录不理解的内容，后续重点复习
4. **明日预习**: 浏览明天的学习主题

---

**元数据**:
- 阶段 ID: {stage['stage_id']}
- 天数：{day}
- 主题标签：[{stage['stage_name']}, {topic}]
- 创建时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""
    
    return topic, lesson

def generate_questions(day, topic):
    """生成配套习题"""
    questions = f"""# Day {day:03d} 习题练习

**对应课程**: Day {day:03d} - {topic}  
**建议完成时间**: 10 分钟  
**题目数量**: 10 题

---

## 选择题

### 1. 关于{topic}的基础概念，下列说法正确的是：
A. [选项 A 内容]
B. [选项 B 内容]
C. [选项 C 内容]
D. [选项 D 内容]

### 2. {topic}的核心理论是由哪位心理学家提出的？
A. [心理学家 A]
B. [心理学家 B]
C. [心理学家 C]
D. [心理学家 D]

### 3. 下列哪项不属于{topic}的研究范畴？
A. [选项 A]
B. [选项 B]
C. [选项 C]
D. [选项 D]

### 4. 在{topic}领域，经典的实验范式是：
A. [实验 A]
B. [实验 B]
C. [实验 C]
D. [实验 D]

### 5. 关于{topic}的应用，以下说法错误的是：
A. [选项 A]
B. [选项 B]
C. [选项 C]
D. [选项 D]

### 6. {topic}与下列哪个概念关系最密切？
A. [概念 A]
B. [概念 B]
C. [概念 C]
D. [概念 D]

### 7. 在心理咨询中，{topic}的知识主要用于：
A. [用途 A]
B. [用途 B]
C. [用途 C]
D. [用途 D]

### 8. 下列关于{topic}的说法，哪项是正确的？
A. [选项 A]
B. [选项 B]
C. [选项 C]
D. [选项 D]

### 9. {topic}的研究方法主要包括：
A. [方法 A]
B. [方法 B]
C. [方法 C]
D. [方法 D]

### 10. 综合应用：在面对实际案例时，如何运用{topic}的知识？
A. [方案 A]
B. [方案 B]
C. [方案 C]
D. [方案 D]

---

## 答案与解析

1. **答案**: A  
   **解析**: 【详细说明为什么 A 正确，其他选项错在哪里】

2. **答案**: B  
   **解析**: 【详细解析】

3. **答案**: C  
   **解析**: 【详细解析】

4. **答案**: D  
   **解析**: 【详细解析】

5. **答案**: A  
   **解析**: 【详细解析】

6. **答案**: B  
   **解析**: 【详细解析】

7. **答案**: C  
   **解析**: 【详细解析】

8. **答案**: D  
   **解析**: 【详细解析】

9. **答案**: A  
   **解析**: 【详细解析】

10. **答案**: B  
    **解析**: 【详细解析】

---

**元数据**:
- 对应天数：{day}
- 难度等级：中等
- 覆盖知识点：[{topic}]
- 创建时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""
    return questions

def update_index(base_path, day, title):
    """更新索引文件"""
    index_path = base_path / "index.json"
    stage = get_stage_info(day)
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 加载或创建索引
    if index_path.exists():
        with open(index_path, 'r', encoding='utf-8') as f:
            index = json.load(f)
    else:
        index = {
            "name": "心理学知识库",
            "description": "心理咨询师考试自学知识库",
            "created_at": today,
            "last_updated": today,
            "total_lessons": 0,
            "current_stage": 1,
            "current_day": 0,
            "stages": [
                {"id": 1, "name": "基础心理学", "duration_days": 30, "status": "pending"},
                {"id": 2, "name": "发展心理学", "duration_days": 30, "status": "pending"},
                {"id": 3, "name": "社会心理学", "duration_days": 30, "status": "pending"},
                {"id": 4, "name": "咨询心理学", "duration_days": 30, "status": "pending"},
                {"id": 5, "name": "心理诊断与测量", "duration_days": 30, "status": "pending"},
                {"id": 6, "name": "操作技能与综合应用", "duration_days": 30, "status": "pending"}
            ],
            "lessons": [],
            "knowledge_modules": ["基础心理学", "发展心理学", "社会心理学", "咨询心理学", "心理诊断学", "心理测量学"]
        }
    
    # 添加课程记录
    lesson_record = {
        "day": day,
        "title": title,
        "stage_id": stage["stage_id"],
        "stage_name": stage["stage_name"],
        "date": today,
        "file_path": f"daily-lessons/day-{day:03d}.md",
        "questions_path": f"practice-questions/day-{day:03d}-questions.md",
        "tags": [stage["stage_name"], topic],
        "status": "completed"
    }
    
    # 检查是否已存在
    existing = next((l for l in index["lessons"] if l["day"] == day), None)
    if existing:
        existing.update(lesson_record)
    else:
        index["lessons"].append(lesson_record)
    
    # 更新进度
    if day > index.get("current_day", 0):
        index["current_day"] = day
        if day<= 30:
            index["current_stage"] = 1
            index["stages"][0]["status"] = "in_progress"
        elif day <= 60:
            index["current_stage"] = 2
            index["stages"][1]["status"] = "in_progress"
            index["stages"][0]["status"] = "completed"
        elif day <= 90:
            index["current_stage"] = 3
            index["stages"][2]["status"] = "in_progress"
            index["stages"][1]["status"] = "completed"
        elif day <= 120:
            index["current_stage"] = 4
            index["stages"][3]["status"] = "in_progress"
            index["stages"][2]["status"] = "completed"
        elif day <= 150:
            index["current_stage"] = 5
            index["stages"][4]["status"] = "in_progress"
            index["stages"][3]["status"] = "completed"
        else:
            index["current_stage"] = 6
            index["stages"][5]["status"] = "in_progress"
            index["stages"][4]["status"] = "completed"
    
    index["total_lessons"] = len(index["lessons"])
    index["last_updated"] = today
    
    # 保存索引
    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump(index, f, ensure_ascii=False, indent=2)

def main():
    """主函数"""
    base_path = Path(__file__).parent
    
    # 获取天数（从参数或递增）
    import sys
    if len(sys.argv) > 1:
        try:
            day = int(sys.argv[1])
        except:
            day = 1
    else:
        day = 1
    
    print(f"开始同步 Day {day}...")
    
    # 生成内容
    topic, lesson = generate_lesson(day)
    questions = generate_questions(day, topic)
    
    # 保存文件
    lesson_file = base_path / "daily-lessons" / f"day-{day:03d}.md"
    questions_file = base_path / "practice-questions" / f"day-{day:03d}-questions.md"
    
    lesson_file.parent.mkdir(exist_ok=True)
    questions_file.parent.mkdir(exist_ok=True)
    
    with open(lesson_file, 'w', encoding='utf-8') as f:
        f.write(lesson)
    
    with open(questions_file, 'w', encoding='utf-8') as f:
        f.write(questions)
    
    # 更新索引
    update_index(base_path, day, topic)
    
    print(f"✓ Day {day} - {topic}")
    print(f"✓ 课程：{lesson_file}")
    print(f"✓ 习题：{questions_file}")
    print("✅ 同步完成")

if __name__ == "__main__":
    main()
