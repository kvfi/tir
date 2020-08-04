import os
from os import getenv, listdir
from os.path import join, normpath

import markdown
from markdown.extensions.wikilinks import WikiLinkExtension

from tir.utils import remove_list_meta

_EXCLUDED_FILES = ['index.md']


class Post(object):
    d = os.getcwd()
    BASE_DIR = getenv('BASE_DIR', d)
    CONTENT_DIR = normpath(join(BASE_DIR, 'content'))
    POSTS_DIR = join(CONTENT_DIR, 'posts')
    RETROS_DIR = normpath(join(CONTENT_DIR, 'retrospectives'))
    LINKS_DIR = normpath(join(CONTENT_DIR, 'links/'))
    MISC_DIR = normpath(join(CONTENT_DIR, 'misc/'))

    def __init__(self, path: str = None):
        self.path = path
        self.file_base_name = os.path.basename(os.path.splitext(self.path)[0])
        self.meta = None
        self.raw = None
        self.content = None
        self.parse()

    def parse(self):
        try:
            with open(self.path, 'r') as f:
                self.raw = f.read()
            if not self.raw:
                return
            md = markdown.Markdown(
                extensions=[
                    'markdown.extensions.meta',
                    'markdown.extensions.toc',
                    'markdown.extensions.footnotes',
                    'markdown.extensions.def_list',
                    'markdown.extensions.tables',
                    WikiLinkExtension(base_url='https://en.wikipedia.org/wiki/', end_url='')
                ]
            )
            self.content = md.convert(self.raw)
            if hasattr(md, 'Meta') and md.Meta:
                meta = md.Meta
                meta = remove_list_meta(meta)
                if 'online' in meta and meta['online'] == 'false':
                    pass
                if hasattr(md, 'toc'):
                    meta['contents'] = md.toc
                self.meta = meta
            else:
                print('{} is missing meta. Ignoring...'.format(self.path))
                pass
        except FileNotFoundError as fnf:
            raise fnf

    @staticmethod
    def get_slugs():
        posts = listdir(Post.POSTS_DIR)
        return posts
