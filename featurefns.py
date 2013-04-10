from utils import diff_month

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
#                          and l['HomeMatches'] >= lastXGames 
#                          and l['AwayMatches'] >= lastXGames
                          , data['teamdata'][team])
    elif location == 'Home':
        teamdata = filter(lambda l: l['Date'] < date 
                          and l['HomeTeam'] == team
#                           and l['HomeMatches'] >= lastXGames 
#                           and l['AwayMatches'] >= lastXGames
                           , data['teamdata'][team])
    elif location == 'Away':
        teamdata = filter(lambda l: l['Date'] < date 
                          and l['AwayTeam'] == team
#                           and l['HomeMatches'] >= lastXGames 
#                           and l['AwayMatches'] >= lastXGames
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
#    if len(teamdata) == 0: return None
    
    #debug
    if len(teamdata) < lastXGames:
        print 'Setting None', team
        return None
#        raise Exception("Debug this")
    
    for x in teamdata:
#        print x['Date'], x['HomeTeam'], x['AwayTeam'], x['FTR']
        if (x['AwayTeam'] == team and x['FTR'] == awayresult) or (x['HomeTeam'] == team and x['FTR'] == homeresult):
            count += 1
            
    return count/len(teamdata)



#stat = FTGoals / HTGoals / Shots / ShotsOnTarget / HitWoodwork / Corners / Fouls / Offisides / Yellows / Reds / BookingsPoints
def getRecentStats(data, date=None, lastXGames = None, team=None, stat=None):
    try:
        teamdata = filter(lambda l: l['Date'] < date 
    #                      and l['HomeMatches'] >= lastXGames 
    #                      and l['AwayMatches'] >= lastXGames
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
    #    if len(teamdata) == 0: return None
        
        if len(teamdata) < lastXGames:
            print 'Setting None', team
            return None
    #        raise Exception("Debug this")
        
        for x in teamdata:
            if x['AwayTeam'] == team:
                count += x[awaystat]
    #            print x['Date'], x['HomeTeam'], x['AwayTeam'], x[awaystat]
            elif x['HomeTeam'] == team:
                count += x[homestat]
    #            print x['Date'], x['HomeTeam'], x['AwayTeam'], x[homestat]
                
        return count/len(teamdata)
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



def getTrainingData(date, monthsAgo, matchDates, ):
    pass

def trainOnAll(data):
    try:
        lastXGames = 3
        train = []
        global statslist
        #use matches only where both home and away teams have played at least (2*lastXGames)-1 matches
        matches = filter(lambda l: l['HomeMatches'] >= 2*lastXGames 
                         and l['AwayMatches'] >= 2*lastXGames
                         , data['matchdata'][:])
        matches.sort(key=lambda item: item['Date'], reverse=True)
        cnt = 0
        for x in matches[:]:
            cnt+=1
    #        print cnt, x['Date']
            tmp = []
            hedr = []
            for result in ['Wins', 'Losses', 'Draws']:
                for team in [x['HomeTeam'], x['AwayTeam']]:
                    if team == x['HomeTeam']:
                        location = 'Home'
                    elif team == x['AwayTeam']:
                        location = 'Away'
                    
                    hedr.append(str(lastXGames)+result+location)
                    tmp.append(getRecentResults(   data=data,
                                                   date=x['Date'],
                                                   lastXGames=lastXGames,
                                                   team=team,
                                                   result=result,
                                                   location=location))
                    
            
            for team in [x['HomeTeam'], x['AwayTeam']]:
                if team == x['HomeTeam']:
                        location = 'Home'
                elif team == x['AwayTeam']:
                    location = 'Away'
                
                tmp.append(getRecentResults(   data=data,
                                               date=x['Date'],
                                               lastXGames=lastXGames,
                                               team=team,
                                               result=result,
                                               location='All'))
                hedr.append(str(lastXGames)+location+'All')
                
                        
                        
                for stat in statslist:
                    tmp.append(getRecentStats(data=data,
                                              date=x['Date'],
                                              lastXGames=lastXGames,
                                              team=team,
                                              stat=stat))
                    hedr.append(str(lastXGames)+location+stat)
            hedr.append('result')
            tmp.append(x['FTR'])
            train.append(tmp)
        
        return train, hedr
    
    except Exception as e:
        return e