"""Order of Elements in prime fields"""
import argparse
from typing import Optional, List


def test() -> None:
    """
    test against known results
    """
    assert get_ord(2, 4799) == 2399


def get_ord(element: int, p: int, plus: bool=False, silent: bool=True) -> int:
    """
    Find the order of an element in a prime galois field[basic]+++

    Args:
        element (int): element
        p (int): the prime of the galois field
        plus (bool, optional): switch to + operator. Defaults to False.
        silent (bool, optional): printing. Defaults to True.

    Returns:
        int: the order
    """
    tmp = set()
    for i in range(1,p):
        if not plus:
            tmp.add((element**i) % p)
        else:
            tmp.add((element*i) % p)
    if not silent:
        print(f"ord({element}) = {len(tmp)}")
    return len(tmp)


def get_all_ords(p: int, plus: bool=False, silent: bool=True) -> dict[int, int]:
    """
    Get the order of all elements (either order with '+' or '*')

    Args:
        p (int): the prime of the galois field
        plus (bool, optional): Operation for calculating the order. Defaults to False.
        silent (bool, optional): printing. Defaults to True.

    Returns:
        dict[int, int]: dictionary with element and its order
    """
    all_el = {}
    for i in range(2,p):
        tmp = set()
        for j in range(1,p):
            if not plus:
                tmp.add((i**j) % p)
            else:
                tmp.add((j*i) % p)
        if not silent:
            print(f"ord({i}) = {len(tmp)}")
        all_el[i] = len(tmp)
    return all_el

def main(start: str, path: str, args: Optional[List[str]] = None) -> None:

    """
    Main entry point
    """
    parser = argparse.ArgumentParser(
        description='Get the order of element(s) in a prime field', prog=f"{start} {path}")
    parser.add_argument(
        'prime',
        type=int,
        help="prime of the galois field (>2)")
    parser.add_argument(
        'element',
        type=int,
        nargs='?',
        help="element you want to know the order of")
    parser.add_argument(
        '-a',
        action='store_true',
        help="return all generators")
    parser.add_argument(
        '-p',
        action='store_true',
        help="use the + operator instead of *")
    arg = parser.parse_args(args)
    if arg.a:
        get_all_ords(arg.prime, arg.p, silent=False)
    else:
        get_ord(arg.element, arg.prime, arg.p, silent=False)
