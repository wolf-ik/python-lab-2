def read_fields(filename):
    fields_dict = {}
    with open(filename, 'r') as f:
        for line in f:
            key, value = line.split()[:2]
            fields_dict[key] = value
    return fields_dict


def meta(filename):
    class FieldAdder(type):
        def __new__(cls, classname, supers, classdict):
            classdict.update(read_fields(filename))
            return super(FieldAdder, cls).__new__(cls, classname, supers, classdict)
    return FieldAdder


class SomeClass(object):
    __metaclass__ = meta('fields.txt')

    def __init__(self, value):
        self.value = value


if '__main__' == __name__:
    print SomeClass.__dict__
