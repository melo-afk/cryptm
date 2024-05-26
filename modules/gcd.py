"""Greatest common divisor"""
import argparse
from typing import Optional, List

def test() -> None:
    """
    test against known results
    """
    assert gcd(1560, 21) == 3
    assert gcd(1560, 65) == 65
    assert gcd(-3731,-11111) == -41
    assert gcd(769,307) == 1



def gcd(a: int, b: int) -> int:
    """
    Largest common divisor of a and b [basic] +++

    Args:
        a (int): number1
        b (int): number2

    Returns:
        int: common divisor
    """
    if abs(a) < abs(b):
        gcd(b, a)
    if b != 0:
        return gcd(b, a % b)
    return a


def main(start: str, path: str, args: Optional[List[str]] = None) -> None:

    """
    Main entry point
    """
    parser = argparse.ArgumentParser(
        description='gcd algorithm', prog=f"{start} {path}")
    parser.add_argument('num1', type=int, help="Number 1")
    parser.add_argument('num2', type=int, help="Number 2")
    arg = parser.parse_args(args)
    a = gcd(arg.num1, arg.num2)
    print(f"gcd of {arg.num1} and {arg.num2} is {a}")
