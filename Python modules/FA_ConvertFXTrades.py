import ael
import acm
import FBDPRollback
import FBDPCommon
import ABSA_F273728_ConvertFXTrades

Summary = FBDPCommon.Summary


whereNotTrading = "notTrading = YES"
parties = acm.FParty.Select(whereNotTrading)

partyArray = parties.AsArray() 


def PartyNotTrading(partyArray, not_trading):
    for party in partyArray:
        #party=acm.FParty[partyname]
        try:
            #party.Clone()
            party.NotTrading(not_trading)
            party.Commit()
        except Exception, e:
            print "Fail to change Not Trading for ", party.Name(), e
print 'Before party update 1', partyArray
print " Set Party to Not Trading! " 
print "************"       
#PartyNotTrading(partyArray,False)
#print 'After party update 1',partyArray
print "RUN ABSA_F273728_ConvertFXTrades"
print "************"  
try: 
    args={'LogToConsole': 1, 'LogToFile': 0, 'Logfile': 'BDP.log', 'Logmode': 1, 'TestMode': 0}
    ABSA_F273728_ConvertFXTrades.ael_main(args)
except Exception, e:
    print "ABSA_F273728_ConvertFXTrades failed", e
print 'After conversion script', partyArray
print " Set Party to Trading! "    
print "************"           
#PartyNotTrading(partyArray,True)


#PartyNotTrading(list,True)
print 'After party update2', partyArray


