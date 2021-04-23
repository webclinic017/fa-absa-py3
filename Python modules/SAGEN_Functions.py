import ael
def set_party_add_info(party, add_info, value):
    """Set party's specified additional info to supplied value.
        
    party   	- ael Party entity  - Party that additional info refers to
    add_info	- string    	    - Name of add info field
    value   	- string    	    - Value to set add info field to

    Returns 1 if successful, else 0
    """

    try:
        
	existing_addinfos = {}

	for ai in party.additional_infos():

    	    existing_addinfos[ai.addinf_specnbr.field_name] = ai
    	
	if existing_addinfos.has_key(add_info):

	    clone = existing_addinfos[add_info].clone()
	    clone.value = str(value)
	    clone.commit()
    	    
	else:
    	    
	    ai_spec = ael.AdditionalInfoSpec[add_info].clone()
    	    
	    new = ael.AdditionalInfo.new(ai_spec)
    	    print(new.pp())
	    new.addinf_specnbr = ael.AdditionalInfoSpec[add_info].specnbr
	    new.value = value
	    new.recaddr = party.ptynbr
	    new.commit()    
	
	return 1
    
    except:
    
    	return 0

def set_trade_addinf(trade, add_info, value,*rest):
    existing_addinfos = {}

    for ai in trade.additional_infos():

    	existing_addinfos[ai.addinf_specnbr.field_name] = ai
    	
    if existing_addinfos.has_key(add_info):

    	clone = existing_addinfos[add_info].clone()
	clone.value = (str)(value)
	clone.commit()
    	    
    else:
    	print(value)
    	ai_spec = ael.AdditionalInfoSpec[add_info].clone()
    	trd = trade.clone()
    	new = ael.AdditionalInfo.new(trd)
    	new.addinf_specnbr = ai_spec
    	new.value = str(value)
    	new.commit()
