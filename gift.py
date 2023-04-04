import pycardano
from opshin.prelude import *
from pycardano import PlutusV2Script, plutus_script_hash, Network, Address

import utils


GLOBAL_network = Network.TESTNET


@dataclass()
class CancelDatum(PlutusData):
    pubkeyhash: bytes


def validator(datum: CancelDatum, redeemer: None, context: ScriptContext) -> None:
    sig_present = False
    for s in context.tx_info.signatories:
        if datum.pubkeyhash == s:
            sig_present = True
    assert sig_present


def create_script_address(cbor_file="./build/gift/script.cbor"):
    with open(cbor_file, "r") as f:
        script_hex = f.read()
    gift_script = PlutusV2Script(bytes.fromhex(script_hex))
    script_hash = plutus_script_hash(gift_script)
    script_address = Address(script_hash, network=GLOBAL_network)

    return script_address


if __name__ == "__main__":
    # create smart contract address
    gift_script_address = create_script_address()
    # load giver and receiver addresses
    giver_address = utils.get_address(signing_key_path="./keys/giver/payment.skey",
                                      verification_key_path="./keys/giver/payment.vkey")
    receiver_address = utils.get_address(signing_key_path="./keys/taker/payment.skey",
                                         verification_key_path="./keys/taker/payment.vkey")
    # build transaction
    builder = pycardano.TransactionBuilder(context=utils.GLOBAL_context)
    # add giver address as transaction input
    builder.add_input_address(giver_address)
