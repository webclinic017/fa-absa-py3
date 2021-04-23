'''
Date                    : 2011-03-09
Purpose                 : Based on the script SAEQ_SpreadCurveUpdate but uses 2 att spread curves to determine the spread for the update curve                            
Department and Desk     : EQ Derivatives MO
Requester               : Marko Milutinovic 
Developer               : Rohan van der Walt
CR Number               : 596123, 883192, 886983, 2099554

HISTORY
================================================================================
Date       Change no    Developer          Description
--------------------------------------------------------------------------------
2012-02-09 889519       Herman Hoon        Changed the module to only use the current ZAR spread curve and a spread.
2012-02-24 		Herman Hoon	   Updated to reference the actaul spread if there is any.
2014-07-10 2099554      Anil Parbhoo       Defined a new Base Spread Curve
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
    
def get_or_interpolate_spread(zar_basis_yc, us_spreadPeriod, date):
    zar_spreads  = zar_basis_yc.Attributes().First().Spreads() #get list of spread points 
    TODAY = ael.date_today()
    basisSpread = 0
    foundSpread = False
    for zar_spread in zar_spreads:
        if convertDatePeriod(zar_spread.Point().DatePeriod()) == convertDatePeriod(us_spreadPeriod):
            basisSpread = zar_spread.Spread()
            foundSpread = True
            print 'Found spread of %f for %s on period %s' %(basisSpread, zar_basis_yc.Name(), us_spreadPeriod) 
        
    if not foundSpread:
        basisSpread = ABSA_Rate.ABSA_yc_rate('', zar_basis_yc.Name(), TODAY, date, 'Quarterly', 'Act/365', 'Par FRN Rate', zar_basis_yc.Currency().Name())
        print 'Interpolated spread of %f for %s on period %s' %(basisSpread, zar_basis_yc.Name(), us_spreadPeriod)
    
    return basisSpread
    
    
ael_gui_parameters = {'windowCaption':'Dual Spread Curve Change Update'}
ael_variables = [
#[variable name, Display Name, Type, Candidate values, Default, mandatory, Multiple, Description , Input Hook, enabled]
['Curve1', 'ZAR Curve', acm.FYieldCurve, listOfYieldCurves(), None, 1, 0, 'Mandatory curve, used to calculate spread changes.', None, 1],
['Curve2', 'Base Spread Curve', acm.FYieldCurve, listOfYieldCurves(), None, 1, 0, 'Mandatory curve, used with ZAR Curve to calculate spread changes.', None, 1],
['staticSpread', 'Static Spread', 'double', 50, None, 1, 0, 'Additional spread in basis points that should be subtracted from the updated curve.', None, 1],
['updateCurve', 'Update Curve', acm.FYieldCurve, listOfYieldCurves(), None, 1, 0, 'Curve that will be updated with the spread.', None, 1],
['simulate', 'Simulate', 'string', ['No', 'Yes'], 'Yes', 1, 0, 'Only output values and changes, no changes will be made to the DB.', None, 1]
]

def ael_main(dict):
    zar_basis_yc1        = dict['Curve1']
    zar_basis_yc2      = dict['Curve2']
    update_yc              = dict['updateCurve']
    staticSpread        = dict['staticSpread']
    #print variables chosen
    print 'Curve1 = ', zar_basis_yc1.Name()
    print 'Curve2 = ', zar_basis_yc2.Name()
    print 'staticSpread = ', staticSpread
    print 'updateCurve = ', update_yc.Name()
    
    
    staticSpread = staticSpread / 10000
    
    #get list of spreads points
    
    update_spreads  = update_yc.Attributes().First().Spreads()
    
    
    
    for us in update_spreads: # where us represents an 'update spread'
        us_date = ael.date(us.Point().PointDate())
        us_period = us.Point().DatePeriod()
        basisSpread1 = get_or_interpolate_spread(zar_basis_yc1, us_period, us_date)
        basisSpread2 = get_or_interpolate_spread(zar_basis_yc2, us_period, us_date)
        adjustValue = staticSpread - basisSpread1 + basisSpread2
        
        print "Adjusting %s for %s to %f" %(update_yc.Name(), us.Point().DatePeriod(), adjustValue) 
        if dict['simulate'] == 'No':
            us.Spread(adjustValue)
            try:
                us.Commit()
                print "\tCommit - Done"
            except Exception:
                print "Error comitting the spread value for curve %s" %(update_yc.Name())
                raise
        print '=======' # so it is easier to read the log of the differnt buckets
    print 'Completed successfully'
    
