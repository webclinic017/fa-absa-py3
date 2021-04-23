
'''
Purpose                 :Market Risk feed files
Department and Desk     :IT
Requester:              :Natalie Austin
Developer               :Douglas Finkel
CR Number               :264536,275268,278978,489655

 -- HISTORY --
Date           CR               Requestor          Developer          Change
----------------------------------------------------------------------------------------
2016-01-20     CHNG0003404656   Ashley Canter      Chris Human        http://abcap-jira/browse/MINT-444
2016-02-22     CHNG0003469409   Ashley Canter      Chris Human        http://abcap-jira/browse/MINT-488
'''

import ael, string, acm, MR_MainFunctions

InsL = []
MemL = []
YCList = []

# OPENFILE ##########################################################################################################
    
def OpenFile(temp,FileDir,Filename,*rest):

    filename            = FileDir + Filename

    outfile             =  open(filename, 'w')

    outfile.close()

    del InsL[:]
    InsL[:] = []  
    
    del MemL[:]
    MemL[:] = []


    del YCList[:]
    YCList[:] = []
    return filename

# OPENFILE ##########################################################################################################



# WRITE - FILE ######################################################################################################

def Write(yc,FileDir,Filename,*rest):
    
    filename            = FileDir + Filename
    currins     =       acm.FInstrument[yc.curr.insaddr]

    if (yc.yield_curve_name) not in YCList:
            YCList.append(yc.yield_curve_name)
    
    if yc.yield_curve_name in ('CDIssuerCurve_HR', 'CDIssuerCurve_HR_EUR', 'CDIssuerCurve_HR_GHS', 'CDIssuerCurve_HR_USD'):
        if (yc.seqnbr) not in InsL:
            InsL.append(yc.seqnbr)
            
            outfile = open(filename, 'a')
            
            for member in yc.attributes():
                for spreads in member.spreads():
                    
                    MemId = member.issuer_ptynbr.ptyid + '_' + yc.curr.insid + spreads.point_seqnbr.date_period
                    if (MemId) not in MemL:
                        MemL.append(MemId)
                        
                        #Base record
                        
                        BASFLAG             =       'BAS'
                        HeaderName          =       'Constant Term Default Swap'
                        OBJECT              =       'Constant Term Default SwapSPEC'
                        TYPE                =       'Constant Term Default Swap'
                        
                        asqlcode = "select i.insaddr from Instrument i where i.instype in ('Bond') and i.generic = 'Yes' and i.issuer_ptynbr ='%s'" %(member.issuer_ptynbr.ptynbr)
                        for instrument, in ael.asql(asqlcode, 1)[1][0]:
                            insaddr =  instrument.insaddr
                            break
                               
                        IDENTIFIER          =       member.issuer_ptynbr.ptyid + '_' + yc.curr.insid + '_CTDS_' + spreads.point_seqnbr.date_period
                        
                        NAME                =       (member.issuer_ptynbr.ptyid)[0:30] + '_' + yc.curr.insid + '_CTDS_' + spreads.point_seqnbr.date_period
                        
                        CurrencyUNIT        =       yc.curr.insid
                        CouponGenENUM       =       'Backward'
                        CouponRateCAL       =       ''
                        
                        CouponRateDAYC      =       MR_MainFunctions.DayCountFix(yc.storage_daycount)
                        CouponRatePERD      =       MR_MainFunctions.BusRule(yc.storage_rate_type)
                        CouponRateVAL       =       0
                        
                        if yc.storage_rate_type in ('Quarterly', 'Annual Comp'):
                            TermNB      =       '3'
                            TermUNIT    =       'Months'

                            #5 November 2010
                            #Douglas Finkel
                            #Logic built around the storage_rate_type of the yield curve to show 3 Months
                            #TermUNIT            =       MR_MainFunctions.CurveUnits(spreads.point_seqnbr.date_period)
                            #TermNB              =       MR_MainFunctions.Rolling_NameFix(spreads.point_seqnbr.date_period)

                        DiscountCurveXREF   =       MR_MainFunctions.NameFix(currins.MappedDiscountLink().Link().AsString().rsplit(',')[0].lstrip("'").rstrip("'"))
                        
                        EffectiveDATE       =       MR_MainFunctions.Datefix(ael.date_today())
                        MaturityDATE        =       MR_MainFunctions.Datefix(MR_MainFunctions.AddDatePeriod(ael.date_today(), spreads.point_seqnbr.date_period))
                        
                        if insaddr == 'None':
                            ReferenceAssetXREF  =       ''
                        else:
                            ReferenceAssetXREF  =       'insaddr_' + str(insaddr) +'_' +str(member.curr.insid)
                        
                        LegalEntityXREF     =       'ptynbr_' + str(member.issuer_ptynbr.ptynbr)+str(member.curr.insid)
                        
                        StateProcFUNC       =       '@default swap'
                        PremiumTypeENUM     =       'Rolling Premium'
                        CouponProratedFLAG  =       ''
                        PercentLossVAL      =       ''

                        HazardCurveXREF     =       member.issuer_ptynbr.ptyid + '_' + yc.curr.insid + '_HazardCurve' #ins.Legs().First().CreditRef().Issuer().Name() + '_' + str(i.curr.insid) + '_HazardCurve'

                        SpotPriceDAYC       =       MR_MainFunctions.DayCountFix(yc.storage_daycount)
                        SpotPricePERD       =       MR_MainFunctions.BusRule(yc.storage_rate_type)
                        
                        SpotPriceVAL        =       spreads.spread

                        SlidingTermUNIT     =       MR_MainFunctions.CurveUnits(spreads.point_seqnbr.date_period)
                        SlidingTermNB       =       MR_MainFunctions.Rolling_NameFix(spreads.point_seqnbr.date_period)
                        TheoModelXREF       =       'CDS Model'
                        MarketModelXREF     =       'CDS Mkt Model'
                        
                        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, NAME, IDENTIFIER, CurrencyUNIT, CouponGenENUM, CouponRateCAL, CouponRateDAYC, CouponRatePERD, CouponRateVAL, TermUNIT, TermNB, DiscountCurveXREF, EffectiveDATE, MaturityDATE, ReferenceAssetXREF, LegalEntityXREF, StateProcFUNC, PremiumTypeENUM, CouponProratedFLAG, PercentLossVAL, HazardCurveXREF, SpotPriceDAYC, SpotPricePERD, SpotPriceVAL, SlidingTermUNIT, SlidingTermNB, TheoModelXREF, MarketModelXREF))

                        # Roll Over Variable Notional
                
                        BASFLAG             =       'rm_ro'
                        HeaderName          =       'Constant Term Default Swap : Variable Notional'
                        ATTRIBUTE           =       'Variable Notional'
                        OBJECT              =       'Constant Term Default SwapSPEC'
                        
                        VariabNotionalVAL   = '100'
                        VariabNotionalUNIT  = yc.curr.insid
                        VariabNotionalDATE  = MaturityDATE
                        VariabNotionalSSEQ  = ''
                        VariabNotionalSEQ   = ''
                        
                        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, VariabNotionalVAL, VariabNotionalUNIT, VariabNotionalDATE, VariabNotionalSSEQ, VariabNotionalSEQ))
            
            outfile.close()

    return str(yc.seqnbr)

