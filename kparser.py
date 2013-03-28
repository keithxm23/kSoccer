import sys, os, datetime

def parseFolder(path):
    matchdata = {}
    teammatchdata = {}
    try:
        for fn in os.listdir(path):
            if fn.endswith(".csv"):
                print 'Parsing:', path+'/'+fn
                with open(path+'/'+fn, 'rU') as f:
                    for line in f:
                        headers = line.split(",")
                        break
                    match = {}
                    for line in f:
                        tmp = line.split(",")
                        for x in xrange(1,23):
                            match[headers[x]] = tmp[x]
                        if len(tmp[1].split('/')[-1]) == 4:
                            match['Date'] = datetime.datetime.strptime(tmp[1],"%d/%m/%Y").date()
                        else:
                            match['Date'] = datetime.datetime.strptime(tmp[1],"%d/%m/%y").date()
                        key = tmp[1]+tmp[2]+tmp[3]#set key as concatenation of date+hometeam+awayteam
                        matchdata[key] = match
                        for x in [2,3]:
                            if tmp[x] in teammatchdata:
                                teammatchdata[tmp[x]].append(match)
                            else:
                                teammatchdata[tmp[x]] = [match]
    
                f.close()
    except Exception as e:
        print str(e)
        sys.exit('file %s, line %d: %s' % (path+'/'+fn, line, e))
    return matchdata, teammatchdata
        