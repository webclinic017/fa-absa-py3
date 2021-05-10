""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/corp_actions/etc/FScripDivConst.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
    FScripDivPerform - Module which process the scrip dividend.

DESCRIPTION
----------------------------------------------------------------------------"""


UNDERLYING_INS_TYPES_ALLOWED = ('Stock',)
DERIVATIVE_INS_TYPES_ALLOWED = ('CFD',)
INS_TYPES_ALLOWED = UNDERLYING_INS_TYPES_ALLOWED + DERIVATIVE_INS_TYPES_ALLOWED


TRADE_STATUS_SIMULATED = 'Simulated'
TRADE_STATUS_VOID = 'Void'


TRADE_STATUS_NOT_CONTRIBUTING_QUANTITY = (TRADE_STATUS_SIMULATED,
        TRADE_STATUS_VOID)


ROUNDING_UP_OR_DOWN = 'Normal'
ROUNDING_DOWN_ONLY = 'Down'


ROUNDING_CHOICES = (ROUNDING_UP_OR_DOWN, ROUNDING_DOWN_ONLY)


SCRIP_ISSUE_TRADE_TIME = '00:00:04'
