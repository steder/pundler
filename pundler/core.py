import argparse
try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict # 2.6 fallback

import glob

import logging
import sys
import textwrap

from pip.index import PackageFinder
from pip.req import InstallRequirement, RequirementSet
from pip.locations import build_prefix, src_prefix

from . import settings

# in this case create the 'pundler' logger, but if called again from elsewhere will give another reference to this one
logger = logging.getLogger('pundler')
logger.setLevel(logging.DEBUG)

# change your formatting all from one place, or from the calling program when this gets turned into library code
formatter = logging.Formatter(fmt = '%(message)s')

#set it up to log to the console for now
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


def get_requirement_files():
    """
    Get the "best" requirements file we can find
    """
    paths = []
    for regex in settings.REQUIREMENTS_SOURCE_GLOBS:
        paths.extend(glob.glob(regex))
    return paths


def get_requirements(filename):
    logger.info("processing %s" % filename)
    with open(filename, "r") as f:
        for line in f.readlines():
            line = line.strip()
            if line.startswith("#"):
                continue
            yield line


class Pundler(object):
    def __init__(self, upgrade=False):
        self.deps = OrderedDict()
        self.args = []
        self.upgrade = upgrade

    def process_requirements(self, filename):
        for line in get_requirements(filename):
            line = line.strip()
            if line.startswith("-"):
                self.args.append(line)
                continue

            self.deps[line] = []

            print("upgrade?:", self.upgrade)
            requirement_set = RequirementSet(
                build_dir=build_prefix,
                src_dir=src_prefix,
                download_dir=None,
                upgrade=self.upgrade,
            )

            requirement = InstallRequirement.from_line(line, None)

            requirement_set.add_requirement(requirement)

            install_options = []
            global_options = []
            # TODO: specify index_urls from optional requirements.yml
            finder = PackageFinder(
                find_links=[],
                index_urls=["http://pypi.python.org/simple/"]
            )

            requirement_set.prepare_files(finder, force_root_egg_info=False, bundle=False)
            requirement_set.install(install_options, global_options)

            for package in requirement_set.requirements.values():
                if package.satisfied_by.has_metadata('PKG-INFO'):
                    dep = "%s==%s" % (package.name, package.installed_version)
                    print("values:", dep)
                    self.deps[line].append(dep)

            for package in requirement_set.successfully_installed:
                dep = "%s==%s" % (package.name, package.installed_version)
                print("installed:", dep)
                self.deps[line].append(dep)

            self.deps[line] = set(self.deps[line])

        package_set = set([])

        lock_filename = filename.replace(".in", ".txt")
        with open(lock_filename, "w") as output:
            output.write("# this file generated from '%s' by pundler:\n" % (filename,))
            for argument in self.args:
                output.write("%s\n"%(argument,))
                output.write("\n")
            for requested_package in self.deps:
                output.write("# requirement '%s' depends on:\n" % (requested_package,))
                for dependency in self.deps[requested_package]:
                    logger.info("dependency %s" % dependency)
                    if dependency not in package_set:
                        dependency = dependency.lower()
                        package_set.add(dependency)
                        output.write("%s\n" % (dependency,))
                    else:
                        output.write("#%s\n" % (dependency,))
                output.write("\n")



def install(args):
    filenames = get_requirement_files()
    if not filenames:
        logger.warn(
            textwrap.dedent(
            """
            Sorry, I couldn't find any requirements files!
            I tried the following globs:
            """) + "\n - ".join([""] + settings.REQUIREMENTS_SOURCE_GLOBS)
        )
        sys.exit(-2)
    for filename in filenames:
        pundler = Pundler(upgrade=args.upgrade)
        pundler.process_requirements(filename)


def update(args):
    args.upgrade = True
    install(args)


def get_parser():
    parser = argparse.ArgumentParser(description='Manage python requirements')
    # parser.add_argument('integers', metavar='N', type=int, nargs='+',
    #                    help='an integer for the accumulator')
    # parser.add_argument('--sum', dest='accumulate', action='store_const',
    #                     const=sum, default=max,
    #                     help='sum the integers (default: find the max)')
    subparsers = parser.add_subparsers(title='subcommands',
                                       description='valid subcommands',
                                       help='additional help')
    install_parser = subparsers.add_parser('install')
    install_parser.set_defaults(func=install)
    update_parser = subparsers.add_parser('update')
    update_parser.set_defaults(func=update)
    return parser


def main():
    args = get_parser().parse_args()
    args.upgrade = False
    args.func(args)
