'''
Purpose                 :Market Risk feed files
Department and Desk     :IT
Requester:              :Natalie Austin
Developer               :Douglas Finkel / Henk Nel
CR Number               :264536
'''

'''
Purpose                 :Market Risk feed files
Department and Desk     :IT
Requester:              :Natalie Austin
Developer               :Douglas Finkel / Henk Nel
CR Number               :289168
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



# WRITE - FILE ######################################################################################################

def Write(v,FileDir,Filename,*rest):    
    filename            = FileDir + Filename   
    relativeStrikePriceFromAbsolute = acm.GetFunction('relativeStrikePriceFromAbsolute', 4) 
    cs = acm.Calculations().CreateStandardCalculationsSpaceCollection() 
    if (v.seqnbr) not in InsL:
        InsL.append(v.seqnbr)
        outfile = open(filename, 'a')
    
        #Base record
        
        BAS                     =       'BAS'
        Volatility              =       'Volatility - Moneyness/TermSPEC'
        OBJECT                  =       'Volatility - Moneyness/TermSPEC'
        TYPE                    =       'Volatility - Moneyness/Term'
        IDENTIFIER              =       v.vol_name
        NAME                    =       v.vol_name
        
        ActiveFLAG              =       'TRUE'
        
        CurveUnitCAL            =       ''                
        CurveUnitDAYC           =       MR_MainFunctions.DayCountFix('Act/365')        
        CurveUnitPERD           =       'annual'    
        CurveUnitUNIT            =       '%'
        
        DatumDATE               =       MR_MainFunctions.Datefix(acm.Time().DateNow())
        
        OriginOffsetNB          =       '0'
        RelativeCurveFLAG       =       'TRUE'
        StateProcFUNC           =       ''
        TimeEvolutionFUNC       =       '@Constant'
        FunctionIdFLAG          =       'TRUE'
        
        GnVolMTSfExt0FLAG       =       'FALSE'
        GnVolMTSfExt1FLAG       =       'FALSE'
        GnVolMnyTrmSf0SIN       =       '@Linear'
        GnVolMnyTrmSf1SIN       =       '@Linear'
        
        MoneynessTypeENUM       =       'K / S'
     
        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BAS, Volatility, OBJECT, TYPE, IDENTIFIER, NAME, ActiveFLAG, CurveUnitCAL, CurveUnitDAYC, CurveUnitPERD, CurveUnitUNIT, DatumDATE, OriginOffsetNB, RelativeCurveFLAG, StateProcFUNC, TimeEvolutionFUNC, FunctionIdFLAG, GnVolMTSfExt0FLAG, GnVolMTSfExt1FLAG, GnVolMnyTrmSf0SIN, GnVolMnyTrmSf1SIN, MoneynessTypeENUM))
        
        # Roll Over Generic Volatility Moneyness Term Surface
    
        BASFLAG                 =       'rm_ro'
        Volatility              =       'Volatility - Moneyness/TermSPEC : Generic Volatility Moneyness Term Surface'
        ATTRIBUTE               =       'Generic Volatility Moneyness Term Surface'
        OBJECT                  =       'Volatility - Moneyness/TermSPEC'

        GnVolMnyTrmSf0AXS       =       '' 
        GnVolMnyTrmSf1AXS       =       '' 
        GnVolMnyTrmSfNODE       =       '' 

        for points in v.points():
#            print points.insaddr.insid
            if points.insaddr:
                ins = acm.FInstrument[points.insaddr.insid]
                ins_calc = ins.Underlying().Calculation()
                
                #GnVolMnyTrmSf0AXS   =   points.insaddr.strike_price
                if ins_calc.TheoreticalPrice(cs).Number() == 0:
                    GnVolMnyTrmSf0AXS   =   0
                    print 'Zero underlying price in instrument {0}'.format(ins.Name())
                else:
                    GnVolMnyTrmSf0AXS   =   ins.StrikePrice() / ins_calc.TheoreticalPrice(cs).Number()
                
                GnVolMnyTrmSf1AXS   =   ael.date_today().days_between(points.insaddr.exp_day) #MR_MainFunctions.CurveDays(points.insaddr.exp_period)            
            else:
                GnVolMnyTrmSf0AXS   =       points.strike
                GnVolMnyTrmSf1AXS   =       MR_MainFunctions.CurveDays(points.exp_period)
            
            GnVolMnyTrmSfNODE   =       points.volatility
              
            outfile.write('%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, Volatility, ATTRIBUTE, OBJECT, GnVolMnyTrmSf0AXS, GnVolMnyTrmSf1AXS, GnVolMnyTrmSfNODE))
    
    
        # Roll Over Function Parameters
        
        rm_ro               =       'rm_ro'
        Volatility          =       'Volatility - Moneyness/TermSPEC : Function Parameters'
        ATTRIBUTE           =       'Function Parameters'
        OBJECT              =       'Volatility - Moneyness/TermSPEC'
        
        FunctionParamsVAL   =       ''
        if FunctionParamsVAL != '':
            outfile.write('%s,%s,%s,%s,%s\n'%(rm_ro, Volatility, ATTRIBUTE, OBJECT, FunctionParamsVAL))
        
        # Roll Over  Procedure Parameter
        
        rm_ro               =       'rm_ro'
        Volatility          =       'Volatility - Moneyness/TermSPEC : Procedure Parameter'
        ATTRIBUTE           =       'Procedure Parameter'
        OBJECT              =       'Volatility - Moneyness/TermSPEC'
        
        ProcedureParamXREF  =       ''
        if ProcedureParamXREF != '':
            outfile.write('%s,%s,%s,%s,%s\n'%(rm_ro, Volatility, ATTRIBUTE, OBJECT, ProcedureParamXREF))
        
        outfile.close()
        
    return str(v.seqnbr)

# WRITE - FILE ######################################################################################################
