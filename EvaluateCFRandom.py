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

def main():
    if len(sys.argv) < 4:
        usageErr()
        exit()
    jokeCsv = './jester-data-1.csv'
    completeRatingsMatrix, users, items = parser.toSparseMatrix(jokeCsv)

    size = int(sys.argv[2])
    repeats = int(sys.argv[3])

    uiPairs = []
    np.random.randint(0,100)
    while (len(uiPairs) < size):
        candidates = np.random.randint(0,100, (size, 2))
        uiPairs.concatenate(check(candidates))

   # userId = int(sys.argv[1])
   # itemId = int(sys.argv[2])
    user = users[userId]
    item = items[itemId]

    index, = np.where(user.ratedItems == itemId)
    if index:
        actual = user.ratings[index]
        itemRatings = np.delete(item.ratings, index)

    method = int(sys.argv[1])
    if method == 1:
        predictedRating = np.sum(itemRatings)/len(itemRatings) if index else item.avgRating
    elif method == 2:
        predictedRating = weightedSum.weightedSum(users, items, user, item)
    elif method == 3:
        predictedRating = adjustWeightSum.adjustedWeightedSum(users, items, user, item)
    elif method == 4:
        k = int(sys.argv[4])
#TODO i think u mightve forgotten to omit the rating if it doesnt exist
        predictedRating = knnFiltering.avgKnn(k, users, items, user, item)
    else:
        usageErr()
        exit()



if __name__ == '__main__':
    main()
