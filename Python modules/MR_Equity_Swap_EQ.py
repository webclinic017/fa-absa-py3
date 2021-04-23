'''
Purpose                 :[Market Risk feed files],[Removed check as described by change 573640],[ValNotional changed to positive for certain instruments]
Department and Desk     :[IT],[Market Risk],[Market Risk]
Requester:              :[Natalie Austin],[Susan Kruger],[Susan Kruger]
Developer               :[Douglas Finkel],[Willie van der Bank],[Bhavnisha Sarawan][Kevin Kistan]
CR Number               :[264536,573640],[749647],[C147729],[2418286]
'''


import ael, string, acm, PositionFile, MR_MainFunctions, datetime
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

def Write(i,FileDir,Filename,PositionName,*rest):
    
    filename            = FileDir + Filename

    ins = acm.FInstrument[i.insaddr]
    context = acm.GetDefaultContext()
    if ins.IndexReference():
        quotation_factor = 1 / ins.IndexReference().Quotation().QuotationFactor()
    else:
        quotation_factor = 1 / ins.Quotation().QuotationFactor()
    
    for l in i.legs():
        leg = acm.FInstrument[l.legnbr]
        if l.type == 'Total Return':
            if (str(i.insaddr) + '_' + str(l.legnbr)) not in InsL:
                InsL.append(str(i.insaddr) + '_' + str(l.legnbr))
                
                outfile = open(filename, 'a')
                
                #Base record
                BASFLAG             =       'BAS'
                HeaderName          =       'Equity Swap EQ Leg'
                OBJECT              =       'Swap Pre-determined LegSPEC'
                TYPE                =       'Swap Pre-determined Leg'            
                NAME                =       MR_MainFunctions.NameFix(i.insid)[0:46] + '_EQ'                
                IDENTIFIER          =       'insaddr_'+str(i.insaddr)+'_'+str(l.legnbr)                
                CurrencyCAL         =       ''
                CurrencyDAYC        =       ''
                CurrencyPERD        =       ''
                CurrencyUNIT        =       l.curr.insid  
                EffectiveDATE       =       MR_MainFunctions.Datefix(l.start_day)              
                NotionlAtStartFLAG  =       ''       
                NotionalAtEndFLAG   =       ''                
                CouponRateCAL       =       ''
                CouponRateDAYC      =       ''
                CouponRatePERD      =       ''
                CouponRateVAL       =       ''
                CalendarAdjFLAG     =       ''                
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
                if l.index_ref.instype == 'Stock':
                    InitialIndxLvlFUNC = ''
                else:
                    InitialIndxLvlFUNC  =       '@issue date level' 		 
                InitialIndxLvlUNIT  =       ''
                if l.initial_index_value == 0:
                    InitialIndxLvlVAL  = 0
                    for leg in i.legs():
                        if (l.legnbr != leg.legnbr):
                            if leg.initial_index_value != 0:
                                InitialIndxLvlVAL  = (1/leg.initial_index_value)/quotation_factor
                            else:
                                InitialIndxLvlVAL  = 0
			else:
		            InitialIndxLvlVAL  = 0
                else:
                    InitialIndxLvlVAL  = l.initial_index_value/quotation_factor                
                InitialIndxLvlSTRG  =       ''
                PaymntProcXREF      =       str(ins.IndexReference().Name())+'_PP'            
                try:
                    UndrCrvIndXREF      =       str(l.index_ref.insid)+'_NI'
                except:
                    UndrCrvIndXREF      =       ''                    
                try:
                    DiscountCurveXREF   =       ins.MappedDiscountLink().Value().Link().YieldCurveComponent().Curve().Name()
                except:
                    DiscountCurveXREF   =       ins.MappedDiscountLink().Value().Link().YieldCurveComponent().Name()                
                CouponProratedFLAG  =       ''
                TheoModelXREF       =       'Swap Pre-determined Leg(Cashflows)'
                MarketModelXREF     =       ''
                FairValueModelXREF  =       ''
                SettlementProcFUNC  =       '' 
                outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, NAME, IDENTIFIER, CurrencyCAL, CurrencyDAYC, CurrencyPERD, CurrencyUNIT, EffectiveDATE, NotionlAtStartFLAG, NotionalAtEndFLAG, CouponRateCAL, CouponRateDAYC, CouponRatePERD, CouponRateVAL, CalendarAdjFLAG, StateProcFUNC, TermNB, TermUNIT, TermCAL, CouponGenENUM, FixedCouponDateNB, BusDayRuleRULE, BusDayRuleBUSD, BusDayRuleCONV, BusDayRuleCAL, InitialIndxLvlFUNC, InitialIndxLvlUNIT, InitialIndxLvlVAL, InitialIndxLvlSTRG, PaymntProcXREF, UndrCrvIndXREF, DiscountCurveXREF, CouponProratedFLAG, TheoModelXREF, MarketModelXREF, FairValueModelXREF, SettlementProcFUNC))
                
                # Roll Over Equity Swap EQ Leg            
                BASFLAG             =       'rm_ro'
                HeaderName          =       'Equity Swap EQ Leg : Variable Notional'
                ATTRIBUTE           =       'Variable Notional'
                OBJECT              =       'Swap Pre-determined LegSPEC'                
                for cf in l.cash_flows():
                    if cf.pay_day > ael.date_today():
                        
                        VariabNotionalDATE  =       MR_MainFunctions.Datefix(cf.pay_day)
                        VariabNotionalENUM  =       ''
                        VariabNotionalCAL   =       ''
                        VariabNotionalDAYC  =       ''
                        VariabNotionalPERD  =       ''
                        VariabNotionalUNIT  =       i.curr.insid                        
                        CashFlow = acm.FCashFlow[cf.cfwnbr]
                        calcSpace = acm.Calculations().CreateStandardCalculationsSpaceCollection()
                        if l.index_ref:
                            if l.index_ref.instype in ('Bond', 'IndexLinkedBond', 'PriceIndex'):
                                VariabNotionalVAL = abs(cf.nominal_amount())
                            elif l.index_ref.instype in ('Stock', 'EquityIndex'): 
                                VariabNotionalVAL = (cf.nominal_amount() / CashFlow.Calculation().NominalFactor(calcSpace))*l.initial_index_value / quotation_factor
                            elif l.index_ref.instype in  ('ETF'):
                                VariabNotionalVAL = l.initial_index_value
                            else:
                                VariabNotionalVAL = (cf.nominal_amount() / CashFlow.Calculation().NominalFactor(calcSpace))*l.initial_index_value
                        else:
                            VariabNotionalVAL = cf.nominal_amount()
 
                        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, VariabNotionalDATE, VariabNotionalENUM, VariabNotionalCAL, VariabNotionalDAYC, VariabNotionalPERD, VariabNotionalUNIT, VariabNotionalVAL))
                
                outfile.close()

    return i.insid
# WRITE - FILE ######################################################################################################
