'''-----------------------------------------------------------------------
MODULE
    MarkitWire_Listener

DESCRIPTION
    
    Date                : 2010-06-24, 2010-06-28, 2010-07-05, 2010-07-07, 2010-07-16, 2010-08-03, 2010-08-12, 2010-09-01, 2010-10-19, 2011-03-24, 2012-04-20
    Purpose             : MarketWire Listener to update trades
                          Amendment to check for start and end days according to business days' convention
                          The adaptor will capture broker fees on the face of the trade - this needed to be added to 
                            additional payments and payable a month after trade date
                          The adaptor is sending back full trade messages including the broker fee which we moved to add payments, back on the face of
                            the trade - change to check if we already have it then remove it
                          The broker name needs to remain on the face of the trade - if it is removed however, then we end up in a loop by picking up our
                            own listener updates which causes screen to flicker.  We now get an add_info set when the adaptor sends an update, which is 
                            when we will process, we then clear the flag so we dont call the listener recursively.
                          Termination fees sent in via the adaptor need to be adjusted to banking day
                          FIRSTRAND bank subaccounts will be fed in from MW via add info field Source Cpty Name.  If this field is present then the counterparty
                            on the face of the trade needs to be updated with the relevant FirstRand subaccount entity.
                          Amendment to use the currency of the instrument for the broker fee
                          IMM daycount does not apply mod following thereafter due to bug in FA core code.  In the case of IMM, call mod following thereafter
                          Adaptor now tags first reset and cashflow - listener updated to remove this step from being performed
                          Change required for Prime Services bookings between the prime desk and the other internal desk to show as a mirror
                          Missed the check on the Prime Services bookings to ensure that both trades are in BOBO before linking via mirror
                          Added Reset.day to set of fields which need to be corrected for IMM day method.
                          Trades sent from MarkitWire filter to CSA_ValGroup Module
    Department and Desk : Front Office IRD Desk / MO / PCG / PCG
    Requester           : Nick Manterfield / Miguel da Silva
    Developer           : Anwar Banoo, Willie van der Bank, Nidheesh Sharma
    CR Number           : 352371, 355403, 362277, 365019, 378221, 394313, 400769, 419941, 467920, 608195, 792929, 813466, 871395, 157393

ENDDESCRIPTION
-----------------------------------------------------------------------'''

import ael
from CSA_ValGroup import CSA_ValGroup_Trades

PROD = True
MW_TF = 'MarkitWire_Listener'
ADDINFONAME = 'MW_TradeUpdated'
ADDINFO_SUBACCOUNTNAME = 'Source Ctpy Name'
ADDINFO_MARKITWIRE = 'CCPmiddleware_id'
HACKED_COUNTERPARTY = 'FIRSTRAND '
HACKED_SWIFT_PROD = 'FIRNZAJJ'
HACKED_SWIFT_UAT = 'MEGA1234'
IMM_OVERRIDE = 'Mod. Following'
PRIMEBROKER_ID = 32737

def processEntry(ins): 
    curr = ins.curr
    currentEarliest = None
    for leg in ins.legs():
        
        for reset in leg.resets():            
            if currentEarliest:
                if reset.start_day < currentEarliest.start_day:
                    currentEarliest = reset
            else:
                currentEarliest = reset
                
    try:        
        clone_Reset = currentEarliest.clone()
        clone_Reset.extern_id = ins.extern_id2
        clone_Reset.commit()

        try:
            clone_Cashflow = currentEarliest.cfwnbr.clone()
            clone_Cashflow.extern_id = ins.extern_id2
            clone_Cashflow.commit()
        except Exception, e:
            print 'Error updating cashflow with external id:', e
        
    except Exception, e:
        print 'Error updating reset with external id:', e
        
