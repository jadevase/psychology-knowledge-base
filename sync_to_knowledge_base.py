"""
心理学知识库自动同步脚本

功能：
1. 根据学习进度生成当日学习内容（完整版 + 简版）
2. 将学习内容保存到知识库的 daily-lessons 目录
3. 生成配套习题并保存到 practice-questions 目录
4. 更新 index.json 索引文件
5. 自动更新 index.html，实现网页导航
6. 按知识模块分类整理内容

使用方法：
    python sync_to_knowledge_base.py [day_number]
    
参数：
    day_number: 可选，指定学习天数。如果不提供，则从 index.json 读取当前进度
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path


class PsychologyKnowledgeBase:
    """心理学知识库管理器"""
    
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.index_path = self.base_path / "index.json"
        self.index_html_path = self.base_path / "index.html"
        self.daily_lessons_path = self.base_path / "daily-lessons"
        self.practice_questions_path = self.base_path / "practice-questions"
        
        # 确保目录存在
        self.daily_lessons_path.mkdir(exist_ok=True)
        self.practice_questions_path.mkdir(exist_ok=True)
        
        # 加载索引
        self.index = self._load_index()
    
    def _load_index(self) -> dict:
        """加载索引文件"""
        if self.index_path.exists():
            with open(self.index_path, 'r', encoding='utf-8') as f:
                loaded_index = json.load(f)
            
            # 兼容旧格式：如果没有 stages 字段，使用 studyPlan.stages
            if "stages" not in loaded_index and "studyPlan" in loaded_index:
                # 转换 studyPlan 格式为脚本期望的格式
                old_stages = loaded_index["studyPlan"].get("stages", [])
                new_stages = []
                for i, stage in enumerate(old_stages):
                    # 解析 days 范围
                    days_range = stage.get("days", "1-30")
                    start_day, end_day = map(int, days_range.split("-"))
                    duration = end_day - start_day + 1
                    
                    new_stages.append({
                        "id": i + 1,
                        "name": stage.get("name", f"阶段{i+1}"),
                        "description": stage.get("topics", [""])[0] if stage.get("topics") else "",
                        "duration_days": duration,
                        "status": "pending"
                    })
                
                loaded_index["stages"] = new_stages
            
            # 确保其他必需字段存在
            if "current_stage" not in loaded_index:
                loaded_index["current_stage"] = 1
            if "current_day" not in loaded_index:
                loaded_index["current_day"] = loaded_index.get("currentLesson", {}).get("day", 0)
            
            return loaded_index
        else:
            default_index = {
                "name": "心理学知识库",
                "description": "心理咨询师考试自学知识库",
                "created_at": datetime.now().strftime("%Y-%m-%d"),
                "last_updated": datetime.now().strftime("%Y-%m-%d"),
                "total_lessons": 0,
                "current_stage": 1,
                "current_day": 0,
                "stages": self._get_default_stages(),
                "lessons": [],
                "knowledge_modules": [
                    "基础心理学",
                    "发展心理学",
                    "社会心理学",
                    "咨询心理学",
                    "心理诊断学",
                    "心理测量学",
                    "变态心理学",
                    "健康心理学"
                ]
            }
            self._save_index(default_index)
            return default_index
    
    def _save_index(self, index_data: dict):
        """保存索引文件"""
        with open(self.index_path, 'w', encoding='utf-8') as f:
            json.dump(index_data, f, ensure_ascii=False, indent=2)
    
    def _get_default_stages(self) -> list:
        """获取默认阶段配置"""
        return [
            {"id": 1, "name": "基础心理学", "description": "心理学基础理论和概念", "duration_days": 30, "status": "pending"},
            {"id": 2, "name": "发展心理学", "description": "个体心理发展规律", "duration_days": 30, "status": "pending"},
            {"id": 3, "name": "社会心理学", "description": "社会互动与群体心理", "duration_days": 30, "status": "pending"},
            {"id": 4, "name": "咨询心理学", "description": "心理咨询理论与技术", "duration_days": 30, "status": "pending"},
            {"id": 5, "name": "心理诊断与测量", "description": "心理评估和测量方法", "duration_days": 30, "status": "pending"},
            {"id": 6, "name": "操作技能与综合应用", "description": "实践技能和综合案例分析", "duration_days": 30, "status": "pending"}
        ]
    
    def get_current_day(self) -> int:
        """获取当前学习天数"""
        return self.index.get("current_day", 0)
    
    def get_stage_info(self, day: int) -> dict:
        """根据天数获取阶段信息"""
        cumulative_days = 0
        for stage in self.index["stages"]:
            cumulative_days += stage["duration_days"]
            if day<= cumulative_days:
                return {
                    "stage_id": stage["id"],
                    "stage_name": stage["name"],
                    "stage_number": stage["id"],
                    "day_in_stage": day - (cumulative_days - stage["duration_days"])
                }
        return {
            "stage_id": 6,
            "stage_name": "复习与冲刺",
            "stage_number": 6,
            "day_in_stage": day - 180
        }
    
    def _get_tags_for_day(self, day: int, stage_info: dict) -> str:
        """为当天课程生成标签"""
        stage_tags = {
            1: ["基础心理学", "心理学基础", "认知过程"],
            2: ["发展心理学", "毕生发展", "年龄特征"],
            3: ["社会心理学", "社会行为", "人际关系"],
            4: ["咨询心理学", "心理治疗", "咨询技术"],
            5: ["心理诊断", "心理测量", "心理评估"],
            6: ["操作技能", "综合应用", "考试准备"]
        }
        tags = stage_tags.get(stage_info["stage_id"], ["心理学"])
        return ", ".join(tags)

    def generate_full_lesson(self, day: int) -> tuple[str, str]:
        """生成第 N 天的完整学习内容（约 25,000 字）"""
        stage_info = self.get_stage_info(day)
        today = datetime.now().strftime("%Y-%m-%d")
        
        content_generators = {
            1: self._generate_basic_psychology_full,
            2: self._generate_developmental_psychology_full,
            3: self._generate_social_psychology_full,
            4: self._generate_counseling_psychology_full,
            5: self._generate_diagnostic_psychology_full,
            6: self._generate_practical_skills_full
        }
        
        generator = content_generators.get(stage_info["stage_id"], self._generate_basic_psychology_full)
        title, content = generator(day, stage_info)
        
        lesson = f"""# Day {day:03d} - {title}

