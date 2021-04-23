'''
Purpose                 :Market Risk feed files
Department and Desk     :IT
Requester:              :Natalie Austin
Developer               :Douglas Finkel / Henk Nel
CR Number               :264536

 -- HISTORY --
Date           CR               Requestor          Developer          Change
----------------------------------------------------------------------------------------
2016-01-20     CHNG0003404656   Ashley Canter      Chris Human        http://abcap-jira/browse/MINT-444
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

def Write(yc,FileDir,Filename,*rest):
    
    filename            = FileDir + Filename

    if (yc.seqnbr) not in InsL:
        InsL.append(yc.seqnbr)
        outfile = open(filename, 'a')
        
        for member in yc.attributes():

            #Base record
            
            BAS                 =       'BAS'
            ZeroSPEC            =       'ZeroSPEC'
            OBJECT              =       'ZeroSPEC'
            TYPE                =       'Zero'
            IDENTIFIER          =       MR_MainFunctions.NameFix(member.issuer_ptynbr.ptyid + '_' + yc.curr.insid + '_HazardCurve')
            NAME                =       MR_MainFunctions.NameFix(member.issuer_ptynbr.ptyid + '_' + yc.curr.insid + '_HC')
            
            ActiveFLAG          =       'TRUE'
            CreditStateENUM     =       ''
            CurveFUNC           =       ''
            CurveUnitCAL        =       ''
            
            CurveUnitDAYC           =       MR_MainFunctions.DayCountFix(yc.storage_daycount)
            
            CurveUnitPERD           = 'quarter'
            
            CurveUnitUNIT       =       '%'
            DatumDATE           =       MR_MainFunctions.Datefix(acm.Time().DateNow())
            OriginOffsetNB      =       '0'
            RelativeCurveFLAG   =       'TRUE'
            StateProcFUNC       =       '@hazard curve bootstrap (scenario)'
            TimeEvolutionFUNC   =       '@Constant'
            FunctionIdFLAG      =       'TRUE'
            GenZeroSfExt0FLAG   =       'FALSE'
            GenZeroSurface0SIN  =       '@Inverse Constant'
            
            outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BAS, ZeroSPEC, OBJECT, TYPE, IDENTIFIER, NAME, ActiveFLAG, CreditStateENUM, CurveFUNC, CurveUnitCAL, CurveUnitDAYC, CurveUnitPERD, CurveUnitUNIT, DatumDATE, OriginOffsetNB, RelativeCurveFLAG, StateProcFUNC, TimeEvolutionFUNC, FunctionIdFLAG, GenZeroSfExt0FLAG, GenZeroSurface0SIN))

            # Roll Over Function Parameters
            # Roll Over Generic Volatility Moneyness Term Surface
            BASFLAG                 =       'rm_ro'
            Volatility              =       'ZeroSPEC : Generic Zero Surface'
            ATTRIBUTE               =       'Generic Zero Surface'
            OBJECT                  =       'ZeroSPEC'
            
            GnVolMnyTrmSf0AXS       =       '' 
            GnVolMnyTrmSfNODE       =       '' 
            
#            for points in yc.points():
            
            GnVolMnyTrmSf0AXS   =       '' #MR_MainFunctions.Rolling_NameFix(points.date_period)
            GnVolMnyTrmSfNODE   =       '' #points.value
            
            if GnVolMnyTrmSfNODE != '':
                outfile.write('%s,%s,%s,%s,%s,%s\n'%(BASFLAG, Volatility, ATTRIBUTE, OBJECT, GnVolMnyTrmSf0AXS, GnVolMnyTrmSfNODE))

            for spreads in member.spreads():

                if spreads.point_seqnbr.date_period != '0d':
                
                    # Roll Over Function Parameters
                    BASFLAG                 =       'rm_ro'
                    Volatility              =       'ZeroSPEC : Function Parameters'
                    ATTRIBUTE               =       'Function Parameters'
                    OBJECT                  =       'ZeroSPEC'
                    FunctionParamsVAL       =       ''
                    
                    if FunctionParamsVAL != '':
                        outfile.write('%s,%s,%s,%s,%s\n'%(BASFLAG, Volatility, ATTRIBUTE, OBJECT, FunctionParamsVAL))
                    
                    # Roll Over  Procedure Parameter
                    BASFLAG                 =       'rm_ro'
                    Volatility              =       'ZeroSPEC : Procedure Parameter'
                    ATTRIBUTE               =       'Procedure Parameter'
                    OBJECT                  =       'ZeroSPEC'
                    
                    ProcedureParamXREF  =       member.issuer_ptynbr.ptyid + '_' + yc.curr.insid + '_CTDS_' + spreads.point_seqnbr.date_period
                    
                    outfile.write('%s,%s,%s,%s,%s\n'%(BASFLAG, Volatility, ATTRIBUTE, OBJECT, ProcedureParamXREF))
            
        outfile.close()

    return str(yc.seqnbr)
    
# WRITE - FILE ######################################################################################################
