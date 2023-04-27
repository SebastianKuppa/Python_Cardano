import utils
import identity_validator

import pycardano
import pathlib


if __name__ == '__main__':
    giver_skey_abs_path = pathlib.Path("keys/giver/payment.skey").absolute()
    giver_vkey_abs_path = pathlib.Path("keys/giver/payment.vkey").absolute()
    giver_skey, giver_vkey, giver_addr = utils.load_keys_and_address(signing_key_path=giver_skey_abs_path,
                                                                     verification_key_path=giver_vkey_abs_path)
    # load receiver addresses
    giver_skey_abs_path = pathlib.Path("keys/taker/payment.skey").absolute()
    giver_vkey_abs_path = pathlib.Path("keys/taker/payment.vkey").absolute()
    taker_skey, taker_vkey, taker_addr = utils.load_keys_and_address(
        signing_key_path="/home/sk/PycharmProjects/Python_Cardano/keys/taker/payment.skey",
        verification_key_path="/home/sk/PycharmProjects/Python_Cardano/keys/taker/payment.vkey")

    # init datum
    datum = identity_validator.IdentityDatum("Bob", "Mueller", 22)
    datum_hash = pycardano.datum_hash(datum)
    # create an empty redeemer, because it needs to be passed to the script transaction, but it has no
    # needed information for the script
    redeemer = pycardano.Redeemer(0)
    # redeemer = pycardano.Redeemer(data=PlutusData(), tag=pycardano.RedeemerTag.SPEND)

    # create smart contract address
    script, script_address = utils.get_script_address_and_script(
        "/home/sk/PycharmProjects/Python_Cardano/smart_contracts/identity_spend_contract/build/identity_validator/script.cbor")

    utils.add_funds_and_datum_to_contract(script_address, giver_addr, giver_skey, datum, amount=1_000_000)
