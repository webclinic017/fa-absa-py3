
'''
Purpose                 :Market Risk feed files
Department and Desk     :IT
Requester:              :Natalie Austin
Developer               :Douglas Finkel
CR Number               :264536, 677357

Description             :Added position extract

Date           CR               Requestor          Developer          Change
----------------------------------------------------------------------------------------
2020-09-11     CHG0128302	Garth Saunders	   Heinrich Cronje    https://absa.atlassian.net/browse/CMRI-776
2021-03-11     CHG0158547       Thando Mpalala     Andile Biyana      https://absa.atlassian.net/browse/FAFO-41
'''
import ael, string, acm, PositionFile, MR_MainFunctions

import BondIndex
import CPIBondIndex

BOND_CORRECTION_FACTOR = 1000 #This is used to scale the weights coming from BondIndex module.

InsL = []


# OPENFILE ##########################################################################################################
    
def OpenFile(temp,FileDir,Filename,PositionName,*rest):

    filename            = FileDir + Filename
    PositionFilename    = FileDir + PositionName
    
    outfile             =  open(filename, 'w')
    outfileP            =  open(PositionFilename, 'w')
    
    outfile.close()
    outfileP.close()
    
    del InsL[:]
    InsL[:] = []

    return filename

# OPENFILE ##########################################################################################################

# WRITEBONDINDEX ####################################################################################################

