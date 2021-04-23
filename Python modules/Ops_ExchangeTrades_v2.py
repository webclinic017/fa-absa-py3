import ael, acm

'''
Purpose                       :  [Updated column definitions to map from 322 to 43],[Amended dump filename],
                                [Added new column for normalised traded price],
                                [Added new columns and adapted to include updated trades],[Added column DealtAIP]
Department and Desk           :  [PCG],[PCG],[Intellimatch],[Intellimatch],[Intellimatch]
Requester                     :  [Charl theron],[Charl theron],[Marius Atkinson],[Marius Atkinson],[Bruce Mukhola]
Developer                     :  [Ickin Vural],[Anwar Banoo],[Anwar Banoo],[Ickin Vural],[Willie van der Bank]
CR Number                     :  [C000000176544],[C000000249668],[C000000290033],[C000000373935,C000000412920],[C000000749362 23/09/2011]


History
=======
2017-08-02 Vojtech Sidorin  FAU-2899: Replace NominalAtDate, which is missing in FA 2017.
'''

class PortfolioSheetCalcSpace( object ):
    CALC_SPACE = acm.FCalculationSpace('FPortfolioSheet' )
    @classmethod
    def get_column_calc( cls, obj, column_id ):
        calc = PortfolioSheetCalcSpace.CALC_SPACE.CreateCalculation( obj, column_id )
        return calc
        
class TradeSheetCalcSpace( object ):
    CALC_SPACE = acm.FCalculationSpace('FTradeSheet' )
    @classmethod
    def get_column_calc( cls, obj, column_id ):
        calc = TradeSheetCalcSpace.CALC_SPACE.CreateCalculation( obj, column_id )
        return calc


def get_Column(trade, col):   
   
    eval            = 0
    column          = col  
    eval            = PortfolioSheetCalcSpace.get_column_calc(trade, column)
    
    if eval:
        return eval.FormattedValue()
    else:
        return 0

def get_PL(trade, col):
    
    if acm.Time().AsDate(trade.Instrument().ExpiryDate()) < acm.Time().DateNow():
        return 0
    else:
        eval            = 0
        column          = col 
        eval            = PortfolioSheetCalcSpace.get_column_calc(trade, column)
      
        if eval:
            return eval.FormattedValue()
        else:
            return 0     


def get_PLUsedPriceEnd(trade, *rest):
    
    eval            = 0
    column          = 'Portfolio Profit Loss Price End Date'  
    eval            = TradeSheetCalcSpace.get_column_calc(trade, column)
    
    if eval:
        return eval.FormattedValue()
    else:
        return 0

   
        


ael_gui_parameters = {'hideExtracControls' : True,
                      'windowCaption' : 'Trade Extract'}
ael_variables = [ ['Filter', 'Filter', 'string', None, 'FrontArena_SafexTrade', 1],
                  ['FileName', 'File Name', 'string', None, 'FrontArena_SafexTrade', 1],
                  ['Path', 'Path', 'string', None, 'F:\\', 1]  ]

