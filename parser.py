#CSC466 F19 Lab 6
#Sarah Bae, shbae@calpoly.edu
#Roxanne Miller, rmille60@calpoly.edu
#parser.py: python3 parser.py

import numpy as np
from scipy.sparse import coo_matrix, csr_matrix

class Item:
    def __init__(self, id):
        self.id = id
        self.avgRating = 0
        self.invUserFreq = 0
        self.ratings = []
    def __repr__(self):
        return f'Item:{self.id}, avgRating:{self.avgRating}, invUserFreq:{self.invUserFreq}\n'

class User:
    def __init__(self, id, ratedItems=[], ratings = [], avgRating=0):
        self.id = id
        self.ratedItems = ratedItems
        self.ratings = ratings
        self.avgRating = avgRating
    def __repr__(self):
        return f'User:{self.id}, avgRating:{self.avgRating}\n'
    
def invUsrFreqAvgRating(users, items):
    for item in items:
        item.ratings = np.array(item.ratings)
        item.invUserFreq = np.log2(item.ratings.size/len(users))
        item.avgRating = np.mean(item.ratings)
    return items

#using sparse matrix constructor from
#https://stackoverflow.com/questions/32368667/python-the-best-way-to-read-a-sparse-file-into-a-sparse-matrix?rq=1
def toSparseMatrix(jokeCsv):
    X_data = []
    X_row, X_col = [], []
    users = []
    items = [Item(i) for i in range(100)]

    with open(jokeCsv, "r") as f:
        for row_idx, string in enumerate(f.readlines()):
            row = string.strip("\n").split(",")
            row = row[1:] #ignore the first number, this is the number of ratings from current user
            usrRatings = np.array(list(map(float, row)))
            col_inds, = np.where(usrRatings!=99)

            X_col.extend(col_inds)
            X_row.extend([row_idx]*len(col_inds))
            X_data.extend(usrRatings[col_inds])

            user = User(id=row_idx, ratedItems=col_inds, ratings = usrRatings[col_inds], avgRating=usrRatings[col_inds].mean())
            users.append(user)

            for item in col_inds:
                items[item].ratings.append(usrRatings[item])
    items = invUsrFreqAvgRating(users, items)
    matrix = coo_matrix((X_data, (X_row, X_col)), dtype=float)
    return matrix, users, items

def main():
    jokeCsv = './jester-data-1.csv'
    matrix, users, items = toSparseMatrix(jokeCsv)

if __name__ == '__main__':
    main()
