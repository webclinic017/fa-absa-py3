'''
Purpose                       :  Updates the Prod_Vol add info field on all volatilities to indicate which are part of the ACMB GLobal Context. These
                                 are considered to be production volatilties. Used as part of audit listener as well.
Department and Desk           :  PCG MO
Requester                     :  Dirk Strauss
Developer                     :  Zaakirah Kajee
CR Number                     :  483599
Date                          :  2010-11-04
'''

import ael, acm,  SAGEN_IT_Functions

def setVolAddInfo():

    context = acm.FContext['ACMB Global']
    links =  acm.FContextLink.Select("context = %s and type = 'Volatility'" %context.Oid())
    vlist = []
    for l in links:
        vol = acm.FVolatilityStructure[l.Name()]
        und = vol.UnderlyingStructure()
        vlist.append(vol)
        while und:
            vol = vol.UnderlyingStructure()
            und = vol.UnderlyingStructure()
            vlist.append(vol)

    for vol in acm.FVolatilityStructure.Select(''):      
        if vol in vlist and (vol.AdditionalInfo().Prod_Vol() !=  True):
            SAGEN_IT_Functions.set_AdditionalInfoValue_ACM(vol, 'Prod_Vol', 'True')
        if vol not in vlist and (vol.AdditionalInfo().Prod_Vol() !=  False ):
            SAGEN_IT_Functions.set_AdditionalInfoValue_ACM(vol, 'Prod_Vol', 'False')

setVolAddInfo()
