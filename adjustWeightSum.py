#CSC466 F19 Lab 6
#Sarah Bae, shbae@calpoly.edu
#Roxanne Miller, rmille60@calpoly.edu
#adjustWeightSum.py: python3 adjustWeightSum.py <userid> <itemid> <output csv filename>

import sys
import parser
import numpy as np

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

    return matchingItems, targetUserRatings, secondUserRatings

def adjustedWeightedSum(users, items, user, item, simMeasure):
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
            matchingItems, targetUserRatings, secondUserRatings = compareUsers(user, secondUser, item.id)
            similarity = simMeasure(matchingItems, items, targetUserRatings, secondUserRatings)
            
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

