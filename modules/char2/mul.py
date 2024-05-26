"""Multiply and reduce two polynomials with a relation/defining polynomial"""
import argparse
from typing import Optional, List
from __helper import auto_int
from char2.reduce import reduce


def mul(a: int, b: int, pol: int, silent: bool=True) -> int:
    """
    Multiplies two polynomials and reduces the result [basic-char2]+++

    Args:
        a (int): polynomial a
        b (int): polynomial b
        pol (int): polynomial relation used for reduction
        silent (bool): flag to control debug output

    Returns:
        int: reduced polynomial resulting from the multiplication
    """
    result = 0
    while b > 0:
        if b & 1:
            result ^= a
        a <<= 1
        if a.bit_length() > pol.bit_length() - 1:
            a = reduce(a, pol)
        b >>= 1
    
    result = reduce(result, pol)
    
    if not silent:
        print(f"multiplied: {hex(result)}")
    
    return result


def main(start: str, path: str, args: Optional[List[str]] = None) -> None:

    """
    Main entry point
    """
    parser = argparse.ArgumentParser(
        description='Multiply two numbers in a relation (numbers in binary representation), usage: cryptm.py curves_rel/mul <a> <b> <polynomial>')
    parser.add_argument('a', type=auto_int, help="coefficent 1")
    parser.add_argument('b', type=auto_int, help="coefficent 2")
    parser.add_argument('pol', type=auto_int, help="polynomial")
    arg = parser.parse_args(args)
    mul(arg.a, arg.b, arg.pol, silent=False)
