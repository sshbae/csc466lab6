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

def main():
    if len(sys.argv) < 4:
        print(f"Usage: python3 EvaluateCFRandom.py <Method: 1. meanUtil\n2. weightedSum\n3.adjWeightedSum\n4. knnMeanUtil\n Size Repeats")
    #jokeCsv = './jester-data-1.csv'
    #completeRatingsMatrix, users, items = parser.toSparseMatrix(jokeCsv)
    #print(completeRatingsMatrix)
    #userId = int(sys.argv[1])
    #itemId = int(sys.argv[2])
    #user = users[userId]
    #item = items[itemId]

    #index, = np.where(user.ratedItems == itemId)
    #if index:
    #    actual = user.ratings[index]
    #    #changedUser = User(user.id, np.delete(user.ratedItems, index), np.delete(user.ratings, index))
    #    #changedUser.avgRating = np.sum(changedUser.ratings)/len(changedUser.ratings)
    #    itemRatings = np.delete(item.ratings, index)

    #method = sys.argv[3]
    #if method == 'meanUtil':
    #    predictedRating = np.sum(itemRatings)/len(itemRatings) if index else item.avgRating
    #elif method == 'weightedSum':
    #    predictedRating = None
    #elif method == 'adjWeightedSum':
    #    predictedRating = None
    #elif method =='avgKnn':
    #    k = int(sys.argv[4])
    #    predictedRating = knnFiltering.avgKnn(k, users, items, user, item)
    #else:
    #    exit()



if __name__ == '__main__':
    main()
