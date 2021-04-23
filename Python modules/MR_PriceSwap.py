
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
    
def OpenFile(temp,FileDir,Filename,*rest):

    filename = FileDir + Filename
    outfile =  open(filename, 'w')
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

def Write(i,FileDir,Filename,*rest):
    
    filename = FileDir + Filename
    insaddr = i.insaddr
    Instrument = acm.FInstrument[insaddr]

    # Defining the fields
    columnsHeaders='''BASFLAG HeaderName OBJECT TYPE NAME IDENTIFIER CurrencyCAL CurrencyDAYC CurrencyPERD 
    CurrencyUNIT CallOptionFLAG ContractSizeVAL CorrelationVAL CorrelationSrfXREF FXVolatilityCAL FXVolatilityDAYC 
    FXVolatilityFUNC FXVolatilityPERD FXVolatilityUNIT FXVolatilityVAL FXVolatilitySTRG FXVolatilitySfXREF StrikePriceCAL 
    StrikePriceDAYC StrikePriceFUNC StrikePricePERD StrikePriceUNIT StrikePriceVAL StrikePriceSTRG UnderlyingXREF 
    ProcessTypeENUM MeanRvrsnConstCAL MeanRvrsnConstDAYC MeanRvrsnConstFUNC MeanRvrsnConstPERD MeanRvrsnConstUNIT 
    MeanRvrsnConstVAL MeanRvrsnConstSTRG AveragingTypeENUM MaturityDATE FixingRuleENUM BusDayRuleRULE BusDayRuleBUSD 
    BusDayRuleCONV BusDayRuleCAL NumofFixiDateNB AvgSoFarCAL AvgSoFarDAYC AvgSoFarFUNC AvgSoFarPERD AvgSoFarUNIT AvgSoFarVAL 
    AvgSoFarSTRG AvgStartDateDATE AveEndDateDATE AveSoFarCAL AveSoFarDAYC AveSoFarFUNC AveSoFarPERD AveSoFarUNIT AveSoFarVAL 
    AveSoFarSTRG AveStartDateDATE HistoricalCrvXREF FixedTodayFLAG DiscountCurveXREF VolatilityCAL VolatilityDAYC VolatilityFUNC 
    VolatilityPERD VolatilityUNIT VolatilityVAL VolatilitySTRG VolSurfaceXREF SettlementTYPE SettlementProcFUNC TheoModelXREF MarketModelXREF   
    FairValueModelXREF
    '''
    
    if (insaddr) not in InsL:
        InsL.append(insaddr)
    
        # Data initialisation
        data={}
        
        #Base record  
        # Populating the fields
        data['BASFLAG']           = 'BAS'
        data['HeaderName']        = 'Asian'
        data['OBJECT']            = 'AsianSPEC'
        data['TYPE']              = 'Asian'   
        data['NAME']              = 'CALL_'+ MR_MainFunctions.NameFix(i.insid)          #For (payoff max(A(S)-K,0)) 
        data['IDENTIFIER']        = 'insaddr_'+ str(insaddr) + '_1'
        data['CallOptionFLAG']    = 'True'
        data['ContractSizeVAL']   = Instrument.ContractSize()
        data['ProcessTypeENUM']   = 'Geometric Brownian'
        data['AveragingTypeENUM'] = 'Discrete'
        data['MaturityDATE']      = MR_MainFunctions.Datefix(str(Instrument.ExpiryDateOnly()))
        data['FixingRuleENUM']    = 'Calendar'
        data['BusDayRuleCAL']     = 'Weekends'
        data['AvgSoFarFUNC']      = '@GD2 historical'
        data['FixedTodayFLAG']    = 'True'
        data['TheoModelXREF']     = 'Asian Option'
        data['StrikePriceVAL']    = '0'
        
        for l in i.legs():
            if l.type == 'Float':
                float_rate = getattr(l, 'float_rate')
                data['UnderlyingXREF']    =  'insaddr_' + str(float_rate.insaddr)
                data['HistoricalCrvXREF'] = float_rate.insid + '_HistoricalCurve'
                data['CurrencyUNIT']      = l.float_rate.curr.insid

               
        data['AvgStartDateDATE'] = MR_MainFunctions.Datefix(str(l.start_day))

        try:
            data['DiscountCurveXREF'] = Instrument.MappedDiscountLink().Value().Link().YieldCurveComponent().Curve().Name()
        except:
            data['DiscountCurveXREF'] = Instrument.MappedDiscountLink().Value().Link().YieldCurveComponent().Name()
        
        # Writing the CSV file
        with open (filename, 'ab') as csvfile:
                csvwriter = csv.writer(csvfile)
                writeCSVRow(columnsHeaders, data, csvwriter)
                
        csvfile.close()
    return i.insid

# WRITE - FILE ######################################################################################################
