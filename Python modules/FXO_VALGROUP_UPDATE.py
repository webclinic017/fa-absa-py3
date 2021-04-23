import ael, acm


new_val = acm.FChoiceList[2177]
           
def set_valgroup(ins_list):
    for ins in ins_list:
        if ins.ValuationGrpChlItem() != new_val:
            ins.ValuationGrpChlItem(new_val)
            try:
                ins.Commit()
            except:
                print 'Failed on ', ins.Name()
                
def TrdFilter():

    TrdFilter=[]
    
    for t in acm.FTradeSelection.Select(''):
        TrdFilter.append(t.Name())
    TrdFilter.sort()
    return TrdFilter

ael_variables = [ 
                 ('TrdFilter', 'Trade Filter', 'string', TrdFilter(), '', 1)
                 ] 
                 
    
def ael_main(ael_dict):
    try:
        tf = acm.FTradeSelection[(ael_dict["TrdFilter"])]
        set_valgroup(tf.Instruments())
        print 'All instruments updated'
    except:
        print 'Invalid trade filter'
