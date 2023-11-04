from lab4.utils import write_to_file
from lab4.json_parser import JSONParser
from lab4.converters import JSON2CSVConverter
import unittest


class TestJSONParser(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.parser = JSONParser()
        self.converter = JSON2CSVConverter()

    def test_converter_complex(self) -> None:
        file = "data/wed_timetable.json"
        data = self.parser.parse_file(file)["lessons"]
        converted = self.converter.convert(data)
        write_to_file("data/wed_timetable.csv", converted)


if __name__ == "__main__":
    unittest.main()
