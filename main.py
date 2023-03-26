import utils


if __name__ == '__main__':
    # if no key files exists in folder ./keys yet, create them
    # utils.create_address()

    # print the address of keys in ./keys folder
    testnet_address = utils.get_address()
    utils.get_address_utxos(testnet_address)
