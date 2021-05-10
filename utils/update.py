#!/usr/bin/python3.8
import json
import random
from data import *


def update():
    make_tables()
    with open(f'{path}/wallets.txt', 'r') as inf:
        wallets = inf.readlines()
    dirs = os.listdir(f'{path}/update')
    for _dir in dirs:
        if '.json' in _dir:
            with open(f'{path}/update/{_dir}', 'r') as inf:
                db_add = json.load(inf)
                account_insert(
                    phone=db_add['phone'],
                    api_id=db_add['api_id'],
                    api_hash=db_add['api_hash'],
                    app_version=db_add['app_version'],
                    device_model=db_add['device_model'],
                    system_version=db_add['system_version'],
                    wallet=random.choice(wallets)
                )
            os.replace(f'{path}/update/{_dir}', f'{path}/data/{_dir}')
        elif '.session' in _dir:
            os.replace(f'{path}/update/{_dir}', f'{path}/session/{_dir}')
