""" This module contains the constants used in the project """

import json

CONST = {}

all_cases = []


def read_json(url):
    """parse json file into data"""
    with open(url) as file:
        return json.load(file)


# mammographic masses
data_file = "../datasets/mammographic-masses/mammographic.json"

DATABASE = 'mammography'

ALL_FEATURES = ['c_bi', 'n_age', 'c_shape', 'c_margin', 'c_density']

SOLUTION = 'severity'

PROBABILITY_FEATURES = {ALL_FEATURES[0]: 1 / 7, ALL_FEATURES[1]: 0.01, ALL_FEATURES[2]: 0.25,
                        ALL_FEATURES[3]: 0.2, ALL_FEATURES[4]: 0.2, SOLUTION: 0.5}

MAX_FEATURE = {'n_age': 100}
MIN_FEATURE = {'n_age': 18}

POSSIBLE_SOLUTIONS = [0, 1]

TABLES = '../datasets/mammographic-masses/tables.sql'

DATA = '../datasets/mammographic-masses/mammographic.json'

# ------------------------------------------------------------------------------------------------------------
# # immunotheraphy
# data_file = "../datasets/immunotheraphy/immunotheraphy.json"
#
# DATABASE = 'immunotheraphy'
#
# ALL_FEATURES = ["c_sex", "n_age", "n_time", "n_number_of_warts", "c_type", "n_area", "c_induration_diameter"]
#
# SOLUTION = "result_of_treatment"
#
# PROBABILITY_FEATURES = {
#     "c_sex": 0.5,
#     "n_age": 0.01,
#     "n_time": 0.01,
#     "n_number_of_warts": 0.05,
#     "c_type": 0.334,
#     "n_area": 0.01,
#     "c_induration_diameter": 0.01,
#     "result_of_treatment": 0.5
# }
#
# MAX_FEATURE = {
#     "n_age": 56,
#     "n_time": 12,
#     "n_number_of_warts": 19,
#     "c_induration_diameter": 70,
#     "n_area": 900
# }
# MIN_FEATURE = {
#     "n_age": 15,
#     "n_time": 0,
#     "n_number_of_warts": 1,
#     "c_induration_diameter": 5,
#     "n_area": 6
# }
#
# POSSIBLE_SOLUTIONS = [0, 1]
#
# TABLES = '../datasets/immunotherapy/tables.sql'
#
# DATA = '../datasets/immunotherapy/immunotheray.json'

# -----------------------------------------------------------------------------
# # Thyroid
# data_file = "../datasets/thyroid/thyroid.json"
#
# DATABASE = 'thyroid'
#
# ALL_FEATURES = ["n_t3_resin", "n_total_serum_thyroxin", "n_total_serum_triiodothyronine",
#                 "n_TSH", "n_difference_of_TSH"]
#
# SOLUTION = "class"
#
# PROBABILITY_FEATURES = {
#     "n_t3_resin":0.01,
#     "n_total_serum_thyroxin":0.01,
#     "n_total_serum_triiodothyronine":0.01,
#     "n_TSH":0.2,
#     "n_difference_of_TSH":0.2,
#     "class": 0.334
# }
#
# MAX_FEATURE = {
#     "n_t3_resin":144,
#     "n_total_serum_thyroxin": 22.3,
#     "n_total_serum_triiodothyronine": 10.0,
#     "n_TSH": 56.4,
#     "n_difference_of_TSH": 40.8
# }
# MIN_FEATURE = {
#     "n_t3_resin":65,
#     "n_total_serum_thyroxin": 0.5,
#     "n_total_serum_triiodothyronine": 0.2,
#     "n_TSH": 0.3,
#     "n_difference_of_TSH": -0.7
# }
#
# POSSIBLE_SOLUTIONS = [1, 2, 3]
#
# TABLES = '../datasets/thyroid/tables.sql'
#
# DATA = '../datasets/thyroid/thyroid.json'
