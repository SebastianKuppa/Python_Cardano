import pycardano

import utils
import pathlib


def add_funds_to_sum_contract(script_address, giver_address, giver_skey, datum, amount):
    # build transaction for sending funds and datum to script address
    builder = pycardano.TransactionBuilder(context=utils.GLOBAL_context)
    # add giver address as transaction input
    builder.add_input_address(giver_address)

    # add gift_script as transaction output
    builder.add_output(pycardano.TransactionOutput(script_address,
                                                   amount,
                                                   datum=datum))
    # sign the script transaction by giver
    signed_tx = builder.build_and_sign([giver_skey], change_address=giver_address)
    # submit transaction
    utils.GLOBAL_context.submit_tx(signed_tx.to_cbor())
    transaction_fee = pycardano.fee(utils.GLOBAL_context, len(signed_tx.to_cbor("bytes")))
    print(f"Send {amount} lovelace to {script_address} successfully.")
    print(f"The transaction fee was: {transaction_fee} lovelace.")


def taker_takes_gift(script, script_address, datum, redeemer, taker_address, taker_skey, taker_vkey):
    # utxo to spend in order to activate the gift script on chain
    utxo_to_spend = utils.GLOBAL_context.utxos(str(script_address))[-1]
    # init transaction
    transaction = utils.TransactionBuilder(utils.GLOBAL_context)
    # add smart contract as transaction input
    transaction.add_script_input(utxo_to_spend, script, redeemer=redeemer)

    # get non_nft utxo from take address in order to provide the transaction collateral
    non_nft_utxo = utils.check_for_non_nft_utxo_at_address(taker_address)
    # add colleteral to address
    transaction.collaterals.append(non_nft_utxo)

    # we must specify at least the start of the tx valid range in slots
    transaction.validity_start = utils.GLOBAL_context.last_block_slot
    # This specifies the end of tx valid range in slots
    transaction.ttl = transaction.validity_start + 1000

    # add taker as required signer
    # transaction.required_signers = [taker_vkey.hash()]
    # get estimated transaction fee
    min_transaction_fee = transaction._estimate_fee()
    # add taker_address as transaction output
    # take_output = pycardano.TransactionOutput(taker_address, amount=1_000_000)
    # transaction.add_output(take_output)

    # sign transaction with taker payment_key
    signed_tx = transaction.build_and_sign([taker_skey], taker_address)
    # submit transaction on-chain
    utils.GLOBAL_context.submit_tx(signed_tx.to_cbor())
    print(f"Cardanoscan: https://preview.cexplorer.io/tx/{signed_tx.id}")


if __name__ == '__main__':
    # load giver addresses
    giver_skey_abs_path = pathlib.Path("../../keys/giver/payment.skey").absolute()
    giver_vkey_abs_path = pathlib.Path("../../keys/giver/payment.vkey").absolute()
    giver_skey, giver_vkey, giver_addr = utils.load_keys_and_address(signing_key_path=giver_skey_abs_path,
                                                                     verification_key_path=giver_vkey_abs_path)
    # load receiver addresses
    taker_skey_abs_path = pathlib.Path("../../keys/taker/payment.skey").absolute()
    taker_vkey_abs_path = pathlib.Path("../../keys/taker/payment.vkey").absolute()
    taker_skey, taker_vkey, taker_addr = utils.load_keys_and_address(signing_key_path=taker_skey_abs_path,
                                                                     verification_key_path=taker_vkey_abs_path)
    # create datum and its hash
    datum = 22

    # create redeeme
    # redeemer = 20
    redeemer = pycardano.Redeemer(data=20)

    # get smart contract address on testnet
    sum_script, sum_script_address = utils.get_script_address_and_script("./build/sum_validator/testnet.addr")


    # send ada with datum to contract
    # utils.add_funds_and_datum_to_contract(sum_script_address, giver_addr, giver_skey, datum, amount=2_000_000)
    # TransactionId(hex='9bcf395364f835a2e22605dc0e46139116c44b47ca4f9b619c205110fd51d7d7')
    # take funds from contract
    taker_takes_gift(sum_script, sum_script_address, datum, redeemer, taker_addr, taker_skey, taker_vkey)

