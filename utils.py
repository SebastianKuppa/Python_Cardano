import os
import pycardano
import blockfrost
from blockfrost import ApiUrls, api, ApiError
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
from keys.api import BLOCKFROST_API

import cbor2
import pathlib

# set network
GLOBAL_network = pycardano.Network.MAINNET
# API Key for my Google Account on Blockfrost.io
GLOBAL_context = BlockFrostChainContext(BLOCKFROST_API, base_url=ApiUrls.mainnet.value)
api = blockfrost.api.BlockFrostApi(BLOCKFROST_API, base_url=ApiUrls.mainnet.value)


def get_onchain_address(address):
    """Gets the on-chain info for a given address.

        Args:
            address (str): The address to get the on-chain address for.

        Returns:
            str: The on-chain address.
    """
    try:
        address = api.address(
            address=address)
        print(address.type)
        for amount in address.amount:
            print(amount.quantity, amount.unit)

    except ApiError as e:
        print(e)
    return address


def init_check():
    """Checks the health of the Cardano network.

        Returns:
            None
    """
    try:
        health = api.health()
        print(health)  # prints object:    HealthResponse(is_healthy=True)
        health = api.health(return_type='json')  # Can be useful if python wrapper is behind api version
        print(health)  # prints json:      {"is_healthy":True}
        health = api.health(return_type='pandas')
        print(health)  # prints Dataframe:         is_healthy
        #                       0         True

        account_rewards = api.account_rewards(
            stake_address='stake1ux3g2c9dx2nhhehyrezyxpkstartcqmu9hk63qgfkccw5rqttygt7',
            count=20,
        )
        print(account_rewards[0].epoch)  # prints 221
        print(len(account_rewards))  # prints 20

        account_rewards = api.account_rewards(
            stake_address='stake1ux3g2c9dx2nhhehyrezyxpkstartcqmu9hk63qgfkccw5rqttygt7',
            count=20,
            gather_pages=True,  # will collect all pages
        )
        print(account_rewards[0].epoch)  # prints 221
        print(len(account_rewards))  # prints 57

        address = api.address(
            address='addr1qxqs59lphg8g6qndelq8xwqn60ag3aeyfcp33c2kdp46a09re5df3pzwwmyq946axfcejy5n4x0y99wqpgtp2gd0k09qsgy6pz')
        print(address.type)  # prints 'shelley'
        for amount in address.amount:
            print(amount.unit)  # prints 'lovelace'

    except ApiError as e:
        print(e)


def generate_and_save_keys(signing_key_path="./keys/payment.skey", verification_key_path="./keys/payment.vkey"):
    """Generates a new payment signing key and saves it to a file.

        Args:
            signing_key_path (str): The path to the file to save the signing key to.
            verification_key_path (str): The path to the file to save the verification key to.

        Returns:
            tuple(PaymentSigningKey, PaymentVerificationKey): The generated signing key and verification key.
    """
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
    print(f"payment_verification_key.hash(): {payment_verification_key.hash()}")
    print(f'Loaded address: {payment_address}')
    return payment_signing_key, payment_verification_key, payment_address


def create_address():
    payment_signing_key = pycardano.PaymentSigningKey.generate()
    payment_signing_key.save("./keys/payment.skey")
    payment_verification_key = pycardano.PaymentVerificationKey.from_signing_key(payment_signing_key)
    payment_verification_key.save("./keys/payment.vkey")

    address = Address(payment_part=payment_verification_key.hash(), network=GLOBAL_network)
    print(f'Created address: {address}')


def get_script_address_and_script_WIP(script_path="./build/sum_validator/"):
    cbor_path = os.path.join(script_path, "script.cbor")
    with open(cbor_path) as f:
        cbor_hex = f.read()
    cbor = bytes.fromhex(cbor_hex)
    script = PlutusV2Script(cbor)
    print(f"script_hash: {plutus_script_hash(script)}")
    # script_hash: 60372aaf3c2482849de960d716252d2f0ea779a5d6aed549f5e5768b
    script_hash = plutus_script_hash(script)
    # script = PlutusV2Script(cbor2.loads(bytes.fromhex(GLOBAL_context.api.script_cbor(script_hash).cbor)))
    script = PlutusV2Script(bytes.fromhex(GLOBAL_context.api.script_cbor(script_hash=script_hash).cbor))
    script_address = pycardano.Address(script_hash, network=GLOBAL_network)

    return script, script_address


def get_script_address_and_script(script_path):
    print(f"reading cbor file from {script_path}")
    with open(script_path) as f:
        script_hex = f.read()
    script = PlutusV2Script(bytes.fromhex(script_hex))
    script_hash = plutus_script_hash(script)
    print(f"Created script with script_hash: {script_hash}")
    script_address = pycardano.Address(script_hash, network=pycardano.Network.TESTNET)
    print(f"Script address: {script_address}")

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
                                                   datum_hash=pycardano.datum_hash(datum)))
    # sign the script transaction by giver
    signed_tx = builder.build_and_sign([giver_skey], change_address=giver_address)
    # submit transaction
    GLOBAL_context.submit_tx(signed_tx.to_cbor())
    transaction_fee = pycardano.fee(GLOBAL_context, len(signed_tx.to_cbor("bytes")))
    print(f"Send {amount} lovelace to {script_address} successfully.")
    print(f"The transaction fee was: {transaction_fee} lovelace.")
    print(f"Cardanoscan: https://preview.cexplorer.io/tx/{signed_tx.id}")


