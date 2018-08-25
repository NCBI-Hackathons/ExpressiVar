import inspect
import wrapt
import contextlib
from expressivar.exceptions import UnmodifiableModeError
from io import SEEK_SET, SEEK_CUR
import os


def is_file_like(f):
    return callable(getattr(f, 'read', None))


def file_or_path(strictmodes=False, **argmap):
    """Checks whether named arguments to decorated functions are file-likeish

    File-likeish means either a string-like object representing a path to a
    file or a `file-like` object. If it is a file-like object, then pass it
    unmodified. Otherwise, the path will attempted to be opened and the
    resulting file-like object passed in its place.
    """

    @wrapt.decorator
    def inner(wrapped, instance, args, kw):
        w_args = inspect.getcallargs(wrapped, *args, **kw)
        managed = []
        to_reopen = []
        for _name in argmap:
            _val = w_args.get(_name, None)
            if _val is None:
                continue
            if not is_file_like(_val):
                # throw here??
                managed.append((_name, _val))
            else:
                # This is file-like. Test modes if strictness specified
                if strictmodes:
                    desired_mode = argmap[_name]
                    try:
                        actual_mode = _val.mode
                        if desired_mode != actual_mode:
                            to_reopen.append((_name, _val, desired_mode))
                    except AttributeError as e:
                        raise UnmodifiableModeError(_val) from e
                else:
                    pass

        with contextlib.ExitStack() as stack:
            for _key, _path in managed:
                mode = argmap[_key]
                w_args[_key] = stack.enter_context(open(_path, mode))
            for _key, _file, _mode in to_reopen:
                # TODO(zeroslack): handle possible OSError due to seek, tell...
                w_args[_key] = stack.enter_context(reopen(_file, _mode))
            return wrapped.__call__(**w_args)

    return inner


@contextlib.contextmanager
def reopen(fh, mode):
    """Simply reopens a open file with a new mode."""
    try:
        pos = fh.tell()
        fd = os.dup(fh.fileno())
        with os.fdopen(fd, mode) as file_:
            file_.seek(pos)
            yield file_
    finally:
        pass


@contextlib.contextmanager
def rewind(fh):
    """Simply rewinds an open file."""
    pos, direction = 0, SEEK_CUR
    try:
        pos, direction = fh.tell(), SEEK_SET
        fh.flush()
        fh.seek(0)
        yield fh
    finally:
        with contextlib.suppress(OSError):
            fh.seek(pos, direction)
