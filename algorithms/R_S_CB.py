# """This module uploads cases from file to the database."""
#
# from constants import SOLUTION
#
# import json
# from sqlite3 import OperationalError
# from random import shuffle
# from constants import ALL_FEATURES
# from rules_generation import rules_generation
# from stochastic_validation import randomness_ratio
# from stochastic_validation import significance
# from absolute_validation import validation_per_rules
# from segmentation import segment_all
#
# import init
#
# S = init.Singleton.get_instance()
#
#
# def read_json(url):
#     """parse json file into data"""
#     with open(url) as file:
#         return json.load(file)
#
#
# def create_tables(filename):
#     """
#     :param filename: the file that contains sql code
#           for tables creation
#     :return: tables will be created in the database
#     """
#     # Open and read the file as a single buffer
#     _fd = open(filename, 'r')
#     sql_file = _fd.read()
#     _fd.close()
#     _c = S.cursor()
#
#     # all SQL commands (split on ';')
#     sql_commands = sql_file.split(';')
#
#     # Execute every command from the input file
#     for command in sql_commands:
#         # This will skip and report errors
#         # For example, if the tables do not yet exist, this will skip over
#         # the DROP TABLE commands
#         try:
#             print(command)
#             _c.execute(command)
#         except OperationalError as msg:
#             print("Command skipped: ", msg)
#     S.commit()
#
#
# def insert_cases(_items):
#     """
#     :param _items: a case
#     :return: insert the case in the case-base if doesn't exist,
#     else increment its frequency
#     """
#     items = [tuple(cas.values()) for cas in _items]
#     _c = S.cursor()
#     new_all_features = ['new.' + x for x in ALL_FEATURES]
#     old_all_features = ['old.' + x for x in ALL_FEATURES]
#     print("with new ({1}, {0}, frequency, randomized, rule, expert) as ( values ({2}, ? , 1, 0, 1, 1)) "
#           "insert or replace into cases (_id_case, {1}, {0}, frequency, randomness, significance, rule, "
#           "                              expert, randomized) "
#           "select old._id_case, {3}, new.{0}, old.frequency + 1, old.randomness, old.significance, "
#           "       old.rule, new.expert, old.randomized "
#           "from new left join cases as old on ({3}, new.{0}) is ({4}, old.{0})"
#           .format(SOLUTION, ','.join(ALL_FEATURES), ','.join(['?'] * len(ALL_FEATURES)),
#                   ','.join(new_all_features), ','.join(old_all_features)), items)
#     _c.executemany("with new ({1}, {0}, frequency, randomized, rule, expert) as ( values ({2}, ? , 1, 0, 1, 1)) "
#                    "insert or replace into cases (_id_case, {1}, {0}, frequency, randomness, significance, rule, "
#                    "                              expert, randomized) "
#                    "select old._id_case, {3}, new.{0}, old.frequency + 1, old.randomness, old.significance, "
#                    "       old.rule, new.expert, old.randomized "
#                    "from new left join cases as old on ({3}, new.{0}) is ({4}, old.{0})"
#                    .format(SOLUTION, ','.join(ALL_FEATURES), ','.join(['?'] * len(ALL_FEATURES)),
#                            ','.join(new_all_features), ','.join(old_all_features)), items)
#     S.commit()
#
#
# def upload_data(tables_file, data_file):
#     """
#     :return: upload data to cases table
#     """
#     # create tables in the database
#     _c = S.cursor()
#     create_tables(tables_file)
#
#     # read the json from file
#     all_cases = []
#     for _it in read_json(data_file):
#         all_cases.append(_it)
#
#     # 1. insert cases in the cases table
#     shuffle(all_cases)
#     part_cases = all_cases[:50]
#     insert_cases(part_cases)
#
#     # get all the inserted cases
#     print('select _id_case, {1}, {0} from cases'.format(SOLUTION, ','.join(ALL_FEATURES)))
#     _c.execute('select _id_case, {1}, {0} from cases'.format(SOLUTION, ','.join(ALL_FEATURES)), ())
#     dictionaries_cases = []
#     for row in _c.fetchall():
#         dictionaries_cases.append(dict((_c.description[i][0], value)
#                                        for i, value in enumerate(row)))
#
#     # 2. rules generation
#     rules_generation()
#
#     # 3. calculate the stochastic and the absolute validity
#     for _it in dictionaries_cases:
#         # calculate the stochastic validity of the case
#         _it['randomness'] = randomness_ratio(_it)
#         _it['significance'] = significance(_it)
#         _e = S.cursor()
#         print('select frequency from cases where _id_case = ?')
#         _e.execute('select frequency from cases where _id_case = ?', (_it['_id_case'],))
#         _it['frequency'] = _e.fetchone()[0]
#         _it['rule'] = validation_per_rules(_it)
#     segment_all(dictionaries_cases, 0)
#
#     # update the stochastic and absolute validity of the case
#     items = [(cas['randomness'], cas['significance'], cas['rule'], cas['_id_case'])
#              for cas in dictionaries_cases]
#     print('update cases set randomness = ?, significance = ?, rule = ? where _id_case = ?')
#     _c.executemany('update cases set randomness = ?, significance = ?, rule = ? where _id_case = ?', items)
#     S.commit()
#
#
# def correction():
#     _c = S.cursor()
#     print('select {0}, {1} from test_cases'.format(",".join(ALL_FEATURES), SOLUTION))
#     _c.execute('select {0}, {1} from test_cases'.format(",".join(ALL_FEATURES), SOLUTION))
#     results = []
#     for row in _c.fetchall():
#         results.append(dict((_c.description[i][0], value) for i, value in enumerate(row)))
#     for res in results:
#         print('select _id_case from new_cases where ({0}, {1}) is ({2}, ?)'
#               .format(",".join(ALL_FEATURES), SOLUTION, ','.join(['?'] * len(ALL_FEATURES))))
#         _c.execute('select _id_case from new_cases where ({0}, {1}) is ({2}, ?)'
#                    .format(",".join(ALL_FEATURES), SOLUTION, ','.join(['?'] * len(ALL_FEATURES))),
#                    (tuple(res[x] for x in ALL_FEATURES), res[SOLUTION]))
#         _id_case = _c.fetchone()
#         if _id_case is not None:
#             print('update new_cases set frequency = frequency - 1 where _id_case is ? ')
#             _c.execute('update new_cases set frequency = frequency - 1 where _id_case is ? ', (_id_case[0],))
#     S.commit()
#     print('select {1}, {0} from new_cases'.format(SOLUTION, ",".join(ALL_FEATURES)))
#     _c.execute('select {1}, {0} from new_cases'.format(SOLUTION, ",".join(ALL_FEATURES)))
#     results = []
#     for row in _c.fetchall():
#         results.append(dict((_c.description[i][0], value)
#                             for i, value in enumerate(row)))
#     for res in results:
#         print('update cases set expert = 1 where ({1}, {0}) is ({2}, ?)'
#               .format(SOLUTION, ",".join(ALL_FEATURES), ','.join(['?'] * len(ALL_FEATURES))))
#         _c.execute('update cases set expert = 1 where ({1}, {0}) is ({2}, ?)'
#                    .format(SOLUTION, ",".join(ALL_FEATURES), ','.join(['?'] * len(ALL_FEATURES)),
#                            (tuple(res[x] for x in ALL_FEATURES), res[SOLUTION]) + res[SOLUTION]))
#     S.commit()
#
#
# # correction()
# upload_data('../datasets/mammographic-masses/tables.sql',
#             '../datasets/mammographic-masses/mammographic.json')
# # rules_generation()
