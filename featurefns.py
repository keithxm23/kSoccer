from utils import diff_month
from stadia import stadia
import math


statslist = [
             'FTGoals', 
             'HTGoals', 
             'Shots', 
             'ShotsOnTarget',
#             'HitWoodwork',
             'Corners', 
             'Fouls', 
#             'Offsides', 
             'Yellows', 
             'Reds'
             ]

def getRecentResults(data, date, lastXGames, team, result, location):
    if location == 'All':
        teamdata = filter(lambda l: l['Date'] < date 
                          and l['HomeMatches'] >= lastXGames 
                          and l['AwayMatches'] >= lastXGames
                          , data['teamdata'][team])
    elif location == 'Home':
        teamdata = filter(lambda l: l['Date'] < date 
                          and l['HomeTeam'] == team
                           and l['HomeMatches'] >= lastXGames 
                           and l['AwayMatches'] >= lastXGames
                           , data['teamdata'][team])
    elif location == 'Away':
        teamdata = filter(lambda l: l['Date'] < date 
                          and l['AwayTeam'] == team
                           and l['HomeMatches'] >= lastXGames 
                           and l['AwayMatches'] >= lastXGames
                           , data['teamdata'][team])
    else:
        raise Exception("Invalid location argument for getRecentResults")
    
    teamdata = teamdata[:lastXGames]

    if result == 'Wins':
        homeresult = 'H'
        awayresult = 'A'
    elif result == 'Losses':
        homeresult = 'A'
        awayresult = 'H'
    elif result == 'Draws':
        homeresult = 'D'
        awayresult = 'D'
    else:
        raise Exception("Invalid result argument for getRecentResults")
    
    count = 0.0
    if len(teamdata) == 0: return None
    
    #debug
#    if len(teamdata) < lastXGames:
#        print 'Setting None', team
#        return None
#        raise Exception("Debug this")
    
    for x in teamdata:
#        print x['Date'], x['HomeTeam'], x['AwayTeam'], x['FTR']
        if (x['AwayTeam'] == team and x['FTR'] == awayresult) or (x['HomeTeam'] == team and x['FTR'] == homeresult):
            count += 1
            
    return count*count/len(teamdata)








def getLastEncounters(data, date, lastXGames, homeTeam, awayTeam, result):
    if homeTeam == awayTeam:
        return None
    
    teamdata = filter(lambda l: l['Date'] < date 
                      and awayTeam in [l['HomeTeam'], l['AwayTeam']] 
                      , data['teamdata'][homeTeam])
    
    teamdata = teamdata[:lastXGames]

    if result == 'Wins':
        homeresult = 'H'
        awayresult = 'A'
    elif result == 'Losses':
        homeresult = 'A'
        awayresult = 'H'
    elif result == 'Draws':
        homeresult = 'D'
        awayresult = 'D'
    else:
        raise Exception("Invalid result argument for getRecentResults")
    
    count = 0.0
    if len(teamdata) == 0: return 0.0
    
    #debug
#    if len(teamdata) < lastXGames:
#        print 'Setting None', team
#        return None
#        raise Exception("Debug this")
    
    for x in teamdata:
#        print x['Date'], x['HomeTeam'], x['AwayTeam'], x['FTR']
        if ((x['HomeTeam'] == homeTeam and x['FTR'] == homeresult) or (x['AwayTeam'] == homeTeam and x['FTR'] == awayresult)):
            count += 1
            
    return count*count/len(teamdata)







#stat = FTGoals / HTGoals / Shots / ShotsOnTarget / HitWoodwork / Corners / Fouls / Offisides / Yellows / Reds / BookingsPoints
def getRecentStats(data, date=None, lastXGames = None, team=None, stat=None):
    try:
        teamdata = filter(lambda l: l['Date'] < date 
                          and l['HomeMatches'] >= lastXGames 
                          and l['AwayMatches'] >= lastXGames
                          , data['teamdata'][team])    
        teamdata = teamdata[:lastXGames]
    
        statmap = {'FTGoals' : ('FTHG','FTAG'),
                   'HTGoals' : ('HTHG','HTAG'),
                   'Shots' : ('HS','AS'),
                   'ShotsOnTarget' : ('HST','AST'),
    #               'HitWoodwork' : ('HHW','AHW'),  HHW, AHW Not present in all csv files
                   'Corners' : ('HC','AC'),
                   'Fouls' : ('HF','AF'),
    #               'Offsides' : ('HO','AO'),
                   'Yellows' : ('HY','AY'),
                   'Reds' : ('HR','AR'),
                   'BookingsPoints' : ('HBP','ABP'),
                   }
        try:
            homestat, awaystat = statmap[stat]
        except KeyError:
            raise Exception("Invalid 'stat' argument for getRecentStats")
    
        count = 0.0
        if len(teamdata) == 0: return None
        
