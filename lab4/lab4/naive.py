from lab4.utils import read_file, write_to_file, XMLUtils


def naive_convert(json_str: str):
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
        elif line.startswith('"') and "[" not in line:
            key, val = map(lambda x: x.strip(), line.removesuffix(",").replace('"', "").split(": "))
            xml.append(XMLUtils.tag(key, val))
    return "\n".join(xml)


if __name__ == "__main__":
    file = "data/wed_timetable.json"
    converted = naive_convert(read_file(file))
    write_to_file("data/naive_converted.xml", converted)
