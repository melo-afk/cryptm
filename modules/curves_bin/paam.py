"""Multiply a point on a binary ec"""
import argparse
from typing import Optional, List
from sqm import get_factors
from curves_bin import Point, DomainParams
from curves_bin.padd import add_points
from curves_bin.pdupe import dupe_point
from curves_bin.pexists import exists
from __helper import auto_int


def test() -> None:
    """
    test against known results
    """
    assert mul_point(4, Point(0x3, 0x2), DomainParams(0x5, 0x1, 0xb)) == Point(0x5, 0x6)
    assert mul_point(5, Point(0x3, 0x2), DomainParams(0x5, 0x1, 0xb)) == Point(0x7, 0x4)


def mul_point(m: int, p: Point, dp: DomainParams, silent: bool=True) -> Point:
    """
    Multiply a point with Add and Multiply: e.g 5 * P(r,s) [ecc-point-char2]+++

    Args:
        m (int): amount of multiplications
        r (int): r / x component of the point
        s (int): s / y component of the point
        a (int): paramter a of the elliptic curve
        b (int): paramter b of the elliptic curve
        p (int): the modulo of the galois field
        debug (bool, optional): debugging. Defaults to False.
        silent (bool, optional): no printing. Default to True.

    Returns:
        (int,int): new point
    """
    new = p
    factors = get_factors(m)
    l = factors[0] - 1
    del factors[0]
    while l >= 0:
        new = dupe_point(new, dp)
        if l in factors:
            new = add_points(new, p, dp)
        l -= 1
    if not silent:
        ex = exists(new, dp)
        print(f"The point {m}*{p}={new} exists: {ex}")
    return new


def main(start: str, path: str, args: Optional[List[str]] = None) -> None:

    """
    Main entry point
    """
    parser = argparse.ArgumentParser(
        description='Multiply a point on a binary ec: e.g 5*P', prog=f"{start} {path}")
    parser.add_argument('m', type=auto_int, help="amount of multiplications")
    parser.add_argument(
        'r',
        type=auto_int,
        help="r / x component of the point")
    parser.add_argument(
        's',
        type=auto_int,
        help="s / y component of the point")
    parser.add_argument('a', type=auto_int, help="paramter a of the elliptic curve")
    parser.add_argument('b', type=auto_int, help="paramter b of the elliptic curve")
    parser.add_argument('p', type=auto_int, help="the polynomial/defining relation of the galois field")
    arg = parser.parse_args(args)
    mul_point(arg.m, Point(arg.r,arg.s), DomainParams(arg.a,arg.b,arg.p),silent=False)
