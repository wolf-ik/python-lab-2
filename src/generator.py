import random


def generate_file(filename, fields_count=None, lines_count=None,
                  field_separator='\t', line_separator='\n',	is_numeric=False):
    lines_count = random.randint(4, 4242) if not lines_count else lines_count
    fields_count = random.randint(2, 42) if not fields_count else fields_count
    with open(filename, 'w') as f:
        for _ in xrange(lines_count):
            for _ in xrange(fields_count):
                if is_numeric:
                    f.write('{}'.format(random.randint(-1000000, 1000000)))
                else:
                    for _ in xrange(random.randint(1, 42)):
                        f.write('{}'.format(chr(random.randint(97, 122))))
                f.write(field_separator)
            f.write(line_separator)

if '__main__' == __name__:
    print generate_file('sort.in', fields_count=1, lines_count=10000000, is_numeric=False)
