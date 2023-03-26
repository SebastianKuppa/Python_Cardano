import pycardano
from blockfrost import ApiUrls
from pycardano import (
    PaymentSigningKey,
    BlockFrostChainContext,
    PaymentVerificationKey,
    Transaction,
    TransactionBody,
    TransactionInput,
    TransactionOutput,
    TransactionWitnessSet,
    VerificationKeyWitness,
)

GLOBAL_network = pycardano.Network.TESTNET


def generate_and_save_keys(signing_key_path="./keys/payment.skey", verification_key_path="./keys/payment.vkey"):
    payment_signing_key = pycardano.PaymentSigningKey.generate()
    payment_signing_key = payment_signing_key.save(signing_key_path)
    payment_verification_key = pycardano.PaymentVerificationKey.from_signing_key(payment_signing_key)
    payment_verification_key = payment_verification_key.save(verification_key_path)

    return payment_signing_key, payment_verification_key


def load_keys(signing_key_path="./keys/payment.skey", verification_key_path="./keys/payment.vkey"):
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
    # API Key for my Google Account on Blockfrost.io
    context = BlockFrostChainContext("previeweD6696Lpx1kz0cLHF7UanRvb6plg0uXf", base_url=ApiUrls.preview.value)
    # get utxos for address
    return context.api.address_utxos(address)


def get_lovelace_amount_from_address(address):
    # get utxos for address
    utxos = get_address_utxos(address)

    # loop over all utxos and add the quantity of lovelace together
    amount_lovelace = 0
    for utxo in utxos:
        amount_lovelace += int(utxo.amount[0].quantity)
    print(f"The address: {address} has currently {calc_ada_from_lovelace(amount_lovelace)} ADA ({amount_lovelace} lovelace).")

    return amount_lovelace


def raw_transaction(address):
    # get utxos for address
    utxos = get_address_utxos(address)
    tx_id = utxos[0].tx_hash
    tx_in = TransactionInput.from_primitive([tx_id, 0])
    output1 = TransactionOutput.from_primitive([address, 100000000000])
    output2 = TransactionOutput.from_primitive([address, 799999834103])
    print('test')
