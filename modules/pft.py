"""Prime fermat test (prime-test)"""
import argparse
from typing import Optional, List
from mtm import montgomery_ladder

def test() -> None:
    """
    test against known results
    """
    assert prime_fermat_test(1051) is True
    assert prime_fermat_test(1052) is False
    assert prime_fermat_test(31) is True


def prime_fermat_test(p: int, tests: int|None=None, debug: bool=False) -> bool:
    """
    Prime fermat test [prime-test] +++

    Args:
        p (int): the possible prime number to check
        tests (int): amount of tests
        debug (bool): debug printing

    Returns:
        bool: likely prime or not
    """
    # set the boundary of max tests if max is not specfified
    if not tests:
        tests = p - 1
    i = 2
    prime = True
    # check every number from 2 to max-1
    while i < tests:
        a = montgomery_ladder(i, p - 1, p)
        if debug:
            print("base: " + str(i) + ", remaining: " + str(a))
        i += 1
        # => if the result of i^p-1 mod p is not 1, p is not prime, therfore break
        if a != 1:
            prime = False
            break
    if prime is False:

        print(str(p) + " is not a prime")
        return False
    else:
        # because carmichael numbers exist only likely
        print(str(p) + " is likely a prime")
        return True


def main(start: str, path: str, args: Optional[List[str]] = None) -> None:

    """
    Main entry point
    """
    parser = argparse.ArgumentParser(
        description='Prime fermat test', prog=f"{start} {path}")
    parser.add_argument('prime', type=int, help="the prime number to check")
    parser.add_argument(
        'tests',
        nargs='?',
        type=int,
        default=10,
        help="the amount of tests, defaults to 10")
    arg = parser.parse_args(args)
    prime_fermat_test(arg.prime, arg.tests)


if __name__ == "__main__":
    prime_fermat_test(131071, 10)
