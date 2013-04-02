import sys, os, datetime

def parseFolder(path):
    matchdata = []
    teamdata = {}
    try:
        for fn in os.listdir(path):
            if fn.endswith(".csv"):
                print 'Parsing:', path+'/'+fn
                with open(path+'/'+fn, 'rU') as f:
                    for line in f:
                        headers = line.split(",")
                        break
                    for line in f:
                        match = {}
                        match['season'] = fn.strip('.csv')
                        tmp = line.split(",")
                        for x in xrange(1,23):
                            try:
                                tmp[x] = float(tmp[x])
                            except ValueError:
                                pass
                            match[headers[x]] = tmp[x]
                        if len(tmp[1].split('/')[-1]) == 4:
                            match['Date'] = datetime.datetime.strptime(tmp[1],"%d/%m/%Y").date()
                        else:
                            match['Date'] = datetime.datetime.strptime(tmp[1],"%d/%m/%y").date()
                        matchdata.append(match)
                        for x in [2,3]:
                            if tmp[x] in teamdata:
                                teamdata[tmp[x]].append(match)
                            else:
                                teamdata[tmp[x]] = [match]
                f.close()
    except Exception as e:
        print str(e)
        sys.exit('file %s, line %d: %s' % (path+'/'+fn, line, e))
        
    matchdata = sorted(matchdata, key=lambda match: match['Date'], reverse=True)
    for l in teamdata.keys():
        teamdata[l] = sorted(teamdata[l], key=lambda match: match['Date'], reverse=True)
    return teamdata, matchdata
        