import os
from typing import List, Set

from tir.posts import Post


def acquire_files(include_private=False) -> Set[Post]:

    posts: Set[Post] = set()

    for root, dirs, files in os.walk(Post.CONTENT_DIR):
        for file in files:
            file_path: str = f'{root.replace(os.getcwd(), "")[1:]}/{file}'
            p: Post = Post(file_path)
            posts.add(p)

    return posts


def rm_dir_files(path: str):
    for n in os.scandir(path):
        os.remove(n.path)


def hash_content(path: str) -> List[int]:
    files = []
    content_hashes = []
    if os.path.isdir(path):
        files.extend([f.path for f in os.scandir(path)])
    elif os.path.isfile(path):
        files.append(path)
    else:
        print('This is a special file. Not handling...')

    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            content_hashes.append(f.read().__hash__())

    return content_hashes
