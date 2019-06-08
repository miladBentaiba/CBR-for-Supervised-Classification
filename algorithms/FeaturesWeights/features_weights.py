""" This module weights features and select the most appropriate ones. """

from itertools import combinations
from constants import FEATURES_NUMB

DATA = [
    {
        "cbi": 5,
        "nage": 67,
        "cshape": 3,
        "cmargin": 5,
        "cdensity": 3,
        "solution": 1,
        "frequency": 1
    },
    {
        "cbi": 4,
        "nage": 43,
        "cshape": 1,
        "cmargin": 1,
        "cdensity": None,
        "solution": 1,
        "frequency": 1
    },
    {
        "cbi": 5,
        "nage": 58,
        "cshape": 4,
        "cmargin": 5,
        "cdensity": 3,
        "solution": 1,
        "frequency": 1
    },
    {
        "cbi": 4,
        "nage": 28,
        "cshape": 1,
        "cmargin": 1,
        "cdensity": 3,
        "solution": 0,
        "frequency": 1
    },
    {
        "cbi": 5,
        "nage": 74,
        "cshape": 1,
        "cmargin": 5,
        "cdensity": None,
        "solution": 1,
        "frequency": 1
    },
    {
        "cbi": 4,
        "nage": 65,
        "cshape": 1,
        "cmargin": None,
        "cdensity": 3,
        "solution": 0,
        "frequency": 1
    },
    {
        "cbi": 4,
        "nage": 70,
        "cshape": None,
        "cmargin": None,
        "cdensity": 3,
        "solution": 0,
        "frequency": 1
    },
    {
        "cbi": 5,
        "nage": 42,
        "cshape": 1,
        "cmargin": None,
        "cdensity": 3,
        "solution": 0,
        "frequency": 1
    },
    {
        "cbi": 5,
        "nage": 57,
        "cshape": 1,
        "cmargin": 5,
        "cdensity": 3,
        "solution": 1,
        "frequency": 1
    },
    {
        "cbi": 5,
        "nage": 60,
        "cshape": None,
        "cmargin": 5,
        "cdensity": 1,
        "solution": 1,
        "frequency": 1
    },
    {
        "cbi": 5,
        "nage": 76,
        "cshape": 1,
        "cmargin": 4,
        "cdensity": 3,
        "solution": 1,
        "frequency": 1
    },
    {
        "cbi": 3,
        "nage": 42,
        "cshape": 2,
        "cmargin": 1,
        "cdensity": 3,
        "solution": 1,
        "frequency": 1
    },
    {
        "cbi": 4,
        "nage": 64,
        "cshape": 1,
        "cmargin": None,
        "cdensity": 3,
        "solution": 0,
        "frequency": 1
    },
    {
        "cbi": 4,
        "nage": 36,
        "cshape": 3,
        "cmargin": 1,
        "cdensity": 2,
        "solution": 0,
        "frequency": 1
    },
    {
        "cbi": 4,
        "nage": 60,
        "cshape": 2,
        "cmargin": 1,
        "cdensity": 2,
        "solution": 0,
        "frequency": 1
    },
    {
        "cbi": 4,
        "nage": 54,
        "cshape": 1,
        "cmargin": 1,
        "cdensity": 3,
        "solution": 0,
        "frequency": 1
    },
    {
        "cbi": 3,
        "nage": 52,
        "cshape": 3,
        "cmargin": 4,
        "cdensity": 3,
        "solution": 0,
        "frequency": 1
    },
    {
        "cbi": 4,
        "nage": 59,
        "cshape": 2,
        "cmargin": 1,
        "cdensity": 3,
        "solution": 1,
        "frequency": 1
    }
]


def features_weighting(data):
    """
    :return: calculate features weights
    """
    weight = {}
    # initiate the weights to 0
    for _x in range(FEATURES_NUMB):
        weight[list(data[0].keys())[_x]] = 0
    # calculate the weights using all possible pairs
    for pair in list(combinations(data, 2)):
        comparator = 1 if pair[0]['solution'] == pair[1]['solution'] else -1
        for i, _x in enumerate(pair[0]):
            # iterate over features
            # if feature is quantitative (n = numerical)
            if i < FEATURES_NUMB and _x[0] == 'n':
                if pair[0][_x] is not None and pair[1][_x] is not None and \
                        abs(pair[0][_x] - pair[1][_x]) < 10:
                    weight[_x] += (pair[0]["frequency"] * comparator)  # age
                else:
                    weight[_x] -= (int(pair[0]["frequency"]) * comparator)
            # if feature is qualitative (c = categorical)
            elif i < FEATURES_NUMB and _x[0] == 'c':
                if pair[0][_x] == pair[1][_x]:
                    weight[_x] += (pair[0]["frequency"] * comparator)  # frequency
                else:
                    weight[_x] -= (pair[0]["frequency"] * comparator)  # frequency
    # normalizing the calculated weights
    max_weight = weight[max(weight, key=weight.get)]
    min_weight = weight[min(weight, key=weight.get)]

    for i, _x in enumerate(data[0]):
        if i < FEATURES_NUMB:
            weight[_x] = (weight[_x] - min_weight) / (max_weight - min_weight)
    return weight

# features_weighting(DATA)
