import acm

def PartyNotTradingRestore():

    try:
        partyFile = open('/apps/frontnt/REPORTS/BackOffice/Atlas-End-Of-Day/Not_Trading_Counterparty.txt', 'r')
    except:
        print 'Failed to open file'
    line=partyFile.readline()
    while line:
        
        try:
            name=line[:-1]
            party=acm.FParty[name]
            party.NotTrading(True)
            party.Commit()
            print 'Restored Not Trading for', party.Name()
        except Exception, e:
            print "Fail to change Not Trading for ", name, e
        line=partyFile.readline()
    partyFile.close()

PartyNotTradingRestore()