def correctIMM_DateIssue(reset):
    leg = reset.legnbr
    ins = leg.insaddr     
   
    print reset.legnbr.pay_day_method, reset.legnbr.reset_day_method
    
    if (reset.legnbr.reset_day_method == 'IMM'):        
        clone_Reset = reset.clone()                    
        clone_Reset.end_day = clone_Reset.end_day.adjust_to_banking_day(ins.curr, leg.reset_day_method)
        clone_Reset.end_day = clone_Reset.end_day.adjust_to_banking_day(ins.curr, IMM_OVERRIDE)
        clone_Reset.start_day = clone_Reset.start_day.adjust_to_banking_day(ins.curr, leg.reset_day_method)
        clone_Reset.start_day = clone_Reset.start_day.adjust_to_banking_day(ins.curr, IMM_OVERRIDE)
        clone_Reset.day = clone_Reset.day.adjust_to_banking_day(ins.curr, leg.reset_day_method)
        clone_Reset.day = clone_Reset.day.adjust_to_banking_day(ins.curr, IMM_OVERRIDE)
        clone_Reset.commit()
        
    if (reset.legnbr.pay_day_method == 'IMM'):                
        clone_Cashflow = reset.cfwnbr.clone()
        clone_Cashflow.end_day = clone_Cashflow.end_day.adjust_to_banking_day(ins.curr, leg.reset_day_method)
        clone_Cashflow.end_day = clone_Cashflow.end_day.adjust_to_banking_day(ins.curr, IMM_OVERRIDE)
        clone_Cashflow.start_day = clone_Cashflow.start_day.adjust_to_banking_day(ins.curr, leg.reset_day_method)
        clone_Cashflow.start_day = clone_Cashflow.start_day.adjust_to_banking_day(ins.curr, IMM_OVERRIDE)
        clone_Cashflow.pay_day = clone_Cashflow.pay_day.adjust_to_banking_day(ins.curr, leg.reset_day_method)
        clone_Cashflow.pay_day = clone_Cashflow.pay_day.adjust_to_banking_day(ins.curr, IMM_OVERRIDE)                
        
        clone_Cashflow.commit()


def changeInstrumentBankingDay(ins):
    try:
        for leg in ins.legs():            
            #new_date = ins.exp_day.adjust_to_banking_day(ins.curr, leg.reset_day_method)  
            #if new_date != ins.exp_day:            
            if leg.type != 'Fixed':
                currentLatest = None
                currentEarliest = None
                
                for reset in leg.resets():
                    correctIMM_DateIssue(reset)
                    
                    if currentLatest:
                        if reset.end_day > currentLatest.end_day:
                            currentLatest = reset
                    else:
                        currentLatest = reset 
                        
                    if currentEarliest:
                        if reset.start_day < currentEarliest.start_day:
                            currentEarliest = reset
                    else:
                        currentEarliest = reset 
    
                if leg.reset_day_method != 'IMM':
                    try:
                        clone_Reset = currentLatest.clone()                    
                        clone_Reset.end_day = clone_Reset.end_day.adjust_to_banking_day(ins.curr, leg.reset_day_method)
                        
                        clone_Cashflow = currentLatest.cfwnbr.clone()
                        clone_Cashflow.end_day = clone_Cashflow.end_day.adjust_to_banking_day(ins.curr, leg.reset_day_method)
                                
                        clone_Reset.commit()
                        clone_Cashflow.commit()
                                                                              
                    except Exception, errMsg:
                        print 'Exception in setting end reset values:', errMsg
                        
                    try:
                        clone_Reset = currentEarliest.clone()
                        clone_Reset.start_day = clone_Reset.start_day.adjust_to_banking_day(ins.curr, leg.reset_day_method)

                        clone_Cashflow = currentEarliest.cfwnbr.clone()
                        clone_Cashflow.start_day = clone_Cashflow.start_day.adjust_to_banking_day(ins.curr, leg.reset_day_method)
                                
                        clone_Reset.commit()
                        clone_Cashflow.commit()
                                                                              
                    except Exception, errMsg:
                        print 'Exception in setting start reset values:', errMsg
                    
            else:
                currentLatest = None
                currentEarliest = None
                for cashflow in leg.cash_flows():
                    if currentLatest:
                        if cashflow.end_day > currentLatest.end_day:
                            currentLatest = cashflow
                    else:
                        currentLatest = cashflow
                            
                    if currentEarliest:
                        if cashflow.start_day < currentEarliest.start_day:
                            currentEarliest = cashflow
                    else:
                        currentEarliest = cashflow
                try:
                    clone_Cashflow = currentLatest.clone()
                    clone_Cashflow.end_day = clone_Cashflow.end_day.adjust_to_banking_day(ins.curr, leg.reset_day_method)
                    clone_Cashflow.commit()
                except Exception, errMsg:
                    print 'Exception in setting end cashflow values:', errMsg
                    
                try:
                    clone_Cashflow = currentEarliest.clone()
                    clone_Cashflow.start_day = clone_Cashflow.start_day.adjust_to_banking_day(ins.curr, leg.reset_day_method)                    
                    clone_Cashflow.commit()
                except Exception, errMsg:
                    print 'Exception in setting start cashflow values:', errMsg
                    
            try:            
                clone_leg = leg.clone()
                clone_leg.end_day = clone_leg.end_day.adjust_to_banking_day(ins.curr, leg.reset_day_method)
                clone_leg.start_day = clone_leg.start_day.adjust_to_banking_day(ins.curr, leg.reset_day_method)
                if leg.reset_day_method == 'IMM':
                    clone_leg.end_day = clone_leg.end_day.adjust_to_banking_day(ins.curr, IMM_OVERRIDE)
                    clone_leg.start_day = clone_leg.start_day.adjust_to_banking_day(ins.curr, IMM_OVERRIDE)

                clone_leg.commit()
            except Exception, errMsg:
                print 'Exception setting leg start and end:', errMsg

        try:
            i_clone = ins.clone()
            i_clone.exp_day = i_clone.exp_day.adjust_to_banking_day(ins.curr, leg.reset_day_method)
            if leg.reset_day_method == 'IMM':
                i_clone.exp_day = i_clone.exp_day.adjust_to_banking_day(ins.curr, IMM_OVERRIDE)
            i_clone.commit()
        except Exception, errMsg:
            print 'Exception setting instrument end:', errMsg

        '''
        try:
            i_clone = ins.clone()
            i_clone.start_day = i_clone.start_day.adjust_to_banking_day(ins.curr, leg.reset_day_method)
            i_clone.commit()
        except Exception, errMsg:
            print 'Exception setting instrument start:', errMsg
        '''    
    except Exception, errMsg:
        print 'Exception:', errMsg
        
