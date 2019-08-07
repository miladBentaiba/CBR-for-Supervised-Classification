"""This module uploads cases from file to the database."""

import json
from sqlite3 import OperationalError
from random import shuffle
from constants import ALL_FEATURES, TABLES, SOLUTION, DATA

import init

S = init.Singleton.get_instance()


def read_json(url):
    """parse json file into data"""
    with open(url) as file:
        return json.load(file)


def create_tables():
    """
    :return: tables will be created in the database
    """
    # Open and read the file as a single buffer
    _fd = open(TABLES, 'r')
    sql_file = _fd.read()
    _fd.close()
    _c = S.cursor()

    # all SQL commands (split on ';')
    sql_commands = sql_file.split(';')

    # Execute every command from the input file
    for command in sql_commands:
        try:
            # print(command)
            _c.execute(command)
        except OperationalError as msg:
            # print("Command skipped: ", msg)
            return False
    S.commit()
    return True


def insert_cases(_items):
    """
    :param _items: a case
    :return: insert the case in the case-base if doesn't exist,
    else increment its frequency
    """
    # items = [tuple(cas.values()) for cas in _items]
    for cas in _items:
        s = cas[SOLUTION]
        cas.pop(SOLUTION)
        cas[SOLUTION] = s
        _c = S.cursor()
        new_all_features = ['new.' + x for x in ALL_FEATURES]
        old_all_features = ['old.' + x for x in ALL_FEATURES]
        # print("with new ({1}, {0}, frequency, randomized, rule, expert) as ( values ({2}, ? , 1, 0, null, 1)) "
        #       "insert or replace into cases (_id_case, {1}, {0}, frequency, randomness, significance, rule, "
        #       "                              expert, randomized) "
        #       "select old._id_case, {3}, new.{0}, old.frequency + 1, old.randomness, old.significance, "
        #       "       old.rule, new.expert, old.randomized "
        #       "from new left join cases as old on ({3}, new.{0}) is ({4}, old.{0})"
        #       .format(SOLUTION, ','.join(ALL_FEATURES), ','.join(['?'] * len(ALL_FEATURES)),
        #               ','.join(new_all_features), ','.join(old_all_features)), tuple(cas.values()))
        _c.execute('with new ({1}, {0}, frequency, randomized, rule, expert) as ( values ({2}, ? , 1, 0, 1, 1)) '
                   'insert or replace into cases (_id_case, {1}, {0}, frequency, randomness, significance, rule, '
                   '                              expert, randomized) '
                   'select old._id_case, {3}, new.{0}, old.frequency + 1, old.randomness, old.significance, '
                   '       old.rule, new.expert, old.randomized '
                   'from new left join cases as old on ({3}, new.{0}) is ({4}, old.{0})'
                   .format(SOLUTION, ','.join(ALL_FEATURES), ','.join(['?'] * len(ALL_FEATURES)),
                           ','.join(new_all_features), ','.join(old_all_features)), tuple(cas.values()))
        S.commit()
    _c.execute('select * from cases where expert is not "true"')
    cases = []
    for row in _c.fetchall():
        cases.append(dict((_c.description[i][0], value)
                          for i, value in enumerate(row)))
    return cases


def upload_data(data_file, percentage):
    """
    :return: upload data to cases table
    """
    # create tables in the database
    # print("create tables in the database")
    _c = S.cursor()
    created = create_tables()
    if created:
        # read the json from file
        # print("read the json from file")
        all_cases = []

        for _it in read_json(data_file):
            all_cases.append(_it)

        # 1. insert cases in the cases table
        # print("1. insert cases in the cases table")
        numb = int(len(all_cases) * percentage)
        shuffle(all_cases)
        insert_cases(all_cases[:numb+1])
        insert_test_cases(all_cases[numb+1:])
        S.commit()

    # get all the inserted cases
    # print("get all the inserted cases")
    # print('select _id_case, {1}, {0} from cases'.format(SOLUTION, ','.join(ALL_FEATURES)))
    _c.execute('select _id_case, {1}, {0} from cases'.format(SOLUTION, ','.join(ALL_FEATURES)), ())
    dictionaries_cases = []
    for row in _c.fetchall():
        dictionaries_cases.append(dict((_c.description[i][0], value)
                                       for i, value in enumerate(row)))

    # 2. rules generation
    # print("2. rules generation")
    from rules_generation import rules_generation
    rules_generation()

    I_S_CB_validation(dictionaries_cases)
    I_S_CB_segment()


