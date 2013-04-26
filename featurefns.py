from utils import diff_month
from stadia import stadia
import math
from math import fabs

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
                      and homeTeam in [l['HomeTeam'], l['AwayTeam']] 
                      , data['matchdata'])
    
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

def getTeamReferee(data, team, date, refree):
    teamdata = filter(lambda l: l['Date'] < date
                      and (team in [l['HomeTeam'], l['AwayTeam']] )
                      and (refree == l['Referee']),
                      data['teamdata'][team]
                      )
    
    avgwins = len(filter(lambda l: (team in l['HomeTeam'] and l['FTR'] == 'H')
                         and (team in l['AwayTeam'] and l['FTR'] == 'A'),data['teamdata'][team]))
    avgdraws = len(filter(lambda l:l['FTR'] == 'D', data['teamdata'][team]))
    avglosses = len(data['teamdata'][team]) - avgwins - avgdraws
    
    W=L=D=0
    for t in teamdata:
        if t['FTR'] == 'D':
            D += 1
        elif (team == t['HomeTeam'] and t['FTR'] == 'H'):
            W += 1
        else:
            L += 1
    
    if W > 0: W *= 100/len(teamdata)
    if L > 0: L *= 100/len(teamdata)
    if D > 0: D *= 100/len(teamdata)
    if avgwins > 0: avgwins *= 100/len(data['teamdata'][team])
    if avglosses > 0: avglosses *= 100/len(data['teamdata'][team])
    if avgdraws > 0: avgdraws *= 100/len(data['teamdata'][team])
    
    return W - avgwins, L - avglosses, D - avgdraws


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

def trainOnAll(data):
    teamdat = {}
    matchdat = {}
    try:
        lastXGames = 3
        train = []
        global statslist
        #use matches only where both home and away teams have played at least (2*lastXGames)-1 matches
        matches = filter(lambda l: l['HomeMatches'] >= 2*lastXGames 
                         and l['AwayMatches'] >= 2*lastXGames
                         , data['matchdata'][:])
        matches.sort(key=lambda item: item['Date'], reverse=True)
        cnt = 0.0
        for x in matches[:]:
            cnt+=1.0
            print cnt/len(matches), x['Date']
            tmp = []
            hedr = []
#            Refree infulence
#            hw, hl, hd = getTeamReferee(data, x['HomeTeam'], x['Date'], x['Referee'])
#            aw, al, ad = getTeamReferee(data, x['AwayTeam'], x['Date'], x['Referee'])
            
#            hedr.append('RefWin')
#            tmp.append((hw*fabs(hw))-(aw*fabs(aw)))
#            hedr.append('RefLoss')
#            tmp.append((hl*fabs(hl))-(al*fabs(al)))
#            hedr.append('RefDraw')
#            tmp.append((hd*fabs(hd))-(ad*fabs(ad)))
            for result in ['Wins', 'Losses', 'Draws']:
                
                hom = getLastEncounters(data=data, 
                                         date=x['Date'], 
                                         lastXGames=lastXGames, 
                                         homeTeam=x['HomeTeam'], 
                                         awayTeam=x['AwayTeam'], 
                                         result=result)
                
                if hom == None:
                    tmp.append(None)
                else:
                    tmp.append(hom)
                hedr.append('H2H'+str(lastXGames)+'encounters'+result)
                                
#                for teamC in data['teamdata'].keys():
                for teamC in []:
#                for teamC in ['Chelsea','Man City', 'Man United', 'Arsenal'
#                              'Liverpool','Tottenham',
#                              'Wigan','Everton','Sunderland'
#                              ]:
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
            
                
#            tmp.append(getDist(x['HomeTeam'],x['AwayTeam']))
#            hedr.append('distance')
            
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

def getEucDist(vect1, vect2):
    return pow(sum([pow(vect1[x]-vect2[x],2) for x in xrange(0,len(vect1))]),0.5)
    