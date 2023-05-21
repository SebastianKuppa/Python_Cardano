from blockfrost import ApiUrls
import blockfrost
import pycardano

from keys.api import BLOCKFROST_API
import utils

GLOBAL_context = pycardano.BlockFrostChainContext(BLOCKFROST_API, base_url=ApiUrls.mainnet.value)


if __name__ == '__main__':
    test_address = 'addr1q9lu5yyrwu3uf3v647y78n0jh9c4svvt3acszfttm0dp4ftffc7dx4nw7h7wvg8msu5mdqegf2hnsa5e5z9vzs7ptqfsceeesr'
    test = GLOBAL_context.api.address(test_address, return_type="json")
    script_hash = '71a65ca58a4e9c755fa830173d2a5caed458ac0c73f97db7faae2e7e3b'
    test2 = GLOBAL_context.api.script(script_hash)
    print(f"Current protocol params: {GLOBAL_context.api.blocks_next}")
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
    _, script_address = utils.get_script_address_and_script("./smart_contracts/sum_contract/build/sum_validator/script.cbor")
    utils.print_utxos_from_address(script_address)
    # execute transaction between input and output addresses
    # transaction_cbor = utils.simple_send_transaction(input_address, output_address, send_amount=100_000_000)
    # time.sleep(10)
    # print(f"Transaction evaluation: \n{utils.GLOBAL_context.evaluate_tx(transaction_cbor)}")

    # script transaction fee 199909 lovelace

    # input_address: addr_test1vrpttmc34s5lm2eljpyhecyqclyt08k7up2d2ng0043c6vgjqvxx6, contains
    # 7885.518988
    # 7891.308315
    # ADA
    # output_address: addr_test1vp2zv2s7vfxeherqhylvtaeul02hjxqluymjffjqlcdre3cptc9sd, contains
    # 11966.67244
    # ADA)
