"""
Markdown 转 PDF 转换脚本 v2
使用 markdown 和 reportlab 库将 Markdown 文件转换为 PDF
支持中文显示
"""

import os
import re
from pathlib import Path
from datetime import datetime
from markdown import markdown

def install_packages():
    """安装必要的 Python 包"""
    import subprocess
    packages = ['markdown', 'reportlab']
    for pkg in packages:
        try:
            __import__(pkg)
        except ImportError:
            print(f"正在安装 {pkg}...")
            subprocess.check_call(['pip', 'install', pkg, '-i', 'https://pypi.tuna.tsinghua.edu.cn/simple'])
    print("所有依赖包已安装完成")

def md_to_paragraphs(md_content):
    """将 Markdown 内容解析为结构化段落"""
    paragraphs = []
    lines = md_content.split('\n')
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # 跳过空行
        if not line:
            i += 1
            continue
        
        # 标题
        if line.startswith('# '):
            paragraphs.append(('h1', line[2:]))
        elif line.startswith('## '):
            paragraphs.append(('h2', line[3:]))
        elif line.startswith('### '):
            paragraphs.append(('h3', line[4:]))
        elif line.startswith('#### '):
            paragraphs.append(('h4', line[5:]))
        # 列表项
        elif line.startswith('- ') or line.startswith('* ') or re.match(r'^\d+\. ', line):
            list_items = []
            while i < len(lines) and (lines[i].strip().startswith('- ') or 
                                       lines[i].strip().startswith('* ') or 
                                       re.match(r'^\d+\. ', lines[i].strip())):
                item_text = re.sub(r'^[-*]\s*', '', lines[i].strip())
                item_text = re.sub(r'^\d+\.\s*', '', item_text)
                list_items.append(item_text)
                i += 1
            paragraphs.append(('list', list_items))
            continue
        # 引用块
        elif line.startswith('>'):
            quote_lines = []
            while i< len(lines) and lines[i].strip().startswith('>'):
                quote_lines.append(lines[i].strip()[1:].strip())
                i += 1
            paragraphs.append(('quote', ' '.join(quote_lines)))
            continue
        # 代码块
        elif line.startswith('```'):
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code_lines.append(lines[i])
                i += 1
            paragraphs.append(('code', '\n'.join(code_lines)))
        # 普通段落
        else:
            # 收集连续的非空行
            para_lines = [line]
            i += 1
            while i < len(lines) and lines[i].strip() and not lines[i].strip().startswith('#') and \
                  not lines[i].strip().startswith('-') and not lines[i].strip().startswith('*') and \
                  not re.match(r'^\d+\. ', lines[i].strip()) and not lines[i].strip().startswith('>') and \
                  not lines[i].strip().startswith('```'):
                para_lines.append(lines[i])
                i += 1
            paragraphs.append(('p', ' '.join(para_lines)))
            continue
        
        i += 1
    
    return paragraphs