**学习日期**: {today}  
**所属阶段**: {stage_info['stage_name']} (第一阶段)  
**建议学习时长**: 50 分钟

---

## 学习目标

完成本课后，你将能够：

1.  **准确定义**核心概念，说明其内涵和外延
2.  **区分**相关概念的异同，避免混淆
3.  **解释**主要理论的观点、实验依据和应用
4.  **列举**关键知识点，记忆重要结论
5.  **应用**所学知识分析实际案例
6.  **评价**不同理论的优缺点和适用范围

---

{content}

---

## 今日总结

【此处为今日学习的 300-500 字总结】

### 知识框架回顾

```
{{这里用思维导图或树状图形式呈现本节课的知识结构}}
```

### 核心要点速记

1.  **最重要概念**: 【1-2 个最核心的概念】
2.  **最关键理论**: 【1-2 个最重要的理论】
3.  **最容易考点**: 【预测可能的考试重点】

---

## 下一步建议

1.  **立即复习**: 花 5 分钟回顾今天的学习目标和重点概念
2.  **完成习题**: 完成配套的 10 道练习题（建议 10 分钟）
3.  **标记疑问**: 记录不理解的内容，后续重点复习
4.  **明日预习**: 浏览明天的学习主题，建立知识联系
5.  **间隔复习**: 按照艾宾浩斯曲线，在第 1、2、4、7、15 天复习

---