def ael_main(parameter, *rest):
    header = 'TradeRef, Instrument, InstrumentType, UnderlyingInstrument, UnderlyingInstrumentType, Portfolio, PortfolioID, CounterParty, Call/Put, StrikePrice, ' + \
             'Expiry, Quantity, Nominal, TradedPrice, CreateTime, TradeTime, ValueDay, ExternalID, FreeText1, FreeText2, OTC, ContractSize, QuoteType, ' + \
             'UnderlyingContractSize, UnderlyingQuoteType, Currency, PLPosStart, PLPosEnd, UsedPriceStart, UsedPriceEnd, CashStart, CashEnd, ValStart, ValEnd, ' + \
             'PLPeriodStart, PLPeriodEnd, TPL, TPLD, NormalisedTradePrice, UpdateTime, CreateTime, Status, DealtAIP \n'
    
    tradeFilter = parameter['Filter']
    path = parameter['Path']
    filename = parameter['FileName']
    
    filteredTrades = acm.FTradeSelection[tradeFilter]
    fileName = path + filename    
    
    outfile=  open(fileName, 'w')
    outfile.write(header)        
        
    print len(filteredTrades.Trades())
    
    if filteredTrades:
        tag = acm.CreateEBTag()
        periodStart = None
        periodEnd = None
        usedPriceStart = acm.FDictionary()
        usedPriceEnd = acm.FDictionary()
        calc_space = acm.Calculations().CreateStandardCalculationsSpaceCollection()
    
             
        tradeSet = [trade for trade in filteredTrades.Trades() if (ael.date_from_time(trade.UpdateTime()).to_string('%Y-%m-%d') >= acm.Time().DateToday() or ael.date_from_time(trade.CreateTime()).to_string('%Y-%m-%d') >= acm.Time().DateToday() )]
        
        for trade in tradeSet:
            
            instrument = trade.Instrument()
            if instrument.Otc() == 0:    
                outLine = trade.Name()
                outLine += ',' + instrument.Name()
                outLine += ',' + instrument.InsType()
                if instrument.Underlying():
                    outLine += ',' + instrument.Underlying().Name()
                    outLine += ',' + instrument.Underlying().InsType()
                else:
                    outLine += ',,' 
                
                outLine += ',' + trade.Portfolio().Name()
                outLine += ',' + str(trade.Portfolio().Oid())
                outLine += ',' + trade.Counterparty().Name()
                if instrument.InsType() == 'Option':
                    if instrument.IsCallOption():
                        optionType = 'Call'
                    else:
                        optionType = 'Put'        
                    outLine += ',' + optionType
                    outLine += ',' + str(instrument.StrikePrice())
                else:
                    outLine += ',,'                        
                outLine += ',' + instrument.ExpiryDate()
                outLine += ',' + str(trade.Quantity())
                outLine += ',' + str(trade.Calculation().Nominal(calc_space, trade.ValueDay(), "ZAR").Number())
                outLine += ',' + str(trade.Price())
                outLine += ',' + str(ael.date_from_time(trade.CreateTime()))
                outLine += ',' + trade.TradeTime()
                outLine += ',' + str(trade.ValueDay())
                outLine += ',' + str(trade.OptionalKey())
                outLine += ',' + str(trade.Text1())
                outLine += ',' + str(trade.Text2())
                outLine += ',' + 'No'
                outLine += ',' + str(instrument.ContractSize())
                outLine += ',' + str(instrument.QuoteType())
                
                normalisedTradePrice = trade.Price()                
                if instrument.Underlying():
                    outLine += ',' + str(instrument.Underlying().ContractSize())
                    outLine += ',' + str(instrument.Underlying().QuoteType())
                    if instrument.Underlying().QuoteType() == 'Per 100 Units':
                        normalisedTradePrice = trade.Price()/100.0
                else:
                    outLine += ',,'
                
                outLine += ',' + instrument.Currency().Name()                        
                
                outLine += ',' + str(get_PL(trade, 'Portfolio Profit Loss Position End')).replace(',', '')
                outLine += ',' + str(get_PL(trade, 'Portfolio Profit Loss Position End')).replace(',', '')
                
                if not usedPriceStart.HasKey(instrument.Oid()):
                    usedPriceStart[instrument.Oid()] = 0
                outLine += ',' + str(usedPriceStart[instrument.Oid()]).replace(',', '')
    
                if not usedPriceEnd.HasKey(instrument.Oid()):
                    usedPriceEnd[instrument.Oid()] = get_Column(trade, 'Portfolio Profit Loss Price End Date')
                outLine += ',' + str(usedPriceEnd[instrument.Oid()]).replace(',', '')
                
                outLine += ',' + str(get_Column(trade, 'Portfolio Cash Start' )).replace(',', '')
                outLine += ',' + str(get_Column(trade, 'Portfolio Cash End')).replace(',', '')
                
                
                
                #tr = acm.CreateTradeRow(trade,1)
                tr=trade
                               
                
                outLine += ',' + str(get_Column(tr, 'Portfolio Value End' )).replace(',', '')
                outLine += ',' + str(get_Column(tr, 'Portfolio Value End')).replace(',', '')
                
                if periodStart == None:
                    periodStart = ael.date(get_Column(trade, 'PLPeriodStart')).to_string('%Y-%m-%d')
                outLine += ',' + str(periodStart)
               
                if periodEnd == None:
                    periodEnd = ael.date(get_Column(trade, 'PLPeriodEnd')).to_string('%Y-%m-%d')
                outLine += ',' + str(periodEnd)                        
                
                outLine += ',' + str(get_Column(tr, 'Portfolio Total Profit and Loss')).replace(',', '')
                outLine += ',' + str(get_PL(tr, 'Portfolio Profit Loss Position End')).replace(',', '')
                outLine += ',' + str(normalisedTradePrice)
                
                outLine += ',' + ael.date_from_time(trade.UpdateTime()).to_string('%Y-%m-%d')
                outLine += ',' + ael.date_from_time(trade.CreateTime()).to_string('%Y-%m-%d')
                
                outLine += ',' + str(trade.Status())
                outLine += ',' + str(ael.Instrument[instrument.Underlying().Oid()].dirty_from_yield(ael.Instrument[instrument.Oid()].exp_day.add_banking_day(ael.Instrument['ZAR'], 3), None, None, trade.Price()))
                
                outfile.write(outLine + '\n')    
    
        
  
    outfile.close()
    print "Complete"
