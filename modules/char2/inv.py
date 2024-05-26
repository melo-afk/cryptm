"""Bruteforce the inverse element"""
import argparse
from typing import Optional, List
from char2.mul import mul
from char2.reduce import reduce
from __helper import auto_int


def bruteforce_inverse(a: int, pol: int, silent: bool=True) -> int:
    """
    Bruteforce the inverse of an element [basic-char2]+++

    Args:
        a (int): element to inverse
        pol (int): polynomial

    Returns:
        int: inversed element
    """
    if a > pol:
        a = reduce(a, pol)
    for i in range(1, 2**(pol.bit_length())+1):
        
        tmp = mul(a, i, pol)
        if tmp == 1:
            if not silent:
                print(f"found inverse: {hex(i)}")
            return i
    return -1


def main(start: str, path: str, args: Optional[List[str]] = None) -> None:

    """
    Main entry point
    """
    parser = argparse.ArgumentParser(
        description='Multiply two numbers in a relation (numbers in binary representation), usage: cryptm.py curves_rel/mul <a> <b> <polynomial>')
    parser.add_argument('a', type=auto_int, help="coefficent 1")
    parser.add_argument('pol', type=auto_int, help="polynomial")
    arg = parser.parse_args(args)
    bruteforce_inverse(arg.a, arg.pol, silent=False)
