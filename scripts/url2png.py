import os
import re
import requests
from urllib.parse import urlparse
from datetime import datetime

markdown_name = 'transformation'

# 原始 Markdown 文件路径
markdown_path = '/app/source/_posts/feishu.md'

# 输出路径
output_markdown_path = '/app/source/_posts/' + markdown_name + '.md'

# 图片保存目录
image_dir = '/app/source/img/' + markdown_name
image_cite_dir = '../img/' + markdown_name
os.makedirs(image_dir, exist_ok=True)

title = '位姿表示与变换'
categories = 'learn'
date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# === 添加头部信息 ===
header = f"""---
title: {title}
date: {date}
categories: {categories}
math: true
---\n\n"""

with open(markdown_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 处理图片路径的正则
pattern = r'!\[\]\(([^)]+)\)'

def replace_path(match):
    original_path = match.group(1)
    filename = os.path.basename(original_path)
    new_path = f'/img/{markdown_name}/{filename}'
    return f'![]({new_path})'

# 执行图片路径替换
new_content = re.sub(pattern, replace_path, content)

# === 新增功能：将 $$ 替换为 $ ===
new_content = new_content.replace('$$', '$')

# 保存新的 Markdown 文件
with open(output_markdown_path, 'w', encoding='utf-8') as f:
    f.write(header + new_content)

print("✅ Done: Markdown updated (Images reformatted & Math delimiters converted).")