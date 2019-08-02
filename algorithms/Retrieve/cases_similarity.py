""" This module compares two cases and returns the similarity between them"""

import constants


def compare_nominative(feature, value1, value2):
    """
    :param feature: name of the nominative feature
    :param value1: value of the feature in the first case
    :param value2: value of the feature in the second case
    :return: similarity between the values
    """
    if value1 == value2:
        sim_value = 1
    elif value1 is None or value2 is None:
        sim_value = constants.PROBABILITY_FEATURES[feature]
    else:
        sim_value = 0
    return sim_value


def compare_quantitative(feature, value1, value2):
    """
    :param feature: name of the nominative feature
    :param value1: value of the feature in the first case
    :param value2: value of the feature in the second case
    :return: similarity between the values
    """
    if value1 is None or value2 is None:
        sim_value = constants.PROBABILITY_FEATURES[feature]
    else:
        sim_value = 1 - ((abs(value1 - value2)) * 1.0 /
                         (constantss.MAX_FEATURE[feature] - constants.MIN_FEATURE[feature]))
    return sim_value


def compare_cases(obj1, obj2, weights):
    """
    :param weights: features weights
    :param obj1: the first case
    :param obj2: the second case
    :return: similarity between the two cases using weights
    """
    similarity = 0
    weights_sum = 0
    # similarity between two nominative features is calculated differently from
    # two quantitative values
    for _x in constants.ALL_FEATURES:
        # if _x is nominative
        if _x[0] == 'c':
            similarity += compare_nominative(_x, obj1[_x], obj2[_x]) * weights[_x]
            weights_sum += weights[_x]
        # if _x is qualitative
        elif _x[0] == 'n':
            similarity += compare_quantitative(_x, obj1[_x], obj2[_x]) * weights[_x]
            weights_sum += weights[_x]
    return similarity / weights_sum


def compare_cases_initial(obj1, obj2):
    """
    :param obj1: the first case
    :param obj2: the second case
    :return: similarity between the two cases before having weights
    """
    similarity = 0
    weights_sum = 0
    # similarity between two nominative features is calculated differently from
    # two quantitative values
    for _x in constants.ALL_FEATURES:
        # if _x is nominative
        if _x[0] == 'c':
            similarity += compare_nominative(_x, obj1[_x], obj2[_x])
            weights_sum += 1
        # if _x is qualitative
        elif _x[0] == 'n':
            similarity += compare_quantitative(_x, obj1[_x], obj2[_x])
            weights_sum += 1
    return similarity / weights_sum


# print(compare_cases_initial(DATA[0], DATA[2]))
