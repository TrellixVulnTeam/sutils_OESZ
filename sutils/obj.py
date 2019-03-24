class ADict(dict):
    """
    dict where you can get k/v from attr access
    """
    def __getstate__(self):
        return self.__dict__.items()

    def __setstate__(self, items):
        for key, val in items:
            self.__dict__[key] = val

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, dict.__repr__(self))

    def __setitem__(self, key, value):
        return super().__setitem__(key, value)

    def __getitem__(self, name):
        return super().__getitem__(name)

    def __delitem__(self, name):
        return super().__delitem__(name)

    __getattr__ = __getitem__
    __setattr__ = __setitem__

    def copy(self):
        ch = self.__class__(self)
        return ch
