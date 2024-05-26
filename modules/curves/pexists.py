"""Check if point exists on a prime ec"""
import argparse
from typing import Optional, List
from curves import Point, DomainParams


def test() -> None:
    """
    test against known results
    """
    assert exists(Point(501, 449), DomainParams(1, 679, 1151)) is True
    assert exists(Point(265, 911), DomainParams(1, 679, 1151)) is True
    assert exists(Point(866, 715), DomainParams(1, 679, 1151)) is True
    assert exists(Point(2, 2), DomainParams(1, 679, 1151)) is False


def exists(p: Point, dp: DomainParams, silent: bool=True) -> bool:
    """
    Check if a point exists in the curve [ecc-point]+++

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
    # infinity always exists
    if p.r == p.s == -1:
        return True
    left = (p.s**2) % dp.p
    right = ((p.r**3) + dp.a * p.r + dp.b) % dp.p
    if not silent:
        print(f"exists: {right==left}")
    return right == left


def main(start: str, path: str, args: Optional[List[str]] = None) -> None:

    """
    Main entry point
    """
    parser = argparse.ArgumentParser(
        description='Check if the point exists on a prime ec', prog=f"{start} {path}")
    parser.add_argument('r', type=int, help="r / x component of the point")
    parser.add_argument('s', type=int, help="s / y component of the point")
    parser.add_argument('a', type=int, help="paramter a of the elliptic curve")
    parser.add_argument('b', type=int, help="paramter b of the elliptic curve")
    parser.add_argument('p', type=int, help="the modulo of the galois field")
    arg = parser.parse_args(args)
    exists(Point(arg.r, arg.s), DomainParams(arg.a, arg.b, arg.p), silent=False)
