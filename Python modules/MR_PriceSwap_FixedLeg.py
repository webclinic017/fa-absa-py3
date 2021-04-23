
'''
Purpose                 :[Market Risk feed files],[To model a Price Swap as an asian option in order to get the correct average value (float leg) and a swap fixed leg]
Department and Desk     :[IT],[MR]
Requester:              :Jacqueline Calitz
Developer               :Heinrich Cronje
CR Number               :XXXXXX
'''


import ael, string, acm, PositionFile, MR_MainFunctions
import csv
InsL = []


# OPENFILE ##########################################################################################################
    
def OpenFile(temp,FileDir,Filename,PositionName,*rest):
    
    filename            = FileDir + Filename
        
    outfile             =  open(filename, 'w')
        
    outfile.close()
        
    del InsL[:]
    InsL[:] = []
    
    return filename

# OPENFILE ##########################################################################################################

def writeCSVRow(_headers, _dataSet, _csvPtr):
    _out = []

    # Populating the tuple for the output
    for _col in tuple(_headers.split()):
        _out.append(_dataSet[_col] if _col in _dataSet else '')

    _csvPtr.writerow(_out)

# WRITE - FILE ######################################################################################################

def Write(i,FileDir,Filename,PositionName,*rest):

    filename    = FileDir + Filename
    insaddr     = i.insaddr
    Instrument  = acm.FInstrument[insaddr]
            
    # Defining the fields
    columnsHeaders='''BASFLAG HeaderName OBJECT TYPE NAME IDENTIFIER CurrencyCAL CurrencyDAYC CurrencyPERD CurrencyUNIT NotionlAtStartFLAG 
    NotionalAtEndFLAG EffectiveDATE CouponRateCAL CouponRateDAYC CouponRatePERD CouponRateVAL StateProcFUNC TermNB TermUNIT 
    TermCAL CouponGenENUM FixedCouponDateNB BusDayRuleRULE BusDayRuleBUSD BusDayRuleCONV BusDayRuleCAL InitialIndxLvlFUNC 
    InitialIndxLvlUNIT InitialIndxLvlVAL InitialIndxLvlSTRG PaymntProcXREF DiscountCurveXREF CouponProratedFLAG TheoModelXREF 
    MarketModelXREF FairValueModelXREF SettlementProcFUNC 
    '''
    
    columnsHeadersCashflow='''BASFLAG HeaderName ATTRIBUTE OBJECT VariabNotionalDATE VariabNotionalENUM VariabNotionalCAL 
    VariabNotionalDAYC VariabNotionalPERD VariabNotionalUNIT VariabNotionalVAL 
    '''

    if (insaddr) not in InsL:
        InsL.append(insaddr)
        
        # Data initialisation
        data={}
        cData={}        # Cashflow data
        
        #Base record
        data['BASFLAG']               = 'BAS'
        data['HeaderName']            = 'Swap Fixed Leg'
        data['OBJECT']                = 'Swap Fixed LegSPEC'
        data['TYPE']                  = 'Swap Fixed Leg'
        data['NAME']                  = MR_MainFunctions.NameFix(i.insid)+'_Fixed'
        data['IDENTIFIER']            = 'insaddr_'+ str(insaddr)+'_2'
        data['BusDayRuleCAL']         = 'Weekends'
        data['CouponGenENUM']         = 'Backward'
        data['StateProcFUNC']         = '@cash flow generator'
        data['TermUNIT']              = 'Maturity'
        data['InitialIndxLvlVAL']     = '0'        
        data['TheoModelXREF']         = 'Swap Fixed Leg(Cashflows)'
        
        for l in i.legs():
            if l.type == 'Fixed':
                data['CouponRateDAYC']  = MR_MainFunctions.DayCountFix(l.daycount_method)
                data['CouponRateVAL']   = getattr(l, 'fixed_rate')
                data['CurrencyUNIT']    = l.curr.insid
                data['EffectiveDATE']   = MR_MainFunctions.Datefix(l.start_day)
                
        try:
            data['DiscountCurveXREF'] = Instrument.MappedDiscountLink().Value().Link().YieldCurveComponent().Curve().Name()
        except:
            data['DiscountCurveXREF'] = Instrument.MappedDiscountLink().Value().Link().YieldCurveComponent().Name()
       
        # Writing the CSV file
        with open (filename, 'ab') as csvfile:
            csvwriter = csv.writer(csvfile)
            writeCSVRow(columnsHeaders, data, csvwriter)
            
            #Rollover record            
            cData['BASFLAG']            = 'rm_ro'
            cData['HeaderName']         = 'Swap Fixed Leg : Variable Notional'
            cData['ATTRIBUTE']          = 'Variable Notional'
            cData['OBJECT']             = 'Swap Fixed LegSPEC'           
            
            if l.type == 'Fixed':
                cData['VariabNotionalUNIT']    = l.curr.insid
            
          
            for cf in l.cash_flows():
                if cf.pay_day > ael.date_today():
                    cData['VariabNotionalDATE']    = MR_MainFunctions.Datefix(cf.pay_day) 
                    cData['VariabNotionalVAL']     = abs(cf.nominal_amount())*100                    
                    
            writeCSVRow(columnsHeadersCashflow, cData, csvwriter)
            
        csvfile.close()

    return i.insid

# WRITE - FILE ######################################################################################################
