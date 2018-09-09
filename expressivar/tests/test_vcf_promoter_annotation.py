import os.path
import tempfile

import expressivar
from expressivar.dec import rewind
from expressivar.vcf import promoter_annotator
import pytest


@pytest.fixture
def tests_basedir(scope='session'):
    """Base directory for tests."""
    pkg_base = os.path.dirname(expressivar.__file__)
    return os.path.join(pkg_base, 'tests')


@pytest.fixture
def input_file(tests_basedir):
    return os.path.join(tests_basedir, 'data', 'annotated_promoter_input.vcf')


@pytest.fixture
def output_file():
    """Temporary output file."""
    return tempfile.TemporaryFile(mode='w+')


@pytest.fixture
def expected_output(tests_basedir):
    ofile = os.path.join(
        tests_basedir, 'data', 'annotated_promoter_output.txt'
    )
    with open(ofile, 'r') as f:
        return f.read()


def test_promoter_annotation(input_file, output_file, expected_output):
    with output_file:
        promoter_annotator.annotate_effective_promoters(
            input_file, output_file
        )
        with rewind(output_file):
            assert output_file.read() == expected_output
