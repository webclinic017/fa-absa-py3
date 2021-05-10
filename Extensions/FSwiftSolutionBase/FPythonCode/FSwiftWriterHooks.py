"""----------------------------------------------------------------------------
MODULE:
    FSwiftWriterHooks

DESCRIPTION:
    A module for providing customizations for last minute changes in Swift message
    User can customize the swift message using provided methods

FUNCTIONS:
    export_exit_hook
    message_exit_hook

VERSION: 3.0.0-0.5.3344
----------------------------------------------------------------------------"""
import FSwiftWriterLogger

notifier = FSwiftWriterLogger.FSwiftWriterLogger('SwiftWriter', 'FSwiftWriterNotifyConfig')

def export_exit_hook(acm_obj, pyobj):
    '''This hook is called after the pyobject for message type is generated using mappings specified. User can
     do any last minute changes to the pyobject here. This function should return the modified pyobj and that
     object will be used to generate the swift message
     Note : Please make sure that you re-assign the value of swift tag after you have changed the value of particular field.
     e.g
     pyobj.TransactionReference = datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S%f")
     pyobj.TransactionReference.swiftTag = "20"
    '''
    return pyobj

def message_exit_hook(swift_msg):
    ''' This hook is called in network rules validation after the swift message is generated. User can do any last minute
    change to the message here. This function should return swift_message in swift message format.
    Input and output to this api is string.
    Ex: Swift message should be in format like:
    {1:F01OURODEFFAXXX0000000000}{2:I192CIBCCATTXXXXN}{3:{108:FAS-21425-1}}{4:
    :20:FAS-21425-1
    :21:FAS-21424-1
    :11S:103
    180531
    :79:Settlement Id 21424 was due to
    2018-05-31
    -}
    '''
    return swift_msg

"""Uncomment the following hook to provide it's implementation"""

"""def validate_use_of_extended_x_char_for_counterparty_hook(swift_msg):
    ''' This hook is called for validating extended x characters in the
        swift message. If you are customizing this implementation you need
        to check if the message contains extended characters.
        If the additional info SWIFTExtXChrNotUsed on destination party
        is set to true and message contains extented characters, return the
        object of the party(FParty), flag as false and error string.
        
        :param swift_msg - swift message
        :return object of the destination party (FParty), flag and error string. 
        
        example:
        import acm
        destinationParty = acm.FParty['DestinationPartyName']
        retVal = True
        error_str = ''        

    '''    
    destinationParty = ''
    retVal = True
    error_str = ''
    return destinationParty, retVal, error_str"""

