from types import FunctionType


class TracerInstance:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        result = self.func(*args, **kwargs)
        with open('logs.txt', 'a') as f:
            pattern = 'name-{0}\nargs-{2}\nkwargs-{3}\nres-{1}\n'.format(
                self.func.__name__, result, args[1:], kwargs)
            f.write(pattern + '\n')
        return result


def tracer(func):
    instance = TracerInstance(func)

    def on_call(*args, **kwargs):
        return instance(*args, **kwargs)
    return on_call


class Meta(type):
    def __new__(cls, classname, supers, classdict):
        for attr, attrval in classdict.items():
            if type(attrval) is FunctionType and not attrval.__name__.startswith('__'):
                classdict[attr] = tracer(attrval)
        return super(Meta, cls).__new__(cls, classname, supers, classdict)


class Logger(object):
    __metaclass__ = Meta

    def __str__(self):
        with open('logs.txt') as f:
            logs = f.read()
        return logs


class SomeClass(Logger):
    def __init__(self, value):
        self.value = value

    def foo(self, value):
        return value + self.value

    def bar(self, value=42):
        return str(value)


if '__main__' == __name__:
    instance = SomeClass(23)
    instance.foo(19)
    instance.bar(value=80)
    instance.bar()
    print instance
