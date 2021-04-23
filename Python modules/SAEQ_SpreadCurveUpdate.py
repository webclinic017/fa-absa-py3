'''
Date                    : 2011-03-09
Purpose                 : To check the change for the day between the SOB spread curve and the "live" spread curve. 
                          Then apply the equal and opposite changes to the USD spread curve.                            
Department and Desk     : EQ Derivatives MO
Requester               : Marko Milutinovic 
Developer               : Rohan van der Walt
CR Number               : 596123, 883192, 886983

HISTORY
================================================================================
Date       Change no    Developer          Description
--------------------------------------------------------------------------------
2012-02-09 889519       Herman Hoon        Changed the module to only use the current ZAR spread curve and a spread.
2012-02-24 		Herman Hoon	   Updated to reference the actaul spread if there is any.
'''

import acm, ael, ABSA_Rate
import re

def convertDatePeriod(key):
    '''Converts the date period to a string that is consistent
    '''
    keyFormat = r'([\d]+)([ymwdYMWD])'
    myMatch = re.match(keyFormat, key)
    if myMatch:
        number = int(myMatch.group(1))
        if myMatch.group(2).upper() == "D":
            return str(number) + "D"
        if myMatch.group(2).upper() == "W":
            return str(number) + "W"                
        if myMatch.group(2).upper() == "M":
            #Convert months to years, only if number n multiple of 12.
            if (number % 12) == 0:
                return str(number/12) + "Y"
            else:
                return str(number) + "M"
        if myMatch.group(2).upper() == "Y":
            return str(number) + "Y"
    else:
        raise Exception("Key Format Error: '%s' expecting %s" % (key, keyFormat))   

def listOfYieldCurves():
    return acm.FAttributeSpreadCurve.Select('')

ael_gui_parameters = {'windowCaption':'Spread Curve Change Update'}
ael_variables = [
['Curve', 'ZAR Curve', acm.FYieldCurve, listOfYieldCurves(), None, 1, 0, 'End of business curve, used to calculate spread changes.', None, 1],
['updateSpread', 'Update Spread', 'double', 50, None, 1, 0, 'Additional spread in basis points that should be subtracted from the updated curve.', None, 1],
['updateCurve', 'Update Curve', acm.FYieldCurve, listOfYieldCurves(), None, 1, 0, 'Curve that will be updated with the spread.', None, 1],
['simulate', 'Simulate', 'string', ['No', 'Yes'], 'Yes', 1, 0, 'Only output values and changes, no changes will be made to the DB.', None, 1]
]

def ael_main(dict):
    zar_basis_yc        = dict['Curve']
    usd_yc              = dict['updateCurve']
    updateSpread        = dict['updateSpread']
    
    if not updateSpread:
        updateSpread = 0
    else:
        updateSpread = updateSpread / 10000
    
    #get list of spreads points
    zar_spreads  = zar_basis_yc.Attributes().First().Spreads()
    usd_spreads  = usd_yc.Attributes().First().Spreads()
    spreadPoints = []
    
    TODAY = ael.date_today()
    for us in usd_spreads:
        date = ael.date(us.Point().PointDate())
        us_spreadPeriod = us.Point().DatePeriod()
        
        basisSpread = 0
        foundSpread = False
        #if there is spreads get the spread, otherwise interpolate the spread
        for zar_spread in zar_spreads:
            if convertDatePeriod(zar_spread.Point().DatePeriod()) == convertDatePeriod(us_spreadPeriod):
                basisSpread = zar_spread.Spread()
                foundSpread = True
                print 'Found spread for %s on period %s' %(zar_basis_yc.Name(), us_spreadPeriod) 
        
        if not foundSpread:
            basisSpread = ABSA_Rate.ABSA_yc_rate('', zar_basis_yc.Name(), TODAY, date, 'Quarterly', 'Act/365', 'Par FRN Rate', zar_basis_yc.Currency().Name())
            print 'Interpolating spread for %s on period %s' %(zar_basis_yc.Name(), us_spreadPeriod)
            
        adjustValue = -updateSpread - basisSpread
        
        print "Adjusting %s's current value of %f for %s to %f" %(usd_yc.Name(), us.Spread(), us.Point().DatePeriod(), adjustValue) 
        if dict['simulate'] == 'No':
            us.Spread(adjustValue)
            try:
                us.Commit()
                print "\tCommit - Done"
            except Exception, e:
                print "Error comitting the spread value for curve %s" %(usd_yc.Name())
    print 'Completed successfully'
