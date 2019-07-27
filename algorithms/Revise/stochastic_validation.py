""" This module calculates the stochastic validation of a case """

import json

from init import Singleton
from Retrieve.cases_similarity import compare_cases
from constants import SOLUTION
from constants import POSSIBLE_SOLUTIONS
from constants import ALL_FEATURES
from FeaturesWeights.features_weights import Weighting

S = Singleton.get_instance()
_weights = Weighting.get_instance()


def frequency_ratio(obj):
    """
    :param obj: the case
    :return: ratio of the frequency of the case divided by the ratio of its problem part
    """
    _c = S.cursor()
    print("select sum(frequency) from cases where ({0}) is ({1}) limit 1"
          .format(','.join(ALL_FEATURES), ','.join(['?'] * len(ALL_FEATURES))))
    _c.execute("select sum(frequency) from cases where ({0}) is ({1}) limit 1"
               .format(','.join(ALL_FEATURES), ','.join(['?'] * len(ALL_FEATURES))),
               tuple(obj[x] for x in ALL_FEATURES))
    results = _c.fetchone()[0]
    print(results)
    return obj['frequency'] / results


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
    print("*************", _s0, _s1)
    # _s1 contains all other solutions except the solution of obj
    _s1.remove(obj[SOLUTION])
    _c = S.cursor()
    print('select (select sum(frequency) from cases where '
          '{3}=?1 and expert is 1) as s0,'
          '(select sum(frequency) from cases '
          'where ?2 in ({0}) and '
          'expert is 1) as s1, '
          ' (select sum(frequency) from cases '
          '   where ({1}, ?2, '
          'expert) is ({2}, ?1, 1) ) as f0, '
          ' (select sum(frequency) from cases '
          '   where ({1}) is ({2}) '
          '  and ?2 in ({0}) and expert is 1) as f1'
          .format(",".join(map(str, _s1)), ",".join(ALL_FEATURES),
                  ",".join(['?'] * len(ALL_FEATURES)), SOLUTION))
    _c.execute('select (select sum(frequency) from cases where '
               '{3}=?1 and expert is 1) as s0,'
               '(select sum(frequency) from cases '
               'where ?2 in ({0}) and '
               'expert is 1) as s1, '
               ' (select sum(frequency) from cases '
               '   where ({1}, ?2, '
               'expert) is ({2}, ?1, 1) ) as f0, '
               ' (select sum(frequency) from cases '
               '   where ({1}) is ({2}) '
               '  and ?2 in ({0}) and expert is 1) as f1'
               .format(",".join(map(str, _s1)), ",".join(ALL_FEATURES),
                       ",".join(['?'+str(x) for x in range(3, 8)]), SOLUTION),
               (SOLUTION, str(_s0)) + tuple(obj[x] for x in ALL_FEATURES))
    results = _c.fetchone()
    res = {'s0': 0 if results[0] is None else results[0],
           's1': 0 if results[1] is None else results[1],
           'f0': 0 if results[2] is None else results[2],
           'f1': 0 if results[3] is None else results[3]}
    randomness = 1 if res['s1'] == 0 or res['f1'] == 0 else \
        (res['s1'] * res['f0']) / ((res['s0'] * res['f1']) + (res['s1'] * res['f0']))
    return randomness


def significance(obj):
    """
    :param obj: the case
    :return: max similarity to a valid case (if they have the same solution) or 1 - max
    if they don't have the same solution
    """
    _c = S.cursor()
    print('select distinct ? from cases where ({0}, expert) '
          'is ({1}, 1)'.format(','.join(ALL_FEATURES), ",".join(['?'] * len(ALL_FEATURES))),  (obj[SOLUTION],) + tuple(obj[x] for x in ALL_FEATURES))
    _c.execute('select distinct ? from cases where ({0}, expert) '
               'is ({1}, 1)'.format(','.join(ALL_FEATURES), ",".join(['?'] * len(ALL_FEATURES))),
               (obj[SOLUTION],) + tuple(obj[x] for x in ALL_FEATURES))
    results = _c.fetchall()
    if results and (obj[SOLUTION],) in results:
        signif = 1
    elif results and (obj[SOLUTION],) not in results:
        signif = 0
    else:
        print('select {0}, ? from cases where expert is 1'.format(','.join(ALL_FEATURES)))
        _c.execute('select {0}, ? from cases where expert is 1'
                   .format(','.join(ALL_FEATURES)), (SOLUTION,))
        results = _c.fetchall()
        max_similarity = 0
        similar_case = {}
        for _case in results:
            _rs = json.dumps({ALL_FEATURES[x]: _case[x] for x in range(len(ALL_FEATURES))}
                             .update({SOLUTION: _case[len(ALL_FEATURES)]}), allow_nan=True)
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
