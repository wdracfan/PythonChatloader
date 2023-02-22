from telethon import TelegramClient
from date_comp import *
import pytz
from time import sleep
import asyncio
from telethon.tl.types import PeerChannel

'''

В этом файле описан бот, который взаимодействует с telegram.
Бот умеет выполнять следующие команды:
    1) Найти канал по хэндлу (@*+)
    2) Получить сообщения из канала принадлежащие определенным дням
    3) Получить сообщения из канала в определенный день
     
'''


class TgBot:

    def __init__(self, api_id, api_hash):
        self.client = TelegramClient('TelegramRead', api_id, api_hash)
        self.client.start()

   #async def create_bot(self, api_id, api_hash):
   #     async with await TelegramClient('anon', api_id, api_hash).start() as client:
    #        self.client = client

    # gets all messages in certain date
    async def get_messages_by_date(self, chat_id, date: datetime):  # will be async, if we add many bots in future
        tomorrow = date + datetime.timedelta(days=1)
        messages = []

        async for msg in self.client.iter_messages(PeerChannel(chat_id), offset_date=tomorrow, wait_time=5):
            if date_is_less(msg.date, date):
                return messages
            if compare_dates(date, msg.date):
                messages.append(msg)
            print("got message")
            if len(messages) > 5:
                break
            await asyncio.sleep(5)

        if len(messages) == 0:
            return -1
        return messages

    # download all messages from chat
    # check_db - stops if found message that is presented in database
    def get_all_messages(self, chat_id, start_date=None, end_date=None, check_db=True):
        if start_date is None:
            start_date = datetime.datetime.now(tz=pytz.utc)

        if end_date is None:
            end_date = start_date
            end_date = end_date - datetime.timedelta(weeks=4 * 12 * 10)

        if end_date > start_date:
            raise Exception("end_date can't be greater than start_date")

        while not compare_dates(start_date, end_date):
            messages = self.get_messages_by_date(chat_id, start_date)
            if messages == -1:  # there won't be any messages further
                break

            # do smth with messages
            #print(start_date)
            #for i in messages:
            #    print(i.stringify())


            start_date = start_date - datetime.timedelta(days=1)
            sleep(1)

    # finds channel by handle in global chats or raises an exception
    async def find_channel(self, channel_handle: str):
        #import asyncio
        #from telethon import sync
        if len(channel_handle) == 0:
            raise Exception("Handle can't be empty")

        if channel_handle[0] != '@':
            raise Exception("Handle must starts with \'@\'")

        # Этот участок уходит в бесконечный цикл, хз почему, раньше работало
        # возможно это из-за настроек loop
        # res = await self.client(functions.contacts.SearchRequest(
        #     q=channel_handle,
        #     limit=10))
        #
        # for i in res.chats: # users are not supported for now(?)
        #     if i.username == channel_handle[1:]:
        #         return i
        res = await self.client.get_entity(entity=channel_handle[1:])
        print(res)

        if res is None:
            raise Exception("Channels with this handle were not found")
        return res

