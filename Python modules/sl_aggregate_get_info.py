"""-----------------------------------------------------------------------------
PROJECT                 :  Security Borrowing and Lending
PURPOSE                 :  Retrives details of an aggregated trade
DEPATMENT AND DESK      :  Prime Services, Securities Lending
REQUESTER               :  Linda Breytenbach
DEVELOPER               :  Francois Truter
CR NUMBER               :  371587
-----------------------------------------------------------------------------"""

import ael
import acm
import sl_functions
import sys, csv

def _projectedCashFlow(trade, instrument, leg, cashflow):
    nsTime = acm.Time()
    dayCount = instrument.DayCountMethod()
    if dayCount == 'None':
        dayCount = acm.EnumFromString('DaycountMethod', 'Act/365')
    daysInYear = nsTime.YearLength(dayCount)
    period = nsTime.DateDifference(cashflow.EndDate(), cashflow.StartDate()) / daysInYear
    return period * trade.Quantity() * instrument.RefValue() * instrument.RefPrice() * instrument.Underlying().Quotation().QuotationFactor() * leg.FixedRate() / 100 * -1
    
def _testProjectedCashFlowCalcs():
    ''' It is not possible to run the normal projected cashflow calculations on the archived cashflows. 
        The caluculations produce errors, because it accesses "deleted" records, therefore the calculations
        have been reproduced in _projectedCashFlow, this function was used to compare the calculations on 
        a few cashflows in order to get a sense of whether the calculations are producing consistent results.
    '''
    
    query = acm.CreateFASQLQuery('FCashFlow', 'AND')
                
    op = query.AddOpNode('AND')
    op.AddAttrNode('Leg.Instrument.InsType', 'EQUAL', acm.EnumFromString('InsType', 'SecurityLoan'))
    
    op = query.AddOpNode('AND')
    op.AddAttrNode('EndDate', 'LESS', '2010-04-30')
    
    errors = False
    for cashflow in query.Select():
        calc1 = acm.GetCalculatedValueFromString(cashflow, acm.GetDefaultContext(), "hybridProjectedCashFlowPosition", None).Value().Number()
        leg = cashflow.Leg()
        instrument = leg.Instrument()
        trades = instrument.Trades()
        if trades:
            trade = trades.First()
            calc1 = calc1 * trade.Quantity()
            calc2 = _projectedCashFlow(trade, instrument, leg, cashflow)
            if round(calc1, 4) != round(calc2, 4):
                print('err:', trade.Oid(), cashflow.PayDate(), calc1, calc2)
                errors = True
            else:
                print('ok')
            
    if errors:
        print('There were errors')
    else:
        print('No errors')    
        
class MyDialect(csv.excel):
    lineterminator = '\n'
    quoting = csv.QUOTE_NONNUMERIC
csv.register_dialect("myDialect", MyDialect)

def _writeDetails(trade, writer, prevTradeNumber = None):
    securityLoan = trade.Instrument()
    quantity = sl_functions.underlying_quantity(trade.Quantity(), securityLoan)
    legnbrs = ael.dbsql('SELECT legnbr FROM leg WHERE insaddr = %i' % securityLoan.Oid())
    for legnbr in legnbrs[0]:
        cfwnbrs = ael.dbsql('SELECT cfwnbr FROM cash_flow WHERE legnbr = %i ORDER BY pay_day' % legnbr[0])
        leg = acm.FLeg[legnbr[0]]
        for cfwnbr in cfwnbrs[0]:
            cashflow = acm.FCashFlow[cfwnbr[0]]
            writer.writerow([trade.Oid(), prevTradeNumber, quantity, securityLoan.RefPrice(), leg.FixedRate(), cashflow.PayDate(), _projectedCashFlow(trade, securityLoan, leg, cashflow), trade.CounterpartyId(), trade.PortfolioId()])

def _printAggregatedTradeInfo(aggregateTrade):
    trdnbrs = ael.dbsql('SELECT trdnbr FROM trade WHERE aggregate_trdnbr = %i and archive_status = 1 ORDER BY trdnbr DESC' % aggregateTrade.Oid())
    writer = None
    if trdnbrs and len(trdnbrs) > 0:
        writer = csv.writer(sys.stdout, 'myDialect')
        writer.writerow(['Trade Number', 'Prev Trade Number', 'Quantity', 'Loan Price', 'Rate', 'Pay Date', 'Cash Flow', 'Counterparty', 'Portfolio'])
    else:
        'No aggregated trades returned'

    tradeNumbers = []
    for trdnbr in trdnbrs[0]:
        tradeNumbers.append(trdnbr[0])
        
    for tradeNumber in tradeNumbers:
        trade = acm.FTrade[tradeNumber]
        if trade.SLPartialReturnIsPartOfChain():
            partialTrade = trade.SLPartialReturnFirstTrade()
            prevTradeNumber = None
            while partialTrade:
                if partialTrade.Oid() in tradeNumbers:
                    _writeDetails(partialTrade, writer, prevTradeNumber)
                    prevTradeNumber = partialTrade.Oid()
                    if trade.Oid() != partialTrade.Oid():
                        tradeNumbers.remove(partialTrade.Oid())
                else:
                    print('partialy returned trade %i not aggregated' % partialTrade.Oid())
                partialTrade = partialTrade.SLPartialReturnNextTrade()
        else:
            _writeDetails(trade, writer)
        writer.writerow([])

tradesKey = 'Trades'

#Variable Name, Display Name, Type, Candidate Values, Default, Mandatory, Multiple, Description, Input Hook, Enabled
ael_variables = [
    [tradesKey, 'Trade', 'FTrade', None, None, 1, 1, 'The aggregate trades to get information on', None, 1]
]

def ael_main(parameters):
    trades = parameters[tradesKey]
    for trade in trades:
        if trade.Aggregate() == 0:
            print('Trade %i is not and aggregate trade.' % trade.Oid())
        else:
            header = 'Details for trade %i' % trade.Oid()
            print(header)
            print('-' * len(header))
            _printAggregatedTradeInfo(trade)
