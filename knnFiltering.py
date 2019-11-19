#CSC466 F19 Lab 6
#Sarah Bae, shbae@calpoly.edu
#Roxanne Miller, rmille60@calpoly.edu
#knnFiltering.py: python3 knnFiltering.py <output csv filename>

import sys
import parser

def main():
    jokeCsv = './jester-data-1.csv'
    completeRatingsMatrix, users, items = parser.toSparseMatrix(jokeCsv)
    print(completeRatingsMatrix)
    outfile = sys.argv[1]

if __name__ == '__main__':
    main()
