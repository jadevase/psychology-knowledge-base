#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
从 index.json 生成完整的 index.html
使用方法：python generate_html.py
"""

import json
from pathlib import Path
from datetime import datetime

def generate_html():
    """读取 index.json 并生成完整的 index.html"""
    base_path = Path(__file__).parent
    index_path = base_path / "index.json"
    html_path = base_path / "index.html"
    
    # 加载索引
    with open(index_path, 'r', encoding='utf-8') as f:
        index_data = json.load(f)
    
    lessons = index_data.get("lessons", [])
    total_days = 180
    current_day = index_data.get("current_day", max([l.get("day", 0) for l in lessons], default=0))
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
        full_lessons_html += f'''                    <a href="{full_path}" class="nav-item">
                        <h3>Day {day:03d} - {title}（完整版）</h3>
                        <p>详细讲解（约 25,000 字） | 更新日期：{date}</p>
                    </a>
'''
        
        # 简版
        simple_path = lesson.get("simple_path", f"daily-lessons/day-{day:03d}.md")
        simple_lessons_html += f'''                    <a href="{simple_path}" class="nav-item">
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
    
    # 生成完整的 HTML
    html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>心理咨询师考试知识库</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        header {{
            text-align: center;
            color: white;
            padding: 40px 20px;
        }}
        header h1 {{ font-size: 2.5em; margin-bottom: 10px; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }}
        header p {{ font-size: 1.2em; opacity: 0.9; }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }}
        .stat-card {{
            background: white;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .stat-number {{ font-size: 2.5em; font-weight: bold; color: #667eea; }}
        .stat-label {{ color: #666; margin-top: 5px; }}
        .main-nav {{
            background: white;
            border-radius: 10px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .nav-section {{ margin-bottom: 30px; }}
        .nav-section h2 {{
            color: #333;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }}
        .nav-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 15px;
        }}
        .nav-item {{
            display: block;
            padding: 20px;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            border-radius: 8px;
            text-decoration: none;
            color: #333;
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        .nav-item:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        }}
        .nav-item h3 {{ color: #667eea; margin-bottom: 8px; font-size: 1.1em; }}
        .nav-item p {{ font-size: 0.9em; color: #666; }}
        .progress-section {{
            background: white;
            border-radius: 10px;
            padding: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .progress-section h2 {{ color: #333; margin-bottom: 20px; }}
        .progress-bar {{
            background: #e0e0e0;
            border-radius: 10px;
            height: 30px;
            overflow: hidden;
            margin: 20px 0;
        }}
        .progress-fill {{
            background: linear-gradient(90deg, #667eea, #764ba2);
            height: 100%;
            width: 0%;
            transition: width 0.5s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
        }}
        footer {{
            text-align: center;
            color: white;
            margin-top: 40px;
            padding: 20px;
        }}
        @media (max-width: 768px) {{
            header h1 {{ font-size: 1.8em; }}
            .stats {{ grid-template-columns: repeat(2, 1fr); }}
            .nav-grid {{ grid-template-columns: 1fr; }}
        }}
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
                <div class="stat-number">{len(lessons)}</div>
                <div class="stat-label">已发布课程</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{current_day}</div>
                <div class="stat-label">当前进度（天）</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{completion_rate}%</div>
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
{full_lessons_html}
                </div>
            </div>

            <div class="nav-section">
                <h2>📝 简版课程（核心要点）</h2>
                <div class="nav-grid">
{simple_lessons_html}
                </div>
            </div>

            <div class="nav-section">
                <h2>✍️ 习题练习</h2>
                <div class="nav-grid">
{questions_html}
                </div>
            </div>
        </div>

        <div class="progress-section">
            <h2>📊 学习进度追踪</h2>
            <div class="progress-bar">
                <div class="progress-fill" id="progress-fill">{completion_rate}%</div>
            </div>
        </div>

        <footer>
            <p>💪 坚持每天进步一点点，你离心理咨询师证书又近了一天！</p>
            <p style="margin-top: 10px; opacity: 0.8;">学习周期：180 天 | 每日投入：50 分钟自学 + 10 分钟习题</p>
        </footer>
    </div>

    <script>
        const progressFill = document.getElementById('progress-fill');
        progressFill.style.width = '{completion_rate}%';
    </script>
</body>
</html>
'''
    
    # 保存
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✓ 已生成导航页面：{html_path}")
    print(f"  - 共 {len(lessons)} 天课程")
    print(f"  - 当前进度：Day {current_day}")
    print(f"  - 完成率：{completion_rate}%")

if __name__ == "__main__":
    generate_html()
