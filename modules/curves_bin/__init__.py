"""binary EC classes"""
from dataclasses import dataclass

def test() -> None:
    """
    test against known results
    """
    assert DomainParams(1,0,0xb).defines_ec() is False
    assert DomainParams(0x5, 0x1, 0xb).defines_ec() is True

@dataclass(slots=True)
class DomainParams:
    """Domain Parameters of an binary elliptic curve"""
    a: int
    b: int
    rel: int

    def defines_ec(self) -> bool:
        """
        check if the given domain parameters define an ec
        """
        if self.b == 0 or self.rel < 2:
            return False
        return True
    
@dataclass(slots=True)
class Point:
    """Point tuple"""
    r: int
    s: int

    def get_pol(self, cord: int) -> str:
        """
        pretty print polynomials
        """
        tmp = ""
        if cord == -1:
            return "infinity"
        bcord = bin(cord)[2:]
        for i, char in enumerate(bcord):
            if char == "1":
                match (len(bcord)-i-1):
                    case 0:
                        tmp += "1 + "
                    case 1:
                        tmp += "x + "
                    case _:
                        tmp += f"x^{len(bcord)-i-1} + "
        return tmp[:-3]

    def __str__(self) -> str:
        return f"({self.get_pol(self.r)}, {self.get_pol(self.s)})"
    