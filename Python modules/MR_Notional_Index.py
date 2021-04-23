'''
Purpose                 :[Market Risk feed files],[Set the indexation lag to 1 Day for equity swaps],[Set the indexation lag to 0 Months for PriceIndex],
                        [Set the indexation lag to 0 Years for Bond and IndexLinkedBond]
Department and Desk     :[IT],[Market Risk],[Market Risk],[Market Risk]
Requester:              :[Natalie Austin],[Susan Kruger],[Susan Kruger],[Susan Kruger]
Developer               :[Douglas Finkel],[Willie van der Bank],[Willie van der Bank],[Willie van der Bank]
CR Number               :[264536, 644690, 701575],[749647 25/08/2011],[824244 11/11/2011],[831357 18/11/2011]


Decription
Notional indices for Currency Swaps are missing
Added Indexation lag of Price Indices to be set according to the Index Type field

-- HISTORY --
Date           CR               Requestor          Developer          Change
----------------------------------------------------------------------------------------
2018-11-01     CHG1001083227    Market RisK        Andile Biyana      http://abcap-jira/browse/ABITFA-5619
'''

import ael, string, acm, PositionFile, MR_MainFunctions

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
    
    if (i.insaddr) not in InsL:
        InsL.append(i.insaddr)
        
        #Base record
        outfile = open(filename, 'a')
        
        BASFLAG                 =       'BAS'
        HeaderName              =       'Notional Index'
        OBJECT                  =       'Notional IndexSPEC'
        TYPE                    =       'Notional Index'
        NAME                    =       MR_MainFunctions.NameFix(str(i.insid))+'_NI'
        IDENTIFIER              =       MR_MainFunctions.NameFix(str(i.insid))+'_NI'    
        
        if i.instype in ('EquityIndex', 'Stock', 'Bond', 'IndexLinkedBond', 'ETF'):
            PostDeterminedFLAG = 'TRUE'
        elif i.instype == 'PriceIndex':
            PostDeterminedFLAG = 'FALSE'
            
        if i.instype == 'ETF': 
            HistoricalCrvXREF       =       MR_MainFunctions.NameFix(str(i.und_insaddr.insid))+'_HistoricalCurve'
        else:
            HistoricalCrvXREF       =       MR_MainFunctions.NameFix(str(i.insid))+'_HistoricalCurve'
        
        if i.instype in ('Bond', 'IndexLinkedBond'):
            IndxatnLagTermNB = '0'
            IndxatnLagTermUNIT = 'Years'
        elif i.instype in ('EquityIndex', 'Stock', 'ETF'): #'PriceIndex' removed
            IndxatnLagTermNB = '1'
            IndxatnLagTermUNIT = 'Days'
        elif i.instype in ('PriceIndex'): #'PriceIndex' added in own logic
            IndxatnLagTermNB = '0'
            IndxatnLagTermUNIT = 'Months'
        
        BusDayRuleRULE  = ''
        BusDayRuleBUSD  = ''
        BusDayRuleCONV  = '' 
        BusDayRuleCAL   = ''        
        UseInstLagFLAG          =       ''
        IndexLevelFUNC          =       '@lag'        
        UnderlyingXREF          =       ''
        if i.instype in ('Stock', 'Bond', 'IndexLinkedBond'):
            UnderlyingXREF          =   str(i.insid)+'_Synthetic'
        if i.instype in ('EquityIndex', 'PriceIndex'):
            UnderlyingXREF          =   'insaddr_'+str(i.insaddr) #+'_MarketIndex'
        if i.instype in ('ETF'):
        		UnderlyingXREF          =   'insaddr_'+str(i.und_insaddr.insaddr)    
        
        try:
            DiscountCurveXREF   =       ins.MappedDiscountLink().Value().Link().YieldCurveComponent().Curve().Name()
        except:
            DiscountCurveXREF   =       ins.MappedDiscountLink().Value().Link().YieldCurveComponent().Name()
        if i.insid == 'SACPI':
            DiscountCurveXREF = 'ZAR-CPI'
        TermNB                  =       ''
        TermUNIT                =       'Maturity'
        dcins = ael.YieldCurve[DiscountCurveXREF]
        
        UnitDAYC                =       MR_MainFunctions.DayCountFixNotionalIndex(dcins.storage_daycount)
        UnitPERD                =       MR_MainFunctions.BusRule(dcins.storage_rate_type)
        UnitUNIT                =       '%'
        
        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, NAME, IDENTIFIER, PostDeterminedFLAG, HistoricalCrvXREF, IndxatnLagTermNB, IndxatnLagTermUNIT, BusDayRuleRULE, BusDayRuleBUSD, BusDayRuleCONV, BusDayRuleCAL, UseInstLagFLAG, IndexLevelFUNC, UnderlyingXREF, DiscountCurveXREF, TermNB, TermUNIT, UnitDAYC, UnitPERD, UnitUNIT ))
        
        outfile.close()    

    return i.insid

# WRITE - FILE ######################################################################################################




# WRITE2 - FILE ######################################################################################################

def Write2(temp,FileDir,Filename,PositionName,currpair,LockedLeg,ResetLeg,*rest):
    
    filename            = FileDir + Filename
    insLL = acm.FInstrument[LockedLeg]
    insRL = acm.FInstrument[ResetLeg]
    LocalCAL = acm.FCalendar['ZAR Johannesburg'].Name()[0:3]
    #Base record
    
    outfile = open(filename, 'a')
    
    BASFLAG                 =       'BAS'
    HeaderName              =       'Notional Index'
    OBJECT                  =       'Notional IndexSPEC'
    TYPE                    =       'Notional Index'
    NAME                    =       currpair+'_NI'
    IDENTIFIER              =       currpair+'_NI'
    PostDeterminedFLAG      =       'TRUE'    
    HistoricalCrvXREF       =       currpair+'_HistoricalCurve'    
    IndxatnLagTermNB = '0'
    IndxatnLagTermUNIT = 'Months'
    BusDayRuleRULE = 'Preceding'
    BusDayRuleBUSD = 0
    BusDayRuleCONV = 'Regular' 
    BusDayRuleCAL = 'Cal'+LocalCAL
    UseInstLagFLAG          =        'True'
    IndexLevelFUNC          =       '@lag'
    UnderlyingXREF          =       str(insRL.Currency().Name()) + str(insLL.Currency().Name()) + '_FX'    
    DiscountCurveXREF       =       currpair+'_FX_Forward'
    TermNB                  =       ''
    TermUNIT                =       'Maturity'
    
    try:
        DiscountCurve   =       insLL.MappedDiscountLink().Value().Link().YieldCurveComponent().Curve().Name()
    except:
        DiscountCurve   =       insLL.MappedDiscountLink().Value().Link().YieldCurveComponent().Name()
        
    ics = ael.YieldCurve[DiscountCurve]
    UnitDAYC                =       'actual/360'
    UnitPERD                =       'simple'
    UnitUNIT                =       '%'

    outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, NAME, IDENTIFIER, PostDeterminedFLAG, HistoricalCrvXREF, IndxatnLagTermNB, IndxatnLagTermUNIT, BusDayRuleRULE, BusDayRuleBUSD, BusDayRuleCONV, BusDayRuleCAL, UseInstLagFLAG, IndexLevelFUNC, UnderlyingXREF, DiscountCurveXREF, TermNB, TermUNIT, UnitDAYC, UnitPERD, UnitUNIT ))
    
    outfile.close()    

    return insLL.Name()

# WRITE2 - FILE ######################################################################################################
