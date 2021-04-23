'''
Purpose                 :Market Risk feed files
Department and Desk     :IT
Requester:              :Natalie Austin
Developer               :Douglas Finkel
CR Number               :264536,278978,480836,522873,677357,686302, 692658, 883286

Description             :Added separate logic for randised USD curves only - @Inverse Constant
Description             :Added separate logic for randised USD curves only - DatumDATE
Description             :Added new randised curve - ZAR/REDW/SAFEX

'''

import ael, string, acm, PositionFile, MR_MainFunctions
InsL = []
RandisedL = []

# OPENFILE ##########################################################################################################
    
def OpenFile(temp,FileDir,Filename,*rest):
    
    filename            = FileDir + Filename
    outfile             =  open(filename, 'w')
    outfile.close()
    
    del InsL[:]
    InsL[:] = []
    
    del RandisedL[:]
    RandisedL[:] = []
    
    return filename

# OPENFILE ##########################################################################################################



# WRITE2 - FILE #####################################################################################################

def Write2(ycSeqNbr,FileDir,Filename,*rest):
    
    yc = ael.YieldCurve[ycSeqNbr]
    filename = FileDir + Filename
    RandisedOutfile = open(filename, 'a')
    
    # PART TWO - Only Randised Spot Commodities
    # PART TWO (A) - FXconv curve
    # Base record
    # Spot Commodity (Randised)	Spot Commodity (Foreign)	ExchangeRate	ConversionConstant
    # ZAR/BEAN/SAFEX	        USD/SOYA/CBOT	                USD/ZAR_IP	0.367437
    # ZAR/COPP/SAFEX	        USD/COPPER/COMEX	        USD/ZAR_IP	0.01
    # ZAR/CORN/SAFEX	        USD/HRCORN/CBOT	                USD/ZAR_IP	0.393679
    # ZAR/GOLD/SAFEX	        USD/GOLD/COMEX	                USD/ZAR_IP	1
    # ZAR/MEAL/SAFEX	        USD/SOYMEAL/CBOT	        USD/ZAR_IP	1.103
    # ZAR/OILS/SAFEX	        USD/SOYOIL/CBOT	                USD/ZAR_IP	22.0523
    # ZAR/PLAT/SAFEX	        USD/PLAT/NYMEX	                USD/ZAR_IP	1
    # ZAR/SILV/SAFEX	        USD/SILVER/COMEX	        USD/ZAR_IP	1
    # ZAR/WTIO/SAFEX	        USD/WTICrude/NME	        USD/ZAR_IP	1
    # ZAR/REDW/SAFEX            USD/HRWEAT/CBOT                 USD/ZAR_IP      0.36745
    # ZAR/HRWWEAT/SAFEX         USD/HRWWEAT/KCBT                USD/ZAR_IP      0.354143 

    # ############################################################################################################################



    # Date Change 01 November 2010
    # Changed by: Douglas Finkel
    # Purpose: The name of the given curves was incorrect and adjusted


    dict={}
    dict['ZAR/BEAN/SAFEX_Curve'] = ('USD/SOYA', 'USD/ZAR_IP', 'USD/ZAR_Compound_Rate', '0.367437')
    dict['ZAR/COPP/SAFEX_Curve'] = ('USD/COPPER/COMEX_Curve', 'USD/ZAR_IP', 'USD/ZAR_Compound_Rate', '0.01')
    dict['ZAR/CORN/SAFEX_Curve'] = ('USD/CORN', 'USD/ZAR_IP', 'USD/ZAR_Compound_Rate', '0.393679')
    dict['ZAR/GOLD/SAFEX_Curve'] = ('USD/GOLD/COMEX_Curve', 'USD/ZAR_IP', 'USD/ZAR_Compound_Rate', '1')
    dict['ZAR/MEAL/SAFEX_Curve'] = ('USD/SOYMEAL', 'USD/ZAR_IP', 'USD/ZAR_Compound_Rate', '1.103')
    dict['ZAR/OILS/SAFEX_Curve'] = ('USD/SOYOIL', 'USD/ZAR_IP', 'USD/ZAR_Compound_Rate', '22.0523')
    dict['ZAR/PLAT/SAFEX_Curve'] = ('USD/PLAT/NYMEX_Curve', 'USD/ZAR_IP', 'USD/ZAR_Compound_Rate', '1')
    dict['ZAR/SILV/SAFEX_Curve'] = ('USD/SILVER/COMEX_Curve', 'USD/ZAR_IP', 'USD/ZAR_Compound_Rate', '1')
    dict['ZAR/WTIO/SAFEX_Curve'] = ('WTI_Crude', 'USD/ZAR_IP', 'USD/ZAR_Compound_Rate', '1')
    dict['ZAR/REDW/SAFEX_Curve'] = ('USD/WHEAT', 'USD/ZAR_IP', 'USD/ZAR_Compound_Rate', '0.36745')
    dict['ZAR/WEAT/KCBT']        = ('USD/WHEAT/KCBT', 'USD/ZAR_IP', 'USD/ZAR_Compound_Rate', '0.354143')
    
    if dict.has_key(yc.yield_curve_name):
        Foreign, ExchangeRate, Compound_Rate, ConversionConstant =   dict[yc.yield_curve_name]
        
        BASFLAG                 =       'BAS'
        HeaderName              =       'Forward CurveSPEC'
        OBJECT                  =       'Forward CurveSPEC'
        TYPE                    =       'Forward Curve'
        IDENTIFIER              =       yc.yield_curve_name + '_FXconv'
        NAME                    =       yc.yield_curve_name + '_FXConv'
        CurveFUNC               =       '@product'
        CurveUnitDAYC           =       ''
        CurveUnitPERD           =       ''
        CurveUnitUNIT           =       yc.curr.insid
        DatumDATE               =       '0'
        ForwardSurf0EXT         =       'FALSE'
        ForwardSurf0SIN         =       '@Linear'
        FunctionIdFLAG          =       'TRUE'
        PromptCurveXREF         =       ''
        
        RandisedOutfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, IDENTIFIER, NAME, CurveFUNC, CurveUnitDAYC, CurveUnitPERD, CurveUnitUNIT, DatumDATE, ForwardSurf0EXT, ForwardSurf0SIN, FunctionIdFLAG, PromptCurveXREF))
        
        # Roll Over Forward Surface
        BASFLAG                 =       'rm_ro'
        Volatility              =       'Forward CurveSPEC : Forward Surface'
        ATTRIBUTE               =       'Forward Surface'
        OBJECT                  =       'Forward CurveSPEC'
        
        cs = acm.Calculations().CreateStandardCalculationsSpaceCollection()
        
        for benchmarks in yc.benchmarks():
            ins = acm.FInstrument[benchmarks.instrument.insid]
            
            if ins.ExpiryDate():
                days_to_expiry = ael.date_today().days_between(ael.date(ins.ExpiryDateOnly()))
            elif ins.ExpiryPeriod():
                days_to_expiry = MR_MainFunctions.CurveDays(ins.ExpiryPeriod())
            else:
                days_to_expiry = ''
            
            ForwardSurf0AXS     =       days_to_expiry
            
            calc = ins.Calculation()
            TheoPrice = calc.TheoreticalPrice(cs)

            if ins.MtmFromFeed():
                if str(ins.SLPrice()) in ('1.#QNAN', 'NaN', 'nan'):
                    ForwardSurfNODE = ''
                else:
                    ForwardSurfNODE = ins.SLPrice()
            else:
                try:
                    if str(TheoPrice.Number()) in ('1.#QNAN', 'NaN', 'nan'):
                        ForwardSurfNODE   =       ''
                    else:
                        ForwardSurfNODE   =       TheoPrice.Number()
                except:
                    ForwardSurfNODE     =   ''

            if ForwardSurfNODE != '':
                ForwardSurfNODE = 0
                RandisedOutfile.write('%s,%s,%s,%s,%s,%s\n'%(BASFLAG, Volatility, ATTRIBUTE, OBJECT, ForwardSurf0AXS, ForwardSurfNODE))
        
        # Roll Over Function Parameters
        BASFLAG                 =       'rm_ro'
        Volatility              =       'Forward CurveSPEC : Function Parameters'
        ATTRIBUTE               =       'Function Parameters'
        OBJECT                  =       'Forward CurveSPEC'
        FunctionParamsVAL       =       ''
        if FunctionParamsVAL   !=       '':
            RandisedOutfile.write('%s,%s,%s,%s,%s\n'%(BASFLAG, Volatility, ATTRIBUTE, OBJECT, FunctionParamsVAL))
        
        # Roll Over  Procedure Parameter exchange rate
        BASFLAG                 =       'rm_ro'
        Volatility              =       'Forward CurveSPEC : Procedure Parameter'
        ATTRIBUTE               =       'Procedure Parameter'
        OBJECT                  =       'Forward CurveSPEC'
        ProcedureParamXREF      =       ExchangeRate #Assign the exchange rate (from table)
        if ProcedureParamXREF  !=       '':
            RandisedOutfile.write('%s,%s,%s,%s,%s\n'%(BASFLAG, Volatility, ATTRIBUTE, OBJECT, ProcedureParamXREF))
      
        # Roll Over  Procedure Parameter exchange rate
        BASFLAG                 =       'rm_ro'
        Volatility              =       'Forward CurveSPEC : Procedure Parameter'
        ATTRIBUTE               =       'Procedure Parameter'
        OBJECT                  =       'Forward CurveSPEC'
        ProcedureParamXREF      =       Compound_Rate #Assign the compound rate (from table)
        if ProcedureParamXREF  !=       '':
            RandisedOutfile.write('%s,%s,%s,%s,%s\n'%(BASFLAG, Volatility, ATTRIBUTE, OBJECT, ProcedureParamXREF))

        # Roll Over  Procedure Parameter Driver/Underlying Foreign Spot Commodity
        BASFLAG                 =       'rm_ro'
        Volatility              =       'Forward CurveSPEC : Procedure Parameter'
        ATTRIBUTE               =       'Procedure Parameter'
        OBJECT                  =       'Forward CurveSPEC'
        ProcedureParamXREF      =       Foreign + '_FwdCurve' #Assign the foreign spot commodity forward curve (from table)
        if ProcedureParamXREF  !=       '':
            RandisedOutfile.write('%s,%s,%s,%s,%s\n'%(BASFLAG, Volatility, ATTRIBUTE, OBJECT, ProcedureParamXREF))
        
        # ############################################################################################################################
        
        #PART TWO (B) - Randised Forward Curve
        #Base record
        BASFLAG                 =       'BAS'
        HeaderName              =       'Forward CurveSPEC'
        OBJECT                  =       'Forward CurveSPEC'
        TYPE                    =       'Forward Curve'
        IDENTIFIER              =       yc.yield_curve_name + '_FwdCurve'
        NAME                    =       yc.yield_curve_name + '_FwdCurve'
        CurveFUNC		        =       '@factor sum'
        CurveUnitDAYC           =       ''
        CurveUnitPERD           =       ''
        CurveUnitUNIT           =       yc.curr.insid
        DatumDATE               =       ael.date_today()
        ForwardSurf0EXT         =       'FALSE'
        
        ForwardSurf0SIN         =       '@Linear'
        
        FunctionIdFLAG          =       'TRUE'
        PromptCurveXREF         =       yc.yield_curve_name + '_PromptCurve'
        RandisedOutfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, IDENTIFIER, NAME, CurveFUNC, CurveUnitDAYC, CurveUnitPERD, CurveUnitUNIT, DatumDATE, ForwardSurf0EXT, ForwardSurf0SIN, FunctionIdFLAG, PromptCurveXREF))
        
        # Roll Over Forward Surface
        BASFLAG                 =       'rm_ro'
        Volatility              =       'Forward CurveSPEC : Forward Surface'
        ATTRIBUTE               =       'Forward Surface'
        OBJECT                  =       'Forward CurveSPEC'
        
        cs = acm.Calculations().CreateStandardCalculationsSpaceCollection()
        
        for benchmarks in yc.benchmarks():
            ins = acm.FInstrument[benchmarks.instrument.insid]

            if ins.ExpiryDate():
                days_to_expiry = ael.date_today().days_between(ael.date(ins.ExpiryDateOnly()))
            elif ins.ExpiryPeriod():
                days_to_expiry = MR_MainFunctions.CurveDays(ins.ExpiryPeriod())
            else:
                days_to_expiry  = ''
            
            ForwardSurf0AXS     = days_to_expiry
            
            calc = ins.Calculation()
            TheoPrice = calc.TheoreticalPrice(cs)

            if ins.MtmFromFeed():
                if str(ins.SLPrice()) in ('1.#QNAN', 'NaN', 'nan'):
                    ForwardSurfNODE = ''
                else:
                    ForwardSurfNODE = ins.SLPrice()
            else:
                try:
                    if str(TheoPrice.Number()) in ('1.#QNAN', 'NaN', 'nan'):
                        ForwardSurfNODE   =       ''
                    else:
                        ForwardSurfNODE   =       TheoPrice.Number()
                except:
                    ForwardSurfNODE     =   ''

            if ForwardSurfNODE != '':
                ForwardSurfNODE = 0
                RandisedOutfile.write('%s,%s,%s,%s,%s,%s\n'%(BASFLAG, Volatility, ATTRIBUTE, OBJECT, ForwardSurf0AXS, ForwardSurfNODE))
        
        # Roll Over Function Parameters
        BASFLAG                 =       'rm_ro'
        Volatility              =       'Forward CurveSPEC : Function Parameters'
        ATTRIBUTE               =       'Function Parameters'
        OBJECT                  =       'Forward CurveSPEC'
        FunctionParamsVAL       =       ConversionConstant #conversion factor from table
        RandisedOutfile.write('%s,%s,%s,%s,%s\n'%(BASFLAG, Volatility, ATTRIBUTE, OBJECT, FunctionParamsVAL))
        
        # Roll Over  Procedure Parameter Driver/Underlying Foreign Spot Commodity
        BASFLAG                 =       'rm_ro'
        Volatility              =       'Forward CurveSPEC : Procedure Parameter'
        ATTRIBUTE               =       'Procedure Parameter'
        OBJECT                  =       'Forward CurveSPEC'
        ProcedureParamXREF      =       yc.yield_curve_name + '_FXconv' #Assign the randised spot commodity fx converter curve curve (created in Part TWO (A))
        if ProcedureParamXREF  !=       '':
            RandisedOutfile.write('%s,%s,%s,%s,%s\n'%(BASFLAG, Volatility, ATTRIBUTE, OBJECT, ProcedureParamXREF))
        
        RandisedOutfile.close()
    
    return str(ycSeqNbr)

