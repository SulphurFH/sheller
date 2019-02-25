import time
from random import randint


def generate_ts_unique_code(code_type):
    rand_num = randint(0, 99999)
    code = "%01d%d%05d" % (code_type, int(time.time()), rand_num)
    return code
