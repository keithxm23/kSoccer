import csv, sys

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
        
print betrights
print preds
print betpreds
print count

        

