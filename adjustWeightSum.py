#CSC466 F19 Lab 6
#Sarah Bae, shbae@calpoly.edu
#Roxanne Miller, rmille60@calpoly.edu
#adjustWeightSum.py: python3 adjustWeightSum.py <userid> <itemid> <output csv filename>

import sys
import parser
import numpy as np

def cosSim(doc1, doc2):
    numer = 0
    denom1 = 0
    denom2 = 0

    numerArray = np.multiply(doc1, doc2)
    numer = np.sum(numerArray)

    denom1Array = np.power(doc1, 2)
    denom1 = np.sum(denom1Array)
    denom1 = np.sqrt(denom1)

    denom2Array = np.power(doc2, 2)
    denom2 = np.sum(denom2Array)
    denom2 = np.sqrt(denom2)

    return numer / (denom1 * denom2)

def userAvgRating(ratings):
    return np.mean(ratings)

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

def adjustedWeightedSum(users, items, user, item):
    summation = 0
    normalFactor = 0
    
    for i in range(len(users)):
        if i == user.id or item.id not in users[i].ratedItems:
            continue
        else:
            secondUser = users[i]
            index, = np.where(user.ratedItems == item.id)
            if index:
                targetUserAvg = userAvgRating(np.delete(user.ratings, index))
            else: 
                targetUserAvg = userAvgRating(user.ratings)
            targetUserRatings, secondUserRatings = compareUsers(user, secondUser, item.id)
            similarity = cosSim(targetUserRatings, secondUserRatings)
            
            secondUserUtilityIndex, = np.where(secondUser.ratedItems == item.id)
            index, = np.where(secondUser.ratedItems == item.id)
            if index:
                secondUserAvg = userAvgRating(np.delete(secondUser.ratings, index))
            else: 
                secondUserAvg = userAvgRating(secondUser.ratings)
            secondUserUtility = secondUser.ratings[secondUserUtilityIndex] - secondUserAvg
            
            summation += similarity * secondUserUtility
            normalFactor += abs(similarity)

    return targetUserAvg + ((1 / normalFactor) * summation)

