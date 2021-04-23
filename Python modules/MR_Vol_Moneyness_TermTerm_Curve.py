'''
Purpose                 :Market Risk feed files
Department and Desk     :IT
Requester:              :Natalie Austin
Developer               :Douglas Finkel / Henk Nel
CR Number               :264536
'''

import ael, string, acm, MR_MainFunctions

InsL = []

# OPENFILE ##########################################################################################################
    
def OpenFile(temp,FileDir,Filename,*rest):
    filename            = FileDir + Filename
    outfile             =  open(filename, 'w')
    outfile.close()

    del InsL[:]
    InsL[:] = []

    return filename

# OPENFILE ##########################################################################################################

def vol_bm_mat(ins):
    dt = ael.date_today()
    
    if ins.instype in ('Cap', 'Floor'):
        per = ins.legs()[0].rolling_period
    elif ins.instype == 'Option':
        per = ins.und_insaddr.legs()[0].end_period
    else:
        per = ''
        
    if per == '':
        return ael.date('1899-12-31').to_string('%y%m%d') + '_0d'
    else:        
        return dt.add_period(per)


def vol_bm_exp(ins):
    dt = ael.date_today()
    
    if ins.instype in ('Cap', 'Floor'):
        per = ins.legs()[0].end_period        
    elif ins.instype == 'Option':
        per = ins.exp_period
    else:
        per = ''
        
    if per == '':
        return ael.date('1899-12-31').to_string('%y%m%d') + '_0d'
    else:       
        return dt.add_period(per)

# WRITE - FILE ######################################################################################################

