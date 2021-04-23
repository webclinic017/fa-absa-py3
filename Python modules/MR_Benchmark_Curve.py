'''
Purpose                 :Market Risk feed files
Department and Desk     :IT
Requester:              :Natalie Austin
Developer               :Douglas Finkel
CR Number               :264536,287397,290307,477922

 -- HISTORY --
Date           CR               Requestor          Developer          Change
----------------------------------------------------------------------------------------
2015-09-03                                         Chris Human        http://abcap-jira/browse/MINT-352
2016-01-28     CHNG0001946630   Ashley Canter      Chris Human        http://abcap-jira/browse/MINT-420
2016-03-08     CHNG0003469409   Ashley Canter      Chris Human        http://abcap-jira/browse/MINT-527
2017-01-12                      Mandlenkosi Ngcobo Faize Adams        http://abcap-jira/browse/MRINFRA-120  
2019-11-29                      Louis Jaka         Richard Coppin     https://jira-agl.absa.co.za/browse/FAFO-64
'''

import ael, string, acm, MR_MainFunctions

InsL = []
CurveDatesList = []

# OPENFILE ##########################################################################################################
    
def OpenFile(temp,FileDir,Filename,*rest):

    filename = FileDir + Filename
    outfile = open(filename, 'w')
    outfile.close()

    del InsL[:]
    InsL[:] = []  

    return filename

# OPENFILE ##########################################################################################################


# PREWRITE ##########################################################################################################
def PreWrite(yc,FileDir,Filename,*rest):
    if (yc.seqnbr) not in InsL:
        InsL.append(yc.seqnbr)

    return str(yc.yield_curve_name)

# PREWRITE ##########################################################################################################


# WRITE - FILE ######################################################################################################

