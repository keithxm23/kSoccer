from __future__ import division
from operator import itemgetter
import itertools
import operator

def openfile(fname):
    with open(fname) as f:
        content = f.readlines()
    return content


#http://stackoverflow.com/a/1520716/1415352
def most_common(L):
  groups = itertools.groupby(sorted(L))
  def _auxfun((item, iterable)):
    return len(list(iterable)), -L.index(item)
  return max(groups, key=_auxfun)[0]
  
  
def getMatrixFromTxtFile(filename):
    f = open(filename);
    matrix = []
    for line in f.readlines():
        matrix.append([float(value) for value in line.split()])
    f.close()
    return matrix

#Get column i of matrix
def column(matrix, i):
    return map(itemgetter(i), matrix)

def transpose(matrix):
    return map(list, zip(*matrix))

#splits matrix at rowindex (note: the row corresponding to rowindex is included in the bottom split
def splitHorizontal(rowindex, matrix):
    topData = []
    bottomData = []
    for i in xrange(0,rowindex):
        topData.append(matrix[i])
    for i in xrange(rowindex, len(matrix)):
        bottomData.append(matrix[i])
    return topData, bottomData

def mean(array):
    try:
        return sum(array)/float(len(array))
    except ZeroDivisionError:
        return 0.0
    
def MSE(labels):
    try:
        meanval = mean(labels)
        err = 0.0
        for l in labels:
            err += pow((meanval-l),2.0)
        err /= len(labels)
        return err
    except ZeroDivisionError:
        return 0.0
    
    
def getError(labels,predictions):
    error = 0.0
    for l,p in zip(labels, predictions):
        error += pow((l-p),2)
    error /= float(len(labels))
    return error
    
#Other methods you may want to use that are already built into python

#Sort matrix by column i in ascending
#sorted(matrix, key=lambda x:float(x[i]))

