
def getRecentResults(data, date=None,lastXGames = None, team=None, result=None, location=None):
    if location == 'All':
        teamdata = filter(lambda l: l['Date'] < date ,data['teamdata'][team])
    elif location == 'Home':
        teamdata = filter(lambda l: l['Date'] < date and l['HomeTeam'] == team,data['teamdata'][team])
    elif location == 'Away':
        teamdata = filter(lambda l: l['Date'] < date and l['AwayTeam'] == team,data['teamdata'][team])
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
    for x in teamdata:
        print x['Date'], x['HomeTeam'], x['AwayTeam'], x['FTR']
        if x['AwayTeam'] == team and x['FTR'] == awayresult:
            count += 1
        elif x['HomeTeam'] == team and x['FTR'] == homeresult:
            count += 1
            
    return count/len(teamdata)



#stat = FTGoals / HTGoals / Shots / ShotsOnTarget / HitWoodwork / Corners / Fouls / Offisides / Yellows / Reds / BookingsPoints
def getRecentStats(data, date=None, lastXGames = None, team=None, stat=None):
    teamdata = filter(lambda l: l['Date'] < date ,data['teamdata'][team])    
    teamdata = teamdata[:lastXGames]

    statmap = {'FTGoals' : ('FTHG','FTAG'),
               'HTGoals' : ('HTHG','HTAG'),
               'Shots' : ('HS','AS'),
               'ShotsOnTarget' : ('HST','AST'),
#               'HitWoodwork' : ('HHW','AHW'),  HHW, AHW Not present in all csv files
               'Corners' : ('HC','AC'),
               'Fouls' : ('HF','AF'),
               'Offisdes' : ('HO','AO'),
               'Yellows' : ('HY','AY'),
               'Reds' : ('HR','AR'),
               'BookingsPoints' : ('HBP','ABP'),
               }
    try:
        homestat, awaystat = statmap[stat]
    except KeyError:
        raise Exception("Invalid 'stat' argument for getRecentStats")

    count = 0.0
    for x in teamdata:
        if x['AwayTeam'] == team:
            count += x[awaystat]
            print x['Date'], x['HomeTeam'], x['AwayTeam'], x[awaystat]
        elif x['HomeTeam'] == team:
            count += x[homestat]
            print x['Date'], x['HomeTeam'], x['AwayTeam'], x[homestat]
            
    return count/len(teamdata)

def getMatchDates():
    pass

def getFeatureGenerator(home=None, away=None):
#    lastXgames = 4
    featureGenerator = []
    for result in ['Wins', 'Losses', 'Draws']:
        for team in [home, away]:
            if team == home:
                location = 'home'
            elif team == away:
                location = 'away'
            
            featureGenerator.append((getRecentResults, {#'data':data,
                                                       'lastXGames':2,
                                                       'team':team,
                                                       'result':result,
                                                       'location':location}))
            
    
    for team in [home, away]:
        featureGenerator.append((getRecentResults, {#'data':data,
                                           'lastXGames':4,
                                           'team':team,
                                           'result':result,
                                           'location':'All'}))
        
        for stat in ['FTGoals', 'HTGoals', 'Shots', 'ShotsOnTarget',  'Corners', 'Fouls', 'Offisides', 'Yellows', 'Reds']:
            featureGenerator.append((getRecentStats, {#'data':data,
                                                   'lastXGames':4,
                                                   'team':team,
                                                   'stat':stat}))
            
    
    return featureGenerator

def getRecentGenerator(getRecentFn=None, params=None, date=None):
    if getRecentFn is getRecentResults:
        return getRecentResults(params['data'], date=date, lastXGames = params['lastXGames'],
                          team=params['team'], result=params['result'], location=params['location'])
    elif getRecentFn is getRecentStats:
        return getRecentStats(params['data'], date=date, lastXGames = params['lastXGames'],
                          team=params['team'], stat=params['stat'])
    else:
        raise Exception("Invalid 'getRecentFn' argument for getRecentStats")

def getTrainingData(date=None, monthsAgo=None, matchDates=None, ):
    pass