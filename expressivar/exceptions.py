class UnmodifiableModeError(Exception):
    """Raised when file-like object has indeterminate open mode."""

    def __init__(self, target, *args, **kwargs):
        super().__init__(target, *args, **kwargs)
        self.target = target

    def __repr__(self):
        return '{}: {}'.format(self.__class__.__name__, self.target)


class UnmodifiableAttributeError(AttributeError):
    """Raised when file-like object attribute cannot be modified."""

    def __init__(self, target, *args, **kwargs):
        super().__init__(target, *args, **kwargs)
        self.target = target

    def __repr__(self):
        return '{}: {}'.format(self.__class__.__name__, self.target)
