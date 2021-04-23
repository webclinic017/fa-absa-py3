'''
Purpose                       :  Large holdings for complex exposures
Department and Desk           :  PCG 
Requester                     :  Guy Mcloughlin
Developer                     :  Anwar Banoo
CR Number                     :  281576
'''

import ael, string, acm

insl = []
cs = acm.Calculations().CreateStandardCalculationsSpaceCollection()
yesterday = ael.date_today().add_banking_day(ael.Instrument['ZAR'], -1)

def Datefix(d, *rest):
    if d == None:
        return ''
    else:
        return ael.date_from_time(d).to_string('%Y/%m/%d %H:%M')

# OPENFILE ##########################################################################################################

def OpenFile(temp,FileDir,Filename,*rest):
    filename = FileDir + Filename + '%s.csv' %(ael.date_today().to_string('%Y%m%d'))
    outfile  =  open(filename, 'w')
    outfile.write('Instrument,Instrument,Price,Qty,Portfolio,TradeCurrency,Status,Counterparty,Trader,B/S,Underlying,Type,Trd No,Date and Time,Isin,' +  
                   'Strike,Exercise,ExpT(Y),EndDate,OTC,EQDelta,IsCall,IsAsian,Settlement Type,YMtM,Execution Time,Update Time,CounterpartyType,' +
                   'CounterpartyUpdateTime\n')
    outfile.close()
    
    return filename

# OPENFILE ##########################################################################################################



# WRITE - FILE ######################################################################################################

class SheetCalcSpace( object ):
    CALC_SPACE = acm.FCalculationSpace('FTradeSheet' )
    @classmethod
    def get_column_calc( cls, obj, column_id ):
        calc = SheetCalcSpace.CALC_SPACE.CreateCalculation( obj, column_id )
        return calc


def get_EQDelta(t, *rest):
    '''
Retruns the Trading Manager instrument Strike Price column 
    '''

    column_id       = 'Portfolio Delta Implicit Equity'

    calc = SheetCalcSpace.get_column_calc(t, column_id)
    Value = calc.Value().Number()
    
    return Value
    
def get_YMtM(i, *rest):
    calc = i.Calculation()    
    Value = calc.MarketPrice(cs, yesterday, True, acm.FInstrument[i.Currency().Name()], False, acm.FParty['internal'], False).Value().Number()    
    return Value

def Write(t,FileDir,Filename,*rest): 
    filename = FileDir + Filename + '%s.csv' %(ael.date_today().to_string('%Y%m%d'))
    outfile = open(filename, 'a')    
    
    ins = acm.FInstrument[t.insaddr.insid]
    trade = acm.FTrade[t.trdnbr]
    
    if ins.InsType() == 'Combination':
        for insi in ins.Instruments():
            if insi.InsType() == 'Stock':
        
                TrdNbr          =       trade.Oid()    
                Instrument      =       trade.Instrument().Name()
                Price           =       trade.Price()           
                Qty             =       trade.Quantity()
                Portfolio       =       trade.Portfolio().Name()
                TradeCurrency   =       trade.Currency().Name()
                Status          =       trade.Status()
                Counterparty    =       trade.Counterparty().Name()

                try:
                    Trader          =       trade.Trader().Name()
                except:
                    Trader          =       ''
                
                    
                if(trade.Quantity()>0):
                    B_S =  'Buy'
                else:
                    B_S = 'Sell'
               
                try:
                    Underlying      =       insi.Name()
                except:
                    Underlying      =       ''

                Type            =       ins.InsType()    
                Date_and_Time   =       trade.TradeTime()
                Isin            =       ins.Isin()
                Strike          =       ''
                Exercise        =       ''
                ExpT            =       abs(acm.Time().DateDifference(acm.Time().DateToday(), ins.ExpiryDate()) / 365.0)
                EndDate         =       ins.ExpiryDate()
                
                if(ins.Otc()== 'True'):
                    OTC             =       'Yes'
                else:
                    OTC             =       'No'
                    
                EQDelta         =       -1 * trade.Quantity()
                
                if(ins.IsCall()== 'True'):
                    IsCall          =       'Yes'
                else:
                    IsCall          =       'No'
                    
                IsAsian         =       ''
                SettlementType  =       ins.SettlementType()
                YMtM            =       get_YMtM(insi)
                Execution_Time  =       Datefix(trade.ExecutionTime())    
                Update_Time     =       Datefix(trade.UpdateTime())
                CounterpartyType=       trade.Counterparty().Type()
                CounterpartyUpdateTime = Datefix(trade.Counterparty().UpdateTime())       
                    
                outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(TrdNbr, Instrument, Price, Qty, Portfolio,
                                TradeCurrency, Status, Counterparty, Trader, B_S, Underlying, Type, TrdNbr, Date_and_Time, Isin, Strike, Exercise, ExpT, EndDate, OTC, EQDelta,
                                IsCall, IsAsian, SettlementType, YMtM, Execution_Time, Update_Time, CounterpartyType, CounterpartyUpdateTime))
    
    else:
        TrdNbr          =       trade.Oid()    
        Instrument      =       trade.Instrument().Name()
        Price           =       trade.Price()           
        Qty             =       trade.Quantity()
        Portfolio       =       trade.Portfolio().Name()
        TradeCurrency   =       trade.Currency().Name()
        Status          =       trade.Status()
        Counterparty    =       trade.Counterparty().Name()

        try:
            Trader          =       trade.Trader().Name()
        except:
            Trader          =       ''
        
            
        if(trade.Quantity()>0):
            B_S =  'Buy'
        else:
            B_S = 'Sell'
       
        Underlying      =       'Multiple'

        Type            =       ins.InsType()    
        Date_and_Time   =       trade.TradeTime()
        Isin            =       ins.Isin()
        Strike          =       ''
        Exercise        =       ''
        ExpT            =       abs(acm.Time().DateDifference(acm.Time().DateToday(), ins.ExpiryDate()) / 365.0)
        EndDate         =       ins.ExpiryDate()
        
        if(ins.Otc()== 'True'):
            OTC             =       'Yes'
        else:
            OTC             =       'No'
            
        EQDelta         =       -1 * trade.Quantity()
        
        if(ins.IsCall()== 'True'):
            IsCall          =       'Yes'
        else:
            IsCall          =       'No'
            
        IsAsian         =       ''
        SettlementType  =       ins.SettlementType()
        YMtM            =       get_YMtM(ins)
        Execution_Time  =       Datefix(trade.ExecutionTime())    
        Update_Time     =       Datefix(trade.UpdateTime())
        CounterpartyType=       trade.Counterparty().Type()
        CounterpartyUpdateTime = Datefix(trade.Counterparty().UpdateTime())       
            
        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(TrdNbr, Instrument, Price, Qty, Portfolio,
                        TradeCurrency, Status, Counterparty, Trader, B_S, Underlying, Type, TrdNbr, Date_and_Time, Isin, Strike, Exercise, ExpT, EndDate, OTC, EQDelta,
                        IsCall, IsAsian, SettlementType, YMtM, Execution_Time, Update_Time, CounterpartyType, CounterpartyUpdateTime))

    outfile.close()
    

    return 'Success'

# WRITE - FILE ######################################################################################################

#OpenFile(0,'C:\\','Large_Holdings_ComboTrades.csv')
#trd = ael.Trade[4897730]
#Write(trd, 'C:\\','Large_Holdings_ComboTrades.csv')
