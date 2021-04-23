import ael, acm
'''
Purpose                       :  [Position Data for Yield-X],[Added additional columns ClosingAIP and TPLD], [Added in a number of columns]
Department and Desk           :  [Intellimatch],[Intellimatch], [PCG]
Requester                     :  [Marius Atkinson],[Bruce Mukhola],[Diana Rodrigues]
Developer                     :  [Ickin Vural],[Willie van der Bank], [Jaysen Naicker]
CR Number                     :  [C000000373935,C000000412920,C000000462331,C000000519727],[C000000749362 23/09/2011][CHNG0000252498] 
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

def get_Column_Number(trade, col):   
   
    eval            = 0
    column          = col  
    eval            = TradeSheetCalcSpace.get_column_calc(trade, column)
    
    if eval:
        try:
            if eval.Value().Number().__str__() == 'nan':
                return 0
            else:
                return eval.Value().Number()
        except:
            return eval.Value()
    else:
        return 0


def get_ValStart(trade, *rest):    
    
    column = 'Portfolio Value Start'
    yesterday  = ael.date_today().add_banking_day(ael.Instrument['ZAR'], -1)
    
    try:   
        TradeSheetCalcSpace.CALC_SPACE.SimulateGlobalValue('Portfolio Profit Loss Start Date', 'Custom Date')
        TradeSheetCalcSpace.CALC_SPACE.SimulateGlobalValue('Portfolio Profit Loss Start Date Custom', yesterday)
        eval   = TradeSheetCalcSpace.get_column_calc(trade, column)
        out = float(eval.Value().Number())
    except Exception, e:
            out = 0
    finally:
        TradeSheetCalcSpace.CALC_SPACE.RemoveGlobalSimulation('Portfolio Profit Loss Start Date')
        TradeSheetCalcSpace.CALC_SPACE.RemoveGlobalSimulation('Portfolio Profit Loss Start Date Custom')        
        
    return out
    
def get_Column_PPLPED(trade, col):

    column = col  
    eval   = TradeSheetCalcSpace.get_column_calc(trade, column)
    
    if eval:
        try:       
            if eval.Value().Number().__str__() == 'nan':
                return 0
            else:
                return float(eval.Value().Number())
        except Exception, e:
            try:
                return float(eval.Value())
            except Exception, e:
                return 0
    else:
        return 0

        
def get_PLUsedPriceStart(trade, *rest):    
    
    column = 'Portfolio Profit Loss Price Start Date'
    yesterday  = ael.date_today().add_banking_day(ael.Instrument['ZAR'], -1)
    
    try:   
        TradeSheetCalcSpace.CALC_SPACE.SimulateGlobalValue('Portfolio Profit Loss Start Date', 'Custom Date')
        TradeSheetCalcSpace.CALC_SPACE.SimulateGlobalValue('Portfolio Profit Loss Start Date Custom', yesterday)
        eval   = TradeSheetCalcSpace.get_column_calc(trade, column)
        out = float(eval.Value())
    except Exception, e:
        out =  0
    finally:
        TradeSheetCalcSpace.CALC_SPACE.RemoveGlobalSimulation('Portfolio Profit Loss Start Date')
        TradeSheetCalcSpace.CALC_SPACE.RemoveGlobalSimulation('Portfolio Profit Loss Start Date Custom')        
        
    return out
        
      
def get_PLPosEnd(trade, *rest):
         
    if acm.Time().AsDate(trade.Instrument().ExpiryDate()) < acm.Time().DateNow():
        return 0
    else:
        eval            = 0
        column          = 'Portfolio Profit Loss Position End'  
        eval            = PortfolioSheetCalcSpace.get_column_calc(trade, column)
      
        if eval:
            return eval.Value()
        else:
            return 0


def get_PLPosStart(trade, *rest):
    
    if acm.Time().AsDate(trade.Instrument().ExpiryDate()) < acm.Time().DateNow():
        return 0
    else:
        eval            = 0
        yesterday  = ael.date_today().add_banking_day(ael.Instrument['ZAR'], -1)
        try:
            PortfolioSheetCalcSpace.CALC_SPACE.SimulateGlobalValue('Portfolio Profit Loss Start Date', 'Custom Date')
            PortfolioSheetCalcSpace.CALC_SPACE.SimulateGlobalValue('Portfolio Profit Loss Start Date Custom', yesterday)
            column          = 'Portfolio Profit Loss Position Start'  
            eval            = PortfolioSheetCalcSpace.get_column_calc(trade, column) 
            out = eval.Value()
        except:
            out = 0
        finally:
            PortfolioSheetCalcSpace.CALC_SPACE.RemoveGlobalSimulation('Portfolio Profit Loss Start Date')
            PortfolioSheetCalcSpace.CALC_SPACE.RemoveGlobalSimulation('Portfolio Profit Loss Start Date Custom')
        
    return out
            

def get_PLTotal(trade,  *rest):
    eval            = 0
    column          = 'Portfolio Total Profit and Loss'  
    eval            = PortfolioSheetCalcSpace.get_column_calc(trade, column)
     
    if eval:
        try:
            if eval.Value().Number().__str__() == 'nan':
                return 0
            else:
                return eval.Value().Number()
        except Exception, e:
            return 0
    else:
        return 0


def get_TPLD(trade, *rest):
    
    eval            = 0
    column          = 'Portfolio Total Profit and Loss Daily'  
    eval            = PortfolioSheetCalcSpace.get_column_calc(trade, column)
     
    if eval:
        try:
            if eval.Value().Number().__str__() == 'nan':
                return 0
            else:
                return eval.Value().Number()
        except Exception, e:
            return 0
    else:
        return 0
        
ael_gui_parameters = {'hideExtracControls' : True,
                      'windowCaption' : 'Trade Extract'}
ael_variables = [ ['Filter', 'Filter', 'string', None, 'FrontArena_Yield_X_Trades', 1],
                  ['FileName', 'File Name', 'string', None, 'FrontArena_Yield_X_Posistions', 1],
                  ['Path', 'Path', 'string', None, 'F:\\', 1]]


class HoldingObject( object ):
    Quantity = 0
    Nominal = 0
    CalcVal = 0

def ael_main(parameter, *rest):
    header = 'Portfolio, PortfolioID, Underlying.ContractSize, Instrument, Val Start, Val End, Currency, PLPosEnd, Contract Size, ' + \
             'Period Start, Period End, TPL, Used Price Start, Used Price End, InstrumentType, UnderlyingInstrument, ' + \
             'UnderlyingInstrumentType, Call/Put, Strike Price, Expiry, QuoteType, ClosingAIP, TPLD, ' + \
             'PLPosStart, QuotationFactor, NormalisedUnderlyingInstrument, NormalisedUsedPriceStart, NormalisedUsedPriceEnd, OpeningFrontNotional, ClosingFrontNotional,\n'
    
    tradeFilter = parameter['Filter']
    path = parameter['Path']
    filename = parameter['FileName']
    
    filteredTrades = acm.FTradeSelection[tradeFilter]
    fileName = path + filename
    
    
    outfile=  open(fileName, 'w')
    outfile.write(header)
    
    date = ael.date_today()
    
    
    cnt = 1
    if filteredTrades:
        
        InsPort = acm.FDictionary()

        for trade in filteredTrades.Trades():
            print cnt, len(filteredTrades.Trades())
            cnt += 1
            instrument = trade.Instrument()
            key = trade.Instrument().Name() + '|' + trade.Portfolio().Name()
            if not InsPort.HasKey(key):
                myObject = acm.FDictionary()
                
                portfolioName = trade.Portfolio().Name()
                
                myObject['Portfolio'] = portfolioName  #portfolio name
                pysicalPortfolio = acm.FPhysicalPortfolio[portfolioName]
                myObject['PortfolioNumber'] = str(pysicalPortfolio.Oid())  #portfolio number
                try:
                    myObject['Underlying ContractSize'] = instrument.Underlying().ContractSize() 
                except:
                    myObject['Underlying ContractSize'] = ',,'
                myObject['Instrument'] = trade.Instrument().Name() #instrument name
                myObject['Val Start'] = 0
                myObject['Val End'] = 0
                myObject['Currency'] = instrument.Currency().Name()
                myObject['PLPosEnd'] = 0
                myObject['PLPosStart'] = 0
                myObject['Contract Size'] = instrument.ContractSize()
                periodStart = date.add_banking_day(ael.Instrument['ZAR'], -1)
                myObject['Period Start'] = str(periodStart)
                periodEnd = get_Column(trade, 'PLPeriodEnd' )
                myObject['Period End'] = str(periodEnd)
                myObject['TPL'] = 0
                myObject['Used Price Start'] = 0
                myObject['Used Price End'] = 0
                myObject['TPLD'] = 0
                myObject['InstrumentType'] = instrument.InsType()
                try:
                    myObject['UnderlyingInstrument'] = instrument.Underlying().Name()
                except:
                    myObject['UnderlyingInstrument'] = ',,'
                try:
                    myObject['UnderlyingInstrumentType'] = instrument.Underlying().InsType()
                    if instrument.InsType() == 'Option':
                        if instrument.IsCallOption():
                            optionType = 'Call'
                        else:
                            optionType = 'Put'
                        myObject['Call/Put'] = optionType
                        myObject['Strike Price'] = str(instrument.StrikePrice())
                    else:
                        myObject['Call/Put'] = ',,'
                        myObject['Strike Price'] = ',,'
                except:
                    myObject['UnderlyingInstrumentType'] = ',,'
                    myObject['Call/Put'] = ',,'
                    myObject['Strike Price'] = ',,'
                myObject['Expiry'] = instrument.ExpiryDate()
                myObject['QuoteType'] = str(instrument.QuoteType())
                
                #The last three prices in the list will be the most recent internal, SPOT or SPOT_SOB.
                try:
                    if instrument.HistoricalPrices()[len(instrument.HistoricalPrices())-1].Market().Id() == 'internal':
                        price = instrument.HistoricalPrices()[len(instrument.HistoricalPrices())-1].Settle()
                    elif instrument.HistoricalPrices()[len(instrument.HistoricalPrices())-2].Market().Id() == 'internal':
                        price = instrument.HistoricalPrices()[len(instrument.HistoricalPrices())-2].Settle()
                    elif instrument.HistoricalPrices()[len(instrument.HistoricalPrices())-3].Market().Id() == 'internal':
                        price = instrument.HistoricalPrices()[len(instrument.HistoricalPrices())-3].Settle()

                    myObject['ClosingAIP'] = ael.Instrument[instrument.Underlying().Oid()].dirty_from_yield(ael.Instrument[instrument.Oid()].exp_day.add_banking_day(ael.Instrument['ZAR'], 3), None, None, price)
                except Exception, e:
                    myObject['ClosingAIP'] = 0
                
                myObject['QuotationFactor'] = instrument.Quotation().QuotationFactor()
                
                myObject['NormalisedUnderlyingInstrument'] = ''        
                
                if instrument.Underlying():
                    myObject['NormalisedUnderlyingInstrument'] = instrument.Underlying().Name()
                
                    if instrument.Underlying().InsType() in ('Commodity', 'Future/Forward'):
                        if instrument.Underlying().Name().lower().find('zar/') == 0:
                            myObject['NormalisedUnderlyingInstrument'] = instrument.Underlying().Name().split('/')[1]
                    elif instrument.Underlying().InsType() in ('EquityIndex'):
                        if instrument.Underlying().Name().lower().find('zar/') == 0:
                            if instrument.Underlying().Name().lower().__contains__('_divfut_underlying'):
                                myObject['NormalisedUnderlyingInstrument'] = instrument.Underlying().Name().split('/', 1)[1]
                            else:
                                myObject['NormalisedUnderlyingInstrument'] = instrument.Underlying().Name().split('/', 1)[1].split('_')[0]
                    elif instrument.Underlying().InsType() in ('Stock', 'ETF'):
                        if instrument.Underlying().Name().lower().find('zar/') == 0:
                            myObject['NormalisedUnderlyingInstrument'] = instrument.Underlying().Name().split('/', 1)[1].split('_')[0]
                        
                myObject['NormalisedUsedPriceStart'] = 0
                myObject['NormalisedUsedPriceEnd'] = 0 
                myObject['OpeningFrontNotional'] = 0
                myObject['ClosingFrontNotional'] = 0
                InsPort[key] = myObject
                        
            myWorkingObject = InsPort[key]
            myWorkingObject['Val Start'] += get_ValStart(trade)
           
            try:
                myWorkingObject['Val End'] += get_Column_Number(trade, 'Portfolio Value End')
            except:
                pass
                
            try:
                myWorkingObject['PLPosEnd'] += get_PLPosEnd(trade)
            except:
                pass
            
            try:
                myWorkingObject['PLPosStart'] += get_PLPosStart(trade)
            except:
                pass
                
            myWorkingObject['TPL'] += get_PLTotal(trade)
            myWorkingObject['Used Price Start'] = get_PLUsedPriceStart(trade)
            myWorkingObject['Used Price End'] = get_Column_PPLPED(trade, 'Portfolio Profit Loss Price End Date')
            myWorkingObject['TPLD'] += get_TPLD(trade)
     
            
            if instrument.InsType() == 'Future/Forward' and instrument.QuoteType() == 'Per Contract':
                myWorkingObject['NormalisedUsedPriceStart'] = myWorkingObject['Used Price Start'] * myWorkingObject['QuotationFactor'] /myWorkingObject['Contract Size']
                myWorkingObject['NormalisedUsedPriceEnd'] = myWorkingObject['Used Price End'] * myWorkingObject['QuotationFactor'] /myWorkingObject['Contract Size']
            else:
                myWorkingObject['NormalisedUsedPriceStart'] = myWorkingObject['Used Price Start'] * myWorkingObject['QuotationFactor'] 
                myWorkingObject['NormalisedUsedPriceEnd'] = myWorkingObject['Used Price End'] * myWorkingObject['QuotationFactor'] 
            
            if myWorkingObject['Call/Put'] in ('Call', 'Put'):
                myWorkingObject['OpeningFrontNotional'] = myWorkingObject['PLPosStart'] * myWorkingObject['NormalisedUsedPriceStart']
                myWorkingObject['ClosingFrontNotional'] = myWorkingObject['PLPosEnd'] * myWorkingObject['NormalisedUsedPriceEnd'] 
            else:
                myWorkingObject['OpeningFrontNotional'] = myWorkingObject['PLPosStart'] * myWorkingObject['NormalisedUsedPriceStart'] * myWorkingObject['Contract Size'] 
                myWorkingObject['ClosingFrontNotional'] = myWorkingObject['PLPosEnd'] * myWorkingObject['NormalisedUsedPriceEnd'] * myWorkingObject['Contract Size']
                
        for key in InsPort.Keys():    
            print 'Output:', key
            myWorkingObject = InsPort[key]            
            
            outLine = myWorkingObject['Portfolio'].replace(',', '')
            outLine += ',' + str(myWorkingObject['PortfolioNumber']).replace(',', '')
            outLine += ',' + str(myWorkingObject['Underlying ContractSize']).replace(',', '')
            outLine += ',' + myWorkingObject['Instrument'].replace(',', '')
            outLine += ',' + str(myWorkingObject['Val Start']).replace(',', '')
            outLine += ',' + str(myWorkingObject['Val End']).replace(',', '')
            outLine += ',' + myWorkingObject['Currency'].replace(',', '')
            outLine += ',' + str(myWorkingObject['PLPosEnd']).replace(',', '')
            outLine += ',' + str(myWorkingObject['Contract Size']).replace(',', '')
            outLine += ',' + myWorkingObject['Period Start'].replace(',', '')
            outLine += ',' + myWorkingObject['Period End'].replace(',', '')
            outLine += ',' + str(myWorkingObject['TPL']).replace(',', '')
            outLine += ',' + str(myWorkingObject['Used Price Start']).replace(',', '')
            outLine += ',' + str(myWorkingObject['Used Price End']).replace(',', '')
            outLine += ',' + myWorkingObject['InstrumentType'].replace(',', '')
            outLine += ',' + myWorkingObject['UnderlyingInstrument'].replace(',', '')
            outLine += ',' + myWorkingObject['UnderlyingInstrumentType'].replace(',', '')
            outLine += ',' + myWorkingObject['Call/Put'].replace(',', '')
            outLine += ',' + myWorkingObject['Strike Price'].replace(',', '')
            outLine += ',' + myWorkingObject['Expiry'].replace(',', '')
            outLine += ',' + myWorkingObject['QuoteType'].replace(',', '')
            outLine += ',' + str(myWorkingObject['ClosingAIP']).replace(',', '')
            outLine += ',' + str(myWorkingObject['TPLD']).replace(',', '')
            outLine += ',' + str(myWorkingObject['PLPosStart']).replace(',', '')
            outLine += ',' + str(myWorkingObject['QuotationFactor']).replace(',', '')
            outLine += ',' + str(myWorkingObject['NormalisedUnderlyingInstrument']).replace(',', '')
            outLine += ',' + str(myWorkingObject['NormalisedUsedPriceStart']).replace(',', '')
            outLine += ',' + str(myWorkingObject['NormalisedUsedPriceEnd']).replace(',', '')
            outLine += ',' + str(myWorkingObject['OpeningFrontNotional']).replace(',', '')
            outLine += ',' + str(myWorkingObject['ClosingFrontNotional']).replace(',', '')
            outfile.write(outLine + '\n')    
        
    outfile.close()
    print "Completed Successfully ::"
