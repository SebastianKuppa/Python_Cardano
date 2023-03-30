import utils


if __name__ == '__main__':
    # utils.generate_and_save_keys(signing_key_path="./keys/taker/payment.skey",
    #                              verification_key_path="./keys/taker/payment.vkey")
    # if no key files exists in folder ./keys yet, create them
    # utils.create_address()

    # print the address of keys in ./keys folder
    testnet_address = utils.get_address(signing_key_path="./keys/taker/payment.skey",
                                        verification_key_path="./keys/taker/payment.vkey")
    print(testnet_address)
    # amount_lovelaces = utils.get_lovelace_amount_from_address(testnet_address)
    # utils.build_transaction(testnet_address)
    utils.datum_to_cbor()
