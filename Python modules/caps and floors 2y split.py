'''
Purpose: creat new cap/floor instrument and trades and defin ezero nominal of CF starting after 2y
Department : Trading
Desk : IRD Desk
Requester :  Parin Gokaldas
Developer : Anil Parbhoo
CR Number : 1047867
Jira Reference Number : ABITFA:1729

'''

import acm, PS_Functions

# main functions

cut_off_date = acm.Time().DateAddDelta(acm.Time().DateToday(), 2, 0, 0)


def all_new_ins_names():

    s = "expiryDate > %s"  % acm.Time().DateToday()

    cap_ins = acm.FCap.Select(s)
    floor_ins = acm.FFloor.Select(s)

    new_cap_floor_ins = []


    for c in cap_ins:
        if '_2y' in c.Name():
            new_cap_floor_ins.append(c.Name())
            
    for f in floor_ins:
        if '_2y' in f.Name():
            new_cap_floor_ins.append(f.Name())
            
    return new_cap_floor_ins

def newInstrument(trade):
    i = trade.Instrument()
    new_ins_name = i.Name() + '_2y'
    if acm.FInstrument[new_ins_name]:
        acm.Log('the NEW instrument %s already exists for existing trade %s ' % (new_ins_name, trade.Oid()))
    else:
        ins = i.Clone()
        ins.Name(new_ins_name) 
        ins.ExternalId1('')
        ins.ExternalId2('')
        ins.Isin('')

        
        ins.Commit()
        acm.Log('Created ins =  %s' %(ins.Name()))
        
        
        legs = ins.Legs()
        for l in legs:
            cfs = l.CashFlows()
            for cf in cfs:
                
                PS_Functions.SetAdditionalInfo(cf, 'Org_nominal_factor', cf.NominalFactor())
                    
                            
        
            

def nominal_factor_adjustment(cf):
    
    ccf = cf.Clone()
    if cf.StartDate()<=cut_off_date:
        ccf.NominalFactor(cf.add_info('Org_nominal_factor'))
    else:
        ccf.NominalFactor(0.00) 
    cf.Apply(ccf)
    cf.Commit()


def ReversePayments(trade):

    for payment in trade.Payments():
        payment.Amount(payment.Amount()*-1)
        payment.Commit()
        


def offsetting_corresponding_Trade(trade):

    i = trade.Instrument()
    new_ins_name = i.Name() + '_2y' # based on an existing instrument name of a trade + _2y

    
    existing_ins = acm.FInstrument[new_ins_name]
    
    
    #Create offsetting trade ot - that is equal and opposite to existing trade
        
    ot = trade.Clone() 
    ot.MirrorTrade = None
    ot.Instrument(existing_ins) 
    ot.Quantity(trade.Quantity()*-1) 
    ot.Premium(trade.Premium()*-1)
    ot.Counterparty('NLD DESK')
    ot.OptionalKey('')
    ot.Status('FO Confirmed')
    ot.Text1('Offsetting Trade')
    ot.Text2(trade.Oid())
    ot.ContractTrdnbr(trade.Oid())
    ot.TrxTrade(trade.Oid())
   
    ot.Commit()
    acm.Log('for existing trade %s the trade number of Offsetting Trade =  %s' %(trade.Oid(), ot.Oid()))
    ReversePayments(ot)
    
    #Create corresponding trade ct - that is same as existing trade

    pd={'NLDO':'NLDO_SE', 'Swap Risk':'Swap_Risk_SE'}

    ct = ot.Clone()
    #ct.MirrorTrade = None
    
    changePort = acm.FPhysicalPortfolio[pd[ot.Portfolio().Name()]]
    ct.Instrument(existing_ins)
    ct.Quantity(ot.Quantity()*-1) 
    ct.Premium(ot.Premium()*-1)
    ct.Counterparty('NLD DESK')
    ct.Text1('Corresponding Trade')
    ct.Text2(trade.Oid())
    ct.Portfolio = changePort #define a portfolio for the new offsetting trade
    ct.OptionalKey('')
    ct.Status('FO Confirmed')
    ct.ContractTrdnbr(ot.Oid())
    ct.TrxTrade(ot.Oid())
   
    ct.Commit()
    acm.Log('for existing trade %s the trade number of Corresponding Trade =  %s' %(trade.Oid(), ct.Oid()))
    ReversePayments(ct)

