"""----------------------------------------------------------------------------------------------------
DESCRIPTION
    This module contains code to fix the resets for SOFR rate index deposits as per the lockout.

-------------------------------------------------------------------------------------------------------
HISTORY
=======================================================================================================
Date            JIRA no       Developer               Requester               Description
-------------------------------------------------------------------------------------------------------
2020-02-07      FAFO-71       Amit Kardile            Haroon Mansoor          Initial Implementation
-------------------------------------------------------------------------------------------------------
"""
import acm

def popup(shell, message):
    return acm.UX.Dialogs().MessageBoxInformation(shell, message)

def fix_lockout_resets_check_failed(shell, obj):
    if obj.IsKindOf('FInstrument') and obj.InsType() == 'Deposit' and obj.Legs():
        try:
            instrument = obj
            leg = instrument.Legs()[0]
            if (leg and leg.FloatRateReference() and leg.FloatRateReference().InsType() == 'RateIndex' and leg.FloatRateReference().AdditionalInfo().Lockout_Eligible()):
                if not (leg.ResetType() == 'Compound' and leg.ResetPeriod() == '1d'):
                    popup(shell, "In case of SOFR rate index, please specify reset to daily compounding.")
                    return True
                lockout = instrument.AdditionalInfo().Lockout()
                if lockout is None:
                    popup(shell, "Please specify Lockout.")
                    return True
                elif lockout < 0:
                    popup(shell, "Lockout must be positive.")
                    return True
                elif lockout == 0:
                    return
                elif lockout > 0:
                    for cashflow in leg.CashFlows():
                        if cashflow.CashFlowType() in ['Float Rate', 'Call Float Rate']:
                            #Change the date of the last number of resets as defined in Lockout add info to the previous reset date
                            resets = cashflow.Resets().SortByProperty('Day', True)[-(lockout+1):]
                            if resets:
                                lockout_date = resets[0].Day()
                                for reset in resets[1:]:
                                    if reset.Day() != lockout_date:
                                        default_reset_date = reset.Day()
                                        reset.Day(lockout_date)
                                        print("Changed the SOFR float leg's reset date from %s to lockout date %s" %(default_reset_date, lockout_date))
        except Exception as e:
            error = 'Error occured while applying lockout on SOFR index deposit. Log: %s' % str(e)
            popup(shell, error)
            return True
