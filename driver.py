#CSC466 F19 Lab 6
#Sarah Bae, shbae@calpoly.edu
#Roxanne Miller, rmille60@calpoly.edu
#driver.py: python3 driver.py <user id (0-99)> <item id (0-99)> <method: meanUtil, >

import sys
import parser
import numpy as np
import knnFiltering
import weightedSum
import adjustWeightSum

def main():
    jokeCsv = './jester-data-1.csv'
    completeRatingsMatrix, users, items = parser.toSparseMatrix(jokeCsv)
    #print(completeRatingsMatrix)
    userId = int(sys.argv[1])
    itemId = int(sys.argv[2])
    user = users[userId]
    item = items[itemId]

    index, = np.where(user.ratedItems == itemId)
    if index:
        actual = user.ratings[index]
        #changedUser = User(user.id, np.delete(user.ratedItems, index), np.delete(user.ratings, index))
        #changedUser.avgRating = np.sum(changedUser.ratings)/len(changedUser.ratings)
        itemRatings = np.delete(item.ratings, index)

    method = sys.argv[3]
    if method == 'meanUtil':
        predictedRating = np.sum(itemRatings)/len(itemRatings) if index else item.avgRating
    elif method == 'weightedSum':
        predictedRating = weightedSum.weightedSum(users, items, user, item)
    elif method == 'adjWeightSum':
        predictedRating = adjustWeightSum.adjustedWeightedSum(users, items, user, item)
    elif method =='avgKnn':
        k = int(sys.argv[4])
        predictedRating = knnFiltering.avgKnn(k, users, items, user, item)
    else:
        exit()

    print(f"predicted rating: {predictedRating}")


if __name__ == '__main__':
    main()
