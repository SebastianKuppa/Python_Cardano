import pycardano
from blockfrost import ApiUrls
from pycardano import BlockFrostChainContext

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
    # address = pycardano.Address.from_primitive(address.payment_part)
    # print(f'Address: {address}')
    return address


def get_lovelace_amount_from_address(address):
    context = BlockFrostChainContext("previeweD6696Lpx1kz0cLHF7UanRvb6plg0uXf", base_url=ApiUrls.preview.value)
    utxos = context.api.address_utxos(address)
    amount_lovelace = 0
    for utxo in utxos:
        amount_lovelace += int(utxo.amount[0].quantity)
    return amount_lovelace

