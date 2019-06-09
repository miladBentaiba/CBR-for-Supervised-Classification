""" this module randomizes pairs of cases to generate new others """

import json

from FeaturesWeights.features_weights import Weighting
import init
from constants import ALL_FEATURES


S = init.Singleton.get_instance()


def features_interchanging(obj1, obj2):
    """
    :param obj1: the first case
    :param obj2: the second case
    :return: at most two generated cases by the most weighted features interchanging
    """
    _c = S.cursor()
    ordered_features = order_features()
    new_cases = []
    # number of features to substitute is number_substitutions
    obj3 = dict(obj1)
    obj4 = dict(obj2)
    number_substitutions = NUMBER_LEVELS - 1  # level
    for index in range(number_substitutions):
        feature = ordered_features[index]
        obj3[feature] = obj2[feature]
        obj4[feature] = obj1[feature]
    if obj3 not in (obj1, obj2):
        obj3.pop('_id_case')
        _c.execute('select count(*) from cases where bi is ? and age is ? and shape is ? and margin is ?'
                   ' and density is ? and severity is ?', (obj3['bi'], obj3['age'], obj3['shape'],
                                                           obj3['margin'], obj3['density'], obj3['severity']))
        numb = _c.fetchone()[0]
        if numb == 0:
            new_cases.append(json.dumps(obj3))

    if obj4 not in (obj1, obj2, obj3):
        obj4.pop('_id_case')
        _c.execute('select count(*) from cases where bi is ? and age is ? and shape is ? and margin is ?'
                   ' and density is ? and severity is ?', (obj4['bi'], obj4['age'], obj4['shape'],
                                                           obj4['margin'], obj4['density'], obj4['severity']))
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
        _c.execute('select cases._id_case, bi, age, shape, margin, density, severity '
                   ' from cases inner join cases_in_segment '
                   '             on (cases._id_case = cases_in_segment._id_case)'
                   ' where cases_in_segment._id_segment = ? and level = 1',
                   (_id_segment[0],))
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