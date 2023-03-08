"""

Этот класс описывает сообщение, которое хранится в бд

"""
import telethon.tl.types.messages


class Message:

    def __init__(self, msg: telethon.types.Message = None, chatid: int = -1, line: tuple = None):
        self.id = None
        self.chatid = chatid

        if msg is not None:
            self.message = msg.message
            self.date = msg.date

        if line is not None:
            self.id = line[0]
            self.chatid = line[1]
            self.date = line[2]
            self.message = line[3]

        assert self.chatid != -1

    def get_value(self):
        if id is None:
            return self.chatid, self.date, self.message
        return self.id, self.chatid, self.date, self.message

