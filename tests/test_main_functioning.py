import sys
import pytest
import os

"""
test basic functioning of the program
"""


@pytest.fixture(scope='session')
def make_config(tmpdir_factory):
    # reusing function cause decorators syntax sugar lol :)
    def initsite(dire, input_dir, output_dir):
        with open(str(dire.join('sconfig.py')), 'w') as myfile:

            ##
            # Make the assets direcory and add a dumy file to it
            ##

            dire.mkdir('assets')
            open(str(dire.join('assets/testing.x')), 'a').close()

            myfile.writelines(
                ['CONTENT_DIR=\'%s\'\n' % str(dire.join(input_dir)),
                 'OUTPUT_DIR=\'%s\'\n' % str(dire.join(output_dir)),
                 'THEME_DIR=\'%s\'\n' % os.path.join(os.getcwd(), 'example_path'),
                 'ASSETS_PATH=\'%s\'\n' % str(dire.join('assets'))
                ]
            )

    dire = tmpdir_factory.mktemp("somedirectory")
    initsite(
        dire,
        'test_input',
        'test_output'
    )

    # register testing directory path
    sys.path.append(
        str(dire)
    )
    import sconfig
    funfun = str(dire.join('sconfig.py'))
    return funfun, sconfig


def test_init_site(make_config):
    a, b = make_config
    assert os.path.basename(b.CONTENT_DIR) == 'test_input'
    assert os.path.basename(b.OUTPUT_DIR) == 'test_output'


def test_make_site(make_config):
    a, b = make_config

    def makesite():
        from simplegen.simplegen import make
        make(quite=True)

    makesite()

    ##
    # assert for the output
    ##

    assert os.listdir(b.OUTPUT_DIR) == ['assets']
    assert os.listdir(os.path.join(b.OUTPUT_DIR, 'assets')) != []


def test_copy_assets(make_config):
    a, b = make_config

    def makesite():
        from simplegen.simplegen import make
        make(quite=True)

    makesite()

    assert 'testing.x' in os.listdir(os.path.join(b.OUTPUT_DIR, 'assets'))