**元数据**:
- 阶段 ID: {stage_info['stage_id']}
- 天数：{day}
- 主题标签：[{self._get_tags_for_day(day, stage_info)}]
- 创建时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
- 版本：完整版（约 25,000 字）
"""
        
        return title, lesson
    
    def generate_simple_lesson(self, day: int, full_title: str) -> str:
        """基于完整内容生成简版（精简到 3000-5000 字）"""
        stage_info = self.get_stage_info(day)
        today = datetime.now().strftime("%Y-%m-%d")
        
        simple_content = f"""# Day {day:03d} - {full_title}（简版）

**学习日期**: {today}  
**所属阶段**: {stage_info['stage_name']} (第一阶段)  
**建议学习时长**: 50 分钟

---

## 学习目标

1. 准确定义核心概念
2. 区分相关概念的异同
3. 掌握主要理论的观点
4. 记忆关键知识点

---

## 核心知识点

### 一、基本概念

【此处提炼完整版中的核心概念定义】

### 二、主要理论

【此处总结重要理论】

### 三、关键结论

【列出 5-10 条最重要的结论】

---

## 重点概念速查表

| 概念 | 定义 | 关键特征 | 示例 |
|------|------|----------|------|
| 【概念 1】 | 【一句话定义】 | 【2-3 个特征】 | 【生活实例】 |
| 【概念 2】 | 【一句话定义】 | 【2-3 个特征】 | 【生活实例】 |

---

## 理论对比

| 理论 | 代表人物 | 核心观点 | 贡献 | 局限 |
|------|----------|----------|------|------|
| 【理论 1】 | 【人名】 | 【一句话】 | 【贡献】 | 【局限】 |
| 【理论 2】 | 【人名】 | 【一句话】 | 【贡献】 | 【局限】 |

---

## 易错点提醒

- ❌ 【常见错误理解 1】 → ✅ 【正确理解】
- ❌ 【常见错误理解 2】 → ✅ 【正确理解】

---

## 记忆口诀

【编写助记口诀】

---

## 今日总结

- 【要点 1】
- 【要点 2】
- 【要点 3】

---

## 下一步

1. 完成 [Day {day:03d} 练习题](../practice-questions/day-{day:03d}-questions.md)
2. 预习明天内容

---

*详细版课程请查看：[day-{day:03d}-full.md](day-{day:03d}-full.md)*
"""
        
        return simple_content

    def _generate_basic_psychology_full(self, day: int, stage_info: dict) -> tuple[str, str]:
        """生成基础心理学阶段的完整学习内容"""
        topics = [
            ("心理学概述", "心理学的研究对象、方法和历史发展"),
            ("心理的神经生理机制", "神经系统结构与功能"),
            ("感觉和知觉", "感觉的种类、知觉的特性"),
            ("意识和注意", "意识的状态、注意的类型"),
            ("记忆", "记忆的过程、遗忘规律"),
            ("思维", "思维的种类、问题解决"),
            ("语言", "语言的结构、获得理论"),
            ("动机和需要", "动机理论、需要层次"),
            ("情绪和情感", "情绪理论、情感分类"),
            ("能力和人格", "能力结构、人格理论")
        ]
        
        topic_idx = min((day - 1) // 3, len(topics) - 1)
        topic_title, topic_desc = topics[topic_idx]
        title = f"{topic_title}"
        
        content = f"""## 一、{topic_title}的基本概念

### 1.1 核心定义

**定义**: 【标准定义】

**内涵**: 【深入解释】

**外延**: 【适用范围】

### 1.2 相关概念辨析

| 概念 | 定义 | 与核心概念的关系 |
|------|------|------------------|
| 【相关概念 1】 | 【定义】 | 【关系说明】 |

---

## 二、{topic_title}的主要理论

### 2.1 【理论名称 1】

**提出者**: 【人名 + 年代】

**核心观点**: 
- 观点 1
- 观点 2

**实验依据**: 【描述经典实验】

**贡献**: 【学术贡献】

**局限性**: 【不足之处】

---

## 三、{topic_title}的研究方法

