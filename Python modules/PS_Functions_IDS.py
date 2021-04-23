#************************************************************************************************************************
#Script Name             :PS_Functions_IDS
#Description             :Extention on PS_Functions specific to IDS
#Developer               :Momberg Heinrich
#CR Number(s)            :ABITFA-605(IDS)
#************************************************************************************************************************
import ael, acm

#***********************************************************************************************
# Public variables
#***********************************************************************************************
calendar = acm.FCalendar['ZAR Johannesburg']
INCEPTION = acm.Time().DateFromYMD(1970, 1, 1)
TODAY = acm.Time().DateToday()
FIRSTOFYEAR = acm.Time().FirstDayOfYear(TODAY)
FIRSTOFMONTH = acm.Time().FirstDayOfMonth(TODAY)
YESTERDAY = acm.Time().DateAddDelta(TODAY, 0, 0, -1)
TWODAYSAGO = acm.Time().DateAddDelta(TODAY, 0, 0, -2)
PREVBUSDAY = calendar.AdjustBankingDays(TODAY, -1)
TWOBUSDAYSAGO = calendar.AdjustBankingDays(TODAY, -2)

startDateList   = {'Inception':INCEPTION,
                   'First Of Year':FIRSTOFYEAR,
                   'First Of Month':FIRSTOFMONTH,
                   'PrevBusDay':PREVBUSDAY,
                   'TwoBusinessDaysAgo':TWOBUSDAYSAGO,
                   'TwoDaysAgo':TWODAYSAGO,
                   'Yesterday':YESTERDAY,
                   'Custom Date':TODAY,
                   'Now':TODAY} 
startDateKeys = startDateList.keys()
startDateKeys.sort()

endDateList     = {'Now':TODAY,
                   'TwoDaysAgo':TWODAYSAGO,
                   'PrevBusDay':PREVBUSDAY,
                   'Yesterday':YESTERDAY,
                   'Custom Date':TODAY}
endDateKeys = endDateList.keys()
endDateKeys.sort()



#***********************************************************************************************
# Method name:  _getCallAccounts
# Description:  Finds all the call accounts for the passed party
# Parameters:   party - The name of a counter party
# Return Type:  array
#***********************************************************************************************
def getCallAccounts(portfolio, party):
    
    query = acm.CreateFASQLQuery('FTrade', 'AND')
    op = query.AddOpNode('AND')
    op.AddAttrNode('Counterparty.Oid', 'EQUAL', party.Oid())
    
    if(portfolio):
        op = query.AddOpNode('AND')
        op.AddAttrNode('Portfolio.Name', 'EQUAL', portfolio.Name())
    
    op = query.AddOpNode('AND')
    op.AddAttrNode('Instrument.InsType', 'EQUAL', acm.EnumFromString('InsType', 'Deposit'))
    
    op = query.AddOpNode('AND')
    op.AddAttrNode('Instrument.OpenEnd', 'EQUAL', acm.EnumFromString('OpenEndStatus', 'Open End') )
    
    for status in ['Void', 'Confirmed Void', 'Simulated', 'Terminated']:
        op.AddAttrNode('Status', 'NOT_EQUAL', acm.EnumFromString('TradeStatus', status))
    
    callAccounts = []
    for trade in query.Select():
        callAccounts.append(trade.Instrument())

    return callAccounts


# Method name:  _getReportTypes
# Description:  Finds all the call accounts for the passed party
# Parameters:   party - The name of a counter party
# Return Type:  array
#***********************************************************************************************
def getReportTypes():
    types = ['.pdf', '.csv']
    return types



#***********************************************************************************************
# Method name:  _getXSLTemplates
# Description:  Finds all prime services extension modules of type xsl template 
# Return Type:  array
#***********************************************************************************************
def getXSLTemplates():
        xmlTemplates = []
        context         = acm.GetDefaultContext()
        primeModule     = context.GetModule('Prime Services')
        if not primeModule:
            raise Exception('Prime Service extension module not found')
        
        for d in primeModule.Definitions():
            if str(d.TypeClass()) == 'FXSLTemplate':
                xmlTemplates.append(d.Name())
            
        return xmlTemplates
