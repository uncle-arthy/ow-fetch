from builtins import property

__author__ = "Alexei Evdokimov"
import os


class AppID(object):
    
    def __init__(self):
        self._id = ""
        self.fetch_id()

    def fetch_id(self):
        got_file = False
        with os.scandir() as it:
            if "app.id" in [e.name for e in it]:
                got_file = True

        if got_file:
            with open("app.id") as f:
                self._id = f.read()
        else:
            raise FileNotFoundError  # TODO: implement automatic APPID downloading

    @property
    def appid(self):
        return self._id


class Cities(object):
    pass


class DBHandler(object):
    pass


class Forecast(object):
    pass


if __name__ == '__main__':
    ai = AppID()
    print(ai.appid)
