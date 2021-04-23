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
    outfile.write('Portfolio,Instrument,Settlement Type,Pos,DispCurr,Isin,C/P,Expiry,Strike Fx,Strike,Underlying,CtrSz,QuotationType,Curr,IsAsian,OTC,ExerciseType,EQDelta,Type,YMtM,Und Type\n')
    outfile.close()
    
    return filename

# OPENFILE ##########################################################################################################



# WRITE - FILE ######################################################################################################

class SheetCalcSpace( object ):
    CALC_SPACE = acm.FCalculationSpace('FPortfolioSheet' )
    @classmethod
    def get_column_calc( cls, obj, column_id ):
        calc = SheetCalcSpace.CALC_SPACE.CreateCalculation( obj, column_id )
        return calc

class TSheetCalcSpace( object ):
    CALC_SPACE = acm.FCalculationSpace('FTradeSheet' )
    @classmethod
    def get_column_calc( cls, obj, column_id ):
        calc = TSheetCalcSpace.CALC_SPACE.CreateCalculation( obj, column_id )
        return calc
        
def get_EQDelta(i, *rest):
    '''
Retruns the Trading Manager instrument Strike Price column 
    '''

    column_id       = 'Portfolio Delta Implicit Equity'

    calc = SheetCalcSpace.get_column_calc(i, column_id)
    Value = calc.Value().Number()
    
    return Value

def get_YMtM(i, *rest):
    calc = i.Calculation()    
    Value = calc.MarketPrice(cs, yesterday, True, acm.FInstrument[i.Currency().Name()], False, acm.FParty['internal'], False).Value().Number()    
    return Value
    
def Write(i,portfolio,position,FileDir,Filename,*rest):
    filename = FileDir + Filename + '%s.csv' %(ael.date_today().to_string('%Y%m%d'))
    outfile = open(filename, 'a')    
    
    ins = acm.FInstrument[i.insid]
    
    if ins.InsType == 'Combination':
        for insi in ins.Instruments():
            if insi.InsType() == 'Stock':
                Portfolio = portfolio
                Instrument = ins.Name()
                Settlement = ins.SettlementType()
                Pos = position
                DispCurr = ins.Currency().Name()
                Isin = ins.Isin()
                CP = ''
                Expiry = ins.ExpiryDate()
                StrikeFx = ''
                Strike = ''
                Underlying = insi.Name()
                CtrSz = ins.ContractSize()
                Quotation = ins.Quotation().QuotationType()
                Curr = ins.Currency().Name()
                IsAsian = ''
                OTC = ins.Otc()
                ExerciseType = ''
                EQDelta = get_EQDelta(ins)
                Type = ins.InsType()
                YMtm = get_YMtM(insi)
                UndType = insi.InsType()
            
                outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n' %(Portfolio, Instrument, Settlement, Pos, DispCurr, Isin, CP,
                            Expiry, StrikeFx, Strike, Underlying, CtrSz, Quotation, Curr, IsAsian, OTC, ExerciseType, EQDelta, Type, YMtm, UndType))
    
    else:
        Portfolio = portfolio
        Instrument = ins.Name()
        Settlement = ins.SettlementType()
        Pos = position
        DispCurr = ins.Currency().Name()
        Isin = ins.Isin()
        CP = ''
        Expiry = ins.ExpiryDate()
        StrikeFx = ''
        Strike = ''
        Underlying = 'Multiple'
        CtrSz = ins.ContractSize()
        Quotation = ins.Quotation().QuotationType()
        Curr = ins.Currency().Name()
        IsAsian = ''
        OTC = ins.Otc()
        ExerciseType = ''
        EQDelta = -1 * position
        Type = ins.InsType()
        YMtm = get_YMtM(ins)
        UndType = 'Stock'    
    
        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n' %(Portfolio, Instrument, Settlement, Pos, DispCurr, Isin, CP,
                    Expiry, StrikeFx, Strike, Underlying, CtrSz, Quotation, Curr, IsAsian, OTC, ExerciseType, EQDelta, Type, YMtm, UndType))

    return 'Success'

# WRITE - FILE ######################################################################################################

#OpenFile(0,'C:\\','Large_Holdings_ComboTrades.csv')
#trd = ael.Trade[8617029]
#Write(trd, 'C:\\','Large_Holdings_ComboTrades.csv')
