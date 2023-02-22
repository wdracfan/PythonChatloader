import asyncio

import psycopg
from Message import Message
from Request import Request

'''

Базы данных:
    1) requests - база, где будут храниться запросы пользователя и их статус коды
        id PRIMARY KEY - id
        url TEXT NOT NULL - url запроса
        request_time timestamp NOT NULL - время запроса
        response_time timestamp NULL - время ответа(NULL - не обработан) 
        status INTEGER NULL - статус запроса (NULL - не обработан)
        
    2) messages - база данных, содержащая скачанные пользователем сообщения
        id PRIMARY KEY - id(в базе данных!!!!)
        chatid BITINT NOTNULL - id канала
        date timestamp - время, в которое было написанно сообщение
        message TEXT - само сообщение
        TODO добавить реакции/имя пользователя(если есть) и т.д.
    
    3) channels - база данных, содержащая каналы TODO

'''


class DatabaseCommands:

    def __init__(self, config):
        self.config = config
        self.create_messages()
        self.create_request()

    def create_messages(self):   # creates messages table
        with psycopg.connect(
                self.config["PostgresOptions"]) as aconn:
            with aconn.cursor() as acur:
                acur.execute(
                    "CREATE TABLE IF NOT EXISTS messages("
                    "id SERIAL PRIMARY KEY, "
                    "chatid BIGINT NOT NULL,"
                    "date TIMESTAMP,"
                    "message TEXT)")

    async def get_messages(self, chatid: int):    # gets all messages by chatid
        async with await psycopg.AsyncConnection.connect(
                self.config["PostgresOptions"]) as aconn:
            async with aconn.cursor() as acur:
                rows = await acur.execute(
                    "SELECT * FROM messages WHERE"
                    "chatid == %s",
                    chatid)
                res = await rows.fetchmany(100)  # <---- тут ограничение, потом что-нибудь придумаем
                if res is None:
                    return []

                res = [Message(line=i) for i in res]
                return res

    # async def get_message   <--- тут любые запросы сообщений, любые операции

    async def write_messages(self, messages: list):     # adds list of messages to database
        async with await psycopg.AsyncConnection.connect(
                self.config["PostgresOptions"]) as aconn:
            async with aconn.cursor() as acur:
                for i in messages:
                    await acur.execute(
                        "INSERT INTO messages (chatid, date, message)"
                        "VALUES (%s, %s, %s)", (i.chatid, i.date, i.message))

    async def check_for_message(self, message):        # returns True if message presented in database and else either
        async with await psycopg.AsyncConnection.connect(
                self.config["PostgresOptions"]) as aconn:
            async with aconn.cursor() as acur:
                rows = await acur.execute(
                    "SELECT * FROM messages WHERE"
                    "chatid == %s AND date == %s AND message == %s",
                    (message.chatid, message.date, message.message))
                res = await rows.fetchone()
                if res is None or len(res) == 0:
                    return False
                return True

    def create_request(self):   # creates requests table
        with psycopg.connect(
                self.config["PostgresOptions"]) as aconn:
            with aconn.cursor() as acur:
                acur.execute(
                    "CREATE TABLE IF NOT EXISTS requests("
                    "id SERIAL PRIMARY KEY, "
                    "url TEXT NOT NULL,"
                    "request_time TIMESTAMP NOT NULL,"
                    "response_time TIMESTAMP,"
                    "status INTEGER)")

    async def read_request(self):   # gets first unprocessed request
        async with await psycopg.AsyncConnection.connect(
                self.config["PostgresOptions"]) as aconn:
            async with aconn.cursor() as acur:
                req = await acur.execute(
                    "SELECT * FROM requests WHERE"
                    "status == NULL")
                req = await req.fetchone()

                if req is None:
                    return req
                req = Request(req)
                return req

    async def answer_request(self, response: Request):   # answers to request
        async with await psycopg.AsyncConnection.connect(
                self.config["PostgresOptions"]) as aconn:
            async with aconn.cursor() as acur:
                req = await acur.execute(
                    "SELECT * FROM requests WHERE"
                    "id == %s", response.id)
                req = await req.fetchone()
                if req is None:
                    raise Exception(f"Request to response was not found: id = {response.id}")

                req = Request(req)
                if req.status is not None:
                    raise Exception(f"Request to response was already handler: id = {response.id}")

                await acur.execute(
                    "UPDATE request SET"
                    "(response_time, status) = (%s, %s)"
                    "WHERE id == %s", (response.resp, response.status, response.id)
                )
