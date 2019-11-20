#CSC466 F19 Lab 6
#Sarah Bae, shbae@calpoly.edu
#Roxanne Miller, rmille60@calpoly.edu
#weightedSum.py: python3 weightedSum.py <userid> <itemid> <output csv filename>

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

def compareUsers(targetUser, secondUser, itemId):
    targetUserItems = targetUser.ratedItems[targetUser.ratedItems != itemId]
    matchingItems = np.intersect1d(targetUserItems, secondUser.ratedItems)
    targetUserItems = np.take(targetUser.ratings, matchingItems)
    secondUserItems = np.take(secondUser.ratings, matchingItems)

def weightedSum(userId, itemId, users, items):
    targetUser = users[userId]
    targetItem = items[itemId]
    for i in range(len(users)):
        if i == userId:
            continue
        else:
            targetUserRatings, secondUserRatings = compareUsers(targetUser, users[i], itemId)

def main():
    jokeCsv = './jester-data-1.csv'
    completeRatingsMatrix, users, items = parser.toSparseMatrix(jokeCsv)
    # print(completeRatingsMatrix)
    userId = int(sys.argv[1])
    itemId = int(sys.argv[2])

    outfile = sys.argv[3]



if __name__ == '__main__':
    main()