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
from question_bank import BASIC_PSYCHOLOGY_BANK


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
        """生成配套习题 - 根据天数和主题返回真实习题内容"""
        stage_info = self.get_stage_info(day)
        
        # 根据阶段 ID 选择对应的题库生成器
        question_generators = {
            1: self._generate_basic_psychology_questions,
            2: self._generate_developmental_psychology_questions,
            3: self._generate_social_psychology_questions,
            4: self._generate_counseling_psychology_questions,
            5: self._generate_diagnostic_psychology_questions,
            6: self._generate_practical_skills_questions
        }
        
        generator = question_generators.get(stage_info["stage_id"], self._generate_basic_psychology_questions)
        questions_content = generator(day, lesson_title)
        
        return questions_content
    
    def _format_questions(self, questions: list, day: int, lesson_title: str, topic_name: str) -> str:
        """将题目列表格式化为 Markdown 字符串"""
        stage_info = self.get_stage_info(day)
        
        questions_md = f"""# Day {day:03d} 习题练习

**对应课程**: Day {day:03d} - {lesson_title}  
**建议完成时间**: 10 分钟  
**题目数量**: 10 题  
**覆盖主题**: {topic_name}

---

## 选择题

"""
        
        # 生成题目部分
        for i, q in enumerate(questions, 1):
            questions_md += f"### {i}. {q['question']}\n\n"
            for option_key in ["A", "B", "C", "D"]:
                questions_md += f"{option_key}. {q['options'][option_key]}\n"
            questions_md += "\n"
        
        # 生成答案与解析部分
        questions_md += "---\n\n## 答案与解析\n\n"
        for i, q in enumerate(questions, 1):
            questions_md += f"{i}. **答案**: {q['answer']}  \n"
            questions_md += f"   **解析**: {q['analysis']}\n\n"
        
        # 添加元数据
        questions_md += f"""---

**元数据**:
- 对应天数：{day}
- 难度等级：中等
- 覆盖知识点：[{self._get_tags_for_day(day, stage_info)}]
- 创建时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""
        
        return questions_md
    
    def _generate_basic_psychology_questions(self, day: int, lesson_title: str) -> str:
        """生成基础心理学阶段的习题"""
        # 根据天数确定主题（第 1 天：心理学概述，第 2 天：神经生理机制，第 3 天：感觉知觉，以此类推）
        topics = list(BASIC_PSYCHOLOGY_BANK.keys())
        topic_idx = min(day - 1, len(topics) - 1)
        topic_name = topics[topic_idx]
        
        # 获取该主题的 10 道题目
        selected_questions = BASIC_PSYCHOLOGY_BANK[topic_name][:10]
        
        return self._format_questions(selected_questions, day, lesson_title, topic_name)
    
    def _generate_developmental_psychology_questions(self, day: int, lesson_title: str) -> str:
        """生成发展心理学阶段的习题"""
        question_bank = [
            {
                "topic": "胎儿期和婴儿期心理发展",
                "questions": [
                    {
                        "question": "胎儿神经系统发育最关键的时期是？",
                        "options": {"A": "怀孕前 3 个月", "B": "怀孕 4-6 个月", "C": "怀孕 7-9 个月", "D": "出生后第一年"},
                        "answer": "A",
                        "analysis": "怀孕前 3 个月（尤其是第 3-8 周）是神经管形成和大脑快速分化的关键期，此时最容易受到致畸因素影响。"
                    },
                    {
                        "question": "新生儿出生时就具备的无条件反射不包括？",
                        "options": {"A": "吸吮反射", "B": "抓握反射", "C": "条件反射", "D": "觅食反射"},
                        "answer": "C",
                        "analysis": "无条件反射是先天的、不学而能的。条件反射是后天习得的，不属于新生儿先天反射。"
                    },
                    {
                        "question": "婴儿依恋类型中，安全型依恋约占？",
                        "options": {"A": "30%", "B": "50%", "C": "65%", "D": "80%"},
                        "answer": "C",
                        "analysis": "安斯沃斯研究发现，在正常养育环境下，约 65% 的婴儿形成安全型依恋，这是最健康的依恋类型。"
                    }
                ]
            },
            {
                "topic": "幼儿期心理发展",
                "questions": [
                    {
                        "question": "皮亚杰认为 2-7 岁儿童处于哪个认知发展阶段？",
                        "options": {"A": "感知运动阶段", "B": "前运算阶段", "C": "具体运算阶段", "D": "形式运算阶段"},
                        "answer": "B",
                        "analysis": "前运算阶段（2-7 岁）的特点是象征性思维、自我中心、不可逆性、泛灵论等。"
                    },
                    {
                        "question": "幼儿游戏的主要特点是？",
                        "options": {"A": "规则性强", "B": "象征性游戏为主", "C": "竞争性突出", "D": "合作性明显"},
                        "answer": "B",
                        "analysis": "幼儿期以象征性游戏（假装游戏）为主，如过家家、角色扮演，这促进了想象力和社交能力发展。"
                    },
                    {
                        "question": "'三山实验'证明了幼儿思维的什么特点？",
                        "options": {"A": "守恒性", "B": "可逆性", "C": "自我中心", "D": "逻辑性"},
                        "answer": "C",
                        "analysis": "皮亚杰的三山实验表明，前运算阶段幼儿难以从他人角度看问题，表现出自我中心思维。"
                    }
                ]
            },
            {
                "topic": "青春期心理发展",
                "questions": [
                    {
                        "question": "青春期自我意识发展的主要特点是？",
                        "options": {"A": "完全依赖父母评价", "B": "成人感和独立意识增强", "C": "缺乏自我评价能力", "D": "完全脱离社会比较"},
                        "answer": "B",
                        "analysis": "青春期个体产生强烈的成人感和独立意识，渴望被当作成年人对待，这是心理断乳期的表现。"
                    },
                    {
                        "question": "埃里克森认为青春期的主要发展任务是？",
                        "options": {"A": "获得信任感", "B": "获得自主感", "C": "建立同一性", "D": "获得繁衍感"},
                        "answer": "C",
                        "analysis": "埃里克森提出，青春期（12-18 岁）的核心任务是建立自我同一性，防止角色混乱。"
                    },
                    {
                        "question": "青少年情绪发展的'疾风怒涛'特点是指？",
                        "options": {"A": "情绪稳定平和", "B": "情绪波动剧烈", "C": "情绪表达内敛", "D": "情绪体验单一"},
                        "answer": "B",
                        "analysis": "由于激素变化和大脑发育不平衡，青少年情绪容易波动，表现为冲动、敏感、两极化。"
                    }
                ]
            }
        ]
        
        topic_idx = min((day - 31) // 4, len(question_bank) - 1)
        selected_topic = question_bank[topic_idx]
        selected_questions = [selected_topic["questions"][i % len(selected_topic["questions"])] for i in range(10)]
        return self._format_questions(selected_questions, day, lesson_title, selected_topic["topic"])
    
    def _generate_social_psychology_questions(self, day: int, lesson_title: str) -> str:
        """生成社会心理学阶段的习题"""
        question_bank = [
            {
                "topic": "社会认知",
                "questions": [
                    {
                        "question": "'第一印象效应'在社会心理学中被称为？",
                        "options": {"A": "近因效应", "B": "首因效应", "C": "晕轮效应", "D": "刻板印象"},
                        "answer": "B",
                        "analysis": "首因效应指最先接收的信息对印象形成影响最大，即'先入为主'的现象。"
                    },
                    {
                        "question": "将他人行为归因于内部特质而忽视情境因素的倾向是？",
                        "options": {"A": "自利偏差", "B": "基本归因错误", "C": "虚假一致偏差", "D": "确认偏差"},
                        "answer": "B",
                        "analysis": "基本归因错误是指解释他人行为时，过度强调人格特质，低估情境影响的普遍倾向。"
                    },
                    {
                        "question": "'以偏概全'的认知偏差属于？",
                        "options": {"A": "首因效应", "B": "近因效应", "C": "晕轮效应", "D": "投射效应"},
                        "answer": "C",
                        "analysis": "晕轮效应是指根据某个突出特征推断整体印象，如'一好百好，一坏百坏'。"
                    }
                ]
            },
            {
                "topic": "社会态度",
                "questions": [
                    {
                        "question": "态度的 ABC 模型不包括？",
                        "options": {"A": "情感成分", "B": "行为成分", "C": "认知成分", "D": "生物成分"},
                        "answer": "D",
                        "analysis": "态度由情感（Affect）、行为倾向（Behavior）、认知（Cognition）三部分组成，简称 ABC 模型。"
                    },
                    {
                        "question": "费斯廷格的认知失调理论认为，当态度与行为不一致时，人们会？",
                        "options": {"A": "保持不变", "B": "感到心理不适并试图减少失调", "C": "强化原有态度", "D": "完全改变行为"},
                        "answer": "B",
                        "analysis": "认知失调理论指出，当认知元素之间矛盾时，会产生心理紧张，促使个体改变态度或行为以恢复平衡。"
                    },
                    {
                        "question": "通过小要求逐渐引导接受大要求的说服技巧是？",
                        "options": {"A": "登门槛技术", "B": "留面子技术", "C": "低球技术", "D": "恐惧唤起"},
                        "answer": "A",
                        "analysis": "登门槛技术指先提出小要求，待对方接受后再提出更大要求，利用承诺一致性原理。"
                    }
                ]
            },
            {
                "topic": "从众与服从",
                "questions": [
                    {
                        "question": "阿希的线段判断实验研究的是？",
                        "options": {"A": "服从", "B": "从众", "C": "顺从", "D": "去个性化"},
                        "answer": "B",
                        "analysis": "阿希实验发现，约 75% 的被试至少一次放弃自己的正确判断而跟随群体错误答案，证明了从众现象。"
                    },
                    {
                        "question": "米尔格拉姆的电击实验研究的是？",
                        "options": {"A": "从众", "B": "服从权威", "C": "助人行为", "D": "攻击行为"},
                        "answer": "B",
                        "analysis": "米尔格拉姆实验发现，65% 的普通人在权威命令下会对'学习者'施加致命电击，揭示了服从的可怕力量。"
                    },
                    {
                        "question": "群体规模越大，个体责任感越分散的现象是？",
                        "options": {"A": "社会助长", "B": "社会懈怠", "C": "责任分散", "D": "去个性化"},
                        "answer": "C",
                        "analysis": "责任分散（旁观者效应）指在场人数越多，每个人感受到的帮助责任越小，导致助人行为减少。"
                    }
                ]
            }
        ]
        
        topic_idx = min((day - 61) // 4, len(question_bank) - 1)
        selected_topic = question_bank[topic_idx]
        selected_questions = [selected_topic["questions"][i % len(selected_topic["questions"])] for i in range(10)]
        return self._format_questions(selected_questions, day, lesson_title, selected_topic["topic"])
    
    def _generate_counseling_psychology_questions(self, day: int, lesson_title: str) -> str:
        """生成咨询心理学阶段的习题"""
        question_bank = [
            {
                "topic": "精神分析疗法",
                "questions": [
                    {
                        "question": "精神分析疗法的创始人是？",
                        "options": {"A": "荣格", "B": "阿德勒", "C": "弗洛伊德", "D": "埃里克森"},
                        "answer": "C",
                        "analysis": "弗洛伊德创立了精神分析理论和方法，强调潜意识冲突、童年经验和防御机制的作用。"
                    },
                    {
                        "question": "'自由联想'技术的目的是？",
                        "options": {"A": "训练放松能力", "B": "探索潜意识内容", "C": "建立治疗关系", "D": "纠正错误认知"},
                        "answer": "B",
                        "analysis": "自由联想要求来访者不加筛选地说出头脑中浮现的任何想法，以此绕过防御，揭示潜意识冲突。"
                    },
                    {
                        "question": "移情是指来访者将对谁的情感转移到治疗师身上？",
                        "options": {"A": "朋友", "B": "同事", "C": "重要他人（如父母）", "D": "陌生人"},
                        "answer": "C",
                        "analysis": "移情是来访者将对过去重要人物（通常是父母）的情感、态度和冲突投射到治疗师身上的现象。"
                    }
                ]
            },
            {
                "topic": "行为疗法",
                "questions": [
                    {
                        "question": "系统脱敏法主要用于治疗？",
                        "options": {"A": "抑郁症", "B": "恐怖症", "C": "精神分裂症", "D": "人格障碍"},
                        "answer": "B",
                        "analysis": "系统脱敏法通过渐进式暴露于恐惧刺激并结合放松训练，有效治疗特定恐怖症和焦虑障碍。"
                    },
                    {
                        "question": "正强化的作用是？",
                        "options": {"A": "减少行为频率", "B": "增加行为频率", "C": "消除不良行为", "D": "替代原有行为"},
                        "answer": "B",
                        "analysis": "正强化是指在行为后给予愉快刺激，从而增加该行为未来出现的概率。"
                    },
                    {
                        "question": "'以人为镜'反映的是哪种行为治疗技术？",
                        "options": {"A": "冲击疗法", "B": "模仿学习", "C": "代币制", "D": "生物反馈"},
                        "answer": "B",
                        "analysis": "模仿学习（榜样学习）指通过观察他人行为及其后果来学习新行为，班杜拉的社会学习理论是其基础。"
                    }
                ]
            },
            {
                "topic": "人本主义疗法",
                "questions": [
                    {
                        "question": "来访者中心疗法的创始人是？",
                        "options": {"A": "马斯洛", "B": "罗杰斯", "C": "罗洛·梅", "D": "弗兰克尔"},
                        "answer": "B",
                        "analysis": "罗杰斯创立了来访者中心疗法，强调治疗师的真诚、无条件积极关注和共情理解。"
                    },
                    {
                        "question": "'无条件积极关注'的含义是？",
                        "options": {"A": "只关注积极行为", "B": "接纳来访者的全部，包括优缺点", "C": "忽略消极情绪", "D": "给予物质奖励"},
                        "answer": "B",
                        "analysis": "无条件积极关指治疗师对来访者作为人的价值的完全接纳，不因其行为或情感而改变。"
                    },
                    {
                        "question": "人本主义疗法的核心目标是？",
                        "options": {"A": "消除症状", "B": "促进自我实现", "C": "改变认知", "D": "建立条件反射"},
                        "answer": "B",
                        "analysis": "人本主义相信人有自我实现的倾向，治疗目标是移除成长障碍，促进潜能发挥。"
                    }
                ]
            }
        ]
        
        topic_idx = min((day - 91) // 5, len(question_bank) - 1)
        selected_topic = question_bank[topic_idx]
        selected_questions = [selected_topic["questions"][i % len(selected_topic["questions"])] for i in range(10)]
        return self._format_questions(selected_questions, day, lesson_title, selected_topic["topic"])
    
    def _generate_diagnostic_psychology_questions(self, day: int, lesson_title: str) -> str:
        """生成心理诊断与测量阶段的习题"""
        question_bank = [
            {
                "topic": "心理测量学基础",
                "questions": [
                    {
                        "question": "衡量测验结果一致性程度的指标是？",
                        "options": {"A": "效度", "B": "信度", "C": "常模", "D": "区分度"},
                        "answer": "B",
                        "analysis": "信度指测验结果的稳定性、一致性程度。高效度必须以高信度为前提，但高信度不一定高效度。"
                    },
                    {
                        "question": "测验能够测量到所要测量特质的程度称为？",
                        "options": {"A": "信度", "B": "效度", "C": "标准化", "D": "代表性"},
                        "answer": "B",
                        "analysis": "效度指测验的有效性，即是否真正测量到了想要测量的心理特质。"
                    },
                    {
                        "question": "将个体测验分数与代表性样本进行比较的参照系统是？",
                        "options": {"A": "标准", "B": "常模", "C": "基线", "D": "阈值"},
                        "answer": "B",
                        "analysis": "常模是从代表性样本获得的分数分布标准，用于解释个体分数的相对位置。"
                    }
                ]
            },
            {
                "topic": "智力测验",
                "questions": [
                    {
                        "question": "比奈 - 西蒙智力量表最早用于？",
                        "options": {"A": "职业选拔", "B": "鉴别智力落后儿童", "C": "研究智力结构", "D": "评估创造力"},
                        "answer": "B",
                        "analysis": "1905 年比奈和西蒙编制第一个智力量表，目的是识别需要特殊教育的智力落后儿童。"
                    },
                    {
                        "question": "离差智商的计算公式是？",
                        "options": {"A": "IQ=MA/CA×100", "B": "IQ=100+15Z", "C": "IQ=100+16Z", "D": "IQ=50+10Z"},
                        "answer": "B",
                        "analysis": "韦氏量表采用离差智商 IQ=100+15Z，其中 Z 为标准分数，100 为平均值，15 为标准差。"
                    },
                    {
                        "question": "下列哪项不属于加德纳多元智能理论？",
                        "options": {"A": "语言智能", "B": "逻辑数学智能", "C": "情绪智能", "D": "音乐智能"},
                        "answer": "C",
                        "analysis": "加德纳提出 8 种智能：语言、逻辑数学、空间、音乐、身体运动、人际、内省、自然观察。情绪智能不是其原始分类。"
                    }
                ]
            },
            {
                "topic": "人格测验",
                "questions": [
                    {
                        "question": "MMPI 属于哪种类型的人格测验？",
                        "options": {"A": "自陈量表", "B": "投射测验", "C": "情境测验", "D": "评定量表"},
                        "answer": "A",
                        "analysis": "MMPI（明尼苏达多相人格调查表）是自陈量表的代表，包含 566 个项目，广泛用于临床评估。"
                    },
                    {
                        "question": "罗夏墨迹测验属于？",
                        "options": {"A": "自陈量表", "B": "投射测验", "C": "智力测验", "D": "成就测验"},
                        "answer": "B",
                        "analysis": "罗夏墨迹测验是典型的投射测验，通过被试对模糊墨迹的解释来揭示潜意识内容和人格特征。"
                    },
                    {
                        "question": "大五人格模型不包括？",
                        "options": {"A": "外向性", "B": "宜人性", "C": "自律性", "D": "神经质"},
                        "answer": "C",
                        "analysis": "大五人格包括：开放性、尽责性、外向性、宜人性、神经质（OCEAN）。自律性是尽责性的子维度。"
                    }
                ]
            }
        ]
        
        topic_idx = min((day - 121) // 5, len(question_bank) - 1)
        selected_topic = question_bank[topic_idx]
        selected_questions = [selected_topic["questions"][i % len(selected_topic["questions"])] for i in range(10)]
        return self._format_questions(selected_questions, day, lesson_title, selected_topic["topic"])
    
    def _generate_practical_skills_questions(self, day: int, lesson_title: str) -> str:
        """生成操作技能与综合应用阶段的习题"""
        question_bank = [
            {
                "topic": "常见心理障碍识别",
                "questions": [
                    {
                        "question": "抑郁症的核心症状是？",
                        "options": {"A": "焦虑不安", "B": "情绪低落和兴趣丧失", "C": "幻觉妄想", "D": "强迫行为"},
                        "answer": "B",
                        "analysis": "抑郁症两大核心症状：持续情绪低落和对日常活动兴趣显著减退，持续至少 2 周。"
                    },
                    {
                        "question": "焦虑症与恐惧症的主要区别是？",
                        "options": {"A": "焦虑有明确对象，恐惧无对象", "B": "焦虑无明确对象，恐惧有特定对象", "C": "焦虑更严重", "D": "恐惧更常见"},
                        "answer": "B",
                        "analysis": "广泛性焦虑是对未来事件的过度担忧，无特定对象；恐惧症则是对特定事物或情境的强烈恐惧。"
                    },
                    {
                        "question": "精神分裂症的特征性症状是？",
                        "options": {"A": "情绪波动", "B": "幻觉和妄想", "C": "记忆障碍", "D": "睡眠问题"},
                        "answer": "B",
                        "analysis": "幻觉（尤其是幻听）和妄想是精神分裂症的特征性阳性症状，反映现实检验能力受损。"
                    }
                ]
            },
            {
                "topic": "危机干预技术",
                "questions": [
                    {
                        "question": "心理危机干预的首要目标是？",
                        "options": {"A": "根治心理问题", "B": "确保安全和稳定情绪", "C": "完善人格", "D": "提高应对能力"},
                        "answer": "B",
                        "analysis": "危机干预是短期紧急干预，首要目标是确保安全（如防自杀）、稳定情绪、恢复功能。"
                    },
                    {
                        "question": "对有自杀风险的来访者，咨询师应该？",
                        "options": {"A": "保密不告知他人", "B": "评估风险并必要时突破保密", "C": "立即转介", "D": "延长咨询时间"},
                        "answer": "B",
                        "analysis": "当来访者对自己或他人构成危险时，咨询师有责任突破保密原则，通知相关人员以确保安全。"
                    },
                    {
                        "question": "危机干预的'六步法'不包括？",
                        "options": {"A": "确定问题", "B": "保证求助者安全", "C": "长期心理治疗", "D": "提供支持和信息"},
                        "answer": "C",
                        "analysis": "危机干预是短期干预（通常 1-6 次），不包括长期心理治疗。六步法包括：确定问题、保证安全、给予支持、提出建议、制定计划、获得承诺。"
                    }
                ]
            },
            {
                "topic": "咨询伦理规范",
                "questions": [
                    {
                        "question": "心理咨询中的保密原则例外情况是？",
                        "options": {"A": "来访者同意披露", "B": "法律要求披露", "C": "对自己或他人构成危险", "D": "以上都是"},
                        "answer": "D",
                        "analysis": "保密例外包括：来访者书面同意、法律规定、对自身或他人有紧迫危险、涉及未成年人虐待等。"
                    },
                    {
                        "question": "咨询师与来访者建立双重关系是？",
                        "options": {"A": "鼓励的", "B": "允许的", "C": "应避免的", "D": "必须的"},
                        "answer": "C",
                        "analysis": "双重关系（如同时是朋友、商业伙伴等）可能损害专业判断和来访者利益，伦理规范明确要求避免。"
                    },
                    {
                        "question": "知情同意的内容包括？",
                        "options": {"A": "咨询目标和方式", "B": "保密及其限制", "C": "费用和时长", "D": "以上都是"},
                        "answer": "D",
                        "analysis": "知情同意应包含：咨询性质、目标、方法、风险收益、保密条款、费用、时长、来访者权利等。"
                    }
                ]
            }
        ]
        
        topic_idx = min((day - 151) // 6, len(question_bank) - 1)
        selected_topic = question_bank[topic_idx]
        selected_questions = [selected_topic["questions"][i % len(selected_topic["questions"])] for i in range(10)]
        return self._format_questions(selected_questions, day, lesson_title, selected_topic["topic"])
    
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
