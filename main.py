from pycardano import Address, Network, PaymentSigningKey, PaymentVerificationKey

payment_signing_key = PaymentSigningKey.generate()
payment_signing_key.save("payment.skey")
payment_verification_key = PaymentVerificationKey.from_signing_key(payment_signing_key)
payment_verification_key.save("payment.vkey")

network = Network.TESTNET
address = Address(payment_part=payment_verification_key.hash(), network=network)
print(address)