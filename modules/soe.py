""""Sieve of erastothenes (prime-generating)"""
import argparse
from typing import Optional, List


def test() -> None:
    """
    test against known results
    """
    assert sieve_erastothenes(9) == [2, 3, 5, 7]
    assert sieve_erastothenes(100) == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]


def sieve_erastothenes(b: int) -> list[int]:
    """
    Find all primes <= b with the help of the sieve of erastothenes [prime-generation]+++

    Args:
        b (int): the limit

    Returns:
        list[int]: list with primes
    """
    if b < 2:
        raise RuntimeError(f"{b} is too small. Enter only values >= 2")
    nums = [True for _ in range(b + 1)]
    nums[0] = nums[1] = False
    for i in range(2, b + 1):
        if not nums[i]:
            continue
        for j in range(i * i, b + 1):
            if j % i == 0 and j != i:
                nums[j] = False

    primes = [i for i, p in enumerate(nums) if p]
    return primes


def main(start: str, path: str, args: Optional[List[str]] = None) -> None:

    """
    Main entry point
    """
    parser = argparse.ArgumentParser(
        description='Sieve of erastothenes', prog=f"{start} {path}")
    parser.add_argument(
        'limit',
        type=int,
        help="the limit to which pimes should be returned")
    arg = parser.parse_args(args)
    print(sieve_erastothenes(arg.limit))


if __name__ == "__main__":
    print(sieve_erastothenes(100))