#        if len(teamdata) < lastXGames:
#            print 'Setting None', team
#            return None
    #        raise Exception("Debug this")
        
        for x in teamdata:
            if x['AwayTeam'] == team:
                count += x[awaystat]
    #            print x['Date'], x['HomeTeam'], x['AwayTeam'], x[awaystat]
            elif x['HomeTeam'] == team:
                count += x[homestat]
    #            print x['Date'], x['HomeTeam'], x['AwayTeam'], x[homestat]
                
        return count*count/len(teamdata)
    except Exception as e:
        return e




def getMatchDates(data, home, away, dateBefore, monthsOld):
    teamdata = filter(lambda l: l['Date'] < dateBefore 
                      and (home in [l['HomeTeam'], l['AwayTeam']] 
                           and 
                           away in [l['HomeTeam'], l['AwayTeam']]) 
                      and 
                      diff_month(dateBefore, l['Date']) <= 18, data['matchdata'])
    for x in teamdata: print x['Date'], x['HomeTeam'], x['AwayTeam']
    a=1

def getFeatureGenerator(home, away):
#    lastXgames = 4
    global statslist
    featureGenerator = []
    for result in ['Wins', 'Losses', 'Draws']:
        for team in [home, away]:
            if team == home:
                location = 'Home'
            elif team == away:
                location = 'Away'
            
            featureGenerator.append((getRecentResults, {
                                                       'lastXGames':2,
                                                       'team':team,
                                                       'result':result,
                                                       'location':location}))
            
    
    for team in [home, away]:
        featureGenerator.append((getRecentResults, {
                                                   'lastXGames':4,
                                                   'team':team,
                                                   'result':result,
                                                   'location':'All'}))
        
        for stat in statslist:
            featureGenerator.append((getRecentStats, {
                                                      'lastXGames':4,
                                                      'team':team,
                                                      'stat':stat}))
                
    
    return featureGenerator

def getRecentGenerator(getRecentFn, params, date):
    if getRecentFn is getRecentResults:
        return getRecentResults(params['data'], date=date, lastXGames = params['lastXGames'],
                          team=params['team'], result=params['result'], location=params['location'])
    elif getRecentFn is getRecentStats:
        return getRecentStats(params['data'], date=date, lastXGames = params['lastXGames'],
                          team=params['team'], stat=params['stat'])
    else:
        raise Exception("Invalid 'getRecentFn' argument for getRecentStats")



def getTrainingData(dataset, teamwise, date, homeTeam, awayTeam):
    data = [l[:-4] for l in dataset 
                 if l[-3] < date
                 and homeTeam in l[-2:-3]
                 and awayTeam in l[-2:-3]]
    
    tmp = []

def trainOnAll(data, teamA=None, teamB=None):
    teamdat = {}
    matchdat = {}
    try:
        lastXGames = 3
        train = []
        global statslist
        #use matches only where both home and away teams have played at least (2*lastXGames)-1 matches
        matches = filter(lambda l: l['HomeMatches'] >= 2*lastXGames 
                         and l['AwayMatches'] >= 2*lastXGames
                         and (teamA in [l['HomeTeam'],l['AwayTeam']]
                              or teamB in [l['HomeTeam'],l['AwayTeam']])
                         , data['matchdata'][:])
        matches.sort(key=lambda item: item['Date'], reverse=True)
        cnt = 0.0
        for x in matches[:]:
            cnt+=1.0
            print cnt/len(matches), x['Date']
            tmp = []
            hedr = []
            
            
            for result in ['Wins', 'Losses', 'Draws']:
