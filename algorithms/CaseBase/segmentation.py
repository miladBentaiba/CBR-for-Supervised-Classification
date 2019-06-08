from ..FeaturesWeights.features_weights import DATA
from ..FeaturesWeights.features_weights import features_weighting
#from FeaturesWeights import features_weights
#import FeaturesWeights.features_weights
# python -m  algorithms.CaseBase.segmentation.py
#from CBR.algorithms.FeaturesWeights import features_weights
from ...experiments import __init__
print('test', features_weighting(DATA))

# import sys
# print(sys.path)

import FeaturesWeights
print('feature weights inside seg', FeaturesWeights)
Seg = FeaturesWeights.features_weighting(FeaturesWeights.DATA)