from json2xml import json2xml
from json2xml.utils import readfromstring
from .utils import read_file, write_to_file


def with_lib_convert(json_str: str):
    return json2xml.Json2xml(readfromstring(json_str)).to_xml()


if __name__ == "__main__":
    file = "data/wed_timetable.json"
    converted = with_lib_convert(read_file(file))
    write_to_file("data/with_lib_converted.xml", converted)
