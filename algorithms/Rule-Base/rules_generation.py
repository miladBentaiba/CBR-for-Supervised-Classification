""" This module allows for rule generation using fully valid cases """

from constantsMammographicMasses import POSSIBLE_SOLUTIONS
from constantsMammographicMasses import SOLUTION
from FeaturesWeights.features_weights import Weighting
from features_weights import order_features
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
    ordered_features = order_features()
    for feature in ordered_features:
        column_list.append(feature)
        where_clause += ' and ' + feature + ' is not null'
        for solution in POSSIBLE_SOLUTIONS:
            columns = ",".join(column_list)
            # print("insert or ignore into rules ({0}, {2})"
            #       " select distinct {0}, {2} from"
            #       "  (select distinct {0}, {2} from cases"
            #       "  where ({0}) in ("
            #       "    select {0} from cases where expert = 1 and {2} = ?1)"
            #       "   and ({0}) not in ("
            #       "    select {0} from cases where expert = 1 and {2} <> ?1)"
            #       "  ) where 1 {1}"
            #       .format(columns, where_clause, SOLUTION), (solution,))
            _c.execute("insert or ignore into rules ({0}, {2})"
                       " select distinct {0}, {2} from"
                       "  (select distinct {0}, {2} from cases"
                       "  where ({0}) in ("
                       "    select {0} from cases where expert = 1 and {2} = ?1)"
                       "   and ({0}) not in ("
                       "    select {0} from cases where expert = 1 and {2} <> ?1)"
                       "  ) where 1 {1}"
                       .format(columns, where_clause, SOLUTION), (solution,))
    S.commit()