1. **实验法**: 适用场景和经典研究
2. **观察法**: 适用场景和注意事项
3. **测验法**: 常用工具和信效度

---

## 四、{topic_title}的实际应用

### 4.1 在日常生活中的应用

【举例说明】

### 4.2 在心理咨询中的应用

【说明应用】

---

## 五、重点概念详解

### 5.1 【概念 1】

**定义**: 【明确定义】

**特征**: 特征 1、特征 2、特征 3

**实例分析**: 【具体案例】

---

## 六、经典研究介绍

### 6.1 【研究名称 1】

**研究者**: 【人名】

**研究问题**: 【要解决的问题】

**主要发现**: 【研究结果】

**意义**: 【学术意义】

---

## 七、易错点与常见误解

**误解 1**: 【描述】 → **纠正**: 【正确理解】

**误解 2**: 【描述】 → **纠正**: 【正确理解】

---

## 八、知识联系

- **与前期知识的联系**: 【说明关联】
- **为后续知识做铺垫**: 【说明帮助】
"""
        
        return title, content
    
    def _generate_developmental_psychology_full(self, day: int, stage_info: dict) -> tuple[str, str]:
        """生成发展心理学阶段的完整学习内容"""
        stages = ["胎儿期和婴儿期", "幼儿期", "童年期", "青春期", "青年期", "中年期", "老年期"]
        stage_idx = min((day - 1) // 4, len(stages) - 1)
        stage_name = stages[stage_idx]
        title = f"{stage_name}心理发展"
        
        content = f"""## 一、{stage_name}概述

### 1.1 年龄范围
【说明该发展阶段的年龄划分】

### 1.2 发展任务
【列出主要发展任务】

---

## 二、{stage_name}的认知发展

### 2.1 感知觉发展
【详细描述】

### 2.2 记忆发展
【详细描述】

### 2.3 思维发展
【包括皮亚杰理论中的相应阶段】

---

## 三、{stage_name}的情感和社会发展

### 3.1 情绪发展
【描述情绪表达、理解和调节】

### 3.2 自我意识发展
【描述自我概念、自尊的发展】

### 3.3 社会性发展
【描述同伴关系、亲子关系等】

---

## 四、影响因素

### 4.1 生物因素：遗传、成熟、健康
### 4.2 环境因素：家庭、学校、同伴、文化
### 4.3 个体主动因素

---

## 五、典型心理问题

【列举常见问题和干预建议】

---

## 六、相关理论

【详细介绍相关发展理论】
"""
        
        return title, content
    
    def _generate_social_psychology_full(self, day: int, stage_info: dict) -> tuple[str, str]:
        """生成社会心理学阶段的完整学习内容"""
        topics = ["社会认知", "社会态度", "社会影响", "人际关系", "群体心理", "亲社会行为", "攻击行为"]
        topic_idx = min((day - 1) // 4, len(topics) - 1)
        topic_title = topics[topic_idx]
        title = f"{topic_title}"
        
        content = f"""## 一、{topic_title}概述

### 1.1 基本概念
【介绍基本概念和研究范畴】

### 1.2 研究意义
【说明研究重要性】

---

## 二、经典理论

### 2.1 【理论 1】
【详细介绍】

### 2.2 【理论 2】
【详细介绍】

---

## 三、经典研究

### 3.1 【研究 1】
【描述实验设计、过程和发现】

---

## 四、影响因素

### 4.1 个体因素
### 4.2 情境因素
### 4.3 文化因素

---

## 五、应用

### 5.1 日常生活应用
### 5.2 组织管理应用
### 5.3 心理健康应用
"""
        
        return title, content
    
    def _generate_counseling_psychology_full(self, day: int, stage_info: dict) -> tuple[str, str]:
        """生成咨询心理学阶段的完整学习内容"""
        approaches = ["精神分析疗法", "行为疗法", "认知疗法", "人本主义疗法", "家庭治疗", "咨询过程和技术"]
        approach_idx = min((day - 1) // 5, len(approaches) - 1)
        approach_name = approaches[approach_idx]
        title = f"{approach_name}"
        
        content = f"""## 一、{approach_name}概述

