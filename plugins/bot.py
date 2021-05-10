#!/usr/bin/python3.8
from pyrogram import Client, filters
from pyrogram.errors import UserDeactivatedBan, YouBlockedUser, PeerIdInvalid, FloodWait
from pyrogram.session import Session
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta
from data import *
import requests
import time
from colorama import Fore, init
import sys
import re
import os

Session.notice_displayed = True
init(autoreset=True)


def bot(phone):
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
            print(Fore.BLUE + f"{phone}: {app.get_me()['first_name']} enters bot")
        except Exception as exc:
            print(Fore.RED + f'{exc}')
            time.sleep(3)
            print(Fore.BLUE + f"{phone}: {app.get_me()['first_name']} enters bot")
        try:
            app.send_message(741849360, '🤖 Message bots')
        except YouBlockedUser:
            app.unblock_user(741849360)
            app.send_message(741849360, '🤖 Message bots')
        except PeerIdInvalid:
            app.send_message('Litecoin_click_bot', '/start XPTMA')
            app.send_message(741849360, '🤖 Message bots')
        except Exception as exc:
            print(Fore.RED + f'{exc}')
            sys.exit()

    @app.on_message(filters.chat(741849360) & filters.regex('Press the "Message bot" botton'))
    def bot_wrapper(client, message):
        try:
            url = re.findall(r'http[s]?://doge.click/bot/\w+', f'{str(message)}')[0]
        except IndexError:
            print(Fore.RED + 'DDOS on BOT')
            message.click('⏩ Skip')
            sys.exit()
        headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                 'Chrome/89.0.4389.90 Safari/537.36'}
        try:
            site = requests.get(url, headers=headers).text
            _bot = re.findall(r'Telegram: Contact @(.*)<', site)[0]
            bot_init_message = app.send_message(f'{_bot}', '/start')
            bot_id = bot_init_message["chat"]["id"]
            bot_init_message_id = bot_init_message["message_id"]
            time.sleep(10)
            for message_to_forward in app.iter_history(bot_id, limit=1):
                message_to_forward_id = message_to_forward["message_id"]
                if bot_init_message_id != message_to_forward_id:
                    app.forward_messages(741849360, 'me', message_to_forward_id)
                else:
                    message.click('⏩ Skip')
            app.block_user(bot_id)
        except IndexError:
            message.click('⏩ Skip')
        except requests.exceptions.Timeout:
            message.click('⏩ Skip')
        except FloodWait as exc:
            print(Fore.RED + f'{phone} flood {exc.x} sec!')
            sys.exit()
        except Exception as exc:
            print(Fore.RED + f'{exc}')
            message.click('⏩ Skip')
            sys.exit()

    @app.on_message(filters.chat(741849360) & filters.regex('bot tasks are'))
    def bot_wrapper(client, message):
        print(Fore.RED + f'{phone}: no BOT')
        sys.exit()

    @app.on_message(filters.chat(741849360) & filters.regex('for messaging a bot!'))
    def bot_wrapper(client, message):
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
