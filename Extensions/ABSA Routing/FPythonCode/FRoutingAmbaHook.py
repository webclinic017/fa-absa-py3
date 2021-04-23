import acm
from FRoutingUtils import is_member_of_or_same_as
from FRoutingUtils import fetch_receivers

sourcePortfolio = acm.Routing.SourcePortfolio()
receivers = fetch_receivers()
roundRobinCounter = 0
'''================================================================================================
================================================================================================'''
def default_receiver_selection(mbfObject, fObject, receivers):
    global roundRobinCounter
    idx = roundRobinCounter % len(receivers)
    roundRobinCounter += 1
    return receivers[idx]
'''================================================================================================
================================================================================================'''
def subject_for_receiver(oldSubject, receiver):
    if len(receivers) > 1:
        return '%s/%s' % (oldSubject, receiver)
    else:
        return oldSubject
'''================================================================================================
================================================================================================'''
def do_sender_modify(mbfObject, subject, receiverSelectionFunction):
    retval = None
    try:
        mbfString = mbfObject.mbf_object_to_string()
        fObject = acm.AMBAMessage.CreateCloneFromMessage(mbfString)
        if fObject:
            if fObject.IsKindOf(acm.FTrade) and fObject.Instrument().InsType() in ['Curr', 'FXOptionDatedFwd']:
                if is_member_of_or_same_as(fObject.Portfolio(), sourcePortfolio):
                    receiver = receiverSelectionFunction(mbfObject, fObject, receivers)
                    newSubject = subject_for_receiver(subject, receiver)
                    retval = mbfObject, newSubject

            elif fObject.IsKindOf(acm.FRoutingRedirection):
                receiver = receiverSelectionFunction(mbfObject, fObject, receivers)
                newSubject = subject_for_receiver(subject, receiver)
                retval = mbfObject, newSubject

            else:
                message = mbfObject.mbf_object_to_string()
                print 'Cannot handle message (make sure the AMBA is configured to only subscribe to Trade and RoutingRedirection records): %s' % message
                retval = None
        
    except Exception, e:
        print e
        retval = None
    
    return retval
'''================================================================================================
================================================================================================'''
def sender_modify(mbfObject, subject):   
    return do_sender_modify(mbfObject, subject, default_receiver_selection)
'''================================================================================================
================================================================================================'''





