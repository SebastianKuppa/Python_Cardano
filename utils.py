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
    PlutusData
)
from opshin.prelude import *

GLOBAL_network = pycardano.Network.TESTNET
# API Key for my Google Account on Blockfrost.io
GLOBAL_context = BlockFrostChainContext("previeweD6696Lpx1kz0cLHF7UanRvb6plg0uXf", base_url=ApiUrls.preview.value)


def generate_and_save_keys(signing_key_path="./keys/payment.skey", verification_key_path="./keys/payment.vkey"):
    payment_signing_key = pycardano.PaymentSigningKey.generate()
    payment_signing_key.save(signing_key_path)
    payment_verification_key = pycardano.PaymentVerificationKey.from_signing_key(payment_signing_key)
    payment_verification_key.save(verification_key_path)

    return payment_signing_key, payment_verification_key


def load_keys(signing_key_path="./keys/giver/payment.skey", verification_key_path="./keys/giver/payment.vkey"):
    payment_signing_key = pycardano.PaymentSigningKey.load(signing_key_path)
    payment_verification_key = pycardano.PaymentVerificationKey.load(verification_key_path)

    return payment_signing_key, payment_verification_key


def create_address():
    payment_signing_key = pycardano.PaymentSigningKey.generate()
    payment_signing_key.save("./keys/payment.skey")
    payment_verification_key = pycardano.PaymentVerificationKey.from_signing_key(payment_signing_key)
    payment_verification_key.save("./keys/payment.vkey")

    network = pycardano.Network.TESTNET
    address = pycardano.Address(payment_part=payment_verification_key.hash(), network=network)
    print(f'Created address: {address}')


def get_address(signing_key_path="./keys/payment.skey", verification_key_path="./keys/payment.vkey"):
    _, payment_verification_key = load_keys(signing_key_path=signing_key_path,
                                            verification_key_path=verification_key_path)
    network = pycardano.Network.TESTNET
    address = pycardano.Address(payment_part=payment_verification_key.hash(), network=network)

    return address


def calc_ada_from_lovelace(amount_lovelace):
    return float(amount_lovelace)/1000000


def get_address_utxos(address):
    # get utxos for address
    return GLOBAL_context.api.address_utxos(address)


def get_lovelace_amount_from_address(address):
    # get utxos for address
    utxos = get_address_utxos(address)

    # loop over all utxos and add the quantity of lovelace together
    amount_lovelace = 0
    for utxo in utxos:
        amount_lovelace += int(utxo.amount[0].quantity)
    # print(f"The address: {address} has currently {calc_ada_from_lovelace(amount_lovelace)} ADA ({amount_lovelace} lovelace).")

    return amount_lovelace


def address_ada_quantity(input_address):
    return calc_ada_from_lovelace(get_lovelace_amount_from_address(input_address))


def simple_send_transaction(input_address, output_address, send_amount=100_000_000):
    input_sk, input_vk = load_keys(signing_key_path="./keys/giver/payment.skey",
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
    # tx_to_cbor = signed_tx.to_cbor()
    GLOBAL_context.submit_tx(signed_tx.to_cbor())
    print(f'Submitted transaction successfully.')


@dataclass
class Sample_datum(PlutusData):
    CONSTR_ID = 1
    a: int
    b: bytes
    c: pycardano.IndefiniteList
    d: dict


def datum_to_cbor():
    datum = Sample_datum(123, b"1234", pycardano.IndefiniteList([4, 5, 6]), {1: b"1", 2: b"2"})
    datum_as_cbor = datum.to_cbor()
    print(f"datum as cbor: {datum_as_cbor}")

