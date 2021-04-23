'''
Purpose: NON-scheduled task (that uses a python script)  to book MM trades for a given FX Swap trade
Department : Trading
Desk : Money Market
Requester :  Jogessar, Pavitra: Absa Capital
Developer : Anil Parbhoo
CR Number : 950870
Jira Reference Number : ABITFA:1927
Previous CR Numbers relating to this deployment : 502058

'''









import ael, acm
#==================================================
def findConnectTrdnbr(y):
    
    near_leg_trdnbr = y
    #near_trade = acm.FTrade[near_leg_trdnbr]
    
    for t in acm.FPhysicalPortfolio[acm.FTrade[y].Portfolio().Name()].Trades():
        if t.ValueDay()>= acm.Time().DateToday() and t.Status()!='Void':
            if t.Instrument().InsType()=='Curr':
                if t.ConnectedTrdnbr()==near_leg_trdnbr and t.Oid()<>near_leg_trdnbr:
                    b = t.Oid()
    return b 
    

    
#=================================================





def createDepositTrade(inputCurr, near, far, fixedRate, port, acq, cp, quan):
    today = ael.date_today()
    start = ael.date(near)
    end = ael.date(far)  
    dep = ael.Instrument.new('Deposit')
    curr1  = ael.Instrument[inputCurr] 

    p = ael.Portfolio[port].prfnbr
    a = ael.Party[acq].ptynbr
    c = ael.Party[cp].ptynbr
    
    
    dep.curr = curr1
    dep.generic = 0
    dep.notional = 0
    dep.instype = 'Deposit'
    dep.quote_type = 'Pct of Nominal'
    dep.otc=1
    dep.mtm_from_feed=0
    dep.spot_banking_days_offset = curr1.spot_banking_days_offset
    
    chl = ael.ChoiceList.read('list="ValGroup" and entry="AC_GLOBAL_Funded"')
    dep.product_chlnbr = chl
    dep.contr_size = 1000000.0
    dep.und_instype = 'None'
    dep.settlement = 'None'
    dep.paytype = 'Spot'
    dep.exp_period='3m'
    dep.pay_day_offset=0
    
    pf = ael.ChoiceList.read('list="PriceFindingGroup" and entry="Close"')
    dep.price_finding_chlnbr = pf
    
    l = dep.legs()[0]      
    l.type='Fixed'
    l.payleg=0
    l.daycount_method = curr1.legs()[0].daycount_method
    l.curr=curr1
    l.nominal_factor = 1.0
    l.start_day = start
    l.end_day = end
    l.pay_day_method = 'Following'
    l.pay_calnbr = curr1.legs()[0].pay_calnbr
    l.fixed_rate = fixedRate
    l.rolling_base_day = end
    
    dep.insid = dep.suggest_id()
    try:
        dep.commit()
        t = ael.Trade.new(dep)
        t.insaddr=dep.insaddr
        t.prfnbr = p
        t.acquire_day = start
        t.value_day = start
        t.acquirer_ptynbr=a
        t.curr=curr1
        t.quantity = quan
        t.price = 100.0
        t.premium = -quan * dep.contr_size
        t.status = 'Simulated'
        t.counterparty_ptynbr = c 
        
        ai = ael.AdditionalInfo.new(t)
        ais = ael.AdditionalInfoSpec['Funding Instype']
        ai.addinf_specnbr = ais.specnbr
        if quan >= 0.0:
            ai.value = 'CL Non Zar'
        else:
            ai.value = 'CD Non Zar'
        
        if today>start:
            t.time = start.to_time()
        try:
            t.commit()
            
            ael.log('Trade number for deposit  ' + dep.insid + '  is  ' + str(t.trdnbr))
        
            return
        except:
            ael.log('trade for deposit instrument was not committed')
        
        
        
    except:
        ael.log('instrument for deposit was not committed')
        return
    



#=================================================


acquirer=[]
allParties = acm.FParty.Select('')
for party in allParties:
	if party.Type() == 'Intern Dept':
            acquirer.append(party.Name())


counterparty=[]
for party in allParties:
	if party.Type() in ('Intern Dept', 'Counterparty'):
            counterparty.append(party.Name()) 


portfolio=[]
port = acm.FPhysicalPortfolio.Select('')
for p in port:
    portfolio.append(p.Name())


curr=[]
ins = acm.FCurrency.Select('')
for i in ins:
    curr.append(i.Name()) 
    
    
   

ael_variables = [('FxCashtrdnbr', 'FxCashFxSwapTradeNumber_Data', 'int', None, None, 0, 0, 'FxSwap Trade Number'),

('selectedPortfolio', 'Portfolio_Data', 'string', portfolio, 'Non ZAR Fair Value', 1, 0),
('selectedCounterParty', 'CounterParty_Data', 'string', counterparty, None, 1, 0),
('selectedAcquirer', 'Acquirer_Data', 'string', acquirer, 'Money Market Desk', 1, 0),
('selectedCurr1', 'Curr1_Data', 'string', curr, None, 0, 0, 'LEFT hand currency of currency pair of the FX Cash trade'),
('DepositRateCurr1', 'IntRateCurr1_Data', 'string', None, None, 0, 0, 'Fixed deposit rate for curr 1'),
('selectedCurr2', 'Curr2_Data', 'string', curr, None, 0, 0, 'RIGHT hand currency of currency pair of the FX Cash trade'),
('DepositRateCurr2', 'IntRateCurr2_Data', 'string', None, None, 0, 0, 'Fixed deposit rate for curr 2')
]



def ael_main(dict):

    
    fxtrade = acm.FTrade[dict['FxCashtrdnbr']]
    fxins = fxtrade.Instrument()
    fxinsType = fxins.InsType()
    if fxinsType == 'Curr':        
        if fxtrade.ValueDay() >= acm.Time().DateNow():
            far_leg_trdnbr = findConnectTrdnbr(fxtrade.Oid())
            
            far_leg_trade = acm.FTrade[far_leg_trdnbr]

            
            if fxins.Name() == dict['selectedCurr1']:
               
                createDepositTrade(fxins.Name(), fxtrade.ValueDay(), far_leg_trade.ValueDay(), float(dict['DepositRateCurr1']), dict['selectedPortfolio'], dict['selectedAcquirer'], dict['selectedCounterParty'], round(float(fxtrade.Quantity()/1000000.0), 6))
            
            else:
            
                ael.log('curr 1 trade dont match inputted currency')
                            
            if fxtrade.Currency().Name() == dict['selectedCurr2']: 
          
                createDepositTrade(fxtrade.Currency().Name(), fxtrade.ValueDay(), far_leg_trade.ValueDay(), float(dict['DepositRateCurr2']), dict['selectedPortfolio'], dict['selectedAcquirer'], dict['selectedCounterParty'], round(float(fxtrade.Premium()/1000000.0), 6))
            else:
            
                ael.log('curr 2 of trade dont match inputted currency')
        else:
            ael.log('the value date of the trade inputted has already passed')
   
    else:
        ael.log('the trade number inputted does NOT relate to a FxCash trade. Re-enter different trade number')
    
        
        
