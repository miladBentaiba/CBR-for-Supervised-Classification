""" allow for only one connexion and one close of the database """

import sqlite3
from constants import DATABASE


class Singleton:
    """ open and close an sqlite connexion """
    __instance = None

    @staticmethod
    def get_instance():
        """ Static access method. """
        if Singleton.__instance is None:
            Singleton()
        return Singleton.__instance

    def __init__(self):
        """ Virtually private constructor """
        if Singleton.__instance is None:
            Singleton.__instance = sqlite3.connect(DATABASE + '.db')


    @staticmethod
    def __close__():
        """ close the database connexion """
        if Singleton.__instance is None:
            raise Exception("No connexion is open")
        else:
            Singleton.__instance.close()
            Singleton.__instance = None


Singleton.get_instance()
