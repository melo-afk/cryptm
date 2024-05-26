"""Duplicate Points on a binary ec"""
import argparse
from typing import Optional, List
from char2.mul import mul
from char2.reduce import reduce
from char2.inv import bruteforce_inverse
from curves_bin import Point, DomainParams
from __helper import auto_int


def test() -> None:
    """
    test against known results
    """
    assert dupe_point(Point(0x3, 0x7), DomainParams(0x2, 0x4, 0xb)) == Point(0x6, 0x7)
    assert dupe_point(Point(0x6, 0x7), DomainParams(0x2, 0x4, 0xb)) == Point(0, 0x2)


def dupe_point(p: Point, dp: DomainParams, silent: bool=True) -> Point:
    """
    Duplicates a point: 2*P = P+P [ecc-point-char2]+++

    Args:
        r (int): r / x component of the point
        s (int): s / y component of the point
        a (int): paramter a of the elliptic curve
        b (int): paramter b of the elliptic curve
        p (int): the modulo of the galois field
        debug (bool, optional): debugging. Defaults to False.
        silent (bool, optional): no printing. Defaults to True.

    Returns:
        tuple[int,int]: new point
    """
    if p.r == p.s == -1 or p.r == 0:
        if not silent:
            print("infinity")
        return Point(-1,-1)


    mr = bruteforce_inverse(p.r, dp.rel)
    mr = mul(p.s, mr, dp.rel)

    m = reduce(mr ^ p.r, dp.rel)

    u = reduce(mul(m, m, dp.rel) ^ m ^ dp.a, dp.rel)
    v = reduce(mul(m, u ^ p.r, dp.rel) ^ u ^ p.s, dp.rel)
    new = Point(u,v)
    if not silent:
        print(f"added point: {new} m: {hex(m)}")
    return new


def main(start: str, path: str, args: Optional[List[str]] = None) -> None:

    """
    Main entry point
    """
    parser = argparse.ArgumentParser(
        description='Duplicate a point on a binary ec: 2*P = P+P', prog=f"{start} {path}")
    parser.add_argument('r', type=int, help="r / x component of the point")
    parser.add_argument('s', type=int, help="s / y component of the point")
    parser.add_argument('a', type=auto_int, help="paramter a of the elliptic curve")
    parser.add_argument('b', type=auto_int, help="paramter b of the elliptic curve")
    parser.add_argument('p', type=auto_int, help="the polynomial/defining relation of the galois field")
    arg = parser.parse_args(args)
    dupe_point(Point(arg.r, arg.s), DomainParams(arg.a, arg.p, arg.p), silent=False)
