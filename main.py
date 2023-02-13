from telethon import TelegramClient
import datetime
import pytz
import time


# gets api keys for telegram bot to log in
def get_api_keys():
    with open("bot-password.txt", "r") as f:
        id = int(f.readline())
        hash = f.readline()
        return (id, hash)


# get all messages from dialog/channel by date
# return -1 if there won't be any msg further
def get_messages_by_date(chatid, date: datetime):
    tomorrow = date + datetime.timedelta(days=1)
    messages = []

    for msg in client.iter_messages(chatid, offset_date=tomorrow, wait_time=5):
        if msg.date < date:
            return messages
        messages.append(msg)

    if len(messages) == 0:
        return -1
    return messages


# downlaod all messages from chat
def get_all_messages(chatid, start_date = None, end_date = None):  # make it async!!!!
    if (start_date == None):
        start_date = datetime.datetime.now(tz=pytz.utc)
        start_date = datetime.datetime(start_date.date(),)

    if (end_date > start_date):
        raise Exception("end_date can't be greater than start_date")

    while (start_date != end_date):
        messages = get_messages_by_date(chatid, start_date)
        if messages == -1:
            break
        # do smth with messages
        start_date = start_date - datetime.timedelta(days=1)
        time.sleep(1)


# gets a list of chats/channels
def get_all_channels():
    new_channels = []
    for channel in client.iter_dialogs():
        new_channels.append(channel)
    return new_channels


if __name__ == '__main__':
    (api_id, api_hash) = get_api_keys()

    client = TelegramClient('TelegramRead', api_id, api_hash)
    client.start()
    #client.run_until_disconnected()

    #channels = get_all_channels()
    #for i in channels:
    #    print(i.id, i.title)
    #get_all_messages(1225428712)
    #get_messages_by_date(1225428712, datetime.datetime(2023, 1, 29, tzinfo=pytz.utc))
    #dialog_name = "Sasha Bossert"
    #async for dialog in client.iter_dialogs():
    #    if (dialog.is_channel and dialog.name == "Топор Live"):


