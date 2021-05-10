#!/usr/bin/python3.8
import sys
import time
from pyrogram import Client
from pyrogram.errors import UserDeactivatedBan, FloodWait, ChannelInvalid, ChannelPrivate, UserNotParticipant
from data import *
from colorama import Fore, init

init(autoreset=True)


def cleaner(phone):
    app = Client(
        session_name=phone,
        api_id=get_api_id(phone),
        api_hash=get_api_hash(phone),
        app_version=get_app_version(phone),
        device_model=get_device_model(phone),
        system_version=get_system_version(phone),
        lang_code='en',
        workdir=f'{path}/session/')

    try:
        app.start()
        print(Fore.BLUE + f"{phone}: {app.get_me()['first_name']} cleans chats")
    except UserDeactivatedBan as error:
        print(Fore.RED + f'{phone}: {error.MESSAGE}')
        account_delete(phone)
        os.replace(f'{path}/session/{phone}.session',
                   f'{path}/banned/{phone}.session')
        os.replace(f'{path}/json/{phone}.json',
                   f'{path}/banned/{phone}.json')
        sys.exit()
    except Exception as error:
        print(Fore.RED + f'{error}')
        time.sleep(3)
        print(Fore.BLUE + f"{phone}: {app.get_me()['first_name']} cleans chats")

    ids = get_id_key(phone)
    for _id in ids:
        timer = get_timer(_id)
        if timer < round(time.time()):
            chat = get_chanel_id(_id)
            try:
                app.leave_chat(chat)
                chanel_delete(_id, chat)
            except ChannelInvalid as exc:
                #print(Fore.RED + f'{chat}: {exc.MESSAGE}')
                pass
            except ChannelPrivate as exc:
                #print(Fore.RED + f'{chat}: {exc.MESSAGE}')
                pass
            except UserNotParticipant as exc:
                #print(Fore.RED + f'{chat}: {exc.MESSAGE}')
                chanel_delete(_id, chat)
            except FloodWait as exc:
                print(Fore.RED + f'{phone} flood {exc.x} sec!')
                sys.exit()
            except Exception as error:
                print(Fore.RED + f'{error}')
    app.stop()
    sys.exit()
