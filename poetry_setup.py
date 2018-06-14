import sys
from os import path
from pathlib import Path
from tempfile import NamedTemporaryFile

from autopep8 import fix_code
from jinja2 import Environment
from poetry.io import NullIO
from poetry.masonry.builders.builder import Builder
from poetry.poetry import Poetry
from yapf.yapflib.style import CreateGoogleStyle
from yapf.yapflib.yapf_api import FormatCode

try:
    # pip>=10
    from pip._internal.download import PipSession
    from pip._internal.req import parse_requirements
except ImportError:
    from pip.download import PipSession
    from pip.req import parse_requirements


TEMPLATES_PATH = Path(path.abspath(path.dirname(__file__))) / 'templates'


class PoetrySetup:
    # templates
    requirements_path = TEMPLATES_PATH / 'requirements.txt'
    setup_path = TEMPLATES_PATH / 'setup.py'

    # outputs
    requirements_name = 'requirements.txt'
    constraints_name = 'constraints.txt'
    setup_name = 'setup.py'

    def __init__(self, path='.'):
        if not isinstance(path, Path):
            path = Path(path)
        self.path = path
        self.package = self._get_package(path)

    @staticmethod
    def _get_package(path):
        poetry = Poetry.create(path)
        package = poetry._package
        package.scripts = poetry._local_config.get('scripts')
        builder = Builder(poetry, venv=None, io=NullIO)
        # builder.find_files_to_add()
        package.entrypoints = builder.convert_entry_points()
        return package

    def get_requirements(self, optional=False):
        if not any(r.is_optional() == optional for r in self.package.all_requires):
            return
        with self.requirements_path.open(encoding='utf-8') as f:
            document = f.read()
        template = Environment().from_string(document)
        document = template.render(package=self.package, optional=optional)
        # rm junk
        document = document.replace('    ', '')
        # sort lines
        lines = sorted(line for line in document.split('\n') if line)
        document = '\n'.join(lines) + '\n'
        return document

    def get_setup(self):
        # get requirements
        # https://stackoverflow.com/a/16624700
        with NamedTemporaryFile('w', delete=False) as f:
            requirements = self.get_requirements()
            f.write(requirements)
            f.flush()
            requirements = parse_requirements(f.name, session=PipSession())
            requirements = [str(r.req) for r in requirements]

        # render template
        with self.setup_path.open(encoding='utf-8') as f:
            document = f.read()
        template = Environment().from_string(document)
        document = template.render(package=self.package, requirements=requirements)

        # format by yapf
        style = CreateGoogleStyle()
        document, _changed = FormatCode(document, style_config=style)
        # remove empty strings
        while '\n\n' in document:
            document = document.replace('\n\n', '\n')
        # format by autopep8
        document = fix_code(document)
        return document

    def sync(self):
        document = self.get_requirements(optional=False)
        if document:
            path = self.path / self.requirements_name
            with path.open('w', encoding='utf-8') as f:
                f.write(document)

        document = self.get_requirements(optional=True)
        if document:
            path = self.path / self.constraints_name
            with path.open('w', encoding='utf-8') as f:
                f.write(document)

        document = self.get_setup()
        path = self.path / self.setup_name
        with path.open('w', encoding='utf-8') as f:
            f.write(document)


def main(argv=sys.argv[1:]):
    PoetrySetup(*argv).sync()


if __name__ == '__main__':
    main()
