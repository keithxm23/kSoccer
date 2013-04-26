from utils import openfile, column
from node import Node
from tree import buildTree, predict
import copy, random, time
from math import ceil
import csv

def adaboost(train, test, headers, fullTestData):
    ylabels = ['H', 'A', 'D']
    results = []
    for y in ylabels:
#        print "Training for", y
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
    file = open("resultdata.csv", 'a')
    writer = csv.writer(file, quoting=csv.QUOTE_ALL)
    for p in xrange(0,len(prediction)):
        writer.writerow([column(fullTestData,-2)[p], column(fullTestData,-1)[p], prediction[p], column(test,-2)[p], column(fullTestData,-4)[p]]) 
        print [column(fullTestData,-2)[p], column(fullTestData,-1)[p], prediction[p], column(test,-2)[p], column(fullTestData,-4)[p]]
        if prediction[p] == column(test,-2)[p]:
            corr+=1
    
    file.close()
    try:
        print str(float(corr)*100/len(prediction)), len(prediction)
    except ZeroDivisionError:
        print 0, len(prediction)
    print "done"