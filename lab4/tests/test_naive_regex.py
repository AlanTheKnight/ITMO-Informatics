from lab4.naive_regex import naive_regex_convert
from lab4.utils import read_file
import unittest
import xml.etree.ElementTree as ET


class TestNaiveRegexXMLConvert(unittest.TestCase):
    def test_converter_complex(self) -> None:
        file = "data/wed_timetable.json"
        converted = naive_regex_convert(read_file(file))
        parsed = ET.fromstring(converted)
        self.assertEqual(parsed.tag, "root")
        self.assertEqual(len(parsed), 6)
        self.assertEqual(len(parsed[3]), 16)


if __name__ == "__main__":
    unittest.main()
