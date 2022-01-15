import os

import markdown
from jinja2 import Environment, FileSystemLoader
from markdown.extensions.wikilinks import WikiLinkExtension

from tir.parsers.markdown.links import CustomInlineLinksExtension
from tir.posts import Post
from tir.utils import format_date, url_for, _
from tir.parsers.markdown.links import CustomInlineLinksExtension
from tir.parsers.markdown.local_links import LocalLinksExtension


class TemplateLoader:

    def __init__(self, layout_directory: str = None, config=None):
        if config is None:
            config = {}
        self.conf = config
        self.env = Environment(
            loader=FileSystemLoader(os.path.join(
                layout_directory, 'templates')),
            autoescape=True
        )
        self.md = markdown.Markdown(
            extensions=[
                'markdown.extensions.meta',
                'markdown.extensions.toc',
                'markdown.extensions.footnotes',
                'markdown.extensions.def_list',
                'markdown.extensions.tables',
                'markdown.extensions.sane_lists',
                WikiLinkExtension(
                    base_url=f'https://fr.wikipedia.org/wiki/', end_url=''),
                LocalLinksExtension(),
                CustomInlineLinksExtension()
            ]
        )
        self.env.globals['url_for'] = url_for
        self.env.globals['_'] = _
        self.env.globals['format_date'] = format_date
        self.env.globals['config'] = self.conf
        # self.env.globals['read_post'] = Post.read_post
        self.env.globals['parse_md'] = self.md.convert
