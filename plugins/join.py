#!/usr/bin/python3.8
from pyrogram import Client, filters
from pyrogram.errors import UserDeactivatedBan, YouBlockedUser, PeerIdInvalid, FloodWait, UsernameNotOccupied
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

global counter, chat_id


def join(phone):
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

        global counter
        counter = 0

        try:
            print(Fore.BLUE + f"{phone}: {app.get_me()['first_name']} joins chats")
        except Exception as exc:
            print(Fore.RED + f'{exc}')
            time.sleep(3)
            print(Fore.BLUE + f"{phone}: {app.get_me()['first_name']} joins chats")
        try:
            app.send_message(741849360, '📣 Join chats')
        except YouBlockedUser:
            app.unblock_user(741849360)
            app.send_message(741849360, '📣 Join chats')
        except PeerIdInvalid:
            app.send_message('Litecoin_click_bot', '/start XPTMA')
            app.send_message(741849360, '📣 Join chats')
        except Exception as exc:
            print(Fore.RED + f'{exc}')
            sys.exit()

    @app.on_message(filters.chat(741849360) & filters.regex('After joining, press the "Joined"'))
    def bot_wrapper(client, message):

        global counter, chat_id

        if counter == 0:
            try:
                url = re.findall(r'http[s]?://doge.click/join/\w+', f'{str(message)}')[0]
            except IndexError:
                print(Fore.RED + 'DDOS on JOIN')
                sys.exit()
            headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                     'Chrome/89.0.4389.90 Safari/537.36'}
            try:
                site = requests.get(url, headers=headers).text
                chat = re.findall(r'Telegram: Contact @(.*)<', site)[0]
                chat_id = app.join_chat(f'{chat}')['id']
                timer = round(time.time())
                chanel_insert(phone, chat_id, timer)
                message.click('✅ Joined')
            except (IndexError, requests.exceptions.Timeout, UsernameNotOccupied):
                message.click('⏩ Skip')
            except FloodWait as exc:
                print(Fore.RED + f'{phone} flood {exc.x} sec!')
                sys.exit()
            except Exception as exc:
                print(f'{exc}')
                message.click('⏩ Skip')

        if counter == 1:
            message.click('✅ Joined')

        if counter == 2:
            counter = 0
            message.click('⏩ Skip')

    @app.on_message(filters.chat(741849360) & filters.regex('You must stay in the'))
    def bot_wrapper(client, message):
        global chat_id
        timer = (int(re.findall(r'(\d+) hour', f'{message["text"]}')[0]) * 3600) + round(time.time())
        chanel_upgrade(phone, chat_id, timer)

    @app.on_message(filters.chat(741849360) & filters.regex('Please press the'))
    def bot_wrapper(client, message):
        global counter
        counter = 0
        app.send_message(741849360, '📣 Join chats')

    @app.on_message(filters.chat(741849360) & filters.regex('Use /join to get a new one'))
    def bot_wrapper(client, message):
        app.send_message(741849360, '/join')

    @app.on_message(filters.chat(741849360) & filters.regex('try rejoining the'))
    def bot_wrapper(client, message):
        global counter
        if counter == 0:
            counter = 1
            app.send_message(741849360, '/join')
        else:
            counter = 2
            app.send_message(741849360, '/join')

    @app.on_message(filters.chat(741849360) & filters.regex('join tasks are'))
    def bot_wrapper(client, message):
        print(Fore.RED + f'{phone}: no JOIN')
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
