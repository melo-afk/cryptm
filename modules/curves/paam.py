"""Multiply a point on a prime ec"""
import argparse
from typing import Optional, List
from curves import Point, DomainParams
from curves.padd import add_points
from curves.pdupe import dupe_point
from curves.pexists import exists
from sqm import get_factors


def test() -> None:
    """
    test against known results
    """
    assert mul_point(199, Point(501, 449), DomainParams(1, 679, 1151)) == Point(866, 715)
    assert mul_point(211, Point(501, 449), DomainParams(1, 679, 1151)) == Point(265, 911)
    assert mul_point(199, Point(265, 911), DomainParams(1, 679, 1151)) == Point(163, 507)
    assert mul_point(211, Point(866, 715), DomainParams(1, 679, 1151)) == Point(163, 507)


def mul_point(m: int, p: Point, dp: DomainParams, debug: bool=False, silent: bool=True) -> Point:
    """
    Multiply a point with Square and Multiply: e.g 5 * P(r,s) [ecc-point]+++

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
            new = add_points(new, p, dp, debug=debug)
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
        description='Multiply a point on a prime ec: e.g 5*P', prog=f"{start} {path}")
    parser.add_argument('m', type=int, help="amount of multiplications")
    parser.add_argument('r', type=int, help="r / x component of the point")
    parser.add_argument('s', type=int, help="s / y component of the point")
    parser.add_argument('a', type=int, help="paramter a of the elliptic curve")
    parser.add_argument('b', type=int, help="paramter b of the elliptic curve")
    parser.add_argument('p', type=int, help="the modulo of the galois field")
    parser.add_argument('-d', action='store_true', help="debug logging")
    arg = parser.parse_args(args)
    mul_point(arg.m,Point(arg.r,arg.s), DomainParams(arg.a,arg.b,arg.p),arg.d,silent=False)
