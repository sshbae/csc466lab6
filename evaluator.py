#CSC466 F19 Lab 6
#Sarah Bae, shbae@calpoly.edu
#Roxanne Miller, rmille60@calpoly.edu
#weightedSum.py: python3 weightedSum.py <userid> <itemid> <output csv filename>
import pandas as pd
import numpy as np

def evaluatePredictions(predictions, actuals):
    predRecommendations = []
    actualRecommendations = []

    for i in range(len(predictions)):
        if predictions[i] >= 5:
            predRecommendations.append("recommend")
        else:
            predRecommendations.append("dont_recommend")
        
        if actuals[i] >= 5:
            actualRecommendations.append("recommend")
        else:
            actualRecommendations.append("dont_recommend")

    confusionMatrix = pd.crosstab(np.array(predRecommendations), np.array(actualRecommendations))
    
    col_diffs = set(predRecommendations) - set(actualRecommendations)
    row_diffs = set(actualRecommendations) - set(predRecommendations)
    
    for col in col_diffs:
        confusionMatrix[col] = 0
    for row in row_diffs:
        new_row = np.zeros(confusionMatrix.shape[1])
        confusionMatrix.loc[row] = new_row

    diagonal = pd.Series(np.diag(confusionMatrix), index=[confusionMatrix.index, confusionMatrix.columns])

    for index, row in confusionMatrix.iterrows():
        recall = row[index] / row.sum() if row.sum() > 0 else 0
        precision = row[index] / confusionMatrix[index].sum()
        denoma = 1 / recall if recall > 0 else 0
        denomb = 1 / precision if precision > 0 else 0
        fMeasure = 2 / denoma + denomb if denoma > 0 or denomb > 0 else 0

        falsePositives = confusionMatrix[index].sum() - row[index]
        trueNegatives = diagonal.sum() - row[index]

        print("Recall for %s: %f" % (index, recall))
        print("Precision for %s: %f" % (index, precision))
        print("F Measure for %s: %f" % (index, fMeasure))
    
    overallAccuracy = diagonal.sum() / len(predRecommendations)
    correct = 0
    incorrect = 0
    for i in range(len(predRecommendations)):
        if predRecommendations[i] == actualRecommendations[i]:
            correct += 1
        else: 
            incorrect += 1

    print()
    print("Overall Correct Predictions: %d" % correct)
    print("Overall Incorrect Predictions: %d" % incorrect)
    print("Overall Accuracy: %f" % overallAccuracy)

    print(confusionMatrix)
