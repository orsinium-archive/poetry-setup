from poetry_setup import PoetrySetup


def test_requirements():
    ps = PoetrySetup('example')
    rs = ps.get_requirements(optional=False)
    assert 'toml (>=0.9,<0.10)\n' in rs
    assert '-e git+https://github.com/sdispater/cleo.git@master#egg=cleo\n' in rs

    cs = ps.get_requirements(optional=True)
    assert 'pendulum' not in rs
    assert 'pendulum' in cs


def test_setup():
    ps = PoetrySetup('example')
    setup = ps.get_setup()
    assert "name='example'," in setup           # name
    assert "version='0.1.0'," in setup          # version
    assert 'pathlib2 (>=2.2,<3.0)' in setup     # requirements
    assert '; python_version >= "2.7" and python_version < "2.8"' in setup  # marker
    assert "my-script=example.core:main" in setup   # entrypoints
