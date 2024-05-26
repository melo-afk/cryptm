"""Montgomery ladder (pow)"""
import argparse
from typing import Optional, List


def test() -> None:
    """
    test against known results
    """
    assert montgomery_ladder(17, 19, 23) == 5
    assert montgomery_ladder(-7, 21, 23) == 13
    assert montgomery_ladder(7, 2021, 1051) == 663
    assert montgomery_ladder(953, 2211, 4799) == 2620


def montgomery_ladder(base: int, power: int, mod: int, debug: bool=False, latex: bool=False) -> int:
    """
    Montgommery ladder to calculate: base**power % mod [high-power-modulo] +++

    Args:
        base (int): the base
        power (int): amount of tests
        mod (int): amount of tests
        debug (bool, optional): debug printing. Default to False.
        latex (bool, optional): printing latex friendly. Default to False.

    Returns:
        int: result
    """
    x, y = 1, base
    power_bin = bin(power)[2:]
    i = len(power_bin)
    if debug:
        if latex:
            print(f"y_{{{i}}}&= {y} &x_{{{i}}}&= {x} &i&= {i}")  # latex friendly
        else:
            print(f"y{i}: {y} x{i}: {x} i: {i}")
    while i > 0:
        if int(power_bin[:1]) == 1:
            x = (y * x) % mod
            y = (y**2) % mod
        else:
            y = (y * x) % mod
            x = (x**2) % mod
        power_bin = power_bin[1:]  # cut the first bit away
        i -= 1
        if debug:
            if latex:
                print(f"y_{{{i}}}&= {y} &x_{{{i}}}&= {x} &i&= {i}")
            else:
                print(f"y{i}: {y} x{i}: {x} i: {i}")
    return x


def main(start: str, path: str, args: Optional[List[str]] = None) -> None:

    """
    Main entry point
    """
    parser = argparse.ArgumentParser(
        description='Montgomery ladder', prog=f"{start} {path}")
    parser.add_argument('base', type=int, help="base")
    parser.add_argument('power', type=int, help="power")
    parser.add_argument('mod', type=int, help="modulo")
    parser.add_argument('-d', action='store_true', help="debug logging")
    arg = parser.parse_args(args)
    print(montgomery_ladder(arg.base, arg.power, arg.mod, arg.d))


if __name__ == "__main__":
    print(montgomery_ladder(953, 2211, 4799))
