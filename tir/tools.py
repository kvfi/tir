"""
todos:
* create html directory if doesn't exist
* format date in meta
* check if toc is rendered
* get stats at the end of build
* make configurable options: github, website, url, http/https, templates
* remove personal files and replace with samples (logo, ...)
* don't remove tir.yml if it already exists
"""

import os
import shutil
import subprocess
from datetime import datetime

import pkg_resources
from jinja2 import Environment, FileSystemLoader

from tir.posts import Post
from tir.settings import config


def url_for(route, slug=None, filename=''):
    if route == 'index':
        return '/'
    if route == 'post':
        return slug + '.html'
    elif route == 'static':
        return '{}/{}'.format('static', filename)


def format_date(value):
    date = datetime.strptime(value, "%Y-%m-%d")
    day = date.day
    if 4 <= day <= 20 or 24 <= day <= 30:
        suffix = "th"
    else:
        suffix = ["st", "nd", "rd"][day % 10 - 1]
    return date.strftime('%B %e<sup>' + suffix + '</sup> %Y')


def copytree(src, dst, symlinks=False, ignore=None):
    if not os.path.exists(dst):
        os.makedirs(dst)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            copytree(s, d, symlinks, ignore)
        else:
            if not os.path.exists(d) or os.stat(s).st_mtime - os.stat(d).st_mtime > 1:
                shutil.copy2(s, d)


def mktree(path):
    if not os.path.exists(path):
        os.makedirs(path)


def _(text):
    return text


def is_init():
    return os.path.exists('tir.yml')


def init():
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
        print('An error has occured. Are you sure "yarn" is installed on your system?')
    print('Tir project was successfully installed.')
    return True


def build():
    if not is_init():
        print('Project does not seem to be initialized. Type "tir init" to create a Tir project here.')
        return False
    try:
        templates_dir = pkg_resources.resource_filename('tir', 'templates')
        print('Replace assets files')
        assets_src_dir = pkg_resources.resource_filename('tir', 'assets')
        assets_target_dir = '{}/{}'.format(os.getcwd(), 'assets')
        print('Removing {}'.format(assets_target_dir))
        if os.path.exists(assets_target_dir):
            shutil.rmtree(assets_target_dir)
        shutil.copytree(assets_src_dir, assets_target_dir)
        print('Assets successfully updated')
        env = Environment(loader=FileSystemLoader(templates_dir))
        post_tpl = env.get_template('post.html')
        index_tpl = env.get_template('home.html')
        env.globals['url_for'] = url_for
        env.globals['_'] = _
        env.globals['format_date'] = format_date
        env.globals['config'] = config
        print('Building...')
        slugs = Post.get_slugs()
        target_dir = 'build/html/'
        for slug in slugs:
            slug = slug.replace('.md', '')
            p = Post()
            x = p.read(slug)
            target_path = target_dir + slug + '.html'
            mktree(target_dir)
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
        with open(target_dir + '/index.html', 'w', encoding='utf-8') as fh:
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
        subprocess.run(['yarn', 'build'])
        copytree('assets/images', '{}/static/images'.format(target_dir))
    except Exception as e:
        raise e
    print('Build was successful.')
    return True
