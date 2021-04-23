import acm
import at_addInfo

nr = 0

def ProjectCashFlowAmend(fTrade):
    '''
    trade = acm.FTrade()
    trade.Instrument(fTrade.Instrument())
    trade.Currency('ZAR')
    trade.TradeTime(acm.Time().DateToday())
    trade.Acquirer('IRD DESK')
    trade.Portfolio('Swap Flow')
    trade.Counterparty('BARCLAYS BANK PLC')
    trade.Quantity(fTrade.Nominal())
    trade.Status('BO-BO Confirmed')
    trade.Trader('CHABUDAR')
    trade.Type('Normal')
    trade.ValueDay(acm.Time().DateToday())
    trade.Commit()   
    '''
    try:
        ContractTrade = fTrade
        #ContractTrade.Status('Terminated')
        #ContractTrade.Status('FO Confirmed')
        #ContractTrade.Type('Normal')
        #ContractTrade.OptionalKey('')
        #ContractTrade.Commit()
        
        ClosingTrade = ContractTrade.Clone()
        ClosingTrade.Nominal(-1*ContractTrade.Nominal())
        ClosingTrade.TradeTime(acm.Time.TimeNow())
        ClosingTrade.ValueDay(acm.Time.DateToday())
        ClosingTrade.AcquireDay(acm.Time.DateToday())
        ClosingTrade.OptionalKey('')
        ClosingTrade.Type('Closing')
        ClosingTrade.Status('Terminated')
        ClosingTrade.Trader('CHABUDAR')
        ClosingTrade.Portfolio('Swap Flow')
        ClosingTrade.MirrorTrade(None)
        ClosingTrade.Instrument(ContractTrade.Instrument())
        print ClosingTrade.Instrument().Name()
        ClosingTrade.Commit()    
        specCCP = acm.FAdditionalInfoSpec['CCPmiddleware_id']
        addInfoCCP = acm.FAdditionalInfo.Select01('recaddr='+ str(fTrade.Oid()) +' and addInf=' + str(specCCP.Oid()), '')
        at_addInfo.save_or_delete(ClosingTrade, 'CCPmiddleware_id', addInfoCCP.Value())
        print ClosingTrade.Oid(), addInfoCCP.FieldValue(), ClosingTrade.Trader().Name()
        for payment in ClosingTrade.Payments():
            print '****************** Payments removed XXXXXXXXXXX', payment.Type(), payment.Amount(), ClosingTrade.Oid()
            payment.Delete()
    except StandardError, e:
        print 'The following error occurred ************************ Trade ID', fTrade.Oid(), str(e)
        

#fTrade = acm.FTrade[59340491]

#print ProjectCashFlowAmend(fTrade)

#ListItems = [58966121]
ListItems = [
51867291,
55021292,
55317614,
54412541,
55883790,
56017271,
55765497,
54887339,
56375807,
53806002,
55798454,
57130561,
53700463,
54549475,
54621794,
56890877,
54549435,
54621795,
55021301,
55728852,
56790818,
49663845,
56505290,
58740261,
54760663,
55241767,
55773071,
54483803,
54892771,
58966121,
54776796,
53113969,
56557798,
53308430,
52574466,
52578663,
55303946,
55303935,
55021297,
55711008,
52056826,
55904077,
45090225,
54233468,
46739350,
56466353,
52291265,
54060072,
51909810,
53274571,
52217583,
55573659,
55475714,
51909951,
51402491,
54506908,
54059681,
54555129,
51909607,
54554784,
54331682,
54059731,
52217567,
55820621,
54059534,
54761889,
54060124,
54538374,
53449214,
54059846,
55475719,
53396300,
54515760,
55566605,
54059242,
56999705,
53700459,
54708640,
54060324,
53769726,
53781138,
54554983,
51152430,
51482768,
54645347,
54634598,
51836581,
39109151,
54060298,
54059438,
51676776,
52290557,
54060292,
55003906,
51265016,
52290694,
53409618,
54427577,
57085018,
53781056,
53707101,
53745646,
52290978,
54555087,
54676874,
54554786,
54059936,
53176894,
54060006,
53700461,
54643311,
51402512,
53545786,
52155587,
40414078,
46471225,
52894385,
51988457,
57441568,
52333030,
57917221,
58923156,
48223203,
55950917,
55894555,
52712796,
52333053,
56829376,
57095471,
52901147,
52333055,
52136016,
51843873,
53117318,
52056794,
51918411,
52392081,
52766615,
52333054,
52333025,
53353424,
52901159,
53320412,
52333050,
52333032,
58627031,
54554537,
57549236,
52021483,
56758134,
52333026,
55699723,
59237469,
59379491,
59340491,
55939763,
56498049,
41449607,
54315852,
54874347,
56356958,
59295942,
51652968,
53980047,
55307189,
55796558,
52867414,
53157522,
55449837,
49883612,
56536957,
54946144,
46284368,
52021484,
55979971,
48094328,
46501318]


print 'Started the update script..............'
for listItem in ListItems:
    fTrade = acm.FTrade[listItem]
    if fTrade == None:
        print 'Not found ***********************', listItem
    else:
        #if fTrade.Trader().Name() not in ('SULLIVGR','ABAC499','LOIOH2'):
        #    if fTrade.Counterparty().Name() not in ('ABAX FIXED INTEREST FUND TRUST','CITIGROUP GLOBAL MARKETS','STANDARD BANK SA','FIRSTRAND BANK LTD'):
        nr+=1
                #print 'Count',nr,'- FA Trade',fTrade.Oid(),fTrade.Trader().Name(),' - ',fTrade.TradeTime(),'Counterparty',fTrade.Counterparty().Name(),'Acquirer',fTrade.Acquirer().Name()
                #for payment in fTrade.Payments():
                #    print '****************** PAYMETS','Front Arena trade',fTrade.Oid(),payment.Type(),payment.Amount()
        print 'Count', nr
        ProjectCashFlowAmend(fTrade)
print 'Completed the update script..............'

