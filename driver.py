#CSC466 F19 Lab 6
#Sarah Bae, shbae@calpoly.edu
#Roxanne Miller, rmille60@calpoly.edu
#driver.py: python3 driver.py <user id (0-99)> <item id (0-99)> <method: meanUtil, >

import sys
import parser
import numpy as np
import meanUtilityFiltering

def mean_util

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
    index, = np.where(user.ratedItems == itemId)
    print(f"index is {index}")
    print(f"user rated items is {user.ratedItems}")
    print(f"user ratings is {user.ratings}")
    score = user.ratings[index]

    method = sys.argv[3]

    switch(method):
        case 'meanUtil':
            meanUtilityFiltering.meanUtil(score, user, item, users, items)



if __name__ == '__main__':
    main()
