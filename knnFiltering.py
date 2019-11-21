#CSC466 F19 Lab 6
#Sarah Bae, shbae@calpoly.edu
#Roxanne Miller, rmille60@calpoly.edu
#knnFiltering.py: python3 knnFiltering.py <output csv filename>

import sys
import parser
import numpy as np

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

def compareUsers(targetUser, secondUser, itemId):
    targetRatings = targetUser.ratings
    targetUserItems = targetUser.ratedItems

    index, = np.where(targetUser.ratedItems == itemId)
    if index:
        targetUserItems = targetUser.ratedItems[targetUser.ratedItems != itemId]
        targetRatings = np.delete(targetUser.ratings, index)

    matchingItems = np.intersect1d(targetUserItems, secondUser.ratedItems)

    targetUserIndices = np.searchsorted(targetUserItems, matchingItems)
    secondUserIndices = np.searchsorted(secondUser.ratedItems, matchingItems)

    targetUserRatings = np.take(targetRatings, targetUserIndices)
    secondUserRatings = np.take(secondUser.ratings, secondUserIndices)

    return targetUserRatings, secondUserRatings

def avgKnn(k, users, items, user, item):
    sims = []
    for user2 in users:
        ratings1, ratings2 = compareUsers(user, user2, item.id)
        sims.append(cosSim(ratings1, ratings2))
    sims = -np.sort(-np.array(sims))
    return sims[:k].sum()/np.minimum(k, len(sims))
