"""P minus one method (factorization)"""
import argparse
from typing import Optional, List
from mtm import montgomery_ladder
from gcd import gcd


def test() -> None:
    """
    test against known results
    """
    assert p_minus1(1241143) == [547, 2269]
    assert p_minus1(-1241143) == [-547, 2269]
    assert p_minus1(10460353204) == [7, 1494336172]


def calc_k(b: int, debug: bool=False) -> int:
    """
    returns the prime powers of b as a product
    """
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
    resl = []
    res = 1
    for prime in primes:
        power = 1
        while True:
            if prime**power > b:

                # for cases when the prime itself is larger  than b => prevents
                # resl from filling up with 1s
                if power > 1:
                    resl.append(prime**(power - 1))
                    res *= prime**(power - 1)
                break
            power += 1
    if debug:
        print(f"the prime factors are: {resl}")
    return res


def p_minus1(n: int, b: int=3, debug: bool=False) -> list[int]:
    """
    P minus 1 method  [prime-factorization] +++

    Args:
        p (int): the prime
        b (int): start value of b
        debug (bool): debug printing

    Returns:
        list[int]: list of prime factors
    """
    a = 2
    if debug:
        print(f"Starting parameters: n: {n}, b: {b}, a: {a}")
    neg = False
    if n < 0:
        neg = True
        n *= -1
    while True:
        # find the prime powers of b first (and get the product of them)
        k = calc_k(b, debug)

        # perform a^k mod n and subtract 1, handle also results that are 0
        amod = montgomery_ladder(a, k, n)
        amod = amod - 1 if amod > 0 else n - 1
        # calculate the gcd between amod and n
        g = gcd(amod, n)

        # increment a or b, or print the dividor depending on the gcd
        # result
        if g == 1:
            b += 1
        elif g == n:
            a += 1
        else:
            print(f"found a dividor: {g}, cofactor: {int(n/g)}, b: {b}")
            return [g, (int(n / g))] if neg is False else [-1 * g, (int(n / g))]
        if debug:
            print(f"current a: {a}, b:{b}, gcd: {g}")


def main(start: str, path: str, args: Optional[List[str]] = None) -> None:

    """
    Main entry point
    """
    parser = argparse.ArgumentParser(
        description='P minus 1 method', prog=f"{start} {path}")
    parser.add_argument('num1', type=int, help="power")
    parser.add_argument(
        'b',
        nargs='?',
        type=int,
        default=3,
        help="starting value for b, defaults to 3")
    parser.add_argument('-d', action='store_true', help="debug logging")
    arg = parser.parse_args(args)
    p_minus1(arg.num1, arg.b, arg.d)


if __name__ == "__main__":
    p_minus1(275237, 13, debug=True)
    p_minus1(275237, 13, True)
