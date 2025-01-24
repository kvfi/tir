import logging
import os
import shutil
import time

import sass

from tir.config import REQUIRED_PATHS, get_config
from tir.files import hash_content, rm_dir_files
from tir.posts import Post
from tir.templates import TemplateLoader
from tir.tools import is_init, minify_file
from tir.utils import mktree, scantree

logger = logging.getLogger(__name__)


class Tir(object):

    def __init__(self):
        """Tir def

        Performs some checks on the environment before doing anything else.
        """

        self.conf = get_config()

        self.theme = self.conf.visuals.theme
        self.lang = self.conf.lang
        self.build_dir = self.conf.build_dir
        self.working_dir = os.getcwd()
        self.content_dir = os.path.join(self.working_dir, 'content')
        self.posts_dir = os.path.join(self.content_dir, 'posts')
        self.notes_dir = os.path.join(self.content_dir, 'notes')

        self.oc = []

    @staticmethod
    def init():
        if is_init():
            return False
        print('Initializing Tir project...')
        skeleton_dirs = REQUIRED_PATHS
        skeleton_files = ['tir.yml']
        for skeleton_dir in skeleton_dirs:
            mktree(skeleton_dir)
        for skeleton_file in skeleton_files:
            shutil.copyfile(
                pkg_resources.resource_filename(
                    'tir',
                    'data/{}'.format(skeleton_file)
                ), '{}/{}'.format(os.getcwd(), skeleton_file)
            )

        # copy quickstart data
        shutil.copytree(
            pkg_resources.resource_filename('tir', 'data'),
            os.path.join(os.getcwd()),
            dirs_exist_ok=True
        )
        print('Tir project was successfully installed.')
        return True

    def build(self, path: str = None):
        if not is_init():
            print(
                'Project does not seem to be initialized. Type "tir init" to create a Tir project here.')
            return False
        try:
            if os.path.exists(self.build_dir) and not path:
                shutil.rmtree(self.build_dir)
            tpl_visuals_dir = os.path.join(os.getcwd(), 'layout', self.theme)
            print('Selected template:', tpl_visuals_dir)
            print('Replace assets files')
            assets_src_dir = os.path.join(tpl_visuals_dir, 'assets')
            assets_target_dir = os.path.join(
                os.getcwd(), self.build_dir, 'static')

            tpl_loader = TemplateLoader(
                layout_directory=tpl_visuals_dir, config=self.conf)

            print('Building static files...')
            css_dir = os.path.join(assets_target_dir, 'css')
            mktree(css_dir)
            compiled_scss = sass.compile(filename=os.path.join(
                assets_src_dir, 'scss', 'main.scss'))
            stylesheet_path = os.path.join(css_dir, 'stylesheet.css')
            with open(stylesheet_path, 'w+', encoding='utf-8') as f:
                f.write(compiled_scss)
            minified_stylesheet_path = minify_file(stylesheet_path)

            shutil.copytree(
                os.path.join(tpl_visuals_dir, 'assets', 'images'),
                os.path.join(self.build_dir, 'static', 'images')
            )

            elements = []

            print('Building content...')

            for entry in scantree(self.posts_dir):
                if entry.is_file():
                    p = Post(entry.path, css_path=minified_stylesheet_path, tpl_loader=tpl_loader)
                    elements.append(p)

            for entry in elements:
                entry.write()
            print('Build was successful.')
            return True

        except Exception as e:
            raise e

    def watch(self):
        self.oc = hash_content(self.posts_dir)
        print('Now watching for changes...'.format(self.posts_dir))
        while 1:
            time.sleep(2)
            cc = hash_content(self.posts_dir)
            if self.oc == cc:
                pass
            else:
                self.oc = cc
                self.build()
