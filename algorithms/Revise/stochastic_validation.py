""" This module calculates the stochastic validation of a case """

import json

from init import Singleton
from Retrieve.cases_similarity import compare_cases
from constants import SOLUTION
from constants import POSSIBLE_SOLUTIONS
from FeaturesWeights.features_weights import Weighting

S = Singleton.get_instance()
_weights = Weighting.get_instance()


# TODO
def frequency_ratio(obj):
    """
    :param obj: the case
    :return: ratio of the frequency of the case divided by the ratio of its problem part
    """
    _c = S.cursor()

    _c.execute('select sum(frequency) from cases where (bi, age, shape, margin, density) '
               'is (?, ?, ?, ?, ?) limit 1', (obj['bi'], obj['age'], obj['shape'],
                                              obj['margin'], obj['density']))
    results = _c.fetchone()[0]
    return obj['frequency'] / results


# TODO
def randomness_ratio(obj):
    """
    _s0 * (f0 + f1)                                _s1 * f0
    --------------    when normalized gives: ---------------------
    f0 * (_s0 + _s1)                          _s0 * f1 + _s1 * f0
    :param obj: the case
    :return: probability of getting the case (depends on the starting case-base)
    """
    _s0 = obj[SOLUTION]
    _s1 = POSSIBLE_SOLUTIONS.copy()
    # _s1 contains all other solutions except the solution of obj
    _s1.remove(obj[SOLUTION])
    _c = S.cursor()
    _c.execute('select (select sum(frequency) from cases where '
               '' + SOLUTION + '=?6 and expert is 1) as s0,'
               '(select sum(frequency) from cases '
               'where ?7 in ({0}) and '
               'expert is 1) as s1, '
               ' (select sum(frequency) from cases '
               '   where (bi, age, shape, margin, density, ?7, '
               'expert) is (?1, ?2, ?3, ?4, ?5, ?6, 1) ) as f0, '
               ' (select sum(frequency) from cases'
               '   where (bi, age, shape, margin, density) is (?1, ?2, ?3, ?4, ?5) '
               '  and ?7 in ({0}) and expert is 1) as f1'
               .format(",".join(map(str, _s1))),
               (obj['bi'], obj['age'], obj['shape'], obj['margin'], obj['density'], SOLUTION, str(_s0)))
    results = _c.fetchone()
    res = {'s0': 0 if results[0] is None else results[0],
           's1': 0 if results[1] is None else results[1],
           'f0': 0 if results[2] is None else results[2],
           'f1': 0 if results[3] is None else results[3]}
    randomness = 1 if res['s1'] == 0 or res['f1'] == 0 else \
        (res['s1'] * res['f0']) / ((res['s0'] * res['f1']) + (res['s1'] * res['f0']))
    return randomness


# TODO
def significance(obj):
    """
    :param obj: the case
    :return: max similarity to a valid case (if they have the same solution) or 1 - max
    if they don't have the same solution
    """
    _c = S.cursor()
    _c.execute('select distinct ? from cases where (bi, age, shape, margin, density, expert) '
               'is (?, ?, ?, ?, ?, 1)',
               (SOLUTION, obj['bi'], obj['age'], obj['shape'], obj['margin'], obj['density']))
    results = _c.fetchall()
    if results and (obj[SOLUTION],) in results:
        signif = 1
    elif results and (obj[SOLUTION],) not in results:
        signif = 0
    else:
        _c.execute('select bi, age, shape, margin, density, ? '
                   'from cases where expert is 1', (SOLUTION,))
        results = _c.fetchall()
        max_similarity = 0
        similar_case = {}
        for _case in results:
            _rs = json.dumps({'bi': _case[0], 'age': _case[1], 'shape': _case[2],
                              'margin': _case[3], 'density': _case[4],
                              SOLUTION: _case[5]}, allow_nan=True)
            sim = compare_cases(obj, json.loads(_rs), _weights)
            if sim > max_similarity:
                max_similarity = sim
                similar_case = json.loads(_rs)
        if similar_case[SOLUTION] == obj[SOLUTION]:
            signif = max_similarity
        elif similar_case[SOLUTION] != obj[SOLUTION] and max_similarity < 0.5:
            signif = 0
        else:
            signif = 1 - max_similarity
    return signif


def stochastic_validity(obj):
    """
    :param obj: the case
    :return: its stochastic validity based on the cases in the case-base
    """
    randomness = obj['randomness'] if obj['randomness'] is not None else randomness_ratio(obj)
    signif = obj['significance'] if obj['significance'] is not None else significance(obj)
    if obj['frequency'] == 0:
        return (randomness + signif) / 2
    else:
        return (frequency_ratio(obj) + randomness + signif) / 3