def processBrokerFee(trade):
    t_c = trade.clone()

    fee = t_c.fee
    
    broker = None
    if t_c.broker_ptynbr:
        broker = t_c.broker_ptynbr.ptynbr
    
    t_c.fee = 0
    #2010-07-16 anwar amended next line not to remove the broker from the face of the trade - we only act on this as a result of MW adaptor setting 
    #       an add_info value to tell us it has sent an update.
    #t_c.broker_ptynbr = None
    
    for payment in t_c.payments():
        print payment.type
        if (payment.type == 'Broker Fee'):
            payment.delete()
        elif (payment.type == 'Termination Fee'):
            payment.payday = payment.payday.adjust_to_banking_day(payment.curr, t_c.insaddr.legs()[0].reset_day_method)

    if fee:
        d1 = ael.date_today().add_months(1).to_ymd()
        if len(str(d1[1])) == 1: 
            payDay = ael.date(str(d1[0]) +'-0'+ str(d1[1]) + '-' + str(10)).adjust_to_banking_day(ael.Instrument['ZAR']) 
        else:
            payDay = ael.date(str(d1[0]) +'-'+ str(d1[1]) + '-' + str(10)).adjust_to_banking_day(ael.Instrument['ZAR'])     
    
        newPayment = ael.Payment.new(t_c)

        newPayment.ptynbr          = broker
        newPayment.type            = 'Broker Fee'
        newPayment.payday          = payDay
        newPayment.amount          = fee
        newPayment.curr            = t_c.insaddr.curr
        # 2010-09-01 'ZAR'

    addInfo = trade.add_info(ADDINFO_SUBACCOUNTNAME)
    if addInfo:
        if t_c.counterparty_ptynbr:
            checkBIC = HACKED_SWIFT_PROD
            for item in ael.ServerData.select():
                if item.customer_name != 'Production':
                    checkBIC = HACKED_SWIFT_UAT
            
            if (t_c.counterparty_ptynbr.swift == checkBIC):
                import acm
                selectQuery = "name like '%s*%s'" % (HACKED_COUNTERPARTY, addInfo)
                party = acm.FCounterParty.Select(selectQuery).AsSet()
                party.Union(acm.FClient.Select(selectQuery))
                if party:
                    t_c.counterparty_ptynbr = party[0].Oid()

    t_c.commit()            

