'''mkReadSheet: last updated on Sat Nov 21 13:57:34 2009. Extracted by Stowaway on 2009-11-21.'''
import acm
import ael
'''-----------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------'''
TradeFilterList = []
for tf in acm.FTradeSelection.Select(''):
    TradeFilterList.append(str(tf.Name()))
TradeFilterList.sort()
testlist = ['TManager_LandingArea_Bonds', 'TManager_LandingArea_BsB', 'TManager_landingArea_Combin', 'TManager_LandingArea_Curr', 'TManager_landingArea_FRN', 'TManager_landingArea_Fut_Fwd', 'TManager_landingArea_Options']
'''-----------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------'''
CurrencyList = []
for curr in acm.FCurrency.Select(''):
    CurrencyList.append(str(curr.Name()))
CurrencyList.sort()
'''-----------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------'''
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
'''-----------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------'''
ael_variables = \
[
['tradeFilter', 'TradeFilter', 'string', testlist, None],
['filePath', 'File and Path', 'string', None, 'F:/Output.txt'],
['currency', 'Valuation Currency', 'string', CurrencyList, 'ZAR'],
['startDate', 'Start Date', 'string', StartDateList.keys(), 'Inception', 0, 0, '', None, 1],
['startDateCustom', 'Start Date Custom', 'string', None, INCEPTION.to_string(ael.DATE_ISO), 0, 0, 'Set the grouping wanted for each portfolio', None, 1],
['endDate', 'End Date', 'string', EndDateList.keys(), 'Now', 0, 0, '', None, 1],
['enddateCustom', 'End Date Cutom', 'string', None, TODAY.to_string(ael.DATE_ISO), 0, 0, '', None, 1],
]
'''-----------------------------------------------------------------------------------------------------------
LandingArea_Curr
-----------------------------------------------------------------------------------------------------------'''
def ael_main(ael_dict):

    columnId   = 'Portfolio Currency'
    tf         = acm.FTradeSelection[ael_dict['tradeFilter']]
    #sheetType  = 'FPortfolioSheet'     
    sheetType  = 'FTradeSheet'     
    filePath   = ael_dict['filePath'] #+ '_' + ael_dict['tradeFilter'] + '.TAB'           
    file       = open(filePath, 'w')
    calcSpace  = acm.Calculations().CreateCalculationSpace('Standard', sheetType)
    
    
    Heading =  'TrdNbr' + '\t' + 'HVal'
    file.writelines(Heading + "\n")
    
    if ael_dict['startDate'] == 'Custom Date':
        startDate = ael_dict['startDateCustom']
    else:
        startDate = str(StartDateList[ael_dict['startDate']])

    if ael_dict['endDate'] == 'Custom Date':
        endDate = ael_dict['enddateCustom']
    else:
        endDate = str(EndDateList[ael_dict['endDate']])
    
    print startDate
    print endDate
    
    calcSpace.SimulateGlobalValue('Portfolio Profit Loss Start Date', 'Custom Date')
    calcSpace.SimulateGlobalValue('Portfolio Profit Loss End Date', 'Custom Date')
    calcSpace.SimulateGlobalValue('Portfolio Profit Loss Start Date Custom', startDate)
    calcSpace.SimulateGlobalValue('Portfolio Profit Loss End Date Custom', endDate)
    calcSpace.SimulateValue(tf, columnId, ael_dict['currency'])
    topnode = calcSpace.InsertItem(tf)
    #grouper1           = acm.Risk().GetGrouperFromName('Currency')
    #grouper2           = acm.Risk().GetGrouperFromName('Currency')
    #ch_grouper      = acm.FChainedGrouper([grouper1,grouper2])
    calcSpace.Refresh()
    portfolioIter       = calcSpace.RowTreeIterator().FirstChild()  
    childIter           = portfolioIter.FirstChild()
    Count               = 0
    while childIter:
   
        Trade           = acm.FTrade[childIter.Tree().Item().StringKey()]
        #Remove CRE trades from overwrite file
        ex_val = Trade.add_info('ExternalVal')
        port_ai = Trade.Portfolio().add_info('MTM_From_External')
        
        #print childIter.Tree().StringKey(), 'ex_val ', ex_val, 'port-ai ', port_ai
        if (port_ai != 'Yes') or (not ex_val):
            #print 'NOT CRE TRADE'
            if Trade.Instrument().InsType() == 'Curr':
            
                if Trade.TradeProcess() in (8192, 4096):
                    ValEnd  = calcSpace.CalculateValue(childIter.Tree(), 'Portfolio Value End')
                    try:
                        num         = str(ValEnd.Value().Number())
                        Line        =  childIter.Tree().Item().StringKey() + '\t' + num
                        file.writelines(Line + "\n")
                    except:
                        print 'could not find val'
            
                if Trade.TradeProcess() == 32768:

                    
                    ValEndFarLeg     = calcSpace.CalculateValue(childIter.Tree(), 'Portfolio Value End')
                    NearTrade        = acm.FTrade[Trade.ConnectedTrdnbr()]


                    calcSpace.SimulateValue(NearTrade, columnId, ael_dict['currency'])
                    ValEndNearLeg    = calcSpace.CalculateValue(NearTrade, 'Portfolio Value End')
                    calcSpace.RemoveSimulation(NearTrade, columnId)

                    try:
                        num         = str(ValEndNearLeg.Value().Number() + ValEndFarLeg.Value().Number())
                        Line        = str(Trade.Oid()) + '\t' + num

                        file.writelines(Line + "\n")
                    except:
                        print 'could not find val'
            else:

                try:
                                
                    ValEnd  = calcSpace.CalculateValue(childIter.Tree(), 'Portfolio Value End')
                    num     = str(ValEnd.Value().Number())
                    Line    =  childIter.Tree().Item().StringKey() + '\t' + num
                    file.writelines(Line + "\n")
                except:
                    print 'could not find val'

        childIter = childIter.NextSibling()

    calcSpace.RemoveSimulation(tf, columnId)
    calcSpace.RemoveGlobalSimulation('Portfolio Profit Loss Start Date')
    calcSpace.RemoveGlobalSimulation('Portfolio Profit Loss End Date')
    calcSpace.RemoveGlobalSimulation('Portfolio Profit Loss Start Date Custom')
    calcSpace.RemoveGlobalSimulation('Portfolio Profit Loss End Date Custom')
    file.close()
'''-----------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------'''
