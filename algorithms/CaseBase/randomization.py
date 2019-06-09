""" this module randomizes pairs of cases to generate new others """

import json

from FeaturesWeights.features_weights import Weighting
import init
from constants import ALL_FEATURES
from constants import SOLUTION


S = init.Singleton.get_instance()


def features_interchanging(obj1, obj2):
    """
    :param obj1: the first case
    :param obj2: the second case
    :return: at most two generated cases by the most weighted features interchanging
    """
    _c = S.cursor()
    ordered_features = Weighting.order_features()
    new_cases = []
    # number of features to substitute is number_substitutions
    obj3 = dict(obj1)
    obj4 = dict(obj2)
    number_substitutions = len(ALL_FEATURES) - 1  # level
    for index in range(number_substitutions):
        feature = ordered_features[index]
        obj3[feature] = obj2[feature]
        obj4[feature] = obj1[feature]
    if obj3 not in (obj1, obj2):
        obj3.pop('_id_case')
        _c.execute('select count(*) from cases where ({0}, ?) is ({1})'
                   .format(','.join(ALL_FEATURES), ','.join(['?'] * len(ALL_FEATURES))),
                   (SOLUTION,) + tuple(obj3[x] for x in ALL_FEATURES) + (obj3[SOLUTION],))
        numb = _c.fetchone()[0]
        if numb == 0:
            new_cases.append(json.dumps(obj3))

    if obj4 not in (obj1, obj2, obj3):
        obj4.pop('_id_case')
        _c.execute('select count(*) from cases where ({0}, ?) is ({1})'
                   .format(','.join(ALL_FEATURES), ','.join(['?'] * len(ALL_FEATURES))),
                   (SOLUTION,) + tuple(obj4[x] for x in ALL_FEATURES) + (obj4[SOLUTION],))
        numb = _c.fetchone()[0]
        if numb == 0:
            new_cases.append(json.dumps(obj4))

    return new_cases


def randomization(iteration_number):
    """
    :param iteration_number: the number of the iteration
    :return:
    """
    # new_cases will contain all the generated cases in one iteration
    print('[')
    # new_cases = []
    _d = S.cursor()
    _d.execute('select distinct _id_segment from segment')
    segments = _d.fetchall()
    # for each segment
    done = False
    for _id_segment in segments:
        # for each level in the segment
        _c = S.cursor()
        # get all the cases
        _c.execute('select cases._id_case, {0}, ? '
                   ' from cases inner join cases_in_segment '
                   '             on (cases._id_case = cases_in_segment._id_case)'
                   ' where cases_in_segment._id_segment = ? and level = 1'
                   .format(','.join(ALL_FEATURES)),
                   (SOLUTION, _id_segment[0],))
        cases = []
        # structure the query results in jsonArray
        for row in _c.fetchall():
            cases.append(dict((_c.description[i][0], value) for i, value in enumerate(row)))

        # do the attributes interchanging
        for i, cs1 in enumerate(cases):
            for j, cs2 in enumerate(cases):
                if cs1 != cs2:
                    added = features_interchanging(cs1, cs2)
                    for g_cas in added:
                        if not done:
                            done = True
                            print(g_cas)
                        else:
                            print(',', g_cas)
                    # new_cases = new_cases + added

    print(']')
