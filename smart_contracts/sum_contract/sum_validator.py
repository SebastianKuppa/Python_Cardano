from opshin.prelude import *


def validator(datum: int, redeemer: Redeemer, context: ScriptContext) -> None:
    
    assert datum + redeemer.data == 42, "Sum of datum and redeemer is not 42."
