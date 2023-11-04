from json2xml import json2xml
from json2xml.utils import readfromstring


def with_lib_convert(json_str: str):
    return json2xml.Json2xml(readfromstring(json_str)).to_xml()
