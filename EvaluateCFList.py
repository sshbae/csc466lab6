#CSC466 F19 Lab 6
#Sarah Bae, shbae@calpoly.edu
#Roxanne Miller, rmille60@calpoly.edu
'''
EvaluateCFList.py: python3 EvaluateCFList.py <int method: 1. meanUtil
                                                        2. weightedSum
                                                        3. adjWeightedSumCosSim
                                                        4. adjWeightedSumPearsonCorr
                                                        5. knnMeanUtilCosSim
                                                        6. knnMeanUtilPearsonCorr
                                                        >
                                           <filename of uiPairs>
'''

import sys
import parser
import numpy as np
import knnFiltering
import weightedSum
import adjustWeightSum
import pandas as pd
import evaluator

def usageErr():
        print(f"Usage: python3 EvaluateCFRandom.py <Method: 1. meanUtil 2. weightedSum 3.adjWeightedSum(cosSim) 4. adjWeightedSum(PearsonCorr) 5. knnMeanUtil(cosSim) 6. knnMeanUtil(pearson)>"
        "\n\t\t\t\t\t<filename of uiPairs>")

def transform(userRatings, items, itemIds):
    for i in range(userRatings.size):
        userRatings[i] *= items[itemIds[i]].invUserFreq
    return userRatings

def pearsonCorr(itemIds, items, user1, user2):
    user1 = transform(user1, items, itemIds)
    user2 = transform(user2, items, itemIds)
    numer1Array = np.subtract(user1, np.full(user1.size, user1.mean()))
    numer2Array = np.subtract(user2, np.full(user2.size, user2.mean()))
    denom1 = np.sum(np.power(numer1Array, 2))
    denom2 = np.sum(np.power(numer2Array, 2))
    
    return (np.sum(numer1Array) * np.sum(numer2Array)) / (denom1 * denom2)

def cosSim(itemIds, items, user1, user2):
    user1 = transform(user1, items, itemIds)
    user2 = transform(user2, items, itemIds)
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

def MAE(deltas):
    residuals = np.absolute(deltas)
    return np.sum(residuals)/deltas.size

def getPrediction(method, users, items, user, item):
    index, = np.where(user.ratedItems == item.id)
    actual = user.ratings[index]
    if method == 1:
        itemRatings = np.delete(item.ratings, index)
        predictedRating = np.sum(itemRatings)/len(itemRatings) if index else item.avgRating
    elif method == 2:
        predictedRating = weightedSum.weightedSum(users, items, user, item)
    elif method == 3:
        predictedRating = adjustWeightSum.adjustedWeightedSum(users, items, user, item, cosSim)
    elif method == 4:
        predictedRating = adjustWeightSum.adjustedWeightedSum(users, items, user, item, pearsonCorr)
    elif method == 5:
        k = int(sys.argv[3])
        predictedRating = knnFiltering.avgKnn(k, users, items, user, item, cosSim)
    elif method == 6:
        k = int(sys.argv[3])
        predictedRating = knnFiltering.avgKnn(k, users, items, user, item, pearsonCorr)
    else:
        usageErr()
        exit()
    return actual[0], predictedRating
    

def isValid(users, pair):
    if pair[1] in users[pair[0]].ratedItems:
        return True
    return False

def getPairs(uiPairsFile):
    pairs = []
    df = pd.read_csv(uiPairsFile, header=None)
    for index, row in df.iterrows():
        pairs.append((row[0], row[1]))

    return pairs

def main():
    if len(sys.argv) < 3:
        usageErr()
        exit()
    jokeCsv = './jester-data-1.csv'
    completeRatingsMatrix, users, items = parser.toSparseMatrix(jokeCsv)

    method = int(sys.argv[1])
    uiPairsFile = open(sys.argv[2], "r")
    userItemPairs = np.array(getPairs(uiPairsFile))

    f = open('outList.csv', 'w+')
    f.write("userID,itemID,Actual_Rating,Predicted_Rating,Delta_Rating\n")

    userIds = []
    itemIds = []
    predictions = []
    actuals = []
    deltas = []

    for pair in userItemPairs:
        if isValid(users, pair):
            user = users[pair[0]]
            userIds.append(user.id)
            itemIds.append(pair[1])

            actualRating, predictedRating = getPrediction(method, users, items, user, items[pair[1]])
            predictions.append(predictedRating)
            actuals.append(actualRating)

            deltas.append(abs(predictedRating - actualRating))
    predictions = np.array(predictions).flatten()
    actuals = np.array(actuals).flatten()
    deltas = np.array(deltas).flatten()

    evaluator.evaluatePredictions(predictions, actuals)
    for i in range(len(userIds)):
        f.write(f"{userIds[i]},{itemIds[i]},{actuals[i]},{predictions[i]},{deltas[i]}\n")
    f.write(f"{MAE(np.array(deltas))}")
    f.write(f"\n{np.sqrt(np.sum(np.power(deltas, 2))/(deltas.size - 1))}")
    f.close()

if __name__ == '__main__':
    main()
