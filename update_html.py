#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
单独更新 index.html 的脚本
使用方法：python update_html.py
"""

import json
from pathlib import Path
from datetime import datetime

def update_html():
    """读取 index.json 并更新 index.html"""
    base_path = Path(__file__).parent
    index_path = base_path / "index.json"
    html_path = base_path / "index.html"
    
    # 加载索引
    with open(index_path, 'r', encoding='utf-8') as f:
        index_data = json.load(f)
    
    lessons = index_data.get("lessons", [])
    total_days = 180
    current_day = max([l.get("day", 0) for l in lessons], default=0)
    completion_rate = round((current_day / total_days) * 100)
    
    # 生成课程列表 HTML
    full_lessons_html = ""
    simple_lessons_html = ""
    questions_html = ""
    
    for lesson in sorted(lessons, key=lambda x: x.get("day", 0)):
        day = lesson.get("day", 0)
        title = lesson.get("title", "未知标题")
        date = lesson.get("date", "")
        
        # 完整版
        full_path = lesson.get("file_path", f"daily-lessons/day-{day:03d}-full.md")
        full_lessons_html += f'''<a href="{full_path}" class="nav-item">
                        <h3>Day {day:03d} - {title}（完整版）</h3>
                        <p>详细讲解（约 25,000 字） | 更新日期：{date}</p>
                    </a>
'''
        
        # 简版
        simple_path = lesson.get("simple_path", f"daily-lessons/day-{day:03d}.md")
        simple_lessons_html += f'''<a href="{simple_path}" class="nav-item">
                        <h3>Day {day:03d} - {title}（简版）</h3>
                        <p>核心要点速查 | 更新日期：{date}</p>
                    </a>
'''
        
        # 习题
        questions_path = lesson.get("questions_path", f"practice-questions/day-{day:03d}-questions.md")
        questions_html += f'''<a href="{questions_path}" class="nav-item">
                        <h3>Day {day:03d} 练习题</h3>
                        <p>10 道选择题 + 详细解析 | 更新日期：{date}</p>
                    </a>
'''
    
    # 读取 HTML 模板
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # 替换占位符
    html_content = html_content.replace('{{TOTAL_DAYS}}', str(len(lessons)))
    html_content = html_content.replace('{{CURRENT_DAY}}', str(current_day))
    html_content = html_content.replace('{{COMPLETION_RATE}}', str(completion_rate))
    html_content = html_content.replace('{{FULL_LESSONS_LIST}}', full_lessons_html)
    html_content = html_content.replace('{{SIMPLE_LESSONS_LIST}}', simple_lessons_html)
    html_content = html_content.replace('{{QUESTIONS_LIST}}', questions_html)
    
    # 保存
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✓ 已更新导航页面：{html_path}")
    print(f"  - 共 {len(lessons)} 天课程")
    print(f"  - 当前进度：Day {current_day}")
    print(f"  - 完成率：{completion_rate}%")

if __name__ == "__main__":
    update_html()
