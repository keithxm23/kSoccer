from utils import *
from node import Node
from math import log, exp, sqrt
import sys
import operator

cntr = 0
featsUsed = {}

def buildTree(node, leftLabel, headers):
    if node.data == []:
        return None
    
    global featsUsed
    featureIndex, dataPointIndex, error, lr = getBestSplit(node, leftLabel)
    if headers[featureIndex] in featsUsed:
        featsUsed[headers[featureIndex]] += 1
    else:
        featsUsed[headers[featureIndex]] = 1
        
    prevError = node.splitError
    node.featureIndex = featureIndex
    node.dataPointIndex = dataPointIndex
    node.splitError = error

    
        
    if type(dataPointIndex) == type(''):#check if the datapoint at which we split is a string(discrete label) or int
        node.thresh = dataPointIndex
        
        node = updateDiscrete(node, featureIndex, node.thresh,leftLabel, lr)
    else:
        node.thresh = node.data[dataPointIndex][featureIndex]
        
        node = updateContinuous(node, featureIndex, node.thresh,leftLabel, lr)
        
        
    global cntr
    cntr+=1
#    print str(error)+"\t"+str(cntr)
    if prevError != None:
        if abs(error - prevError) <= 0.0000001 or cntr > 50:
#        if abs(error - prevError) <= 0.00001:
#        if cntr > 40:
#            print cntr
            cntr = 0
            print sorted(featsUsed.iteritems(), key=operator.itemgetter(1), reverse = True)
            return node
        
    if error == 0.5:
        print sorted(featsUsed.iteritems(), key=operator.itemgetter(1), reverse = True)
        return node
    
    return buildTree(node, leftLabel, headers)

def predict(data, splits, leftLabel):
#    LEGEND for splits:[0]=featureIndex [1]=featureLabel    [2]=alpha   [3]=leftLabel
    temp = []
    count = 0
    tp = tn = fp = fn = 0
    for x in data:
        asum = 0
        for s in splits:
            if (type(s[1]) == type('') and x[s[0]] == s[1]) or (type(s[1]) == type(1.0) and x[s[0]] < s[1]):#left branch
                if len(splits) == 4 or s[4] == 'left':
                    asum += s[2]
                else:
                    asum -= s[2]
            else:
                if len(splits) == 4 or s[4] == 'left':
                    asum -= s[2]
                else:
                    asum += s[2]
                
                    
#        if sum < 0:# and x[-2]=='r':
        count+=1
#        print str(asum) +"\t"+ x[-2]+"\t"+"\t"+str(count)
            
        if (x[-2] != leftLabel and asum < 0):
            tn+=1
        if (x[-2] ==  leftLabel and asum > 0):
            tp+=1
        if (x[-2] ==  leftLabel and asum < 0):
            fn+=1
        if (x[-2] !=  leftLabel and asum > 0):
            fp+=1
        temp.append(asum)
        
#    print leftLabel, str(float(tp+tn)/len(data)), tp, tn,fn,fp
    return temp
                
                
            
        
        
#Split a node on best feature-threshold pair and returns the feature and datapoint 
#indices to split on and the error-value of the split
def getBestSplit(node,leftLabel):
    minErrorSeen = float("inf")
    minFeatureIndex = None
    minThreshIndex = None
    minlr = None
    #looping over each feature (-1 for the last column which is label) and another -1 since we've 
    # added the Dt as the last column
    for i in xrange(len(node.data[0])-1-1):
        try:
            #feature list contains some labels
            if any('' in s for s in column(node.data, i)):#checks if every element in a column is a string
                for s in set(column(node.data, i)):#looping over each different value
#                    if s!= '?':#do not create a split for '?' i.e. missing data labels
                    if True:#realized that we get better results if we split on the ? too
                        thisError, lr = getDiscreteSplitError(i, s, node.data,leftLabel)
                        if minErrorSeen > thisError:
                            minErrorSeen = thisError
                            minFeatureIndex = i
                            minThreshIndex = s
                            minlr = lr
                            
            else:
                raise TypeError
        
        except TypeError:
            #feature list contains only numbers
#            node.data = sorted(node.data, key=lambda x:float(x[i]))
            for j in xrange(len(node.data)):#looping over each data point
                thisError, lr = getSplitError(i, j, node.data,leftLabel)
                if minErrorSeen > thisError:
                    minErrorSeen = thisError
                    minFeatureIndex = i
                    minThreshIndex = j
                    minlr = lr
                    
    return minFeatureIndex, minThreshIndex, minErrorSeen, minlr



def updateDiscrete(node, featureIndex, featureLabel,leftLabel,lr):
    try:
        alpha = 0.5*log((1.0-node.splitError)/node.splitError)
    except ZeroDivisionError:
        alpha = float("inf")
    z = 2.0*sqrt(node.splitError*(1.0-node.splitError))
