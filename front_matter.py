# coding: utf-8

import os
import re
import time

import frontmatter

# 更新md文件的front matter：1.增加创建时间；2.提取tag
def update_front_matter(file):

    with open(file, 'r', encoding='utf-8') as f:
       post = frontmatter.loads(f.read())
    
    is_write = False
    
    if not post.metadata.get('create_date', None):
        timeArray = time.localtime((os.path.getctime(file)))
        post['create_date'] = time.strftime("%Y-%m-%d %H:%M", timeArray)
        if not is_write:
            is_write = True

    if not post.metadata.get('title', None):
        post['title'] = os.path.splitext(os.path.basename(file))[0]
        if not is_write:
            is_write = True
    
    # 将代码块内容去掉
    temp_content = re.sub(r'```([\s\S]*?)```[\s]?','',post.content)
    # 获取tag列表
    tags = re.findall(r'\s#[\u4e00-\u9fa5a-zA-Z]+', temp_content, re.M|re.I)
    ret_tags = list(set(map(lambda x: x.strip(), tags)))
    print('tags in content: ', ret_tags)
    print('tags in front matter: ', post.get("tags", []))
    if len(ret_tags) == 0:
        pass
    elif post.get("tags", []) != set(ret_tags): 
        post['tags'] = ret_tags
        if not is_write:
            is_write = True
    
    if is_write:
        with open(file, 'w', encoding='utf-8') as f:
            f.write(frontmatter.dumps(post))

# 递归获取提供目录下所有文件
def list_all_files(root_path, ignore_dirs=[]):
    files = []
    default_dirs = [".git", ".obsidian", ".config"]
    ignore_dirs.extend(default_dirs)

    for parent, dirs, filenames in os.walk(root_path):
        dirs[:] = [d for d in dirs if not d in ignore_dirs]
        filenames = [f for f in filenames if not f[0] == '.']
        for file in filenames:
            if file.endswith(".md"):
                files.append(os.path.join(parent, file))
    return files


if __name__ == "__main__":
    # file_path = './xwlearn/test.md'
    # update_front_matter(file_path)
    ignore_dirs = []
    files = list_all_files('./_posts/notion', ignore_dirs=ignore_dirs)

    print("current dir: ", os.path.dirname(os.path.abspath(__file__)))
    for file in files:
        print("---------------------------------------------------------------")
        print('current file: ', file)
        update_front_matter(file)
        time.sleep(1)
