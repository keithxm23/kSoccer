import sys, os, datetime, csv

def parseFolder(path):
    matchdata = []
    teamdata = {}
    try:
        for fn in os.listdir(path):
            if fn.endswith(".csv"):
                scoreTable = {}
                print 'Parsing:', path+'/'+fn
                with open(path+'/'+fn, 'rU') as f:
                    reader = csv.reader(f)
                    linecount = 0
                    for row in reader:
                        linecount += 1
                        if linecount == 1:
#                    for line in f:
                            headers = row
                            continue
#                        break
#                    for line in f:
                        match = {}
                        match['season'] = fn.strip('.csv')
#                        row = line.split(",")
                        for x in xrange(1,len(headers)):
                            try:
                                row[x] = float(row[x])
                            except ValueError:
                                pass
                            match[headers[x]] = row[x]
                        if len(row[1].split('/')[-1]) == 4:
                            match['Date'] = datetime.datetime.strptime(row[1],"%d/%m/%Y").date()
                        else:
                            match['Date'] = datetime.datetime.strptime(row[1],"%d/%m/%y").date()
                        

                        try:
                            match['HomePoints'] = scoreTable[match['HomeTeam']]['points']
                        except KeyError:
                            match['HomePoints'] = 0
                        
                        try:
                            match['AwayPoints'] = scoreTable[match['AwayTeam']]['points']
                        except KeyError:
                            match['AwayPoints'] = 0
                        
                        for t in [match['HomeTeam'], match['AwayTeam']]:
                            if t in scoreTable.keys():
                                scoreTable[t]['matchesPlayed'] += 1
                                if t == match['HomeTeam']:
                                    if match['FTR'] == 'H':
                                        scoreTable[t]['points'] += 3
                                    elif match['FTR'] == 'D':
                                        scoreTable[t]['points'] += 1
                                    else:
                                        scoreTable[t]['points'] += 0
                                else:
                                    if match['FTR'] == 'H':
                                        scoreTable[t]['points'] += 0
                                    elif match['FTR'] == 'D':
                                        scoreTable[t]['points'] += 1
                                    else:
                                        scoreTable[t]['points'] += 3
                            else:
                                scoreTable[t] = {}
                                scoreTable[t]['matchesPlayed'] = 1
                                if t == match['HomeTeam']:
                                    if match['FTR'] == 'H':
                                        scoreTable[t]['points'] = 3
                                    elif match['FTR'] == 'D':
                                        scoreTable[t]['points'] = 1
                                    else:
                                        scoreTable[t]['points'] = 0
                                else:
                                    if match['FTR'] == 'H':
                                        scoreTable[t]['points'] = 0
                                    elif match['FTR'] == 'D':
                                        scoreTable[t]['points'] = 1
                                    else:
                                        scoreTable[t]['points'] = 3
                        
                        match['HomeMatches'] = scoreTable[match['HomeTeam']]['matchesPlayed'] - 1
                        match['AwayMatches'] = scoreTable[match['AwayTeam']]['matchesPlayed'] - 1
                        
                        for x in [2,3]:
                            if row[x] in teamdata:
                                teamdata[row[x]].append(match)
                            else:
                                teamdata[row[x]] = [match]
                                
                        matchdata.append(match)
                        
                            
                f.close()
    except Exception as e:
        print str(e)
        sys.exit('file %s, line %d: %s' % (path+'/'+fn, row, e))
        
    matchdata = sorted(matchdata, key=lambda match: match['Date'], reverse=True)
    for l in teamdata.keys():
        teamdata[l] = sorted(teamdata[l], key=lambda match: match['Date'], reverse=True)
    return teamdata, matchdata
        