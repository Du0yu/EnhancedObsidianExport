import os
import re
from shutil import copyfile
from urllib.parse import urlparse
import requests


# 读取Markdown文件内容
def read_markdown_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content


# 匹配Markdown文件中的图片链接
def find_image_links(markdown_content):
    # 匹配Markdown图片链接的正则表达式
    pattern = r'!\[.*?\]\((.*?)\)'
    image_links = re.findall(pattern, markdown_content)
    return image_links


# 下载网络图片并保存到指定目录
def download_and_save_image(url, destination_folder):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    response = requests.get(url, stream=True)
    if response.status_code == 200:
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        image_path = os.path.join(destination_folder, filename)
        print(image_path)
        with open(image_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
        return image_path
    else:
        return None


# 处理本地图片链接和网络图片链接
def process_images(input_markdown_path, output_markdown_path, image_output_path):
    markdown_content = read_markdown_file(input_markdown_path)
    image_links = find_image_links(markdown_content)
    output_directory = os.path.dirname(output_markdown_path)

    count = 1
    nums = len(image_links)
    for link in image_links:
        print(f"replacing {count}/{nums}")
        count += 1
        if link.startswith('http'):
            # 如果是网络图片链接，下载并保存到指定目录
            downloaded_image_path = download_and_save_image(link, image_output_path)
            if downloaded_image_path:
                relative_image_path = os.path.relpath(downloaded_image_path,
                                                      os.path.dirname(output_markdown_path)).replace('\\', '/')
                markdown_content = markdown_content.replace(link, os.path.join('!', relative_image_path))
        else:
            # 处理本地图片链接，复制图片到指定目录
            image_path = os.path.abspath(os.path.join(os.path.dirname(input_markdown_path), link))
            if os.path.exists(image_path):
                relative_image_path = os.path.relpath(image_path, os.path.dirname(output_markdown_path)).replace('\\',
                                                                                                                 '/')
                destination_path = os.path.join(image_output_path, os.path.basename(relative_image_path))
                copyfile(image_path, destination_path)
                destination_relative_path = os.path.relpath(destination_path,
                                                            os.path.dirname(output_markdown_path)).replace('\\', '/')
                print(destination_relative_path)
                markdown_content = markdown_content.replace(link, destination_relative_path)

    with open(output_markdown_path, 'w', encoding='utf-8') as modified_file:
        print(f"writing to {output_markdown_path}")
        modified_file.write(markdown_content)


# 示例调用
if __name__ == '__main__':
    input_md = r'D:\Code\export-markdown\modified_markdown_file1.md'
    output_md = r'D:\Code\export-markdown\modified_markdown_file1.md'
    image_output = r"D:\Code\export-markdown\test"

    process_images(input_md, output_md, image_output)
    print(f"Modified Markdown file saved at: {output_md}")