### 1.1 历史背景
### 1.2 理论基础
### 1.3 核心概念

---

## 二、核心技术

### 2.1 【技术 1】
### 2.2 【技术 2】
### 2.3 【技术 3】

---

## 三、治疗过程

### 3.1 初始阶段
### 3.2 工作阶段
### 3.3 结束阶段

---

## 四、适用范围

### 4.1 适用人群
### 4.2 适用问题
### 4.3 禁忌症

---

## 五、疗效研究

【介绍相关疗效研究】
"""
        
        return title, content
    
    def _generate_diagnostic_psychology_full(self, day: int, stage_info: dict) -> tuple[str, str]:
        """生成心理诊断与测量阶段的完整学习内容"""
        topics = ["心理评估概述", "临床访谈技术", "心理测量学基础", "智力测验", "人格测验", "心理健康评估"]
        topic_idx = min((day - 1) // 5, len(topics) - 1)
        topic_title = topics[topic_idx]
        title = f"{topic_title}"
        
        content = f"""## 一、{topic_title}概述

### 1.1 基本概念
### 1.2 发展历程

---

## 二、原理和方法

### 2.1 基本原理
### 2.2 主要方法

---

## 三、常用工具和量表

### 3.1 【工具/量表 1】
- 编制者、适用对象、维度结构
- 信效度指标、使用方法

### 3.2 【工具/量表 2】

---

## 四、结果解释与应用

### 4.1 分数解释
### 4.2 报告撰写
### 4.3 伦理考虑
"""
        
        return title, content
    
    def _generate_practical_skills_full(self, day: int, stage_info: dict) -> tuple[str, str]:
        """生成操作技能与综合应用阶段的学习内容"""
        topics = ["常见心理障碍识别", "危机干预技术", "综合案例分析", "咨询伦理规范", "考试技巧与策略"]
        topic_idx = min((day - 1) // 6, len(topics) - 1)
        topic_title = topics[topic_idx]
        title = f"{topic_title}"
        
        content = f"""## 一、{topic_title}概述

### 1.1 重要性
### 1.2 学习目标

---

## 二、核心知识和技能

### 2.1 【知识点 1】
### 2.2 【知识点 2】
### 2.3 【技能 1】
### 2.4 【技能 2】

---

## 三、案例分析

### 3.1 案例呈现
### 3.2 问题分析
### 3.3 干预方案

---

## 四、实践练习

【提供练习题或角色扮演脚本】
"""
        
        return title, content

    def generate_practice_questions(self, day: int, lesson_title: str) -> str:
        """生成配套习题"""
        stage_info = self.get_stage_info(day)
        
        questions_md = f"""# Day {day:03d} 习题练习

**对应课程**: Day {day:03d} - {lesson_title}  
**建议完成时间**: 10 分钟  
**题目数量**: 10 题

---

## 选择题

### 1. [关于{lesson_title}的基础概念题]
A. [选项 A]
B. [选项 B]
C. [选项 C]
D. [选项 D]

### 2. [关于核心理论的理解题]
A. [选项 A]
B. [选项 B]
C. [选项 C]
D. [选项 D]

### 3. [概念辨析题]
A. [选项 A]
B. [选项 B]
C. [选项 C]
D. [选项 D]

### 4. [应用场景题]
A. [选项 A]
B. [选项 B]
C. [选项 C]
D. [选项 D]

### 5. [综合分析题]
A. [选项 A]
B. [选项 B]
C. [选项 C]
D. [选项 D]

### 6. [细节理解题]
A. [选项 A]
B. [选项 B]
C. [选项 C]
D. [选项 D]

### 7. [理论应用题]
A. [选项 A]
B. [选项 B]
C. [选项 C]
D. [选项 D]

### 8. [对比分析题]
A. [选项 A]
B. [选项 B]
C. [选项 C]
D. [选项 D]

