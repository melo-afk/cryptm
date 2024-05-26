"""Square and multiply (pow)"""
import argparse
from typing import Optional, List


def test() -> None:
    """
    test against known results
    """
    assert square_n_multiply(17, 19, 23) == 5
    assert square_n_multiply(-7, 21, 23) == 13
    assert square_n_multiply(7, 2021, 1051) == 663
    assert square_n_multiply(953, 2211, 4799) == 2620

def square_n_multiply(base: int, power: int, mod: int) -> int:
    """
    Square and multiply [high-power-modulo] +++

    Args:
        base (int):
        power (int):
        mod (int):

    Returns:
        int: result
    """
    factors = get_factors(power)
    l = factors[0]  # -> highest factor
    x = 1
    while l >= 0:
        if l in factors:
            x = ((x**2) * base) % mod
        else:
            x = (x**2) % mod
        l -= 1
    return x


def get_factors(k: int) -> list[int]:
    """
    dividing k into powers of 2
    e.g: k=19 returns: [5,1,0] => 2^5+2^1+2^0=19
    """
    i, x = 0, 0
    a: list[int] = []
    while True:
        temp = 2**i
        if x == k:
            return a
        if x + temp > k:
            x += 2**(i - 1)
            a.append(i - 1)
            i = 0
        i += 1


def main(start: str, path: str, args: Optional[List[str]] = None) -> None:

    """
    Main entry point
    """
    parser = argparse.ArgumentParser(
        description='Square and multiply', prog=f"{start} {path}")
    parser.add_argument('base', type=int, help="base")
    parser.add_argument('power', type=int, help="power")
    parser.add_argument('mod', type=int, help="modulo")
    arg = parser.parse_args(args)
    print(square_n_multiply(arg.base, arg.power, arg.mod))


