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
        idf = np.log((len(self.docs) - df + 0.5)/(df + 0.5))
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
