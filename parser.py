#CSC466 F19 Lab 6
#Sarah Bae, shbae@calpoly.edu
#Roxanne Miller, rmille60@calpoly.edu
#parser.py: python3 parser.py <output csv file name>

import os
import re
import sys
import math
import numpy as np
from datetime import datetime
from scipy.sparse import coo_matrix

class Item:
    def __init__(self, id):
        self.id = id
        self.avgRating = 0
        self.invUserFreq = 0
        self.ratings = []
    def __repr__(self):
        return 'id:%d' % self.id

class User:
    def __init__(self, id, ratedItems=[], avgRating=0):
        self.id = id
        self.ratedItems = ratedItems
        self.avgRating = avgRating
    def __repr__(self):
        return 'id:%d' % self.id
    
# doc1 and doc2 are doc.frequencies arrays
def cosSim(doc1, doc2):
    numer = 0
    denom1 = 0
    denom2 = 0

    numerArray = np.multiply(doc1, doc2)
    numer = np.sum(numerArray)

    denom1Array = np.power(doc1, 2)
    denom1 = np.sum(denom1Array)
    denom1 = np.sqrt(denom1)

    denom2Array = np.power(doc2, 2)
    denom2 = np.sum(denom2Array)
    denom2 = np.sqrt(denom2)

    return numer / (denom1 * denom2)

def okapi(doc1, doc2):
    tot = 0
    normParam = 1.5
    docLenParam = 0.75
    for wordIndex in range(len(doc1)):
        if 0 == doc1[wordIndex] and 0 == doc2[wordIndex]:
            continue
        df = self.docFreq[wordIndex]
        idf = math.log((len(self.docs) - df + 0.5)/(df + 0.5))
        numerDoc1 = (normParam + 1) * doc1[wordIndex]
        denomDoc1 = normParam * (1 - docLenParam + docLenParam * (doc1.length/self.self.avgDL)) + doc1[wordIndex]
        numerDoc2 = (normParam + 1) * doc2[wordIndex]
        denomDoc2 = normParam * (1 - docLenParam + docLenParam * (doc2.length/self.self.avgDL)) + doc2[wordIndex]
        tot += (idf * (numerDoc1/denomDoc1) * (numerDoc2/denomDoc2))
    return tot

def convertToTfIdf(builder, documents, docFrequency):
    for doc in documents:
        for i in range(len(doc.frequencies)):
            doc.frequencies[i] = tf_idf(i, doc, docFrequency, len(documents))

def invUsrFreqAvgRating(users, items):
    for item in items:
        item.ratings = np.array(item.ratings).astype(np.float)
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
            usrRatings = string.strip("\n").split(",")
            num = int(usrRatings[0])
            usrRatings = usrRatings[1:] #ignore the first number, this is the number of ratings from current user
            row = np.array(list(map(float, usrRatings)))
            #print(f,"row: {row}")
            col_inds, = np.where(row!=99)
            #print(f"col inds: {col_inds}")
            X_col.extend(col_inds)
            #print(f"x col: {X_col}")
            X_row.extend([row_idx]*len(col_inds))
            #print(f"x row: {X_row}")
            X_data.extend(row[col_inds])

            user = User(id=row_idx, ratedItems=col_inds, avgRating=row[col_inds].mean())
            users.append(user)

            for item in col_inds:
                items[item].ratings.append(usrRatings[item])
    items = invUsrFreqAvgRating(users, items)

    print(" Starting to transform to a sparse matrix" + str(datetime.now()))
    matrix = coo_matrix((X_data, (X_row, X_col)), dtype=int)
    print("Finished transform to a sparse matrix " + str(datetime.now()))
    return matrix.tocsr(), users, items

def main():
    jokeCsv = './jester-data-1.csv'
    completeRatingsMatrix, users, items = toSparseMatrix(jokeCsv)
    print(completeRatingsMatrix)
    outfile = sys.argv[1]

if __name__ == '__main__':
    main()
