"""Add two points on a prime ec"""
import argparse
from typing import Optional, List
from curves import Point, DomainParams
from curves.pexists import exists
from curves.pdupe import dupe_point
from egcd import egcd


def test() -> None:
    """
    test against known results
    """
    assert add_points(Point(1,1), Point(5,3), DomainParams(-3,-10,13)) == Point(4,4)
    assert add_points(Point(5,3), Point(8,6), DomainParams(-3,-10,13)) == Point(1,1)
    assert add_points(Point(4,2), Point(9,12), DomainParams(14,3,17)) == Point(8,7)
    assert add_points(Point(5,11), Point(5,8), DomainParams(10,3,19)) == Point(-1,-1)


def add_points(p1: Point, p2: Point, dp: DomainParams, debug: bool=False, silent: bool=True) -> Point:
    """
    Add two points: P1+P2 [ecc-point]+++

    Args:
        p1.r (int): r / x component of point 1
        p1.s (int): s / y component of point 1
        p2.r (int): r / x component of point 2
        p2.s (int): s / y component of point 2
        a (int): paramter a of the elliptic curve
        b (int): paramter b of the elliptic curve
        p (int): the modulo of the galois field
        debug (bool, optional): _description_. Defaults to False.

    Returns:
        tuple[int,int]: _description_
    """

    # infinity + infinity = infinity
    if p1.r == p2.r == p1.s == p2.s == -1:
        return Point(-1, -1)
    
    # P1 + infinity = P1
    if p2.r == p2.s == -1:
        return Point(p1.r, p1.s)
    
    # infinity + P2 = P2
    if p1.r == p1.s == -1:
        return Point(p2.r, p2.s)
    
    #if p1.r == p2.r and p2.s == p - p1.s:
    if p1.s == dp.p - p2.s and p1.s == 0:
        print("infinity a")
        return Point(-1, -1)
    
    if p1.r == p2.r and p1.s == dp.p - p2.s:
        return Point(-1, -1)
    
    if p1.r == p2.r and p1.s == p2.s:
        return dupe_point(Point(p1.r,p1.s),dp)

    n = (p2.s - p1.s) % dp.p if (p2.s - p1.s) > 0 else dp.p + ((p2.s - p1.s) % dp.p)
    o = (p2.r - p1.r) % dp.p if (p2.r - p1.r) > 0 else dp.p + ((p2.r - p1.r) % dp.p)
    if n % o == 0:
        m = n // o
    else:
        o1 = egcd(dp.p, o % dp.p)
        m = (n * o1) % dp.p
    u = ((m**2) - p1.r - p2.r) % dp.p
    v = (m * (u - p1.r) + p1.s) % dp.p
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
        description='Add two points on a prime ec: P1+P2', prog=f"{start} {path}")
    parser.add_argument('r1', type=int, help="r / x component of point 1")
    parser.add_argument('s1', type=int, help="s / y component of point 1")
    parser.add_argument('r2', type=int, help="r / x component of point 2")
    parser.add_argument('s2', type=int, help="s / y component of point 2")
    parser.add_argument('a', type=int, help="paramter a of the elliptic curve")
    parser.add_argument('b', type=int, help="paramter b of the elliptic curve")
    parser.add_argument('p', type=int, help="the modulo of the galois field")
    parser.add_argument('-d', action='store_true', help="debug logging")
    arg = parser.parse_args(args)
    add_points(Point(arg.r1, arg.s1), Point(arg.r2, arg.s2), DomainParams(arg.a, arg.b, arg.p), arg.d, silent=False)
