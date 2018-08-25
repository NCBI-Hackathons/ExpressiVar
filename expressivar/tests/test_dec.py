from io import SEEK_END
from io import StringIO
from tempfile import TemporaryFile
import builtins
import os

from expressivar import dec
from expressivar import exceptions
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


def test_file_or_path_strictmodes(mocker, filehandle):
    expected_mode = 'r'

    @dec.file_or_path(infile=expected_mode, strictmodes=True)
    def dummy_func(infile):
        pass

    with pytest.raises(exceptions.UnmodifiableModeError) as excinfo:
        dummy_func(filehandle)
    assert str(filehandle) in str(excinfo.value)

    m = mocker.patch.object(os, 'fdopen')
    with TemporaryFile(mode='rb') as fh:
        dummy_func(fh)
        old_fd = fh.fileno()
        fdopen_call = m.call_args[0]
        new_fd, new_mode = fdopen_call
        assert new_mode == expected_mode
        assert os.fstat(old_fd) == os.fstat(new_fd)
