import acm, os, csv, ael, math
from Eagle_Comm_Absa_Util import _hybridNominalPosition, date_from_timestamp
tag = acm.CreateEBTag() 
today = acm.Time().DateToday()
calc_space = acm.Calculations().CreateStandardCalculationsSpaceCollection()
import datetime


SOURCE_TRADE_ID = ''
SOURCE_LEG_ID =''
SOURCE_CASH_ID =''
SOURCE_RESET_ID = ''
RESET_TYPE = ''
RESET_VALUE = ''
RESET_DATE = ''
NOTIONAL = ''
RFIS_DATE = ''





def _resetType(reset):
    if reset.Day() < today:
        return 'FIXED'
    else:
        return 'PROJECTED'
     
def _resetValue(reset): 
    if _resetType(reset) == 'Fixed':
        return reset.FixingValue()
    
    else:
        value = 0
        try:
            sheetType  = 'FMoneyFlowSheet'
            context    = acm.GetDefaultContext()
            columnName = 'Cash Analysis Fixing Estimate'
            calcSpace  = acm.Calculations().CreateCalculationSpace( context, sheetType )
            v = calcSpace.CalculateValue( reset, columnName ).Value()              
            value = v.Value().Number()
        except:
            pass
        return value
                    
        
def _notional(reset, cashflow, leg, trade):
              
        notional = abs(_hybridNominalPosition(cashflow)*trade.Quantity())
        
        if trade.Quantity()> 0 and leg.PayLeg() :
            notional = notional*(-1)
        elif trade.Quantity() < 0 and leg.PayLeg()==False:
            notional = notional*(-1)
            
        
        if leg.ResetPeriod()!='0d':
        
            if reset.ResetType()=='Unweighted':
                weight = len(cashflow.Resets())
                notional = (notional/float(weight))
            else:
                days_betwn_cashflows = ael.date(cashflow.StartDate()).days_between(ael.date(cashflow.EndDate()))  
                
                bus_days_betwn_resets = ael.date(reset.StartDate()).days_between(ael.date(reset.Day()))  
                     
                
               
                weight = bus_days_betwn_resets/float(days_betwn_cashflows)
                
                notional = notional*weight
            
        return notional
        


def get_trades_data():
    
    queryName='EAGLE_PriceSwap'
    storedQuery = acm.FStoredASQLQuery.Select('user = 0 name="%s"' % queryName)[0]     
    all_trades3= storedQuery.Query().Select()
    
    return all_trades3
    
def writePriceSwapsResets(file):
    internaCount = 0
    internalChecksum = 0
    countChecksumDict = {}
    trades = get_trades_data() 
    RESET_DATE = ''
    
    for trade in trades:
    
        legs = trade.Instrument().Legs()
        for leg in legs:
            cashflows = leg.CashFlows()
            for cashflow in cashflows:
                if cashflow.PayDate()>today:
                    resets = cashflow.Resets()
                    for reset in resets:
                        RESET_VALUE = 0
                        value = 0
                        
                        try:                    
                            SOURCE_TRADE_ID = trade.Oid()
                        except:
                            pass
                        try:
                            SOURCE_LEG_ID = leg.Oid()
                        except:
                            pass
                        try:
                            SOURCE_CASH_ID = cashflow.Oid()
                        except:
                            pass
                        try:
                            SOURCE_RESET_ID = reset.Oid()
                        except:
                            pass
                        try:
                            RESET_TYPE = _resetType(reset)
                        except:
                            pass
                        try:
                            
                            value = _resetValue(reset)
                            if (not math.isnan(value)):
                                RESET_VALUE = value
                                
                                
                        except:
                            pass
                        try:                        
                            RESET_DATE = datetime.datetime.strptime(reset.Day(), '%Y-%m-%d').strftime('%Y%m%d')
                            
                        except Exception, e:
                            pass
                        
                        try:
                            NOTIONAL = _notional(reset, cashflow, leg, trade)
                        except Exception, e:
                            pass
                        
                        try:
                            RFIS_DATE = RESET_DATE
                        except Exception, e:
                            pass
                    
                        fields = ['030', SOURCE_TRADE_ID, SOURCE_LEG_ID, SOURCE_CASH_ID, SOURCE_RESET_ID, RESET_TYPE, RESET_VALUE, RESET_DATE, NOTIONAL, RFIS_DATE]
                        try:
                        
                            
                            writer = csv.writer(file, delimiter='|', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                            writer.writerow(fields)
                            
                            internaCount = internaCount + 1
                            
                            if (not math.isnan(value)):
                                internalChecksum = internalChecksum + value
                                
                        except Exception, e:
                            pass
                            

  
    countChecksumDict['counter'] =  internaCount
    countChecksumDict['checksum'] = internalChecksum
    return countChecksumDict

                    
                    
