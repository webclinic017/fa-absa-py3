import ael, acm

# VuralIck Updated column definitions to map from 322 to 43 #

'''
Purpose                       :  Updated column definitions to map from 322 to 43
Department and Desk           :  PCG 
Requester                     :  Charl theron
Developer                     :  Ickin Vural
CR Number                     :  C000000176544 

Purpose                       :  Amended dump filename
Department and Desk           :  PCG 
Requester                     :  Charl theron
Developer                     :  Anwar Banoo
CR Number                     :  C000000249668

Purpose                       :  Added new column for normalised traded price
Department and Desk           :  Intellimatch
Requester                     :  Marius Atkinson
Developer                     :  Anwar Banoo
CR Number                     :  C000000290033


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


def get_PLPeriodStart(trade, *rest):   
   
    eval            = 0
    column          = 'PLPeriodStart'  
    eval            = PortfolioSheetCalcSpace.get_column_calc(trade, column)
    
    if eval:
        return eval.FormattedValue()
    else:
        return 0
    
def get_PLPeriodEnd(trade, *rest):
    
    eval            = 0
    column          = 'PLPeriodEnd'  
    eval            = PortfolioSheetCalcSpace.get_column_calc(trade, column)
    
    if eval:
        return eval.FormattedValue()
    else:
        return 0

def get_PLUsedPriceStart(trade, *rest):    
    
    return 0



def get_PLUsedPriceEnd(trade, *rest):
    
    eval            = 0
    column          = 'Portfolio Profit Loss Price End Date'  
    eval            = TradeSheetCalcSpace.get_column_calc(trade, column)
    
    if eval:
        return eval.FormattedValue()
    else:
        return 0
        
        
def get_PLPosStart(trade, *rest):
    
    if acm.Time().AsDate(trade.Instrument().ExpiryDate()) < acm.Time().DateNow():
        return 0
    else:
        eval            = 0
        column          = 'Portfolio Profit Loss Position End'  
        eval            = PortfolioSheetCalcSpace.get_column_calc(trade, column)
      
        if eval:
            return eval.FormattedValue()
        else:
            return 0
        
        
def get_PLPosEnd(trade, *rest):
         
    if acm.Time().AsDate(trade.Instrument().ExpiryDate()) < acm.Time().DateNow():
        return 0
    else:
        eval            = 0
        column          = 'Portfolio Profit Loss Position End'  
        eval            = PortfolioSheetCalcSpace.get_column_calc(trade, column)
      
        if eval:
            return eval.FormattedValue()
        else:
            return 0
    
        
        
def get_PLCashStart(trade, *rest):
   
    eval            = 0
    column          = 'Portfolio Cash Start'  
    eval            = PortfolioSheetCalcSpace.get_column_calc(trade, column)
   
    if eval:
        return eval.FormattedValue()
    else:
        return 0
        
        
def get_PLCashEnd(trade, *rest):

    eval            = 0
    column          = 'Portfolio Cash End'  
    eval            = PortfolioSheetCalcSpace.get_column_calc(trade, column)
   
    if eval:
        return eval.FormattedValue()
    else:
        return 0


def get_PLValStart(trade, ebTag, *rest):   
    
 
    eval            = 0
    column          = 'Portfolio Value Start'  
    eval            = PortfolioSheetCalcSpace.get_column_calc(trade, column)
  
    if eval:
        return eval.FormattedValue()
    else:
        return 0


def get_PLValEnd(trade, ebTag, *rest):
    
    eval            = 0
    column          = 'Portfolio Value End'  
    eval            = PortfolioSheetCalcSpace.get_column_calc(trade, column)
  
    if eval:
        return eval.FormattedValue()
    else:
        return 0

def get_PLTotal(trade, ebTag, *rest):
    
    eval            = 0
    column          = 'Portfolio Total Profit and Loss'  
    eval            = PortfolioSheetCalcSpace.get_column_calc(trade, column)
     
    if eval:
        return eval.FormattedValue()
    else:
        return 0
    
def get_PLTotalDaily(trade, ebTag, *rest):
       
    if acm.Time().AsDate(trade.Instrument().ExpiryDate()) < acm.Time().DateNow():
        return 0
    else:
        eval            = 0
        column          = 'Portfolio Profit Loss Position End'  
        eval            = PortfolioSheetCalcSpace.get_column_calc(trade, column)
      
        if eval:
            return eval.FormattedValue()
        else:
            return 0

ael_gui_parameters = {'hideExtracControls' : True,
                      'windowCaption' : 'Trade Extract'}
ael_variables = [ ['Filter', 'Filter', 'string', None, 'Exchange_Traded_Futures', 1],
                  ['Path', 'Path', 'string', None, 'F:\\', 1]  ]

def ael_main(parameter, *rest):
    header = 'TradeRef, Instrument, InstrumentType, UnderlyingInstrument, UnderlyingInstrumentType, Portfolio, CounterParty, Call/Put, StrikePrice, ' + \
             'Expiry, Quantity, Nominal, TradedPrice, CreateTime, TradeTime, ValueDay, ExternalID, FreeText1, FreeText2, OTC, ContractSize, QuoteType, ' + \
             'UnderlyingContractSize, UnderlyingQuoteType, Currency, PLPosStart, PLPosEnd, UsedPriceStart, UsedPriceEnd, CashStart, CashEnd, ValStart, ValEnd, ' + \
             'PLPeriodStart, PLPeriodEnd, TPL, TPLD, NormalisedTradePrice \n'
    
    tradeFilter = parameter['Filter']
    path = parameter['Path']
    
    filteredTrades = acm.FTradeSelection[tradeFilter]
    fileName = path + 'FrontArena_SafexTrade%s.csv' %(ael.date_today().to_string('%Y%m%d'))
    
    
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
    
        for trade in filteredTrades.Trades():        
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
                
                outLine += ',' + str(get_PLPosStart(trade)).replace(',', '')
                outLine += ',' + str(get_PLPosEnd(trade)).replace(',', '')
                
                if not usedPriceStart.HasKey(instrument.Oid()):
                    usedPriceStart[instrument.Oid()] = get_PLUsedPriceStart(instrument)
                outLine += ',' + str(usedPriceStart[instrument.Oid()]).replace(',', '')
    
                if not usedPriceEnd.HasKey(instrument.Oid()):
                    usedPriceEnd[instrument.Oid()] = get_PLUsedPriceEnd(trade)
                outLine += ',' + str(usedPriceEnd[instrument.Oid()]).replace(',', '')
                
                outLine += ',' + str(get_PLCashStart(trade, tag)).replace(',', '')
                outLine += ',' + str(get_PLCashEnd(trade, tag)).replace(',', '')
                
                
                
                #tr = acm.CreateTradeRow(trade,1)
                tr=trade
                               
                
                outLine += ',' + str(get_PLValStart(tr, tag)).replace(',', '')
                outLine += ',' + str(get_PLValEnd(tr, tag)).replace(',', '')
                
                if periodStart == None:
                    periodStart = get_PLPeriodStart(trade)
                outLine += ',' + str(periodStart)
               
                if periodEnd == None:
                    periodEnd = get_PLPeriodEnd(trade)
                outLine += ',' + str(periodEnd)                        
                
                outLine += ',' + str(get_PLTotal(tr, tag)).replace(',', '')
                outLine += ',' + str(get_PLTotalDaily(tr, tag)).replace(',', '')
                outLine += ',' + str(normalisedTradePrice)
                
                outfile.write(outLine + '\n')    
    
                
  
    outfile.close()
    print "Complete"
    
    
