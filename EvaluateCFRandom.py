#CSC466 F19 Lab 6
#Sarah Bae, shbae@calpoly.edu
#Roxanne Miller, rmille60@calpoly.edu
'''
EvaluateCFRandom.py: python3 EvaluateCFRandom.py <int method: 1. meanUtil
                                                            2. weightedSum
                                                            3. adjWeightedSum
                                                            4. knnMeanUtil
                                                >
                                               <int size>
                                               <int repeats>
'''

import sys
import parser
import numpy as np
import knnFiltering
import weightedSum
import adjustWeightSum

def usageErr():
        print(f"Usage: python3 EvaluateCFRandom.py <Method: 1. meanUtil 2. weightedSum 3.adjWeightedSum 4. knnMeanUtil>\n\t\t\t\t\t<Size>\n\t\t\t\t\t<Repeats>")

def MAE(deltas):
    residuals = np.absolute(deltas)
    return np.sum(residuals)/deltas.size

def check(candidateUIPairs, users):
    j = 0
    uiPairs = candidateUIPairs.copy()
    for i, uiPair in enumerate(candidateUIPairs):
        userId = uiPair[0]
        itemId = uiPair[1]
        index, = np.where(users[userId].ratedItems == itemId)
        if index.size == 0:
            uiPairs = np.delete(uiPairs, j, axis=0)
            j -= 1
        j += 1
    return uiPairs

def getPrediction(method, users, items, user, item):
    index, = np.where(user.ratedItems == item.id)
    actual = user.ratings[index]
    if method == 1:
        itemRatings = np.delete(item.ratings, index)
        predictedRating = np.sum(itemRatings)/len(itemRatings)
    elif method == 2:
        predictedRating = weightedSum.weightedSum(users, items, user, item)
    elif method == 3:
        predictedRating = adjustWeightSum.adjustedWeightedSum(users, items, user, item)
    elif method == 4:
        k = int(sys.argv[4])
        predictedRating = knnFiltering.avgKnn(k, users, items, user, item)
    else:
        usageErr()
        exit()
    return actual[0], predictedRating

def main():
    if len(sys.argv) < 4:
        usageErr()
        exit()
    jokeCsv = './jester-data-1.csv'
    completeRatingsMatrix, users, items = parser.toSparseMatrix(jokeCsv)

    size = int(sys.argv[2])
    repeats = int(sys.argv[3])

    f = open('outRandom.csv', 'w+')
    f.write("userID,itemID,Actual_Rating,Predicted_Rating,Delta_Rating\n")

    MAEs = []
    for i in range(repeats):
        uiPairs = []
        while (len(uiPairs) < size):
            candidateUIPairs = np.random.randint(0,100, (size, 2))
            uiPairs.extend(check(candidateUIPairs, users))
        uiPairs = np.array(uiPairs[:size])

        method = int(sys.argv[1])
        predictions = []
        actuals = []
        deltas = []

        for uiPair in uiPairs:
            userId = uiPair[0]
            itemId = uiPair[1]
            actual, prediction = getPrediction(method, users, items, users[userId], items[itemId])
            actuals.append(actual)
            predictions.append(prediction)
            deltas.append(prediction - actual)
        deltas = np.array(deltas).flatten()
        MAEs.append(MAE(deltas))

        if method != 1:
            predictions = np.array(predictions).flatten()
            deltas = np.array(deltas).flatten()

        for i in range(size):
            f.write(f"{uiPairs[i][0]},{uiPairs[i][1]},{actuals[i]},{predictions[i]},{deltas[i]}\n")
    MAEs = np.array(MAEs)
    for mae in MAEs:
        f.write(f"{mae},")
    f.write(f"\n{np.sum(MAEs)/MAEs.size}")
    f.write(f"\n{np.sqrt(np.sum(np.power(MAEs, 2))/(MAEs.size - 1)) if MAEs.size > 1 else 0}")
    f.close()

    

if __name__ == '__main__':
    main()
