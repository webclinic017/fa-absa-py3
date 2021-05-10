"""----------------------------------------------------------------------------
MODULE:
    FMTHooks

DESCRIPTION:
    OPEN EXTENSION MODULE
    This module provides extension points for user customization at the entry
    point of the message processing, to allow for detailed filtering and even
    modification of the incoming message, and at the two points before and after
    the pairing and the matching functionality

FUNCTIONS:
    on_entry(mt_object):
        a) Provision to override the FParameters FMTnnn_Config
        b) Option to ignore certain MT message types.
        Since the available object is the incoming MT message, it is possible
        to do direct Swift attribute controls and checks.
        Returns the resulting mt_object.

    message_entry_hook(swift_data):
        Provision to override the swift data before any processing takes place.
        Returns swift message object in swift message format.

    pre_pair(mt_object):
        method to override the default pairing logic to identify an object in
        the database. Input is the corresponding MT class object which has
        various access methods to allow the user to write the logic.
        If you do not want any further (default) pairing logic after the
        pre_pair (you have established that there is no suitable pair) you can
        raise an exception, and the processing will be stopped, and the BPR will
        land in the Unpaired state.
        Returns the resulting mt_object.

    post_pair(mt_object, paired_objects):
        Method to enhance the default pairing logic.
        Input is the MT class object and paired confirmations/settlements if found.
        User can add additional checks or adjustments here, for example logic
        to choose when more than one object is paired.
        Returns the resulting mt_object

    pre_match(their_mt_object, our_mt_object):
        User specific logic to be performed just before the matching functionality.
        Return a tuple with possibly modified their_mt_object and our_mt_object.

    post_match(their_mt_object, our_mt_object, cmp_success, cmp_result):
        User specific logic for adding functionality post matching.
        Returns a tuple (cmp _success, cmp_result) where cmp_success (in and out)
        is a Boolean and cmp_result is a dictionary of tuples (their, our).
        E.g. the cmp_result could be { "amount":("3000","4000") }

    post_processing_before_commit(swift_message, commit_dict):
        User specific logic for changing dict could be added for MT535
        The dictionary of trades and instruments for a given ISIN before commit are provided for any changes to be done


VERSION: 2.1.2-0.5.3064
----------------------------------------------------------------------------"""
import FSwiftReaderLogger
notifier = FSwiftReaderLogger.FSwiftReaderLogger('SwiftReader', 'FSwiftReaderNotifyConfig')
def on_entry(mt_object):
    return mt_object
    '''
    # Sample to change the pairing attribute list/matching attribute list/eligibility query
    mt_type = mt_object.Type()
    if mt_type == 'MT123':
        if mt_object.Counterparty() == 'XYZ':
            setattr(mt_object.config_param, 'Pair', "{'Amount':{'CMP_FUNC':'myprecision','ARG':'100','LEVEL':'M'}, 'ValueDate':{'LEVEL':'O'}}")
            setattr(mt_object.config_param, 'EligibilityQuery', 'MyEligibility')
            setattr(mt_object.config_param, 'Match', "{'Amount':{'CMP_FUNC':'myprecision','ARG':'100','LEVEL':'M'}, 'ValueDate':{'LEVEL':'O'}}")
    return mt_object
    '''
    '''
    # Sample to ignore message
    mt_type = mt_object.Type()
    if mt_type == 'MT456':
        return None
    elif mt_type == 'MT123' and mt_object.Counterparty() == 'XYZ':
        return None
    '''
def message_entry_hook(swift_data):
    ''' User can override the swift data before any processing takes place.  '''
    return swift_data

def pre_pair(mt_object):
    """ User specific logic to find the paring object. If object is determined then that will be used for pairing"""
    return None

def post_pair(mt_object, paired_objects):
    """  User specific logic for additional checks or adjustments"""
    pair_object = None
    if len(paired_objects) == 1:
        pair_object = paired_objects[0]
        notifier.INFO('Selecting object %s with oid %d for pairing'%(pair_object.Class().Name(), pair_object.Oid()))
    return pair_object

def pre_match(their_mt_object, our_mt_object):
    """ User specific logic to be performed just before matching functionality"""
    return their_mt_object, our_mt_object

def post_match(their_mt_object, our_mt_object, cmp_success, cmp_result):
    """ User specific logic for adding functionality post matching. Returns tuple (match_success, cmp_result)"""
    return cmp_success, cmp_result

def eligibility_extension(eligible_objects, mt_object):
    """ User specific logic for filtering eligible objects for pairing using incoming message"""
    return eligible_objects

def post_processing_before_commit(swift_message, commit_dict):
    """For MT535 - The dictionary of trades and instruments for a given ISIN before commit are provided for any changes to be done"""
    # sample code to set the counterparty is as show below
    '''
    import acm
    key = commit_dict.keys()[0]
    val = commit_dict[key]
    if not val[0].Counterparty():
        val[0].Counterparty(acm.FParty['____'])
    commit_dict[key] = val
    '''
    return commit_dict

def statement_message_validation_check(settlement_obj, statement_line, statement_line_obj, cmp_success = None):
    """function to check that settlement_obj need to process for MT950 message
    settlement_obj : acm object of settlement or some time None in case if not paired with any settlement object
    statement_line : line correspond to settlement in statement
    statement_line_obj : Object of statement line
    cmp_success : True/False depend on matching result
    """

    '''
    
    import acm
    write your logic
    '''
    return True
