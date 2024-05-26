"""Prime EC classes"""
from dataclasses import dataclass

def test() -> None:
    """
    test against known results
    """
    assert DomainParams(-3, 1, 100).defines_ec() is True
    assert DomainParams(-3, 1, 100).get_discriminant() == 1296
    assert DomainParams(-3, 1, 100).get_invariant() == 144

@dataclass(slots=True)
class DomainParams:
    """Domain Parameters of an prime elliptic curve"""
    a: int
    b: int
    p: int

    def defines_ec(self) -> bool:
        """
        check if the given domain parameters define an ec
        """
        if 4 * self.a**3 + 27* self.b**2 == 0:
            return False
        return True
        
    def get_discriminant(self) -> int:
        """
        get the discriminant of the ec
        """
        return -16 * (4 * self.a**3 + 27* self.b**2)

    def get_invariant(self) -> float:
        """
        get the j invariant of the ec
        """
        return -1728 * ((4 * self.a**3) / self.get_discriminant())

@dataclass(slots=True)
class Point:
    """Point tuple"""
    r: int
    s: int

    def __str__(self) -> str:
        return f"{self.r, self.s}"
