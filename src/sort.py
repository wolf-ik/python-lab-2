from multiprocessing.pool import ThreadPool
import argparse
import tempfile
import heapq


MAX_THREADS = 2
MAX_FILES_PER_THREAD = 1e5


def parse_args():
    parser = argparse.ArgumentParser(description='My wonderful description.')
    parser.add_argument('-in', '-input', type=str, dest='input_file', help='Input file name.')
    parser.add_argument('-out', '--output', type=str, dest='output_file', help='Output file name.')
    parser.add_argument('-bf', '--buffer_size', type=int, dest='buffer_size', help='Buffer size (lines).')
    return parser.parse_args()


def set_default_args(args):
    default = {
        'buffer_size': 1e5,
        'input_file': 'sort.in',
        'output_file': 'sort.out',
    }
    for arg, value in args.__dict__.items():
        if value is None:
            args.__dict__[arg] = default[arg]


def save_lines_to_tempfile(lines):
    f = tempfile.NamedTemporaryFile(delete=True)
    for line in sorted(lines):
        f.write("{0}{1}".format(line, '\n'))
    f.seek(0)
    return f


def get_temp_files_from_input(input_file, buffer_size):
    res = []
    buf = 0
    current_lines =[]
    for in_line in input_file:
        if buf >= buffer_size:
            res.append(save_lines_to_tempfile(current_lines))
            buf = 1
            current_lines = [in_line]
        else:
            buf += 1
            current_lines.append(in_line)
    if buf > 0:
        res.append(save_lines_to_tempfile(current_lines))
    return res
            

def get_files_for_merge(cur_lvl, max_count):
    res = []
    for i in xrange(min(max_count, len(cur_lvl))):
        res.append(cur_lvl.pop())
    return res


def merge(files):
    f = tempfile.NamedTemporaryFile(delete=True)
    for line in heapq.merge(*files):
        if line != '\n':
            f.write("{0}{1}".format(line, '\n'))
    for old_f in files:
        old_f.close()
    f.seek(0)
    return f


def main():
    thread_pool = ThreadPool(processes=MAX_THREADS)
    args = parse_args()
    set_default_args(args)
    
    with open(args.input_file, 'r') as input_file:
        cur_lvl = get_temp_files_from_input(input_file, args.buffer_size)
    if len(cur_lvl) == 0:
        raise ValueError("No data was fuond.")
    next_lvl = []
    
    while len(cur_lvl) != 1:
        async_res = []
        while len(cur_lvl) > 0:
            files = get_files_for_merge(cur_lvl, MAX_FILES_PER_THREAD)
            async_res.append(thread_pool.apply_async(merge, (files,)))
            #next_lvl.append(merge(files))
        for async in async_res:
            next_lvl.append(async.get())
        cur_lvl = next_lvl
        next_lvl = []
    
    with open(args.output_file, 'w') as output_file:
        for line in cur_lvl[0]:
            if line != '\n':
                output_file.write(line)


if '__main__' == __name__:
    main()

