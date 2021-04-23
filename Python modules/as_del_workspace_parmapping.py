import ael


def del_pm(temp, nbr, *rest):
    
    #print dir(ael)
    
    
    pm = ael.ParameterMapping[nbr]
    #print pm.workspace_name
    #pm.delete()
    
    #for i in pm.par_mapping_instances():
    #    print i.pp()
    #    i.delete()
    '''
    #pm.delete()
    
    
    '''
        
    #pmi = ael.ParMappingInstance[nbr]
    #print pmi.pp()
    #pmi.delete()
    #print pmi.parameter_type, pmi.connect_name 
    
    #pm.delete()

    return 'success'




print(del_pm(1, 49))





