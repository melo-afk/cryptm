"""Babystep giantstep discrete log finder"""
import argparse
from typing import Optional, List
import math
from mtm import montgomery_ladder


def test() -> None:
    """
    test against known results
    """
    assert babygiantstep(3,5,7) == 5
    assert babygiantstep(2,35,101) == 33
    assert babygiantstep(5,38,103) == 22
    assert babygiantstep(10,38,313) == 70


def babygiantstep(g:int, a: int, p: int, silent: bool=True) -> int:
    """
    Babystep GIANTSTEP discrete logarithm finder [dlog]+++

    Args:
        g (int): generator
        a (int): the result
        p (int): mod
        silent (bool, optional): no printing. Defaults to True.
    
    Returns:
        int: _description_
    """
    if a > p:
        a %= p
    m = math.ceil(math.sqrt(p-1))
    b = {}
    for i in range(m):
        b[(g**i) % p] = i
    mm = p - m - 1
    tmp = montgomery_ladder(g, mm, p)
    for i in range(m):
        x = (a * montgomery_ladder(tmp, i, p)) % p 
        if x in b.keys():
            if not silent:
                print(f"the power is: n={(i * m + b[x]) % p}")
            return (i * m + b[x]) % p
    return 0


def main(start: str, path: str, args: Optional[List[str]] = None) -> None:

    """
    Main entry point
    """
    parser = argparse.ArgumentParser(
        description=' Babystep giantstep dlog finder', prog=f"{start} {path}")
    parser.add_argument('gen', type=int, help="generator")
    parser.add_argument('res', type=int, help="the target")
    parser.add_argument('mod', type=int, help="prime modulo")
    arg = parser.parse_args(args)
    babygiantstep(arg.gen, arg.res, arg.mod, silent=False)
