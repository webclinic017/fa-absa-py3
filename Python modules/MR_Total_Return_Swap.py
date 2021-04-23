
"""
Purpose                 :[Market Risk feed files]
Department and Desk     :[IT],[MR]
Requester:              :[Natalie Austin]
Developer               :[Douglas Finkel]
CR Number               :[264536,489655]


 -- HISTORY --
Date           CR               Requestor                       Developer                  Change
----------------------------------------------------------------------------------------------------------------------------
2018-11-14     CHG1001129249    Dharshan Tathiah		Menzi Mndaweni  	   http://abcap-jira/browse/MRINFRA-8
* Change Description - Added the 'Return on Price' attribute, changed the 'Last Bond Price' and 'Variable Notionals' attribute *
2020-09-11     CHG0128302	Garth Saunders	                Heinrich Cronje            https://absa.atlassian.net/browse/CMRI-776

"""

import ael, string, acm, PositionFile, MR_MainFunctions

InsL = []


# OPENFILE ##########################################################################################################
    
def OpenFile(temp,FileDir,Filename,PositionName,*rest):

    filename            = FileDir + Filename
    PositionFilename    = FileDir + PositionName
    
    outfile             =  open(filename, 'w')
    outfileP            =  open(PositionFilename, 'w')
    
    outfile.close()
    outfileP.close()

    del InsL[:]
    InsL[:] = []

    return filename

# OPENFILE ##########################################################################################################



# WRITE - FILE ######################################################################################################

