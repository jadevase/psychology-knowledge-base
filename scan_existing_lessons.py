"""
扫描现有课程文件并更新索引
"""
import json
import re
from pathlib import Path
from datetime import datetime

base_path = Path(__file__).parent
daily_lessons_path = base_path / "daily-lessons"
practice_questions_path = base_path / "practice-questions"
index_path = base_path / "index.json"

# 加载现有索引
with open(index_path, 'r', encoding='utf-8') as f:
    index = json.load(f)

# 扫描每日课程文件
lessons = []
for lesson_file in sorted(daily_lessons_path.glob("day-*.md")):
    filename = lesson_file.name
    
    # 跳过模板文件
    if "template" in filename:
        continue
    
    # 提取天数
    match = re.match(r"day-(\d+)(?:-full)?\.md", filename)
    if not match:
        continue
    
    day = int(match.group(1))
    is_full = "-full" in filename
    
    # 检查是否已存在
    existing = next((l for l in lessons if l["day"] == day), None)
    
    if not existing:
        # 读取文件标题
        with open(lesson_file, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()
            title_match = re.search(r"Day \d+ - (.+?)(?:（.+）)?$", first_line)
            title = title_match.group(1) if title_match else f"第{day}天课程"
        
        # 确定阶段
        if day <= 30:
            stage_id, stage_name = 1, "基础心理学"
        elif day <= 60:
            stage_id, stage_name = 2, "发展心理学"
        elif day <= 90:
            stage_id, stage_name = 3, "社会心理学"
        elif day <= 120:
            stage_id, stage_name = 4, "咨询心理学"
        elif day <= 150:
            stage_id, stage_name = 5, "心理诊断与测量"
        else:
            stage_id, stage_name = 6, "操作技能与综合应用"
        
        lesson_record = {
            "day": day,
            "title": title,
            "stage_id": stage_id,
            "stage_name": stage_name,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "file_path": f"daily-lessons/day-{day:03d}-full.md",
            "simple_path": f"daily-lessons/day-{day:03d}.md",
            "questions_path": f"practice-questions/day-{day:03d}-questions.md",
            "tags": ["基础心理学", "心理学基础"],
            "status": "completed"
        }
        lessons.append(lesson_record)

# 按天数排序
lessons.sort(key=lambda x: x["day"])

# 更新索引
index["lessons"] = lessons
index["total_lessons"] = len(lessons)
index["current_day"] = max([l["day"] for l in lessons]) if lessons else 0
index["last_updated"] = datetime.now().strftime("%Y-%m-%d")

# 保存索引
with open(index_path, 'w', encoding='utf-8') as f:
    json.dump(index, f, ensure_ascii=False, indent=2)

print(f"✓ 扫描完成！共发现 {len(lessons)} 天的课程")
for lesson in lessons:
    print(f"  - Day {lesson['day']:03d}: {lesson['title']}")

print(f"\n✓ 索引文件已更新：{index_path}")