#                for teamC in data['teamdata'].keys():
                for teamC in ['Chelsea', 'Liverpool','Tottenham','Man City', 'Man United',
                              'Wigan','Everton','Sunderland']:
                    hom = getLastEncounters(data=data, 
                                             date=x['Date'], 
                                             lastXGames=lastXGames, 
                                             homeTeam=x['HomeTeam'], 
                                             awayTeam=teamC, 
                                             result=result)
                    awy = getLastEncounters(data=data, 
                                             date=x['Date'], 
                                             lastXGames=lastXGames, 
                                             homeTeam=x['AwayTeam'], 
                                             awayTeam=teamC, 
                                             result=result)
                    
                    if hom == None or awy == None:
                        tmp.append(None)
                    else:
                        tmp.append(hom-awy)
                    hedr.append(teamC+str(lastXGames)+'encounters'+result)
                    
                homa = getRecentResults(   data=data,
                                               date=x['Date'],
                                               lastXGames=lastXGames,
                                               team=x['HomeTeam'],
                                               result=result,
                                               location='All')
                awya = getRecentResults(   data=data,
                                               date=x['Date'],
                                               lastXGames=lastXGames,
                                               team=x['AwayTeam'],
                                               result=result,
                                               location='All')
                if homa == None or awya == None:
                    tmp.append(None)
                else:
                    tmp.append(homa - awya)
                hedr.append(str(lastXGames)+'All'+result)

                homr = getRecentResults(   data=data,
                                               date=x['Date'],
                                               lastXGames=lastXGames,
                                               team=x['HomeTeam'],
                                               result=result,
                                               location='Home')
                awyr = getRecentResults(   data=data,
                                               date=x['Date'],
                                               lastXGames=lastXGames,
                                               team=x['AwayTeam'],
                                               result=result,
                                               location='Away')
                if homr == None or awyr == None:
                    tmp.append(None)
                else:
                    tmp.append(homr - awyr)
                hedr.append(str(lastXGames)+result)
                
                                
                        
                        
            for stat in statslist:
                homs = getRecentStats(data=data,
                                          date=x['Date'],
                                          lastXGames=lastXGames,
                                          team=x['HomeTeam'],
                                          stat=stat)
                awys = getRecentStats(data=data,
                                          date=x['Date'],
                                          lastXGames=lastXGames,
                                          team=x['AwayTeam'],
                                          stat=stat)
                if homs == None or awys == None:
                    tmp.append(None)
                else:
                    tmp.append(homs - awys)
                hedr.append(str(lastXGames)+stat)
                
            
            tmp.append(pow(x['HomePoints'],2)-pow(x['AwayPoints'],2))
            hedr.append('PtsDiff')
                
            tmp.append(getDist(x['HomeTeam'],x['AwayTeam']))
            hedr.append('distance')
            
            hedr.append('result')
            tmp.append(x['FTR'])
            
            hedr.append('BetResult')
            tmp.append(x['BetResult'])
            
            hedr.append('Date')
            tmp.append(x['Date'])
            
            hedr.append('HomeTeam')
            tmp.append(x['HomeTeam'])
            
            hedr.append('AwayTeam')
            tmp.append(x['AwayTeam'])
#            
            train.append(tmp)
            
            if x['HomeTeam'] in teamdat:
                teamdat[x['HomeTeam']].append(tmp)
            else:
                teamdat[x['HomeTeam']] = [tmp]
                
            if x['AwayTeam'] in teamdat:
                teamdat[x['AwayTeam']].append(tmp)
            else:
                teamdat[x['AwayTeam']] = [tmp]
                
            if x['HomeTeam']+x['AwayTeam'] in matchdat:
                matchdat[x['HomeTeam']+x['AwayTeam']].append(tmp)
            else:
                matchdat[x['HomeTeam']+x['AwayTeam']] = [tmp]
        
        return train, teamdat, matchdat, hedr
    
    except Exception as e:
        return e
    
    
def deg2rad(deg):
    return deg * (math.pi/180)


def getDist(homeTeam, awayTeam):
    R = 6371 # Radius of the earth in km
    (lat2,lat1) = (stadia[homeTeam][0], stadia[awayTeam][0])
    (lon2,lon1) = (stadia[homeTeam][1], stadia[awayTeam][1])
    dLat = deg2rad(lat2-lat1); # deg2rad below
    dLon = deg2rad(lon2-lon1) 
    a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(deg2rad(lat1)) * math.cos(deg2rad(lat2)) *  math.sin(dLon/2) * math.sin(dLon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c # Distance in km
    return d

    