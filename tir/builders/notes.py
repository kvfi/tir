import os

from tir import Post, mktree


def build_notes_index(notes_dir: str):
    print('Building notes...')
    with os.scandir(notes_dir) as it:
        for entry in it:
            if entry.name.endswith('.md') and entry.is_file():
                p = Post(entry.path)
                target_path = '%s/%s%s' % (self.build_dir, p.file_base_name, self.file_ext)
                mktree(self.build_dir)
                with open(target_path, 'w', encoding='utf-8') as fh:
                    head = {'stylesheet_file_name': minified_stylesheet_path}
                    fh.write(tpl_loader.env.get_template(
                        'index.html' if p.file_base_name == 'index' else 'post.html').render(
                        post=p,
                        head=head
                    ))
                print('Compiling {}...'.format(target_path))