def create_pdf_from_md(md_file, output_dir):
    """使用 reportlab 创建 PDF"""
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm, inch
    from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
    from reportlab.lib.colors import HexColor, black, darkblue, gray
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    
    # 读取 Markdown 文件
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # 解析为结构化段落
    paragraphs = md_to_paragraphs(md_content)
    
    # 创建 PDF 文档
    pdf_path = output_dir / f"{Path(md_file).stem}.pdf"
    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=A4,
        leftMargin=2.5*cm,
        rightMargin=2.5*cm,
        topMargin=2.5*cm,
        bottomMargin=2.5*cm
    )
    
    # 获取样式表
    styles = getSampleStyleSheet()
    
    # 注册中文字体（使用系统字体）
    font_found = False
    font_paths = [
        r"C:\Windows\Fonts\msyh.ttc",      # 微软雅黑
        r"C:\Windows\Fonts\simsun.ttc",    # 宋体
        r"C:\Windows\Fonts\simhei.ttf",    # 黑体
    ]
    
    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                pdfmetrics.registerFont(TTFont('ChineseFont', font_path))
                font_found = True
                print(f"使用中文字体：{font_path}")
                break
            except Exception as e:
                print(f"字体加载失败 {font_path}: {e}")
                continue
    
    if not font_found:
        print("警告：未找到合适的中文字体，PDF 可能无法正确显示中文")
        # 使用默认字体作为后备
        pdfmetrics.registerFont(TTFont('ChineseFont', r"C:\Windows\Fonts\arial.ttf"))
    
    # 自定义样式
    style_h1 = ParagraphStyle(
        name='CustomH1',
        parent=styles['Heading1'],
        fontName='ChineseFont',
        fontSize=24,
        textColor=HexColor('#2c3e50'),
        spaceAfter=30,
        spaceBefore=40,
        alignment=TA_LEFT,
        leading=32
    )
    
    style_h2 = ParagraphStyle(
        name='CustomH2',
        parent=styles['Heading2'],
        fontName='ChineseFont',
        fontSize=18,
        textColor=HexColor('#34495e'),
        spaceAfter=20,
        spaceBefore=30,
        alignment=TA_LEFT,
        leading=24
    )
    
    style_h3 = ParagraphStyle(
        name='CustomH3',
        parent=styles['Heading3'],
        fontName='ChineseFont',
        fontSize=14,
        textColor=HexColor('#7f8c8d'),
        spaceAfter=15,
        spaceBefore=20,
        alignment=TA_LEFT,
        leading=18
    )
    
    style_h4 = ParagraphStyle(
        name='CustomH4',
        parent=styles['Normal'],
        fontName='ChineseFont',
        fontSize=12,
        textColor=HexColor('#95a5a6'),
        spaceAfter=10,
        spaceBefore=15,
        alignment=TA_LEFT,
        leading=16
    )
    
    style_normal = ParagraphStyle(
        name='CustomNormal',
        parent=styles['Normal'],
        fontName='ChineseFont',
        fontSize=12,
        textColor=black,
        spaceAfter=12,
        spaceBefore=6,
        alignment=TA_JUSTIFY,
        leading=20
    )
    
    style_quote = ParagraphStyle(
        name='CustomQuote',
        parent=styles['Normal'],
        fontName='ChineseFont',
        fontSize=11,
        textColor=gray,
        spaceAfter=15,
        spaceBefore=15,
        leftIndent=20,
        borderLeftWidth=3,
        borderLeftColor=darkblue,
        alignment=TA_LEFT,
        leading=18
    )
    
    style_code = ParagraphStyle(
        name='CustomCode',
        parent=styles['Normal'],
        fontName='Courier',  # 使用等宽字体
        fontSize=10,
        textColor=HexColor('#c7254e'),
        spaceAfter=15,
        spaceBefore=15,
        backColor=HexColor('#f8f8f8'),
        borderColor=HexColor('#ddd'),
        borderWidth=1,
        padding=5,
        alignment=TA_LEFT,
        leading=14
    )
    
    # 构建 PDF 内容
    story = []
    
    for para_type, content in paragraphs:
        if para_type == 'h1':
            story.append(Paragraph(content, style_h1))
            story.append(Spacer(1, 0.3*cm))
        elif para_type == 'h2':
            story.append(Paragraph(content, style_h2))
            story.append(Spacer(1, 0.2*cm))
        elif para_type == 'h3':
            story.append(Paragraph(content, style_h3))
            story.append(Spacer(1, 0.15*cm))
        elif para_type == 'h4':
            story.append(Paragraph(content, style_h4))
            story.append(Spacer(1, 0.1*cm))
        elif para_type == 'p':
            story.append(Paragraph(content, style_normal))
        elif para_type == 'list':
            for item in content:
                # 使用圆点符号
                list_para = f"• {item}"
                story.append(Paragraph(list_para, style_normal))
        elif para_type == 'quote':
            story.append(Paragraph(content, style_quote))
        elif para_type == 'code':
            # 转义 HTML 特殊字符
            safe_content = content.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            story.append(Paragraph(safe_content, style_code))
    
    # 添加一些间距
    story.append(Spacer(1, 0.5*cm))
    
    # 生成 PDF
    doc.build(story)
    
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
    print("Markdown 转 PDF 转换器 v2 (使用 reportlab)")
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
            pdf_path = create_pdf_from_md(md_file, output_dir)
            converted_files.append(pdf_path)
            file_size = pdf_path.stat().st_size / 1024 / 1024  # MB
            print(f"✓ 成功：{pdf_path.name} ({file_size:.2f} MB)")
        except Exception as e:
            print(f"✗ 失败：{md_file.name}")
            print(f"  错误：{str(e)}")
            import traceback
            traceback.print_exc()
    
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
