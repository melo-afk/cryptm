"""Duplicate Points on a prime ec"""
import argparse
from typing import Optional, List
from curves import Point, DomainParams
from curves.pexists import exists
from egcd import egcd


def test() -> None:
    """
    test against known results
    """
    assert dupe_point(Point(1,1), DomainParams(-3,-10,13)) == Point(11,12)
    assert dupe_point(Point(4,2), DomainParams(14,3,17)) == Point(7,11)
    assert dupe_point(Point(9,12), DomainParams(14,3,17)) == Point(14,6)
    assert dupe_point(Point(-1,-1), DomainParams(14,3,17)) == Point(-1,-1)
    assert dupe_point(Point(9,0), DomainParams(14,3,17)) == Point(-1,-1)


def dupe_point(p: Point, dp: DomainParams, debug: bool=False, silent: bool=True) -> Point:
    """
    Duplicate a point: 2*P = P+P [ecc-point]+++

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
    if p.r == p.s == -1 or p.s == 0:
        return Point(-1, -1)


    n = (3 * (p.r**2) + dp.a) % dp.p 
    if n < 0:
        n += dp.p
    if n % (2 * p.s) == 0:
        m = n // (2 * p.s)
    else:
        
        s1 = egcd(dp.p, (2 * p.s) % dp.p)
        #if s1 == 0:
        #    print(n,(2*p.s) % dp.p)
        #    print(dp.p, (2 * p.s) % dp.p)
        m = (n * s1) % dp.p
    u = (m**2 - 2 * p.r) % dp.p
    v = (m * (u - p.r) + p.s) % dp.p
    v = dp.p - v
    new = Point(u,v)
    if debug or not silent:
        e = exists(new, dp)
        print(f"P={new}, m={m}, exists: {e}")
    return new


def main(start: str, path: str, args: Optional[List[str]] = None) -> None:

    """
    Main entry point
    """
    parser = argparse.ArgumentParser(
        description='Duplicate a point on a prime ec: 2*P = P+P', prog=f"{start} {path}")
    parser.add_argument('r', type=int, help="r / x component of the point")
    parser.add_argument('s', type=int, help="s / y component of the point")
    parser.add_argument('a', type=int, help="paramter a of the elliptic curve")
    parser.add_argument('b', type=int, help="paramter b of the elliptic curve")
    parser.add_argument('p', type=int, help="the modulo of the galois field")
    parser.add_argument('-d', action='store_true', help="debug logging")
    arg = parser.parse_args(args)
    dupe_point(Point(arg.r, arg.s), DomainParams(arg.a, arg.b, arg.p), arg.d, silent=False)