def clearAdaptorUpdateFlag(trdnbr):
    aisp = ael.AdditionalInfoSpec[ADDINFONAME]
    if aisp:
        aiList = ael.AdditionalInfo.select('addinf_specnbr = %i' %aisp.specnbr)    
        myTrade = [ai for ai in aiList if ai.recaddr == trdnbr]
        for ai in myTrade:
            aic = ai.clone()
            aic.value = 'No'
            aic.commit()
        ael.poll()

def generateQuery(AcquirerId, MWTradeNumber, CounterpartyId):
    import acm
    print AcquirerId, MWTradeNumber, CounterpartyId
    query = acm.CreateFASQLQuery('FTrade', 'AND')
    query.AddAttrNode('Status', 'EQUAL', acm.EnumFromString('TradeStatus', 'BO-BO Confirmed'))
    query.AddAttrNode('Acquirer.Oid', 'EQUAL', AcquirerId)
    query.AddAttrNode('Counterparty.Oid', 'EQUAL', CounterpartyId)
    query.AddAttrNode('OptionalKey', 'RE_LIKE_NOCASE', '*%s*' %MWTradeNumber)
    
    trades = query.Select()
    if trades.Size() != 1:
        if trades.Size() > 1:
            print 'Error retrieving mirror trade, more than one matching trade exists'
        else:
            print 'No matching mirror trade exists'
        return None
    return trades.First().Oid()
    
def updatePrimeMirror(tradeRef, mirrorRef):
    if mirrorRef and tradeRef:
        print mirrorRef, tradeRef
        t_c = ael.Trade[tradeRef].clone()
        t_c.mirror_trdnbr = mirrorRef
        t_c.commit()
        
        t_c = ael.Trade[mirrorRef].clone()
        t_c.mirror_trdnbr = tradeRef
        t_c.commit()
        print 'Trade %i and Mirror Trade %i updated.' %(tradeRef, mirrorRef)

def actionPrimeMirror(trade):
    import acm
    print 'Processing trade %i...' %trade.trdnbr
    if (trade.counterparty_ptynbr.type == 'Intern Dept') and (trade.acquirer_ptynbr.type == 'Intern Dept') and (trade.status == 'BO-BO Confirmed'):
        MWTradeNumber = trade.add_info(ADDINFO_MARKITWIRE)[0:10]
        
        #desk acquirer - need to find the prime trade for its id
        if (trade.counterparty_ptynbr.ptynbr == PRIMEBROKER_ID):
            trd = generateQuery(PRIMEBROKER_ID, MWTradeNumber, trade.acquirer_ptynbr.ptynbr)
            updatePrimeMirror(trade.trdnbr, trd)
            
        #prime acquirer - need to find the desk trade to flag the id
        if (trade.acquirer_ptynbr.ptynbr == PRIMEBROKER_ID):
            trd = generateQuery(trade.counterparty_ptynbr.ptynbr, MWTradeNumber, PRIMEBROKER_ID)
            updatePrimeMirror(trd, trade.trdnbr)
    

def listener(o, e, arg, op):
    if e.record_type == 'Trade' and op != 'delete':
        #2010-07-16 anwar amended next line not to remove the broker from the face of the trade - we only act on this as a result of MW adaptor setting 
        #       an add_info value to tell us it has sent an update.    
        if e.add_info(ADDINFONAME) == 'Yes':
            print 'Most of this code has been removed for now - Arthur Grace'
            #clearAdaptorUpdateFlag(e.trdnbr)
            #CSA_ValGroup_Trades(o,e,arg,op)
            #actionPrimeMirror(e)
            #adaptor will now be responsible for tracking the external id on the cashflows
            #processEntry(e.insaddr)        
            #changeInstrumentBankingDay(e.insaddr)
            processBrokerFee(e)
            #added by Nidheesh Sharma - Sends trades from MarkitWire filter to CSA_ValGroup Module
            
#Listener start function. Backend needs to call this function each morning.
def start():    
    ael.TradeFilter[MW_TF].trades().subscribe(listener)
    print 'Listener started...'

#Listener stop function. Backend needs to call this function each evening.
def stop():
    ael.TradeFilter[MW_TF].trades().unsubscribe(listener)
    print 'Listener stopped.'
    
#start()
#stop()
