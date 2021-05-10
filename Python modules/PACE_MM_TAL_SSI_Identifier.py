'''----------------------------------------------------------------------------------------------------------
MODULE                  :       PACE_MM_TAL_SSI_Identifier
PURPOSE                 :       This AEL contains functions to determine valid Funding Desk SSIs
DEPARTMENT AND DESK     :       Money Market Desk
REQUASTER               :       Linton Behari-Ram
DEVELOPER               :       Heinrich Cronje
CR NUMBER               :       603220
-------------------------------------------------------------------------------------------------------------

HISTORY
=============================================================================================================
Date            Change no       Developer                       Description
-------------------------------------------------------------------------------------------------------------
2012-09-14      603220          Heinrich Cronje                 Initial Implementation
2014-10-14                      Matthias Riedel                 Adjust for Non ZAR
-------------------------------------------------------------------------------------------------------------

DESCRIPTION OF AEL:

    This AEL contains functions to determine valid Funding Desk SSIs.
    This will be called from the ASQL PACE_MM_SSI_Report.
----------------------------------------------------------------------------------------------------------'''

import acm
import PACE_MM_Parameters as Params

def isHighLevelSSI(ssi):
    if ssi.Currency() and ssi.Currency().Name() in Params.VALID_CURRENCIES \
        and ssi.FromParty() and ssi.FromParty().Name() == Params.VALID_CURR_CALENDAR_DAYCOUNT_ACQUIRER_COMBINATION[ssi.Currency().Name()][2] \
        and ssi.InstrumentType() == 'None' and ssi.UndInsType() == 'None' \
        and ssi.CashSettleCashFlowType() == 'None' and not ssi.SettleCategoryChlItem() \
        and ssi.OtcInstr() == 'OTC':
            return True
    return False

def isLowLevelSSI(ssi):
    if ssi.Currency() and ssi.Currency().Name() in Params.VALID_CURRENCIES \
        and ssi.FromParty() and ssi.FromParty().Name()  == Params.VALID_CURR_CALENDAR_DAYCOUNT_ACQUIRER_COMBINATION[ssi.Currency().Name()][2]  \
        and ssi.InstrumentType() == 'Deposit' and ssi.UndInsType() == 'None' \
        and ssi.CashSettleCashFlowType() == 'Fixed Amount' and not ssi.SettleCategoryChlItem() \
        and ssi.OtcInstr() == 'OTC':
            return True
    return False

def hasValidSSIRule(ssi):
    for ssiRule in ssi.Rules():
        if not ssiRule.EffectiveTo() and ssiRule.EffectiveFrom() == '1970-01-01':
            if ssiRule.CashAccount():
                return True
    return False

def isValidSSI(ssi, *rest):
    ssi = acm.FSettleInstruction[ssi.seqnbr]
    if isHighLevelSSI(ssi) or isLowLevelSSI(ssi):
        return hasValidSSIRule(ssi)
    return False
