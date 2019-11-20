#CSC466 F19 Lab 6
#Sarah Bae, shbae@calpoly.edu
#Roxanne Miller, rmille60@calpoly.edu
#meanUtilityFiltering.py: python3 meanUtilityFiltering.py

import sys
import parser
import numpy as np

def mean_util(score, user, item, users, items):
    if score != 99:
        actual = score
        index, = np.where(user.ratedItems == itemId)
        users[user.id].ratings[index] = 99
    predict()
