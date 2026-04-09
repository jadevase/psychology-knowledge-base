import json
from datetime import datetime
from pathlib import Path

# 基础路径
base_path = Path(__file__).parent
daily_lessons_path = base_path / "daily-lessons"
practice_questions_path = base_path / "practice-questions"
index_path = base_path / "index.json"

# 确保目录存在
daily_lessons_path.mkdir(exist_ok=True)
practice_questions_path.mkdir(exist_ok=True)

# 第 1 天内容
day = 1
today = datetime.now().strftime("%Y-%m-%d")
topic = "心理学概述"

lesson_content = f"""# Day {day:03d} - {topic}

**学习日期**: {today}  
**所属阶段**: 基础心理学 (第 1 阶段)  
**建议学习时长**: 50 分钟

---

## 学习目标

通过今天的学习，你将能够：
1. 理解心理学的定义、研究对象和主要流派
2. 掌握心理学研究的基本方法
3. 了解心理学在生活中的实际应用

---

## 核心内容

### 一、心理学的定义与研究对象

**心理学 (Psychology)** 是研究心理现象及其规律的科学。它既研究个体的心理活动（如感知、记忆、思维、情绪等），也研究群体的心理现象（如人际关系、群体行为等）。

心理学的研究对象包括：
- **心理过程**: 认知过程（感觉、知觉、记忆、思维）、情绪情感过程、意志过程
- **个性心理**: 个性倾向性（需要、动机、兴趣）、个性心理特征（能力、气质、性格）

### 二、心理学的主要流派

1. **构造主义 (Structuralism)**
   - 代表人物：冯特 (Wundt)、铁钦纳 (Titchener)
   - 核心观点：主张用内省法分析意识的基本元素
   - 贡献：使心理学成为一门独立科学

2. **机能主义 (Functionalism)**
   - 代表人物：詹姆斯 (James)、杜威 (Dewey)
   - 核心观点：关注意识的功能和作用，强调适应环境
   - 贡献：推动应用心理学发展

3. **行为主义 (Behaviorism)**
   - 代表人物：华生 (Watson)、斯金纳 (Skinner)
   - 核心观点：主张研究可观察的行为，反对研究意识
   - 贡献：建立科学的行为研究方法

4. **精神分析学派 (Psychoanalysis)**
   - 代表人物：弗洛伊德 (Freud)
   - 核心观点：强调潜意识对行为的决定作用
   - 贡献：开创人格理论和心理治疗方法

5. **人本主义心理学 (Humanistic Psychology)**
   - 代表人物：马斯洛 (Maslow)、罗杰斯 (Rogers)
   - 核心观点：强调人的自我实现潜能和主观能动性
   - 贡献：提出积极的人性观

6. **认知心理学 (Cognitive Psychology)**
   - 兴起时间：20 世纪 60 年代
   - 核心观点：将人视为信息加工系统，研究认知过程
   - 贡献：成为当代心理学的主流范式

### 三、心理学的研究方法

1. **观察法**: 在自然或控制条件下系统观察行为
2. **实验法**: 操纵自变量，观察因变量变化，确定因果关系
3. **调查法**: 通过问卷、访谈收集数据
4. **测验法**: 使用标准化心理测量工具评估心理特征
5. **个案法**: 深入研究个别对象的详细信息

### 四、心理学的应用领域

- **临床与咨询心理学**: 心理障碍诊断与治疗
- **教育心理学**: 学习与教学过程优化
- **工业与组织心理学**: 人力资源管理、工作环境改善
- **健康心理学**: 促进身心健康行为
- **社会心理学**: 理解人际互动与群体行为

---

## 重点概念解析

- **心理学**: 研究心理现象及其规律的科学，兼具自然科学和社会科学属性
- **意识**: 个体对自身心理活动和外部环境的觉知状态
- **潜意识**: 个体无法直接觉察但影响行为的心理活动
- **行为主义**: 主张只研究可观察行为，采用刺激 - 反应模式的心理学流派
- **认知**: 个体获取、加工、存储和使用信息的心理过程

---

## 易错点提醒

1. **心理学≠读心术**: 心理学是科学，不是猜测他人想法的玄学
2. **心理学≠心理咨询**: 心理咨询只是心理学的一个应用领域
3. **各流派并非对立**: 不同流派从不同角度解释心理现象，各有贡献和局限

---

## 今日学习总结

今天是心理学学习的第一天，我们了解了：
- 心理学的定义和研究对象
- 六大主要流派的核心观点和代表人物
- 五种基本研究方法
- 心理学的主要应用领域

这些基础知识将为后续深入学习各个分支奠定坚实基础。

---

*文件生成时间*: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""

# 生成习题
questions_content = f"""# Day {day:03d} 配套习题 - {topic}

