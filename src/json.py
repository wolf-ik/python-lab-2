class JsonException(TypeError):
    def __init__(self, object_type):
        self.object_type = object_type

    def __str__(self):
        return str(type(self.object_type)) + ' is not JSON serializable'


def number_handler(value):
    return str(value)


def list_handler(value):
    result_str = []
    for element in value:
        result_str.append(to_json(element))
    return '[' + ', '.join(result_str) + ']'


def dict_handler(value):
    return_str = []
    for key in value.keys():
        if type(key) != str:
            return_str.append('"' + to_json(key) +
                              '": ' + to_json(value[key]))
        else:
            return_str.append(to_json(key) + ': ' + to_json(value[key]))
    return '{' + ', '.join(return_str) + '}'


def str_handler(value):
    return repr(value)


def null_handler(value):
    return 'null'


def bool_handler(value):
    if value:
        return 'true'
    else:
        return 'false'


def obj_handler(value):
    attributes = [attribute for attribute in dir(value)
    if not callable(attribute) and not attribute.startswith('__')]
    return dict_handler({attribute: getattr(value, attribute) for attribute in attributes})


handlers_mapping = {
    int: number_handler,
    float: number_handler,
    list: list_handler,
    tuple: list_handler,
    str: str_handler,
    unicode: str_handler,
    bool: bool_handler,
    dict: dict_handler,
    type(None): null_handler,
}


def to_json(obj, raise_unknown=False):
    handler = handlers_mapping.get(type(obj))
    if not handler:
        if raise_unknown:
            raise JsonException(obj)
        else:
            return obj_handler(obj)
    return handler(obj)


class Human(object):
    def __init__(self):
        self.a = 42
        self.b = [True, None]


if '__main__' == __name__:
    print to_json({"a'w": [True, False, None, 42, 2.5], 'b\'"\nw': ({'key': 'value'}, {'key2': 'hello'})})
    print to_json(Human())
    print to_json(Human(), raise_unknown=True)
