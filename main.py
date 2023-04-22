import utils
import time


if __name__ == '__main__':
    print(f"Current protocol params: {utils.GLOBAL_context.protocol_param}")
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
    utils.print_utxos_from_address("addr_test1wpc4h2fygpcuu7degsta7v03pcq2c8zr6g6v8s7f8c7hanqqzeur2")
    # execute transaction between input and output addresses
    # transaction_cbor = utils.simple_send_transaction(input_address, output_address, send_amount=100_000_000)
    # time.sleep(10)
    # print(f"Transaction evaluation: \n{utils.GLOBAL_context.evaluate_tx(transaction_cbor)}")

    # script transaction fee 199909 lovelace

    # input_address: addr_test1vrpttmc34s5lm2eljpyhecyqclyt08k7up2d2ng0043c6vgjqvxx6, contains
    # 7926.661944
    # ADA
    # output_address: addr_test1vp2zv2s7vfxeherqhylvtaeul02hjxqluymjffjqlcdre3cptc9sd, contains
    # 11928.937094
    # ADA)
