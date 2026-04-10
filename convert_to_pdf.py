"""
Markdown 转 PDF 转换脚本
使用 markdown 和 weasyprint 库将 Markdown 文件转换为 PDF
"""

import os
from pathlib import Path
from datetime import datetime

# 检查并安装必要的库
def install_packages():
    """安装必要的 Python 包"""
    import subprocess
    packages = ['markdown', 'weasyprint']
    for pkg in packages:
        try:
            __import__(pkg)
        except ImportError:
            print(f"正在安装 {pkg}...")
            subprocess.check_call(['pip', 'install', pkg, '-i', 'https://pypi.tuna.tsinghua.edu.cn/simple'])
    print("所有依赖包已安装完成")

def convert_md_to_pdf(md_file, output_dir):
    """将单个 Markdown 文件转换为 PDF"""
    from markdown import markdown
    from weasyprint import HTML, CSS
    
    # 读取 Markdown 文件
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # 转换为 HTML
    html_content = markdown(md_content, extensions=[
        'extra',           # 支持表格、定义列表等
        'codehilite',      # 代码高亮
        'toc',             # 目录
        'nl2br',           # 换行符转<br>
    ])
    
    # 添加 CSS 样式
    css = CSS(string='''
        @page {
            size: A4;
            margin: 2cm;
        }
        
        body {
            font-family: "Microsoft YaHei", "SimSun", serif;
            line-height: 1.8;
            font-size: 12pt;
            color: #333;
        }
        
        h1 {
            font-size: 24pt;
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
            page-break-after: avoid;
        }
        
        h2 {
            font-size: 18pt;
            color: #34495e;
            margin-top: 30px;
            page-break-after: avoid;
        }
        
        h3 {
            font-size: 14pt;
            color: #7f8c8d;
            page-break-after: avoid;
        }
        
        h4, h5, h6 {
            font-size: 12pt;
            color: #95a5a6;
            page-break-after: avoid;
        }
        
        p {
            text-align: justify;
            margin: 10px 0;
        }
        
        ul, ol {
            margin: 10px 0;
            padding-left: 30px;
        }
        
        li {
            margin: 5px 0;
        }
        
        code {
            background-color: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: "Consolas", "Courier New", monospace;
            font-size: 10pt;
        }
        
        pre {
            background-color: #f8f8f8;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #3498db;
            overflow-x: auto;
            page-break-inside: avoid;
        }
        
        blockquote {
            border-left: 4px solid #3498db;
            padding-left: 20px;
            margin: 15px 0;
            color: #7f8c8d;
            font-style: italic;
        }
        
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
            page-break-inside: auto;
        }
        
        th, td {
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }
        
        th {
            background-color: #3498db;
            color: white;
            font-weight: bold;
        }
        
        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        
        strong {
            font-weight: bold;
            color: #2c3e50;
        }
        
        em {
            font-style: italic;
        }
        
        hr {
            border: none;
            border-top: 1px solid #ddd;
            margin: 30px 0;
        }
        
        a {
            color: #3498db;
            text-decoration: none;
        }
        
        .header-info {
            background-color: #ecf0f1;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 30px;
        }
    ''')
    
    # 完整的 HTML 文档
    full_html = f'''
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <title>心理学课程 - {Path(md_file).stem}</title>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    '''
    
    # 生成 PDF
    html_doc = HTML(string=full_html)
    pdf_path = output_dir / f"{Path(md_file).stem}.pdf"
    html_doc.write_pdf(pdf_path, stylesheets=[css])
    
    return pdf_path

def main():
    """主函数"""
    base_path = Path(__file__).parent
    
    # 输入文件
    md_files = [
        base_path / "daily-lessons" / "day-001-full.md",
        base_path / "daily-lessons" / "day-002-full.md"
    ]
    
    # 输出目录
    output_dir = base_path / "pdf-output"
    output_dir.mkdir(exist_ok=True)
    
    print("=" * 60)
    print("Markdown 转 PDF 转换器")
    print("=" * 60)
    print(f"\n开始时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"\n输入文件:")
    for f in md_files:
        if f.exists():
            print(f"  ✓ {f.name}")
        else:
            print(f"  ✗ {f.name} (未找到)")
    
    print(f"\n输出目录：{output_dir}")
    print("\n" + "-" * 60)
    
    # 安装必要的包
    print("\n[步骤 1/2] 检查并安装依赖包...")
    install_packages()
    
    # 转换文件
    print("\n[步骤 2/2] 开始转换文件...")
    converted_files = []
    
    for md_file in md_files:
        if not md_file.exists():
            print(f"\n⚠ 跳过：{md_file.name} (文件不存在)")
            continue
        
        try:
            print(f"\n正在转换：{md_file.name} ...")
            pdf_path = convert_md_to_pdf(md_file, output_dir)
            converted_files.append(pdf_path)
            file_size = pdf_path.stat().st_size / 1024 / 1024  # MB
            print(f"✓ 成功：{pdf_path.name} ({file_size:.2f} MB)")
        except Exception as e:
            print(f"✗ 失败：{md_file.name}")
            print(f"  错误：{str(e)}")
    
    # 输出摘要
    print("\n" + "=" * 60)
    print("转换完成!")
    print("=" * 60)
    print(f"\n成功转换：{len(converted_files)} 个文件")
    print(f"完成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if converted_files:
        print(f"\nPDF 文件位置:")
        for pdf in converted_files:
            print(f"  📄 {pdf}")
    
    return len(converted_files)

if __name__ == "__main__":
    exit_code = main()
    exit(0 if exit_code > 0 else 1)