def Write(v,FileDir,Filename,*rest):    
    filename            = FileDir + Filename    
    if (v.seqnbr) not in InsL:
        InsL.append(v.seqnbr)
        outfile = open(filename, 'a')
        
        relativeStrikePriceFromAbsolute = acm.GetFunction('relativeStrikePriceFromAbsolute', 4)
        cs = acm.Calculations().CreateStandardCalculationsSpaceCollection()

        volsurfacedict = {}
        #points in vol surface
        #acm.FInstrument['USD/CAP/1Y/RFWD-2'].Inspect()
        for points in v.points():
            
            if points.insaddr:
                ins = acm.FInstrument[points.insaddr.insaddr]
                ins_calc = ins.Underlying().Calculation()
                und_price =  ins_calc.TheoreticalPrice(cs)

                
                if points.insaddr.strike_type in ('Rel Frw', 'Rel Spot'):
                    Strike              =       points.insaddr.strike_price
                else:
                    Strike              =       round(relativeStrikePriceFromAbsolute(und_price, ins.StrikePrice(), 3, False).Number(), 1)
                    
                    if str(Strike) == '1.#QNAN':
                        Strike          =       points.strike
                           
                GnVolMnyTrmSf0AXS   =       ael.date_today().days_between(vol_bm_mat(points.insaddr))
                GnVolMnyTrmSf1AXS   =       ael.date_today().days_between(vol_bm_exp(points.insaddr))
                GnVolMnyTrmSfNODE   =       v.vol_get(ins.StrikePrice(), vol_bm_exp(points.insaddr), vol_bm_mat(points.insaddr), 1)
                
            else:
            
                #print v.vol_name, points.strike, v.vol_type
                Strike              =       points.strike
                GnVolMnyTrmSf0AXS   =       MR_MainFunctions.CurveDays(points.undmat_period)
                GnVolMnyTrmSf1AXS   =       MR_MainFunctions.CurveDays(points.exp_period)
                GnVolMnyTrmSfNODE   =       points.volatility
            
            #Creating dictionary to hold intial 3D vol surface values
            
            if volsurfacedict.has_key(Strike):
                volsurfacedict[Strike][GnVolMnyTrmSf0AXS, GnVolMnyTrmSf1AXS] = GnVolMnyTrmSfNODE
            else:
                volsurfacedict[Strike]={}
                volsurfacedict[Strike][GnVolMnyTrmSf0AXS, GnVolMnyTrmSf1AXS] = GnVolMnyTrmSfNODE
                
                
        for Strike in volsurfacedict.keys():
        
            #Base record
            BAS	                =       'BAS'
            HeaderName          =	'Volatility - Term/TermSPEC'
            OBJECT              =       'Volatility - Term/TermSPEC'
            TYPE                =       'Volatility - Term/Term'
            
            IDENTIFIER	        =       v.vol_name + '_TT_' + str(Strike)
            NAME                =       v.vol_name + '_TT_' + str(Strike)
            
            ActiveFLAG          =       'TRUE'
            
            CurveUnitCAL	=       ''        
            CurveUnitDAYC       =       MR_MainFunctions.DayCountFix('Act/365')        
            CurveUnitPERD       =       'annual'	
            CurveUnitUNIT	=       '%'
            
            DatumDATE	        =       MR_MainFunctions.Datefix(acm.Time().DateNow())
            OriginOffsetNB	=       '0'
            
            RelativeCurveFLAG	=       'TRUE'
            
            if v.vol_type == 'Benchmark Spread Call/Put':
                StateProcFUNC       =       '@spread'
            else: 
                StateProcFUNC       =       ''
                
            TimeEvolutionFUNC	=       '@Constant'        
            FunctionIdFLAG	=       'TRUE'     
            
            GenVolSTSfExt0FLAG	=       'FALSE'
            GenVolSTSfExt1FLAG	=       'FALSE'
            GenVolStrTrmSf0SIN  =       '@Linear'
            GenVolStrTrmSf1SIN  =       '@Linear'
        
            outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BAS, HeaderName, OBJECT, TYPE, IDENTIFIER, NAME, ActiveFLAG, CurveUnitCAL, CurveUnitDAYC, CurveUnitPERD, CurveUnitUNIT, DatumDATE, OriginOffsetNB, RelativeCurveFLAG, StateProcFUNC, TimeEvolutionFUNC, FunctionIdFLAG, GenVolSTSfExt0FLAG, GenVolSTSfExt1FLAG, GenVolStrTrmSf0SIN, GenVolStrTrmSf1SIN))

            # Roll Over Function Parameters
            BASFLAG                 =       'rm_ro'
            Volatility              =       'Volatility - Term/TermSPEC : Function Parameters'
            ATTRIBUTE               =       'Function Parameters'
            OBJECT                  =       'Volatility - Term/TermSPEC'
            FunctionParamsVAL       =       ''
            if FunctionParamsVAL != '':
                outfile.write('%s,%s,%s,%s,%s\n'%(BASFLAG, Volatility, ATTRIBUTE, OBJECT, FunctionParamsVAL))
            
            # Roll Over  Procedure Parameter
            BASFLAG                 =       'rm_ro'
            Volatility              =       'Volatility - Term/TermSPEC : Procedure Parameter'
            ATTRIBUTE               =       'Procedure Parameter'
            OBJECT                  =       'Volatility - Term/TermSPEC'
            
            if v.und_vol_seqnbr:
                ProcedureParamXREF      =       v.und_vol_seqnbr.vol_name + '_TT_0.0'
            else:
                ProcedureParamXREF      =       ''
            
            if ProcedureParamXREF != '':
                outfile.write('%s,%s,%s,%s,%s\n'%(BASFLAG, Volatility, ATTRIBUTE, OBJECT, ProcedureParamXREF))                

            # Build volatility surface
            for Key in  volsurfacedict[Strike].keys():
                
                # Roll Over Generic Volatility Term Term Surface
                
                BASFLAG                 =       'rm_ro'
                Volatility              =       'Volatility - Term/TermSPEC : Generic Volatility Term Term Surface'
                ATTRIBUTE               =       'Generic Volatility Term Term Surface'
                OBJECT                  =       'Volatility - Term/TermSPEC'

                GnVolMnyTrmSf0AXS       =       Key[0] 
                GnVolMnyTrmSf1AXS       =       Key[1]
                GnVolMnyTrmSfNODE       =       volsurfacedict[Strike][GnVolMnyTrmSf0AXS, GnVolMnyTrmSf1AXS]

                outfile.write('%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, Volatility, ATTRIBUTE, OBJECT, GnVolMnyTrmSf0AXS, GnVolMnyTrmSf1AXS, GnVolMnyTrmSfNODE))


        
        BAS	                =       'BAS'
        HeaderName          =	'Volatility - Moneyness/Term/TermSPEC'
        OBJECT              =       'Volatility - Moneyness/Term/TermSPEC'
        TYPE                =       'Volatility - Moneyness/Term/Term'
        IDENTIFIER	        =       v.vol_name
        NAME                =       v.vol_name
        CurveUnitDAYC       =       MR_MainFunctions.DayCountFix('Act/365')    
        CurveUnitPERD       =       'annual'
        CurveUnitCAL	=       ''        
        RelativeCurveFLAG	=       'TRUE'
        OriginOffsetNB	=       '0'
        TimeEvolutionFUNC	=       '@Constant'        
        FunctionIdFLAG	=       'TRUE'     
        DatumDATE	        =       MR_MainFunctions.Datefix(acm.Time().DateNow())
        CurveFUNC       =               '@term/term 3D'
        MoneynessTypeENUM       = 'S - K'

        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BAS, HeaderName, OBJECT, TYPE, IDENTIFIER, NAME, CurveUnitDAYC, CurveUnitPERD, CurveUnitCAL, RelativeCurveFLAG, OriginOffsetNB, TimeEvolutionFUNC, FunctionIdFLAG, DatumDATE, CurveFUNC, MoneynessTypeENUM))
    
        for Strike in sorted(volsurfacedict.keys()):
        
            BASFLAG                 =       'rm_ro'
            Volatility              =       'Volatility - Moneyness/Term/TermSPEC : Procedure Parameters'
            ATTRIBUTE               =       'Procedure Parameter'
            OBJECT                  =       'Volatility - Moneyness/Term/TermSPEC'
            ProcedureParamXREF      =       v.vol_name + '_TT_' + str(Strike)
            
            if ProcedureParamXREF != '':
                outfile.write('%s,%s,%s,%s,%s\n'%(BASFLAG, Volatility, ATTRIBUTE, OBJECT, ProcedureParamXREF))
            
            BASFLAG                 =       'rm_ro'
            Volatility              =       'Volatility - Moneyness/Term/TermSPEC : Function Parameters'
            ATTRIBUTE               =       'Function Parameters'
            OBJECT                  =       'Volatility - Moneyness/Term/TermSPEC'
            FunctionParamsVAL       =       Strike
            
            if FunctionParamsVAL != '':
                outfile.write('%s,%s,%s,%s,%s\n'%(BASFLAG, Volatility, ATTRIBUTE, OBJECT, FunctionParamsVAL))
                
        outfile.close()

    return 'Success'
    
# WRITE - FILE ######################################################################################################




