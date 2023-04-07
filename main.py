import utils


if __name__ == '__main__':
    # get address from digital signatures
    input_address = utils.get_address(signing_key_path="./keys/giver/payment.skey",
                                      verification_key_path="./keys/giver/payment.vkey")
    output_address = utils.get_address(signing_key_path="./keys/taker/payment.skey",
                                       verification_key_path="./keys/taker/payment.vkey")
    # calc ada amount from adresses
    input_address_ada_amount = utils.address_ada_quantity(input_address)
    output_address_ada_amount = utils.address_ada_quantity(output_address)
    # print address information
    print(f"input_address: {input_address}, "
          f"contains {input_address_ada_amount} ADA")
    print(f"output_address: {output_address}, "
          f"contains {output_address_ada_amount} ADA)")
    # execute transaction between input and output addresses
    utils.simple_send_transaction(input_address, output_address, send_amount=100_000_000)
