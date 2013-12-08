import argparse
from collections import OrderedDict
import logging
import os
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


def get_requirement_file():
    """
    Get the "best" requirements file we can find
    """
    for filename in settings.REQUIREMENTS_SOURCE_FILES:
        if os.path.exists(filename):
            return filename
    logger.warn(
        textwrap.dedent(
            """Sorry, I couldn't find a requirements.yml or
            requirements.in!""")
    )


def get_requirements(filename):
    if filename is not None:
        logger.info("processing %s" % filename)
        with open(filename, "r") as f:
            for line in f.readlines():
                line = line.strip()
                yield line


def install(args, lock_filename="requirements.txt"):
    deps = OrderedDict()

    filename = get_requirement_file()
    for line in get_requirements(filename):
        line = line.strip()
        deps[line] = []

        requirement_set = RequirementSet(
            build_dir=build_prefix,
            src_dir=src_prefix,
            download_dir=None)

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
            deps[line].append("%s==%s" % (package.name, package.installed_version))

        for package in requirement_set.successfully_installed:
            deps[line].append("%s==%s" % (package.name, package.installed_version))

        deps[line] = set(deps[line])

    package_set = set([])

    with open(lock_filename, "w") as output:
        output.write("# this file generated from '%s' by pundler:\n" % (filename,))
        for requested_package in deps:
            output.write("# requirement '%s' depends on:\n" % (requested_package,))
            for dependency in deps[requested_package]:
                logger.info("dependency %s" % dependency)
                if dependency not in package_set:
                    dependency = dependency.lower()
                    package_set.add(dependency)
                    output.write("%s\n" % (dependency,))
                else:
                    output.write("#%s\n" % (dependency,))
            output.write("\n")


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
    return parser


def main():
    args = get_parser().parse_args()
    args.func(args)
