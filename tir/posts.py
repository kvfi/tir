import os
from datetime import datetime
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

    def __init__(self):
        self.meta = None
        self.content = None
        self.yearly = False

    def read(self, el, dir_path=POSTS_DIR, ext='.md'):
        try:
            with open('{}'.format(join(dir_path, el + ext)), encoding='utf8') as f:
                md = markdown.Markdown(
                    extensions=['markdown.extensions.meta', 'markdown.extensions.toc', 'markdown.extensions.footnotes',
                                'markdown.extensions.def_list', 'markdown.extensions.tables',
                                WikiLinkExtension(base_url='https://en.wikipedia.org/wiki/', end_url='')])
                html = md.convert(f.read())
                self.content = html
                if hasattr(md, 'Meta') and md.Meta:
                    meta = md.Meta
                    meta = remove_list_meta(meta)
                    if 'online' in meta and meta['online'] == 'false':
                        pass
                    if hasattr(md, 'toc'):
                        meta['contents'] = md.toc
                    self.meta = meta
                # Special handling
                # In case we process a journal entry (retrospective) we want the date to be the title
                if dir_path == Post.RETROS_DIR:
                    d = datetime.strptime(self.meta['date'], "%d-%m-%Y")
                    if self.yearly:
                        title = d.year
                    else:
                        title = '{}/{}/{}'.format(d.day, d.month, d.year)
                    self.meta['title'] = 'Retrospective {}'.format(title)
                return self
        except FileNotFoundError as fnf:
            raise fnf

    @staticmethod
    def get_slugs(limit=None):
        if limit is not None:
            posts = listdir(Post.POSTS_DIR)[:limit]
        else:
            posts = listdir(Post.POSTS_DIR)
        posts.remove('index.md')
        return posts

    @staticmethod
    def get_intro():
        post = Post()
        return post.read(Post.MISC_DIR + '/intro.md')

    @staticmethod
    def read_all(slugs):
        posts = []
        for slug in slugs:
            post = Post()
            p = post.read(Post.POSTS_DIR, slug.replace('.md', ''))
            posts.append(p)
        return posts
