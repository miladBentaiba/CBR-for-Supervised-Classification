""" This module contains the constants used in the project """


PROBABILITY_FEATURES = {'cbi': 1/7, 'nage': 0.01, 'cshape': 0.25, 'cmargin': 0.2,
                        'cdensity': 0.2, 'cseverity': 0.5}
MAX_FEATURE = {'nage': 100}
MIN_FEATURE = {'nage': 18}
SOLUTION = 'severity'
POSSIBLE_SOLUTIONS = [0, 1]
ALL_FEATURES=['cbi', 'nage', 'cshape', 'cmargin', 'cdensity']
