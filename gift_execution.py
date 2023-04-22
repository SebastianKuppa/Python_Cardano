from smart_contracts.gift_contract import gift
import pycardano
from opshin.prelude import *
from pycardano import PlutusV2Script, plutus_script_hash, Address

import utils


def create_script_and_address(cbor_file="./smart_contracts/gift_contract/build/gift/script.cbor"):
    with open(cbor_file, "r") as f:
        script_hex = f.read()
    script = PlutusV2Script(bytes.fromhex(script_hex))
    script_hash = plutus_script_hash(script)
    script_address = Address(script_hash, network=utils.GLOBAL_network)

    return script, script_address


def add_funds_to_gift_contract(gift_script_address, giver_address, giver_skey, datum_hash, amount):
    # build transaction for sending funds and datum to script address
    builder = pycardano.TransactionBuilder(context=utils.GLOBAL_context)
    # add giver address as transaction input
    builder.add_input_address(giver_address)

    # add gift_script as transaction output
    builder.add_output(pycardano.TransactionOutput(gift_script_address,
                                                   amount,
                                                   datum_hash=datum_hash))
    # sign the script transaction by giver
    signed_tx = builder.build_and_sign([giver_skey], change_address=giver_address)
    # addr_test1wqnl9utp25gfheqgsn5x4s9evfv0mjv8cdq7e57aandfllgyw9cnk
    # submit transaction
    utils.GLOBAL_context.submit_tx(signed_tx.to_cbor())
    transaction_fee = pycardano.fee(utils.GLOBAL_context, len(signed_tx.to_cbor("bytes")))
    print(f"Added {amount} lovelace to {gift_script_address} successfully.")
    print(f"The transaction fee was: {transaction_fee}")


def taker_takes_gift(gift_script, gift_script_address, datum, redeemer, taker_address, taker_skey, taker_vkey):
    # utxo to spend in order to activate the gift script on chain
    utxo_to_spend = utils.GLOBAL_context.utxos(str(gift_script_address))[-1]
    # init transaction
    redeem_gift_transaction = utils.TransactionBuilder(utils.GLOBAL_context)
    # add smart contract as transaction input
    redeem_gift_transaction.add_script_input(utxo_to_spend, gift_script, datum, redeemer)

    # get non_nft utxo from take address in order to provide the transaction collateral
    non_nft_utxo = utils.check_for_non_nft_utxo_at_address(taker_address)
    # add colleteral to address
    redeem_gift_transaction.collaterals.append(non_nft_utxo)
    # add taker as required signer
    redeem_gift_transaction.required_signers = [taker_vkey.hash()]
    transaction_fee = redeem_gift_transaction.fee
    # add taker_address as transaction output
    take_output = pycardano.TransactionOutput(taker_address, 2_000_000)
    redeem_gift_transaction.add_output(take_output)
    # sign transaction with taker payment_key
    signed_tx = redeem_gift_transaction.build_and_sign([taker_skey], taker_address)
    # submit transaction on-chain
    utils.GLOBAL_context.submit_tx(signed_tx.to_cbor())


if __name__ == "__main__":
    # load giver addresses
    giver_skey, giver_vkey, giver_addr = utils.load_keys_and_address(signing_key_path="./keys/giver/payment.skey",
                                                                     verification_key_path="./keys/giver/payment.vkey")
    # load receiver addresses
    taker_skey, taker_vkey, taker_addr = utils.load_keys_and_address(signing_key_path="./keys/taker/payment.skey",
                                                                     verification_key_path="./keys/taker/payment.vkey")

    # init datum
    datum = gift.CancelDatum(taker_vkey.hash().to_primitive())
    datum_hash = pycardano.datum_hash(datum)
    # create an empty redeemer, because it needs to be passed to the script transaction, but it has no
    # needed information for the script
    redeemer = pycardano.Redeemer(data=PlutusData(), tag=pycardano.RedeemerTag.SPEND)

    # create smart contract address
    gift_script, gift_script_address = create_script_and_address()
    # add funds to gift script
    add_funds_to_gift_contract(gift_script_address, giver_addr, giver_skey, datum_hash, amount=6_000_000)
    # retrieve funds from gift script
    # taker_takes_gift(gift_script, gift_script_address, datum, redeemer, taker_addr, taker_skey, taker_vkey)
