import acm

def PartyNotTradingRestore():
    try:
        partyFile = open('PartyFile.txt', 'r')
    except:
        print 'Failed to open file'
    line=partyFile.readline()
    while line:
        #party=acm.FParty[partyname]
        try:
            name=line[:-1]
            print name
            party=acm.FParty[name]
            party.NotTrading(True)
            party.Commit()
            print 'Restored Not Trading for', party.Name()
        except Exception, e:
            print "Fail to change Not Trading for ", name, e
        line=partyFile.readline()
    partyFile.close()

PartyNotTradingRestore()
