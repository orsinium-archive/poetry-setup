"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""
# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from os import path
# io.open is needed for projects that support Python 2.7
# It ensures open() defaults to text mode with universal newlines,
# and accepts an argument to specify the text encoding
# Python 3 only projects can skip this import
from io import open
here = path.abspath(path.dirname(__file__))
# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.
setup(
    # https://packaging.python.org/specifications/core-metadata/#name
    name='my-package',  # Required
    # https://www.python.org/dev/peps/pep-0440/
    # https://packaging.python.org/en/latest/single_source_version.html
    version='0.1.0',  # Required
    # https://packaging.python.org/specifications/core-metadata/#summary
    description="The description of the package",  # Required
    # https://packaging.python.org/specifications/core-metadata/#description-optional
    long_description=long_description,  # Optional
    # https://packaging.python.org/specifications/core-metadata/#description-content-type-optional
    long_description_content_type='text/markdown',  # Optional (see note above)
    url="https://github.com/sdispater/poetry",  # Optional
    author="Sébastien Eustace",  # Optional
    author_email="sebastien@eustace.io",  # Optional
    keywords=' '.join(['packaging', 'poetry']),  # Optional
    packages=find_packages(),  # Required
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=['peppercorn'],  # Optional
    # NOT SUPPORTED YET
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files
    data_files=[],  # Optional
    entry_points={  # Optional
        'console_scripts': [
            'my-script=my_package:main',
        ],
    },
    # https://packaging.python.org/specifications/core-metadata/#project-url-multiple-use
    project_urls={  # Optional
        'homepage': 'https://github.com/sdispater/poetry',
    },
)
