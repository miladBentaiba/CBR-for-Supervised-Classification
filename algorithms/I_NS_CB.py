"""This module uploads cases from file to the database."""

from constants import SOLUTION

import json
from sqlite3 import OperationalError
from random import shuffle


from stochastic_validation import randomness_ratio
from stochastic_validation import significance
from rules_generation import rules_generation
from rules_generation import validation_per_rules
from segmentation import segment_all

import init

S = init.Singleton.get_instance()


def read_json(url):
    """parse json file into data"""
    with open(url) as file:
        return json.load(file)


def create_tables(filename):
    """
    :param filename: the file that contains sql code
          for tables creation
    :return: tables will be created in the database
    """
    # Open and read the file as a single buffer
    _fd = open(filename, 'r')
    sql_file = _fd.read()
    _fd.close()
    _c = S.cursor()

    # all SQL commands (split on ';')
    sql_commands = sql_file.split(';')

    # Execute every command from the input file
    for command in sql_commands:
        # This will skip and report errors
        # For example, if the tables do not yet exist, this will skip over
        # the DROP TABLE commands
        try:
            _c.execute(command)
        except OperationalError as msg:
            print("Command skipped: ", msg)


def insert_cases(_items):
    """
    :param _items: a case
    :return: insert the case in the case-base if doesn't exist,
    else increment its frequency
    """
    items = [tuple(cas.values()) for cas in _items]
    _c = S.cursor()
    _c.executemany("with new (bi, age, shape, margin, density, {0}, frequency, randomized,"
                   " rule, expert) "
                   "as (values (?, ?, ?, ?, ?, ?, 1, 0, 1, 1)) "
                   "insert or replace into cases "
                   "  (_id_case, bi, age, shape, margin, density, {0}, frequency, "
                   "   randomness, significance, rule, expert, randomized) "
                   "select old._id_case, new.bi, new.age, new.shape, new.margin, new.density, "
                   "       new.{0}, old.frequency + 1, old.randomness, old.significance, "
                   "       old.rule, new.expert, old.randomized "
                   "from new left join cases as old on "
                   " (new.c_bi, new.n_age, new.c_shape, new.c_margin, new.c_density, new.{0})"
                   " is (old.c_bi, old.n_age, old.c_shape, old.c_margin, old.c_density, old.{0})".format(SOLUTION), items)
    S.commit()


def upload_data():
    """
    :return: upload data to cases table
    """
    # create tables in the database
    _c = S.cursor()
    create_tables('../database/tables.sql')

    # read the json from file
    all_cases = []
    for _it in read_json('../data/native.txt'):
        all_cases.append(_it)

    # 1. insert cases in the cases table
    shuffle(all_cases)
    part_cases = all_cases[:50]
    insert_cases(part_cases)

    # get all the inserted cases
    _c.execute('select _id_case, bi, age, shape, margin, density, {0} from cases'.format(SOLUTION), ())
    dictionaries_cases = []
    for row in _c.fetchall():
        dictionaries_cases.append(dict((_c.description[i][0], value)
                                       for i, value in enumerate(row)))

    # 2. rules generation
    #rules_generation()

    # 3. calculate the stochastic and the absolute validity
    """for _it in dictionaries_cases:
        # calculate the stochastic validity of the case
        _it['randomness'] = randomness_ratio(_it)
        _it['significance'] = significance(_it)
        _e = S.cursor()
        _e.execute('select frequency from cases where _id_case = ?', (_it['_id_case'],))
        _it['frequency'] = _e.fetchone()[0]
        _it['rule'] = validation_per_rules(_it)
    segment_all(dictionaries_cases, 0)"""

    """# update the stochastic and absolute validity of the case
    items = [(cas['randomness'], cas['significance'], cas['rule'], cas['_id_case'])
             for cas in dictionaries_cases]
    _c.executemany('update cases set randomness = ?1, significance = ?2, rule = ?3 '
                   'where _id_case = ?4', items)"""
    S.commit()


def correction():
    _c = S.cursor()
    """_c.execute('select bi, age, shape, margin, density, severity from test_cases')
    results = []
    for row in _c.fetchall():
        results.append(dict((_c.description[i][0], value)
                                       for i, value in enumerate(row)))
    for res in results:
        _c.execute('select _id_case from new_cases where bi is ? and age is ?'
                   'and shape is ? and margin is ? and density is ? and severity is ?', (
            res['bi'], res['age'], res['shape'], res['margin'], res['density'], res['severity']
        ))
        _id_case = _c.fetchone()
        if _id_case is not None:
            _c.execute('update new_cases set frequency = frequency - 1 where _id_case is ? ', (_id_case[0],))
    S.commit()"""

    _c.execute('select bi, age, shape, margin, density, {0} from new_cases'.format(SOLUTION))
    results = []
    for row in _c.fetchall():
        results.append(dict((_c.description[i][0], value)
                            for i, value in enumerate(row)))
    for res in results:
        _c.execute('update cases set expert = 1 where (bi, age, shape, margin, density, {0}) is '
                   '(?, ?, ?, ?, ?, ?)'.format(SOLUTION), (res['bi'], res['age'], res['shape'], res['margin'],
                                          res['density'], res[SOLUTION]))
    S.commit()


# correction()
upload_data()
# rules_generation()
