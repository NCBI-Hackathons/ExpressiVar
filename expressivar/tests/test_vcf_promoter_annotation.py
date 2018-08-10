import os.path
import tempfile

import expressivar
from expressivar.vcf import promoter_annotator
import pytest


@pytest.fixture
def tests_basedir():
    pkg_base = os.path.dirname(expressivar.__file__)
    return os.path.join(pkg_base, 'tests')


@pytest.fixture
def input_file():
    return os.path.join(tests_basedir(), 'data', 'annotated_promoter_input.vcf')


@pytest.fixture
def output_file():
    return tempfile.mkstemp()[-1]


def test_promoter_annotation(input_file, output_file):
    promoter_annotator.annotate_effective_promoters(input_file, output_file)
    print(input_file)
    print(output_file)
    os.unlink(output_file)
