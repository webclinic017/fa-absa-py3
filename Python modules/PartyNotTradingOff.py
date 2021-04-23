import acm

whereNotTrading = "notTrading = YES"
parties = acm.FParty.Select(whereNotTrading)

partyArray = parties.AsArray() 
print partyArray

def PartyNotTradingOff(partyArray):
    try:
        partyFile = open('PartyFile.txt', 'w')
    except:
        print 'Failed to open file'
    for party in partyArray:
        #party=acm.FParty[partyname]
        try:
            partyFile.write(party.Name()+'\n')
            party.NotTrading(False)
            party.Commit()
            print 'Changed Not Trading for', party.Name()
        except Exception, e:
            print "Fail to change Not Trading for ", party.Name(), e
    partyFile.close()

PartyNotTradingOff(partyArray)

