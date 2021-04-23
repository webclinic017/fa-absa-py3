'''
Purpose                 :Market Risk feed files
Department and Desk     :IT
Requester:              :Natalie Austin
Developer               :Douglas Finkel / Henk Nel
CR Number               :264536,278978,290307
2015/11/25              : Brendan Bosman - MINT 412, MINT 416, MINT 417
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


def calculate_string(l,FileDir,Filename,PositionName,comp,Vol_Name,*rest):
    filename    =       FileDir + Filename
    ins = acm.FInstrument[l.insaddr.insaddr]
    inscurve = acm.FInstrument[l.float_rate.insaddr]
    context = acm.GetDefaultContext()

    some_string_value = 'SCI_' + str(l.float_rate.insid) \
                        + '_' + str(getattr(l, 'reset_type')) \
                        + '_' + str(getattr(l, 'reset_period.count')) + str(getattr(l, 'reset_period.unit')) \
                        + '_' + str(l.reset_day_offset) + str(l.reset_day_method)+comp

    return some_string_value

# WRITE - FILE ######################################################################################################
def Write(l,FileDir,Filename,PositionName,Vol_Name,*rest):

    filename    =       FileDir + Filename
    ins = acm.FInstrument[l.insaddr.insaddr]
    inscurve = acm.FInstrument[l.float_rate.insaddr]
    context = acm.GetDefaultContext()
    cfspread   = getattr(l, 'spread')
    rtype = getattr(l, 'reset_type')
    lrp = getattr(l, 'reset_period')
    comp = str(MR_MainFunctions.CompoundConvention(cfspread, rtype, lrp))

    calculated_string = calculate_string(l, FileDir, Filename, PositionName, comp, Vol_Name, *rest)

    if (calculated_string) not in InsL:
        InsL.append(calculated_string)

        outfile = open(filename, 'a')
	#Base record

        BAS                     =       'BAS'
        Volatility              =       'Structured Curve Index'
        OBJECT                  =       'Structured Curve IndexSPEC'
        TYPE                    =       'Structured Curve Index'
        IDENTIFIER              =       calculated_string
        NAME                    =       calculated_string[0:50]

        FactorCAL               =       ''
        FactorDAYC              =       ''
        FactorFUNC              =       ''
        FactorPERD              =       ''
        FactorUNIT              =       ''
        FactorVAL               =       '1'
        FactorSTRG              =       ''
        CouponGenENUM           =       'Backward'
        try:
            DiscountCurveXREF   =       inscurve.MappedDiscountLink().Value().Link().YieldCurveComponent().Curve().Name()
        except:
            DiscountCurveXREF   =       inscurve.MappedDiscountLink().Value().Link().YieldCurveComponent().Name()
        FixedCouponDateNB       =       ''
        HistoricalCrvXREF       =       str(l.float_rate.insid)+'_HistoricalCurve'
        ResetRuleCAL            =       'Standard'

        Days                    =       int(getattr(l, 'reset_day_offset'))
        ResetRuleBUSD           =       0

        if Days < 0:

            if getattr(l, 'reset_day_method') in ('Mod. Following', 'IMM', 'Mod. Preceding', 'Following'):
                ResetRuleRULE   = 'Preceding'
            else:
                ResetRuleRULE = getattr(l, 'reset_day_method')

        elif Days >= 0:
            if getattr(l, 'reset_day_method') in ('Mod. Following', 'IMM'):
                ResetRuleRULE   = 'Following'
            elif getattr(l, 'reset_day_method') in ('Mod. Preceding'):
                ResetRuleRULE   = 'Preceding'
            # To cater for EOM reset_day_method
            elif l.reset_day_method in ('EOM'):  
                ResetRuleRULE   = 'End Month' 
            else:
                ResetRuleRULE = getattr(l, 'reset_day_method')

        ResetRuleBUSD   = abs(Days)

        if getattr(l, 'reset_day_method') in ('Following', 'Preceding'):
            ResetRuleCONV   = 'Regular'
        else:
            ResetRuleCONV   = 'Modified'

        if getattr(l, 'reset_type') in ('Compound', 'Weighted 1m Compound'):
            RateCompositnFUNC   = '@capitalize'
        elif getattr(l, 'reset_type') == 'Flat Compound':
            RateCompositnFUNC   = '@capitalize flat'
        elif getattr(l, 'reset_type') in ('Unweighted', 'Weighted'):
            RateCompositnFUNC   = '@average rates'
        else:
            RateCompositnFUNC   = ''

        SlidingTermNB           =       ''

        if getattr(l, 'reset_type') == 'Single':
            SlidingTermUNIT         =       ''
        else:
            SlidingTermUNIT         =       'Maturity'

        TermCAL                 =       ''

        if getattr(l, 'reset_type') == 'Single':
            TermNB         =       ''
        else:
            TermNB         =       str(getattr(l, 'reset_period.count'))

        if getattr(l, 'reset_type') == 'Single':
            TermUNIT         =       'Maturity'
        else:
            TermUNIT         =       str(getattr(l, 'reset_period.unit'))

        UnitCAL                 =       '%'

        # Get the daycount methd off the instruments leg
        for InsLegs in ael.Instrument[l.float_rate.insid].legs():
            UnitDAYC            =       MR_MainFunctions.DayCountFix(InsLegs.daycount_method)

        if comp == '':
            UnitPERD                =       'simple'
        else:
            UnitPERD                =   MR_MainFunctions.DatePeriodUnit(getattr(l, 'reset_period'), 0)
        UnitUNIT                =       ''

        if getattr(l, 'reset_type') not in ('Single'):
            UndrCurveIndsXREF       =       'CI_' + str(l.float_rate.insid) + '_'+str(getattr(l, 'reset_period.count')) + str(getattr(l, 'reset_period.unit'))
        else:
            UndrCurveIndsXREF       =       'CI_' + str(l.float_rate.insid) + '_Maturity'

        if str(Vol_Name) not in (''):
            IndxModelFUNC           =       '@Black for caps'
        else:
            IndxModelFUNC           =       ''

        VolSurfaceXREF          =       Vol_Name
        # To set ZeroFloor default = 'False'
        ZeroFloorFLAG = 'False'

        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%   
                    (BAS, Volatility, OBJECT, TYPE, IDENTIFIER, NAME,      
                    FactorCAL, FactorDAYC, FactorFUNC,    
                    FactorPERD, FactorUNIT, FactorVAL, FactorSTRG,                      
                    CouponGenENUM, DiscountCurveXREF, FixedCouponDateNB,                       
                    HistoricalCrvXREF, ResetRuleCAL, ResetRuleRULE,   
                    ResetRuleBUSD, ResetRuleCONV, RateCompositnFUNC,    
                    SlidingTermNB, SlidingTermUNIT, TermCAL, TermNB,   
                    TermUNIT, UnitCAL, UnitDAYC, UnitPERD, UnitUNIT,                       
                    UndrCurveIndsXREF, IndxModelFUNC, VolSurfaceXREF, ZeroFloorFLAG))
        outfile.close()

    return str(l.legnbr)

# WRITE - FILE ######################################################################################################



