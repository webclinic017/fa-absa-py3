'''
Change History:
Date          CR/JIRA Number     Developer         Description
2010/03/23    264536             Douglas Finkel    Original Implementation
              289168             Douglas Finkel    Code fixes
2018/07/25    ABITFA-5479        Lucky Lesese      Added Price link to link multiple versions of the same insuance.
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

def Write(i,FileDir,Filename,*rest):
    
    filename            = FileDir + Filename
    
    Instrument = acm.FInstrument[i.insaddr]    
    
    outfile = open(filename, 'a')
    
    # link prices to the underlying price link rather than individual instrument price if it exists
    RIC_Code = ''
    priceLinkDefList = acm.FPriceLinkDefinition.Select("instrument=" + i.insid)
    for pl in priceLinkDefList:
        if pl.PriceDistributor().Name() == "REUTERS_FEED":
            RIC_Code = pl.IdpCode()
            if RIC_Code != '':
                break   
    
    if RIC_Code == '':
        RIC_Code = i.insid
        
    
    Iden_Code = MR_MainFunctions.NameFix(RIC_Code)
    
    # scale the price by the quotation factor to ensure we have the correct scale.
    try:
        if i.quote_type == 'Per 100 Units':
            SpotPriceVAL_amnt        =       i.mtm_price(ael.date_today())/100
        else:
            SpotPriceVAL_amnt        =       i.mtm_price(ael.date_today())
    except:
        SpotPriceVAL_amnt        =       1      
                        
    #Base record
    
    BAS                   =       'BAS'
    Exchange_RateSPEC     =       'Index CurveSPEC'
    OBJECT                =       'Index CurveSPEC'
    TYPE                  =       'Index Curve'    
    
    ActiveFLAG            =       'TRUE'
    CurveFUNC             =       ''
    CurveUnitCAL          =       ''

    CurveUnitDAYC         =       MR_MainFunctions.DayCountFix('Act/365')
        
    CurveUnitPERD         =       'annual'
    CurveUnitUNIT         =       i.curr.insid
    
    DatumDATE             =       MR_MainFunctions.Datefix(acm.Time().DateNow())
    OriginOffsetNB        =       '0'
    
    RelativeCurveFLAG     =       'TRUE'
    StateProcFUNC         =       ''
    TimeEvolutionFUNC     =       '@Sliding Axis 2'
    FunctionIdFLAG        =       'TRUE'
    
    GenIndxSfExt0FLAG     =       'FALSE'
    GenIndxSfExt1FLAG     =       'FALSE'
    GenIndxSuf0SIN        =       '@Linear'
    GenIndxSuf1SIN        =       '@Linear'
    
    # Roll Over Generic Zero Surface

    BASFLAG                     =       'rm_ro'    
    GeneIndxSuf0AXS             =       '0'
    GeneIndxSuf1AXS             =       '0'      

    # Roll Over Function Parameters
            
    FunctionParamsVAL           =       ''
    
    # Roll Over Procedure Parameters
            
    ProcedureParamXREF          =           ''
    
    if i.instype in ('Stock'):
        if Iden_Code not in InsL:
            InsL.append(Iden_Code)
            
            #Base record
            
            IDENTIFIER            =       str(Iden_Code) + '_GrowthCurve'    
            NAME                  =       str(Iden_Code) + '_GrowthCurve'
            
            outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BAS, Exchange_RateSPEC, OBJECT, TYPE, IDENTIFIER, NAME, ActiveFLAG, CurveFUNC, CurveUnitCAL, CurveUnitDAYC, CurveUnitPERD, CurveUnitUNIT, DatumDATE, OriginOffsetNB, RelativeCurveFLAG, StateProcFUNC, TimeEvolutionFUNC, FunctionIdFLAG, GenIndxSfExt0FLAG, GenIndxSfExt1FLAG, GenIndxSuf0SIN, GenIndxSuf1SIN))
            
            # Roll Over Generic Zero Surface
            
            HeaderName                  =       'Index CurveSPEC : Generic Index Surface'
            ATTRIBUTE                   =       'Generic Index Surface'           
            GeneIndxSufNODE             =       str(SpotPriceVAL_amnt)
            
            outfile.write('%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, GeneIndxSuf0AXS, GeneIndxSuf1AXS, GeneIndxSufNODE))
            
            # Roll Over Function Parameters
            
            HeaderName                  =       'Index CurveSPEC : Function Parameters'
            ATTRIBUTE                   =       'Function Parameters'
                        
            if FunctionParamsVAL != '':
                outfile.write('%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, FunctionParamsVAL))
                
            # Roll Over Procedure Parameters
            
            HeaderName                  =       'Index CurveSPEC : Procedure Parameter'
            ATTRIBUTE                   =       'Procedure Parameter'

            if ProcedureParamXREF != '':
                outfile.write('%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, ProcedureParamXREF))
    else:
        if i.insid not in InsL:
            InsL.append(i.insid)
            
            #Base record
                        
            IDENTIFIER              =       str(MR_MainFunctions.NameFix(i.insid)) + '_GrowthCurve'            
            NAME                    =       str(MR_MainFunctions.NameFix(i.insid)) + '_GrowthCurve'
                        
            outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BAS, Exchange_RateSPEC, OBJECT, TYPE, IDENTIFIER, NAME, ActiveFLAG, CurveFUNC, CurveUnitCAL, CurveUnitDAYC, CurveUnitPERD, CurveUnitUNIT, DatumDATE, OriginOffsetNB, RelativeCurveFLAG, StateProcFUNC, TimeEvolutionFUNC, FunctionIdFLAG, GenIndxSfExt0FLAG, GenIndxSfExt1FLAG, GenIndxSuf0SIN, GenIndxSuf1SIN))
            
            # Roll Over Generic Zero Surface   
            
            HeaderName                  =       'Index CurveSPEC : Generic Index Surface'
            ATTRIBUTE                   =       'Generic Index Surface' 
            GeneIndxSufNODE             =       '1'               
             
            outfile.write('%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, GeneIndxSuf0AXS, GeneIndxSuf1AXS, GeneIndxSufNODE))
            
            # Roll Over Function Parameters
            
            HeaderName                  =       'Index CurveSPEC : Function Parameters'
            ATTRIBUTE                   =       'Function Parameters'
            
            if FunctionParamsVAL != '':
                outfile.write('%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, FunctionParamsVAL))
            
            # Roll Over Procedure Parameters
            
            HeaderName                  =       'Index CurveSPEC : Procedure Parameter'
            ATTRIBUTE                   =       'Procedure Parameter'
            
            if ProcedureParamXREF != '':
                outfile.write('%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, ProcedureParamXREF))
            
            # We want to create an additional entry using the Iden Code and the actual spot price
            if i.insid != Iden_Code:         
                if Iden_Code not in InsL:
                    InsL.append(Iden_Code)
                    
                    #Base record
                                        
                    IDENTIFIER              =       str(Iden_Code) + '_GrowthCurve'                    
                    NAME                    =       str(Iden_Code) + '_GrowthCurve'
                                                            
                    outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BAS, Exchange_RateSPEC, OBJECT, TYPE, IDENTIFIER, NAME, ActiveFLAG, CurveFUNC, CurveUnitCAL, CurveUnitDAYC, CurveUnitPERD, CurveUnitUNIT, DatumDATE, OriginOffsetNB, RelativeCurveFLAG, StateProcFUNC, TimeEvolutionFUNC, FunctionIdFLAG, GenIndxSfExt0FLAG, GenIndxSfExt1FLAG, GenIndxSuf0SIN, GenIndxSuf1SIN))
                    
                    # Roll Over Generic Zero Surface
                    
                    HeaderName                  =       'Index CurveSPEC : Generic Index Surface'
                    ATTRIBUTE                   =       'Generic Index Surface'                     
                    GeneIndxSufNODE             =       str(SpotPriceVAL_amnt)              
                      
                    outfile.write('%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, GeneIndxSuf0AXS, GeneIndxSuf1AXS, GeneIndxSufNODE))
                    
                    # Roll Over Function Parameters
                    
                    HeaderName                  =       'Index CurveSPEC : Function Parameters'
                    ATTRIBUTE                   =       'Function Parameters'
                    
                    if FunctionParamsVAL != '':
                        outfile.write('%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, FunctionParamsVAL))

                    # Roll Over Procedure Parameters
                    
                    HeaderName                  =       'Index CurveSPEC : Procedure Parameter'
                    ATTRIBUTE                   =       'Procedure Parameter'
                    
                    if ProcedureParamXREF != '':
                        outfile.write('%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, ProcedureParamXREF))
                                            
        outfile.close()

    return str(i.insid)

# WRITE - FILE ######################################################################################################

