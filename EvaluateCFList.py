#CSC466 F19 Lab 6
#Sarah Bae, shbae@calpoly.edu
#Roxanne Miller, rmille60@calpoly.edu
'''
EvaluateCFList.py: python3 EvaluateCFList.py <int method: 1. meanUtil
                                                        2. weightedSum
                                                        3. adjWeightedSum
                                                        4. knnMeanUtil
                                                        >
                                           <filename of uiPairs>
'''

import sys
import parser
import numpy as np
import knnFiltering
import weightedSum
import adjustWeightSum

def usageErr():
        print(f"Usage: python3 EvaluateCFRandom.py <Method: 1. meanUtil 2. weightedSum 3.adjWeightedSum 4. knnMeanUtil>\n\t\t\t\t\t<filename of uiPairs")

def MAE(deltas):
    residuals = np.absolute(deltas))
    return np.sum(residuals)/deltas.size

def getPrediction(method, users, items, user, item):
    if method == 1:
        index, = np.where(user.ratedItems == itemId)
        if index:
            actual = user.ratings[index]
            itemRatings = np.delete(item.ratings, index)
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
    return actual, predictedRating
    

def isValid(users, pair):
    if pair[1] in users[pair[0]].ratedItems:
        return True
    return False


def main():
    if len(sys.argv) < 3:
        usageErr()
        exit()
    jokeCsv = './jester-data-1.csv'
    completeRatingsMatrix, users, items = parser.toSparseMatrix(jokeCsv)

    method = int(sys.argv[1])
    uiPairsFile = open(sys.argv[2], "r")
    #userItemPairs = [(1, 2), (3, 4), (0, 0)]

    f = open('outList.csv', 'w+')
    f.write("userID, itemID, Actual_Rating, Predicted_Rating, Delta_Rating\n")

    userIds = []
    itemIds = []
    predictions = []
    actuals = []
    deltas = []

    for pair in userItemPairs:
        if isValid(users, pair):
            user = users[pair[0]]
            userIds.append(user)
            itemIds.append(pair[1])

            predictedRating = getPrediction(method, users, items, user, items[pair[1]])
            predictions.append(predictedRating)
            
            actualIndex, = np.where(user.ratedItems == pair[1])
            actualRating = user.ratings[actualIndex]
            actuals.append(actualRating)

            deltas.append(abs(predictedRating - actualRating))

    for i in range(userItemPairs.size):
        f.write(f"{userItemPairs[i][0]},{userItemPairs[i][1]},{actuals[i]},{predictions[i]},{deltas[i]}\n")
    f.write(f"{MAE(np.array(deltas)}")
    f.close()

if __name__ == '__main__':
    main()
