import os

try:
    # Use setuptools if available, for install_requires (among other things).
    import setuptools
    from setuptools import setup
except ImportError:
    setuptools = None
    from distutils.core import setup

kwargs = {}

with open("tir/__init__.py") as f:
    ns = {}
    exec(f.read(), ns)
    version = ns["version"]

with open("README.md") as f:
    kwargs["long_description"] = f.read()

if setuptools is not None:
    python_requires = ">= 3.5"
    kwargs["python_requires"] = python_requires


def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths


initial_files = ['logging.yml',
                 'templates/*',
                 'package.json',
                 'tir.yml',
                 'Gruntfile.js',
                 'assets/*',
                 'assets/**/*',
                 'assets/**/**/*']

setup(
    name="tir",
    version=version,
    packages=["tir"],
    author="kvfi",
    author_email="mail@mail.net",
    url="https://ouafi.net/tir",
    license="https://www.gnu.org/licenses/gpl-3.0.en.html",
    description=(
        "Minimalist static site generator"
    ),
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    setup_requires=['wheel'],
    install_requires=['jinja2', 'markdown', 'pyyaml'],
    package_data={
        'tir': initial_files},
    entry_points={
        'console_scripts': [
            'tir = tir.cli:main'
        ]
    },
    **kwargs
)
