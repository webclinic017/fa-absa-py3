""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/confirmation/etc/FConfirmationClientValidationTemplate.py"
"""----------------------------------------------------------------------------
MODULE
    FConfirmationClientValidationTemplate

DESCRIPTION    
    Before changing these hooks, copy the content to a new module called
    FConfirmationClientValidation. After having made changes to this
    module the confirmation ATS needs to be restarted for the changes
    to take affect.
----------------------------------------------------------------------------"""

def IsManualMatch(confirmation):
    """
    DESCRIPTION: Function determining whether a confirmation record
                 shall be set to status Manual Match.
    INPUT:       An FConfirmation object. Treat object as
                 read-only.
    OUTPUT:      True or False
    """
    
    isManualMatch = False
    return isManualMatch

def IsSetToReleased(confirmation):
    """
    DESCRIPTION: Function determining whether an authorised confirmation
                 record shall be automatically set to status Released.
                 False is returned by default meaning that ConfInstruction
                 STP flag will decide if confirmation status will be Authorised
                 or Released.
    INPUT:       An FConfirmation object. Treat object as
                 read-only.
    OUTPUT:      True or False
    """
    
    isSetToReleased = False
    return isSetToReleased
