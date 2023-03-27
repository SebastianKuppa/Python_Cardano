import utils


if __name__ == '__main__':
    # if no key files exists in folder ./keys yet, create them
    # utils.create_address()

    # print the address of keys in ./keys folder
    testnet_address = utils.get_address()
    amount_lovelaces = utils.get_lovelace_amount_from_address(testnet_address)
    utils.build_transaction(testnet_address)
