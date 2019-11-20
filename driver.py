#CSC466 F19 Lab 6
#Sarah Bae, shbae@calpoly.edu
#Roxanne Miller, rmille60@calpoly.edu
#driver.py: python3 driver.py <user id (0-99)> <item id (0-99)> <method: meanUtil, >

import sys
import parser
import numpy as np
import knnFiltering

def main():
    jokeCsv = './jester-data-1.csv'
    completeRatingsMatrix, users, items = parser.toSparseMatrix(jokeCsv)
    print(completeRatingsMatrix)
    userId = int(sys.argv[1])
    itemId = int(sys.argv[2])
    user = users[userId]
    item = items[itemId]
    print(type(user.ratedItems))
    print(f"item is {item}")
    print(f"index is {index}")
    print(f"user rated items is {user.ratedItems}")
    print(f"user ratings is {user.ratings}")

    index, = np.where(user.ratedItems == itemId)
    if index:
        actual = user.ratings[index]
        #changedUser = User(user.id, np.delete(user.ratedItems, index), np.delete(user.ratings, index))
        #changedUser.avgRating = np.sum(changedUser.ratings)/len(changedUser.ratings)
        itemRatings = np.delete(item.ratings, index)

    method = sys.argv[3]
    switch(method):
        case 'meanUtil':
            predictedRating = np.sum(itemRatings)/len(itemRatings) if index else item.avgRating
        case 'weightedSum':
            predictedRating = 
        case 'adjWeightedSum':
            predcitedRating = 
        case 'avgKnn':
            predictedRating = knnFiltering.avgKnn(users, items)



if __name__ == '__main__':
    main()
