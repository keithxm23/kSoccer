#!/usr/bin/python
from kparser import parseFolder
import cPickle as pickle, datetime
from featurefns import *
import csv
from utils import column, most_common

if __name__ == '__main__':
    try:
        teamdata = pickle.load( open( "teamdata.p", "rb" ) )
        matchdata = pickle.load( open( "matchdata.p", "rb" ) )
    except:
        teamdata, matchdata = parseFolder('footydata/epl')
        pickle.dump( teamdata, open( "teamdata.p", "wb" ) )
        pickle.dump( matchdata, open( "matchdata.p", "wb" ) )
        
    data = {}
    data['teamdata'] = teamdata
    data['matchdata'] = matchdata
    
#    for m in teamdata['Arsenal']: print m['Date'], m['HomeTeam'], m['HomePoints'], m['HomeMatches'], m['AwayTeam'],  m['AwayPoints'], m['AwayMatches']
 
    
#    print getRecentStats(data, date=datetime.date(2013,1,15),lastXGames = 10, team='Arsenal', stat='FTGoals')
#    print getRecentResults(data, date=datetime.date(2012,1,15),lastXGames = 10, team='Arsenal', result='Wins', location='Away')
#    print getRecentResults(data, date=datetime.date(2012,1,15),lastXGames = 10, team='Arsenal', result='Wins', location='All')
#
#    homeTeam = 'Arsenal'
#    awayTeam = 'Aston Villa'
#    matchDates, labels = getMatchDates(data, home=homeTeam, away=awayTeam, dateBefore=datetime.date(2012,1,15), monthsOld=18)
#    matchDates = [x['Date'] for x in data['matchdata']]
    
#    featureGenerator = getFeatureGenerator(home=homeTeam, away=awayTeam)
    
    #code to evaluate different betting agencies
    betkeys = []
    for m in matchdata:
        bk = [k for k in m.keys() if k.startswith('bet_')]
        betkeys += [k for k in bk if k not in betkeys]
    
    
    notcompletebetters = []
    for m in matchdata:
        for b in betkeys:
            if b not in m.keys() and b not in notcompletebetters:
                notcompletebetters.append(b)    
    
    
    betkeys = [k for k in betkeys if k not in notcompletebetters]
    betpreds = []
    for m in matchdata:
        tmp = []
        for b in betkeys:
            tmp.append(m[b])
        tmp.append(most_common(tmp))
        m['BetResult'] = most_common(tmp)
        tmp.append(m['FTR'])
        betpreds.append(tmp)
    data['matchdata'] = matchdata
    
    
    betkeys.append('MajorityBet')
    betkeys.append('Result')
        
    bfile = open("betters.csv", "wb")
    writer = csv.writer(bfile, quoting=csv.QUOTE_ALL)
    writer.writerow(betkeys)
    for tr in betpreds:
        writer.writerow(tr)
    bfile.close()
    
    #calculating accuracy of each
    count = [0 for x in betkeys]
    for bets in betpreds:
        for num, b in enumerate(bets):
            if b == bets[-1]:
                count[num]+=1
    
    
    
    try:
        traindata = pickle.load( open( "traindata.p", "rb" ) )
        headers = pickle.load( open( "headers.p", "rb" ) )
    except:
        traindata, headers = trainOnAll(data)
        pickle.dump( traindata, open( "traindata.p", "wb" ) )
        pickle.dump( headers, open( "headers.p", "wb" ) )
    
    
    #normalize features in training data
#    for x in xrange(len(traindata[0])-1):
#        minval = min(column(traindata,x))
#        if minval < 0:
#            for num, y in enumerate(column(traindata,x)):
#                traindata[num][x] = y - minval
    
    
    ofile = open("traindataArsEve.csv", 'wb')
    writer = csv.writer(ofile, quoting=csv.QUOTE_ALL)
    
    writer.writerow(headers)
    for tr in traindata:
        writer.writerow(tr)
    ofile.close()
    
    
#    for x in featureGenerator: print x
#    trainingData = getTrainingData(matchDates, featureGenerator)
    a=1
