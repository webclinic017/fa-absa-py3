
''' =======================================================================================================
    Purpose                 	:   Added Enumeration Type for FXCash instrument , as well as functions for 
                                :   handling FXCash Instruments
    Department and Desk     	:   SM IT Pricing & Risk
    Requester               	:   Matthew Berry
    Developer               	:   Babalo Edwana
    CR Number              	    :   261644
    
    Changes			            : New Function Added to return the Nominal Currency for a trade, Function will replace the use
				                : of SANLD_NOMINALCURR.get_nomcurr_final.
				
				                : Added new Function to determine an inverted trade, functionality need for FX Option Strategy GUI
    Date			            : 12/04/2010 , 10/02/2011
    Developer		            : Babalo Edwana
    Requester		            : Mathew Berry
    CR Number		            : 282095, 571776
				
				                : Modified TradeIsInverted and getNominalCurrency function to work for futures
    Date			            : 24/11/2011
    Developer		            : Jan Mach
    Requester		            : Mathew Berry
    CR Number		            : 840456

    Change		                : Added function to convert floating point value to String presentation
    Date			            : 07/09/2011
    Developer		            : Babalo Edwana
    Requester		            : Mathew Berry
    CR Number		            : CHNG0000440842

    Changes 	                : Fixed FloatToStrFormat
    Date                        : //2012
    Developer                   : Jan Mach
    Requester                   : Mathew Berry
    CR Number                   :  
    ======================================================================================================== '''

import ael
import time

from DateUtils import PDate
from TMS_Config_Static import CALENDAR_MAPPING
import acm,FBDPCommon,string
import TMS_Functions

DATE_FORMAT = "%Y-%m-%d"

"""
Enumeration class for trade_process field implemented in front 4.3
"""
class EnumFXCash:
    FXSPOT = 4096
    FORWARD = 8192
    SWAP_NEAR_LEG = 16384
    SWAP_FAR_LEG = 32768
    
class Memoize:
    """Memoize(fn) - an instance which acts like fn but memoizes its arguments
       Will only work on functions with non-mutable arguments
    """
    def __init__(self, fn):
        self.fn = fn
        self.memo = {}

    def __call__(self, *args):
        if not self.memo.has_key(args):
            self.memo[args] = self.fn(*args)

        return self.memo[args]

class Callable:
    """ Little wrapper class which we will use to create static methods 
    """
    def __init__(self, anycallable):
        self.__call__ = anycallable
           
def otherleg(trade):
    if trade:
        acmTrade = acm.FTrade[trade.trdnbr]
        if acmTrade.IsFxSwapNearLeg():
            trd_far_leg = acm.FTrade.Select01("connectedTrdnbr=%i and oid<>%i" % (acmTrade.Oid(), acmTrade.Oid()), "")
            if trd_far_leg:
                return trd_far_leg
        elif acmTrade.IsFxSwapFarLeg():
            trd_near_leg_nbr = acmTrade.ConnectedTrdnbr()
            if trd_near_leg_nbr:
                trd_near_leg = acm.FTrade[trd_near_leg_nbr]
            if trd_near_leg:
                return trd_near_leg

def ReformatDate(date, format = DATE_FORMAT, inputformat = DATE_FORMAT):
    return PDate(date, inputformat).strftime(format)

def Date ():
    return time.strftime(DATE_FORMAT, time.localtime())

def setAdditionalInfo(entity, addInfo_fieldName, value):
    existing_addinfos = {}
    for ai in entity.additional_infos():
        existing_addinfos[ai.addinf_specnbr.field_name] = ai

    if existing_addinfos.has_key(addInfo_fieldName):
        new = existing_addinfos[addInfo_fieldName].clone()
    else:
        ai_spec = ael.AdditionalInfoSpec[addInfo_fieldName].clone()
        new = ael.AdditionalInfo.new(entity.clone())
        new.addinf_specnbr = ai_spec

    new.value = value
    new.commit()
    
#Get an additional info field from an Arena Entity.
def getAdditionalInfo(entity, addInfo_fieldName):
    #get the specnbr for the additional info specification
    #as given by addInfo_fieldName
    spec_search = [ai for ai in ael.AdditionalInfoSpec \
                    if ai.field_name == addInfo_fieldName]
    if spec_search != []:
        #Get the value property from the add info table belonging
        #to entity
        lstReturn = [ai.value for ai in entity.additional_infos() \
                    if ai.addinf_specnbr == spec_search[0]]
        return lstReturn != [] and lstReturn[0] or None

