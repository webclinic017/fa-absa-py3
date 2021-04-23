'''
Date                    : 2012-02-12
Purpose                 : To update the USD-SWAP-SPREAD(50bps)BASIS/PT curve by 50bps from the ZAR-BASIS/PriceTesting rates.
                          
Department and Desk     : PCG - VCG
Requester               : Khaya Mtoko
Developer               : Tshepo Mabena
CR Number               : 890139
'''

import acm, UserDict, re

class DateDict(UserDict.UserDict):
    '''
    When using "relative" dates for dict key i.e. 1y or 7m
    This dictionary will return same values for 12m or 1y requests.
    '''
    
    def getDefaultKey(self, key):
        myMatch = re.match(self.keyFormat, key)
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
            raise Exception("Key Format Error: '%s' expecting %s" % (key, self.keyFormat))
    
    def __init__(self):
        UserDict.UserDict.__init__(self)
        self.keyFormat = r'([\d]+)([ymwdYMWD])'

    def __setitem__(self, key, val):
        UserDict.UserDict.__setitem__(self, self.getDefaultKey(key), val)

    def __getitem__(self, key):
        return UserDict.UserDict.__getitem__(self, self.getDefaultKey(key))

    def has_key(self, key):
        return UserDict.UserDict.__contains__(self, self.getDefaultKey(key))

def listOfYieldCurves():
    return acm.FAttributeSpreadCurve.Select('')

ael_gui_parameters = {'windowCaption':'Spread Curve Change Update'}
ael_variables = [['Curve', 'ZAR Curve', acm.FYieldCurve, listOfYieldCurves(), None, 1, 0, 'End of business curve, used to calculate spread changes compared to SOB curve', None, 1],
['updateCurve', 'Update Curve', acm.FYieldCurve, listOfYieldCurves(), None, 1, 0, 'Curve that will be updated with equal and opposite\nspread changes found in above curve comparison', None, 1],
['simulate', 'Simulate', 'string', ['No', 'Yes'], 'Yes', 1, 0, 'Only output values and changes, no changes will be made to the DB', None, 1]]

def ael_main(dict):
    zar_basis_yc = dict['Curve']
    
    usd_yc = dict['updateCurve']

    eod_spreads = zar_basis_yc.Attributes().First().Spreads()
    
    day_spreads = DateDict()
    
    for endSpread in eod_spreads:
        if endSpread.Point().DatePeriod():
            day_spreads[endSpread.Point().DatePeriod()] = endSpread.Spread()
      
    usd_spreads = usd_yc.Attributes().First().Spreads()
    for us in usd_spreads:
        try:
            ycPnt = us.Point()
            spreadAdjust = day_spreads[ycPnt.DatePeriod()]
                        
            print "Spread diff for %s in %s is: %f" % (ycPnt.DatePeriod(), zar_basis_yc.Name(), spreadAdjust) 
                
            if (spreadAdjust != 0.0):
                newValue = -0.005 - spreadAdjust
                print "\tAdjusting %s's current value of %f for %s by (-.5(50 bps) - (%f)) to %f" % (usd_yc.Name(), us.Spread(), ycPnt.DatePeriod(), spreadAdjust, newValue) 
                
                if dict['simulate'] == 'No':
                    us.Spread(newValue)
                    us.Commit()
                    print "\tCommit - Done"
        except KeyError, ke:
            print "Commit Failed For This Period :%s "%(us.Point().DatePeriod())
            
    print "Completed Successfully ::"        
    
