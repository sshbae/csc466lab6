#CSC466 F19 Lab 6
#Sarah Bae, shbae@calpoly.edu
#Roxanne Miller, rmille60@calpoly.edu
#meanUtilityFiltering.py: python3 meanUtilityFiltering.py

import sys
import parser
import numpy as np

def mean_util(score, user, item, users, items):
    if score == 99:
        predict()
    else:
        real = score
        index, = np.where(user.ratedItems == itemId)
        users[user.id].ratings[index] = 99

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

    if (score == 99):


if __name__ == '__main__':
    main()
