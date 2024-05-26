"""Discrete log finder through bruteforce"""
import argparse
from typing import Optional, List


def test() -> None:
    """
    test against known results
    """
    assert dlog(3,5,7) == 5
    assert dlog(2,35,101) == 33
    assert dlog(5,38,103) == 22
    assert dlog(10,38,313) == 70


def dlog(g: int, res: int, p: int) -> int:
    """
    Finds the discrete log: g^x\\equiv res (mod p)[dlog]+++

    Args:
        g (int): the used generator of the galois field
        res (int): the target result
        p (int): the modulo (prime)

    Returns:
        int: power
    """
    for i in range(1, p):
        if (g**i) % p == res:
            print(f"{res}: power {i}")
            return i
    return 0


def main(start: str, path: str, args: Optional[List[str]] = None) -> None:

    """
    Main entry point
    """
    parser = argparse.ArgumentParser(
        description='Discrete log finder', prog=f"{start} {path}")
    parser.add_argument('gen', type=int, help="generator")
    parser.add_argument('res', type=int, help="the target")
    parser.add_argument('mod', type=int, help="prime modulo")
    arg = parser.parse_args(args)
    dlog(arg.gen, arg.res, arg.mod)
