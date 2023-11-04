from .utils import XMLUtils


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
