""" This module represents R_S_CB system. """

from I_S_CB import upload_data
from randomization import randomization

upload_data('../datasets/mammographic-masses/tables.sql',
            '../datasets/mammographic-masses/mammographic.json')

randomization()
