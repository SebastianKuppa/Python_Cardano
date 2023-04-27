from opshin.prelude import *


@dataclass
class IdentityDatum(PlutusData):
    first_name: str
    family_name: str
    age: int


@dataclass
class IdentityRedeemer(PlutusData):
    first_name: str
    family_name: str
    age: int


def validator(datum: IdentityDatum, redeemer: IdentityRedeemer, script: ScriptContext) -> None:
    assert datum.first_name == redeemer.first_name and \
           datum.family_name == redeemer.family_name and \
           datum.age == redeemer.age, "Wrong identity."
