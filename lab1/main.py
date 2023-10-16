import re


def validate_input(fib_string: str):
    """Check if input is a valid Fibonacci number.

    A string is considered a valid number if:
    - It starts with 1
    - It consists of 1's and 0's
    - It doesn't have two consequent 1's
    """
    return re.fullmatch(r"^1(0|((?<!1)1))*$", fib_string)


def fibonacci_generator():
    """Yield the next Fibonacci number."""
    a, b = 1, 1
    while True:
        yield a
        a, b = b, a + b


def fibonacci_to_decimal(fib_string: str):
    """Convert a Fibonacci number to decimal."""
    if not validate_input(fib_string):
        raise ValueError("Provided value is an incorrent Fibonacci number.")

    fibonacci = fibonacci_generator()
    next(fibonacci)  # Skip the first Fibonacci number

    result = 0
    for char in fib_string[::-1]:
        cur = next(fibonacci)
        if char == "1":
            result += cur
    return result


if __name__ == "__main__":
    fib_string = input("Enter a Fibonacci number: ")
    print("Result:", fibonacci_to_decimal(fib_string))
