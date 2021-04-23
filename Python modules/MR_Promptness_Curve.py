'''
Purpose                 :Market Risk feed files
Department and Desk     :IT
Requester:              :Natalie Austin
Developer               :Douglas Finkel
CR Number               :686048

Description             :Added string "nan" for exception handling
'''

import ael, string, acm, PositionFile, MR_MainFunctions
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
        outfile = open(filename, 'a')
        
        #Base record
        BASFLAG             =       'BAS'
        HeaderName          =       'Prompt Curve'
        OBJECT              =       'Prompt CurveSPEC'
        TYPE                =       'Prompt Curve'
        IDENTIFIER          =       yc.yield_curve_name + '_PromptCurve'
        NAME                =       yc.yield_curve_name + '_PromptCurve'
        
        CurveUnitDAYC       =       ''
        CurveUnitPERD       =       ''
        CurveUnitUNIT       =       yc.curr.insid
        
        DatumDATE           =       0
        RelativeCurveFLAG   =       'False'
        
        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, IDENTIFIER, NAME, CurveUnitDAYC, CurveUnitPERD, CurveUnitUNIT, DatumDATE, RelativeCurveFLAG))
        
        # Calculating points in the forward curves and storing the number of points in a list
        PromptSurf0AXS       =       '' 
        PromptSurfNODE       =       '' 
        
        PromptnessList  = []
        Count = 0
        cs = acm.Calculations().CreateStandardCalculationsSpaceCollection()
        
        for benchmarks in yc.benchmarks():
            ins = acm.FInstrument[benchmarks.instrument.insid]
            
            if ins.ExpiryDate():
                days_to_expiry = ael.date_today().days_between(ael.date(ins.ExpiryDateOnly()))
            elif ins.ExpiryPeriod():
                days_to_expiry = MR_MainFunctions.CurveDays(ins.ExpiryPeriod())
            else:
                days_to_expiry = ''
            
            PromptSurf0AXS   =       days_to_expiry

            calc = ins.Calculation()
            TheoPrice = calc.TheoreticalPrice(cs)
            
            '''Changed by Douglas Finkel - 27 October 2010'''
            '''From Price of the Instrument to Theoretical Price on Instrument'''

            if ins.MtmFromFeed():
                if str(ins.SLPrice()) in ('1.#QNAN', 'NaN', 'nan'):
                    PromptSurfNODE = ''
                else:
                    PromptSurfNODE = ins.SLPrice()

            else:
                try:
                    if str(TheoPrice.Number()) in ('1.#QNAN', 'NaN', 'nan'):
                        PromptSurfNODE   =       ''
                    else:
                        PromptSurfNODE   =       TheoPrice.Number()
                except:
                    PromptSurfNODE     =   ''
           
            '''
            if str(ins.SLPrice()) in ('1.#QNAN','NaN','nan'):
                PromptSurfNODE   =    ''
            else:
                PromptSurfNODE   =       ins.SLPrice()
            '''
            if PromptSurfNODE   !=    '':
                Count = Count + 1
                PromptnessList.append(Count)
        
        # Roll Over Generic Prompt Surface
        BASFLAG                 =       'rm_ro'
        Volatility              =       'Prompt Curve : Prompt Surface'
        ATTRIBUTE               =       'Prompt Surface'
        OBJECT                  =       'Prompt CurveSPEC'
        
        for TermPoints in PromptnessList:
            
            PromptSurf0AXS       =       TermPoints
            PromptSurfNODE       =       '1'
            
            outfile.write('%s,%s,%s,%s,%s,%s\n'%(BASFLAG, Volatility, ATTRIBUTE, OBJECT, PromptSurf0AXS, PromptSurfNODE))
            
        outfile.close()

    return yc.yield_curve_name

# WRITE - FILE ######################################################################################################
