from lab4.json_parser import JSONParser
import json
import unittest


class TestJSONParser(unittest.TestCase):
    def setUp(self) -> None:
        self.parser = JSONParser()

    def test_parse_complex(self):
        file = "data/week_timetable.json"
        data = json.load(open(file, "r"))
        self.assertEqual(self.parser.parse_file(file), data)

    def test_parse_numbers(self):
        test_str = '{"number": 123}'
        self.assertEqual(self.parser.parse(test_str), {"number": 123})

    def test_parse_zero(self):
        test_str = '{"number": 0}'
        self.assertEqual(self.parser.parse(test_str), {"number": 0})

    def test_parse_incorrect_number(self):
        test_str = '{"number": 01}'
        with self.assertRaises(Exception):
            self.parser.parse(test_str)

    def test_parse_negative_number(self):
        test_str = '{"number": -123}'
        self.assertEqual(self.parser.parse(test_str), {"number": -123})

    def test_parse_float(self):
        test_str = '{"number": 123.456}'
        self.assertEqual(self.parser.parse(test_str), {"number": 123.456})

    def test_parse_negative_float(self):
        test_str = '{"number": -123.456}'
        self.assertEqual(self.parser.parse(test_str), {"number": -123.456})

    def test_parse_incorrect_float(self):
        test_str = '{"number": 123.}'
        with self.assertRaises(Exception):
            self.parser.parse(test_str)

    def test_parse_incorrect_float2(self):
        test_str = '{"number": 123.abc}'
        with self.assertRaises(Exception):
            self.parser.parse(test_str)

    def test_parse_incorrect_float3(self):
        test_str = '{"number": 123.123.123}'
        with self.assertRaises(Exception):
            self.parser.parse(test_str)

    def test_parse_incorrect_float4(self):
        test_str = '{"number": 123.123.}'
        with self.assertRaises(Exception):
            self.parser.parse(test_str)

    def test_parse_exponent(self):
        test_str = '{"number": 123e10}'
        self.assertEqual(self.parser.parse(test_str), {"number": 123e10})

    def test_parse_strings(self):
        test_str = '{"string": "abc"}'
        self.assertEqual(self.parser.parse(test_str), {"string": "abc"})

    def test_parse_empty_string(self):
        test_str = '{"string": ""}'
        self.assertEqual(self.parser.parse(test_str), {"string": ""})

    def test_parse_string_with_spaces(self):
        test_str = '{"string": "a b c"}'
        self.assertEqual(self.parser.parse(test_str), {"string": "a b c"})

    def test_parse_array(self):
        test_str = '{"array": [1, 2, 3]}'
        self.assertEqual(self.parser.parse(test_str), {"array": [1, 2, 3]})

    def test_parse_nested_array(self):
        test_str = '{"array": [1, [2, 3]]}'
        self.assertEqual(self.parser.parse(test_str), {"array": [1, [2, 3]]})

    def test_parse_nested_object(self):
        test_str = '{"object": {"key": "value"}}'
        self.assertEqual(self.parser.parse(test_str), {"object": {"key": "value"}})

    def test_escape_characters(self):
        test_str = '{"val1": "\\"test\\""}'
        self.assertEqual(self.parser.parse(test_str), {"val1": '"test"'})

    def test_cyrillic(self):
        test_str = '{"val1": "абв"}'
        self.assertEqual(self.parser.parse(test_str), {"val1": "абв"})


if __name__ == "__main__":
    unittest.main()
