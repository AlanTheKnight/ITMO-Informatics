from typing import Union, Any
from .utils import XMLUtils


class AbstractConverter:
    def __init__(self) -> None:
        """Initialize the converter."""
        self.result = ""
        self.indent = 4

    def empty_output(self) -> None:
        self.result = ""

    def convert(self, value: Any, indent: int = 4) -> str:
        self.indent = indent
        self.empty_output()


class JSON2XMLConverter(AbstractConverter):
    def empty_output(self) -> None:
        super().empty_output()
        self.write_xml(XMLUtils.PROLOG)

    def write_xml(self, content: str, depth: int = 0, newline: bool = True):
        """Write XML line to the output."""
        spaces = " " * self.indent * depth
        self.result += spaces + content + ("\n" if newline else "")

    def objectConvert(self, obj: dict, depth: int = 1):
        for key, val in obj.items():
            if isinstance(val, dict):
                # If the value is an object, recursively write it
                # to XML, increasing the indent
                if isinstance(val, dict) or isinstance(val, list):
                    self.write_xml(XMLUtils.tag(key, val), depth)
                else:
                    self.write_xml(XMLUtils.opening_tag(key), depth)
                    self.objectConvert(val, depth + 1)
                    self.write_xml(XMLUtils.closing_tag(key), depth)
            elif isinstance(val, list):  # If the value is an array
                self.arrayConvert(val, key, depth)
            else:  # Then values are simple values
                self.write_xml(XMLUtils.tag(key, str(val)), depth)

    def arrayConvert(self, a: list, key: Union[str, None], depth: int = 1):
        for i, item in enumerate(a):
            # Dynamic key for array that isn't a value of an object
            cur_key = f"col-{i}" if key is None else key
            if isinstance(item, dict) or isinstance(item, list):
                # If the item is an object or an array
                self.write_xml(XMLUtils.opening_tag(cur_key), depth)
                self.toXML(item, depth + 1)
                self.write_xml(XMLUtils.closing_tag(cur_key), depth)
            else:
                # Then items are simple values
                self.write_xml(XMLUtils.tag(cur_key, str(item)), depth)

    def toXML(self, value: Union[dict, list], depth=1):
        """Convert value (object or array) to the XML format"""
        if isinstance(value, dict):
            return self.objectConvert(value, depth)
        elif isinstance(value, list):
            return self.arrayConvert(value, None, depth)
        raise Exception("toXML() used with neither a dict nor a list.")

    def convert(self, value: Any, indent: int = 4) -> Union[dict, list]:
        """Convert the parsed output to the XML format."""
        super().convert(value, indent)
        self.write_xml(XMLUtils.opening_tag("root"))
        self.toXML(value)
        self.write_xml(XMLUtils.closing_tag("root"))
        return self.result


class JSON2CSVConverter(AbstractConverter):
    def csvProcess(self, value: Any):
        return str(value).replace('"', '\\"').replace(",", "\\,")

    def separateByCommas(self, a: list) -> str:
        """Separate the list by commas."""
        return ",".join(map(self.csvProcess, a))

    def convert(self, value: Any, indent: int = 4) -> str:
        """Convert the parsed output to the CSV format."""
        super().convert(value, indent)

        # If the parsed data is an object, write it's columns separated by
        # commas, then write values separated by commas
        if isinstance(value, dict):
            self.result += self.separateByCommas(value.keys()) + "\n"
            self.result += self.separateByCommas(value.values())
            return self.result
        # If the parsed data is an array of objects, write the first row with the keys
        # and then write the values of each object separated by commas
        elif isinstance(value, list) and all([isinstance(obj, dict) for obj in value]):
            keys = set()
            for obj in value:
                keys.update(obj.keys())

            self.result += self.separateByCommas(keys) + "\n"
            for obj in value:
                self.result += self.separateByCommas([obj.get(key, "") for key in keys]) + "\n"
            return self.result
        else:
            raise Exception("CSV converter used with neither a dict nor a list of dicts.")
