import utils
import identity_validator

import pycardano
import pathlib


def add_funds_to_gift_contract(script_address, giver_address, giver_skey, datum_hash, amount):
    # build transaction for sending funds and datum to script address
    builder = pycardano.TransactionBuilder(context=utils.GLOBAL_context)
    # add giver address as transaction input
    builder.add_input_address(giver_address)

    # add gift_script as transaction output
    builder.add_output(pycardano.TransactionOutput(script_address,
                                                   amount,
                                                   datum_hash=datum_hash))
    # sign the script transaction by giver
    signed_tx = builder.build_and_sign([giver_skey], change_address=giver_address)
    # submit transaction
    utils.GLOBAL_context.submit_tx(signed_tx.to_cbor())
    transaction_fee = pycardano.fee(utils.GLOBAL_context, len(signed_tx.to_cbor("bytes")))
    print(f"Send {amount} lovelace to {script_address} successfully.")
    print(f"The transaction fee was: {transaction_fee} lovelace.")
    print(f"Cardanoscan: https://preview.cexplorer.io/tx/{signed_tx.id}")


if __name__ == '__main__':
    giver_skey_abs_path = pathlib.Path("../../keys/giver/payment.skey").absolute()
    giver_vkey_abs_path = pathlib.Path("../../keys/giver/payment.vkey").absolute()
    giver_skey, giver_vkey, giver_addr = utils.load_keys_and_address(signing_key_path=giver_skey_abs_path,
                                                                     verification_key_path=giver_vkey_abs_path)
    # load receiver addresses
    giver_skey_abs_path = pathlib.Path("../../keys/taker/payment.skey").absolute()
    giver_vkey_abs_path = pathlib.Path("../../keys/taker/payment.vkey").absolute()
    taker_skey, taker_vkey, taker_addr = utils.load_keys_and_address(
        signing_key_path="/home/sk/PycharmProjects/Python_Cardano/keys/taker/payment.skey",
        verification_key_path="/home/sk/PycharmProjects/Python_Cardano/keys/taker/payment.vkey")

    # init datum
    datum = identity_validator.IdentityDatum(b"Bob", b"Mueller", 22)
    datum_hash = pycardano.datum_hash(datum)
    # create an empty redeemer, because it needs to be passed to the script transaction, but it has no
    # needed information for the script
    redeemer = pycardano.Redeemer(0)
    # redeemer = pycardano.Redeemer(data=PlutusData(), tag=pycardano.RedeemerTag.SPEND)

    # create smart contract address
    script, script_address = utils.get_script_address_and_script(
        "/home/sk/PycharmProjects/Python_Cardano/smart_contracts/identity_spend_contract/build/identity_validator/script.cbor")

    # utils.add_funds_and_datum_to_contract(script_address, giver_addr, giver_skey, datum, amount=1_000_000)
    add_funds_to_gift_contract(script_address, giver_addr, giver_skey, datum_hash, amount=1_000_000)
