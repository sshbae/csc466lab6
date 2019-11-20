#CSC466 F19 Lab 6
#Sarah Bae, shbae@calpoly.edu
#Roxanne Miller, rmille60@calpoly.edu
#knnFiltering.py: python3 knnFiltering.py <output csv filename>

import sys
import parser

def cosSim(user1, user2):
    numer = 0
    denom1 = 0
    denom2 = 0

    numerArray = np.multiply(user1, user2)
    numer = np.sum(numerArray)

    denom1Array = np.power(user1, 2)
    denom1 = np.sum(denom1Array)
    denom1 = np.sqrt(denom1)

    denom2Array = np.power(user2, 2)
    denom2 = np.sum(denom2Array)
    denom2 = np.sqrt(denom2)

    return numer / (denom1 * denom2)


def avgKnn(users, items):
    cosSim
