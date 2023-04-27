import pycardano
import pathlib
from blockfrost import ApiUrls

import utils
from keys.api import BLOCKFROST_API


# set network
GLOBAL_network = pycardano.Network.TESTNET
# API Key for my Google Account on Blockfrost.io
GLOBAL_context = pycardano.BlockFrostChainContext(BLOCKFROST_API,
                                                  base_url=ApiUrls.preview.value)
# ogmios_context = pycardano.OgmiosChainContext(ws_url=, network=pycardano.Network.TESTNET)


def add_funds_to_sum_contract(script_address, giver_address, giver_skey, datum, amount):
    # build transaction for sending funds and datum to script address
    builder = pycardano.TransactionBuilder(context=GLOBAL_context)
    # add giver address as transaction input
    builder.add_input_address(giver_address)

    # add gift_script as transaction output
    builder.add_output(pycardano.TransactionOutput(script_address,
                                                   amount,
                                                   datum=datum))
    # sign the script transaction by giver
    signed_tx = builder.build_and_sign([giver_skey], change_address=giver_address)
    # submit transaction
    GLOBAL_context.submit_tx(signed_tx.to_cbor())
    transaction_fee = pycardano.fee(GLOBAL_context, len(signed_tx.to_cbor("bytes")))
    print(f"Send {amount} lovelace to {script_address} successfully.")
    print(f"The transaction fee was: {transaction_fee} lovelace.")


def taker_takes_gift(script, script_address, datum, redeemer, taker_address, taker_skey, taker_vkey):
    # utxo to spend in order to activate the gift script on chain
    utxo_to_spend = GLOBAL_context.utxos(str(script_address))[-1]
    test = utxo_to_spend.output.datum_hash
    # init transaction
    transaction = utils.TransactionBuilder(GLOBAL_context)
    # add smart contract as transaction input
    transaction.add_script_input(utxo=utxo_to_spend, script=script, datum=datum, redeemer=redeemer)
    # get non_nft utxo from take address in order to provide the transaction collateral
    non_nft_utxo = utils.check_for_non_nft_utxo_at_address(taker_address)
    # add colleteral to address
    transaction.collaterals.append(non_nft_utxo)
    # add taker as required signer
    transaction.required_signers = [taker_vkey.hash()]

    # add taker_address as transaction output
    # take_output = pycardano.TransactionOutput(taker_address, amount=1_000_000)
    # transaction.add_output(take_output)

    # sign transaction with taker payment_key
    signed_tx = transaction.build_and_sign([taker_skey], taker_address)
    # submit transaction on-chain
    GLOBAL_context.submit_tx(signed_tx.to_cbor())
    print("Transaction was signed and submitted.")
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
    # create datum
    datum = 22
    # create redeemer
    redeemer = pycardano.Redeemer(data=20)

    # get smart contract address on testnet
    sum_script, sum_script_address = utils.get_script_address_and_script("./build/sum_validator/script.cbor")

    # send funds with datum to contract
    utils.add_funds_and_datum_to_contract(sum_script_address, giver_addr, giver_skey, datum, amount=2_000_000)

    # take funds with redeemer from contract
    # taker_takes_gift(sum_script, sum_script_address, datum, redeemer, taker_addr, taker_skey, taker_vkey)
