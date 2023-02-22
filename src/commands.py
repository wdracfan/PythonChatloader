
"""

Этот класс обрабатывает команды пользователя
Классы очень сырой, пока поддерживается только одна команда

"""

import datetime
from tgbot import TgBot
from database_commands import *


class Commands:
    bot = TgBot                      # telegram bot
    db = DatabaseCommands            # database

    @staticmethod
    def start(api_id, api_hash, settings):   # init all stuff
        Commands.bot = TgBot(api_id, api_hash)
        Commands.db = DatabaseCommands(settings)

    @staticmethod
    async def get_messages(chatid: int, date: datetime):         # gets messages by chatid and date
        res = await Commands.bot.get_messages_by_date(chatid, date)
        msg = [Message(msg=i, chatid=chatid) for i in res]
        for i in msg:
            print(i.date, i.message)
        await Commands.db.write_messages(msg)

    @staticmethod
    async def get_chat_id(handle: str):                          # get chatid by handle
        res = await Commands.bot.find_channel(handle)
        print(res.title)
        return res
