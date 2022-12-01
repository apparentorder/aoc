import math
from .tools import cache


def factorial(n: int) -> int:
    """
    n! = 1 * 2 * 3 * 4 * ... * n
    1, 1, 2, 6, 24, 120, 720, ...
    """
    return math.factorial(n)


@cache
def fibonacci(n: int) -> int:
    """
    F(n) = F(n-1) + F(n-2) with F(0) = 0 and F(1) = 1
    0, 1, 1, 2, 3, 5, 8, 13, 21, ...
    """
    if n < 2:
        return n

    return fibonacci(n - 1) + fibonacci(n - 2)


def triangular(n: int) -> int:
    """
    a(n) = binomial(n+1,2) = n*(n+1)/2 = 0 + 1 + 2 + ... + n
    0, 1, 3, 6, 10, 15, ...
    """
    return n * (n + 1) // 2


def pentagonal(n: int) -> int:
    """
    A pentagonal number is a figurate number that extends the concept of triangular and square numbers to the pentagon
    0, 1, 5, 12, 22, 35, ...
    """
    return ((3 * n * n) - n) // 2
