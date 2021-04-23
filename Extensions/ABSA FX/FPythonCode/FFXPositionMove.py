'''================================================================================================
==============================================================================================='''
import acm
from FXUtils import PrettyPrint, CreateRollBackSpec, CreatRollBackData
calcSpace = acm.Calculations().CreateCalculationSpace('Standard', 'FPortfolioSheet')
current_portfolio = currency_paircurrency_pair = column_config = current_acquirer = rollbackSpec = None      
vector = queryfolderlist = acm.FArray()
date_today = acm.Time.DateNow()
dictionary = {}
RND = acm.FPhysicalPortfolio['RND'] 
[queryfolderlist.Add(query.Name()) for query in acm.FStoredASQLQuery.Select('')]
queryfolderlist.Sort()
'''================================================================================================
================================================================================================'''
def CreateNamedParam(vector, currency ):
    param = acm.FNamedParameters();
    param.AddParameter('currency', acm.FCurrency[currency])
    vector.Add( param )    
'''================================================================================================
================================================================================================'''
def CreateTrade(port, value_day, curreny_pair, calculation): 
    Quantity = calculation.Value()[0].Number()
    Premium = calculation.Value()[1].Number()
    if abs(Quantity) > 0.005 and abs(Premium) > 0.005:         
        trade = acm.FTrade()
        trade.Instrument(curreny_pair.Currency1()) 
        trade.Currency(curreny_pair.Currency2())
        trade.Acquirer(RND.PortfolioOwner())       
        trade.Portfolio(RND)  
        trade.Counterparty('FX SPOT')                
        trade.Price(abs(round(Premium/Quantity, 6))) 
        trade.Quantity(Quantity)
        trade.Premium(Premium)
        trade.ValueDay(value_day)
        trade.Status('Internal')
        trade.MirrorPortfolio(port)                 
        trade.AcquireDay(value_day)
        trade.TradeTime(acm.Time.TimeNow())
        trade.Text1('Postion Move')
        PrettyPrint(trade)
        return trade
'''===================================================================================================
==================================================================================================='''
def RecurseTree(node, calc_space):
    
    row         = node.Item()
    row_name    = row.StringKey()
    grouper     = row.GrouperOnLevel().StringKey() #FAttributeGrouper
    global vector, currency_pair, column_config, current_portfolio, rollbackSpec
    if grouper == 'Trade Portfolio': current_portfolio = acm.FPhysicalPortfolio[row_name]
   
    if grouper == 'Position Pair': 
        currency_pair = acm.FCurrencyPair[row_name]
        vector.Clear()
        if currency_pair != None:        
            CreateNamedParam(vector, currency_pair.Currency1().Name())
            CreateNamedParam(vector, currency_pair.Currency2().Name())
            column_config = acm.Sheet.Column().ConfigurationFromVector(vector)
    
    if grouper == 'Value Day' and row.Class() == acm.FMultiInstrumentAndTrades and currency_pair != None:
        if row_name > date_today:
            calculation = calc_space.CreateCalculation(node, 'Portfolio Projected Payments', column_config) #Portfolio Projected Payments Currency Pair'
            trade = CreateTrade(current_portfolio, row_name, currency_pair, calculation)
            if trade != None and dictionary['simulated'] == False: 
                trade.Commit()
                CreatRollBackData(rollbackSpec, trade).Commit()

    child_iter = node.Iterator().FirstChild()
    while child_iter:
        RecurseTree(child_iter.Tree(), calc_space)
        child_iter = child_iter.NextSibling()

'''================================================================================================
================================================================================================'''
ael_variables = \
[
['query', 'Query Folder', 'string', queryfolderlist, None, 0, 0, ''],
#['portFolio','Currency Pair',acm.FCurrencyPair,None,None,0,1,''],
#['currencyPair','Currency Pair',acm.FCurrencyPair,None,None,0,1,''],
['trade', 'Single Trade (will overite query folder)', acm.FTrade, None, None, 0, 1, ''],
['simulated', 'Simulated', 'int', [0, 1], 1, 0, 0, '', None, 1]
]
'''================================================================================================
================================================================================================'''
def ael_main(ael_dict):
    global dictionary, rollbackSpec
    dictionary = ael_dict
    object = ael_dict['trade'] if ael_dict['trade'].Size() > 0 else acm.FStoredASQLQuery[ael_dict['query']].Query()

    if object != None:
        top_node = calcSpace.InsertItem(object)
        grouper1 = acm.Risk().GetGrouperFromName('Trade Portfolio')  
        grouper2 = acm.Risk().GetGrouperFromName('Position Pair')
        grouper3 = acm.Risk().GetGrouperFromName('Value Day')
        ch_grouper = acm.FChainedGrouper([grouper1, grouper2, grouper3])
        top_node.ApplyGrouper(ch_grouper)
        calcSpace.Refresh()
        if dictionary['simulated'] == False: rollbackSpec = CreateRollBackSpec('PositionMove')
        RecurseTree(top_node, calcSpace)
'''================================================================================================
================================================================================================'''
def Run(eii): acm.RunModuleWithParameters('FFXPositionMove', acm.GetDefaultContext()) 
'''================================================================================================
================================================================================================'''



