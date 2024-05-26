"""Get the order of a Point on a binary ec"""
import argparse
from typing import Optional, List
from curves_bin.paam import mul_point
from curves_bin.pexists import exists
from curves_bin import Point, DomainParams
from __helper import auto_int


def test() -> None:
    """
    test against known results
    """
    assert find_ord(Point(0x3, 0x2), DomainParams(0x5, 0x1, 0xb)) == 7
    assert find_ord(Point(0x3, 0x5), DomainParams(0x7, 0x1, 0xb)) == 7
    assert find_ord(Point(0x7, 0x7), DomainParams(0x1, 0x1, 0xb)) == 7


def find_ord(p: Point, dp: DomainParams, ret_points: bool=False, silent: bool=True) -> int|list[Point]:
    """
    Get the order of a point[ecc-point-char2]+++

    Args:
        r (int): r / x coordinate
        s (int): s / y coordinate
        a (int): parameter a of the elliptic curve
        b (int): parameter b of the elliptic curve
        p (int): defining relation
        points (bool): output / return points
        silent (bool, optional): print. Defaults to True.

    Returns:
        int|set: either the order or all points
    """    
    all_points = []
    i = 1
    while True:
        tmp = mul_point(i, p, dp)
        if exists(tmp, dp):
            all_points.append(tmp)
        if tmp.r == tmp.s == -1:
            if not silent:
                print(f"ord(P)={i}")
                if ret_points:
                    print(all_points)
            if ret_points:
                return all_points
            return i
        i += 1


def main(start: str, path: str, args: Optional[List[str]] = None) -> None:

    """
    Main entry point
    """
    parser = argparse.ArgumentParser(
        description='Get the order of an point on a binary ec', prog=f"{start} {path}")
    parser.add_argument('r', type=int, help="r / x component of the point")
    parser.add_argument('s', type=int, help="s / y component of the point")
    parser.add_argument('a', type=auto_int, help="paramter a of the elliptic curve")
    parser.add_argument('b', type=auto_int, help="paramter b of the elliptic curve")
    parser.add_argument('p', type=auto_int, help="the polynomial/defining relation of the galois field")
    parser.add_argument('-a', action='store_true', help="get points back")
    arg = parser.parse_args(args)
    find_ord(Point(arg.r, arg.s), DomainParams(arg.a, arg.b, arg.p), arg.a, silent=False)