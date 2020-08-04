import os

from jinja2 import Environment, FileSystemLoader

from tir.utils import format_date, url_for, _


class TemplateLoader:

    def __init__(self, layout_directory: str = None, config=None):
        if config is None:
            config = {}
        self.conf = config
        self.env = Environment(
            loader=FileSystemLoader(os.path.join(layout_directory, 'templates')),
            autoescape=True
        )

        self.env.globals['url_for'] = url_for
        self.env.globals['_'] = _
        self.env.globals['format_date'] = format_date
        self.env.globals['config'] = self.conf
