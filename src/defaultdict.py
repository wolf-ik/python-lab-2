class DefaultDict(dict):
    def __init__(self, default=None):
        self.default = default
        super(DefaultDict, self).__init__()

    def missing(self, key):
        if self.default:
            self[key] = DefaultDict(self.default)
            return self[key]
        else:
            raise KeyError(key)

    def __getitem__(self, key):
        try:
            return super(DefaultDict, self).__getitem__(key)
        except KeyError:
            return self.missing(key)

if '__main__' == __name__:
    d = DefaultDict(int)
    d['a']['b']['c'] = 42
    print d
