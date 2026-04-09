"""
心理学知识库自动同步脚本

功能：
1. 根据学习进度生成当日学习内容
2. 将学习内容保存到知识库的 daily-lessons 目录
3. 生成配套习题并保存到 practice-questions 目录
4. 更新 index.json 索引文件
5. 按知识模块分类整理内容

使用方法：
    python sync_to_knowledge_base.py [day_number]
    
参数：
    day_number: 可选，指定学习天数。如果不提供，则从 index.json 读取当前进度
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path


class PsychologyKnowledgeBase:
    """心理学知识库管理器"""
    
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.index_path = self.base_path / "index.json"
        self.daily_lessons_path = self.base_path / "daily-lessons"
        self.practice_questions_path = self.base_path / "practice-questions"
        self.knowledge_modules_path = self.base_path / "knowledge-modules"
        
        # 确保目录存在
        self.daily_lessons_path.mkdir(exist_ok=True)
        self.practice_questions_path.mkdir(exist_ok=True)
        self.knowledge_modules_path.mkdir(exist_ok=True)
        
        # 加载索引
        self.index = self._load_index()
    
    def _load_index(self) -> dict:
        """加载索引文件"""
        if self.index_path.exists():
            with open(self.index_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # 创建默认索引
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
    
    def _save_index(self, index_data: dict):
        """保存索引文件"""
        with open(self.index_path, 'w', encoding='utf-8') as f:
            json.dump(index_data, f, ensure_ascii=False, indent=2)
    
    def get_current_day(self) -> int:
        """获取当前学习天数"""
        return self.index.get("current_day", 0)
    
    def get_stage_info(self, day: int) -> dict:
        """根据天数获取阶段信息"""
        cumulative_days = 0
        for stage in self.index["stages"]:
            cumulative_days += stage["duration_days"]
            if day <= cumulative_days:
                return {
                    "stage_id": stage["id"],
                    "stage_name": stage["name"],
                    "stage_number": stage["id"],
                    "day_in_stage": day - (cumulative_days - stage["duration_days"])
                }
        # 超出计划范围
        return {
            "stage_id": 6,
            "stage_name": "复习与冲刺",
            "stage_number": 6,
            "day_in_stage": day - 180
        }
    
    def generate_lesson_content(self, day: int) -> tuple[str, str]:
        """
        生成第 N 天的学习内容
        
        返回：(课程标题，课程内容 markdown)
        """
        stage_info = self.get_stage_info(day)
        today = datetime.now().strftime("%Y-%m-%d")
        
        # 根据阶段和天数生成内容
        content_generators = {
            1: self._generate_basic_psychology_lesson,
            2: self._generate_developmental_psychology_lesson,
            3: self._generate_social_psychology_lesson,
            4: self._generate_counseling_psychology_lesson,
            5: self._generate_diagnostic_psychology_lesson,
            6: self._generate_practical_skills_lesson
        }
        
        generator = content_generators.get(stage_info["stage_id"], self._generate_basic_psychology_lesson)
        title, content = generator(day, stage_info)
        
        # 填充模板
        lesson = f"""# Day {day:03d} - {title}

**学习日期**: {today}  
**所属阶段**: {stage_info['stage_name']} (第{stage_info['stage_number']}阶段)  
**建议学习时长**: 50 分钟

---

{content}

---

## 今日总结

[此处为今日学习的 200-300 字总结，概括核心知识点和学习收获]

---

## 下一步建议

1. **立即复习**: 花 5 分钟回顾今天的学习目标和重点概念
2. **完成习题**: 完成配套的 10 道练习题
3. **标记疑问**: 记录不理解的内容，后续重点复习
4. **明日预习**: 浏览明天的学习主题，建立知识联系

---

