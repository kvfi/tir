import os
from os.path import relpath
from typing import List

from setuptools import find_packages, setup

from tir.version import version


def get_requirements() -> List[str]:
    install_requires = []
    requirement_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'requirements.txt')
    if os.path.isfile(requirement_file):
        with open(requirement_file) as f:
            install_requires = f.read().splitlines()
    return install_requires


def package_files(directories):
    paths = []
    for directory in directories:
        for (path, directories, file_names) in os.walk(directory):
            for filename in file_names:
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
    install_requires=['babel', 'bcrypt', 'cffi', 'cryptography', 'csscompressor', 'colorama', 'jinja2', 'libsass', 'markdown',
                      'markupsafe', 'marshmallow', 'marshmallow-dataclass[enum,union]', 'marshmallow-enum',
                      'mypy-extensions', 'paramiko', 'pycparser', 'pynacl', 'pytz', 'pyyaml', 'six', 'typeguard',
                      'typing-extensions', 'typing-inspect'],
    extra_requires={'test': ['pytest']},
    package_data={
        'tir': package_files(['tir/data'])
    },
    entry_points={
        'console_scripts': [
            'tir = tir.cli:main'
        ]
    },
    packages=find_packages()
)
