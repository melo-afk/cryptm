""""Sqare finder in prime Fields"""
import argparse
from typing import Optional, List
from mtm import montgomery_ladder


def test() -> None:
    """
    test against known results
    """
    assert qsqrt(3,23) == [16,7]
    assert qsqrt(5,29) == [18,11]
    assert qsqrt(1,11) == [1,10]
    assert qsqrt(3,11) == [5,6]
    assert qsqrt(4,11) == [9,2]
    assert qsqrt(5,11) == [4,7]
    assert qsqrt(9,11) == [3,8]
    assert qsqrt(5,23) == 0
    assert qsqrt(2,29) == 0
    assert get_all_squares(11) == {1: [1,10], 3: [5,6], 4: [9,2], 5: [4,7], 9: [3,8]}


def find_lt(p: int) -> tuple[int,int]:
    """
    Needed for: (p-1)/2 = 2**l * t (t must be odd)

    Args:
        p (int): the prime of the galois field

    Returns:
        tuple[int, int]: calculated l, t
    """
    l, t = 0, 1
    while True:
        if (2**l) * t == p and t % 2 != 0:
            return l, t
        elif (2**l) * t > p:
            # increment the power and reset t
            t = 1
            l += 1
        t += 1


def find_non_square(p: int) -> int:
    """
    Finds a non square in a prime field

    Args:
        p (int): the prime of the galois field

    Returns:
        int: The non square
    """
    a = 2
    while True:
        print(a,p)
        if qsqrt(a, p, _skip=True) == 0:
            return a
        elif a > p:
            return 0
        a += 1


def qsqrt(base: int, mod: int, debug: bool=False, silent: bool=True, _skip: bool=False) -> list[int]|int:
    """
    Find sqares of the base modulo the mod [root-finder] +++

    Args:
        base (int): squares
        mod (int): start value of b
        debug (bool): debug printing
        silent (bool, optional): no printing. Default to True.
        _skip (bool): needed for finding non squares (=> only the result of the montgomery ladder is checked)

    Returns:
        list[int]: list of prime factors
    """
    if base > mod and debug:
        print(
            f"the square {base} is larger than the power {mod}. Please enter valid numbers.")
        return 0
    c = montgomery_ladder(base, int((mod - 1) / 2), mod)
    if c == 1:
        if _skip:
            return 1
        if (mod + 1) % 4 != 0:
            l, t = find_lt((mod - 1) // 2)
            b0 = find_non_square(mod)
            b = b0**int((mod - 1) / 2)
            n = 0
            for i in range(l):
                c = montgomery_ladder(
                    base, 2**(l - (i + 1)) * t, mod) * montgomery_ladder(b, n, mod)
                c %= mod
                if c == 1:
                    n = int((n / 2))
                else:
                    n = int((n / 2) + (mod - 1) / 4)

            w = montgomery_ladder(base, int((t + 1) / 2),
                                  mod) * montgomery_ladder(b0, n, mod)
            w %= mod

            # print(w, power-w)
            if debug or not silent:
                print(f"{base} is a square with the roots {w} and {mod-w}")
            return [w, mod - w]
        else:
            w = montgomery_ladder(base, int((mod + 1) / 4), mod)
            if debug or not silent:
                print(f"{base} is a square with the roots {w} and {mod-w}")
            return [w, mod - w]
    else:
        if debug or not silent:
            print(f"{base} is not a square (result was {c} and not 1)")
        return 0


def get_all_squares(p: int, silent: bool=True) -> dict[int, list[int]]:
    """
    Get all squares of a prime field
    Args:
        p (int): the prime

    Returns:
        dict[int:list[int,int]]: Dictionary of 
    """
    all_sq = {}
    for i in range(1, p):
        tmp = qsqrt(i, p, False)
        if isinstance(tmp, list):
            all_sq[i] = tmp
    if not silent:
        for key, item in all_sq.items():
            print(f"sqare: {key}, roots: {item[0],item[1]}")
    return all_sq


def main(start: str, path: str, args: Optional[List[str]] = None) -> None:

    """
    Main entry point
    """
    parser = argparse.ArgumentParser(
        description='Square root finder in a prime field', prog=f"{start} {path}")
    parser.add_argument('square', type=int, help="square")
    parser.add_argument('power', nargs='?', type=int, help="power")
    parser.add_argument('-a', action='store_true', help="find all squares")
    arg = parser.parse_args(args)
    if arg.a:
        get_all_squares(arg.power)
    if not arg.square:
        parser.print_help()
        return
    qsqrt(arg.square, arg.power, silent=False)

