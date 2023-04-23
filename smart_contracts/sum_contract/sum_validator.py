from opshin.prelude import *


def validator(datum: int, redeemer: int, context: ScriptContext) -> None:
    
    assert datum + redeemer == 42, "Sum of datum and redeemer is not 42."
