'''
Purpose                 :Market Risk feed files
Department and Desk     :IT
Requester:              :Natalie Austin
Developer               :Douglas Finkel / Henk Nel
CR Number               :264536

'''

import ael, string, acm,  MR_MainFunctions

InsL = []

# OPENFILE ##########################################################################################################
def OpenFile(temp,FileDir,Filename,PositionName,*rest):

    filename            = FileDir + Filename
    outfile             =  open(filename, 'w')
    outfile.close()

    del InsL[:]
    InsL[:] = []
    
    return filename

# OPENFILE ##########################################################################################################



# WRITE - FILE ######################################################################################################
def Write(l,FileDir,Filename,PositionName,*rest):
    
    filename    =       FileDir + Filename
    
    ins = acm.FInstrument[l.insaddr.insaddr]
    inscurve = acm.FInstrument[l.float_rate.insaddr]
#    trade = acm.FTrade[t.trdnbr]
    context = acm.GetDefaultContext()
    
    if getattr(l, 'reset_type') not in ('Single'):
        LegList = 'CI_' + str(l.float_rate.insid) + '_'+ str(getattr(l, 'reset_period.count')) + str(getattr(l, 'reset_period.unit'))
    else:    
        LegList = 'CI_' + str(l.float_rate.insid) + '_Maturity'
    
    if (LegList) not in InsL:
        InsL.append(LegList)
        
        outfile = open(filename, 'a')
	#Base record
            
        BAS                         =       'BAS'
        Volatility                  =       'Curve Index'
        OBJECT                      =       'Curve IndexSPEC'
        TYPE                        =       'Curve Index'
        
        if getattr(l, 'reset_type') not in ('Single'):
            IDENTIFIER                      =       'CI_' + str(l.float_rate.insid) + '_'+ str(getattr(l, 'reset_period.count')) + str(getattr(l, 'reset_period.unit'))
        else:    
            IDENTIFIER                      =       'CI_' + str(l.float_rate.insid) + '_Maturity'
        if getattr(l, 'reset_type') not in ('Single'):
            NAME                            =       ('CI_' + str(l.float_rate.insid) + '_'+ str(getattr(l, 'reset_period.count')) + str(getattr(l, 'reset_period.unit')))[0:50]
        else:    
            NAME                            =       ('CI_' + str(l.float_rate.insid) + '_Maturity')[0:50]

        try:
            DiscountCurveXREF   =       inscurve.MappedDiscountLink().Value().Link().YieldCurveComponent().Curve().Name()
        except:
            DiscountCurveXREF   =       inscurve.MappedDiscountLink().Value().Link().YieldCurveComponent().Name()
            
        HistoricalCrvXREF           =       str(l.float_rate.insid)+'_HistoricalCurve'
        RuleAtEndBUSD               =       '0'
        RuleAtEndCAL                =       ''
        RuleAtEndCONV               =       'Regular'
        RuleAtEndRULE               =       'Following'
        RuleAtStartBUSD             =       '0'
        RuleAtStartCAL              =       ''
        RuleAtStartCONV             =       'Regular'
        RuleAtStartRULE             =       'Preceding'

        if str(getattr(l, 'reset_period.count'))+str(getattr(l, 'reset_period.unit')) == '0Days':
            TermNB                          =       ''
        elif getattr(l, 'reset_type') not in  'Single':
            TermNB                          =       ''
        else:
            TermNB                          =       str(getattr(l, 'reset_period.count'))

        if str(getattr(l, 'reset_period.count'))+str(getattr(l, 'reset_period.unit')) == '0Days':    
            TermUNIT                    =   'Maturity'
        elif getattr(l, 'reset_type') not in  'Single':
            TermUNIT                    =   'Maturity'
        else:
            TermUNIT                =       str(getattr(l, 'reset_period.unit'))
        UnitCAL                     =       ''
        
        # Get the daycount methd off the instruments leg
        for InsLegs in ael.Instrument[l.float_rate.insid].legs():
            UnitDAYC                =       MR_MainFunctions.DayCountFix(InsLegs.daycount_method)
            
        UnitPERD                    =       'simple'
        UnitUNIT                    =       '%'
        # To set ZeroFloor default to 'False'
        ZeroFloorFLAG = 'False'

        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%   
                    (BAS, Volatility, OBJECT,  
                    TYPE, IDENTIFIER, NAME,                     
                    DiscountCurveXREF, HistoricalCrvXREF,              
                    RuleAtEndBUSD, RuleAtEndCAL, RuleAtEndCONV,                  
                    RuleAtEndRULE, RuleAtStartBUSD, RuleAtStartCAL,                      
                    RuleAtStartCONV, RuleAtStartRULE, TermNB, TermUNIT,  
                    UnitCAL, UnitDAYC, UnitPERD, UnitUNIT, ZeroFloorFLAG))

        outfile.close()

    return l.insaddr.insid
    
# WRITE - FILE ######################################################################################################

