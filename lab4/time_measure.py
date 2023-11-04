from lab4.converters import JSON2XMLConverter
from lab4.json_parser import JSONParser
from lab4.naive import naive_convert
from lab4.naive_regex import naive_regex_convert
from lab4.with_lib import with_lib_convert
from lab4.utils import read_file
import json
import time


def time_measure(func, repeat=100):
    def inner(*args, **kwargs):
        start = time.perf_counter_ns()
        for _ in range(repeat):
            func(*args, **kwargs)
        end = time.perf_counter_ns()
        diff = (end - start) / 1e6
        print(f"{func.__name__}: {diff} ms")

    return inner


@time_measure
def custom_parser_test(content):
    JSONParser().parse(content)


@time_measure
def stdlib_parser_test(content):
    json.loads(content)


@time_measure
def naive_convert_test(content):
    naive_convert(content)


@time_measure
def naive_regex_convert_test(content):
    naive_regex_convert(content)


@time_measure
def with_lib_convert_test(content):
    with_lib_convert(content)


@time_measure
def custom_convert_test(content):
    JSON2XMLConverter().convert(JSONParser().parse(content))


def main():
    file = "data/wed_timetable.json"
    content = read_file(file)
    print("Parsers:")
    custom_parser_test(content)
    stdlib_parser_test(content)
    print("Converters:")
    naive_convert_test(content)
    naive_regex_convert_test(content)
    with_lib_convert_test(content)
    custom_convert_test(content)


if __name__ == "__main__":
    main()
