from os import walk
from os.path import relpath, join

from setuptools import find_packages, setup

version = "0.3.0"
setup(
    name='tir',
    version=version,
    author='kvfi',
    author_email='mail@mail.net',
    url='https://ouafi.net/Tir.html',
    license='https://www.gnu.org/licenses/gpl-3.0.en.html',
    description=(
        'Minimalist static site generator'
    ),
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    setup_requires=['wheel'],
    install_requires=[
        'jinja2',
        'markdown',
        'pyyaml'
    ],
    package_data={
        'tir': [relpath(join(root, name), 'tir')
                for root, _, names in walk(join('tir', 'data')) and walk(join('tir', 'visuals'))
                for name in names]
    },
    entry_points={
        'console_scripts': [
            'tir = tir.cli:main'
        ]
    },
    packages=find_packages()
)
