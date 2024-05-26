"""Euclidic algorithm to find inverse Elements in prime fields"""
import argparse
from typing import Optional, List


def test() -> None:
    """
    test against known results
    """
    assert egcd(769,307) == 511
    assert egcd(35,3) == 12
    assert egcd(21,5) == 17
    assert egcd(15,7) == 13


def egcd(a: int, b: int, silent: bool=True) -> int:
    """
    Extended Euclidean algorithm [basic] +++

    Args:
        a (int): First integer
        b (int): Second integer

    Returns:
        int: The modular inverse if it exists, otherwise 0
    """
    if abs(a) < abs(b):
        return egcd(b, a, silent)
    
    total = []
    old_a, old_b = a, b

    # normal gcd steps
    while b != 0:
        flr = a // b
        a, b = b, a - flr * b
        total.append([a, flr, b])

    if a != 1:
        raise RuntimeError("gcd ist not 1, can not compute the egcd")

    x, y = 1, 0
    for _, flr, _ in reversed(total):
        x, y = y, x - flr * y

    result = y if old_a > old_b else x
    result = result % old_a

    if not silent:
        print(f"1 = {result} * {old_a} + {y} * {old_b}")

    return result


def main(start: str, path: str, args: Optional[List[str]] = None) -> None:

    """
    Main entry point
    """
    parser = argparse.ArgumentParser(
        description='Extended euclidic algorithm', prog=f"{start} {path}")
    parser.add_argument('num1', type=int, help="Number 1")
    parser.add_argument('num2', type=int, help="Number 2")
    arg = parser.parse_args(args)
    egcd(arg.num1, arg.num2, silent=False)
