from typing import Union
from .utils import isdigit1to9, JSONTokens


class JSONParser:
    def __init__(self) -> None:
        """Initialize the parser."""
        self.raw_json = None
        self.i = 0
        self.parsed_data = None

    def advance(self, steps: int = 1) -> None:
        """Advance to the next symbol."""
        self.i += steps

    def eat_whitespace(self) -> None:
        """Skip space characters."""
        while self.raw_json[self.i] in JSONTokens.WHITESPACE:
            self.advance()

    def cur(self) -> str:
        """The current symbol."""
        return self.raw_json[self.i]

    def next(self) -> str:
        """The next symbol."""
        return self.raw_json[self.i + 1]

    def lookup(self, value) -> bool:
        """Check that the given value is located after the current symbol."""
        return (
            self.i + len(value) < len(self.raw_json)
            and self.raw_json[self.i : self.i + len(value)] == value
        )

    def eat(self, expected: Union[str, list]) -> None:
        """Advance to the next symbol expecting the current symbol to be of particular value."""
        if (
            isinstance(expected, str)
            and self.cur() == expected
            or isinstance(expected, list)
            and self.cur() in expected
        ):
            self.advance()
            return
        raise Exception(f'Parsing error at position {self.i}: "{expected}" expected.')

    def eat_number(self) -> int:
        """Read number symbols and return the whole number read."""
        fractional = False
        numeric_value_start = self.i
        if self.cur() == JSONTokens.MINUS:
            self.advance()

        if self.cur() == JSONTokens.ZERO and isdigit1to9(self.next()):
            raise Exception(f"Parsing error in number at position: {self.i}")

        if self.cur() == JSONTokens.ZERO:
            self.advance()

        while self.cur().isdecimal():
            self.advance()
        if self.cur() == ".":
            fractional = True
            self.advance()
            if not self.cur().isdecimal():
                raise Exception(f"Parsing error in number at position: {self.i}")
            while self.cur().isdecimal():
                self.advance()
        if self.cur() == "e" or self.cur() == "E":
            fractional = True
            self.advance()
            if self.cur() == "+" or self.cur() == "-":
                self.advance()
            if not self.cur().isdecimal():
                raise Exception(f"Parsing error in number at position: {self.i}")
            while self.cur().isdecimal():
                self.advance()
        final_value = self.raw_json[numeric_value_start : self.i]
        return float(final_value) if fractional else int(final_value)

    def eat_boolean(self) -> bool:
        """Read boolean value."""
        if self.lookup("true"):
            self.advance(4)
            return True
        elif self.lookup("false"):
            self.advance(5)
            return False
        raise Exception(f"Parsing error in boolean at position: {self.i}")

    def eat_string(self) -> str:
        """Read string symbols and return the whole string read."""
        string_value_start = self.i
        self.advance()
        while self.cur() != JSONTokens.QUOTE:
            if self.cur() == JSONTokens.BACKSLASH and self.next() in JSONTokens.CONTROL_CHARACTERS:
                self.advance()
                if self.cur() == "u":
                    self.advance()
                    for _ in range(4):
                        self.eat(JSONTokens.HEX)
                    continue
                self.advance()
                continue
            self.advance()
        self.advance()
        string = self.raw_json[string_value_start : self.i][1:-1]
        decoded = string.encode("latin-1", "backslashreplace").decode("unicode-escape")
        return decoded

    def eat_array(self) -> list:
        """Read array value recursively."""
        result = []
        self.eat_whitespace()
        while self.cur() != JSONTokens.RIGHT_BRACKET:
            result.append(self.eat_value())
            if self.cur() != JSONTokens.RIGHT_BRACKET:
                self.eat(JSONTokens.COMMA)
        return result

    def eat_null(self) -> None:
        """Read null value."""
        if self.lookup(JSONTokens.NULL):
            self.advance(4)
            return None

    def eat_value(self) -> Union[list, dict, int, str, None, bool]:
        """Read value of an array / object."""
        self.eat_whitespace()
        value = None
        if self.cur().isdigit() or self.cur() == JSONTokens.MINUS:
            value = self.eat_number()
        elif self.cur() == JSONTokens.QUOTE:
            value = self.eat_string()
        elif self.lookup(JSONTokens.TRUE) or self.lookup(JSONTokens.FALSE):
            value = self.eat_boolean()
        elif self.lookup(JSONTokens.NULL):
            value = self.eat_null()
        elif self.cur() == JSONTokens.LEFT_BRACKET:
            self.eat(JSONTokens.LEFT_BRACKET)
            value = self.eat_array()
            self.eat(JSONTokens.RIGHT_BRACKET)
        elif self.cur() == JSONTokens.LEFT_BRACE:
            self.eat(JSONTokens.LEFT_BRACE)
            value = self.eat_object()
            self.eat(JSONTokens.RIGHT_BRACE)
        else:
            raise Exception(f"Parsing error at position: {self.i}")
        self.eat_whitespace()
        return value

    def eat_object(self) -> dict:
        """Read objects value recursively."""
        result = {}
        self.eat_whitespace()
        while self.cur() != JSONTokens.RIGHT_BRACE:
            self.eat_whitespace()
            property_name = self.eat_string()
            self.eat_whitespace()
            self.eat(JSONTokens.COLON)
            property_value = self.eat_value()
            if self.cur() != JSONTokens.RIGHT_BRACE:
                self.eat(JSONTokens.COMMA)
            result[property_name] = property_value
        return result

    def parse(self, json_str: str) -> Union[dict, list]:
        """Parse JSON string."""
        self.raw_json = json_str
        self.i = 0
        self.parsed_data = None

        if self.cur() == JSONTokens.LEFT_BRACKET:
            self.advance()
            self.parsed_data = self.eat_array()
            self.eat(JSONTokens.RIGHT_BRACKET)
        elif self.cur() == JSONTokens.LEFT_BRACE:
            self.advance()
            self.parsed_data = self.eat_object()
            self.eat(JSONTokens.RIGHT_BRACE)
        else:
            raise Exception(f"Parsing error at position: {self.i}")
        return self.parsed_data

    def parse_file(self, filename: str) -> Union[dict, list]:
        """Parse JSON file."""
        with open(filename, "r", encoding="utf-8") as f:
            data = f.read()
        return self.parse(data)