**元数据**:
- 阶段 ID: {stage_info['stage_id']}
- 天数：{day}
- 主题标签：[{self._get_tags_for_day(day, stage_info)}]
- 创建时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
- 最后更新：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""
        
        return title, lesson
    
    def _generate_basic_psychology_lesson(self, day: int, stage_info: dict) -> tuple[str, str]:
        """生成基础心理学阶段的学习内容"""
        topics = [
            ("心理学概述", "心理学的研究对象、方法和历史发展"),
            ("心理的神经生理机制", "神经系统结构与功能、脑与心理的关系"),
            ("感觉和知觉", "感觉的种类、知觉的特性"),
            ("意识和注意", "意识的状态、注意的类型和功能"),
            ("记忆", "记忆的过程、遗忘规律"),
            ("思维", "思维的种类、问题解决策略"),
            ("语言", "语言的结构、语言获得理论"),
            ("动机和需要", "动机的理论、需要的层次"),
            ("情绪和情感", "情绪的理论、情感的分类"),
            ("能力和人格", "能力的结构、人格理论")
        ]
        
        topic_idx = min((day - 1) // 3, len(topics) - 1)
        topic_title, topic_desc = topics[topic_idx]
        
        title = f"{topic_title}"
        
        content = f"""## 学习目标

通过今天的学习，你将能够：
1. 理解{topic_desc}的核心概念
2. 掌握相关的经典理论和实验
3. 运用所学知识解释日常心理现象

---

## 核心内容

### 一、{topic_title}的基本概念

【此处详细讲解{topic_title}的定义、内涵和外延，确保所有专业名词都有清晰定义】

### 二、主要理论和研究

【介绍与{topic_title}相关的重要理论，包括提出者、核心观点、实验依据】

### 三、实际应用

【说明{topic_title}在日常生活和心理咨询中的应用场景】

---

## 重点概念解析

- **概念 1**: 【明确定义 + 特征描述 + 具体示例】
- **概念 2**: 【明确定义 + 特征描述 + 具体示例】
- **概念 3**: 【明确定义 + 特征描述 + 具体示例】

---

## 易错点提醒

1. **易混淆点 1**: 【说明容易混淆的地方，并给出区分方法】
2. **易混淆点 2**: 【说明容易混淆的地方，并给出区分方法】

---

## 知识联系

- **与前期知识的联系**: 【说明与之前学习内容的关联】
- **为后续知识做铺垫**: 【说明对后续学习的帮助】
"""
        
        return title, content
    
    def _generate_developmental_psychology_lesson(self, day: int, stage_info: dict) -> tuple[str, str]:
        """生成发展心理学阶段的学习内容"""
        stages = [
            "胎儿期和婴儿期",
            "幼儿期",
            "童年期",
            "青春期",
            "青年期",
            "中年期",
            "老年期"
        ]
        
        stage_idx = min((day - 1) // 4, len(stages) - 1)
        stage_name = stages[stage_idx]
        
        title = f"{stage_name}心理发展"
        
        content = f"""## 学习目标

通过今天的学习，你将能够：
1. 了解{stage_name}的发展任务和关键特征
2. 掌握该阶段认知、情感、社会性发展的规律
3. 理解影响{stage_name}发展的因素

---

## 核心内容

### 一、{stage_name}的发展任务

【详细说明该发展阶段的主要任务和挑战】

### 二、认知发展特点

【描述该阶段的认知发展水平和特征】

### 三、情感和社会发展

【阐述该阶段的情感特点和社会性发展】

---

## 重点概念解析

- **关键期**: 【定义 + 在该阶段的具体表现】
- **发展任务**: 【定义 + 该阶段的核心任务】
- **心理理论**: 【定义 + 相关研究】

---

## 易错点提醒

1. 避免将发展阶段绝对化，个体差异始终存在
2. 区分年龄特征和个别差异
3. 注意文化背景对发展的影响

---

## 知识联系

- **与前期知识的联系**: 发展是连续性和阶段性的统一
- **为后续知识做铺垫**: 为理解毕生发展观奠定基础
"""
        
        return title, content
    
    def _generate_social_psychology_lesson(self, day: int, stage_info: dict) -> tuple[str, str]:
        """生成社会心理学阶段的学习内容"""
        topics = [
            "社会认知",
            "社会态度",
            "社会影响",
            "人际关系",
            "群体心理",
            "亲社会行为",
            "攻击行为"
        ]
        
        topic_idx = min((day - 1) // 4, len(topics) - 1)
        topic_title = topics[topic_idx]
        
        title = f"{topic_title}"
        
        content = f"""## 学习目标

通过今天的学习，你将能够：
1. 理解{topic_title}的基本概念和理论
2. 掌握相关的经典实验和研究
3. 运用社会心理学知识分析社会现象

---

## 核心内容

### 一、{topic_title}概述

【介绍基本概念和研究范畴】

### 二、经典理论和实验

【阐述重要理论和经典研究】

### 三、现实应用

【说明在实际生活中的应用】

---

## 重点概念解析

- **核心概念 1**: 【定义 + 特征 + 示例】
- **核心概念 2**: 【定义 + 特征 + 示例】

---

## 易错点提醒

1. 注意区分个体水平和社会水平的分析
2. 避免基本归因错误
3. 考虑情境因素的影响

---

## 知识联系

- **与前期知识的联系**: 个体心理是社会行为的基础
- **为后续知识做铺垫**: 为理解群体动力学做准备
"""
        
        return title, content
    
    def _generate_counseling_psychology_lesson(self, day: int, stage_info: dict) -> tuple[str, str]:
        """生成咨询心理学阶段的学习内容"""
        approaches = [
            "精神分析疗法",
            "行为疗法",
            "认知疗法",
            "人本主义疗法",
            "家庭治疗",
            "咨询过程和技术"
        ]
        
        approach_idx = min((day - 1) // 5, len(approaches) - 1)
        approach_name = approaches[approach_idx]
        
        title = f"{approach_name}"
        
        content = f"""## 学习目标

通过今天的学习，你将能够：
1. 了解{approach_name}的理论基础和核心假设
2. 掌握{approach_name}的主要技术和方法
3. 理解{approach_name}的适用范围和局限性

---

## 核心内容

### 一、理论基础

【介绍该疗法的理论渊源和基本假设】

### 二、核心技术

【详细说明主要的治疗技术和操作方法】

### 三、应用场景

【说明适用的心理问题和人群】

---

## 重点概念解析

- **专业术语 1**: 【定义 + 操作定义 + 示例】
- **专业术语 2**: 【定义 + 操作定义 + 示例】

---

## 易错点提醒

1. 不同疗法各有优劣，需根据来访者特点选择
2. 技术应用需遵循伦理规范
3. 重视咨访关系的建立

---

## 知识联系

- **与前期知识的联系**: 基于对心理过程和发展的理解
- **为后续知识做铺垫**: 为实践技能训练奠定基础
"""
        
        return title, content
    
    def _generate_diagnostic_psychology_lesson(self, day: int, stage_info: dict) -> tuple[str, str]:
        """生成心理诊断与测量阶段的学习内容"""
        topics = [
            "心理评估概述",
            "临床访谈技术",
            "心理测量学基础",
            "智力测验",
            "人格测验",
            "心理健康评估"
        ]
        
        topic_idx = min((day - 1) // 5, len(topics) - 1)
        topic_title = topics[topic_idx]
        
        title = f"{topic_title}"
        
        content = f"""## 学习目标

通过今天的学习，你将能够：
1. 理解{topic_title}的基本原理和方法
2. 掌握常用工具的使用和解释
3. 了解信度、效度等测量学指标

---

## 核心内容

### 一、基本原理

【介绍该领域的基本概念和原理】

### 二、常用工具

【说明常用的评估工具和测验】

### 三、结果解释

【讲解如何科学解释评估结果】

---

## 重点概念解析

- **信度**: 【定义 + 类型 + 影响因素】
- **效度**: 【定义 + 类型 + 验证方法】
- **常模**: 【定义 + 作用 + 建立方法】

---

## 易错点提醒

1. 测验结果需结合多方面信息综合判断
2. 避免对测验结果的绝对化解释
3. 严格遵守测验的伦理规范

---

## 知识联系

- **与前期知识的联系**: 基于对心理结构和功能的理解
- **为后续知识做铺垫**: 为案例分析和诊断做准备
"""
        
        return title, content
    
    def _generate_practical_skills_lesson(self, day: int, stage_info: dict) -> tuple[str, str]:
        """生成操作技能与综合应用阶段的学习内容"""
        topics = [
            "常见心理障碍识别",
            "危机干预技术",
            "综合案例分析",
            "咨询伦理规范",
            "考试技巧与策略"
        ]
        
        topic_idx = min((day - 1) // 6, len(topics) - 1)
        topic_title = topics[topic_idx]
        
        title = f"{topic_title}"
        
        content = f"""## 学习目标

通过今天的学习，你将能够：
1. 综合运用所学知识分析和解决问题
2. 掌握实践中的关键技能
3. 提升应试能力

---

## 核心内容

### 一、核心知识点

【梳理该主题的核心知识】

### 二、实践技能

【说明具体的操作方法和技巧】

### 三、案例分析

【通过典型案例加深理解】

---

## 重点概念解析

- **关键概念 1**: 【定义 + 应用要点】
- **关键概念 2**: 【定义 + 应用要点】

---

## 易错点提醒

1. 理论与实践相结合
2. 注意个体差异和文化敏感性
3. 严格遵守职业伦理

---

## 知识联系

- **与前期知识的联系**: 整合前面五个阶段的知识
- **为后续知识做铺垫**: 为实际工作和考试做准备
"""
        
        return title, content
    
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
   **解析**: 【详细解析，说明正确答案的依据和其他选项的错误原因】

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
    
    def save_daily_lesson(self, day: int, lesson_content: str, questions_content: str):
        """保存每日学习内容到知识库"""
        # 保存课程
        lesson_file = self.daily_lessons_path / f"day-{day:03d}.md"
        with open(lesson_file, 'w', encoding='utf-8') as f:
            f.write(lesson_content)
        
        # 保存习题
        questions_file = self.practice_questions_path / f"day-{day:03d}-questions.md"
        with open(questions_file, 'w', encoding='utf-8') as f:
            f.write(questions_content)
        
        print(f"✓ 已保存课程：{lesson_file}")
        print(f"✓ 已保存习题：{questions_file}")
    
    def update_index(self, day: int, title: str):
        """更新索引文件"""
        stage_info = self.get_stage_info(day)
        today = datetime.now().strftime("%Y-%m-%d")
        
        # 添加新课程记录
        lesson_record = {
            "day": day,
            "title": title,
            "stage_id": stage_info["stage_id"],
            "stage_name": stage_info["stage_name"],
            "date": today,
            "file_path": f"daily-lessons/day-{day:03d}.md",
            "questions_path": f"practice-questions/day-{day:03d}-questions.md",
            "tags": self._get_tags_for_day(day, stage_info).split(", "),
            "status": "completed"
        }
        
        # 检查是否已存在
        existing = next((l for l in self.index["lessons"] if l["day"] == day), None)
        if existing:
            existing.update(lesson_record)
        else:
            self.index["lessons"].append(lesson_record)
        
        # 更新当前进度
        if day > self.index["current_day"]:
            self.index["current_day"] = day
            # 更新阶段状态
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
        
        # 更新总数和时间
        self.index["total_lessons"] = len(self.index["lessons"])
        self.index["last_updated"] = today
        
        # 保存索引
        self._save_index(self.index)
        print(f"✓ 已更新索引文件")
    
    def sync_day(self, day: int = None):
        """同步指定天数的学习内容"""
        if day is None:
            day = self.get_current_day() + 1
        
        print(f"\n开始同步 Day {day} 的学习内容...")
        
        # 生成课程内容
        title, lesson_content = self.generate_lesson_content(day)
        print(f"✓ 已生成课程：{title}")
        
        # 生成习题
        questions_content = self.generate_practice_questions(day, title)
        print(f"✓ 已生成习题")
        
        # 保存到知识库
        self.save_daily_lesson(day, lesson_content, questions_content)
        
        # 更新索引
        self.update_index(day, title)
        
        print(f"\n✅ Day {day} 学习内容已成功加入知识库！")
        return day


def main():
    """主函数"""
    kb_path = Path(__file__).parent
    kb = PsychologyKnowledgeBase(kb_path)
    
    # 从命令行参数获取天数，或自动递增
    if len(sys.argv) > 1:
        try:
            day = int(sys.argv[1])
        except ValueError:
            print(f"错误：无效的天数参数 '{sys.argv[1]}'")
            print(f"用法：python {sys.argv[0]} [day_number]")
            sys.exit(1)
    else:
        day = None
    
    # 执行同步
    synced_day = kb.sync_day(day)
    
    # 输出摘要信息
    print("\n" + "="*50)
    print("知识库同步完成")
    print("="*50)
    print(f"当前进度：Day {synced_day}")
    print(f"总课程数：{kb.index['total_lessons']}")
    print(f"当前阶段：{kb.index['current_stage']} - {kb.index['stages'][kb.index['current_stage']-1]['name']}")
    print("="*50)


if __name__ == "__main__":
    main()
