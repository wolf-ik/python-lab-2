from itertools import tee


class Sequence(object):
    def __init__(self, iterable):
        self.iterable = iterable

    def __iter__(self):
        res, self.iterable = tee(iter(self.iterable))
        return res

    def filter(self, func):
        return Sequence((x for x in self.iterable if func(x)))


if '__main__' == __name__:
    l = Sequence((x for x in [1, 42, 6, 84, 12]))
    i = l.filter(lambda x: x % 2 == 0).filter(lambda x: x % 21 == 0)
    print list(i)
    print list(i)