def setTradeAddInfo(trade, fieldName, value):
    try:
        setAdditionalInfo(trade, fieldName, value)
    except Exception, e:
        return "The additional info field \"%s\" could not be set to \"%s\" on trade %d - %s" \
            % (fieldName, value, trade.trdnbr, e)
    
    return "Success"

def getPrfParent(prf):
    parents = list(ael.PortfolioLink.select("member_prfnbr=%s" % prf.prfnbr))

    if parents:
        #A portfolio has a single parent so get it.
        return parents[0].owner_prfnbr

def _getPrfChildren(prf, result):
    children = list(ael.PortfolioLink.select("owner_prfnbr=%s" % prf.prfnbr))
    if children:
        for c in children:
            result.append(c.member_prfnbr.prfnbr)
            _getPrfChildren(c.member_prfnbr, result)

def getPrfChildren(prf):
    children = []
    _getPrfChildren(prf, children)
    return children

def getTimeSeriesDict(instr, timeseries):
    return dict([(ReformatDate(ts.day), ts.value) for ts in instr.time_series() if ts.ts_specnbr.field_name == timeseries])

def _isPrfElement(somePrf, childPrf):
    """ This function will return true if somePrf is an ancestor of childPrf (i.e. childPrf is contained within some subtree of somePrf) """
    prf = getPrfParent(childPrf)
    if prf:
        return prf == somePrf and True or _isPrfElement(somePrf, prf)
    else:
        return False

#We will memoize this function for speed-up
_isPrfElement = Memoize(_isPrfElement)

def isPrfElement(somePrf, childPrf):
    #_isPrfElement = Memoize(_isPrfElement)
    return _isPrfElement(somePrf, childPrf)

def Get_BarCap_Calendar(*calendars):
    #Join the mapped BarCap calendars into a string with infixed "+"
    return "+".join( [CALENDAR_MAPPING[cal] for cal in calendars if CALENDAR_MAPPING.has_key(cal)])

def GetDeliveryDate(trade):
    instr = trade.insaddr
    return max([instr.exp_day.add_banking_day(ccy,instr.pay_day_offset) for ccy in (instr.und_insaddr,instr.strike_curr)])

def getNominalCurrency(obj_Trade):
    curr_pair = ''
        
    obj = FBDPCommon.is_acm_object(obj_Trade) and obj_Trade or FBDPCommon.ael_to_acm(obj_Trade)
    
    if obj.RecordType() == 'Instrument':
        if obj.InsType() == 'Option':
            curr_pair = '/'.join([x for x in (obj.StrikeCurrency().Name(),obj.Underlying().Currency().Name())])
        else:
            curr_pair = '/'.join([x for x in (obj.Currency().Name(),obj.Underlying().Currency().Name())])
    elif obj.RecordType() == 'Trade':
        acmIns = obj.Instrument()
        if acmIns.InsType() == 'Curr' or acmIns.Underlying().InsType() == 'Curr':
            curr_pair = '/'.join ([x for x in (obj.Currency().Name(),acmIns.Name())])
            
    nom_curr = acm.FCurrencyPair.Select('name = %s' % (curr_pair))
    if not nom_curr:
        pairList = string.split(curr_pair,'/')
        curr_pair_rev = '/'.join ([pairList[x] for x in range(1,-1,-1)])
        nom_curr = acm.FCurrencyPair.Select('name = %s' % (curr_pair_rev))
    
    return (nom_curr and nom_curr.At(0).Currency1().Name() or '')

def TradeIsInverted(obj_Trade):
    
    obj = FBDPCommon.is_acm_object(obj_Trade) and obj_Trade or FBDPCommon.ael_to_acm(obj_Trade)
    acmIns = obj.Instrument()
    nominal_currency = getNominalCurrency(acmIns)

    if acmIns.InsType() == 'Option':
        trade_currency = acmIns.StrikeCurrency().Name()
    else:
        trade_currency = acmIns.Currency().Name()
            
    return (nominal_currency == trade_currency)
    
def GetSalesPersonList(trade, instr):
    salesPersonList = []
    
    if trade and instr:
                
        if (trade.sales_person_usrnbr):
            salesPersonList.append(TMS_Functions.Get_BarCap_User_ID(trade.sales_person_usrnbr))
            
        for i in range(2,6):
            if getAdditionalInfo(instr, "Sales_Person%i" % i):
                salesPersonList.append(TMS_Functions.Get_BarCap_User_ID(ael.User[getAdditionalInfo(instr, "Sales_Person%i" % i)]))
        
    return salesPersonList

def FloatToStrFormat(value, decimalPrecision=17):
    if value!=None:
        sFormat = "{0:.%df}" %(decimalPrecision)
        return sFormat.format(value).rstrip('0').rstrip('.')
