from utils import openfile, column
from node import Node
from tree import buildTree, predict
import copy

train = []
contents = openfile("car/car.data")
for line in contents:
    train.append(line.split()+[1.0/len(contents)])
    
#numericFeatures = [1,2,7,10,13,14]#For crx dataset
#featureMean = {}
#for n in numericFeatures:
#    col = column(train,n)
#    csum = 0
#    z = 0
#    for c in col:
#        if c != '?':
#            csum += float(c)
#            z+= 1
#    featureMean[str(n)] = csum/z
    
#for x in train:
#    for y in xrange(0,len(x)-1):
#        if y in numericFeatures:
#            if x[y] != '?':
#                x[y] = float(x[y])
#            else:
#                x[y] = featureMean[str(y)]
    
results = []    
#for x in set(column(train,-2)):
#carlabels = ['u']#['a','u','g','v']
carlabels = ['a','u','g','v']
for x in carlabels:#specific to car dataset
    temptrain = copy.deepcopy(train)
    rootNode = Node(temptrain)
    treeRootNode = buildTree(rootNode, x)
    results.append(predict(temptrain, rootNode.splits, x))

prediction = []
for x in xrange(0,len(results[0])):
    temp = [y for y in column(results, x)]
    prediction.append(carlabels[temp.index(max(temp))])


#for i in xrange(0,len(results[0])):
#    print i, column(results,i)


corr = 0
for x in xrange(0,len(prediction)):
    if prediction[x] == column(train,-2)[x]:
        corr+=1
print float(corr)/len(prediction)
#    
a=1