"""-----------------------------------------------------------------------------
PURPOSE                 :  Re assign instruments with wrong choice list entry and 
                            delete the duplicate choice list entry
DEPATMENT AND DESK      :  
REQUESTER               :  Backend Error driven
DEVELOPER               :  Edmundo Chissungo
CR NUMBER               :  CHNG0002814660
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date       Change no Developer                 Description
--------------------------------------------------------------------------------
"""

import acm

errors=[]

choiceList = acm.FChoiceList.Select('name="AC_GLOBAL_Basis"')
ChoiceListToDelete =0
CorrectChoiceList =0

if len(choiceList) > 1:
    if choiceList[0].List() == 'valgroup':
        ChoiceListToDelete = choiceList[0].Oid()
        CorrectChoiceList  = choiceList[1].Oid()
    else:
        ChoiceListToDelete = choiceList[1].Oid()
        CorrectChoiceList  = choiceList[0].Oid()


ael_variables=[['ToBeDeleted', 'ChoiceListToDelete', 'int', None,\
                ChoiceListToDelete, 1, 0, 'Duplicate choice list.'],
                ['ToBeClone', 'CorrectChoiceList', 'int', None, \
                CorrectChoiceList, 1, 0, 'Intruments assigned to this.'],
                ['RollBack', 'RollBack', 'bool', None, False, 1, 0,\
                    'Is roll back required now?']]


def Repoint_Ins_Choicelist(seqnbr_to_be_deleted, correct_sqnbr):
    """we want all the intruments with this choice list item selected
    the ael Instrument column product_chlnbr holds that detail
    this maps to the acm valuationGrpChlItem column name"""

    roll_back_list= []
    ins = acm.FInstrument.Select('valuationGrpChlItem=%i' % seqnbr_to_be_deleted)
    print 'Selected instruments: %d' %len(ins)
    if len(ins) >0:
        for i in list(ins):
            if not i.ValuationGrpChlItem():
                continue
            try:
                i.ValuationGrpChlItem(correct_sqnbr)
                i.Commit()
                roll_back_list.append(i.Name())
                print i.Name()
            except Exception as ex:
                i.Undo()
                errors.append("Couldn't update repoint instrument %s to appropriate \
                    choice list. %s" % (i, str(ex)))
                raise
    return roll_back_list


def Delete_Choicelist(seqnbr_to_be_deleted):
    """ Delete the selected choice list entry"""
    try:
        cl = acm.FChoiceList[seqnbr_to_be_deleted]
        if cl:
            cl.Delete()
    except Exception as ex:
        cl.Undo()
        errors.append("Couldn't delete choice list %s. %s"% (cl.List(),  str(ex)))
        raise


def Roll_Back(seqnbr_to_be_cloned):
    """ this will roll back the choice list entry deletion """
    try:
        cl = acm.FChoiceList[seqnbr_to_be_cloned] # AC_BLOBAL_Basis -> ValGroup
        if cl:
            new_list_entry = acm.FChoiceList()
            new_list_entry.List("valgroup")
            new_list_entry.Name(cl.Name())
            new_list_entry.Commit()
    except Exception as ex:
        new_list_entry.Undo()
        errors.append("Couldn't create new choice list entry %s. %s"% (cl.List(),  str(ex)))
        raise
    seqnbr = new_list_entry.Oid()
    return seqnbr


def ael_main(parameters):
    print 'started in main'

    seqnbr_to_be_deleted = parameters['ToBeDeleted']
    correct_sqnbr = parameters['ToBeClone']
    rb = parameters['RollBack']

    if rb:
        Roll_Back(correct_sqnbr)
        print "rolled_back"
    else:
        Repoint_Ins_Choicelist(seqnbr_to_be_deleted, correct_sqnbr)
        Delete_Choicelist(seqnbr_to_be_deleted)

    try:
        if not errors:
            print "Completed successfully"
        else:
            print "="*50
            print "Errors:"
            print "\n" + "\n".join(errors)
            print "="*50
    except Exception, ex:
        print str(ex)

