"""----------------------------------------------------------------------------
MODULE
    F273728_ConvertFXTrades - Script for converting pre 4.0 FX Trades to new format.

    (c) Copyright 2005 by Front Capital Systems AB. All rights reserved.

DESCRIPTION

        Run the script by loading it into the Python Editor and selecting
        Special -> Reload Module. A GUI appears that let's you choose between running
        the script in test mode or normal mode. In test mode no changes would be commited
        to the database. The GUI also lets you choose between running the script with no
        diagnostics written to the log console or with detailed diagnostics.

        The execution can be rolled back by using the script FStartRollback. See FCA2324
        about how to roll back a script execution.
        
        Currency Trades are updated with a FX Spot tag on the trade_process bit array field. 
        FX Swap trades are voided and an FX Forward trade or an FX Swap trade pair are created 
        in the Currency Instrument to replace the original deal. The original deal's trade 
        number is stored on the newly created trades' free_text2 field.


ENDDESCRIPTION
----------------------------------------------------------------------------"""
import ael, acm
import FBDPRollback
import FBDPCommon

Summary = FBDPCommon.Summary

class ConvertFXTrades(FBDPRollback.RollbackInfo):

        
    def perform(self, args):
        import FBDPString
        logme = FBDPString.logme
        self.ael_variables_dict = args
        terminated_trades=[]
        
        for i in ael.Instrument.select("instype='Curr'"):
            logme('Processing Currency %s.'%i.insid, 'INFO')                                                  
            for t in i.trades():                                                            
                if (t.trade_process != 0 and t.connected_trdnbr!=None):
                    continue

                logme('Processing a Curr trade', 'DEBUG')
                t = t.clone()
                t.trade_process = 4096
                if t.connected_trdnbr==None:
                    t.connected_trdnbr=t.trdnbr
                self.add(t, ['trade_process'])
                self.add(t, ['connected_trdnbr'])
                Summary().ok(t, Summary().UPDATE)                        
        
        for i in ael.Instrument.select("instype='FxSwap'"):
        #for i in [ael.Instrument['ZAR-USD_090630_R-ZAR 1500000_9.3']]:
            logme('Processing FxSwap %s.'%i.insid, 'INFO')
            for t in i.trades():
                terminated_near=0
                terminated_far=0 
                if t.status=='Simulated' and not i.generic:
                    t=t.clone()
                    t.text1='Previously simulated trade'
                    t.text2='Void as part of upgrade'
                    print 'Simulated'
                    self.beginTransaction()
                elif (t.status in ('Void', 'Confirmed Void') or i.generic):
                    continue
                else:
                    print 'Started'
                    logme('Processing an FXSwap trade', 'INFO')
                    logme('Trade quantity: %d' %t.quantity, 'INFO')
                    logme('# Original Trade payments: %d' %len(t.payments()), 'INFO')
                    '''
                    external_id=t.optional_key
                    if external_id not in [None,'']:
                        t = t.clone()
                        self.beginTransaction()
                        t.optional_key='#'+t.optional_key
                        self.add(t, ['optional_key'])
                        print "Optional key:",t.optional_key
                        self.commitTransaction()
                    '''
                    t = t.clone()
                    t.text1='Converted to cash trade'
                    t.text2='as part of upgrade'
                    orig_instr = t.insaddr
                    orig_type = t.type
                    contract_size = orig_instr.contr_size*t.quantity
                    leg = orig_instr.legs()
                    if leg[0].payleg == 1:
                        payleg = 0
                        nonpayleg = 1
                    else:
                        payleg = 1
                        nonpayleg = 0
                    pay_leg = leg[payleg]
                    rec_leg = leg[nonpayleg]
                    is_outright = 0
                    only_nearleg = 0
                    if rec_leg.nominal_at_start == 0 :
                        is_outright = 1
                    elif rec_leg.nominal_at_end == 0:
                        is_outright = 1
                        only_nearleg = 1
                    if is_outright == 1:
                        logme('This an outright forward', 'DEBUG')
                        fxtype='outright/forward'
                    else:
                        logme('This is an fx swap', 'DEBUG')
                        fxtype='swap'
                    new_instr = rec_leg.curr
                    
                    # Workaround if counterparty is 'Not Trading'
                    ptynbr = t.counterparty_ptynbr
                    if ptynbr.ptyid == 'Not Trading':
                        ptynbr = ael.Party['FMAINTENANCE']

                    #Assign new instr...
                    if not only_nearleg:
                        far_trade = ael.Trade.new(new_instr)
                        far_trade.prfnbr = t.prfnbr
                        far_trade.hedge_trdnbr=t.original().trdnbr
                        far_trade.acquirer_ptynbr = t.acquirer_ptynbr
                        '''
                        if t.counterparty_ptynbr.not_trading:
                            pc=t.counterparty_ptynbr.clone()
                            pc.not_trading=0
                            far_trade.counterparty_ptynbr = pc
                        '''
                        far_trade.counterparty_ptynbr = t.counterparty_ptynbr
                        far_trade.curr = leg[payleg].curr
                        far_trade.curr = pay_leg.curr
                        far_trade.acquire_day = orig_instr.exp_day
                        far_trade.value_day = orig_instr.exp_day
                        far_trade.time = t.time                                               
                        far_trade.trader_usrnbr = t.trader_usrnbr  
                        far_trade.sales_person_usrnbr = t.sales_person_usrnbr 
                        far_trade.guarantor_ptynbr=t.guarantor_ptynbr
                        far_trade.optkey1_chlnbr=t.optkey1_chlnbr
                        far_trade.optkey2_chlnbr=t.optkey2_chlnbr
                        far_trade.optkey3_chlnbr=t.optkey3_chlnbr
                        far_trade.optkey4_chlnbr=t.optkey4_chlnbr
                        far_trade.your_ref=t.your_ref
                        far_trade.text2 = str(t.trdnbr)                                         
                        pay_endfactor = pay_leg.nominal_factor * (1.0 + pay_leg.fixed_rate)
                        rec_endfactor = rec_leg.nominal_factor * (1.0 + rec_leg.fixed_rate)
                        far_trade.price = pay_endfactor / rec_endfactor
                        far_trade.quantity = contract_size * rec_endfactor
                        far_trade.premium = - contract_size * pay_endfactor
                        far_trade.quantity_is_derived = pay_leg.is_locked
                        
                        if t.status=='Terminated':
                            far_trade.status = 'BO Confirmed'
                            terminated_far=1
                        else:
                            far_trade.status = t.status
                        far_trade.type = t.type
                        far_trade.reference_price = pay_leg.nominal_factor / rec_leg.nominal_factor
                        if is_outright:
                            far_trade.sales_margin = t.sales_margin
                            far_trade.broker_ptynbr = t.broker_ptynbr       
                            #far_trade.optional_key=external_id
                            far_trade.fee = t.fee                                               
                            self.TradeAddInfoCopy(t, far_trade)                                  
                            far_trade.trade_process = 8192
                            for p in t.original().payments():
                                pn = ael.Payment.new(far_trade)
                                pn.amount           = p.amount
                                pn.accnbr           = p.accnbr
                                pn.curr             = p.curr
                                pn.fx_transaction   = p.fx_transaction
                                pn.original_curr    = p.original_curr
                                pn.our_accnbr       = p.our_accnbr
                                pn.payday           = p.payday
                                pn.ptynbr           = p.ptynbr
                                pn.text             = p.text
                                pn.type             = p.type
                                pn.valid_from       = p.valid_from
                                logme('payment created for far trade %d of %s: %s' %(far_trade.trdnbr, fxtype, i.insid), 'INFO')
                            
                    if (only_nearleg or not is_outright):
                            near_trade = ael.Trade.new(new_instr)
                            if only_nearleg:
                                near_trade.trade_process = 8192
                            else:
                                far_trade.trade_process = 32768
                            near_trade.prfnbr = t.prfnbr
                            near_trade.hedge_trdnbr=t.original().trdnbr
                            near_trade.acquirer_ptynbr = t.acquirer_ptynbr
                            near_trade.counterparty_ptynbr = t.counterparty_ptynbr
                            '''
                            if t.counterparty_ptynbr.not_trading:
                                pc=t.counterparty_ptynbr.clone()
                                pc.not_trading=0
                                near_trade.counterparty_ptynbr = t.counterparty_ptynbr
                            '''
                            near_trade.curr = pay_leg.curr
                            # Request by JL - accomodate FXSwaps with start date in the future                      
                    
                            if pay_leg.start_day < rec_leg.start_day:
                                near_trade.acquire_day = pay_leg.end_day
                                for cf in pay_leg.cash_flows():
                                    print near_trade.acquire_day
                                    if cf.pay_day<near_trade.acquire_day:
                                        near_trade.acquire_day = cf.pay_day
                            else:
                                near_trade.acquire_day = pay_leg.end_day
                                for cf in rec_leg.cash_flows():
                                    print near_trade.acquire_day
                                    if cf.pay_day<near_trade.acquire_day:
                                        print 'change'
                                        near_trade.acquire_day = cf.pay_day
                            near_trade.value_day=near_trade.acquire_day 
                            near_trade.price = pay_leg.nominal_factor / rec_leg.nominal_factor
                            near_trade.quantity = -contract_size * rec_leg.nominal_factor
                            near_trade.premium = contract_size * pay_leg.nominal_factor
                            near_trade.quantity_is_derived = pay_leg.is_locked
                            
                            if t.status=='Terminated':
                                near_trade.status = 'BO Confirmed'
                                terminated_near=1
                            else:
                                near_trade.status = t.status
                                
                            near_trade.type = t.type
                            near_trade.reference_price = near_trade.price
                            near_trade.sales_margin = t.sales_margin
                            near_trade.time = t.time                                           
                            near_trade.trader_usrnbr = t.trader_usrnbr  
                            near_trade.sales_person_usrnbr = t.sales_person_usrnbr 
                            near_trade.guarantor_ptynbr=t.guarantor_ptynbr
                            near_trade.optkey1_chlnbr=t.optkey1_chlnbr
                            near_trade.optkey2_chlnbr=t.optkey2_chlnbr
                            near_trade.optkey3_chlnbr=t.optkey3_chlnbr
                            near_trade.optkey4_chlnbr=t.optkey4_chlnbr
                            #near_trade.optional_key=external_id
                            near_trade.your_ref=t.your_ref
                            near_trade.text2 = str(t.trdnbr)                                    
                            near_trade.broker_ptynbr = t.broker_ptynbr                          
                            near_trade.fee = t.fee                                              
                            self.TradeAddInfoCopy(t, near_trade) 
                            if not only_nearleg:
                                near_trade.trade_process = 16384
                            for p in t.original().payments():
                                pn = ael.Payment.new(near_trade)
                                pn.amount           = p.amount
                                pn.accnbr           = p.accnbr
                                pn.curr             = p.curr
                                pn.fx_transaction   = p.fx_transaction
                                pn.original_curr    = p.original_curr
                                pn.our_accnbr       = p.our_accnbr
                                pn.payday           = p.payday
                                pn.ptynbr           = p.ptynbr
                                pn.text             = p.text
                                pn.type             = p.type
                                pn.valid_from       = p.valid_from
                                logme('payment created for near trade %d of %s: %s' %(near_trade.trdnbr, fxtype, i.insid), 'INFO')
                            
                    if t.mirror_trdnbr>0:
                        if t.trdnbr==t.mirror_trdnbr.trdnbr:
                            string_trade=str(t.trdnbr)
                            mirrors=ael.Trade.select('mirror_trdnbr='+string_trade)
                            for mirrortrade in mirrors:
                                if mirrortrade.trdnbr!=t.trdnbr:
                                    mirror_port=mirrortrade.prfnbr
                        else:
                            mirror_port=t.mirror_trdnbr.prfnbr
                        self.beginTransaction()
                        if (is_outright == 0):
                            near_trade.commit_with_mirror(t.mirror_trdnbr.prfnbr)
                            far_trade.connected_trdnbr = near_trade
                            far_trade.commit_with_mirror(mirror_port)
                            
                        elif only_nearleg:
                            near_trade.commit_with_mirror(mirror_port)
                        else:
                            far_trade.commit_with_mirror(mirror_port)
                    else:
                        self.beginTransaction()
                        if (is_outright == 0):
                            self.add_trade(near_trade)
                            far_trade.connected_trdnbr = near_trade
                            self.add_trade(far_trade)
                        elif only_nearleg:
                            self.add_trade(near_trade)
                        else:
                            self.add_trade(far_trade)
                
                # now void the original obsolete trade
                t.status = 'Void'
                self.add(t, ['status'])
                try:
                    self.commitTransaction()
                except :
                    self.abortTransaction()
                    Summary().fail(t, Summary().CREATE, i.insid+' failed to commit', t.trdnbr)  
                    continue
                
                #Move Terminated trade to correct Trade status
                if terminated_near or terminated_far:
                    acm.PollDbEvents()
                    self.beginTransaction()
                # since add-trade recomputes premium wrongly for fx, do this:
                    if terminated_near:
                        near_trade = near_trade.clone()
                        near_trade.status='Terminated'
                        self.add(near_trade, ['status'])
                    if terminated_far:
                        far_trade = far_trade.clone()
                        far_trade.status='Terminated'
                        self.add(far_trade, ['status'])
                    self.commitTransaction()
                
            
                    

           
    def TradeAddInfoCopy (self, fromTrade, toTrade):
        aiFromTradeDict = {}
        aiToTradeDict = {}

        #fill aidict for fromTrade... 
        if fromTrade.additional_infos():
            for ai in fromTrade.additional_infos():
                aiFromTradeDict[ai.addinf_specnbr.field_name] = [ai, 0]

        #fill aidict for toTrade...
        if toTrade.additional_infos():
            for ai in toTrade.additional_infos():
                aiToTradeDict[ai.addinf_specnbr.field_name] = [ai, 0]

        # Scan all fromTrade AddInfos...
        for ai in aiFromTradeDict.keys():

            # Existing AddInfo, update...
            for ai2 in aiToTradeDict.keys():
                if ai == ai2 and aiToTradeDict[ai2][1] == 0:
                    for ai2u in toTrade.additional_infos():
                        if ai == ai2u.addinf_specnbr.field_name:
                            ai2u.value = aiFromTradeDict[ai][0].value
                    aiToTradeDict[ai2][1] = 1         #item updated...
                    aiFromTradeDict[ai][1] = 1        #item processed...

            # Non-existing AddInfo, create new...
            if aiFromTradeDict[ai][1] == 0:
                ai2n = ael.AdditionalInfo.new(toTrade)
                ai2n.addinf_specnbr = aiFromTradeDict[ai][0].addinf_specnbr.specnbr
                ai2n.value = aiFromTradeDict[ai][0].value
    
