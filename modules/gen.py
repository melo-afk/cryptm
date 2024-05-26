"""Finding generator(s) in prime fields"""
import argparse
from typing import Optional, List


def test() -> None:
    """
    test against known results
    """
    assert find_gen(23) == 5
    assert find_gen(23, allgen=True) == [5,7,10,11,14,15,17,19,20,21]


def find_gen(p: int, allgen: bool=False) -> int|list[int]:
    """
    Find the smallest generator / all generators [basic]+++

    Args:
        p (int): the prime number of the galois field
        allgen (bool, optional): return all generators. Defaults to False.
    """
    if p <= 2:
        print("values <= 2 are not supported")
        return -1
    gen = []
    for i in range(2, p):
        tmp = []
        for j in range(1, p):
            if (i**j) % p in tmp:
                break
            tmp.append((i**j) % p)
        else:
            gen.append(i)
            if not allgen:
                print(f"generator: {i}")
                return i
    print(f"all generators: {gen}")
    return gen


def main(start: str, path: str, args: Optional[List[str]] = None) -> None:

    """
    Main entry point
    """
    parser = argparse.ArgumentParser(
        description='Generator finder in prime fields', prog=f"{start} {path}")
    parser.add_argument(
        'prime',
        type=int,
        help="prime of the galois field (>2)")
    parser.add_argument(
        '-a',
        action='store_true',
        help="return all generators")
    arg = parser.parse_args(args)
    find_gen(arg.prime, arg.a)
