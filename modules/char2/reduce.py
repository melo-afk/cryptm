"""Reduce a polynomial with a relation/defining polynomial"""
import argparse
from typing import Optional, List
from __helper import auto_int


def reduce(a: int, pol: int, silent: bool=True) -> int:
    """
    Reduces a polynomial using the given polynomial relation [basic-char2]+++

    Args:
        a (int): the polynomial that needs to be reduced
        pol (int): polynomial relation used for reduction (e.g., x^8+x^7+x^6+x+1)
        silent (bool): flag to control debug output

    Returns:
        int: reduced polynomial
    """
    while a.bit_length() >= pol.bit_length():
        shift = a.bit_length() - pol.bit_length()
        a ^= pol << shift
    
    if not silent:
        print(f"reduced: {hex(a)}")
    
    return a


def main(start: str, path: str, args: Optional[List[str]] = None) -> None:

    """
    Main entry point
    """
    parser = argparse.ArgumentParser(
        description='Reduce a polynomial with a relation, usage: cryptm.py curves_rel/mul <a> <polynomial>')
    parser.add_argument('a', type=auto_int, help="coefficent 1")
    parser.add_argument('pol', type=auto_int, help="polynomial")
    arg = parser.parse_args(args)
    reduce(arg.a, arg.pol, silent=False)