try:
    import FBDPGui
    FBDPParameters = FBDPGui.Parameters('FBDPParameters')
    Testmode = FBDPParameters.Testmode
    Logmode = FBDPParameters.Logmode
    LogToConsole = FBDPParameters.LogToConsole
    LogToFile = FBDPParameters.LogToFile
    Logfile = FBDPParameters.Logfile
except:
    Testmode = 1
    Logmode = 0
    LogToConsole = 1
    LogToFile = 0
    Logfile = 'F273728_log'

ael_variables = [('TestMode', 'TestMode', 'int', [0, 1], Testmode, 0, 0),
                  ('Logmode', 'LogMode', 'int', [0, 1, 2], Logmode, 1, 0),
                  ('LogToConsole', 'Log To Console', 'int', [1, 0], LogToConsole, 1, 0),
                  ('LogToFile', 'Log To File', 'int', [1, 0], LogToFile, 1, 0),
                  ('Logfile', 'Logfile', 'string', None, Logfile, 0, 0)]

def ael_main(args):
    print args
    ScriptName = 'ConvertFXTrades'
    import FBDPString
    reload(FBDPString)
    reload(FBDPRollback)
    reload(FBDPCommon)
    logme = FBDPString.logme
    logme.setLogmeVar(ScriptName,
                      args['Logmode'],
                      args['LogToConsole'],
                      args['LogToFile'],
                      args['Logfile'],
                      0, 
                      0, 
                      0)
    logme(None, 'START')
    ConvertFXTrades(ScriptName,
               args,
               Testmode=args['TestMode'])
