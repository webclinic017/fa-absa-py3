""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/confirmation/etc/upgrade/FConfirmationUpgradeDeleteEvent.py"
import acm
import FOperationsUtils as Utils


def DeleteDeprecatedEvents():
    query = acm.CreateFASQLQuery(acm.FChoiceList, 'AND')
    query.AddAttrNode('List', 'EQUAL', 'Event')
    
    orNode = query.AddOpNode('OR')
    orNode.AddAttrNode('Name', 'EQUAL', 'Resend')
    orNode.AddAttrNode('Name', 'EQUAL', 'Amendment')
    orNode.AddAttrNode('Name', 'EQUAL', 'Cancellation')
    orNode.AddAttrNode('Name', 'EQUAL', 'Chaser')
    
    choiceLists = query.Select()
    
    Utils.Log(True, 'Deleting deprecated choice lists ...')
    counter = 0
    name = ''
    for choiceList in choiceLists:
        try:
            name = choiceList.Name()
            choiceList.Delete()
            Utils.Log(True, 'Deleted choice list %s.' % name)
            counter += 1
        except Exception as error:
            Utils.Log(True, 'Error when deleted choice list %s: %s' % (name, error))
            
    Utils.Log(True, 'Deletion of deprecated choice lists complete. Deleted %d choice lists.' % counter)