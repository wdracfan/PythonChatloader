"""

Этот класс описывает запросы пользователей

"""


class Request:

    def __init__(self, lst: tuple):
        self.id = lst[0]
        self.url = lst[1]
        self.req = lst[2]
        self.resp = None
        self.status = None
        if len(lst) >= 4:
            self.resp = lst[3]
        if len(lst) >= 5:
            self.status = lst[4]
        assert self.url is not None

    def get_value(self):
        if self.id is None:
            return self.url, self.req, self.resp, self.status
        return self.id, self.url, self.req, self.resp, self.status
