import sys
from os import path
from pathlib import Path

from autopep8 import fix_code
from jinja2 import Environment
from poetry.io import NullIO
from poetry.masonry.builders.builder import Builder
from poetry.poetry import Poetry
from setuptools import find_packages
from yapf.yapflib.style import CreateGoogleStyle
from yapf.yapflib.yapf_api import FormatCode


TEMPLATES_PATH = Path(path.abspath(path.dirname(__file__))) / 'templates'


class PoetrySetup:
    # templates
    requirements_path = TEMPLATES_PATH / 'requirements.txt.j2'
    setup_path = TEMPLATES_PATH / 'setup.py.j2'

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

    @staticmethod
    def _format_vcs(req):
        result = '{r.vcs}+{r.source}@{r.reference}#egg={r.name}'.format(r=req)
        if req.extras:
            result += '[{}]'.format(','.join(req.extras))
        return result

    def get_requirements(self, optional=False):
        if not any(r.is_optional() == optional for r in self.package.all_requires):
            return
        with self.requirements_path.open(encoding='utf-8') as f:
            document = f.read()
        template = Environment().from_string(document)
        document = template.render(
            package=self.package,
            optional=optional,
            format_vcs=self._format_vcs,
        )
        # rm junk
        document = document.replace('    ', '')
        # sort lines
        lines = sorted(line for line in document.split('\n') if line)
        document = '\n'.join(lines) + '\n'
        return document

    def get_data_files(self):
        data_files = []
        for package in find_packages():
            path = Path(package)
            if not path.is_dir():
                continue
            for child in path.glob('**/*'):
                if not child.is_file():
                    continue
                if child.match('*.py'):
                    continue
                if child.match('*.pyc'):
                    continue
                data_files.append((str(child.parent), [str(child)]))
        return data_files

    def get_setup(self):
        # render template
        with self.setup_path.open(encoding='utf-8') as f:
            document = f.read()
        template = Environment().from_string(document)
        document = template.render(
            package=self.package,
            format_vcs=self._format_vcs,
            data_files=self.get_data_files(),
        )

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