def I_S_CB_segment():
    # print("case-base segmentation")
    _c = S.cursor()
    from segmentation import segment_all
    _c.execute('select _id_case, {1}, {0}, randomness, significance, frequency,'
               ' stochasticity, rule from cases where segmented = "false"'
               .format(SOLUTION, ','.join(ALL_FEATURES)), ())
    dictionaries_cases = []
    for row in _c.fetchall():
        dictionaries_cases.append(dict((_c.description[i][0], value)
                                       for i, value in enumerate(row)))
    segment_all(dictionaries_cases, 0)
    _c.execute('update cases set segmented = "true"')
    S.commit()


def I_S_CB_validation(dictionaries_cases):
    _c = S.cursor()
    # 3. calculate the stochastic and the absolute validity
    # print("3. calculate the stochastic and the absolute validity")
    from stochastic_validation import randomness_ratio
    from stochastic_validation import significance
    from absolute_validation import validation_per_rules
    from stochastic_validation import stochastic_validity

    for _it in dictionaries_cases:
        # calculate the stochastic validity of the case
        _it['randomness'] = randomness_ratio(_it)
        _it['significance'] = significance(_it)
        _e = S.cursor()
        # print('select frequency from cases where _id_case = ?')
        _e.execute('select frequency from cases where _id_case = ?', (_it['_id_case'],))
        _it['frequency'] = _e.fetchone()[0]
        _it['stochasticity'] = stochastic_validity(_it)
        _it['rule'] = validation_per_rules(_it)[0]
    S.commit()

    # update the stochastic and absolute validity of the case
    # print("update the stochastic and absolute validity of the case")
    items = [(cas['randomness'], cas['significance'], cas['rule'], cas['stochasticity'], cas['_id_case'])
             for cas in dictionaries_cases]
    # print('update cases set randomness = ?, significance = ?, rule = ?, stochasticity=? where _id_case = ?')
    _c.executemany('update cases set randomness = ?, significance = ?, rule = ? , '
                   ' stochasticity=? where _id_case = ?', items)
    S.commit()


def correction():
    _c = S.cursor()
    # print('select {0}, {1} from test_cases'.format(",".join(ALL_FEATURES), SOLUTION))
    _c.execute('select {0}, {1} from test_cases'.format(",".join(ALL_FEATURES), SOLUTION))
    results = []
    for row in _c.fetchall():
        results.append(dict((_c.description[i][0], value) for i, value in enumerate(row)))
    for res in results:
        # print('select _id_case from new_cases where ({0}, {1}) is ({2}, ?)'
        #       .format(",".join(ALL_FEATURES), SOLUTION, ','.join(['?'] * len(ALL_FEATURES))))
        _c.execute('select _id_case from new_cases where ({0}, {1}) is ({2}, ?)'
                   .format(",".join(ALL_FEATURES), SOLUTION, ','.join(['?'] * len(ALL_FEATURES))),
                   (tuple(res[x] for x in ALL_FEATURES), res[SOLUTION]))
        _id_case = _c.fetchone()
        if _id_case is not None:
            # print('update new_cases set frequency = frequency - 1 where _id_case is ? ')
            _c.execute('update new_cases set frequency = frequency - 1 where _id_case is ? ', (_id_case[0],))
    S.commit()
    # print('select {1}, {0} from new_cases'.format(SOLUTION, ",".join(ALL_FEATURES)))
    _c.execute('select {1}, {0} from new_cases'.format(SOLUTION, ",".join(ALL_FEATURES)))
    results = []
    for row in _c.fetchall():
        results.append(dict((_c.description[i][0], value)
                            for i, value in enumerate(row)))
    for res in results:
        # print('update cases set expert = 1 where ({1}, {0}) is ({2}, ?)'
        #       .format(SOLUTION, ",".join(ALL_FEATURES), ','.join(['?'] * len(ALL_FEATURES))))
        _c.execute('update cases set expert = 1 where ({1}, {0}) is ({2}, ?)'
                   .format(SOLUTION, ",".join(ALL_FEATURES), ','.join(['?'] * len(ALL_FEATURES)),
                           (tuple(res[x] for x in ALL_FEATURES), res[SOLUTION]) + res[SOLUTION]))
    S.commit()


def insert_test_cases(_items):
    for cas in _items:
        s = cas[SOLUTION]
        cas.pop(SOLUTION)
        cas[SOLUTION] = s
        _c = S.cursor()
        try:
            _c.execute('insert into test_cases ({1}, {0}) values ({2}, ?)'
                       .format(SOLUTION, ','.join(ALL_FEATURES), ','.join(['?'] * len(ALL_FEATURES)), ),
                       tuple(cas.values()))
            S.commit()
        except:
            print("pass")
            pass


upload_data(DATA, 0.1)
