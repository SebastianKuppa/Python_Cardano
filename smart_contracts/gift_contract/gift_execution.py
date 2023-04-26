import pathlib
import pycardano

from smart_contracts.gift_contract import gift_validator
import utils


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


def taker_takes_gift(gift_script, gift_script_address, datum, redeemer, taker_address, taker_skey, taker_vkey, giver_address):
    # utxo to spend in order to activate the gift script on chain
    utxo_to_spend = utils.GLOBAL_context.utxos(str(gift_script_address))[-1]
    # init transaction
    redeem_gift_transaction = utils.TransactionBuilder(utils.GLOBAL_context)
    # add smart contract as transaction input
    redeem_gift_transaction.add_script_input(utxo_to_spend, gift_script, datum=datum, redeemer=redeemer)
    # get non_nft utxo from take address in order to provide the transaction collateral
    non_nft_utxo = utils.check_for_non_nft_utxo_at_address(taker_address)
    # add collateral to address
    redeem_gift_transaction.collaterals.append(non_nft_utxo)
    # add taker as required signer
    redeem_gift_transaction.required_signers = [taker_vkey.hash()]

    # add taker_address as transaction output
    take_output = pycardano.TransactionOutput(taker_address, 1_000_000)
    # redeem_gift_transaction.add_output(take_output)

    # sign transaction with taker payment_key
    signed_tx = redeem_gift_transaction.build_and_sign([taker_skey], taker_address)
    # submit transaction on-chain
    utils.GLOBAL_context.submit_tx(signed_tx.to_cbor())
    print("Transaction was signed and submitted.")
    print(f"Cardanoscan: https://preview.cexplorer.io/tx/{signed_tx.id}")


if __name__ == "__main__":
    # load giver addresses
    giver_skey_abs_path = pathlib.Path("keys/giver/payment.skey").absolute()
    giver_vkey_abs_path = pathlib.Path("keys/giver/payment.vkey").absolute()
    giver_skey, giver_vkey, giver_addr = utils.load_keys_and_address(signing_key_path=giver_skey_abs_path,
                                                                     verification_key_path=giver_vkey_abs_path)
    # load receiver addresses
    giver_skey_abs_path = pathlib.Path("keys/taker/payment.skey").absolute()
    giver_vkey_abs_path = pathlib.Path("keys/taker/payment.vkey").absolute()
    taker_skey, taker_vkey, taker_addr = utils.load_keys_and_address(signing_key_path="/home/sk/PycharmProjects/Python_Cardano/keys/taker/payment.skey",
                                                                     verification_key_path="/home/sk/PycharmProjects/Python_Cardano/keys/taker/payment.vkey")

    # init datum
    datum = gift_validator.CancelDatum(taker_vkey.hash().to_primitive())
    datum_hash = pycardano.datum_hash(datum)
    # create an empty redeemer, because it needs to be passed to the script transaction, but it has no
    # needed information for the script
    redeemer = pycardano.Redeemer(0)
    # redeemer = pycardano.Redeemer(data=PlutusData(), tag=pycardano.RedeemerTag.SPEND)

    # create smart contract address
    gift_script, gift_script_address = utils.get_script_address_and_script("/home/sk/PycharmProjects/Python_Cardano/smart_contracts/gift_contract/build/gift_validator/script.cbor")
    # add funds to gift script
    # add_funds_to_gift_contract(gift_script_address, giver_addr, giver_skey, datum_hash, amount=6_000_000)
    # retrieve funds from gift script
    taker_takes_gift(gift_script, gift_script_address, datum, redeemer, taker_addr, taker_skey, taker_vkey, giver_addr)
