#CSC466 F19 Lab 6
#Sarah Bae, shbae@calpoly.edu
#Roxanne Miller, rmille60@calpoly.edu
#weightedSum.py: python3 weightedSum.py <userid> <itemid> <output csv filename>

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
    targetUserItems = targetUser.ratedItems[targetUser.ratedItems != itemId]
    matchingItems = np.intersect1d(targetUserItems, secondUser.ratedItems)
   
    targetUserIndices = np.searchsorted(targetUserItems, matchingItems)
    secondUserIndices = np.searchsorted(secondUser.ratedItems, matchingItems)    
    
    targetUserRatings = np.take(targetUser.ratings, targetUserIndices)
    secondUserRatings = np.take(secondUser.ratings, secondUserIndices)

    return targetUserRatings, secondUserRatings

def weightedSum(users, items, user, item):
    summation = 0
    normalFactor = 0
    
    for i in range(len(users)):
        if i == user.id or item.id not in users[i].ratedItems:
            continue
        else:
            secondUser = users[i]
            targetUserRatings, secondUserRatings = compareUsers(user, secondUser, item.id)
            similarity = cosSim(targetUserRatings, secondUserRatings)
            
            secondUserUtilityIndex, = np.where(secondUser.ratedItems == item.id)
            secondUserUtility = secondUser.ratings[secondUserUtilityIndex]
            
            summation += similarity * secondUserUtility
            normalFactor += abs(similarity)

    return (1 / normalFactor) * summation

