import inspect
import wrapt
import contextlib

def is_file_like(f):
    return callable(getattr(f, 'read', None))

def file_or_path(**argmap):
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
        for _name in argmap:
            _val = w_args.get(_name, None)
            if _val is None:
                continue
            if not is_file_like(_val):
            # throw here??
                managed.append((_name, _val))

        with contextlib.ExitStack() as stack:
            for _key, _path in managed:
                mode = argmap[_key]
                w_args[_key] = stack.enter_context(open(_path, mode))
            return wrapped.__call__(**w_args)

    return inner

if __name__ == '__main__':
    @file_or_path(inputfile='r', outputfile='w')
    def foo(inputfile, outputfile):
        print('in foo()')

    import tempfile
    with tempfile.TemporaryFile() as ofile:
        foo('foobar', 'foo')
