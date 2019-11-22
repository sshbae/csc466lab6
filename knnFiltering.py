#CSC466 F19 Lab 6
#Sarah Bae, shbae@calpoly.edu
#Roxanne Miller, rmille60@calpoly.edu
#knnFiltering.py: python3 knnFiltering.py <output csv filename>

import sys
import parser
import numpy as np

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

    return matchingItems, targetUserRatings, secondUserRatings

def avgKnn(k, users, items, user, item, simMeasure):
    sims = []
    for user2 in users:
        matchingItems, ratings1, ratings2 = compareUsers(user, user2, item.id)
        sim = simMeasure(matchingItems, items, ratings1, ratings2)
        sims.append(sim)
    sims = -np.sort(-np.array(sims))
    print(sims)
    return sims[:k].sum()/np.minimum(k, len(sims))
