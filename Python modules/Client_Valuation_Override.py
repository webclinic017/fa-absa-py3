"""---------------------------------------------------------------------------------------------------------------
Project                 : Client Valuation Project
Purpose                 : Developed the feed for Exposure Management. 
                           
Department and Desk     : IT - CTB Primary Markets
Requester               : Phil Ledwaba
Developer               : Tshepo Mabena
CR Number               : 829680 
------------------------------------------------------------------------------------------------------------------"""
import acm
import ael
import OverrideFields

def TradeFiletrList():

    TradeFilterList = []
    for tf in acm.FTradeSelection.Select(''):
        TradeFilterList.append(str(tf.Name()))
    TradeFilterList.sort()
    List = ['TManager_LandingArea_Bonds', 'TManager_LandingArea_BsB', 'TManager_landingArea_Combin', 'TManager_LandingArea_Curr', 'TManager_landingArea_FRN', 'TManager_landingArea_Fut_Fwd', 'TManager_landingArea_Options', 'GNA_TM', 'TManager_landingArea_OptionsT']
    return List
    
def CurrencyList():     

    CurrencyList = []
    for curr in acm.FCurrency.Select(''):
        CurrencyList.append(str(curr.Name()))
    CurrencyList.sort()
    
    return CurrencyList

INCEPTION       = ael.date('1970-01-01')
today           = ael.date_today()
TODAY           = ael.date_today()
FIRSTOFYEAR     = TODAY.first_day_of_year()
FIRSTOFMONTH    = TODAY.first_day_of_month()
PREVBUSDAY      = TODAY.add_banking_day(ael.Calendar['ZAR Johannesburg'], -1)
TWOBUSDAYSAGO   = TODAY.add_banking_day(ael.Calendar['ZAR Johannesburg'], -2)  
TWODAYSAGO      = TODAY.add_days(-2)
YESTERDAY       = TODAY.add_days(-1)

StartDateList   = {'Inception': INCEPTION.to_string(ael.DATE_ISO), 'First Of Year': FIRSTOFYEAR.to_string(ael.DATE_ISO), 'First Of Month': FIRSTOFMONTH.to_string(ael.DATE_ISO), 'PrevBusDay': PREVBUSDAY.to_string(ael.DATE_ISO), 'TwoBusinessDaysAgo': TWOBUSDAYSAGO.to_string(ael.DATE_ISO), 'TwoDaysAgo': TWODAYSAGO.to_string(ael.DATE_ISO), 'Yesterday': YESTERDAY.to_string(ael.DATE_ISO), 'Custom Date': TODAY, 'Now': TODAY.to_string(ael.DATE_ISO),} 
EndDateList     = {'Now':TODAY.to_string(ael.DATE_ISO),'TwoDaysAgo':TWODAYSAGO.to_string(ael.DATE_ISO),'PrevBusDay':PREVBUSDAY.to_string(ael.DATE_ISO),'Yesterday':YESTERDAY.to_string(ael.DATE_ISO),'Custom Date':TODAY.to_string(ael.DATE_ISO)}


ael_variables = \
[
['tradeFilter', 'TradeFilter', 'string', TradeFiletrList(), None],
['filePath', 'File and Path', 'string', None, 'F:/Output.txt'],
['currency', 'Valuation Currency', 'string', CurrencyList(), 'ZAR'],
['startDate', 'Start Date', 'string', StartDateList.keys(), 'Inception', 0, 0, '', None, 1],
['startDateCustom', 'Start Date Custom', 'string', None, INCEPTION.to_string(ael.DATE_ISO), 0, 0, 'Set the grouping wanted for each portfolio', None, 1],
['endDate', 'End Date', 'string', EndDateList.keys(), 'Now', 0, 0, '', None, 1],
['enddateCustom', 'End Date Custom', 'string', None, TODAY.to_string(ael.DATE_ISO), 0, 0, '', None, 1],
]

def ael_main(ael_dict):

    columnId   = 'Portfolio Currency'
    tf         = acm.FTradeSelection[ael_dict['tradeFilter']]
    
    sheetType  = 'FTradeSheet'     
    filePath   = ael_dict['filePath'] 
   
    file       = open(filePath, 'w')
    calcSpace  = acm.Calculations().CreateCalculationSpace('Standard', sheetType)
    
    toCurr = ael_dict['currency']
    Heading =  'TrdNbr' + '\t' + 'Vega' + '\t' + 'Gamma'+ '\t' + 'EQDelta' + '\t' + 'YDelta' + '\t' + 'Volatility' + '\t' + 'DivDelta' + '\t' + 'EQGamma_Cash'
    file.writelines(Heading + "\n")
    
    if ael_dict['startDate'] == 'Custom Date':
        startDate = ael_dict['startDateCustom']
    else:
        startDate = str(StartDateList[ael_dict['startDate']])

    if ael_dict['endDate'] == 'Custom Date':
        endDate = ael_dict['enddateCustom']
    else:
        endDate = str(EndDateList[ael_dict['endDate']])
        
    calcSpace.SimulateGlobalValue('Portfolio Profit Loss Start Date', 'Custom Date')
    calcSpace.SimulateGlobalValue('Portfolio Profit Loss End Date', 'Custom Date')
    calcSpace.SimulateGlobalValue('Portfolio Profit Loss Start Date Custom', startDate)
    calcSpace.SimulateGlobalValue('Portfolio Profit Loss End Date Custom', endDate)
    calcSpace.SimulateValue(tf, columnId, ael_dict['currency'])
    topnode = calcSpace.InsertItem(tf)
        
    calcSpace.Refresh()
    portfolioIter       = calcSpace.RowTreeIterator().FirstChild()  
    childIter           = portfolioIter.FirstChild()
    Count               = 0
    while childIter:
   
        Trade           = acm.FTrade[childIter.Tree().Item().StringKey()]
        
        #Remove CRE trades from overwrite file
        ex_val = Trade.add_info('ExternalVal')
        port_ai = Trade.Portfolio().add_info('MTM_From_External')
                
        if (port_ai != 'Yes') or (not ex_val):
        
            Vega    = OverrideFields.get_Vega(Trade, endDate, toCurr)
            Gamma   = OverrideFields.get_Gamma(Trade, endDate, toCurr) 
            EQDelta = OverrideFields.get_EQDelta(Trade) 
            
            YDelta  = OverrideFields.get_YDelta(Trade, endDate, toCurr)
            Volatility    = OverrideFields.get_Volatility(Trade)
            DivDelta      = OverrideFields.get_DivDelta(Trade)
            EQGamma_Cash  = OverrideFields.get_EQGamma_Cash(Trade)
                                        
            try:
                Line    =  childIter.Tree().Item().StringKey() + '\t' + str('%f'%Vega) + '\t' + str('%f'%Gamma) + '\t' + str('%f'%EQDelta) + '\t' + str('%f'%YDelta) + '\t' + str('%f'%Volatility) + '\t' + str('%f'%DivDelta) + ' \t'+ str('%f'%EQGamma_Cash)
                file.writelines(Line + "\n")
            except:
                print 'Coul not write to file'

        childIter = childIter.NextSibling()

    calcSpace.RemoveSimulation(tf, columnId)
    calcSpace.RemoveGlobalSimulation('Portfolio Profit Loss Start Date')
    calcSpace.RemoveGlobalSimulation('Portfolio Profit Loss End Date')
    calcSpace.RemoveGlobalSimulation('Portfolio Profit Loss Start Date Custom')
    calcSpace.RemoveGlobalSimulation('Portfolio Profit Loss End Date Custom')
    file.close()
    print 'Wrote secondary output to::' + filePath 

