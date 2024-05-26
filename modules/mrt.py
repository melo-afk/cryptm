"""Miller rabin test (prime-test)"""
import random
import argparse
from typing import Optional, List
from gcd import gcd
from mtm import montgomery_ladder


def test() -> None:
    """
    test against known results
    """
    assert miller_rabin_test(1051) is True
    assert miller_rabin_test(1052) is False
    assert miller_rabin_test(31) is True


def miller_rabin_test(p: int, tests: int=10, debug: bool=False, silent: bool=True) -> bool:
    """
    Miller Rabin prime test [prime-test] +++

    Args:
        p (int): the possible prime number to check
        tests (int): amount of tests
        debug (bool, optional): debug printing. Default to False.
        silent (bool, optional): no printing. Default to True.

    Returns:
        bool: likely prime or not
    """
    if tests < 1:
        print("minimum amount of tests is 1")
    # quick pre check of p
    if p % 2 == 0 or p < 2:
        print("not a prime")
        return False
    d = p - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    powers = []
    i = 0

    # adding all powers to a list for calculating later
    while i < s:
        powers.append((2**i) * d)
        i += 1
    for _ in range(tests):
        x = random.randrange(2, p - 1)

        # check the gcd first and continue with the next base if the gcd is not
        # 1
        if gcd(x, p) != 1:
            if debug:
                print(f"failed: gcd({x},{p}) was not 1")
            continue

        # check if a^d mod p is 1 => likely prime
        tempd = montgomery_ladder(x, d, p)
        if tempd == 1:
            if debug:
                print(f"passed: base: {x}, power (d): {d}, remaining: {tempd}")
            continue
        else:
            if debug:
                print(f"failed: base: {x}, power (d): {d}, remaining: {tempd}")
        # calculate the result of x^power mod p for every power with the
        # montgomery ladder
        for power in powers:
            temp = montgomery_ladder(x, power, p)
            if temp == p - 1:
                if debug:
                    print(
                        f"passed: base: {x}, power: {power}, remaining: {temp if temp == 1 else -1}")
                break
            else:
                if debug:
                    print(
                        f"failed: base: {x}, power: {power}, remaining: {temp}")
        else:
            if not silent or debug:
                print(f"{p} is not a prime")
            return False
    if not silent or debug:
        print(f"{p} is prime with a probability of : {100-((1/4)**tests)*100:.8f}%")
    return True


def main(start: str, path: str, args: Optional[List[str]] = None) -> None:

    """
    Main entry point
    """
    parser = argparse.ArgumentParser(
        description='Miller rabin test', prog=f"{start} {path}")
    parser.add_argument('power', type=int, help="power")
    parser.add_argument(
        'tests',
        nargs='?',
        type=int,
        default=10,
        help="amount of tests, default is 10")
    parser.add_argument('-d', action='store_true', help="debug logging")
    arg = parser.parse_args(args)
    miller_rabin_test(arg.power, arg.tests, arg.d, silent=False)