def Write(i,FileDir,Filename,PositionName,*rest):

    filename            = FileDir + Filename
    PositionFilename    = FileDir + PositionName

    ins = acm.FInstrument[i.insaddr]
    context = acm.GetDefaultContext()

    if (i.insaddr) not in InsL:
        InsL.append(i.insaddr)

        outfile = open(filename, 'a')

        #Base record
        BASFLAG = 'BAS'
        HeaderName = 'DM Total Return Swap v1'
        OBJECT = 'DM Total Return SwapSPEC'
        TYPE = 'Total Return Swap'

        NAME = MR_MainFunctions.NameFix(i.insid)
        IDENTIFIER = 'insaddr_'+str(i.insaddr)

        CurrencyCAL = ''
        CurrencyDAYC = ''
        CurrencyPERD = ''
        EffectiveDATE = ''
        CurrencyUNIT = i.curr.insid

        for l in i.legs():
            if str(l.type) == 'Total Return':
                EffectiveDATE = MR_MainFunctions.Datefix(l.start_day)
                if EffectiveDATE == ael.date_today():
                    EffectiveDATE = MR_MainFunctions.Datefix(l.start_day.add_days(-1))

        ReferenceAssetXREF = ''
        LegalEntityXREF = ''
        RefAssetReturnENUM = ''
        CouponRateDAYC = ''

        for l in i.legs():
            CouponRateDAYC = MR_MainFunctions.DayCountFix(l.daycount_method)
            if str(l.type) == 'Total Return':
                ReferenceAssetXREF = 'insaddr_'+str(l.float_rate.insaddr)
                if l.float_rate.issuer_ptynbr:
                    LegalEntityXREF = 'ptynbr_' + str(l.float_rate.issuer_ptynbr.ptynbr)+str(l.float_rate.curr.insid)
                if not(l.payleg == 1):
                    RefAssetReturnENUM = 'Receive Reference Asset Return'
                else:
                    RefAssetReturnENUM = 'Pay Reference Asset Return'

        CouponRateCAL = ''
        CouponRatePERD = 'simple'
        CouponRateVAL = ''
        UndrCrvIndXREF = ''
        TermNB = ''
        TermUNIT = 'Maturity'
        SpreadDAYC = ''
        SpreadPERD = ''
        SpreadUNIT = '%'
        SpreadVAL = ''

        for l in i.legs():
            if str(l.type) == 'Float':
                SpreadVAL = l.spread
            if str(l.type) == 'Fixed' and l.fixed_coupon == 0:
                if l.fixed_rate != 0:
                    CouponRateVAL = l.fixed_rate
                else:
                    CouponRateVAL = i.rate

        for l in i.legs():
            if str(l.type) != 'Total Return' and l.fixed_coupon == 0:
                if str(l.type) == 'Float':
                    UndrCrvIndXREF = ('CI_' + str(l.float_rate.insid) + '_'+ str(getattr(l, 'reset_period.count')) + str(getattr(l, 'reset_period.unit')))[0:50]
                    if str(l.rolling_period) not in ('0d', '0m', '0y'):
                        TermNB = getattr(l, 'rolling_period.count')
                        TermUNIT = getattr(l, 'rolling_period.unit')
                elif str(l.type) == 'Fixed':
                    UndrCrvIndXREF = ''
                    if str(l.rolling_period) not in ('0d', '0m', '0y'):
                        TermNB = getattr(l, 'rolling_period.count')
                        TermUNIT = getattr(l, 'rolling_period.unit')

        PremiumSchedXREF = ''
        LastBondPriceVAL = ''

        for l in i.legs():
            if str(l.type) == 'Total Return':
                if str(l.float_rate.insid) != '':
                    LastBondPriceVAL = l.initial_index_value*l.insaddr.contr_size/100
                else:
                    LastBondPriceVAL = '0'

        StateProcFUNC='@total return swap'
        r = getattr(i, 'recovery_rate')
        PercentLossVAL = 1 - r()
        CouponGenENUM = 'Backward'
        ReturnOnPriceFLAG = 'False'
        TermCAL = ''
        BusDayRuleRULE = ''
        BusDayRuleBUSD = ''
        BusDayRuleCONV = ''
        BusDayRuleCAL = ''
        CouponProratedFLAG = ''
        TotRtnPymtTypeENUM = ''
        FlotTotRtnRateXREF = ''
        DiscountCurveXREF = 'ZAR-Gov-Bonds-Disc'
        CrdtSprdCurveXREF = ''
        TheoModelXREF = 'Total Return Swap'
        MarketModelXREF = ''
        FairValueModelXREF = ''
        SettlementProcFUNC = ''
        
        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%
                    (BASFLAG, HeaderName, OBJECT, TYPE, NAME, IDENTIFIER,
                    CurrencyCAL, CurrencyDAYC, CurrencyPERD, CurrencyUNIT,
                    EffectiveDATE, ReferenceAssetXREF, ReturnOnPriceFLAG, LegalEntityXREF,
                    CouponRateCAL, CouponRateDAYC, CouponRatePERD,
                    CouponRateVAL, UndrCrvIndXREF, RefAssetReturnENUM,
                    PremiumSchedXREF, LastBondPriceVAL, StateProcFUNC,
                    PercentLossVAL, CouponGenENUM, TermNB, TermUNIT,
                    TermCAL, BusDayRuleRULE, BusDayRuleBUSD, BusDayRuleCONV,
                    BusDayRuleCAL, CouponProratedFLAG, TotRtnPymtTypeENUM,
                    FlotTotRtnRateXREF, DiscountCurveXREF, CrdtSprdCurveXREF,
                    TheoModelXREF, MarketModelXREF, FairValueModelXREF,
                    SettlementProcFUNC, LegalEntityXREF, SpreadDAYC,
                    SpreadPERD, SpreadUNIT, SpreadVAL))

        #Rollover record
        BASFLAG = 'rm_ro'
        HeaderName = 'DM Total Return Swap v1 : Variable Notional'
        ATTRIBUTE = 'Variable Notional'
        OBJECT = 'DM Total Return SwapSPEC'
        
        VariabNotionalDATE = ''
        VariabNotionalENUM = ''
        VariabNotionalCAL = ''
        VariabNotionalDAYC = ''
        VariabNotionalPERD = ''
        VariabNotionalUNIT = ''
        VariabNotionalVAL = ''
        Legs = i.legs()
        
        for LegNbr in Legs:
            for cf in LegNbr.cash_flows():
                if cf.legnbr.fixed_coupon == 0:
                    if cf.type == 'Total Return':
                        VariabNotionalDATE = MR_MainFunctions.Datefix(cf.pay_day)
                        VariabNotionalENUM = ''
                        VariabNotionalCAL = ''
                        VariabNotionalPERD = ''
                        VariabNotionalUNIT = i.curr.insid
                        VariabNotionalVAL = LegNbr.insaddr.contr_size
                        
                        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%
                                (BASFLAG, HeaderName, ATTRIBUTE, OBJECT, VariabNotionalDATE,
                                VariabNotionalENUM, VariabNotionalCAL, VariabNotionalDAYC,
                                VariabNotionalPERD, VariabNotionalUNIT, VariabNotionalVAL))
        outfile.close()
        
        for trades in i.trades():
            if MR_MainFunctions.ValidTradeNo(trades) == 0:
                if MR_MainFunctions.IsExcludedPortfolio(trades) == False:
                    PositionFile.CreatePosition(trades, PositionFilename)
                
    return i.insid

# WRITE - FILE ######################################################################################################

