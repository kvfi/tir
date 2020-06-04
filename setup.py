import os
from os.path import relpath

from setuptools import find_packages, setup

from tir.version import version


def package_files(directories):
    paths = []
    for directory in directories:
        for (path, directories, filenames) in os.walk(directory):
            for filename in filenames:
                paths.append(relpath(os.path.join(path, filename), 'tir'))
    return paths


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
    install_requires=[
        'jinja2',
        'markdown',
        'pyyaml'
    ],
    extra_requires={'test': ['pytest']},
    package_data={
        'tir': package_files(['tir/data', 'tir/visuals'])
    },
    entry_points={
        'console_scripts': [
            'tir = tir.cli:main'
        ]
    },
    packages=find_packages()
)
