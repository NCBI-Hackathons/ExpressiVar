from io import SEEK_END
from io import StringIO
import builtins
import os

from expressivar import dec
import pytest


@pytest.fixture
def filehandle():
    s = StringIO('some nonesense')
    s.seek(0, SEEK_END)
    return s


def test_rewind(filehandle):
    with filehandle:
        assert filehandle.tell() != 0
        with dec.rewind(filehandle):
            assert filehandle.tell() == 0


def test_file_or_path_with_path(mocker, filehandle):
    @dec.file_or_path(infile='r')
    def dummy_func(infile):
        pass

    fname = '/some/non-existent/path'
    m = mocker.mock_open()
    mocker.patch.object(builtins, 'open', m)
    dummy_func(fname)
    dummy_func(filehandle)
    m.assert_called_once_with(fname, 'r')
