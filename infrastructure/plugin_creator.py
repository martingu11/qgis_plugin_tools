import argparse
import os
import shutil

PLUGIN_DIR = os.getcwd()
ROOT_DIR = os.path.abspath(os.path.join(PLUGIN_DIR, os.pardir))
PLUGIN_NAME = os.path.basename(PLUGIN_DIR)

TEMPLATE_DIR = os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'template'))
TEMPLATE_ROOT_DIR = os.path.join(TEMPLATE_DIR, 'root')
TEMPLATE_PLUGIN_DIR = os.path.join(TEMPLATE_DIR, 'plugin')

ROOT_FILES = [
    '.qgis-plugin-ci',
    'requirements.txt',
    'README.md',
    'LICENSE',
    'docs/development.md',
    'CHANGELOG.md',
    '.github/workflows/tests.yml',
    '.github/workflows/release.yml'
]
PLUGIN_FILES = [
    'test/test_1.py',
    'test/__init__.py',
    'test/pytest.ini',
    'metadata.txt',
    'build.py',
    'logs/.gitignore',
    '__init__.py',
    'plugin.py',
    'resources/ui/.gitignore',
    'resources/i18n/.gitignore',
    'resources/.gitignore',
    'resources/icons/.gitignore',
]


class PluginCreator:

    def __init__(self, organization: str, repo: str) -> None:
        self.organization = organization
        self.repo = repo

    def create(self):
        os.chdir(TEMPLATE_ROOT_DIR)
        for f in ROOT_FILES:
            self.copy_and_edit_file(ROOT_DIR, f)

        os.chdir(TEMPLATE_PLUGIN_DIR)
        for f in PLUGIN_FILES:
            self.copy_and_edit_file(PLUGIN_DIR, f)

    def copy_and_edit_file(self, dst_dir, f):
        print(f)
        dst_file = os.path.join(dst_dir, f)
        dst_file_dir = os.path.dirname(dst_file)
        if not os.path.exists(dst_file_dir):
            os.makedirs(dst_file_dir)
        shutil.copy2(f, dst_file)
        with open(dst_file) as fil:
            content = fil.read()
        content = (content.replace('<plugin_name>', PLUGIN_NAME)
                   .replace('<organization>', self.organization)
                   .replace('<repo>', self.repo))
        with open(dst_file, 'w') as fil:
            fil.write(content)


def parse_args():
    parser = argparse.ArgumentParser(prog='PG Initializer')
    parser.add_argument('-o', '--organization',
                        help='Github / Gitlab organization name. For example GispoCoding in https://github.com/GispoCoding/GlobeBuilder',
                        default='')
    parser.add_argument('-r', '--repository',
                        help='Github / Gitlab repository name. For example GlobeBuilder in https://github.com/GispoCoding/GlobeBuilder',
                        required=True)
    parser.add_argument('-v', '--verbose', type=bool, nargs='?', const=True, help='Verbose')

    if '-' in PLUGIN_NAME or ' ' in PLUGIN_NAME:
        raise ValueError(f'Plugin name {PLUGIN_NAME} contains illegal characters')

    return parser.parse_args()


def create_plugin():
    args = parse_args()
    creator = PluginCreator(args.organization, args.repository)
    creator.create()
