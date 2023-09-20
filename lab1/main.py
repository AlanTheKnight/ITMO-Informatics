def fibonacci_generator():
    """Yield the next Fibonacci number."""
    a, b = 1, 1
    while True:
        yield a
        a, b = b, a + b


def fibonacci_to_decimal(fib_string: str):
    """Convert a Fibonacci number to decimal."""
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