# WRITE2 - FILE #####################################################################################################



# WRITE - FILE ######################################################################################################
def Write(i,FileDir,Filename,*rest):

    # ###############################################################################################################
    # PART ONE - Normal Spot Commodities
    # Exclude all randised foreign commodities (see table for list of commodities to exclude)
    # Added: Douglas Finkel
    # Date: 28 October 2010

    filename = FileDir + Filename
    
    '''    This was coded so as to get all the forward curves attached to the Spot Commodity instruments    '''
    
    if str(i.add_info('Agri Forward Curve')) == '':
        return i.insid
    else:
        ycName = str(i.add_info('Agri Forward Curve'))
        
    yc = ael.YieldCurve[ycName]
    
    if not yc:
        return ''
    
    if (yc.seqnbr) not in InsL:
        InsL.append(yc.seqnbr)
        if yc.yield_curve_type != 'Instrument Spread':
            
            #add additional info if adding randised curve
            if yc.yield_curve_name in ('ZAR/BEAN/SAFEX_Curve', 'ZAR/COPP/SAFEX_Curve', 'ZAR/CORN/SAFEX_Curve', 'ZAR/GOLD/SAFEX_Curve', 'ZAR/MEAL/SAFEX_Curve', 'ZAR/OILS/SAFEX_Curve', 'ZAR/PLAT/SAFEX_Curve', 'ZAR/SILV/SAFEX_Curve', 'ZAR/WTIO/SAFEX_Curve', 'ZAR/REDW/SAFEX_Curve', 'ZAR/WEAT/KCBT'):
                if (yc.seqnbr) not in RandisedL:
                    #RandisedL.append(yc.seqnbr)
                    Write2(yc.seqnbr, FileDir, Filename)
                return yc.yield_curve_name
            
            outfile = open(filename, 'a')
            #Base record
            BASFLAG                 =       'BAS'
            HeaderName              =       'Forward CurveSPEC'
            OBJECT                  =       'Forward CurveSPEC'
            TYPE                    =       'Forward Curve'
            IDENTIFIER              =       yc.yield_curve_name + '_FwdCurve'
            NAME                    =       yc.yield_curve_name + '_FwdCurve'
            CurveFUNC               =       ''
            CurveUnitDAYC           =       ''
            CurveUnitPERD           =       ''
            CurveUnitUNIT           =       yc.curr.insid
            DatumDATE               =       '0'
            ForwardSurf0EXT         =       'FALSE'

            # ################################################
            # Added for randised USD curves only
            if (yc.curr.insid == 'USD'):
                ForwardSurf0SIN     =       '@Inverse Constant'
                DatumDATE           =       ael.date_today()
            else:
                ForwardSurf0SIN     =       '@Linear'
            FunctionIdFLAG          =       'TRUE'
            PromptCurveXREF         =       yc.yield_curve_name + '_PromptCurve'
            
            outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, IDENTIFIER, NAME, CurveFUNC, CurveUnitDAYC, CurveUnitPERD, CurveUnitUNIT, DatumDATE, ForwardSurf0EXT, ForwardSurf0SIN, FunctionIdFLAG, PromptCurveXREF))
            
            BASFLAG                 =       'rm_ro'
            Volatility              =       'Forward CurveSPEC : Forward Surface'
            ATTRIBUTE               =       'Forward Surface'
            OBJECT                  =       'Forward CurveSPEC'
            
            ForwardSurf0AXS         =       ''
            ForwardSurfNODE         =       ''
            
            cs = acm.Calculations().CreateStandardCalculationsSpaceCollection()
            
            for benchmarks in yc.benchmarks():
                ins = acm.FInstrument[benchmarks.instrument.insid]
                
                if ins.ExpiryDate():
                    days_to_expiry = ael.date_today().days_between(ael.date(ins.ExpiryDateOnly()))
                elif ins.ExpiryPeriod():
                    days_to_expiry = MR_MainFunctions.CurveDays(ins.ExpiryPeriod())
                else:
                    days_to_expiry = ''
                
                ForwardSurf0AXS   =       days_to_expiry
                
                calc = ins.Calculation()
                TheoPrice = calc.TheoreticalPrice(cs)
                
                '''Changed by Douglas Finkel - 27 October 2010'''
                '''From Price of the Instrument to Theoretical Price on Instrument'''
                if ins.MtmFromFeed():
                    if str(ins.SLPrice()) in ('1.#QNAN', 'NaN', 'nan'):
                        ForwardSurfNODE = ''
                    else:
                        ForwardSurfNODE = ins.SLPrice()
                else:
                    try:
                        if str(TheoPrice.Number()) in ('1.#QNAN', 'NaN', 'nan'):
                            ForwardSurfNODE   =       ''
                        else:
                            ForwardSurfNODE   =       TheoPrice.Number()
                    except:
                        ForwardSurfNODE     =   ''
                
                '''
                if str(ins.SLPrice()) in ('1.#QNAN','NaN','nan'):
                    ForwardSurfNODE   =    ''
                else:
                    ForwardSurfNODE   =       ins.SLPrice()
                '''
                
                if ForwardSurfNODE   !=    '':
                    outfile.write('%s,%s,%s,%s,%s,%s\n'%(BASFLAG, Volatility, ATTRIBUTE, OBJECT, ForwardSurf0AXS, ForwardSurfNODE))
            
            # Roll Over Function Parameters
            BASFLAG                 =       'rm_ro'
            Volatility              =       'Forward CurveSPEC : Function Parameters'
            ATTRIBUTE               =       'Function Parameters'
            OBJECT                  =       'Forward CurveSPEC'
            FunctionParamsVAL       =       ''
            if FunctionParamsVAL   !=       '':
                outfile.write('%s,%s,%s,%s,%s\n'%(BASFLAG, Volatility, ATTRIBUTE, OBJECT, FunctionParamsVAL))
            
            # Roll Over  Procedure Parameter
            BASFLAG                 =       'rm_ro'
            Volatility              =       'Forward CurveSPEC : Procedure Parameter'
            ATTRIBUTE               =       'Procedure Parameter'
            OBJECT                  =       'Forward CurveSPEC'
            ProcedureParamXREF      =       ''
            if ProcedureParamXREF  !=       '':
                outfile.write('%s,%s,%s,%s,%s\n'%(BASFLAG, Volatility, ATTRIBUTE, OBJECT, ProcedureParamXREF))
                
            outfile.close()
            
    return yc.yield_curve_name
# WRITE - FILE ######################################################################################################