**生成日期**: {today}  
**题型**: 单项选择题  
**题数**: 10 题  
**建议用时**: 10 分钟

---

## 习题部分

**1. 心理学是研究什么现象的科学？**  
A. 生理现象  
B. 心理现象  
C. 社会现象  
D. 自然现象

**2. 构造主义心理学的代表人物是？**  
A. 詹姆斯  
B. 弗洛伊德  
C. 冯特  
D. 斯金纳

**3. 主张用内省法分析意识基本元素的流派是？**  
A. 行为主义  
B. 机能主义  
C. 构造主义  
D. 人本主义

**4. 行为主义心理学强调研究？**  
A. 意识  
B. 潜意识  
C. 可观察的行为  
D. 自我实现

**5. 精神分析学派的创始人是？**  
A. 马斯洛  
B. 罗杰斯  
C. 华生  
D. 弗洛伊德

**6. 强调人的自我实现潜能的心理学流派是？**  
A. 行为主义  
B. 精神分析  
C. 人本主义  
D. 构造主义

**7. 认知心理学兴起于哪个年代？**  
A. 20 世纪 20 年代  
B. 20 世纪 40 年代  
C. 20 世纪 60 年代  
D. 20 世纪 80 年代

**8. 以下哪种方法可以确定因果关系？**  
A. 观察法  
B. 实验法  
C. 调查法  
D. 个案法

**9. 机能主义心理学的核心观点是？**  
A. 分析意识的元素  
B. 关注意识的功能和作用  
C. 研究可观察的行为  
D. 强调潜意识的作用

**10. 心理学的研究对象不包括？**  
A. 心理过程  
B. 个性心理  
C. 生理结构  
D. 群体心理现象

---

## 答案与解析

| 题号 | 答案 | 解析 |
|------|------|------|
| 1 | B | 心理学是研究心理现象及其规律的科学 |
| 2 | C | 冯特是构造主义的代表人物，建立了第一个心理学实验室 |
| 3 | C | 构造主义主张用内省法分析意识的基本元素 |
| 4 | C | 行为主义主张只研究可观察的行为，反对研究意识 |
| 5 | D | 弗洛伊德创立了精神分析学派 |
| 6 | C | 人本主义强调人的自我实现潜能和主观能动性 |
| 7 | C | 认知心理学兴起于 20 世纪 60 年代 |
| 8 | B | 实验法通过操纵自变量来确定因果关系 |
| 9 | B | 机能主义关注意识的功能和作用，强调适应环境 |
| 10 | C | 生理结构属于生物学研究对象，不是心理学的直接研究对象 |

---

*文件生成时间*: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""

# 保存文件
lesson_file = daily_lessons_path / f"day-{day:03d}.md"
questions_file = practice_questions_path / f"day-{day:03d}-questions.md"

lesson_file.write_text(lesson_content, encoding='utf-8')
questions_file.write_text(questions_content, encoding='utf-8')

# 更新索引文件
with open(index_path, 'r', encoding='utf-8') as f:
    index_data = json.load(f)

index_data['total_lessons'] = 1
index_data['current_day'] = 1
index_data['current_stage'] = 1
index_data['last_updated'] = today

if day not in [l.get('day') for l in index_data.get('lessons', [])]:
    index_data['lessons'].append({
        'day': day,
        'topic': topic,
        'stage': '基础心理学',
        'date_added': today,
        'lesson_file': f'daily-lessons/day-{day:03d}.md',
        'questions_file': f'practice-questions/day-{day:03d}-questions.md'
    })

with open(index_path, 'w', encoding='utf-8') as f:
    json.dump(index_data, f, ensure_ascii=False, indent=2)

print(f"✓ 第{day}天学习内容已生成")
print(f"  课程主题：{topic}")
print(f"  学习文档：{lesson_file}")
print(f"  习题文档：{questions_file}")
print(f"  当前进度：第{day}天/共 180 天")
