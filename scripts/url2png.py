import os
import re
import shutil
from urllib.parse import unquote
from datetime import datetime


# ============================================================
# 超参数
# ============================================================

# 生成的 Markdown 文件名，不带 .md
markdown_name = 'coordination_motion'

# 图片名称前缀
# 例如：XXXX
image_prefix = '协同规划'

# Markdown 存放类别，只允许 'daily' 或 'learn'
post_type = 'learn'

# Markdown 标题
title = '双臂协同运动规划（Coordination Motion Planning）'

# Hexo categories
categories = 'learn'


# ============================================================
# 路径设置
# ============================================================

# 原始飞书 Markdown 文件
markdown_path = '/app/source/_posts/feishu.md'

# _posts 根目录
posts_root = '/app/source/_posts'

# 检查 post_type
if post_type not in ['daily', 'learn']:
    raise ValueError("post_type 只能设置为 'daily' 或 'learn'")

# 生成 Markdown 所在目录
output_dir = os.path.join(posts_root, post_type)

# 生成 Markdown 路径
output_markdown_path = os.path.join(
    output_dir,
    markdown_name + '.md'
)

# 图片最终存储目录
# 例如：
# /app/source/_posts/learn/transformation/
image_output_dir = os.path.join(
    output_dir,
    markdown_name
)

# 创建目录
os.makedirs(output_dir, exist_ok=True)
os.makedirs(image_output_dir, exist_ok=True)


# ============================================================
# Markdown 头部
# ============================================================

date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

header = f"""---
title: {title}
date: {date}
categories: {categories}
math: true
---

"""


# ============================================================
# 读取原始 Markdown
# ============================================================

with open(markdown_path, 'r', encoding='utf-8') as f:
    content = f.read()


# ============================================================
# 处理图片
# ============================================================

# 支持：
# ![](Images_attachments/image%206.png)
#
# 以及：
# ![image.png](Images_attachments/image%206.png)
#
# 即无论 [] 中是否存在 alt 文本都可以匹配
pattern = r'!\[([^\]]*)\]\(([^)]+)\)'


def replace_image(match):
    alt_text = match.group(1)
    original_relative_path = match.group(2)

    # URL 解码：
    # image%206.png
    # ->
    # image 6.png
    decoded_relative_path = unquote(original_relative_path)

    # 原始图片绝对路径
    # 例如：
    # /app/source/_posts/Images_attachments/image 6.png
    source_image_path = os.path.join(
        os.path.dirname(markdown_path),
        decoded_relative_path
    )

    # 获取原图片文件名
    # image 6.png
    original_filename = os.path.basename(decoded_relative_path)

    # 分离文件名和扩展名
    filename_without_ext, ext = os.path.splitext(original_filename)

    # 将文件名中的空格替换成 "-"
    #
    # image 6
    # ->
    # image-6
    filename_without_ext = filename_without_ext.replace(' ', '-')

    # 添加前缀
    #
    # image-6.png
    # ->
    # XXXX-image-6.png
    new_filename = f'{image_prefix}-{filename_without_ext}{ext}'

    # 最终图片绝对路径
    #
    # /app/source/_posts/learn/transformation/XXXX-image-6.png
    target_image_path = os.path.join(
        image_output_dir,
        new_filename
    )

    # ========================================================
    # 移动图片
    # ========================================================

    if os.path.exists(source_image_path):

        # 如果目标文件已经存在，则先删除
        if os.path.exists(target_image_path):
            os.remove(target_image_path)

        shutil.move(
            source_image_path,
            target_image_path
        )

        print(
            f'✅ Image moved: '
            f'{source_image_path} -> {target_image_path}'
        )

    else:
        print(
            f'⚠️ Image not found: {source_image_path}'
        )

    # ========================================================
    # 修改 Markdown 图片引用
    # ========================================================

    return f'![]({new_filename})'


# 执行图片处理
new_content = re.sub(
    pattern,
    replace_image,
    content
)


# ============================================================
# 将 $$ 替换成 $
# ============================================================

new_content = new_content.replace('$$', '$')


# ============================================================
# 保存 Markdown
# ============================================================

with open(
    output_markdown_path,
    'w',
    encoding='utf-8'
) as f:
    f.write(header + new_content)


print()
print('==========================================')
print('✅ Markdown conversion completed')
print(f'Markdown: {output_markdown_path}')
print(f'Images:   {image_output_dir}')
print('==========================================')