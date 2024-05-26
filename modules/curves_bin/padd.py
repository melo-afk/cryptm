"""Add two points on a binary ec"""
import argparse
from typing import Optional, List
from char2.mul import mul
from char2.reduce import reduce
from char2.inv import bruteforce_inverse
from curves_bin import Point, DomainParams
from curves_bin.pdupe import dupe_point
from __helper import auto_int

def test() -> None:
    """
    test against known results
    """
    assert add_points(Point(0x3, 0x4), Point(0x6, 0x1), DomainParams(0x2, 0x4, 0xb)) == Point(0x7, 0x7)
    assert add_points(Point(0x3, 0x4), Point(0x2, 0x4), DomainParams(0x3, 0x1, 0xb)) == Point(0x2, 0x6)
    assert add_points(Point(0x2, 0x6), Point(0x7, 0x1), DomainParams(0x3, 0x1, 0xb)) == Point(0x4, 0x1)


def add_points(p1: Point, p2: Point, dp: DomainParams, silent: bool=True) -> Point:
    """
    Add two points: P1+P2 [ecc-point-char2]+++

    Args:
        r1 (int): r / x component of point 1
        s1 (int): s / y component of point 1
        r2 (int): r / x component of point 2
        s2 (int): s / y component of point 2
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
    
    # P + -P or -P + P = infinity
    if p2.r == p1.r and (p2.s == reduce(p1.r ^ p1.s, dp.rel) or p1.s == reduce(p2.r ^ p2.s, dp.rel)):
        return Point(-1, -1)
    
    # P + P = 2P
    if p2.r == p1.r and p2.s == p1.s:
        return dupe_point(p1, dp)


    ms = reduce(p2.s ^ p1.s, dp.rel)
    mr = reduce(p2.r ^ p1.r, dp.rel)
        

    # if mr is
    mr = bruteforce_inverse(mr, dp.rel)
    m = mul(ms, mr, dp.rel)

    u = reduce(mul(m, m, dp.rel) ^ m ^ dp.a ^ p1.r ^ p2.r, dp.rel)
    v = reduce(mul(m, u ^ p1.r, dp.rel) ^ u ^ p1.s, dp.rel)
    new = Point(u,v)
    if not silent:
        print(f"added point: {new} m: {hex(m)}")
    return new


def main(start: str, path: str, args: Optional[List[str]] = None) -> None:

    """
    Main entry point
    """
    parser = argparse.ArgumentParser(
        description='Add two points on a binary ec: P1+P2', prog=f"{start} {path}")
    parser.add_argument('r1', type=int, help="r / x component of the point 1")
    parser.add_argument('s1', type=int, help="s / y component of the point 1")
    parser.add_argument('r2', type=int, help="r / x component of the point 2")
    parser.add_argument('s2', type=int, help="s / y component of the point 2")
    parser.add_argument('a', type=auto_int, help="paramter a of the elliptic curve")
    parser.add_argument('b', type=auto_int, help="paramter b of the elliptic curve")
    parser.add_argument('p', type=auto_int, help="the polynomial/defining relation of the galois field")
    arg = parser.parse_args(args)
    add_points(Point(arg.r1,arg.s1), Point(arg.r2,arg.s2), DomainParams(arg.a, arg.b, arg.p),silent=False)
