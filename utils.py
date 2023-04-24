import os
import pycardano
from blockfrost import ApiUrls
from pycardano import (
    PaymentSigningKey,
    BlockFrostChainContext,
    PaymentVerificationKey,
    Transaction,
    TransactionBody,
    TransactionBuilder,
    TransactionInput,
    TransactionOutput,
    TransactionWitnessSet,
    VerificationKeyWitness,
    PlutusData,
    Address,
    PlutusV2Script,
    plutus_script_hash
)
from opshin.prelude import *
import pathlib

# set network
GLOBAL_network = pycardano.Network.TESTNET
# API Key for my Google Account on Blockfrost.io
GLOBAL_context = BlockFrostChainContext("previeweD6696Lpx1kz0cLHF7UanRvb6plg0uXf", base_url=ApiUrls.preview.value)


def generate_and_save_keys(signing_key_path="./keys/payment.skey", verification_key_path="./keys/payment.vkey"):
    payment_signing_key = pycardano.PaymentSigningKey.generate()
    payment_signing_key.save(signing_key_path)
    payment_verification_key = pycardano.PaymentVerificationKey.from_signing_key(payment_signing_key)
    payment_verification_key.save(verification_key_path)

    return payment_signing_key, payment_verification_key


def load_keys_and_address(signing_key_path="./keys/giver/payment.skey",
                          verification_key_path="./keys/giver/payment.vkey"):
    payment_signing_key = pycardano.PaymentSigningKey.load(signing_key_path)
    payment_verification_key = pycardano.PaymentVerificationKey.load(verification_key_path)
    payment_address = pycardano.Address(payment_part=payment_verification_key.hash(), network=GLOBAL_network)
    print(f'Loaded address: {payment_address}')
    return payment_signing_key, payment_verification_key, payment_address


def create_address():
    payment_signing_key = pycardano.PaymentSigningKey.generate()
    payment_signing_key.save("./keys/payment.skey")
    payment_verification_key = pycardano.PaymentVerificationKey.from_signing_key(payment_signing_key)
    payment_verification_key.save("./keys/payment.vkey")

    address = Address(payment_part=payment_verification_key.hash(), network=GLOBAL_network)
    print(f'Created address: {address}')


def create_script_and_address(cbor_file="./smart_contracts/gift_contract/build/gift/script.cbor"):
    with open(cbor_file, "r") as f:
        script_hex = f.read()
    script = PlutusV2Script(bytes.fromhex(script_hex))
    script_hash = plutus_script_hash(script)
    script_address = Address(payment_part=script_hash, payment_credential=None, network=GLOBAL_network)

    return script, script_address


def get_script_address_and_script(script_path="./build/sum_validator/"):
    script_path = pathlib.Path(script_path)
    # Load script info
    with open(os.path.join(script_path, 'testnet.addr')) as f:
        script_address = pycardano.Address.from_primitive(f.read())
    with open(os.path.join(script_path, "script.cbor")) as f:
        script_hex = f.read()
        script = PlutusV2Script(bytes.fromhex(script_hex))
    return script, script_address


def get_script_address_and_script_2(script_path="./build/sum_validator/"):
    script_path = os.path.join(script_path, "script.cbor")
    with open(script_path) as f:
        cbor_hex = f.read()

    cbor = bytes.fromhex(cbor_hex)

    script = PlutusV2Script(cbor)
    script_hash = plutus_script_hash(script)
    script_address = Address(script_hash, staking_credential=None)
    return script, script_address


def get_address(signing_key_path="./keys/payment.skey", verification_key_path="./keys/payment.vkey"):
    _, payment_verification_key, _ = load_keys_and_address(signing_key_path=signing_key_path,
                                                           verification_key_path=verification_key_path)
    network = pycardano.Network.TESTNET
    address = pycardano.Address(payment_part=payment_verification_key.hash(), network=network)

    return address


def calc_ada_from_lovelace(amount_lovelace):
    return float(amount_lovelace)/1000000


def get_lovelace_amount_from_address(address):
    # get utxos for address
    utxos = GLOBAL_context.utxos(str(address))

    # loop over all utxos and add the quantity of lovelace together
    amount_lovelace = 0
    for utxo in utxos:
        amount_lovelace += utxo.output.amount.coin

    return amount_lovelace


def address_ada_quantity(input_address):
    return calc_ada_from_lovelace(get_lovelace_amount_from_address(input_address))


def check_for_non_nft_utxo_at_address(taker_address: Address):
    non_nft_utxo = None
    for utxo in GLOBAL_context.utxos(str(taker_address)):
        if not utxo.output.amount.multi_asset:
            non_nft_utxo = utxo
            break
    return non_nft_utxo


def print_utxos_from_address(address):
    if not GLOBAL_context.utxos(str(address)):
        print(f"Address: {str(address)} has no UTXOs.")
        return
    print(f"Following UTXOs sit at the address: {str(address)}:\n")
    for i, utxo in enumerate(GLOBAL_context.utxos(str(address))):
        print(f"{i}: {utxo}")


def simple_send_transaction(input_address, output_address, send_amount=100_000_000):
    input_sk, input_vk, _ = load_keys_and_address(signing_key_path="./keys/giver/payment.skey",
                                                  verification_key_path="./keys/giver/payment.vkey")
    # get all utxos of input_address
    utxos = GLOBAL_context.utxos(str(input_address))

    # init transaction
    builder = TransactionBuilder(GLOBAL_context)
    # add input address as transaction input
    builder.add_input_address(address=input_address)
    builder.add_output(TransactionOutput.from_primitive([str(output_address), send_amount]))
    # ttl = time to live
    # TTL = slot + N slots. Where N is the amount of slots you want to
    # add to give the transaction a window to be included in a block.
    # max slot in epoch(5days) = 432_000
    # builder.ttl = 23235963
    # builder.reference_inputs.add(utxos[0])

    signed_tx = builder.build_and_sign(signing_keys=[input_sk], change_address=input_address)
    print(f'signed tx_id: {signed_tx.id}')
    # calc transaction fee
    transaction_fee = pycardano.fee(GLOBAL_context, len(signed_tx.to_cbor("bytes")))
    print(f"The minimum transaction fee is: {calc_ada_from_lovelace(transaction_fee)} ADA")
    # submit transaction on the chain
    transaction_hash = GLOBAL_context.submit_tx(signed_tx.to_cbor())
    print(f'Submitted transaction: {transaction_hash} successfully.')

    return signed_tx.to_cbor()


def add_funds_and_datum_to_contract(script_address, giver_address, giver_skey, datum, amount):
    # build transaction for sending funds and datum to script address
    builder = pycardano.TransactionBuilder(context=GLOBAL_context)
    # add giver address as transaction input
    builder.add_input_address(giver_address)

    # add gift_script as transaction output
    builder.add_output(pycardano.TransactionOutput(script_address,
                                                   amount,
                                                   datum=datum,
                                                   datum_hash=pycardano.datum_hash(datum)))
    # sign the script transaction by giver
    signed_tx = builder.build_and_sign([giver_skey], change_address=giver_address)
    # submit transaction
    GLOBAL_context.submit_tx(signed_tx.to_cbor())
    transaction_fee = pycardano.fee(GLOBAL_context, len(signed_tx.to_cbor("bytes")))
    print(f"Send {amount} lovelace to {script_address} successfully.")
    print(f"The transaction fee was: {transaction_fee} lovelace.")
    print(f"Cardanoscan: https://preview.cexplorer.io/tx/{signed_tx.id}")


