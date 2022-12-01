import math
from decimal import Decimal, ROUND_HALF_UP
from .types import Numeric


def round_half_up(number: Numeric) -> int:
    """ pythons round() rounds .5 to the *even* number; 0.5 == 0 """
    return int(Decimal(number).to_integral(ROUND_HALF_UP))


def get_factors(num: int) -> set:
    f = {num}
    for x in range(1, int(math.sqrt(num)) + 1):
        if num % x == 0:
            f.add(x)
            f.add(num // x)

    return f
