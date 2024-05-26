"""Trial division (factorization)"""
import math
import argparse
from typing import Optional, List
from soe import sieve_erastothenes


def test() -> None:
    """
    test against known results
    """
    assert trial_div((2**3) * (3**2) * (7**3)) == [(2,3), (3,2), (7,3)]
    assert trial_div(-1 * (3**2) * (7**3) * (11**3)) == [(-1,1), (3,2), (7,3), (11,3)]
    assert trial_div(1433 * 8677) == [(1433, 1), (8677, 1)]


def trial_div(n: int, silent: bool=True) -> list[tuple[int, int]]:
    """
    Trial division to find prime factors [prime-factorization] +++

    Args:
        n (int): number to factorize

    Returns:
        list[tuple[int,int]]: list of tuples where a**b is (a,b) 
    """
    i, n_old = 0, n
    factors = []
    primes = sieve_erastothenes(math.ceil(math.sqrt(abs(n))))
    if n < 0:
        n *= -1
        factors.append((-1, 1))

    while i < len(primes) and n > 1:
        p = primes[i]
        if n % p == 0:
            ai = 0
            while n % p == 0:
                n //= p
                ai += 1
            factors.append((p, ai))
        i += 1
    if n > 1:
        factors.append((n, 1))

    tmp = 1
    e = f"{n_old}="
    for item in factors:
        tmp *= item[0] ** item[1]
        e += f"{item[0]}^{item[1]}*"
    e = e[:-1]
    if n_old == tmp:
        if not silent:
            print(e)
        return factors
    raise RuntimeError(f"Error: {n_old} != {tmp}")


def main(start: str, path: str, args: Optional[List[str]] = None) -> None:

    """
    Main entry point
    """
    parser = argparse.ArgumentParser(
        description='Trial division', prog=f"{start} {path}")
    parser.add_argument(
        'prime',
        type=int,
        help="prime number")
    arg = parser.parse_args(args)
    trial_div(arg.prime, silent=False)

