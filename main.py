import utils


if __name__ == '__main__':
    # print the address of keys in ./keys folder
    input_address = utils.get_address(signing_key_path="./keys/giver/payment.skey",
                                      verification_key_path="./keys/giver/payment.vkey")
    output_address = utils.get_address(signing_key_path="./keys/taker/payment.skey",
                                       verification_key_path="./keys/taker/payment.vkey")
    print(f"input_address: {input_address}, "
          f"contains {utils.calc_ada_from_lovelace(utils.get_lovelace_amount_from_address(input_address))} ADA")
    print(f"output_address: {output_address}, "
          f"contains {utils.calc_ada_from_lovelace(utils.get_lovelace_amount_from_address(output_address))} ADA)")
    # utils.simple_send_transaction(input_address, output_address)
