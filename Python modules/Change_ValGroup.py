import ael, sets

# Update the val group of all instruments in a selected trade filter to NewValGroup

def ChangeValGroup(oldVal, newVal, insType, undInsType, includeExpIns):
    
    count = 0
    for vg in ael.ChoiceList['ValGroup'].members():
        if vg.entry == newVal:
            newVG = vg.seqnbr
            break
    
    # Check to see whether we need to include expired instruments or not
    if includeExpIns:
        expiry_day = ael.SMALL_DATE
    else:
        expiry_day = ael.date_today()
    
    # loop through distinct instruments
    if insType in ('BuySellback', 'CFD', 'Convertible', 'Future/Forward', 'Option', 'Repo/Reverse', 'VarianceSwap', 'Warrant'):
        ins_list = sets.Set([i for i in ael.Instrument.select('instype="%s"' %(insType)) \
                if i.product_chlnbr and i.product_chlnbr.entry == oldVal and i.und_insaddr and i.und_instype == undInsType and i.exp_day >= expiry_day]) 
    else:
        ins_list = sets.Set([i for i in ael.Instrument.select('instype="%s"' %(insType)) \
                if i.product_chlnbr and i.product_chlnbr.entry == oldVal and not i.und_insaddr and i.exp_day >= expiry_day])
                
    for i in ins_list:
    	i_clone = i.clone()
    	i_clone.product_chlnbr = newVG
    	
        try:
            i_clone.commit()
            count += 1
        except:
            print 'Error committing instrument %s with ValGroup %s' %(i_clone.insid, i_clone.product_chlnbr.entry)
        
    print count, 'instruments successfully modified'

# Functions to populate the drop down menus defined by ael_variables
def InsTypes():
    # Get a list of instrument types
    ins = [ael.enum_to_string('InsType', e) for e in range(0, 100) if ael.enum_to_string('InsType', e) not in ('None', '?')]
    ins.sort()
    return ins

def ValGroup():
    vg = [c.entry for c in ael.ChoiceList['ValGroup'].members()]
    vg.sort()
    return vg


ael_variables = [('OldValGroup', 'Old Val Group', 'string', ValGroup(), 'SA_XAG', 1),
    	     	('NewValGroup', 'New Val Group', 'string', ValGroup(), 'Government', 1),
                ('insType', 'InsType', 'string', InsTypes(), 'Option', 1),
                ('undInsType', 'Underlying InsType', 'string', InsTypes()),
                ('includeExpIns', 'Include Expired Instruments', 'int', (1, 0), 1, 1)]

def ael_main(ael_dict):

    oldVal = ael_dict["OldValGroup"]
    newVal = ael_dict["NewValGroup"]
    insType = ael_dict["insType"]
    undInsType = ael_dict["undInsType"]
    includeExpIns = ael_dict["includeExpIns"]
    
    print 'Changing %s to %s' %(oldVal, newVal)
    
    ChangeValGroup(oldVal, newVal, insType, undInsType, includeExpIns)
    

