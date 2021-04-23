'''-----------------------------------------------------------------------
MODULE
    DCRM_CDS

DESCRIPTION
    This module is called by the DCRM ASQLs to return the Credit Curve 
    as well as the risk associated with the Credit Curve 

    Department and Desk : Credit Desk
    Requester           : De Clercq Wentzel
    Developer           : Herman Hoon

    History:
    When: 	  CR Number:   Who:		What:       
    2010-05-24    203010       Herman Hoon	Created

    When:           CR Name:                                                Who:            What:       
    2021-01-15      FAFO-179 Adding sorting by new field called tenor date  Tsebo Mokoena   Updated



END DESCRIPTION
-----------------------------------------------------------------------'''
import ael, acm, string
from string import upper
from FAFOUtils import get_calendar_banking_date
from at_time import acm_datetime
from at_logging import getLogger

LOGGER = getLogger(__name__)
debug = 0

def getCreditCurve(i, *rest):
    '''
Returns the credit curve connected to a CDS instrument
    '''
    ins = acm.FInstrument[i.insid]
    try:
        return ins.MappedCreditLink().Link().YieldCurveComponent().Curve().Name()
    except:
        return ''

def getCurveStrip(ycp, *rest):
    return upper(ycp.date_period)

def getCurveStripLower(ycp, *rest):
    return ycp.date_period

def get_tenor_date(ycp, *rest):
    try:
        date = acm_datetime(str(ycp.date_period))
        zar_jhb_calendar = 'ZAR Johannesburg'
        return get_calendar_banking_date(date, zar_jhb_calendar)
    except Exception as error:
        LOGGER.exception(error)

def credspread_delta_shift(temp, ycn, shiftsize, tr, party, dunit, *rest):
    '''
Calculates the risk, by shifting the the spread of each point of the Attribure spread curve
    '''
    t  = ael.Trade[int(tr)]
    yc = ael.YieldCurve[ycn].clone()

    pv0 = t.present_value()
    pv1 = 0
    
    for member in yc.attributes():
        if member.issuer_ptynbr.ptyid == party:
        
            for SpreadMember in member.spreads():
                if (str)(SpreadMember.point_seqnbr.date_period) == dunit:

                    spr0 = SpreadMember.spread
                    
                    spr1 = spr0 + shiftsize
                    SpreadMember.spread = spr1
                    
                    yc.simulate()
                    pv1 = t.present_value()
                    yc.unsimulate()
                    
                    if debug == 1:
                        print yc.yield_curve_name
                        print party
                        print dunit
                        print 'spr0', spr0
                        print 'spr1', spr1
                        print 'pv0', pv0 
                        print 'pv1', pv1
                    
                    x = (pv1 - pv0)
                    return x
    return -1
    
def recovery_shift(temp, ycn, shiftsize, tr, party, *rest):
    '''
Calculates the risk, by shifting the the recovery rate of the Attribure spread curve
    '''
    t  = ael.Trade[int(tr)]
    yc = acm.FYieldCurve[ycn]
    
    pv0 = t.present_value()
    pv1 = 0
    
    for attribute in yc.Attributes():
        if str(attribute.AttributeName()) == party:
            
            recRate = attribute.Clone()
            recRate.RecoveryRate = recRate.RecoveryRate() + shiftsize
            
            attribute.Apply(recRate)
            pv1 = t.present_value()
            attribute.Undo()
  
            pv01 = pv1 - pv0 
    return pv01