def Write(temp,FileDir,Filename,*rest):
    
    filename = FileDir + Filename
    outfile = open(filename, 'a')
    for YcSeqnbr in InsL:
        yc = ael.YieldCurve[YcSeqnbr]

        #Base record    
        BAS = 'BAS'
        ZeroSPEC = 'ZeroSPEC'
        OBJECT = 'ZeroSPEC'
        TYPE = 'Zero'
        
        IDENTIFIER = yc.yield_curve_name + '_Base'
        NAME = yc.yield_curve_name + '_Base'
        
        ActiveFLAG = 'TRUE'
        CreditStateENUM = ''
        CurveFUNC = ''

        CurveUnitCAL = ''
        CurveUnitDAYC = MR_MainFunctions.DayCountFix(yc.storage_daycount)
        CurveUnitPERD = MR_MainFunctions.BusRule(yc.storage_rate_type)  #'annual'   
        CurveUnitUNIT = '%'

        DatumDATE = MR_MainFunctions.Datefix(acm.Time().DateNow())
        OriginOffsetNB = '0'
        RelativeCurveFLAG = 'TRUE'
        StateProcFUNC = ''
        TimeEvolutionFUNC = '@Constant'
        FunctionIdFLAG = 'TRUE'
        GenZeroSfExt0FLAG = 'FALSE'
        GenZeroSurface0SIN = '@Linear'
        
        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BAS, ZeroSPEC, OBJECT, TYPE, IDENTIFIER, NAME, ActiveFLAG, CreditStateENUM, CurveFUNC, CurveUnitCAL, CurveUnitDAYC, CurveUnitPERD, CurveUnitUNIT, DatumDATE, OriginOffsetNB, RelativeCurveFLAG, StateProcFUNC, TimeEvolutionFUNC, FunctionIdFLAG, GenZeroSfExt0FLAG, GenZeroSurface0SIN))
        
        # Roll Over Function Parameters
        GnVolMnyTrmSf0AXS = ''
        GnVolMnyTrmSfNODE = ''
        DateToday = acm.Time().DateToday()
        ACMyc = acm.FYieldCurve[YcSeqnbr]
        
        BASFLAG = 'rm_ro'
        Volatility = 'ZeroSPEC : Generic Zero Surface'
        ATTRIBUTE = 'Generic Zero Surface'
        OBJECT = 'ZeroSPEC'
        
        GnVolMnyTrmSf0AXS = '' 
        GnVolMnyTrmSfNODE = '' 
        
        if yc.yield_curve_name in ('ZAR-CPI', 'ZAR-CPI-Bond'):
            CurveDatesList = []
            CurvePoints = [1, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330, 360, 390, 420, 450, 480, 510, 540, 570, 600, 630, 660, 690, 720, 750, 780, 810, 840, 870, 900, 930, 960, 990, 1020, 1050, 1080, 1110, 1140, 1170, 1200, 1230, 1260, 1290, 1320, 1350, 1380, 1410, 1440, 1470, 1500, 1530, 1560, 1590, 1620, 1650, 1680, 1710, 1740, 1770, 1800, 1830, 1860, 1890, 1920, 1950, 1980, 2010, 2040, 2070, 2100, 2130, 2160, 2190, 2220, 2250, 2280, 2310, 2340, 2370, 2400, 2430, 2460, 2490, 2520, 2550, 2580, 2610, 2640, 2670, 2700, 2730, 2760, 2790, 2820, 2850, 2880, 2910, 2940, 2970, 3000, 3030, 3060, 3090, 3120, 3150, 3180, 3210, 3240, 3270, 3300, 3330, 3360, 3390, 3420, 3450, 3480, 3510, 3540, 3570, 3600, 3630, 3660, 3690, 3720, 3750, 3780, 3810, 3840, 3870, 3900, 3930, 3960, 3990, 4020, 4050, 4080, 4110, 4140, 4170, 4200, 4230, 4260, 4290, 4320, 4350, 4380, 4410, 4440, 4470, 4500, 4530, 4560, 4590, 4620, 4650, 4680, 4710, 4740, 4770, 4800, 4830, 4860, 4890, 4920, 4950, 4980, 5010, 5040, 5070, 5100, 5130, 5160, 5190, 5220, 5250, 5280, 5310, 5340, 5370, 5400, 5430, 5460, 5490, 5520, 5550, 5580, 5610, 5640, 5670, 5700, 5730, 5760, 5790, 5820, 5850, 5880, 5910, 5940, 5970, 6000, 6030, 6060, 6090, 6120, 6150, 6180, 6210, 6240, 6270, 6300, 6330, 6360, 6390, 6420, 6450, 6480, 6510, 6540, 6570, 6600, 6630, 6660, 6690, 6720, 6750, 6780, 6810, 6840, 6870, 6900, 6930, 6960, 6990, 7020, 7050, 7080, 7110, 7140, 7170, 7200, 7230, 7260, 7290, 7320, 7350, 7380, 7410, 7440, 7470, 7500, 7530, 7560, 7590, 7620, 7650, 7680, 7710, 7740, 7770, 7800, 7830, 7860, 7890, 7920, 7950, 7980, 8010, 8040, 8070, 8100, 8130, 8160, 8190, 8220, 8250, 8280, 8310, 8340, 8370, 8400, 8430, 8460, 8490, 8520, 8550, 8580, 8610, 8640, 8670, 8700, 8730, 8760, 8790, 8820, 8850, 8880, 8910, 8940, 8970, 9000, 9030, 9060, 9090, 9120, 9150, 9180, 9210, 9240, 9270, 9300, 9330, 9360, 9390, 9420, 9450, 9480, 9510, 9540, 9570, 9600, 9630, 9660, 9690, 9720, 9750, 9780, 9810, 9840, 9870, 9900, 9930, 9960, 9990, 10020, 10050, 10080, 10110, 10140, 10170, 10200, 10230, 10260, 10290, 10320, 10350, 10380, 10410, 10440, 10470, 10500, 10530, 10560, 10590, 10620, 10650, 10680, 10710, 10740, 10770, 10800, 10830, 10860, 10890, 10920, 10950, 10980, 11010, 11040, 11070, 11100, 11130, 11160, 11190, 11220, 11250, 11280, 11310, 11340, 11370, 11400, 11430, 11460, 11490, 11520, 11550, 11580, 11610, 11640, 11670, 11700, 11730, 11760, 11790, 11820, 11850, 11880, 11910, 11940, 11970, 12000, 12030, 12060, 12090, 12120, 12150, 12180, 12210, 12240, 12270, 12300, 12330, 12360, 12390, 12420, 12450, 12480, 12510, 12540, 12570, 12600, 12630, 12660, 12690, 12720, 12750, 12780, 12810, 12840, 12870, 12900, 12930, 12960, 12990, 13020, 13050, 13080, 13110, 13140, 13170, 13200, 13230, 13260, 13290, 13320, 13350, 13380, 13410, 13440, 13470, 13500, 13530, 13560, 13590, 13620, 13650, 13680, 13710, 13740, 13770, 13800, 13830, 13860, 13890, 13920, 13950, 13980, 14010, 14040, 14070, 14100, 14130, 14160, 14190, 14220, 14250, 14280, 14310, 14340, 14370, 14400]
        else:
            CurveDatesList = []
            CurvePoints = [1, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330, 360, 390, 420, 450, 480, 510, 540, 570, 600, 630, 660, 690, 720, 750, 780, 810, 840, 870, 900, 930, 960, 990, 1020, 1050, 1080, 1110, 1140, 1170, 1200, 1230, 1260, 1290, 1320, 1350, 1380, 1410, 1440, 1470, 1500, 1530, 1560, 1590, 1620, 1650, 1680, 1710, 1740, 1770, 1800, 1830, 1860, 1890, 1920, 1950, 1980, 2010, 2040, 2070, 2100, 2130, 2160, 2190, 2220, 2250, 2280, 2310, 2340, 2370, 2400, 2430, 2460, 2490, 2520, 2550, 2580, 2610, 2640, 2670, 2700, 2730, 2760, 2790, 2820, 2850, 2880, 2910, 2940, 2970, 3000, 3030, 3060, 3090, 3120, 3150, 3180, 3210, 3240, 3270, 3300, 3330, 3360, 3390, 3420, 3450, 3480, 3510, 3540, 3570, 3600, 3630, 3660, 3690, 3720, 3750, 3780, 3810, 3840, 3870, 3900, 3930, 3960, 3990, 4020, 4050, 4080, 4110, 4140, 4170, 4200, 4230, 4260, 4290, 4320, 4350, 4380, 4410, 4440, 4470, 4500, 4530, 4560, 4590, 4620, 4650, 4680, 4710, 4740, 4770, 4800, 4830, 4860, 4890, 4920, 4950, 4980, 5010, 5040, 5070, 5100, 5130, 5160, 5190, 5220, 5250, 5280, 5310, 5340, 5370, 5400, 5430, 5460, 5490, 5520, 5550, 5580, 5610, 5640, 5670, 5700, 5730, 5760, 5790, 5820, 5850, 5880, 5910, 5940, 5970, 6000, 6030, 6060, 6090, 6120, 6150, 6180, 6210, 6240, 6270, 6300, 6330, 6360, 6390, 6420, 6450, 6480, 6510, 6540, 6570, 6600, 6630, 6660, 6690, 6720, 6750, 6780, 6810, 6840, 6870, 6900, 6930, 6960, 6990, 7020, 7050, 7080, 7110, 7140, 7170, 7200, 7230, 7260, 7290, 7320, 7350, 7380, 7410, 7440, 7470, 7500, 7530, 7560, 7590, 7620, 7650, 7680, 7710, 7740, 7770, 7800, 7830, 7860, 7890, 7920, 7950, 7980, 8010, 8040, 8070, 8100, 8130, 8160, 8190, 8220, 8250, 8280, 8310, 8340, 8370, 8400, 8430, 8460, 8490, 8520, 8550, 8580, 8610, 8640, 8670, 8700, 8730, 8760, 8790, 8820, 8850, 8880, 8910, 8940, 8970, 9000, 9030, 9060, 9090, 9120, 9150, 9180, 9210, 9240, 9270, 9300, 9330, 9360, 9390, 9420, 9450, 9480, 9510, 9540, 9570, 9600, 9630, 9660, 9690, 9720, 9750, 9780, 9810, 9840, 9870, 9900, 9930, 9960, 9990, 10020, 10050, 10080, 10110, 10140, 10170, 10200, 10230, 10260, 10290, 10320, 10350, 10380, 10410, 10440, 10470, 10500, 10530, 10560, 10590, 10620, 10650, 10680, 10710, 10740, 10770, 10800]

        if len(CurveDatesList) == 0:
            for InterpelatedPoints in CurvePoints:
                CurveDatesList.append(acm.Time().DateAddDelta(DateToday, 0, 0, int(InterpelatedPoints)))
        
        DateReference = 0
        if ACMyc.IsKindOf(acm.FCompositeCurve):
            for Interpelated in CurvePoints:
                GnVolMnyTrmSf0AXS = Interpelated
                GnVolMnyTrmSfNODE = ACMyc.IrCurveInformation().Rate(DateToday, CurveDatesList[DateReference], yc.storage_rate_type, yc.storage_daycount, 'Spot Rate', None, 0)
                DateReference += 1
                outfile.write('%s,%s,%s,%s,%s,%s\n'%(BASFLAG, Volatility, ATTRIBUTE, OBJECT, GnVolMnyTrmSf0AXS, GnVolMnyTrmSfNODE))
        else:
            ACMyc.Calculate()
            for Interpelated in CurvePoints:
                GnVolMnyTrmSf0AXS = Interpelated
                GnVolMnyTrmSfNODE = ACMyc.IrCurveInformation().Rate(DateToday, CurveDatesList[DateReference], yc.storage_rate_type, yc.storage_daycount, 'Spot Rate', None, 0)
                DateReference += 1
                outfile.write('%s,%s,%s,%s,%s,%s\n'%(BASFLAG, Volatility, ATTRIBUTE, OBJECT, GnVolMnyTrmSf0AXS, GnVolMnyTrmSfNODE))

       # Roll Over Function Parameters
        BASFLAG = 'rm_ro'
        Volatility = 'ZeroSPEC : Function Parameters'
        ATTRIBUTE = 'Function Parameters'
        OBJECT = 'ZeroSPEC'
        FunctionParamsVAL = ''
        if FunctionParamsVAL != '':
            outfile.write('%s,%s,%s,%s,%s\n'%(BASFLAG, Volatility, ATTRIBUTE, OBJECT, FunctionParamsVAL))
            
        # Roll Over  Procedure Parameter
        BASFLAG = 'rm_ro'
        Volatility = 'ZeroSPEC : Procedure Parameter'
        ATTRIBUTE = 'Procedure Parameter'
        OBJECT = 'ZeroSPEC'
        ProcedureParamXREF = ''
        if ProcedureParamXREF != '':
            outfile.write('%s,%s,%s,%s,%s\n'%(BASFLAG, Volatility, ATTRIBUTE, OBJECT, ProcedureParamXREF))


        # Base record
        BAS = 'BAS'
        ZeroSPEC = 'ZeroSPEC'
        OBJECT = 'ZeroSPEC'
        TYPE = 'Zero'
        
        IDENTIFIER = yc.yield_curve_name
        NAME = yc.yield_curve_name
        
        ActiveFLAG = 'TRUE'
        CreditStateENUM = ''
        CurveFUNC = '@sum'

        CurveUnitCAL = ''       
        CurveUnitDAYC = MR_MainFunctions.DayCountFix(yc.storage_daycount)       
        CurveUnitPERD = MR_MainFunctions.BusRule(yc.storage_rate_type)       
        CurveUnitUNIT = '%'

        DatumDATE = MR_MainFunctions.Datefix(acm.Time().DateNow())
        OriginOffsetNB = '0'
        RelativeCurveFLAG = 'TRUE'
        StateProcFUNC = ''
        TimeEvolutionFUNC = '@Constant'
        FunctionIdFLAG = 'TRUE'
        GenZeroSfExt0FLAG = 'FALSE'
        GenZeroSurface0SIN = '@Linear'
        
        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BAS, ZeroSPEC, OBJECT, TYPE, IDENTIFIER, NAME, ActiveFLAG, CreditStateENUM, CurveFUNC, CurveUnitCAL, CurveUnitDAYC, CurveUnitPERD, CurveUnitUNIT, DatumDATE, OriginOffsetNB, RelativeCurveFLAG, StateProcFUNC, TimeEvolutionFUNC, FunctionIdFLAG, GenZeroSfExt0FLAG, GenZeroSurface0SIN))

        # Roll Over  Procedure Parameter
        BASFLAG = 'rm_ro'
        HEADERNAME = 'ZeroSPEC : Procedure Parameter'
        ATTRIBUTE = 'Procedure Parameter'
        OBJECT = 'ZeroSPEC'
	#underlying yield curve
        ProcedureParamXREF = yc.yield_curve_name + '_Base'

        if ProcedureParamXREF != '':
            outfile.write('%s,%s,%s,%s,%s\n'%(BASFLAG, HEADERNAME, ATTRIBUTE, OBJECT, ProcedureParamXREF))

    return str(YcSeqnbr)
    
    outfile.close()
        
# WRITE - FILE ######################################################################################################
