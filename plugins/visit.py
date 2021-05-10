#!/usr/bin/python3.8
from pyrogram import Client, filters
from pyrogram.errors import UserDeactivatedBan, YouBlockedUser, PeerIdInvalid
from pyrogram.session import Session
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta
from data import *
#import undetected_chromedriver as uc
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
            print(Fore.BLUE + f"{phone}: {app.get_me()['first_name']} joins chats")
        except Exception as exc:
            print(Fore.RED + f'{exc}')
            time.sleep(3)
            print(Fore.BLUE + f"{phone}: {app.get_me()['first_name']} joins chats")
        try:
            app.send_message(741849360, '🖥 Visit sites')
        except YouBlockedUser:
            app.unblock_user(741849360)
            app.send_message(741849360, '🖥 Visit sites')
        except PeerIdInvalid:
            app.send_message('Litecoin_click_bot', '/start XPTMA')
            app.send_message(741849360, '🖥 Visit sites')
        except Exception as exc:
            print(Fore.RED + f'{exc}')
            sys.exit()

    @app.on_message(filters.chat(741849360) & filters.regex('Press the "Visit website" button'))
    def bot_wrapper(client, message):
        try:
            url = re.findall(r'http[s]?://doge.click/visit/\w+', f'{str(message)}')[0]
            options = uc.ChromeOptions()
            options.add_argument("--start-maximized")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-extensions")
            options.headless = True
            options.add_argument("--headless")
            options.add_argument(f"--user-data-dir={os.path.abspath(os.curdir)}/data/browser")
            options.add_argument(
                "--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/89.0.4389.90 Safari/537.36")
            chrome = uc.Chrome(options=options)
            chrome.implicitly_wait(15)
            chrome.get(url)
        except IndexError:
            print(Fore.RED + 'DDOS on VISIT')
            message.click('⏩ Skip')
            sys.exit()
        except:
            message.click('⏩ Skip')
        try:
            timer = chrome.find_element_by_id('headbar')
            t_wait = int(timer.get_attribute("data-timer"))
            print(Fore.RED + f'TIMER {t_wait}')
            time.sleep(t_wait + 5)
        except:
            pass

    @app.on_message(filters.chat(741849360) & filters.regex('click tasks are'))
    def bot_wrapper(client, message):
        print(Fore.RED + f'{phone}: no CLICK')
        sys.exit()

    @app.on_message(filters.chat(741849360) & filters.regex('for visiting a site!'))
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
