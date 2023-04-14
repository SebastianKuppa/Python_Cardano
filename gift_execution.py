import gift
import pycardano
from opshin.prelude import *
from pycardano import PlutusV2Script, plutus_script_hash, Network, Address

import utils


GLOBAL_network = Network.TESTNET


def create_script_address(cbor_file="./build/gift/script.cbor"):
    with open(cbor_file, "r") as f:
        script_hex = f.read()
    script = PlutusV2Script(bytes.fromhex(script_hex))
    script_hash = plutus_script_hash(script)
    script_address = Address(script_hash, network=GLOBAL_network)

    return script, script_address


def add_funds_to_gift_contract(gift_script_address, giver_address, giver_skey, datum):
    # build transaction for sending funds and datum to script address
    builder = pycardano.TransactionBuilder(context=utils.GLOBAL_context)
    # add giver address as transaction input
    builder.add_input_address(giver_address)

    # add gift_script as transaction output
    builder.add_output(pycardano.TransactionOutput(gift_script_address,
                                                   5_000_000,
                                                   datum_hash=pycardano.datum_hash(datum)))
    # sign the script transaction by giver
    signed_tx = builder.build_and_sign([giver_skey], change_address=giver_address)
    # submit transaction
    # utils.GLOBAL_context.submit_tx(signed_tx.to_cbor())


def taker_takes_gift(gift_script, gift_script_address, taker_address, datum, redeemer):
    # utxo to spend in order to activate the gift script on chain
    utxo_to_spend = utils.GLOBAL_context.utxos(str(gift_script_address))[0]
    # init transaction
    redeem_gift_transaction = utils.TransactionBuilder(utils.GLOBAL_context)
    redeem_gift_transaction.add_script_input(utxo_to_spend, gift_script, datum, redeemer)
    take_output = pycardano.TransactionOutput(taker_address, 25123456)
    redeem_gift_transaction.add_output(take_output)


if __name__ == "__main__":
    # load giver and receiver addresses
    giver_skey = pycardano.PaymentSigningKey.load("./keys/giver/payment.skey")
    giver_vkey = pycardano.PaymentVerificationKey.load("./keys/giver/payment.vkey")
    giver_address = Address(giver_vkey.hash(), network=utils.GLOBAL_network)

    taker_skey = pycardano.PaymentSigningKey.load("./keys/taker/payment.skey")
    taker_vkey = pycardano.PaymentVerificationKey.load("./keys/taker/payment.vkey")
    taker_address = Address(taker_vkey.hash(), network=utils.GLOBAL_network)

    # init datum
    datum = gift.CancelDatum(taker_vkey.hash().to_primitive())
    # create an empty redeemer, because it needs to be passed to the script transaction, but it has no
    # needed information for the script
    redeemer = pycardano.Redeemer(data=PlutusData(), tag=pycardano.RedeemerTag.SPEND)

    # create smart contract address
    gift_script, gift_script_address = create_script_address()
    # add funds to gift script
    add_funds_to_gift_contract(gift_script_address, giver_address, giver_skey, datum)
    # retrieve funds from gift script
    taker_takes_gift(gift_script, gift_script_address, taker_address, datum, redeemer)