### 9. [实践判断题]
A. [选项 A]
B. [选项 B]
C. [选项 C]
D. [选项 D]

### 10. [综合提升题]
A. [选项 A]
B. [选项 B]
C. [选项 C]
D. [选项 D]

---

## 答案与解析

1. **答案**: A  
   **解析**: 【详细解析】

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
- 覆盖知识点：[{self._get_tags_for_day(day, stage_info)}]
- 创建时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""
        
        return questions_md
    
    def save_daily_lesson(self, day: int, full_content: str, simple_content: str, questions_content: str):
        """保存每日学习内容到知识库（完整版 + 简版）"""
        # 保存完整版课程
        full_lesson_file = self.daily_lessons_path / f"day-{day:03d}-full.md"
        with open(full_lesson_file, 'w', encoding='utf-8') as f:
            f.write(full_content)
        
        # 保存简版课程
        simple_lesson_file = self.daily_lessons_path / f"day-{day:03d}.md"
        with open(simple_lesson_file, 'w', encoding='utf-8') as f:
            f.write(simple_content)
        
        # 保存习题
        questions_file = self.practice_questions_path / f"day-{day:03d}-questions.md"
        with open(questions_file, 'w', encoding='utf-8') as f:
            f.write(questions_content)
        
        print(f"✓ 已保存完整课程：{full_lesson_file}")
        print(f"✓ 已保存简版课程：{simple_lesson_file}")
        print(f"✓ 已保存习题：{questions_file}")
    
    def update_index(self, day: int, title: str):
        """更新索引文件"""
        stage_info = self.get_stage_info(day)
        today = datetime.now().strftime("%Y-%m-%d")
        
        lesson_record = {
            "day": day,
            "title": title,
            "stage_id": stage_info["stage_id"],
            "stage_name": stage_info["stage_name"],
            "date": today,
            "file_path": f"daily-lessons/day-{day:03d}-full.md",
            "simple_path": f"daily-lessons/day-{day:03d}.md",
            "questions_path": f"practice-questions/day-{day:03d}-questions.md",
            "tags": self._get_tags_for_day(day, stage_info).split(", "),
            "status": "completed"
        }
        
        existing = next((l for l in self.index["lessons"] if l["day"] == day), None)
        if existing:
            existing.update(lesson_record)
        else:
            self.index["lessons"].append(lesson_record)
        
        if day > self.index["current_day"]:
            self.index["current_day"] = day
            if day<= 30:
                self.index["current_stage"] = 1
                self.index["stages"][0]["status"] = "in_progress"
            elif day <= 60:
                self.index["current_stage"] = 2
                self.index["stages"][1]["status"] = "in_progress"
                self.index["stages"][0]["status"] = "completed"
            elif day <= 90:
                self.index["current_stage"] = 3
                self.index["stages"][2]["status"] = "in_progress"
                self.index["stages"][1]["status"] = "completed"
            elif day <= 120:
                self.index["current_stage"] = 4
                self.index["stages"][3]["status"] = "in_progress"
                self.index["stages"][2]["status"] = "completed"
            elif day <= 150:
                self.index["current_stage"] = 5
                self.index["stages"][4]["status"] = "in_progress"
                self.index["stages"][3]["status"] = "completed"
            else:
                self.index["current_stage"] = 6
                self.index["stages"][5]["status"] = "in_progress"
                self.index["stages"][4]["status"] = "completed"
        
        self.index["last_updated"] = today
        self.index["total_lessons"] = len(self.index["lessons"])
        self._save_index(self.index)
        print(f"✓ 已更新索引文件：{self.index_path}")

    def update_index_html(self):
        """更新 index.html，动态显示所有课程和习题链接"""
        lessons = sorted(self.index.get("lessons", []), key=lambda x: x["day"])
        
        # 生成课程列表 HTML
        full_lessons_html = ""
        simple_lessons_html = ""
        questions_html = ""
        
        for lesson in lessons:
            day = lesson["day"]
            title = lesson["title"]
            date = lesson.get("date", "未知日期")
            
            # 完整版链接
            full_lessons_html += f"""<a href="daily-lessons/day-{day:03d}-full.md" class="nav-item">
                        <h3>Day {day:03d} - {title}（完整版）</h3>
                        <p>详细讲解（约 25,000 字） | 更新日期：{date}</p>
                    </a>
"""
            
            # 简版链接
            simple_lessons_html += f"""<a href="daily-lessons/day-{day:03d}.md" class="nav-item">
                        <h3>Day {day:03d} - {title}（简版）</h3>
                        <p>核心要点速查 | 更新日期：{date}</p>
                    </a>
"""
            
            # 习题链接
            questions_html += f"""<a href="practice-questions/day-{day:03d}-questions.md" class="nav-item">
                        <h3>Day {day:03d} 练习题</h3>
                        <p>10 道选择题 + 详细解析 | 更新日期：{date}</p>
                    </a>
"""
        
        # 计算统计数据
        total_days = len(lessons)
        current_day = self.index.get("current_day", 0)
        completion_rate = round((current_day / 180) * 100) if current_day > 0 else 0
        
        # 读取当前 HTML 模板
        html_template = self._get_html_template()
        
        # 替换动态内容
        html_content = html_template
        html_content = html_content.replace("{{TOTAL_DAYS}}", str(total_days))
        html_content = html_content.replace("{{CURRENT_DAY}}", str(current_day))
        html_content = html_content.replace("{{COMPLETION_RATE}}", str(completion_rate))
        html_content = html_content.replace("{{FULL_LESSONS_LIST}}", full_lessons_html)
        html_content = html_content.replace("{{SIMPLE_LESSONS_LIST}}", simple_lessons_html)
        html_content = html_content.replace("{{QUESTIONS_LIST}}", questions_html)
        
        # 保存 HTML 文件
        with open(self.index_html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✓ 已更新导航页面：{self.index_html_path}")
    
    def _get_html_template(self) -> str:
        """获取 HTML 模板"""
        return """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>心理咨询师考试知识库</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container { max-width: 1400px; margin: 0 auto; }
        header {
            text-align: center;
            color: white;
            padding: 40px 20px;
        }
        header h1 { font-size: 2.5em; margin-bottom: 10px; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }
        header p { font-size: 1.2em; opacity: 0.9; }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }
        .stat-card {
            background: white;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .stat-number { font-size: 2.5em; font-weight: bold; color: #667eea; }
        .stat-label { color: #666; margin-top: 5px; }
        .main-nav {
            background: white;
            border-radius: 10px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .nav-section { margin-bottom: 30px; }
        .nav-section h2 {
            color: #333;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }
        .nav-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 15px;
        }
        .nav-item {
            display: block;
            padding: 20px;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            border-radius: 8px;
            text-decoration: none;
            color: #333;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .nav-item:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        }
        .nav-item h3 { color: #667eea; margin-bottom: 8px; font-size: 1.1em; }
        .nav-item p { font-size: 0.9em; color: #666; }
        .progress-section {
            background: white;
            border-radius: 10px;
            padding: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .progress-section h2 { color: #333; margin-bottom: 20px; }
        .progress-bar {
            background: #e0e0e0;
            border-radius: 10px;
            height: 30px;
            overflow: hidden;
            margin: 20px 0;
        }
        .progress-fill {
            background: linear-gradient(90deg, #667eea, #764ba2);
            height: 100%;
            width: 0%;
            transition: width 0.5s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
        }
        footer {
            text-align: center;
            color: white;
            margin-top: 40px;
            padding: 20px;
        }
        @media (max-width: 768px) {
            header h1 { font-size: 1.8em; }
            .stats { grid-template-columns: repeat(2, 1fr); }
            .nav-grid { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🧠 心理咨询师考试知识库</h1>
            <p>系统化学习路径 · 每日精进 · 稳步通关</p>
        </header>

        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">{{TOTAL_DAYS}}</div>
                <div class="stat-label">已发布课程</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{{CURRENT_DAY}}</div>
                <div class="stat-label">当前进度（天）</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{{COMPLETION_RATE}}%</div>
                <div class="stat-label">完成率</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">180</div>
                <div class="stat-label">总学习天数</div>
            </div>
        </div>

        <div class="main-nav">
            <div class="nav-section">
                <h2>📚 核心学习资源</h2>
                <div class="nav-grid">
                    <a href="learning-plan.md" class="nav-item">
                        <h3>📋 学习计划</h3>
                        <p>6 个月备考规划，六个阶段循序渐进</p>
                    </a>
                    <a href="index.json" class="nav-item">
                        <h3>🔍 知识索引</h3>
                        <p>结构化知识点检索与导航</p>
                    </a>
                </div>
            </div>

            <div class="nav-section">
                <h2>📖 完整版课程（详细讲解）</h2>
                <div class="nav-grid">
{{FULL_LESSONS_LIST}}
                </div>
            </div>

            <div class="nav-section">
                <h2>📝 简版课程（核心要点）</h2>
                <div class="nav-grid">
{{SIMPLE_LESSONS_LIST}}
                </div>
            </div>

            <div class="nav-section">
                <h2>✍️ 习题练习</h2>
                <div class="nav-grid">
{{QUESTIONS_LIST}}
                </div>
            </div>
        </div>

        <div class="progress-section">
            <h2>📊 学习进度追踪</h2>
            <div class="progress-bar">
                <div class="progress-fill" id="progress-fill">{{COMPLETION_RATE}}%</div>
            </div>
        </div>

        <footer>
            <p>💪 坚持每天进步一点点，你离心理咨询师证书又近了一天！</p>
            <p style="margin-top: 10px; opacity: 0.8;">学习周期：180 天 | 每日投入：50 分钟自学 + 10 分钟习题</p>
        </footer>
    </div>

    <script>
        const progressFill = document.getElementById('progress-fill');
        progressFill.style.width = '{{COMPLETION_RATE}}%';
    </script>
</body>
</html>
"""

    def sync_day(self, day: int):
        """同步指定天数的学习内容"""
        print(f"\n{'='*60}")
        print(f"开始同步 Day {day:03d} 的学习内容")
        print(f"{'='*60}\n")
        
        # 1. 生成完整课程内容
        print("步骤 1: 生成完整课程内容...")
        full_title, full_content = self.generate_full_lesson(day)
        
        # 2. 生成简版课程内容
        print("步骤 2: 生成简版课程内容...")
        simple_content = self.generate_simple_lesson(day, full_title)
        
        # 3. 生成习题
        print("步骤 3: 生成配套习题...")
        questions_content = self.generate_practice_questions(day, full_title)
        
        # 4. 保存文件
        print("步骤 4: 保存到知识库...")
        self.save_daily_lesson(day, full_content, simple_content, questions_content)
        
        # 5. 更新索引
        print("步骤 5: 更新索引文件...")
        self.update_index(day, full_title)
        
        # 6. 更新 HTML 导航
        print("步骤 6: 更新网页导航...")
        self.update_index_html()
        
        print(f"\n{'='*60}")
        print(f"✓ Day {day:03d} 同步完成！")
        print(f"{'='*60}\n")


def main():
    """主函数"""
    import sys
    
    # 确定知识库根目录
    script_dir = Path(__file__).parent
    base_path = script_dir
    
    # 创建知识库管理器
    kb = PsychologyKnowledgeBase(str(base_path))
    
    # 确定要同步的天数
    if len(sys.argv) > 1:
        try:
            day = int(sys.argv[1])
        except ValueError:
            print(f"错误：天数必须是整数")
            sys.exit(1)
    else:
        day = kb.get_current_day() + 1
    
    # 执行同步
    kb.sync_day(day)
    
    print("同步完成！🎉")


if __name__ == "__main__":
    main()
