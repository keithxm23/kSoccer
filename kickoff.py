#!/usr/bin/python
from kparser import parseFolder
import cPickle as pickle, datetime
from featurefns import *
import csv
from utils import column, most_common
from kcross import adaboost
import datetime, operator

if __name__ == '__main__':
    try:
        teamdata = pickle.load( open( "teamdata.pckl", "rb" ) )
        matchdata = pickle.load( open( "matchdata.pckl", "rb" ) )
    except:
        teamdata, matchdata = parseFolder('footydata/epl')
        pickle.dump( teamdata, open( "teamdata.pckl", "wb" ) )
        pickle.dump( matchdata, open( "matchdata.pckl", "wb" ) )
        
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
        traindata, teamwise, matchwise, headers = trainOnAll(data)
        pickle.dump( traindata, open( "traindata.p", "wb" ) )
        pickle.dump( teamwise, open( "teamwise.p", "wb" ) )
        pickle.dump( matchwise, open( "matchwise.p", "wb" ) )
        pickle.dump( headers, open( "headers.p", "wb" ) )
    
    
#    normalize features in training data
    for x in xrange(len(traindata[0])-5):
        tmp = [t for t in column(traindata,x) if t != None]
        if len(tmp) == 0:
            avg = 0.0
        else:
            avg = sum(tmp)/len(tmp)
        mn = min(tmp)
        mx = max(tmp)
        for num, y in enumerate(column(traindata,x)):
            if traindata[num][x] == None:
                try:
                    traindata[num][x] = (avg-mn)/(mx-mn)
                except ZeroDivisionError:
                    traindata[num][x] = 0.0
            else:
                try:
                    traindata[num][x] = (traindata[num][x]-mn)/(mx-mn)
                except ZeroDivisionError:
                    traindata[num][x] = 0.0
        
    
    
    


    teamAs = ['Man United']
    teamBs = ['Wolves', 'West Ham', 'Sunderland', 'Stoke']
    for teamA in teamAs:
        for teamB in teamBs:
            if teamA != teamB:
                tofile = open("testdata.csv", 'wb')
                twriter = csv.writer(tofile, quoting=csv.QUOTE_ALL)
                
                twriter.writerow(headers)
                
                ofile = open("traindata.csv", 'wb')
                writer = csv.writer(ofile, quoting=csv.QUOTE_ALL)
                
                writer.writerow(headers)
                pretrain = []
                test = []
                fullTest = []
                for tr in traindata:
                    if teamA in tr and teamB in tr:
                        if ((tr[-3] >= datetime.date(2008, 9, 1))
            #                and (tr[-5] != 'D')
                            ):
                            twriter.writerow(tr)
                            test.append(tr[:-4])
                            fullTest.append(tr)
                    else:
                        pretrain.append(tr[:])
                
                #Get avg feature values the points that were selected as test points
                for t in test:
                    avgtest = []
                    for x in xrange((len(t)-1)):
                        avgtest.append(sum(column(test,x))/len(column(test,x)))
                                
                #Now for all datapoints except testing one, calculate their euclidean distance
                #from the averaged testpoint and sort in ascending order
                trainEucs = []
                for t in pretrain:
                    trainEucs.append((t,getEucDist(avgtest[:-1],t[:-5])))
                    
                trainEucs.sort(key=operator.itemgetter(1))
                
                train = []
                for tcount, t in enumerate(trainEucs):
                    if tcount <400:
            #        if ((teamA in t[0][-2:]) or teamB in t[0][-2:]) and tcount<300:
            #        if True:
                        train.append(t[0][:-4])
                        writer.writerow(t[0])
                    
                ofile.close()
                tofile.close()
                    
                for t in train:
                    t.append(1.0/len(train))
                    
                for t in test:
                    t.append(None)
                    
                adaboost(train, test, headers, fullTest)
    print "end"
