__author__ = "Alexei Evdokimov"
import os
import sqlite3
import json


class OWConnector(object):
    """
    Handles APPID existance and communicate with openweathermap.org
    """
    def __init__(self):
        self._id = self._fetch_id()

    def _fetch_id(self):
        got_file = False
        with os.scandir() as it:
            if "app.id" in [e.name for e in it]:
                got_file = True

        if got_file:
            with open("app.id") as f:
                return f.read()
        else:
            raise FileNotFoundError  # TODO: implement automatic APPID downloading

    @property
    def appid(self):
        return self._id


class Cities(object):
    """
    Populates database with city.list.json entries
    """
    def __init__(self):
        with open("city.list.json", "rb") as f:
            self._json = json.loads(f.read())
        # self._countries = set([entry["country"] for entry in self._json])

    def make_city_table(self):  # TODO: Make proper db schema (like countries_id in place of simple countries names)
        db = sqlite3.connect("weather.db")
        db.execute("CREATE TABLE `countries` "
                   "(`id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,"
                   "`name` TEXT UNIQUE);")
        with db:
            for country in self._countries:
                db.execute("INSERT INTO countries(name) VALUES (?)", (country, ))

    def populate_db_with_cities(self):
        db = sqlite3.connect("weather.db")
        db.execute("CREATE TABLE `cities` (`city_id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,"
                   "`city_name`	TEXT, `city_country` TEXT);")
        with db:
            for entry in self._json:
                db.execute("INSERT INTO cities(city_id, city_name, city_country) VALUES (?,?,?)",
                           (entry["id"], entry["name"], entry["country"]))


class DBHandler(object):
    """
    Communicate with database
    """
    def __init__(self):
        self._db = sqlite3.connect("weather.db")


class Forecast(object):
    def __init__(self):
        self._db = DBHandler()
        self._owconnector = OWConnector()


if __name__ == '__main__':
    cast = Forecast()

