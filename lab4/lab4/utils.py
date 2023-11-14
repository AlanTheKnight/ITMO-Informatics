from typing import Union


def read_file(filename: str) -> str:
    with open(filename, "r") as f:
        data = f.read()
    return data


def write_to_file(filename: str, content: str) -> None:
    with open(filename, "w") as f:
        f.write(content)
    return content


class XMLUtils:
    PROLOG = '<?xml version="1.0" encoding="UTF-8"?>'

    @classmethod
    def opening_tag(cls, tag_name: str, attrs: Union[dict, None] = None):
        """Return XML opening tag with the given name and attributes."""
        if attrs is None:
            return f"<{tag_name}>"
        attrs_str = " ".join([f'{key}="{value}"' for key, value in attrs.items()])
        return f"<{tag_name} {attrs_str}>"

    @classmethod
    def tag(cls, tag_name: str, value: str, attrs: Union[dict, None] = None):
        """Return XML tag with the given name, value and attributes."""
        return cls.opening_tag(tag_name, attrs) + value + cls.closing_tag(tag_name)

    @classmethod
    def closing_tag(cls, tag_name: str):
        """Return XML closing tag with the given name."""
        return f"</{tag_name}>"


def isdigit1to9(val: str):
    return val.isdecimal() and val != "0"


class JSONTokens:
    WHITESPACE = [" ", "\n", "\t"]
    QUOTE = '"'
    MINUS = "-"
    LEFT_BRACKET = "["
    RIGHT_BRACKET = "]"
    LEFT_BRACE = "{"
    RIGHT_BRACE = "}"
    COLON = ":"
    COMMA = ","
    TRUE = "true"
    FALSE = "false"
    NULL = "null"
    EXPONENT = ["e", "E"]
    PLUS = "+"
    DOT = "."
    ZERO = "0"
    BACKSLASH = "\\"
    CONTROL_CHARACTERS = ['"', "\\", "/", "b", "f", "n", "r", "t", "u"]
    HEX = list("0123456789abcdefABCDEF")
