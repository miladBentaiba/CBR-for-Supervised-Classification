""" This module allows for rule generation using fully valid cases """


from constants import POSSIBLE_SOLUTIONS
from constants import SOLUTION
from FeaturesWeights.features_weights import Weighting
import init

S = init.Singleton.get_instance()
_weights = Weighting.get_instance()


def rules_generation():
    """
    :return: generate rules from a valid case_base and store them in the rule table
    """
    _c = S.cursor()
    column_list = []
    where_clause = ''
    ordered_features = Weighting.order_features()
    for feature in ordered_features:
        column_list.append(feature)
        where_clause += ' and ' + feature + ' is not null'
        for solution in POSSIBLE_SOLUTIONS:
            columns = ",".join(column_list)
            print('columns', columns)
            print('where clause', where_clause)
            _c.execute("insert or ignore into rules ({0}, ?2)"
                       " select distinct {0}, ?2 from"
                       "  (select distinct {0}, ?2 from cases"
                       "  where ({0}) in ("
                       "    select {0} from cases where expert = 1 and ?2 = ?1)"
                       "   and ({0}) not in ("
                       "    select {0} from cases where expert = 1 and ?2 <> ?1)"
                       "  ) where 1 {1}"
                       .format(columns, where_clause), (solution, SOLUTION))
    S.commit()


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
