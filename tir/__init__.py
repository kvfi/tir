import os
import shutil
import subprocess

import pkg_resources
from jinja2 import Environment, FileSystemLoader

from tir.posts import Post
from tir.tools import is_init, _
from tir.utils import mktree, is_windows, url_for, format_date

import logging

logger = logging.getLogger(__name__)


class Tir(object):

    def __init__(self, conf):
        """Tir def

        Performs some checks on the environment before doing anything else.
        """

        self.conf = conf

        self.theme = self.conf.get('visuals').get('theme') or 'default'
        self.build_dir = self.conf['build_dir']

    def init(self):
        if is_init():
            print('A Tir project seems to be already initialized. Nothing to do.')
            return False
        print('Initializing Tir project...')
        skeleton_dirs = ['content/posts', 'content/pages']
        skeleton_files = ['package.json', 'tir.yml', 'Gruntfile.js']
        for skeleton_dir in skeleton_dirs:
            mktree(skeleton_dir)
        for skeleton_file in skeleton_files:
            shutil.copyfile(pkg_resources.resource_filename('tir', skeleton_file),
                            '{}/{}'.format(os.getcwd(), skeleton_file))
        shutil.copytree(pkg_resources.resource_filename('tir', 'assets'),
                        '{}/{}'.format(os.getcwd(), 'assets'))
        print('Installing NodeJS deps...')
        try:
            subprocess.run(['yarn', 'install'])
        except Exception:
            print('An error has occurred. Are you sure "yarn" is installed on your system?')
        print('Tir project was successfully installed.')
        return True

    def build(self):
        if not is_init():
            print('Project does not seem to be initialized. Type "tir init" to create a Tir project here.')
            return False
        try:
            pkg_visuals_dir = pkg_resources.resource_filename('tir', 'visuals')
            tpl_visuals_dir = os.path.join(pkg_visuals_dir, self.theme)
            logger.debug('Selected template: %s', tpl_visuals_dir)
            print('Replace assets files')
            assets_src_dir = os.path.join(tpl_visuals_dir, 'assets')
            assets_target_dir = '{}/{}'.format(os.getcwd(), 'assets')
            print('Removing {}'.format(assets_target_dir))
            if os.path.exists(assets_target_dir):
                shutil.rmtree(assets_target_dir)
            shutil.copytree(assets_src_dir, assets_target_dir)
            print('Assets successfully updated')
            env = Environment(loader=FileSystemLoader(os.path.join(tpl_visuals_dir, 'templates')))
            post_tpl = env.get_template('post.html')
            index_tpl = env.get_template('home.html')
            env.globals['url_for'] = url_for
            env.globals['_'] = _
            env.globals['format_date'] = format_date
            env.globals['config'] = self.conf
            print('Building...')
            slugs = Post.get_slugs()
            for slug in slugs:
                slug = slug.replace('.md', '')
                p = Post()
                x = p.read(slug)
                target_path = '%s/%s.html' % (self.build_dir, slug)
                mktree(self.build_dir)
                with open(target_path, 'w', encoding='utf-8') as fh:
                    head = {'title': x.meta['title'],
                            'description': x.meta['subtitle']}
                    fh.write(post_tpl.render(
                        post=p,
                        head=head,
                    ))
                print('Compiling {}...'.format(target_path))

            # Building index page
            print('Building index page...')
            with open(self.build_dir + '/index.html', 'w', encoding='utf-8') as fh:
                p = Post()
                x = p.read('index', dir_path=Post.MISC_DIR)
                head = {'title': 'ouafi.net',
                        'description': 'Dans un monde fou, toute forme d\'écriture est un remède psychiatrique'}
                fh.write(index_tpl.render(
                    content={'intro': x},
                    post=p,
                    head=head
                ))

            print('Building static files...')
            if not is_windows():
                subprocess.run(['yarn', 'build'])
            else:
                subprocess.Popen(['yarn', 'build'], shell=True)
            print('Build was successful.')
            return True

        except Exception as e:
            raise e
