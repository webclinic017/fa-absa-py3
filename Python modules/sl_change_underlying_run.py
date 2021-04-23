"""-----------------------------------------------------------------------------
PURPOSE              :  Changes underlying instrument on security loans
DEPATMENT AND DESK   :  SM PCG - Securities Lending Desk
REQUESTER            :  Marko Milutinovic
DEVELOPER            :  Francois Truter
CR NUMBER            :  526074
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date       Change no Developer          Description
--------------------------------------------------------------------------------
2010-12-17 526074    Francois Truter    Initial Implementation
"""

import acm
import sl_change_underlying
from sl_process_log import ProcessLog
from sl_process_log import ProcessLogException

SCRIPT_NAME = 'Change Underlying Instrument'
SOURCE_INSTRUMENT_KEY = 'SourceInstrument'
DESTINATION_INSTRUMENT_KEY = 'DestinationInstrument'

OK_AND_CANCEL = 1
OK = 1
CANCEL = 2

#Variable Name, Display Name, Type, Candidate Values, Default, Mandatory, Multiple, Description, Input Hook, Enabled
ael_variables = [
    [SOURCE_INSTRUMENT_KEY, 'Source Instrument', 'FInstrument', None, None, 1, 1, 'Security loans on this instrument will be changed', None, 1],
    [DESTINATION_INSTRUMENT_KEY, 'Destination Instrument', 'FInstrument', None, None, 1, 1, 'Underlying instrument will be changed to this instrument', None, 1]
]
ael_gui_parameters = {'windowCaption': SCRIPT_NAME}

def ael_main(parameters):
    log = ProcessLog(SCRIPT_NAME)
    try:
        sourceInstrument = parameters[SOURCE_INSTRUMENT_KEY][0]
        destinationInstrument = parameters[DESTINATION_INSTRUMENT_KEY][0]
        
        func=acm.GetFunction('msgBox', 3)
        buttonSelected = func(SCRIPT_NAME, 'Are you sure you want change all the underlying instruments from %(source)s to %(destination)s?\nClick [OK] to continue or [Cancel] to abort.'
            % {'source': sourceInstrument.Name(), 'destination': destinationInstrument.Name()}, 1)

        if buttonSelected == OK:
            sl_change_underlying.ChangeUnderlyingInstrument(sourceInstrument, destinationInstrument, log)
        else:
            log.Information('Change aborted')
    except Exception, ex:
        if not isinstance(ex, ProcessLogException):
            log.Exception(str(ex))
        else:
            print str(ex)
    finally:
        print log
    