#    lData = [x for x in node.data if x[featureIndex] == featureLabel]
#    leftLabel = most_common(column(lData,-2))
    for x in xrange(0,len(node.data)):
        try:
            
            if node.data[x][featureIndex] == featureLabel:#leftData
                if lr == 'left':
                    if node.data[x][-2] != leftLabel:
                        node.data[x][-1] *= exp(alpha)/z
                    else:
                        node.data[x][-1] *= exp(-1.0*alpha)/z
                else:
                    if node.data[x][-2] != leftLabel:
                        node.data[x][-1] *= exp(-1.0*alpha)/z
                    else:
                        node.data[x][-1] *= exp(alpha)/z
                    
            else:#rightData
                if lr == 'left':
                    if node.data[x][-2] == leftLabel:
                        node.data[x][-1] *= exp(alpha)/z
                    else:
                        node.data[x][-1] *= exp(-1.0*alpha)/z
                else:
                    if node.data[x][-2] == leftLabel:
                        node.data[x][-1] *= exp(-1.0*alpha)/z
                    else:
                        node.data[x][-1] *= exp(alpha)/z
        except ZeroDivisionError:
                        node.data[x][-1] = 0
                
    node.splits.append((featureIndex, node.thresh, alpha, leftLabel, lr))
    return node

def updateContinuous(node, featureIndex, featureLabel,leftLabel,lr):
    try:
        alpha = 0.5*log((1.0-node.splitError)/node.splitError)
    except ZeroDivisionError:
        alpha = float('inf')
    z = 2.0*sqrt(node.splitError*(1.0-node.splitError))
#    lData = [x for x in node.data if x[featureIndex] < featureLabel]
#    
#    leftLabel = most_common(column(lData,-2))
#    leftLabel = '+'
    
    for x in xrange(0,len(node.data)):
        try:
            if node.data[x][featureIndex] < featureLabel:#leftData
                
                if lr == 'left':             
                    if node.data[x][-2] != leftLabel:
                        node.data[x][-1] *= exp(alpha)/z
                    else:
                        node.data[x][-1] *= exp(-1*alpha)/z
                else:#lr=='right'
                    if node.data[x][-2] != leftLabel:
                        node.data[x][-1] *= exp(-1*alpha)/z
                    else:
                        node.data[x][-1] *= exp(alpha)/z
            else:#rightData
                if lr=='left':
                    
                    if node.data[x][-2] == leftLabel:
                        node.data[x][-1] *= exp(alpha)/z
                    else:
                        node.data[x][-1] *= exp(-1*alpha)/z
                else:#lr=='right'
                    if node.data[x][-2] == leftLabel:
                        node.data[x][-1] *= exp(-1*alpha)/z
                    else:
                        node.data[x][-1] *= exp(alpha)/z
        except ZeroDivisionError:
            node.data[x][-1] = 0
                
    node.splits.append((featureIndex,node.thresh, alpha, leftLabel, lr))
    return node
    
#dataPointIndex is the index after sorting data by that feature
def getSplitError(featureIndex, dataPointIndex, data, leftLabel):
#    data = sorted(data, key=lambda x:float(x[featureIndex]))
#    lData, rData = splitHorizontal(dataPointIndex, data)
    lData = [x for x in data if x[featureIndex] < data[dataPointIndex][featureIndex]]
    rData = [x for x in data if x[featureIndex] >= data[dataPointIndex][featureIndex]]
    assert(len(lData)+len(rData)==len(data))
    leftErr = sum([x[-1] for x in lData if x[-2] != leftLabel])
    rightErr = sum([x[-1] for x in rData if x[-2] == leftLabel])
    
    leftErr2 = sum([x[-1] for x in lData if x[-2] == leftLabel])
    rightErr2 = sum([x[-1] for x in rData if x[-2] != leftLabel])
    
    if (leftErr+rightErr < leftErr2+rightErr2):
        return leftErr + rightErr, 'left'
    else:
        return leftErr2 + rightErr2, 'right'
    
    return leftErr + rightErr

def getDiscreteSplitError(featureIndex, label, data, leftLabel):
    lData = [x for x in data if x[featureIndex] == label]
    rData = [x for x in data if x[featureIndex] != label]# and x[featureIndex] != '?']
    assert(len(lData)+len(rData)==len(data))
    leftErr = sum([x[-1] for x in lData if x[-2] != leftLabel])
    rightErr = sum([x[-1] for x in rData if x[-2] == leftLabel])
    
    leftErr2 = sum([x[-1] for x in lData if x[-2] == leftLabel])
    rightErr2 = sum([x[-1] for x in rData if x[-2] != leftLabel])
    
    if (leftErr+rightErr < leftErr2+rightErr2):
        return leftErr + rightErr, 'left'
    else:
        return leftErr2 + rightErr2, 'right'
    
