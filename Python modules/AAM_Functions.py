'''
Date                    : 2015-10-20
Purpose                 : This script contains functions used for AAM functionality
Department and Desk     : AAM - Front Office
Requester               : Chris Watts
Developer               : Rohan

HISTORY
================================================================================
Date       Developer       Description
--------------------------------------------------------------------------------
2015-10-20 Rohan           Ceded Instrument Warning code added

-----------------------------------------------------------------------
'''
import acm

def on_open_instrument(eii):
    '''
    Shows a warning messagebox for Ceded instruments - this UI handler is only deployed in the AAM organization module
    '''
    instrument = eii.ExtensionObject().OriginalInstrument()
    if instrument:
        if '(CEDED)' in instrument.Name():
            print 'Instrument is CEDED'
            mb = acm.GetFunction('msgBox', 3)
            ret = mb('Warning', 'This instrument is ceded', 0)

def ceded_ins(ins):
    '''
    Returns numerical value to be used by FColumnAppearance - 1.0 maps to Red cell background colour.
    '''
    if '(CEDED)' in ins.Name():
        return 1.0
    else:
        return 0.0
        
def curo_ins_id(ins):
    '''
    returns a instrument ID to be sent to Curo for instrument identification. 
    Their system has an eight char limit, and needs to be unique to ABSA AAM so that there are no ID collisions on their system.
    '''
    result = str(ins.Oid()).replace(' ', '').replace(',', '')[:7]
    result = 'A' + result
    return result
