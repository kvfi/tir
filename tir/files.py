import os
from typing import List


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
        with open(file, 'r') as f:
            content_hashes.append(f.read().__hash__())

    return content_hashes