# set up task 

ael_variables = [
['newIns_Trades', 'Create New Ins Trades and set Nominal Factor_General', 'string', ['No', 'Yes'], 'Yes', 0, 0, 'Create New Instruments, Offsetting and Corresponding Trades', None, 1],
['selectedSimulatedStatus', 'Rollback - Set ALL New trades to Simulate Status_RollBack', 'string', ['No', 'Yes'], 'No', 0, 0, 'newly created trades set to simulate by system user', None, 1]
]




def ael_main(dict):
    if dict['newIns_Trades'] == 'Yes':
    
    
        
        new_ins_set = tuple(all_new_ins_names()) #create a tuple of new ins names
        
        tf = acm.FTradeSelection['Used to book new caps floors']

        existing_trades = tuple(tf.Trades())# create a tuple of existing trades 

        # loop through the existing trades 
        for et in existing_trades:
            
            new_ins_name = et.Instrument().Name()+'_2y'
            
            if new_ins_name in new_ins_set:
                ins = acm.FInstrument[new_ins_name]
                new_trds = ins.Trades()
                
                if len(new_trds) == 0:
                    offsetting_corresponding_Trade(et)
                else:
                    count_new_trdnbrs=[]
                    
                    
                    for nt in new_trds:
                         
                        if nt.Text2()==str(et.Oid()) and nt.Text1() == 'Offsetting Trade' and nt.Status()!='Simulated' :
                            #print 'Offsetting trade %s does exists for existing trade %s' % (nt.Oid(),et.Oid())
                            count_new_trdnbrs.append(nt.Oid())
                            
                        elif nt.Text2()==str(et.Oid()) and nt.Text1() == 'Corresponding Trade' and nt.Status()!='Simulated':
                            #print 'Corresponding trade %s does exists for existing trade %s' % (nt.Oid(),et.Oid())
                            count_new_trdnbrs.append(nt.Oid())
                    
                    
                    if len(count_new_trdnbrs) == 0:
                        offsetting_corresponding_Trade(et)
                    elif len(count_new_trdnbrs) == 1:
                        acm.Log('!!! Recon Problem - Existing trade %s only has ONE of an offsetting and a corresponsing trade' % et.Oid())
                    #elif len(count_new_trdnbrs) == 2:
                        #acm.Log('Existing trade %s has both offsetting and a corresponsing trade' % et.Oid())
                    
                    
                        
            else:
                newInstrument(et)
                offsetting_corresponding_Trade(et)
                
        new_ins_set_after_creation = tuple(all_new_ins_names()) #create a tuple of new ins names after all the neccessary ins have been created       
        for i in new_ins_set_after_creation:
            new_ins = acm.FInstrument[i]
            legs = new_ins.Legs()
            for l in legs:
                all_cfs = l.CashFlows()
                for scf in all_cfs:
                    nominal_factor_adjustment(scf)

        acm.Log('Completed Successfully')        
    if dict['selectedSimulatedStatus'] == 'Yes':

        #Rollback - Set all newly created trades set to simulate. Task to be run by user ATS as a once off after stopping further scheduling of the usual task   
        new_ins_set_current = tuple(all_new_ins_names()) #create a tuple of new ins names the trades of which can be simulated
        
        for i in new_ins_set_current:
            ins = acm.FInstrument[i]
            new_trds = ins.Trades()
            for t in new_trds:
                clone_trade = t.Clone()
                clone_trade.Status('Simulated')
                t.Apply(clone_trade)
                t.Commit()
                
        
        acm.Log('all trades to the new instruments have been set to simulated status')        
    
    

