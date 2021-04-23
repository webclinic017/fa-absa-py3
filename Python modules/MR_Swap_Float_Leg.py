'''
Purpose                 :[Market Risk feed files],[Removed check as described by change 573640], [ValNotional changed to positive for certain instruments.]
Department and Desk     :[IT],[Market Risk],[Market Risk]
Requester:              :[Natalie Austin],[Susan Kruger],[Susan Kruger]
Developer               :[Douglas Finkel],[Willie van der Bank],[Bhavnisha Sarawan]
CR Number               :[264536,421147,573640],[749647],[C147729]
'''




import ael, string, acm, PositionFile, MR_MainFunctions, datetime

InsL = []
cs = acm.Calculations().CreateStandardCalculationsSpaceCollection()

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

def Write(i,FileDir,Filename,PositionName,*rest):
    
    filename            = FileDir + Filename

    outfile = open(filename, 'a')
        
    ins = acm.FInstrument[i.insaddr]
    context = acm.GetDefaultContext()
    
    Legs = i.legs()
    for l in Legs:        
        if l.type == 'Float':
            if (str(i.insaddr) + '_' + str(l.legnbr)) not in InsL:
                InsL.append(str(i.insaddr) + '_' + str(l.legnbr))
                leg = acm.FInstrument[l.legnbr]
     
                #Base record
        
                BASFLAG             =       'BAS'
                HeaderName          =       'Swap Float Leg'
                OBJECT              =       'Swap Pre-determined LegSPEC'
                TYPE                =       'Swap Pre-determined Leg'
                
                NAME                =       MR_MainFunctions.NameFix(i.insid)+'_Float'
                IDENTIFIER          =       'insaddr_'+str(i.insaddr) + '_' + str(l.legnbr)

                CurrencyCAL         =       ''
                CurrencyDAYC        =       ''
                CurrencyPERD        =       ''
                CurrencyUNIT        =       l.curr.insid

                NotionlAtStartFLAG  =       ''
                NotionalAtEndFLAG   =       ''

                #EffectiveDATE       =        ael.date_today()
                #for l in i.legs():
                #        if l.start_day <= EffectiveDATE:
                #                EffectiveDATE = l.start_day
                #EffectiveDATE       =	    MR_MainFunctions.Datefix(EffectiveDATE)
                
                # 573640 - Douglas Finkel - Updated to check that leg start day matches todays date and sets it to yesterdays date
                
                #CurrDayDate = datetime.date.today()
                #CurrDay = MR_MainFunctions.Datefix(str(CurrDayDate))
                #
                #if CurrDay == MR_MainFunctions.Datefix(l.start_day):
                #    PrevDayDate = CurrDayDate + datetime.timedelta(days=(-1))
                #    PrevDay = MR_MainFunctions.Datefix(str(PrevDayDate))
                #    EffectiveDATE       = PrevDay
                #else:
                EffectiveDATE       = MR_MainFunctions.Datefix(l.start_day)
                
                SpreadCAL           =       ''
                SpreadDAYC          =       ''
                SpreadDAYC          =       MR_MainFunctions.DayCountFix(l.daycount_method)
                SpreadFUNC          =       ''
                SpreadPERD          =       'simple'
                SpreadUNIT          =       '%'
                SpreadVAL           =       l.spread
                SpreadSTRG          =       ''

                CouponRateCAL       =       ''
                CouponRateDAYC      =       ''
                CouponRateDAYC      =       MR_MainFunctions.DayCountFix(l.daycount_method)
                CouponRatePERD      =       'simple'
                CouponRateVAL       =       '0'
                
                StateProcFUNC       =       '@cash flow generator'
                
                if l.rolling_period not in ('0d', '0m', '0y'):
                    TermNB = getattr(l, 'rolling_period.count')
                    TermUNIT = getattr(l, 'rolling_period.unit')
                else:
                    TermNB = ''
                    TermUNIT = 'Maturity'
                
                TermCAL             =       ''
                
                CouponGenENUM       =       ''
                FixedCouponDateNB   =       ''
                BusDayRuleRULE      =       ''
                BusDayRuleBUSD      =       ''
                BusDayRuleCONV      =       ''
                BusDayRuleCAL       =       ''
                
                InitialIndxLvlFUNC      =       ''
                InitialIndxLvlUNIT      =       ''
                InitialIndxLvlVAL       =       ''
                InitialIndxLvlSTRG      =       ''
                PaymntProcXREF          =       ''
                
                # 573640 - Douglas Finkel - Removed PaymntProcXREF logic
                '''
                if l.nominal_scaling:
                    if (l.index_ref):
                        if l.index_ref.instype in ('EquityIndex','Stock'):
                            InitialIndxLvlFUNC  =       '@issue date level'
                    if ins.IndexReference():
                        PaymntProcXREF      =       str(ins.IndexReference().Name()) + '_PP'
                    else:
                        PaymntProcXREF      =       ''
                else:
                    InitialIndxLvlFUNC  =       ''
                    PaymntProcXREF      =       ''
                '''
                
                try:
                    cashflow = acm.FCashFlow.Select01("leg = '%s' and startDate <= '%s' and endDate >= '%s'" % (leg.Oid(), acm.Time().TimeNow(), acm.Time().TimeNow()), '')
                    calc = cashflow.Calculation()
                    LastResetRateVAL    =   (calc.ForwardRate(cs) * 100) - cashflow.Spread()
                except:
                    LastResetRateVAL    =       ''
                
                UndrCrvIndXREF      =       ''
                if i.instype == 'TotalReturnSwap':
                    if (l.float_rate):
                        UndrCrvIndXREF          =       'SCI_' + l.float_rate.insid + '_' + str(getattr(l, 'reset_type')) + '_' + str(getattr(l, 'reset_period.count')) + str(getattr(l, 'reset_period.unit')) + '_' + str(l.reset_day_offset) + str(l.reset_day_method)
                    else:
                        TRSi = ael.Instrument[l.insaddr.insaddr]
                        for TRSl in TRSi.legs():
                            if (TRSl.index_ref):
                                UndrCrvIndXREF  = MR_MainFunctions.NameFix(TRSl.index_ref.insid) + '_NI'
                                break
                else:
                    float_rate = getattr(l, 'float_rate')
                    if float_rate:
                        output = float_rate.insid
                        UndrCrvIndXREF          =       'SCI_' + output + '_' + str(getattr(l, 'reset_type')) + '_' + str(getattr(l, 'reset_period.count')) + str(getattr(l, 'reset_period.unit')) + '_' + str(l.reset_day_offset) + str(l.reset_day_method)
                    else:
                        UndrCrvIndXREF  = ''
                
                try:
                    DiscountCurveXREF   =       ins.MappedDiscountLink().Value().Link().YieldCurveComponent().Curve().Name()
                except:
                    DiscountCurveXREF   =       ins.MappedDiscountLink().Value().Link().YieldCurveComponent().Name()
                
                if l.initial_index_value == 0:
                    InitialIndxLvlVAL  = 0
                    for leg in i.legs():
                        if (l.legnbr != leg.legnbr):
                            if leg.initial_index_value != 0:
                                InitialIndxLvlVAL  = 1/leg.initial_index_value
                            else:
                                InitialIndxLvlVAL  = 0
                else:
                    InitialIndxLvlVAL  = l.initial_index_value
                
                CouponProratedFLAG  =       ''
                CouponPrepayENUM    =       ''
                TheoModelXREF       =       'Swap Pre-determined Leg(Cashflows)'
                MarketModelXREF     =       ''
                FairValueModelXREF  =       ''
                SettlementProcFUNC  =       ''

                outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, NAME, IDENTIFIER, CurrencyCAL, CurrencyDAYC, CurrencyPERD, CurrencyUNIT, NotionlAtStartFLAG, NotionalAtEndFLAG, EffectiveDATE, SpreadCAL, SpreadDAYC, SpreadFUNC, SpreadPERD, SpreadUNIT, SpreadVAL, SpreadSTRG, CouponRateCAL, CouponRateDAYC, CouponRatePERD, CouponRateVAL, StateProcFUNC, TermNB, TermUNIT, TermCAL, CouponGenENUM, FixedCouponDateNB, BusDayRuleRULE, BusDayRuleBUSD, BusDayRuleCONV, BusDayRuleCAL, LastResetRateVAL, InitialIndxLvlFUNC, InitialIndxLvlUNIT, InitialIndxLvlVAL, InitialIndxLvlSTRG, PaymntProcXREF, UndrCrvIndXREF, DiscountCurveXREF, CouponProratedFLAG, CouponPrepayENUM, TheoModelXREF, MarketModelXREF, FairValueModelXREF, SettlementProcFUNC))

                BASFLAG             =       'rm_ro'
                HeaderName          =       'Swap Float Leg : Variable Notional'
                ATTRIBUTE           =       'Variable Notional'
                OBJECT              =       'Swap Pre-determined LegSPEC'
                calcSpace = acm.Calculations().CreateStandardCalculationsSpaceCollection()
                
                for cf in l.cash_flows():
                    if cf.pay_day > ael.date_today():
                        VariabNotionalDATE  =       MR_MainFunctions.Datefix(cf.pay_day) 
                        VariabNotionalENUM  =       ''
                        VariabNotionalCAL   =       ''
                        VariabNotionalDAYC  =       ''
                        VariabNotionalPERD  =       ''
                        VariabNotionalUNIT  =       l.curr.insid

                        if i.instype == 'TotalReturnSwap':
                            if VariabNotionalDATE <= EffectiveDATE:
                                VariabNotionalDATE = ael.date(EffectiveDATE).add_days(1)
                                
                        
                            CashFlow = acm.FCashFlow[cf.cfwnbr]

                            NominalFactor = CashFlow.Calculation().NominalFactor(calcSpace)
                            if NominalFactor == 0:
                                NominalFactor = 1
                            
                            if l.initial_index_value == 0:
                                for leg in i.legs():
                                    if (l.legnbr != leg.legnbr):
                                        initialIndex  = leg.initial_index_value
                            else:
                                initialIndex = l.initial_index_value
                            
                            if l.index_ref:
                                if l.index_ref.instype in ('Bond', 'IndexLinkedBond', 'PriceIndex'):
                                    VariabNotionalVAL = abs(cf.nominal_amount())
                                elif l.index_ref and l.index_ref.quote_type == 'Per 100 Units':
                                    VariabNotionalVAL = ((cf.nominal_amount() / NominalFactor)*initialIndex) / 100
                                else:
                                    VariabNotionalVAL = ((cf.nominal_amount() / NominalFactor)*initialIndex)
                            else:
                                VariabNotionalVAL = cf.nominal_amount()
                        else:
                            VariabNotionalVAL = i.contr_size*cf.nominal_factor

                        '''
                        if l.initial_index_value == 0:
                            InitialIndexValue  = 0
                            for leg in i.legs():
                                if (l.legnbr != leg.legnbr):
                                    if leg.initial_index_value != 0:
                                        InitialIndexValue  = 1/leg.initial_index_value
                                    else:
                                        InitialIndexValue  = 0
                        else:
                            InitialIndexValue  = l.initial_index_value

                        if i.instype == 'TotalReturnSwap':
                            if VariabNotionalDATE <= EffectiveDATE:
                                VariabNotionalDATE = ael.date(EffectiveDATE).add_days(1)
                                
                            CashFlow = acm.FCashFlow[cf.cfwnbr]
                            if l.index_ref:
                                VariabNotionalVAL   = (cf.nominal_amount() / CashFlow.Calculation().NominalFactor(calcSpace).Number()*InitialIndexValue)
                            else:
                                if l.index_ref.quote_type == 'Per 100 Units':
                                    VariabNotionalVAL   = (cf.nominal_amount() / CashFlow.Calculation().NominalFactor(calcSpace).Number()*InitialIndexValue)/100
                                else:
                                    VariabNotionalVAL   = (cf.nominal_amount() / CashFlow.Calculation().NominalFactor(calcSpace).Number()*InitialIndexValue)
                        else:
                            VariabNotionalVAL =  i.contr_size*cf.nominal_factor
                        '''
                        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, VariabNotionalDATE, VariabNotionalENUM, VariabNotionalCAL, VariabNotionalDAYC, VariabNotionalPERD, VariabNotionalUNIT, VariabNotionalVAL))
    outfile.close()
    
    return i.insid

# WRITE - FILE ######################################################################################################

#MR_Equity_Swap_Float_Leg
#MR_IRS_FloatLeg
