import csv, sys
#usage: python evalresults.py resultdata.csv "Man United"
file = open(sys.argv[1], 'rb')
fil = csv.reader(file, delimiter=',')

betrights = 0#betters got right
preds = 0#i got right
betpreds = 0#i got betters right
count = 0
for row in fil:
    print ','.join(row)
    count += 1
    if row[-1] == row[-2]:
        betrights += 1
    if row[-2] == row[-3]:
        preds += 1
    if row[-1] == row[-3]:
        betpreds += 1
file.close()
    
print betrights, 'Betters got right'
print preds, 'I got right'
print betpreds, 'Betters and I agree'
print count, 'Total points'

if len(sys.argv) > 2:
    print sys.argv[2], row[0]
    W = 0.0
    L = 0.0
    D = 0.0
    file = open(sys.argv[1], 'rb')
    fil = csv.reader(file, delimiter=',')
    for row in fil:
        if row[-2] == 'D':
            D+=1.0
        elif ((row[-2] == 'H' and row[0] == sys.argv[2])
              or (row[-2] == 'A' and row[1] == sys.argv[2])):
            W += 1.0
        else:
            L += 1.0
    
    print W, L, D
    print W*100.0/float(count), 'Wins'
    print L*100.0/float(count), 'Losses'
    print D*100.0/float(count), 'Draws'
        

