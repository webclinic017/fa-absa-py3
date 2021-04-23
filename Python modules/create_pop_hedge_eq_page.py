import acm

#Script to add instruments to a page to enable them to be picked
#as hedge equivalents.

def add_instrs_to_page(page, ins_names):
    for ins_name in ins_names:
        ins=acm.FInstrument[ins_name]
        if not ins:
            print 'ERROR - Not an ins', ins_name
            continue
        
        if (page.Includes(ins)):
            print 'WARN - ins %s already in page %s' %(ins_name, page.Name())
            continue
        isg = acm.FInstrGroupMap(ins)
        isg.Instrument(ins.Name())
        p_clone=page.Clone()
        p_clone.InstrGroupMaps().Add(isg)
        page.Apply(p_clone)
        page.Commit()
        print 'added %s to page %s' %(ins_name, page.Name())
    
def create_page(page_name):
    new = acm.FPhysInstrGroup()
    new.Name(page_name)
    new.Cid('Instruments')
    new.SuperGroup('FPages')
    new.RecordType('ListNode')
    new.Terminal(True)
    new.Commit()
    print 'page created:', page_name
    return new


def add_hedge_equivalent_instrs_to_page():
    ins_names =['USD/TSY16', 'USD/TSY20', 'USD/TSY17', 'ZAR/R2043', 'ZAR/R2048', 'ZAR/R214',\
                'ZAR/R213', 'ZAR/R210', 'ZAR/R209', 'ZAR/R208', 'ZAR/R207', 'ZAR/R206', 'ZAR/R204',\
                'ZAR/R203', 'ZAR/R2023', 'ZAR/R201', 'ZAR/R197', 'ZAR/R189', 'ZAR/R186', 'ZAR/R157']
    page_name = 'YieldDeltaHedge'

    page = acm.FPhysInstrGroup[page_name]
    if not page:
        page = create_page(page_name)
    add_instrs_to_page(page, ins_names)
    print 'DONE'

add_hedge_equivalent_instrs_to_page()
