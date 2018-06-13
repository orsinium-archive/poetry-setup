from pathlib import Path

from jinja2 import Environment
from poetry.poetry import Poetry


TEMPLATES_PATH = Path('templates')


class PoetrySetup:
    # templates
    requirements_path = TEMPLATES_PATH / 'requirements.txt'

    # outputs
    requirements_name = 'requirements.txt'

    def __init__(self, path):
        if not isinstance(path, Path):
            path = Path(path)
        self.path = path
        self.package = self._get_package(path)

    @staticmethod
    def _get_package(path):
        poetry = Poetry.create(path)
        return poetry._package

    def get_requirements(self):
        with self.requirements_path.open(encoding='utf-8') as f:
            document = f.read()
        template = Environment().from_string(document)
        document = template.render(package=self.package)

        # rm junk
        document = document.replace('    ', '')
        # sort lines
        lines = sorted(line for line in document.split('\n') if line)
        document = '\n'.join(lines) + '\n'
        return document

    def sync(self):
        document = self.get_requirements()
        path = self.path / self.requirements_name
        with path.open('w', encoding='utf-8') as f:
            f.write(document)
