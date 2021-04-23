
import ael, acm
import FBDPGui
reload(FBDPGui)


def insertExoticEvents():
    q = acm.CreateFASQLQuery(acm.FExoticEvent, 'AND')  # empty query

    op = q.AddOpNode('AND')
    op.AddAttrNode('Date', 'GREATER_EQUAL', '0d')
    op.AddAttrNode('Date', 'LESS_EQUAL', None)

    #op = q.AddOpNode('AND')
    #op.AddAttrNode('EndDate', 'GREATER_EQUAL', None)
    #op.AddAttrNode('EndDate', 'LESS_EQUAL', '0d')

    op = q.AddOpNode('AND')
    op.AddAttrNode('Type', 'EQUAL', None)
    
    op = q.AddOpNode('AND')
    op.AddAttrNode('instrument.insType', 'EQUAL', ael.enum_from_string('InsType', 'PriceSwap'))

    op = q.AddOpNode('AND')
    op.AddAttrNode('instrument.trades.status', 'EQUAL', None)

    op = q.AddOpNode('AND')
    op.AddAttrNode('instrument.name', 'EQUAL', None)
    
    return q


if  __name__ == '__main__':
    logme('Running ExoticEventFixing from the platform has not been '\
        'implemented, Must be run from within the client.', 'ERROR')
else:
    # Tool Tip
    ttresets = "Select the exotic events to set fx rate for"
    tttestmode = "Run script in testmode"
    
    q = insertExoticEvents()

    ael_variables = FBDPGui.LogVariables(
        ('testmode', 'Testmode_Fixing', 'int', [0, 1], 0, 0, 0, tttestmode),
        ('exoticEvents', 'Exotic Events_Fixing', 'FExoticEvent', None, q, 0, 1, ttresets))
        
    def ael_main(dictionary):
        import FBDPString
        reload(FBDPString)
        import FBDPCommon
        reload(FBDPCommon)
        import FxPriceSwapFixExoticEventsPerform
        reload(FxPriceSwapFixExoticEventsPerform)

        # Only used for Op Man Fixing (1 = do not commit changes)
   
        logme = FBDPString.logme
        ScriptName = "ExoticEventFixing"
        logme.setLogmeVar(ScriptName,
                          dictionary['Logmode'],
                          dictionary['LogToConsole'],
                          dictionary['LogToFile'],
                          dictionary['Logfile'],
                          dictionary['SendReportByMail'], 
                          dictionary['MailList'], 
                          dictionary['ReportMessageType'])
            
        FBDPCommon.execute_script(FxPriceSwapFixExoticEventsPerform.fixExoticEvents, dictionary)
        logme('FINISH')
        print "Completed Successfully ::"
        

def startRunScript(eii):
    acm.RunModuleWithParameters("FxPriceSwapFixExoticEvents", acm.GetDefaultContext())


