"""Check if point exists on binary ec"""
import argparse
from typing import Optional, List
from char2.mul import mul
from char2.reduce import reduce
from curves_bin import Point, DomainParams
from __helper import auto_int


def test() -> None:
    """
    test against known results
    """
    assert exists(Point(0x3, 0x2), DomainParams(0x5, 0x1, 0xb)) is True
    assert exists(Point(0x3, 0x2), DomainParams(0x5, 0x1, 0xb)) is True
    assert exists(Point(0x3, 0x4), DomainParams(0x2, 0x4, 0xb)) is True
    assert exists(Point(0, 0x2), DomainParams(0x2, 0x4, 0xb)) is True
    assert exists(Point(0x2,0x2), DomainParams(0x2, 0x4, 0xb)) is False


def exists(p: Point, dp: DomainParams, silent: bool=True) -> bool:
    """
    Check if a point exists in the curve [ecc-point-char2]+++

    Args:
        r (int): r / x component of the point
        s (int): s / y component of the point
        a (int): paramter a of the elliptic curve
        b (int): paramter b of the elliptic curve
        p (int): the modulo of the galois field
        silent (bool, optional): no printing. Defaults to True.

    Returns:
        bool
    """
    # the infinite point always exists
    if p.r == p.s == -1:
        return True
    y_sq = mul(p.s, p.s, dp.rel)
    xy = mul(p.r, p.s, dp.rel)
    x_sq = mul(p.r, p.r, dp.rel)
    x_pow3 = mul(p.r, x_sq, dp.rel)
    ax = mul(x_sq, dp.a, dp.rel)
    total = reduce((y_sq ^ xy ^ x_pow3 ^ ax ^ dp.b), dp.rel)
    # s^2 + rs + r^3 + ar^2 + b

    if not silent:
        print(f"the point exists: {total==0}")
    return total == 0


def main(start: str, path: str, args: Optional[List[str]] = None) -> None:

    """
    Main entry point
    """
    parser = argparse.ArgumentParser(
        description='Check if the point exists on a binary ec', prog=f"{start} {path}")
    parser.add_argument('r', type=auto_int, help="r / x component of the point")
    parser.add_argument('s', type=auto_int, help="s / y component of the point")
    parser.add_argument('a', type=auto_int, help="paramter a of the elliptic curve")
    parser.add_argument('b', type=auto_int, help="paramter b of the elliptic curve")
    parser.add_argument('p', type=auto_int, help="the polynomial/defining relation of the galois field")
    arg = parser.parse_args(args)
    exists(Point(arg.r, arg.s), DomainParams(arg.a, arg.b, arg.p), silent=False)
