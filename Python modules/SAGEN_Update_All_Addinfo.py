import ael, string


def UpdateAll(temp, obj, addinf_name, oldvalue, newvalue, *rest):
    flag = 'yes'
    o_clone = obj.clone()
    ais = obj.additional_infos()
    for ai in ais:
    	if ai.addinf_specnbr.field_name == addinf_name:
    	    if (ai.value == oldvalue and ai.value != newvalue):
    	    	flag = 'yes'
		break
	    else:
		flag = 'no'

    if flag == 'yes':
    	addinf = ael.AdditionalInfo.new(t_clone)
    	addinf.addinf_specnbr = ael.AdditionalInfoSpec[addinf_name]
    	addinf.value = newvalue
    	try:
            addinf.commit()
	    obj_clone.commit()
	    print('Object ', obj.record_type, ' addinfo commited\n')
	    return 'Success'
	except:
	    print('Error committing object ', obj.record_type)
	    return 'Fail'
	    
    return 'Unchanged'
	    



