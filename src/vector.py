import numbers


class Vector(object):
    def __init__(self, coordinates):
        self.coordinates = tuple(coordinates)
        self.size = len(self.coordinates)

    def __str__(self):
        return 'Vector(' + ', '.join(str(x) for x in self.coordinates) + ')'

    def __add__(self, other):
        if other.size != self.size:
            raise AttributeError()
        return Vector(x + y for x, y in zip(self.coordinates, other.coordinates))

    def __sub__(self, other):
        if other.size != self.size:
            raise AttributeError()
        return Vector(x - y for x, y in zip(self.coordinates, other.coordinates))

    def __mul__(self, other):
        if isinstance(other, Vector):
            if other.size != self.size:
                raise AttributeError()
            return sum(x * y for x, y in zip(self.coordinates, other.coordinates))
        elif isinstance(other, numbers.Number):
            return Vector(x * other for x in self.coordinates)
        raise AttributeError()

    def __rmul__(self, other):
        return self.__mul__(other)

    def __len__(self):
        return self.size

    def __eq__(self, other):
        return self.coordinates == other.coordinates

    def __getitem__(self, index):
        if type(index) != int:
            raise AttributeError()
        return self.coordinates[index]


if '__main__' == __name__:
    a = Vector([42, 2, 3])
    b = Vector([42, 2, 4])
    print a + b
    print a - b
    print a * b
    print a * 2
    print 2 * a
