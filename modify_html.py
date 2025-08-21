import os
import re
import shutil

# 定义要保留的 HTML 文件列表
published_html_files = [
    'add-a-fax-cover-page.html',
    'add-a-fax-cover-page-admin.html',
    'cancel-a-scheduled-fax.html',
    'check-faxes.html',
    'check-fax-logs-admin.html',
    'configure-ai-call-transcription-desktop.html',
    'configure-ai-call-transcription-for-an-extension.html',
    'configure-ai-call-transcription-mobile.html',
    'delete-fax-cover-pages.html',
    'delete-fax-cover-pages-admin.html',
    'delete-faxes.html',
    'delete-faxes-admin.html',
    'download-fax-data.html',
    'download-fax-data-admin.html',
    'enable-ai-call-transcription.html',
    'enable-websocket-real-time-audio-streaming.html',
    'forward-fax-to-email-or-another-fax-number.html',
    'integrate-yeastar-p-series-pbx-with-telnyx-fax-admin.html',
    'send-faxes-from-linkus-desktop-client.html',
    'transcribe-a-call-desktop.html',
    'transcribe-a-call-mobile.html',
    'update-read-status-of-inbound-faxes.html',
    'websocket-real-time-audio-streaming-overview.html',
]

# 定义要保留的其他文件
retain_files = ['index.html', 'iframe-navigation.js']

# 定义原始和目标文件夹路径
beta_folder = 'beta'
original_images_folder = 'screenshoots'  # 原始文件夹名称
target_images_folder = 'screenshots'    # 新的目标文件夹名称

# 创建目标文件夹（如果不存在）
if not os.path.exists(beta_folder):
    os.makedirs(beta_folder)

if not os.path.exists(target_images_folder):
    os.makedirs(target_images_folder)

# 定义要替换的代码
replacement_code = '''<link rel="stylesheet" href="./css/p-series.css">   
<link rel="stylesheet" href="./css/notes.css">   
<script src="./iframe-navigation.js"></script>  
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-9CK8527Q6J"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-9CK8527Q6J');
</script>
<!-- Microsoft Clarity -->
<script type="text/javascript">
    (function(c,l,a,r,i,t,y){
        c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
        t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
        y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
    })(window, document, "clarity", "script", "hxj5h8f90e");
</script>'''

# 用于存储所有引用的图片路径
referenced_images = set()

# 遍历指定的 HTML 文件
for html_file in published_html_files:
    if os.path.exists(html_file):
        with open(html_file, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # 提取图片路径
        pattern = r'<img[^>]*src="([^"]+)"'
        images = re.findall(pattern, content)
        
        # 将图片路径添加到集合中
        for image in images:
            if image.startswith('../images/') or image.startswith('../icons/'):
                referenced_images.add(os.path.basename(image))
        
        # 替换图片路径
        content = re.sub(r'../images/', 'screenshots/', content)
        content = re.sub(r'../icons/', 'screenshots/', content)  # 替换 ../icons/ 为 screenshots/
        
        # 替换 <div class="wh_content_area"> 之前的内容
        content = re.sub(r'.*?(<div class="wh_content_area">)', f'{replacement_code}\\1', content, flags=re.DOTALL)
        
        # 清除 aria-label="Table of Contents Container" 所在的代码
        content = re.sub(r'<nav[^>]*aria-label="Table of Contents Container"[^>]*>.*?</nav>', '', content, flags=re.DOTALL)
        
        # 清除 aria-label="On this page" 所在的代码
        content = re.sub(r'<nav[^>]*aria-label="On this page"[^>]*>.*?</nav>', '', content, flags=re.DOTALL)
        
        # 将修改后的内容写入 beta 文件夹
        with open(os.path.join(beta_folder, html_file), 'w', encoding='utf-8') as file:
            file.write(content)

# 复制引用的图片到目标文件夹
for image in referenced_images:
    original_image_path = os.path.join(original_images_folder, image)
    target_image_path = os.path.join(target_images_folder, image)
    
    if os.path.exists(original_image_path):
        print(f"正在复制文件：{original_image_path} -> {target_image_path}")
        try:
            shutil.copy2(original_image_path, target_image_path)
        except PermissionError as e:
            print(f"无法复制文件 {original_image_path}：{e}")
    else:
        print(f"文件不存在：{original_image_path}")

# 删除其他 HTML 文件
for filename in os.listdir('.'):
    if filename.endswith('.html') and filename not in published_html_files and filename not in retain_files:
        try:
            os.remove(filename)
        except PermissionError as e:
            print(f"无法删除文件 {filename}：{e}")

# 删除未引用的图片
for filename in os.listdir(original_images_folder):
    if filename not in referenced_images:
        try:
            os.remove(os.path.join(original_images_folder, filename))
        except PermissionError as e:
            print(f"无法删除文件 {filename}：{e}")

print("所有操作已完成！")