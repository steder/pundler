#!/usr/bin/env python
import os

from setuptools import setup, find_packages


requirements = [
    "argparse",
    "pip",
]

test_requirements = [
    "mock",
    "nose",
]

root = os.path.dirname(__file__)


def long_description():
    readme = os.path.join(root, "README.rst")
    long_description = open(readme, "r").read()
    return long_description


def version():
    init = os.path.join(root, "pundler", "__init__.py")
    version = None
    for line in open(init, "r"):
        if line.startswith("__version__"):
            version = line.split("=")[-1].strip().replace('\"', '')
    assert version is not None, "Unable to determine version!"
    return version


setup(name="Pundler",
      version=version(),
      description='An attempt to better manage dependencies in requirements files inspired by Ruby\'s Gem Bundler',
      long_description=long_description(),
      classifiers=['Development Status :: 4 - Beta',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: Apache Software License',
                   'Topic :: Software Development',
                   'Topic :: Utilities'],
      author='Mike Steder',
      author_email='steder@gmail.com',
      url='https://github.com/steder/pundler',
      packages=find_packages(),
      scripts=["bin/pundler"],
      install_requires=requirements,
      tests_require=test_requirements,
      test_suite="pundler",
)
