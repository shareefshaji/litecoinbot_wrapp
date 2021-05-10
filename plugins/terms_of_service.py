#!/usr/bin/python3.8
from pyrogram import Client, filters
from pyrogram.errors import UserDeactivatedBan, YouBlockedUser, PeerIdInvalid
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta
from data import *
import requests
import time
from colorama import Fore, init
import sys
import re
import os

init(autoreset=True)


def terms_of_service(phone):
    app = Client(
        session_name=phone,
        api_id=get_api_id(phone),
        api_hash=get_api_hash(phone),
        app_version=get_app_version(phone),
        device_model=get_device_model(phone),
        system_version=get_system_version(phone),
        lang_code='en',
        workdir=f'{path}/session/')
    scheduler = AsyncIOScheduler()
    scheduler.start()

    @scheduler.scheduled_job('interval', seconds=100, start_date=f'{datetime.now() + timedelta(seconds=3)}')
    def user_init():
        try:
            print(Fore.BLUE + f"{phone}: {app.get_me()['first_name']} entered Telegram")
        except Exception as exc:
            print(Fore.RED + f'{exc}')
            time.sleep(3)
            print(Fore.BLUE + f"{phone}: {app.get_me()['first_name']} entered Telegram")
        try:
            app.send_message(741849360, '💰 Balance')
        except YouBlockedUser:
            app.unblock_user(741849360)
            app.send_message(741849360, '💰 Balance')
        except PeerIdInvalid:
            app.send_message('Litecoin_click_bot', '/start XPTMA')
            app.send_message(741849360, '💰 Balance')
        except Exception as exc:
            print(Fore.RED + f'{exc}')
            sys.exit()

    @app.on_message(filters.chat(741849360) & filters.regex('you must agree to our Terms of Service'))
    def bot_wrapper(client, message):
        headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                 'Chrome/90.0.4430.93 Safari/537.36'}
        url = re.findall(r'http[s]?://dogeclick.com/terms/\w+', f'{str(message)}')[0]
        requests.get(url, headers=headers)
        url = re.findall(r'http[s]?://dogeclick.com/privacy/\w+', f'{str(message)}')[0]
        requests.get(url, headers=headers)
        time.sleep(3)
        message.click(2)
        app.send_message(741849360, '💰 Balance')

    @app.on_message(filters.chat(741849360) & filters.regex('Available balance:'))
    def bot_wrapper(client, message):
        _balance = float(re.findall(r'Available balance: (.*) LTC', message["text"])[0])
        print(Fore.GREEN + f'{message["text"]}')
        sys.exit()

    try:
        app.run()
    except UserDeactivatedBan as error:
        print(Fore.RED + f'{phone}: {error.MESSAGE}')
        account_delete(phone)
        os.replace(f'{path}/session/{phone}.session',
                   f'{path}/banned/{phone}.session')
        os.replace(f'{path}/json/{phone}.json',
                   f'{path}/banned/{phone}.json')
        sys.exit()
