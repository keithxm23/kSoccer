#!/usr/bin/python
from kparser import parseFolder
import cPickle as pickle, datetime
from featurefns import *
import csv
from utils import column

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
    try:
        traindata = pickle.load( open( "traindata.p", "rb" ) )
        headers = pickle.load( open( "headers.p", "rb" ) )
    except:
        traindata, headers = trainOnAll(data)
        pickle.dump( traindata, open( "traindata.p", "wb" ) )
        pickle.dump( headers, open( "headers.p", "wb" ) )
    
    
    #normalize features in training data
    for x in xrange(len(traindata[0])-1):
        minval = min(column(traindata,x))
        if minval < 0:
            for num, y in enumerate(column(traindata,x)):
                traindata[num][x] = y - minval
    
    
    ofile = open("traindata.csv", 'wb')
    writer = csv.writer(ofile, quoting=csv.QUOTE_ALL)
    
    writer.writerow(headers)
    for tr in traindata:
        writer.writerow(tr)
    ofile.close()
#    for x in featureGenerator: print x
#    trainingData = getTrainingData(matchDates, featureGenerator)
    a=1
