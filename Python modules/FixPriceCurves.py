import ael, acm
import FBDPGui
reload(FBDPGui)

def fixPriceCurves(args):

    testmode = args['testmode']
    message = ""
    for curve in  args['priceCurves']:
        #if we are in historical mode, we want to work with valuation parameters for that
        #date unless specified differently; if a current curve is specified, then the
        #historical one is meant
        if not curve.IsHistorical() and acm.IsHistoricalMode():
            price_curve = acm.GetHistoricalEntity(curve, acm.Time().DateToday())
        else:
            price_curve = curve
        if price_curve.Type() == 'Price':
            message = "Fixing %s " % price_curve.Name()
            if price_curve.UseBenchmarkDates() == 0:
                price_curve.UseBenchmarkDates(1)
                price_curve.UseBenchmarkDates(0)      
            else:
                price_curve.UseBenchmarkDates(0)
                price_curve.UseBenchmarkDates(1)
            if testmode == 0:
                message = message + " - Commit"     
                price_curve.Commit()
                price_curve.Calculate()
                price_curve.Commit()
            print message
         
if  __name__ == '__main__':
    logme('Running FixPriceCurve from the platform has not been '\
        'implemented, Must be run from within the client.', 'ERROR')
else:
    # Tool Tip
    ttresets = "Select Price Curves to fix"
    tttestmode = "Run script in testmode"
 
    ael_variables = FBDPGui.LogVariables(
        ('testmode', 'Testmode_Price Curves', 'int', [0, 1], 0, 0, 0, tttestmode),
        ('priceCurves', 'PriceCurves_Price Curves', 'FYieldCurve', None, None, 0, 1, ttresets))
        
    def ael_main(dictionary):
        import FBDPString
        reload(FBDPString)
        import FBDPCommon
        reload(FBDPCommon)

        # Only used for Op Man Fixing (1 = do not commit changes)
   
        logme = FBDPString.logme
        ScriptName = "FixPriceCurves"
        logme.setLogmeVar(ScriptName,
                          dictionary['Logmode'],
                          dictionary['LogToConsole'],
                          dictionary['LogToFile'],
                          dictionary['Logfile'],
                          dictionary['SendReportByMail'], 
                          dictionary['MailList'], 
                          dictionary['ReportMessageType'])
            
        FBDPCommon.execute_script(fixPriceCurves, dictionary)
        logme('FINISH')
        print "Completed Successfully ::"
        

