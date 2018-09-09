from io import SEEK_SET, SEEK_CUR
import builtins
import contextlib
import inspect
import os
from expressivar.exceptions import UnmodifiableAttributeError
from expressivar.exceptions import UnmodifiableModeError
import wrapt


def is_file_like(f):
    return callable(getattr(f, 'read', None))


def file_or_path(strictmodes=False, strictparams=False, **argmap):
    """Checks whether named arguments to decorated functions are file-likeish

    File-likeish means either a string-like object representing a path to a
    file or a `file-like` object. If it is a file-like object, then pass it
    unmodified. Otherwise, the path will attempted to be opened and the
    resulting file-like object passed in its place.

    argmap is a mapping of function parameter names for the decorated fuction
    to the desired arguments to be passed to the opener for the file-likeish
    object.

    strictparams and strictmodes indicate open file attributes and how strictly
    they should be enforced. They cannot both be True. strictmodes will ensure
    the open file has the specified mode; if not, the decorated function will
    receive an open file object pointing to same underlying data, but with the
    specified mode. strictparams will present the decorated function with an
    open file object pointing to same underlying data, opened with the
    specified parameters.
    """

    if strictmodes and strictparams:
        raise ValueError(
            'Only one of strictmodes or strictparams can be specified.'
        )

    OPEN_KWDS = inspect.getfullargspec(builtins.open).args

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
                    try:
                        desired_mode = argmap[_name]['mode']
                    except KeyError:
                        raise ValueError('strictmodes requires a target mode.')
                    try:
                        actual_mode = _val.mode
                        if desired_mode != actual_mode:
                            to_reopen.append(
                                (_name, _val, {'mode': desired_mode})
                            )
                    except AttributeError as e:
                        raise UnmodifiableModeError(_val) from e
                elif strictparams:
                    desired_params = argmap[_name].copy()
                    try:
                        for key in desired_params:
                            if key not in OPEN_KWDS:
                                raise TypeError(
                                    "'{}' is not a valid keyword argument"
                                    "".format(key)
                                )
                    except (TypeError, AttributeError) as e:
                        raise UnmodifiableAttributeError((_val, key)) from e

                    # Always attempt to preserve mode
                    if 'mode' not in desired_params:
                        try:
                            mode = _val.mode
                            desired_params['mode'] = mode
                        except AttributeError as e:
                            pass
                    to_reopen.append((_name, _val, desired_params))

        with contextlib.ExitStack() as stack:
            for _key, _path in managed:
                _kwargs = argmap[_key]
                try:
                    w_args[_key] = stack.enter_context(open(_path, **_kwargs))
                except TypeError as e:
                    raise AttributeError(*e.args) from e
            for _key, _file, _kwargs in to_reopen:
                # TODO(zeroslack): handle possible OSError due to seek, tell...
                try:
                    w_args[_key] = stack.enter_context(
                        reopen(_file, **_kwargs)
                    )
                except TypeError as e:
                    raise UnmodifiableAttributeError((_val, *e.args)) from e
            return wrapped.__call__(**w_args)

    return inner


@contextlib.contextmanager
def reopen(fh, **kwargs):
    """Simply reopens a open file with a new paramaters."""
    try:
        pos = fh.tell()
        fd = os.dup(fh.fileno())
        with os.fdopen(fd, **kwargs) as file_:
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
