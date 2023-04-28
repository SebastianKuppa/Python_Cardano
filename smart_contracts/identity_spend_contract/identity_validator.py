from opshin.prelude import *


@dataclass
class IdentityDatum(PlutusData):
    first_name: bytes
    family_name: bytes
    age: int


@dataclass
class IdentityRedeemer(PlutusData):
    first_name: bytes
    family_name: bytes
    age: int


def validator(datum: IdentityDatum, redeemer: IdentityRedeemer, script: ScriptContext) -> None:
    assert datum.first_name == redeemer.first_name and \
           datum.family_name == redeemer.family_name and \
           datum.age == redeemer.age, "Wrong identity."
