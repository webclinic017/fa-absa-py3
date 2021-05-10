"""-----------------------------------------------------------------------------
PURPOSE                 :  An override on the core GetMTMessage fucntion
                           Implemented as part of the Demat project
REQUESTER               :  Linda Breytenbach
DEVELOPER               :  Manan Ghosh
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date            Change no       Developer		Description
--------------------------------------------------------------------------------
2016-08-19      CHNG0003744247  Manan Ghosh		Initial Implementation
2017-12-11      CHNG0005220511  Willie vd Bank          Refactored the module
"""

import acm

DEMAT_PRESETTLE_CONF = 'Demat PreSettle Conf'
DEMAT_MATCH_REQUEST = 'Demat Match Request'

def GetMTMessage(Confirmation, messageType):
    if DEMAT_MATCH_REQUEST in Confirmation.EventType():
        return '598'
    if DEMAT_PRESETTLE_CONF in Confirmation.EventType():
        return '564'
                    
    return messageType
