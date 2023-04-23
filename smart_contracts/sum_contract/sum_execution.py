import utils
import pathlib


if __name__ == '__main__':
    # load giver addresses
    giver_skey_abs_path = pathlib.Path("keys/giver/payment.skey").absolute()
    giver_vkey_abs_path = pathlib.Path("keys/giver/payment.vkey").absolute()
    giver_skey, giver_vkey, giver_addr = utils.load_keys_and_address(signing_key_path=giver_skey_abs_path,
                                                                     verification_key_path=giver_vkey_abs_path)
    # load receiver addresses
    taker_skey_abs_path = pathlib.Path("keys/taker/payment.skey").absolute()
    taker_vkey_abs_path = pathlib.Path("keys/taker/payment.vkey").absolute()
    taker_skey, taker_vkey, taker_addr = utils.load_keys_and_address(signing_key_path=taker_skey_abs_path,
                                                                     verification_key_path=taker_vkey_abs_path)
