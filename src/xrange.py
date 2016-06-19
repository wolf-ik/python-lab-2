class XRange(object):
    def __init__(self, start, end=None, step=1):
        if end is None:
            self.start = 0
            self.end = start
        else:
            self.start = start
            self.end = end
        self.step = step

    def __len__(self):
        return (self.end - self.start) / self.step + 1

    def __iter__(self):
        current = self.start
        while current < self.end:
            yield current
            current += self.step

    def __getitem__(self, index):
        current_index = 0
        current = self.start
        while current_index < index:
            current_index += 1
            current += self.step
            if current > self.end:
                raise IndexError()
        return current

    def __str__(self):
        if self.step == 1 and self.start == 0:
            return 'XRange({})'.format(self.end)
        elif self.step == 1 and self.start != 0:
            return 'XRange({}, {})'.format(self.start, self.end)
        else:
            return 'XRange({}, {}, {})'.format(self.start, self.end, self.step)

if '__main__' == __name__:
    print XRange(42)
    print XRange(5, step=2)[1]
    try:
        XRange(5)[6]
    except IndexError:
        print 'nice'
