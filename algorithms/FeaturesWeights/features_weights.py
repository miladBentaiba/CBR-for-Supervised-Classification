""" This module weights features and select the most appropriate ones. """
import init
from itertools import combinations

import constants

S = init.Singleton.get_instance()
DATA = [
    {
        "c_bi": 5,
        "n_age": 67,
        "c_shape": 3,
        "c_margin": 5,
        "c_density": 3,
        "severity": 1,
        "frequency": 1
    },
    {
        "c_bi": 4,
        "n_age": 43,
        "c_shape": 1,
        "c_margin": 1,
        "c_density": None,
        "severity": 1,
        "frequency": 1
    },
    {
        "c_bi": 5,
        "n_age": 58,
        "c_shape": 4,
        "c_margin": 5,
        "c_density": 3,
        "severity": 1,
        "frequency": 1
    },
    {
        "c_bi": 4,
        "n_age": 28,
        "c_shape": 1,
        "c_margin": 1,
        "c_density": 3,
        "severity": 0,
        "frequency": 1
    },
    {
        "c_bi": 5,
        "n_age": 74,
        "c_shape": 1,
        "c_margin": 5,
        "c_density": None,
        "severity": 1,
        "frequency": 1
    },
    {
        "c_bi": 4,
        "n_age": 65,
        "c_shape": 1,
        "c_margin": None,
        "c_density": 3,
        "severity": 0,
        "frequency": 1
    },
    {
        "c_bi": 4,
        "n_age": 70,
        "c_shape": None,
        "c_margin": None,
        "c_density": 3,
        "severity": 0,
        "frequency": 1
    },
    {
        "c_bi": 5,
        "n_age": 42,
        "c_shape": 1,
        "c_margin": None,
        "c_density": 3,
        "severity": 0,
        "frequency": 1
    },
    {
        "c_bi": 5,
        "n_age": 57,
        "c_shape": 1,
        "c_margin": 5,
        "c_density": 3,
        "severity": 1,
        "frequency": 1
    },
    {
        "c_bi": 5,
        "n_age": 60,
        "c_shape": None,
        "c_margin": 5,
        "c_density": 1,
        "severity": 1,
        "frequency": 1
    },
    {
        "c_bi": 5,
        "n_age": 76,
        "c_shape": 1,
        "c_margin": 4,
        "c_density": 3,
        "severity": 1,
        "frequency": 1
    },
    {
        "c_bi": 3,
        "n_age": 42,
        "c_shape": 2,
        "c_margin": 1,
        "c_density": 3,
        "severity": 1,
        "frequency": 1
    },
    {
        "c_bi": 4,
        "n_age": 64,
        "c_shape": 1,
        "c_margin": None,
        "c_density": 3,
        "severity": 0,
        "frequency": 1
    },
    {
        "c_bi": 4,
        "n_age": 36,
        "c_shape": 3,
        "c_margin": 1,
        "c_density": 2,
        "severity": 0,
        "frequency": 1
    },
    {
        "c_bi": 4,
        "n_age": 60,
        "c_shape": 2,
        "c_margin": 1,
        "c_density": 2,
        "severity": 0,
        "frequency": 1
    },
    {
        "c_bi": 4,
        "n_age": 54,
        "c_shape": 1,
        "c_margin": 1,
        "c_density": 3,
        "severity": 0,
        "frequency": 1
    },
    {
        "c_bi": 3,
        "n_age": 52,
        "c_shape": 3,
        "c_margin": 4,
        "c_density": 3,
        "severity": 0,
        "frequency": 1
    },
    {
        "c_bi": 4,
        "n_age": 59,
        "c_shape": 2,
        "c_margin": 1,
        "c_density": 3,
        "severity": 1,
        "frequency": 1
    }
]


def features_weighting(data):
    """
    :return: calculate features weights
    """
    weight = {}
    # initiate the weights to 0
    for _x, f in enumerate(constants.ALL_FEATURES):
        weight[list(data[0].keys())[_x]] = 0
    # calculate the weights using all possible pairs
    for pair in list(combinations(data, 2)):
        comparator = 1 if pair[0][constants.SOLUTION] == pair[1][constants.SOLUTION] else -1
        for i, _x in enumerate(constants.ALL_FEATURES):
            # iterate over features
            # if feature is quantitative (n = numerical)
            if _x[0] == 'n':
                if pair[0][_x] is not None and pair[1][_x] is not None and \
                        abs(pair[0][_x] - pair[1][_x]) < 10:
                    weight[_x] += (pair[0]["frequency"] * comparator)  # age
                else:
                    weight[_x] -= (int(pair[0]["frequency"]) * comparator)
            # if feature is qualitative (c = categorical)
            elif _x[0] == 'c':
                if pair[0][_x] == pair[1][_x]:
                    weight[_x] += (pair[0]["frequency"] * comparator)  # frequency
                else:
                    weight[_x] -= (pair[0]["frequency"] * comparator)  # frequency
    # normalizing the calculated weights
    max_weight = weight[max(weight, key=weight.get)]
    min_weight = weight[min(weight, key=weight.get)]

    for i, _x in enumerate(data[0]):
        if i < len(constants.ALL_FEATURES):
            weight[_x] = (weight[_x] - min_weight) / (max_weight - min_weight)
    return weight


class Weighting:
    """ open and close an sqlite connexion """
    __instance = None

    @staticmethod
    def get_instance():
        """ Static access method. """
        if Weighting.__instance is None:
            Weighting(DATA)
        return Weighting.__instance

    def __init__(self, data):
        """ Virtually private constructor """
        if Weighting.__instance is None:
            _cur = S.cursor()
            _cur.execute('select feature, weight from weights')
            results = _cur.fetchall()
            if not results:
                Weighting.__instance = features_weighting(data)
            else:
                Weighting.__instance = {}
                for _x in results:
                    self.__instance[_x[0]] = _x[1]


# w = Weighting(DATA)
# print(features_weighting(DATA))
# x = tuple(v for v in DATA[0].values())
# print(x)
# print(','.join(constants.ALL_FEATURES))
# print(','.join(['?']*len(constants.ALL_FEATURES)))
list2 = tuple('?'+str(x) for x in range(1, len(constants.ALL_FEATURES)+1))
obj = {'a':1, 'b': 2}
print(obj)
obj.append({'c': 3})
print(obj)