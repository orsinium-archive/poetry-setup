from pathlib import Path

from jinja2 import Environment
from poetry.poetry import Poetry


TEMPLATES_PATH = Path('templates')


class PoetrySetup:
    requirements_path = TEMPLATES_PATH / 'requirements.txt'

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
        with self.requirements_path.open() as f:
            document = f.read()
        template = Environment().from_string(document)
        return template.render(package=self.package)
