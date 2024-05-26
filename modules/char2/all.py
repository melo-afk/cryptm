"""Get all elements that are defined through the relation/defining polynomial"""
import argparse
from typing import Optional, List
from char2.mul import mul
from __helper import auto_int


def get_all(pol: int, silent: bool=True) -> dict[str, str]:
    """
    Get all Elements in a gf defined by the relation [basic-char2]+++

    Args:
        p (int): defining polynomial

    Returns:
        dict[int: int]: all elements
    """
    all_el = {}
    tmp = 1
    for i in range(1, 2**(pol.bit_length() - 1) + 1):
        tmp = mul(0x2, tmp, pol)
        # all[f"a**{i}"] = hex(tmp)
        all_el[hex(i)] = hex(tmp)
    if not silent:
        for item in all_el.items():
            print(f"{item[0]}: {item[1]}")
    return all_el


def main(start: str, path: str, args: Optional[List[str]] = None) -> None:

    """
    Main entry point
    """
    parser = argparse.ArgumentParser(
        description='Get all elements that are defined through the relation/defining polynomial, usage: cryptm.py curves_rel/mul <polynomial>')
    parser.add_argument('pol', type=auto_int, help="polynomial")
    arg = parser.parse_args(args)
    get_all(arg.pol, silent=False)
