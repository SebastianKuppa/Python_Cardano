import pycardano


def create_address():
    payment_signing_key = pycardano.PaymentSigningKey.generate()
    payment_signing_key.save("./keys/payment.skey")
    payment_verification_key = pycardano.PaymentVerificationKey.from_signing_key(payment_signing_key)
    payment_verification_key.save("./keys/payment.vkey")

    network = pycardano.Network.TESTNET
    address = pycardano.Address(payment_part=payment_verification_key.hash(), network=network)
    print(f'Created address: {address}')


def get_address(signing_key_path="./keys/payment.skey", verification_key_path="./keys/payment.vkey"):
    payment_signing_key = pycardano.PaymentSigningKey.generate()
    payment_signing_key = payment_signing_key.load(signing_key_path)
    payment_verification_key = pycardano.PaymentVerificationKey.from_signing_key(payment_signing_key)
    payment_verification_key = payment_verification_key.load(verification_key_path)

    network = pycardano.Network.TESTNET
    address = pycardano.Address(payment_part=payment_verification_key.hash(), network=network)
    print(f'Address: {address}')

