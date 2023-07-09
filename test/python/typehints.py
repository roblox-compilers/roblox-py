# TODO: Add compiler support for type hints, in functions and async functions.


def sum_numbers(a: int, b: int) -> int:
    return a + b

print(sum_numbers(10, 5))
print(sum_numbers(10.3, 5))
print(sum_numbers('Bob', 'Mark'))