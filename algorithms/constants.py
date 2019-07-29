""" This module contains the constants used in the project """

import json

CONST = {}
data_file = "../datasets/mammographic-masses/mammographic.json"
all_cases = []


def read_json(url):
    """parse json file into data"""
    with open(url) as file:
        return json.load(file)


# for _it in read_json(data_file):
#     all_cases.append(_it)

DATABASE = 'mammography'

ALL_FEATURES = ['c_bi', 'n_age', 'c_shape', 'c_margin', 'c_density']

SOLUTION = 'severity'

PROBABILITY_FEATURES = {ALL_FEATURES[0]: 1/7, ALL_FEATURES[1]: 0.01, ALL_FEATURES[2]: 0.25,
                        ALL_FEATURES[3]: 0.2, ALL_FEATURES[4]: 0.2, SOLUTION: 0.5}

MAX_FEATURE = {'n_age': 100}
MIN_FEATURE = {'n_age': 18}

POSSIBLE_SOLUTIONS = [0, 1]