# WRITE - FILE ######################################################################################################



# WRITE - FILE ######################################################################################################

def Write2(yc,FileDir,Filename,*rest):
    
    filename            = FileDir + Filename
    currins     =       acm.FInstrument[yc.curr.insaddr]
    
    if yc.yield_curve_name not in ('CDIssuerCurve_HR', 'CDIssuerCurve_HR_EUR', 'CDIssuerCurve_HR_GHS', 'CDIssuerCurve_HR_USD'):
        if (yc.seqnbr) not in InsL:
            InsL.append(yc.seqnbr)
            
            outfile = open(filename, 'a')
            
            for member in yc.attributes():
                for spreads in member.spreads():
                    
                    MemId = member.issuer_ptynbr.ptyid + '_' + yc.curr.insid + spreads.point_seqnbr.date_period
                    if (MemId) not in MemL:
                        MemL.append(MemId)
                        
                        #Base record
                        
                        BASFLAG             =       'BAS'
                        HeaderName          =       'Constant Term Default Swap'
                        OBJECT              =       'Constant Term Default SwapSPEC'
                        TYPE                =       'Constant Term Default Swap'
                        
                        asqlcode = "select i.insaddr from Instrument i where i.instype in ('Bond') and i.generic = 'Yes' and i.issuer_ptynbr ='%s'" %(member.issuer_ptynbr.ptynbr)
                        for instrument, in ael.asql(asqlcode, 1)[1][0]:
                            insaddr =  instrument.insaddr
                            break
                        
                        IDENTIFIER          =       member.issuer_ptynbr.ptyid + '_' + yc.curr.insid + '_CTDS_' + spreads.point_seqnbr.date_period
                        
                        NAME                =       (member.issuer_ptynbr.ptyid)[0:30] + '_' + yc.curr.insid + '_CTDS_' + spreads.point_seqnbr.date_period
                        
                        CurrencyUNIT        =       yc.curr.insid
                        CouponGenENUM       =       'Backward'
                        CouponRateCAL       =       ''
                        
                        CouponRateDAYC      =       MR_MainFunctions.DayCountFix(yc.storage_daycount)
                        CouponRatePERD      =       MR_MainFunctions.BusRule(yc.storage_rate_type)
                        CouponRateVAL       =       0

                        if yc.storage_rate_type in ('Quarterly', 'Annual Comp'):
                            TermNB            =       '3'
                            TermUNIT          =       'Months'
                            
                            #5 November 2010
                            #Douglas Finkel
                            #Logic built around the storage_rate_type of the yield curve to show 3 Months
                            #TermUNIT            =       MR_MainFunctions.CurveUnits(spreads.point_seqnbr.date_period)
                            #TermNB              =       MR_MainFunctions.Rolling_NameFix(spreads.point_seqnbr.date_period)

                        DiscountCurveXREF   =       MR_MainFunctions.NameFix(currins.MappedDiscountLink().Link().AsString().rsplit(',')[0].lstrip("'").rstrip("'"))
                        
                        EffectiveDATE       =       MR_MainFunctions.Datefix(ael.date_today())
                        MaturityDATE        =       MR_MainFunctions.Datefix(MR_MainFunctions.AddDatePeriod(ael.date_today(), spreads.point_seqnbr.date_period))
                        
                        if insaddr == 'None':
                            ReferenceAssetXREF  =       ''
                        else:
                            ReferenceAssetXREF  =       'insaddr_' + str(insaddr) + '_' + str(member.curr.insid)
                        
                        LegalEntityXREF     =       'ptynbr_' + str(member.issuer_ptynbr.ptynbr)+ str(member.curr.insid)
                        
                        StateProcFUNC       =       '@default swap'
                        PremiumTypeENUM     =       'Rolling Premium'
                        CouponProratedFLAG  =       ''
                        PercentLossVAL      =       ''

                        HazardCurveXREF     =       member.issuer_ptynbr.ptyid + '_' + yc.curr.insid + '_HazardCurve' #ins.Legs().First().CreditRef().Issuer().Name() + '_' + str(i.curr.insid) + '_HazardCurve'

                        SpotPriceDAYC       =       MR_MainFunctions.DayCountFix(yc.storage_daycount)
                        SpotPricePERD       =       MR_MainFunctions.BusRule(yc.storage_rate_type)
                        
                        SpotPriceVAL        =       spreads.spread

                        SlidingTermUNIT     =       MR_MainFunctions.CurveUnits(spreads.point_seqnbr.date_period)
                        SlidingTermNB       =       MR_MainFunctions.Rolling_NameFix(spreads.point_seqnbr.date_period)
                        TheoModelXREF       =       'CDS Model'
                        MarketModelXREF     =       'CDS Mkt Model'
                        
                        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, NAME, IDENTIFIER, CurrencyUNIT, CouponGenENUM, CouponRateCAL, CouponRateDAYC, CouponRatePERD, CouponRateVAL, TermUNIT, TermNB, DiscountCurveXREF, EffectiveDATE, MaturityDATE, ReferenceAssetXREF, LegalEntityXREF, StateProcFUNC, PremiumTypeENUM, CouponProratedFLAG, PercentLossVAL, HazardCurveXREF, SpotPriceDAYC, SpotPricePERD, SpotPriceVAL, SlidingTermUNIT, SlidingTermNB, TheoModelXREF, MarketModelXREF))

                        # Roll Over Variable Notional
                
                        BASFLAG             =       'rm_ro'
                        HeaderName          =       'Constant Term Default Swap : Variable Notional'
                        ATTRIBUTE           =       'Variable Notional'
                        OBJECT              =       'Constant Term Default SwapSPEC'
                        
                        VariabNotionalVAL   = '100'
                        VariabNotionalUNIT  = yc.curr.insid
                        VariabNotionalDATE  = MaturityDATE
                        VariabNotionalSSEQ  = ''
                        VariabNotionalSEQ   = ''
                        
                        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, VariabNotionalVAL, VariabNotionalUNIT, VariabNotionalDATE, VariabNotionalSSEQ, VariabNotionalSEQ))
            
            outfile.close()

    return str(yc.seqnbr)

# WRITE - FILE ######################################################################################################


