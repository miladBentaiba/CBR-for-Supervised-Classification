""" This module weights features and select the most appropriate ones. """
import init
from itertools import combinations
import json

import constants

S = init.Singleton.get_instance()


def order_features():
    """
    :return: return a list of features from the most weighted to the less weighted
    """
    return sorted(Weighting.get_instance(), key=Weighting.get_instance().get, reverse=True)


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

    _cur = S.cursor()
    # print(weight.items())
    _cur.executemany('insert into weights (feature, weight) values(?, ?)', weight.items())
    S.commit()
    return weight


class Weighting:
    """ open and close an sqlite connexion """
    __instance = None

    @staticmethod
    def get_instance():
        """ Static access method. """
        if Weighting.__instance is None:
            _cur = S.cursor()
            _cur.execute('select {0}, {1}, frequency from cases'
                         .format(','.join(constants.ALL_FEATURES), constants.SOLUTION))
            cases = []
            for row in _cur.fetchall():
                cases.append(dict((_cur.description[i][0], value)
                                  for i, value in enumerate(row)))
            Weighting(cases)
        return Weighting.__instance

    def __init__(self, data):
        """ Virtually private constructor """
        if Weighting.__instance is None:
            _cur = S.cursor()
            # print('select feature, weight from weights')
            _cur.execute('select feature, weight from weights')
            results = _cur.fetchall()
            if not results:
                _cur = S.cursor()
                _cur.execute('select {0}, {1}, frequency from cases'
                             .format(','.join(constants.ALL_FEATURES), constants.SOLUTION))
                cases = []
                for row in _cur.fetchall():
                    cases.append(dict((_cur.description[i][0], value)
                                      for i, value in enumerate(row)))
                Weighting.__instance = features_weighting(cases)
            else:
                Weighting.__instance = {}
                for _x in results:
                    self.__instance[_x[0]] = _x[1]

# print(Weighting.get_instance())