def WriteBondIndex(i,FileDir,Filename,PositionName,*rest):
    """ This method creates a synthetic instrument modelling an ETF on a bond index
    The bond index is identified as having a corresponding k-Factor timeseries."""

    filename = FileDir + Filename
    PositionFilename = FileDir + PositionName

    Instrument = acm.FInstrument[i.insaddr]
    context = acm.GetDefaultContext()

    if (i.insaddr) not in InsL:
        InsL.append(i.insaddr)

        outfile = open(filename, 'a')

        #Base record
        BASFLAG = 'BAS'
        HeaderName = 'Synthetic Market Index'
        OBJECT = 'Synthetic InstrumentSPEC'
        TYPE = 'Synthetic InstrumentSPEC'

        NAME = MR_MainFunctions.NameFix(i.insid)
        IDENTIFIER = 'insaddr_'+str(i.insaddr)

        CurrencyCAL = ''
        CurrencyDAYC = ''
        CurrencyPERD = ''
        CurrencyUNIT = Instrument.Currency().Name()

        CostOfCarryCAL = ''
        CostOfCarryDAYC = ''
        CostOfCarryPERD = ''
        divYield = Instrument.AdditionalInfo().DividendYield()

        if divYield:
            CostOfCarryVAL = divYield
        else:
            CostOfCarryVAL = ''

        StateProcFUNC = '@aggregate positions'

        try:
            DiscountCurveXREF = Instrument.Currency().MappedDiscountLink().Value().Link().YieldCurveComponent().Curve().Name()
        except:
            DiscountCurveXREF = Instrument.Currency().MappedDiscountLink().Value().Link().YieldCurveComponent().Name()

        TheoModelXREF = 'Basket Instrument'
        MarketModelXREF = ''
        FairValueModelXREF = ''

        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, NAME, IDENTIFIER, CurrencyCAL, CurrencyDAYC, CurrencyPERD, CurrencyUNIT, CostOfCarryCAL, CostOfCarryDAYC, CostOfCarryPERD, CostOfCarryVAL, StateProcFUNC, DiscountCurveXREF, TheoModelXREF, MarketModelXREF, FairValueModelXREF))

        if i.und_insaddr is not None:

            member_types = [member.member_insaddr.instype for member in i.und_insaddr.combination_links()]
            if member.member_insaddr.instype in ('Bond'):
                weight = BondIndex.getKFactor(i.und_insaddr, ael.date_today()) * BOND_CORRECTION_FACTOR/100
            else: 
                weight = BondIndex.getKFactor(i.und_insaddr, ael.date_today()) * BOND_CORRECTION_FACTOR                  

            #Rollover record
            BASFLAG = 'rm_ro'
            HeaderName = 'Synthetic Market Index : Component Weights'
            ATTRIBUTE = 'Component Weights'
            OBJECT = 'Synthetic InstrumentSPEC'
            ComponentWghtVAL = weight

            outfile.write('%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, ComponentWghtVAL))

            #Rollover record
            BASFLAG = 'rm_ro'
            HeaderName = 'Synthetic Market Index : Underlying Financial Entities'
            ATTRIBUTE = 'Underlying Financial Entities'
            OBJECT = 'Synthetic InstrumentSPEC'
            UndrFinEntitisXREF = 'insaddr_' + str(i.und_insaddr.insaddr)
            outfile.write('%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, UndrFinEntitisXREF))

        for trades in i.trades():
            if MR_MainFunctions.ValidTradeNo(trades) == 0:
                PositionFile.CreatePosition(trades, PositionFilename)

        outfile.close()

    return i.insid

# WRITEBONDINDEX ####################################################################################################

# WRITEETF ##########################################################################################################

def WriteETF(i,FileDir,Filename,PositionName,*rest):
    """ This method creates a synthetic instrument modelling an ETF"""

    filename = FileDir + Filename
    PositionFilename = FileDir + PositionName

    Instrument = acm.FInstrument[i.insaddr]
    context = acm.GetDefaultContext()

    if (i.insaddr) not in InsL:
        InsL.append(i.insaddr)

        outfile = open(filename, 'a')

        #Base record
        BASFLAG = 'BAS'
        HeaderName = 'Synthetic Market Index'
        OBJECT = 'Synthetic InstrumentSPEC'
        TYPE = 'Synthetic InstrumentSPEC'

        NAME = MR_MainFunctions.NameFix(i.insid)
        IDENTIFIER = 'insaddr_'+str(i.insaddr)

        CurrencyCAL = ''
        CurrencyDAYC = ''
        CurrencyPERD = ''
        CurrencyUNIT = Instrument.Currency().Name()

        CostOfCarryCAL = ''
        CostOfCarryDAYC = ''
        CostOfCarryPERD = ''
        divYield = Instrument.AdditionalInfo().DividendYield()

        if divYield:
            CostOfCarryVAL = divYield
        else:
            CostOfCarryVAL = ''

        StateProcFUNC = '@aggregate positions'

        try:
            DiscountCurveXREF = Instrument.Currency().MappedDiscountLink().Value().Link().YieldCurveComponent().Curve().Name()
        except:
            DiscountCurveXREF = Instrument.Currency().MappedDiscountLink().Value().Link().YieldCurveComponent().Name()

        TheoModelXREF = 'Basket Instrument'
        MarketModelXREF = ''
        FairValueModelXREF = ''

        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, NAME, IDENTIFIER, CurrencyCAL, CurrencyDAYC, CurrencyPERD, CurrencyUNIT, CostOfCarryCAL, CostOfCarryDAYC, CostOfCarryPERD, CostOfCarryVAL, StateProcFUNC, DiscountCurveXREF, TheoModelXREF, MarketModelXREF, FairValueModelXREF))

        if i.und_insaddr is not None:
            #Rollover record
            BASFLAG = 'rm_ro'
            HeaderName = 'Synthetic Market Index : Component Weights'
            ATTRIBUTE = 'Component Weights'
            OBJECT = 'Synthetic InstrumentSPEC'
            if i.instype == 'ETF' and i.und_insaddr.instype == 'Stock':
                ins = acm.FInstrument[i.insaddr]
	        cs = acm.Calculations().CreateStandardCalculationsSpaceCollection()
                calc = ins.Calculation()
                TheoPrice = calc.TheoreticalPrice(cs)
                ComponentWghtVAL = TheoPrice.Number()
            else:
                ComponentWghtVAL = 1.0
            outfile.write('%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, ComponentWghtVAL))

            #Rollover record
            BASFLAG = 'rm_ro'
            HeaderName = 'Synthetic Market Index : Underlying Financial Entities'
            ATTRIBUTE = 'Underlying Financial Entities'
            OBJECT = 'Synthetic InstrumentSPEC'
            UndrFinEntitisXREF = 'insaddr_' + str(i.und_insaddr.insaddr)
            outfile.write('%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, UndrFinEntitisXREF))

        for trades in i.trades():
            if MR_MainFunctions.ValidTradeNo(trades) == 0:
                PositionFile.CreatePosition(trades, PositionFilename)

        outfile.close()

    return i.insid

# WRITEETF ##########################################################################################################

# WRITE - FILE ######################################################################################################

def Write(i,FileDir,Filename,PositionName,*rest):
    
    filename            = FileDir + Filename
    PositionFilename    = FileDir + PositionName
    
    Instrument = acm.FInstrument[i.insaddr]
 
    if (i.insaddr) not in InsL:
        InsL.append(i.insaddr)

        outfile = open(filename, 'a')
        #Base record
        
        BASFLAG             =       'BAS'
        #2010-07-02 Anwar changed headername from 'Synthetic' as per Susan instruction
        HeaderName          =       'Synthetic Market Index'
        OBJECT              =       'Synthetic InstrumentSPEC'
        TYPE                =       'Synthetic InstrumentSPEC'
        
        NAME                =       MR_MainFunctions.NameFix(i.insid)
        IDENTIFIER          =       'insaddr_'+str(i.insaddr)
        
        CurrencyCAL         =       ''
        CurrencyDAYC        =       ''
        CurrencyPERD        =       ''
        CurrencyUNIT        =       Instrument.Currency().Name()
        
        CostOfCarryCAL      =       ''
        CostOfCarryDAYC     =       ''
        CostOfCarryPERD     =       ''        
        divYield            =       Instrument.AdditionalInfo().DividendYield()
        
        if divYield:
            CostOfCarryVAL      =   divYield
        else:
            CostOfCarryVAL      =   ''
        
        StateProcFUNC       =       '@aggregate positions'
        
        try:
            DiscountCurveXREF       =       Instrument.Currency().MappedDiscountLink().Value().Link().YieldCurveComponent().Curve().Name()
        except:
            DiscountCurveXREF       =       Instrument.Currency().MappedDiscountLink().Value().Link().YieldCurveComponent().Name()
        
        TheoModelXREF       =       'Basket Instrument'
        MarketModelXREF     =       ''
        FairValueModelXREF  =       ''
        
        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, NAME, IDENTIFIER, CurrencyCAL, CurrencyDAYC, CurrencyPERD, CurrencyUNIT, CostOfCarryCAL, CostOfCarryDAYC, CostOfCarryPERD, CostOfCarryVAL, StateProcFUNC, DiscountCurveXREF, TheoModelXREF, MarketModelXREF, FairValueModelXREF))
	
        for ins in Instrument.InstrumentMaps():
            #Rollover record            
            BASFLAG     =	'rm_ro'
            HeaderName	=	'Synthetic Market Index : Component Weights'
            ATTRIBUTE	=	'Component Weights'
	    OBJECT              =       'Synthetic InstrumentSPEC'
            ComponentWghtVAL = ins.Weight() / Instrument.Factor()                
            outfile.write('%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, ComponentWghtVAL))
            
            #Rollover record            
            BASFLAG     =	'rm_ro'
            HeaderName	=	'Synthetic Market Index : Underlying Financial Entities'
            ATTRIBUTE	=	'Underlying Financial Entities'
	    OBJECT              =       'Synthetic InstrumentSPEC'           
            UndrFinEntitisXREF = 'insaddr_' + str(ins.Instrument().Oid())
            outfile.write('%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, UndrFinEntitisXREF))
        
        for trades in i.trades():
            if MR_MainFunctions.ValidTradeNo(trades) == 0:
                if MR_MainFunctions.IsExcludedPortfolio(trades) == False:
                    PositionFile.CreatePosition(trades, PositionFilename)
	
        outfile.close()      
    
    return i.insid

# WRITE - FILE ######################################################################################################
