from .utils import XMLUtils, read_file, write_to_file
import re


WHITESPACE = r"\s*"
STRING = r"(?:\"[^\"]*\")"
BOOLEAN = r"(?:true|false)"
NULL = r"(?:null)"
NUMBER = r"-?(?:0|(?:[1-9]\d*))(?:\.[0-9]+)?(?:[eE](?:\+|-)?[0-9]+)?"
SIMPLE_VALUE = WHITESPACE + f"({STRING}|{NUMBER}|{BOOLEAN}|{NULL})" + WHITESPACE
OBJECT_PAIR = f"(?:\s*({STRING})\s*:{SIMPLE_VALUE})"


def naive_regex_convert(json_str: str):
    lines = list(map(lambda x: x.strip(), json_str.split("\n")))
    xml = []
    for ind, line in enumerate(lines):
        if ind == 0:
            xml.append(XMLUtils.PROLOG)
            xml.append(XMLUtils.opening_tag("root"))
            continue

        if ind == len(lines) - 1:
            xml.append(XMLUtils.closing_tag("root"))
            continue

        if "{" in line:
            xml.append(XMLUtils.opening_tag("lessons"))
        elif "}" in line:
            xml.append(XMLUtils.closing_tag("lessons"))
        elif m := re.match(OBJECT_PAIR, line):
            key, value = m.group(1)[1:-1], m.group(2)
            if value[0] == '"':
                value = value[1:-1]
            xml.append(XMLUtils.tag(key, value))

    return "\n".join(xml)


if __name__ == "__main__":
    file = "data/wed_timetable.json"
    converted = naive_regex_convert(read_file(file))
    write_to_file("data/naive_converted.xml", converted)
