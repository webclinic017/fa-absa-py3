""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/common/FBDPValidation.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
    FBDPValidation - main validation for BDP scripts

DESCRIPTION

    A validation base class for BDP scripts. Brings common validation into
    a single class for convenience and maintainability. Also allows derived
    classes to override and perform specific validation.

----------------------------------------------------------------------------"""

import acm
from FBDPCurrentContext import Logme


class FBDPValidate(object):
    def __init__(self, params=None):
        self.validate(params)

    def validate(self, params=None):
        self.validateEntities()
        self.validateValuationParams()
        self.validateAccountingParams()
        self.validateAttributes()
        self.validateSubAttributes()
        self.validateGroupers()
        self.validateMode()
        self.validateInstruments()

    def validateEntities(self):
        msg = ''
        defaultParty = acm.FParty['FMAINTENANCE']
        if defaultParty is None:
            msg += ('The FMAINTENANCE Party is required for BDP scripts and '
                    'does not exist.\n')
            msg += 'Please correct this and re-run this script.\n'
            raise RuntimeError(msg)

        defaultUser = acm.FUser['FMAINTENANCE']
        if defaultUser is None:
            msg += ('The FMAINTENANCE User is required for BDP scripts and '
                    'does not exist.\n')
            msg += 'Please correct this and re-run this script.\n'
            raise RuntimeError(msg)

        return True

    def validateValuationParams(self):
        msg = ''
        valparams = acm.ObjectServer().UsedValuationParameters()
        disableFunding = valparams.DisableFunding()
        historicalPaymentFX = valparams.HistoricalFXChoice()
        if disableFunding != True:
            Logme()(" It is recommended that the Valuation Parameters "
                    "checkbox 'Disable Funding' should be checked for this "
                    "BDP script.\n", "WARNING")
        if historicalPaymentFX != 'None':
            msg += ("Valuation Parameter 'Historical Payment FX' must be set "
                    "to None for this BDP script to continue.\n ")
            raise AttributeError(msg)

        return True

    def validateAccountingParams(self):
        return True

    def validateAttributes(self):
        return True

    def validateSubAttributes(self):
        return True

    def validateGroupers(self):
        return True

    def validateMode(self):
        return True

    def validateInstruments(self):
        return True
