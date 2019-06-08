"""This module segments the cases into three parts solution / problem / level."""


from constants import NUMBER_LEVELS
from constants import PROBABILITY_FEATURES


def compare_case_delegate(obj, delegate, _weights):
    """
    :param _weights: features weights
    :param obj: a case
    :param delegate: a segment delegate
    :return: compare the object with the delegate to find the similarity
    """
    total = 0
    weights = 0
    # for each feature _x
    for _x in obj:
        # if _x is nominative
        if _x[0] == 'c':
            # initially, similarity is zero
            sim_x = 0
            # when the value is none, similarity is a probability of
            # having a value of the feature
            if obj[_x] is None:
                sim_x = PROBABILITY_FEATURES[_x]
            else:  # value isn't null
                frequencies = 0
                try:
                    for ite in delegate[_x]:
                        frequencies += ite['frequency']
                        if obj[_x] == ite['value']:
                            sim_x = ite['frequency']
                except KeyError:
                    sim_x = 0
                else:
                    if frequencies == 0:
                        sim_x = PROBABILITY_FEATURES[_x]
                    else:
                        sim_x /= frequencies
            sim_x *= _weights[_x]
            total += sim_x
            weights += _weights[_x]
        # if _x is qualitative
        elif _x[0] == 'n':
            try:
                # age is a quantitative attribute, and has a different similarity function
                total += (1 - abs((obj[_x] - delegate[_x][0]['value']) / 100)) * _weights[_x]
                weights += _weights[_x]
            except KeyError:
                pass
            except TypeError:
                pass
    return total / weights


def get_level(similarity):
    """
    :param similarity: the similarity between  case and a delegate of a segment
    :return: the corresponding level
    """
    level_length = round(1 / NUMBER_LEVELS, 2)
    level_position = 1
    level = -1
    for _x in range(1, NUMBER_LEVELS):
        level_position -= level_length
        level_position = round(level_position, 2)
        if similarity >= level_position:
            level = _x
            break
    return level
