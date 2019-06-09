""" allow for only one connexion and one close of the database """

import sqlite3
from constants import DATABASE
from constants import ALL_FEATURES


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
            Singleton.__instance = sqlite3.connect(DATABASE+'.db')
            Singleton.create_tables()

    @staticmethod
    def create_tables():
        _cur = Singleton.__instance.cursor()
        _cur.execute('CREATE TABLE IF NOT EXISTS cases'
                     '('
                     '    _id_case integer PRIMARY KEY AUTOINCREMENT,'
                     '    c_bi int check (c_bi in (0,1,2,3,4,5,6)),'
                     '    n_age int check (n_age <101),'
                     '    c_shape int check(c_shape in (1,2,3,4)),'
                     '    c_margin int check(c_margin in (1,2,3,4,5)),'
                     '    c_density int check (c_density in (1,2,3,4)),'
                     '    severity int check (severity in (0,1)), /* solution part */'
                     '    frequency int DEFAULT 1 NOT NULL, /* number of times the case exists*/'
                     '    randomness int DEFAULT null, /* a value used to calculate the stochastic validity */'
                     '    significance int DEFAULT null, /* a value used to calculate the stochastic validity */'
                     '    rule boolean DEFAULT null, /* is it valid according to rules? */'
                     '    expert boolean DEFAULT null, /* does the expert approved its validity? */'
                     '    randomized boolean not null default false,'
                     '    CONSTRAINT constraint_case UNIQUE (c_bi, n_age, c_shape, c_margin, c_density, severity)'
                     ');')
        _cur.execute('CREATE TABLE IF NOT EXISTS weights'
                     '('
                     '  feature text primary key not null, /* bi, age, shape, margin or density */'
                     '  weight integer not null /* its weight, maximum 1, minimum 0 */'
                     ');')
        print("select sum(frequency) from cases where {0} is ({1}) limit 1"
                     .format(tuple(ALL_FEATURES), ','.join(['?'] * len(ALL_FEATURES))))
        obj = {"c_bi": 5, "n_age": 67, "c_shape": 3, "c_margin": 5, "c_density": 3,
               "severity": 1, "frequency": 1}
        _cur.execute("select sum(frequency) from cases where ({0}) is ({1}) limit 1"
                   .format(','.join(ALL_FEATURES), ','.join(['?'] * len(ALL_FEATURES))),
                   tuple(obj[x] for x in ALL_FEATURES))
        results = _cur.fetchone()
        print('res', results)


    @staticmethod
    def __close__():
        """ close the database connexion """
        if Singleton.__instance is None:
            raise Exception("No connexion is open")
        else:
            Singleton.__instance.close()
            Singleton.__instance = None


S = Singleton.get_instance()