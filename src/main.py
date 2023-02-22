import asyncio
from datetime import datetime
import os
import configparser
import sys
from commands import Commands
from database_commands import *

import pytz

from tgbot import TgBot

'''
Это список операций, которые умеет выполнять бот.

Операции, доступные пользователю:
    Каналы:
        1) Начать отслеживать новый канал
        2) Прекратить отслеживать определенный канал
    Сообщения:
        1) Получить сообщения с определнного канала за определенную дату
        TODO


Внутренние операции:
    Каналы:
        1) Найти канал - ищет канал по хэндлу (и добавляет его в бд, чтобы больше не искать)
        2) Провалидировать, что данные о канале в бд валидные (совпадение хэндла при одинаковом id)
    Сообщения:
        1) Получить сообщения за определенную дату
        2) Скачать все сообщения канала
        * Тут могут быть любые тяжелые операции с бд
        


Операции с базой данных:
    Каналы:
        отдельная таблица, содержащая информацию о канала каналах
        primary key - хэндл
        1) найти канал по хэндлу (channel or null)
        2) добавить канал
        3) пометить информацию о канале как неактуальную
    Запросы:
        отдельная таблица
        primary key - id, url запроса(не отличать http от https!!!), текущий статус
    Сообщения с каналов:
        primary key - id, id канала, само сообщение (реакции?)
'''


# gets api keys for telegram bot to log in
def get_api_keys():
    with open("bot-password.txt", "r") as f:
        id = int(f.readline())
        hash = f.readline()
        return (id, hash)


# gets settings depend on the env
def get_settings():
    in_container = os.environ.get('IN_A_DOCKER_CONTAINER', False)
    sect = "Container" if in_container else "Development"

    parser = configparser.ConfigParser()
    parser.read('Settings.ini')
    return parser[sect]


async def main():
    print("1) получить сообщения по chatid и записать их в бд\n" +
          "2) получить chatid по хэндлу (или ошибкой в лицо)")
    while True:
        s = input().split()
        if int(s[0]) == 1:
            await Commands.get_messages(int(s[1]), datetime.strptime(s[2], "%d.%m.%Y").date())
        else:
            res = await Commands.get_chat_id(s[1])
            print(res.id)

if __name__ == '__main__':
    (api_id, api_hash) = get_api_keys()
    settings = get_settings()
    Commands.start(api_id, api_hash, settings)

    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    loop = asyncio.new_event_loop()
    #asyncio.set_event_loop(loop)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

    # @client.on(events.NewMessage) - в будущем
    #cli
   # future = loop.create_task(Commands.get_chat_id("@u_now"))
    #loop.(future)

    #loop = asyncio.new_event_loop()
    #f = loop.create_task(bot.find_channel("@u_nowergerg"))
    #loop.run_until_complete(f)
    #for i in bot.iter_dialogs():
    #    print(i)
    #    break
    #loop = asyncio.new_event_loop()
    #res = loop.create_task(bot.get_entity("@andreytrokhachev"))
    #loop.run_until_complete(res)
    #res = asyncio.run(bot.find_channel("@u_nowergerg"))
    #print(res.title)
    #client.get_all_messages(1225428712, datetime.datetime(2023, 2, 17, tzinfo=pytz.utc))

