"""Get the order of a Point on a prime ec"""
import argparse
from typing import Optional, List
from curves import Point, DomainParams
from curves.paam import mul_point
from curves.pexists import exists


def test() -> None:
    """
    test against known results
    """
    assert ord_point(Point(501, 449), DomainParams(1, 679, 1151)) == 1217
    assert ord_point(Point(265, 911), DomainParams(1, 679, 1151)) == 1217
    assert ord_point(Point(4, 5), DomainParams(7, 11, 13)) == 5
    assert ord_point(Point(-1, -1), DomainParams(7, 11, 13)) == 1


def ord_point(p: Point, dp: DomainParams, ret_points: bool=False, silent: bool=True) -> int|list[Point]:
    """
    Get the order of a point on a char>3 ec [ecc-point]+++

    Args:
        r (int): r / x component of the point
        s (int): s / y component of the point
        a (int): paramter a of the elliptic curve
        b (int): paramter b of the elliptic curve
        p (int): the modulo of the galois field
        ret_points (bool): return all points instead of the order
        silent (bool, optional): no printing. Defaults to True.

    Returns:
        int|list: order of the points or all generated points
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
        description='Get the order of an point on a prime ec', prog=f"{start} {path}")
    parser.add_argument('r', type=int, help="r / x component of the point")
    parser.add_argument('s', type=int, help="s / y component of the point")
    parser.add_argument('a', type=int, help="paramter a of the elliptic curve")
    parser.add_argument('b', type=int, help="paramter b of the elliptic curve")
    parser.add_argument('p', type=int, help="the modulo of the galois field")
    parser.add_argument('-a', action='store_true', help="get points back")
    arg = parser.parse_args(args)
    ord_point(Point(arg.r1, arg.s1), DomainParams(arg.a, arg.b, arg.pol), arg.a, silent=False)