from pathlib import Path

from jinja2 import Environment
from poetry.poetry import Poetry
from yapf.yapflib.yapf_api import FormatCode
from yapf.yapflib.style import CreateGoogleStyle
from autopep8 import fix_code


TEMPLATES_PATH = Path('templates')


class PoetrySetup:
    # templates
    requirements_path = TEMPLATES_PATH / 'requirements.txt'
    setup_path = TEMPLATES_PATH / 'setup.py'

    # outputs
    requirements_name = 'requirements.txt'
    constraints_name = 'constraints.txt'
    setup_name = 'setup.py'

    def __init__(self, path):
        if not isinstance(path, Path):
            path = Path(path)
        self.path = path
        self.package = self._get_package(path)

    @staticmethod
    def _get_package(path):
        poetry = Poetry.create(path)
        package = poetry._package
        package.scripts = poetry._local_config.get('scripts')
        return package

    def get_requirements(self, optional=False):
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
        with self.setup_path.open(encoding='utf-8') as f:
            document = f.read()
        template = Environment().from_string(document)
        document = template.render(package=self.package)
        # format
        style = CreateGoogleStyle()
        document, _changed = FormatCode(document, style_config=style)
        # remove empty strings
        while '\n\n' in document:
            document = document.replace('\n\n', '\n')
        document = fix_code(document)
        return document

    def sync(self):
        required = self.get_requirements(optional=False)
        path = self.path / self.requirements_name
        with path.open('w', encoding='utf-8') as f:
            f.write(required)

        optional = self.get_requirements(optional=True)
        if optional != required:
            path = self.path / self.constraints_name
            with path.open('w', encoding='utf-8') as f:
                f.write(optional)

        document = self.get_setup()
        path = self.path / self.setup_name
        with path.open('w', encoding='utf-8') as f:
            f.write(document)
