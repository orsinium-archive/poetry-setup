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
    name='{{ package.name }}',  # Required
    # https://www.python.org/dev/peps/pep-0440/
    # https://packaging.python.org/en/latest/single_source_version.html
    version='{{ package.version }}',  # Required
    # https://packaging.python.org/specifications/core-metadata/#summary
    description={{ package.description }},  # Required
    # https://packaging.python.org/specifications/core-metadata/#description-optional
    long_description=long_description,  # Optional
    # https://packaging.python.org/specifications/core-metadata/#description-content-type-optional
    long_description_content_type='text/markdown',  # Optional (see note above)

    {% if package.homepage %}
        url={{ package.homepage }},  # Optional
    {% endif %}
    {% if package.author_name %}
        author={{ package.author_name }},  # Optional
    {% endif %}

    {% if package.author_email %}
        author_email={{ package.author_email }},  # Optional

        {% endif %}
    {% package.classifiers %}
        # For a list of valid classifiers, see https://pypi.org/classifiers/
        classifiers=[  # Optional
            {% for cl in package.classifiers %}
                '{{ cl }}',
            {% endfor %}
        ],
    {% endif %}

    {% if package.keywords %}
        keywords=(
            {% for kw in package.keywords %}
                ' {{ kw }}'
            {% endfor %}
        ),  # Optional
    {% endif %}

    packages=find_packages(
        {% if package.exclude %}
        exclude=[
            {% for ex in package.exclude %}
                '{{ ex }}',
            {% endfor %}
        ]
        {% endif %}
    ),  # Required

    # https://packaging.python.org/en/latest/requirements.html
    install_requires=['peppercorn',  # Optional

    {% if package.extras %}
        extras_require={{ package.extras|pprint }},
    {% endif %}

    package_data={  # Optional
        'sample': ['package_data.dat'],
    },

    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files
    data_files=[('my_data', ['data/data_file'])],  # Optional

    entry_points={  # Optional
        'console_scripts': [
            'sample=sample:main',
        ],
    },

    # https://packaging.python.org/specifications/core-metadata/#project-url-multiple-use
    project_urls={  # Optional
        'Bug Reports': 'https://github.com/pypa/sampleproject/issues',
        'Funding': 'https://donate.pypi.org',
        'Say Thanks!': 'http://saythanks.io/to/example',
        'Source': 'https://github.com/pypa/sampleproject/',
    },
)
