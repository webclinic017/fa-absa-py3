'''
Once off script to correct the invalid names of Bsb and Repos' that were booked after the upgarde
'''



import ael, acm

def change_to_suggest_name(ins_name):
    ins = ael.Instrument[ins_name]
    
    try:
        print 'before', ins.insid
        ins = ins.clone()
        ins.insid = ins.suggest_id()
        ins.commit()
        print 'after', ins.insid
    except:
        print 'could not change the name for ', ins.insid
    
    
ael_variables = []

def ael_main(dict):

    # BsBs that have invalid names

     
    BsB = "insType = 'BuySellback' and startDate >= '2015-04-28'"

    all_instype = acm.FInstrument.Select(BsB)


    for i in all_instype:
        
        if 'BUSE' in i.Name():
            #print i.Name(), i.StartDate(), i.InsType()
            change_to_suggest_name(i.Name())
