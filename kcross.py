from utils import openfile, column
from node import Node
from tree import buildTree, predict
import copy, random, time
from math import ceil

def adaboost(train, test, headers, fullTestData):
    ylabels = ['H', 'A', 'D']
    results = []
    for y in ylabels:
        print "Training for", y
        rootNode = Node(train)
        treeRootNode = buildTree(rootNode, y, headers)
        results.append(predict(test, rootNode.splits, y))
    
    print "Now making predictions"    
    prediction = []
    for r in xrange(0,len(results[0])):
        temp = [zy for zy in column(results, r)]
        prediction.append(ylabels[temp.index(max(temp))])
        
    print "Now checking predictions"
    corr = 0
    print "Home\tAway\tPrediction\tActual\tBookie"
    for p in xrange(0,len(prediction)):
        print column(fullTestData,-2)[p], column(fullTestData,-1)[p], prediction[p], column(test,-2)[p], column(fullTestData,-4)[p], 
        if prediction[p] == column(test,-2)[p]:
            corr+=1
    
    print str(float(corr)*100/len(prediction))
        
    print "done"