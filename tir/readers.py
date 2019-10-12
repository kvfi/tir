import logging
import os
from datetime import datetime
from os import getenv, listdir
from os.path import join, normpath

import markdown
from markdown.extensions.wikilinks import WikiLinkExtension

from tir.content import ContentObject
from tir.utils import remove_list_meta

log = logging.getLogger(__name__)


class Reader(object):
    log.critical('BASE_DIR is None. Please make sure that your project base directory is set properly.')
    BASE_DIR = getenv('BASE_DIR')
    CONTENT_DIR = normpath(join(BASE_DIR, 'content'))
    POSTS_DIR = join(CONTENT_DIR, 'posts')
    RETROS_DIR = normpath(join(CONTENT_DIR, 'retrospectives'))
    LINKS_DIR = normpath(join(CONTENT_DIR, 'links/'))
    MISC_DIR = normpath(join(CONTENT_DIR, 'misc/'))

    def __call__(self):
        if not Reader.BASE_DIR:
            log.error('BASE_DIR is None. Please make sure that your project base directory is set properly.')

    @staticmethod
    def directory_scan():
        print('BASE_DIR: {}', format(Reader.BASE_DIR))
        log.error('BASE_DIR is None. Please make sure that your project base directory is set properly.')
        walk_dir = Reader.BASE_DIR

        print('walk_dir = ' + walk_dir)

        # If your current working directory may change during script execution, it's recommended to
        # immediately convert program arguments to an absolute path. Then the variable root below will
        # be an absolute path as well. Example:
        # walk_dir = os.path.abspath(walk_dir)
        print('walk_dir (absolute) = ' + os.path.abspath(walk_dir))

        for root, subdirs, files in os.walk(walk_dir):
            print('--\nroot = ' + root)
            list_file_path = os.path.join(root, 'my-directory-list.txt')
            print('list_file_path = ' + list_file_path)

            with open(list_file_path, 'wb') as list_file:
                for subdir in subdirs:
                    print('\t- subdirectory ' + subdir)

                for filename in files:
                    file_path = os.path.join(root, filename)

                    print('\t- file %s (full path: %s)' % (filename, file_path))

                    with open(file_path, 'rb') as f:
                        f_content = f.read()
                        list_file.write(('The file %s contains:\n' % filename).encode('utf-8'))
                        list_file.write(f_content)
                        list_file.write(b'\n')


class MarkdownReader(Reader):

    def __init__(self, path: str) -> None:
        self.path = path
        self.meta = None
        self.content = None
        self.yearly = False

    def read(self) -> ContentObject:
        try:
            with open('{}'.format(join(self.path)), encoding='utf8') as f:
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
                if self.meta.get('type', None) == 'retro':
                    d = datetime.strptime(self.meta['date'], "%d-%m-%Y")
                    if self.yearly:
                        title = d.year
                    else:
                        title = '{}/{}/{}'.format(d.day, d.month, d.year)
                    self.meta['title'] = 'Retrospective {}'.format(title)
                return ContentObject(meta=self.meta, content=self.content)
        except FileNotFoundError as fnf:
            raise fnf

    @staticmethod
    def get_slugs(limit=None):
        if limit is not None:
            posts = listdir(MarkdownReader.CONTENT_DIR)[:limit]
        else:
            posts = listdir(Reader.POSTS_DIR)
        return posts
