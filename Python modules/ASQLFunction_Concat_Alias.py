import ael
def concat_alias(p,ptynbr,aliastype,*rest):
    list = ''
    alias = ael.Party[ptynbr].aliases()
    if len(alias) > 0:
    	for pa in alias:
	    if pa.type != None:
    	    	if pa.type.alias_type_name == aliastype:
	    	    if list == '':
		    	list = pa.alias
		    else:
		    	list = list + ',' + pa.alias   
    return list

	    
