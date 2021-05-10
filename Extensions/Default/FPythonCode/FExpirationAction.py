""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/expiration/etc/FExpirationAction.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
        FExpirationAction.py - Script definition for FExpiration actions.

DESCRIPTION
        The script contains the definitions of FExpiration actions.

ENDDESCRIPTION
----------------------------------------------------------------------------"""


# Expiration actions in both V1 and V2
DEL_OBS_DATA = 'Delete obsolete data'
ARC_UNTRD_INS = 'Archive untraded instruments'
DEL_UNTRD_INS = 'Delete untraded instruments'
ARC_INS_AND_POS_W_OUT_PL = 'Archive instruments and positions without P/L'
DEL_INS_AND_POS_W_OUT_PL = 'Delete instruments and positions without P/L'


# Deprecated expiration actions in V1
ARC_INS_AND_CASH_POST_POS = 'Archive instruments and cashpost positions'
DEL_INS_AND_CASH_POST_POS = 'Delete instruments and cashpost positions'
ARC_INS_AND_TRD_W_OUT_CASH_POST = ('Archive instruments and trades without '
        'cashposting')
DEL_INS_AND_TRD_W_OUT_CASH_POST = ('Delete instruments and trades without '
        'cashposting')


# New expiration actions in V2
ARC_AND_CASH_POST_POS = 'Archive and cash post positions'
DEL_AND_CASH_POST_POS = 'Delete and cash post positions'
ARC_POS_W_OUT_CASH_POST = 'Archive positions without cash posting'
DEL_POS_W_OUT_CASH_POST = 'Delete positions without cash posting'


_ACTION_LIST_COMMON = [
        ARC_UNTRD_INS,
        DEL_UNTRD_INS,
        ARC_INS_AND_POS_W_OUT_PL,
        DEL_INS_AND_POS_W_OUT_PL]


_ACTION_LIST_V1_ONLY = [
        DEL_OBS_DATA,
        ARC_INS_AND_CASH_POST_POS,
        DEL_INS_AND_CASH_POST_POS,
        ARC_INS_AND_TRD_W_OUT_CASH_POST,
        DEL_INS_AND_TRD_W_OUT_CASH_POST]


_ACTION_LIST_V2_ONLY = [
        ARC_AND_CASH_POST_POS,
        DEL_AND_CASH_POST_POS,
        ARC_POS_W_OUT_CASH_POST,
        DEL_POS_W_OUT_CASH_POST]

ACTION_LIST_V1 = _ACTION_LIST_COMMON + _ACTION_LIST_V1_ONLY

ACTION_LIST_V2 = _ACTION_LIST_COMMON + _ACTION_LIST_V2_ONLY

ACTION_LIST_CURRENT = ACTION_LIST_V2

ACTION_LIST_ALL = (_ACTION_LIST_COMMON + _ACTION_LIST_V1_ONLY +
        _ACTION_LIST_V2_ONLY)
