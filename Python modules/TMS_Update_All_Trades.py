import ael, amb, TMS_Recon_Template, SAGEN_str_functions, SAGEN_Functions, time, TMS_Functions

#TrdFilter = 'TMS_Test_Trades_Original_Excl'
#TrdFilter = 'TMS_NLDO & Hedg8'
TrdFilter = 'TMS_Trades_Recon'
#TrdFilter = 'TMS_NLDIR_Opt'

def Update_Party_Fica():
    
    for t in ael.TradeFilter[TrdFilter].trades():
        #if t.counterparty_ptynbr.ptynbr in (17,17892,22819,25408):
        SAGEN_Functions.set_party_add_info(t.counterparty_ptynbr, 'FICA_Compliant', 'Yes')

def Update_Version (Version,Count,Flag,*rest):


    DateToday = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    #DateToday = time.strftime("%Y-%m-%d",time.localtime())
    
        #if t.insaddr.instype == 'CurrSwap':
        #if t.insaddr.instype == 'Option' and t.insaddr.und_instype == 'FRA':
        #if t.insaddr.instype == 'Option' and t.insaddr.und_instype == 'Swap':# and t.prfnbr.display_id() == 'NLDOBB_Struc':
        #if t.insaddr.instype == 'Floor':
        #if t.insaddr.instype == 'Cap':
        #if t.insaddr.instype == 'Swap':
        #if t.insaddr.instype == 'FxSwap':
    
        #print t.insaddr.instype + ' - ' + (str)(t.trdnbr)
        #SAGEN_Functions.set_trade_addinf(t,'TMS_Gen_Message',DateToday)
    
    count_1 = 0
    count_2 = 1
    count_3 = 0
    
    while count_1 < Version:
    
        count_3 = count_3 + Count
        
        for t in ael.TradeFilter[TrdFilter].trades():
            #print t.counterparty_ptynbr.ptynbr
            #if t.counterparty_ptynbr.ptynbr in (17,17892,22819,25408):
            if t.optional_key.__contains__('TMS') == 0:# and t.status == 'Void':
                count_2 = count_2 + 1
            
                try:
                    trd = t.clone()
                    trd.optional_key = Flag + (str)(count_2 + count_3)
                    trd.commit()
                except:
                    print 'Trade could not be cloned'
                
        count_1 = count_1 + 1
        
def Update_Trade(Value,*rest):
    
    DateToday = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    
    for t in ael.TradeFilter[TrdFilter].trades():
        if t.trdnbr in (2684098, 270366):
        #if t.optional_key.__contains__('TMS') == 1 and t.counterparty_ptynbr.ptynbr == 10395:
            print t.trdnbr
            SAGEN_Functions.set_trade_addinf(t, 'TMS_Gen_Message', DateToday)



# and t.optional_key.__contains__('TMS') == 1:#        if t.insaddr.exp_day.to_string('%Y-%m-%d') >= TMS_Functions.Expired_Date() and t.status != 'Void':
#        if t.optional_key.__contains__('TMS') == 0:# and t.status == 'Void':#and ael.date(t.updat_time) == '2008-05-06':
#            try:
#                trd = t.clone()
#                trd.text2 = Value
#                trd.commit()
#            except:
#                print 'Trade could not be cloned'

#Update_Party_Fica()
#Update_Version(10,1000,'F_')
Update_Trade('1st send')

