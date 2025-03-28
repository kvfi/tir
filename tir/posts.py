import os
import pathlib
from os import getenv
from os.path import join, normpath

import markdown
from markdown.extensions.wikilinks import WikiLinkExtension

from tir import get_config
from tir.parsers.markdown.links import CustomInlineLinksExtension
from tir.parsers.markdown.local_links import LocalLinksExtension
from tir.utils import remove_list_meta

_EXCLUDED_FILES = ['index.md']


class Post:
    BASE_DIR = getenv('BASE_DIR', os.getcwd())
    CONTENT_DIR = normpath(join(BASE_DIR, 'content'))
    POSTS_DIR = join(CONTENT_DIR, 'posts')
    RETROS_DIR = normpath(join(CONTENT_DIR, 'retrospectives'))
    LINKS_DIR = normpath(join(CONTENT_DIR, 'links/'))
    MISC_DIR = normpath(join(CONTENT_DIR, 'misc/'))

    def __init__(self, source: str = None, css_path=None, tpl_loader=None, online_only=True, lang='en'):
        self.source: str = source
        self.css_path = css_path
        self.tpl_loader = tpl_loader
        self.target_path = None
        self.file_base_name = os.path.basename(os.path.splitext(self.source)[0])
        self.meta = None
        self.raw = None
        self.content = None
        self.conf = get_config()
        self.online_only = online_only
        self.lang = lang
        self.parse()

    def parse(self):
        try:
            with open(self.source, 'r', encoding='utf8') as f:
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
                    'markdown.extensions.sane_lists',
                    WikiLinkExtension(
                        base_url=f'https://{self.lang}.wikipedia.org/wiki/', end_url=''),
                    LocalLinksExtension(),
                    CustomInlineLinksExtension()
                ]
            )

            self.content = md.convert(self.raw)
            if hasattr(md, 'Meta') and md.Meta:
                meta = md.Meta
                meta = remove_list_meta(meta)
                if 'online' in meta and (meta['online'] == 'false' or self.online_only):
                    pass
                if hasattr(md, 'toc'):
                    meta['contents'] = md.toc
                self.meta = meta
        except FileNotFoundError as fnf:
            raise fnf

    def __repr__(self):
        return f'<Post path={self.source}, file_name_base={self.file_base_name} />'

    def write(self):
        target_path = pathlib.Path(self.conf.build_dir) / pathlib.Path(self.source).parent.relative_to(
            self.POSTS_DIR) / (self.meta['slug'] + self.conf.file_extension)
        print('target full path: %s' % target_path)
        os.makedirs(pathlib.Path(target_path).parent, exist_ok=True)
        with open(target_path, 'w', encoding='utf-8') as fh:
            head = {
                'stylesheet_file_name': self.css_path
            }
            fh.write(self.tpl_loader.env.get_template(
                'index.html' if self.file_base_name == 'index' else 'post.html').render(
                post=self,
                head=head,
                home_content=self.conf.home_content))
