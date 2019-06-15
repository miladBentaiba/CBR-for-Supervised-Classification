
from FeaturesWeights.features_weights import Weighting
from constants import SOLUTION
import init

S = init.Singleton.get_instance()


def validation_per_rules(obj):
    """
    :rtype: dictionary
    :param obj: a case to validate
    :return: depending on the rules. if it doesn't break them return true else false.
    if it's impossible to verify return None
    """
    _c = S.cursor()
    i = 0
    valid = None
    where_clause = ''
    ordered_features = Weighting.order_features()
    for feature in ordered_features:
        i += 1
        where_clause += ' and ' + feature + ' is ' + \
                        (' null ' if obj[feature] is None else str(obj[feature]))
        null_values = ''
        for j in range(i, len(ordered_features)):
            null_values += ' and ' + ordered_features[j] + ' is null'
        _c.execute('select distinct ? from rules where 1 {0}{1}'
                   .format(where_clause, null_values), (SOLUTION,))
        results = _c.fetchall()
        if len(results) == 1 and results[0][0] == obj[SOLUTION]:
            valid = True
            break
        elif len(results) == 1 and results[0][0] != obj[SOLUTION]:
            valid = False
            break
        elif results:
            valid = None
        else:  # len(results) > 1
            valid = None
    return valid
