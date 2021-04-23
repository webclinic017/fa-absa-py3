'''
Purpose                 :Market Risk feed files
Department and Desk     :IT
Requester:              :Natalie Austin
Developer               :Douglas Finkel / Henk Nel
CR Number               :264536
'''

import ael, string, acm, MR_MainFunctions

InsL = []
CInsL = []

# OPENFILE ##########################################################################################################
    
def OpenFile(temp,FileDir,Filename,*rest):

    filename            = FileDir + Filename

    outfile             =  open(filename, 'w')

    outfile.close()
    
    del InsL[:]
    InsL[:] = []
    
    del CInsL[:]
    CInsL[:] = []

    return filename

# OPENFILE ##########################################################################################################



# WRITE - FILE ######################################################################################################

def Write(v,FileDir,Filename,*rest):
    
    filename = FileDir + Filename

    if (v.seqnbr) not in InsL:
        InsL.append(v.seqnbr)
        outfile = open(filename, 'a')
        
        for inspoints in v.points():
            if (inspoints.insaddr.und_insaddr.insaddr) not in CInsL:
                CInsL.append(inspoints.insaddr.und_insaddr.insaddr)
                
                #Base record
                BAS	            =   'BAS'
                Exchange_RateSPEC   =	'Volatility - Strike/TermSPEC'
                OBJECT              =   'Volatility - Strike/TermSPEC'
                TYPE                =   'Volatility - Strike/Term'
                IDENTIFIER	    =   v.vol_name + '_' + inspoints.insaddr.und_insaddr.insid
                
                NAME                =   v.vol_name + '_' + inspoints.insaddr.und_insaddr.insid
                
                ActiveFLAG          =   'TRUE'
                CurveUnitCAL        =   ''
                
                CurveUnitDAYC       =   MR_MainFunctions.DayCountFix('Act/365')
                
                CurveUnitPERD       =   'annual' #MR_MainFunctions.BusRule(yc.storage_rate_type)
                CurveUnitUNIT       =   '%'
                
                DatumDATE           =   MR_MainFunctions.Datefix(acm.Time().DateNow())
                OriginOffsetNB      =   '0'
                
                RelativeCurveFLAG   =   'TRUE'
                StateProcFUNC       =   ''
                TimeEvolutionFUNC   =   '@Constant'
                FunctionIdFLAG      =   'TRUE'
                
                GenVolSTSfExt0FLAG  =   'FALSE'
                GenVolSTSfExt1FLAG  =   'FALSE'
                GenVolStrTrmSf0SIN  =   '@Linear'
                GenVolStrTrmSf1SIN  =   '@Linear'
                
                outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BAS, Exchange_RateSPEC, OBJECT, TYPE, IDENTIFIER, NAME, ActiveFLAG, CurveUnitCAL, CurveUnitDAYC, CurveUnitPERD, CurveUnitUNIT, DatumDATE, OriginOffsetNB, RelativeCurveFLAG, StateProcFUNC, TimeEvolutionFUNC, FunctionIdFLAG, GenVolSTSfExt0FLAG, GenVolSTSfExt1FLAG, GenVolStrTrmSf0SIN, GenVolStrTrmSf1SIN))
                
                # Roll Over Function Parameters
                # Roll Over Generic Volatility Moneyness Term Surface
                
                BASFLAG                 =       'rm_ro'
                Volatility              =       'Volatility - Strike/TermSPEC : Generic Volatility Strike Term Surface'
                ATTRIBUTE               =       'Generic Volatility Strike Term Surface'
                OBJECT                  =       'Volatility - Strike/TermSPEC'
                
                GnVolMnyTrmSf0AXS       =       ''
                GnVolMnyTrmSf1AXS       =       ''
                GnVolMnyTrmSfNODE       =       ''
                
                for points in v.points():
                    if inspoints.insaddr.und_insaddr.insaddr == points.insaddr.und_insaddr.insaddr:
                        
                        GnVolMnyTrmSf0AXS   =       points.insaddr.strike_price/100
                        GnVolMnyTrmSf1AXS   =       MR_MainFunctions.CurveDays(points.insaddr.exp_period)
                        GnVolMnyTrmSfNODE   =       points.volatility
                        
                        outfile.write('%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, Volatility, ATTRIBUTE, OBJECT, GnVolMnyTrmSf0AXS, GnVolMnyTrmSf1AXS, GnVolMnyTrmSfNODE))
                
                # Roll Over Function Parameters
                BASFLAG                 =       'rm_ro'
                Volatility              =       'Volatility - Strike/TermSPEC : Function Parameters'
                ATTRIBUTE               =       'Function Parameters'
                OBJECT                  =       'Volatility - Strike/TermSPEC'
                FunctionParamsVAL       =       ''
                if FunctionParamsVAL   != '':
                    outfile.write('%s,%s,%s,%s,%s\n'%(BASFLAG, Volatility, ATTRIBUTE, OBJECT, FunctionParamsVAL))
                
                # Roll Over  Procedure Parameter
                BASFLAG                 =       'rm_ro'
                Volatility              =       'Volatility - Strike/TermSPEC : Procedure Parameter'
                ATTRIBUTE               =       'Procedure Parameter'
                OBJECT                  =       'Volatility - Strike/TermSPEC'
                ProcedureParamXREF      =       ''
                if ProcedureParamXREF  != '':
                    outfile.write('%s,%s,%s,%s,%s\n'%(BASFLAG, Volatility, ATTRIBUTE, OBJECT, ProcedureParamXREF))
        outfile.close()
        
    return str(v.seqnbr)
    
# WRITE - FILE ######################################################################################################

