from lab4.converters import JSON2XMLConverter
from lab4.json_parser import JSONParser
from lab4.utils import write_to_file
import unittest
import xml.etree.ElementTree as ET


class TestXMLConverter(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.parser = JSONParser()
        self.converter = JSON2XMLConverter()

    def test_week_timetable(self) -> None:
        file = "data/week_timetable.json"
        converted = self.converter.convert(self.parser.parse_file(file))
        write_to_file("data/week_timetable.xml", converted)
        parsed = ET.fromstring(converted)
        self.assertEqual(parsed.tag, "root")

    def test_converter_complex(self) -> None:
        file = "data/wed_timetable.json"
        converted = self.converter.convert(self.parser.parse_file(file))
        write_to_file("data/wed_timetable.xml", converted)
        parsed = ET.fromstring(converted)
        self.assertEqual(parsed.tag, "root")


if __name__ == "__main__":
    unittest.main()
