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

def MAE(predictions, actuals):
    residuals = np.absolute(np.subtract(predictions, actuals))
    return np.sum(residuals)/predictions.size

def check(candidateUIPairs, users):
    for i, uiPair in enumerate(candidateUIPairs):
        userId = uiPair[0]
        itemId = uiPair[1]
        index, = np.where(users[userId]].ratedItems == itemId)
        if not index:
            candidateUIPairs = np.delete(candidateUIPairs, i)

    return candidateUIPairs

#do we ever need to check if it exists? the program makes sure it only ever recieves existing ratings
def evaluate(method, users, items, user, item):
    index, = np.where(user.ratedItems == itemId)
    if index:
        actual = user.ratings[index]
        itemRatings = np.delete(item.ratings, index)

    if method == 1:
        predictedRating = np.sum(itemRatings)/len(itemRatings) if index else item.avgRating
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

def main():
    if len(sys.argv) < 4:
        usageErr()
        exit()
    jokeCsv = './jester-data-1.csv'
    completeRatingsMatrix, users, items = parser.toSparseMatrix(jokeCsv)

    size = int(sys.argv[2])
    repeats = int(sys.argv[3])

    uiPairs = []
    while (len(uiPairs) < size):
        candidateUIPairs = np.random.randint(0,100, (size, 2))
        uiPairs.extend(check(candidateUIPairs, users))
    uiPairs = np.array(uiPairs)

    method = int(sys.argv[1])
    predictions = []
    for uiPair in uiPairs:
        userId = uiPair[0]
        itemId = uiPair[1]
        predictions.append(evaluate(method, users, items, users[userId], items[itemId]))


if __name__ == '__main__':
    main()
