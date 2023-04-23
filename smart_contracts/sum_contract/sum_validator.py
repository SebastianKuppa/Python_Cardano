from opshin.prelude import *


def validator(datum: int, redeemer: int, context: Nothing) -> None:
    assert datum + redeemer == 42, "Sum of datum and redeemer is not 42."
