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
        
        #Base record
        BAS	                =       'BAS'
        Exchange_RateSPEC       =	'Volatility - Term/TermSPEC'
        OBJECT                  =       'Volatility - Term/TermSPEC'
        TYPE                    =       'Volatility - Term/Term'
        IDENTIFIER	        =       v.vol_name + '_TT'
        
        NAME                    =       v.vol_name + '_TT'
        
        ActiveFLAG              =       'TRUE'
        
        CurveUnitCAL	        =       ''        
        CurveUnitDAYC           =       MR_MainFunctions.DayCountFix('Act/365')        
        CurveUnitPERD           =       'annual'	
        CurveUnitUNIT	        =       '%'
        
        DatumDATE	        =       MR_MainFunctions.Datefix(acm.Time().DateNow())
        OriginOffsetNB	        =       '0'
        
        RelativeCurveFLAG	=       'TRUE'        
        StateProcFUNC           =       ''        
        TimeEvolutionFUNC	=       '@Constant'        
        FunctionIdFLAG	        =       'TRUE'     
   
        GenVolSTSfExt0FLAG	=       'FALSE'
        GenVolSTSfExt1FLAG	=       'FALSE'
        GenVolStrTrmSf0SIN      =       '@Linear'
        GenVolStrTrmSf1SIN  	=       '@Linear'
        
        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BAS, Exchange_RateSPEC, OBJECT, TYPE, IDENTIFIER, NAME, ActiveFLAG, CurveUnitCAL, CurveUnitDAYC, CurveUnitPERD, CurveUnitUNIT, DatumDATE, OriginOffsetNB, RelativeCurveFLAG, StateProcFUNC, TimeEvolutionFUNC, FunctionIdFLAG, GenVolSTSfExt0FLAG, GenVolSTSfExt1FLAG, GenVolStrTrmSf0SIN, GenVolStrTrmSf1SIN))
        
        # Roll Over Function Parameters
        # Roll Over Generic Volatility Term Term Surface
        BASFLAG                 =       'rm_ro'
        Volatility              =       'Volatility - Term/TermSPEC : Generic Volatility Term Term Surface'
        ATTRIBUTE               =       'Generic Volatility Term Term Surface'
        OBJECT                  =       'Volatility - Term/TermSPEC'

        GnVolMnyTrmSf0AXS       =       '' 
        GnVolMnyTrmSf1AXS       =       '' 
        GnVolMnyTrmSfNODE       =       '' 

        for points in v.points():
            if points.insaddr:
             
                GnVolMnyTrmSf0AXS   =       ael.date_today().days_between(vol_bm_mat(points.insaddr))
                GnVolMnyTrmSf1AXS   =       ael.date_today().days_between(vol_bm_exp(points.insaddr))
                GnVolMnyTrmSfNODE   =       v.vol_get(0.0, vol_bm_exp(points.insaddr), vol_bm_mat(points.insaddr), 1)

            else:

                GnVolMnyTrmSf0AXS   =       MR_MainFunctions.CurveDays(points.undmat_period)
                GnVolMnyTrmSf1AXS   =       MR_MainFunctions.CurveDays(points.exp_period)
                GnVolMnyTrmSfNODE   =       points.volatility
                
            outfile.write('%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, Volatility, ATTRIBUTE, OBJECT, GnVolMnyTrmSf0AXS, GnVolMnyTrmSf1AXS, GnVolMnyTrmSfNODE))

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
        ProcedureParamXREF      =       ''
        if ProcedureParamXREF != '':
            outfile.write('%s,%s,%s,%s,%s\n'%(BASFLAG, Volatility, ATTRIBUTE, OBJECT, ProcedureParamXREF))
            
        outfile.close()
        
    return 'Success'
    
# WRITE - FILE ######################################################################################################

#OpenFile('1','c:\\','FileName.csv')
#Write(ael.Volatility['EUR/NLD/FloorSurface'],'c:\\','FileName.csv')

