#!/usr/bin/python
from kparser import parseFolder
import cPickle as pickle, datetime
from featurefns import getRecentResults, getRecentStats, getTrainingData, getMatchDates
from featurefns import getFeatureGenerator

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
    
    
 
    
#    print getRecentStats(data, date=datetime.date(2013,1,15),lastXGames = 10, team='Arsenal', stat='FTGoals')
#    print getRecentResults(data, date=datetime.date(2012,1,15),lastXGames = 10, team='Arsenal', result='Wins', location='Away')
#    print getRecentResults(data, date=datetime.date(2012,1,15),lastXGames = 10, team='Arsenal', result='Wins', location='All')
#
    homeTeam = 'Arsenal'
    awayTeam = 'Aston Villa'
#    matchDates, labels = getMatchDates()
    featureGenerator = getFeatureGenerator(home=homeTeam, away=awayTeam)

#    for x in featureGenerator: print x
    trainingData = getTrainingData(matchDates, featureGenerator)
    a=1
