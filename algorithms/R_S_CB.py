""" This module represents R_S_CB system. """

from I_S_CB import insert_cases, read_json, I_S_CB_validation, I_S_CB_segment
from randomization import randomization


randomization()
all_cases = []
for _it in read_json("../datasets/mammographic-masses/rando1.json"):
    all_cases.append(_it)
all_cases = insert_cases(all_cases, 0)
I_S_CB_validation(all_cases)
I_S_CB_segment()
