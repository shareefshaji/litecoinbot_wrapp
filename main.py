#!/usr/bin/python3.8
from multiprocessing import Process
from plugins import *
from utils import *
from data import *
import time
import os

path = os.path.abspath(os.curdir)


while True:
    if __name__ == '__main__':
        update()
        all_time_st = time.time()
        Phones = table_read_row(row='PHONE', table='accounts')
        print(Fore.GREEN + f'ALL ACCOUNT = {len(Phones)}')
        for phone in Phones:
            one_time_st = time.time()
            job_clean = Process(target=cleaner, args=(phone,))
            job_join = Process(target=join, args=(phone,))
            job_balance = Process(target=balance, args=(phone,))
            job_clean.start()
            job_clean.join()
            job_join.start()
            job_join.join()
            job_balance.start()
            job_balance.join()
            one_time_fn = round(time.time() - one_time_st)
            print(Fore.CYAN + f'{phone} end job {one_time_fn} sec!')
        all_time_fn = round(time.time() - all_time_st)
        print(Fore.GREEN + f'{len(Phones)} ACCOUNTS COMPLETE JOBS IN {all_time_fn} sec')
