'''-----------------------------------------------------------------------------
PROJECT                 :  Aggregation
PURPOSE                 :  This is to update the Montly and YEarly values on Aggregation rules
DEPATMENT AND DESK      :  
REQUESTER               :  Jaco Moulder
DEVELOPER               :  Jaco Moulder
CR NUMBER               :  
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date       Change no            Developer       Description
--------------------------------------------------------------------------------
2018-05-04                     Jaco Moulder    Initial Implementation

'''

import acm, FAggruleSelectItem, FBDPGui

ttRule = ("If set, only run the set of aggregation rules defined by these "
        "trade filters. If not set, all aggregation rules will be used.")
ttMonthly = ("Set the required Monlthy value the aggregation rule will "
        "be updated to.")
ttYearly = ("Set the required Yearly value the aggregation rule will "
        "be updated to.")
ttAddMonthly = ("Add the number specified to the existing open days.")
        
def customDialog(shell, params):
    customDlg = FAggruleSelectItem.SelectAggrulesCustomDialog(params)
    return acm.UX().Dialogs().ShowCustomDialogModal(shell,
            customDlg.CreateLayout(), customDlg)

ael_variables = FBDPGui.LogVariables(            
            ['aggrule_filters', 'Aggregation filters_Aggregation', 'int', [], '', 1, 1, ttRule, None, 1, customDialog],
            ['monthlyvalue', 'Monthly Nr of Aggregates to create', 'int', [], 0, 1, 0, ttMonthly, None, 1],
            ['yearlyvalue', 'Yearly Nr of Aggregates to create', 'int', [], 0, 1, 0, ttYearly, None, 1],
            ['addMonthlyValue', 'Add to Monthly value.', 'int', [], 0, 1, 0, ttAddMonthly, None, 1]
        )

def ael_main(dictionary):
    AggRule_FilterNrs = dictionary['aggrule_filters']
    update_monthly = dictionary['monthlyvalue']
    update_yearly = dictionary['yearlyvalue']
    add_monthly = dictionary['addMonthlyValue']
    for AggRule_FilterNr in AggRule_FilterNrs:
        Agg_Rule = acm.FAggregationRule.Select01("fltnbr=%i" % AggRule_FilterNr, "Multiple AggRule Filters passed")
        if update_monthly != 0 or update_yearly != 0:
            print 'Updating aggregation rule FltNbr %s. Monthly value --> %i to %i. Yearly value ---> %i to %i' %(Agg_Rule.Fltnbr(), Agg_Rule.Monthly(), update_monthly, Agg_Rule.Yearly(), update_yearly)
            Agg_Rule.Monthly(update_monthly)
            Agg_Rule.Yearly(update_yearly)
        elif update_monthly == 0 and update_yearly == 0 and add_monthly == 0:
            print 'Updating aggregation rule FltNbr %s. Monthly value --> %i to %i. Yearly value ---> %i to %i' %(Agg_Rule.Fltnbr(), Agg_Rule.Monthly(), update_monthly, Agg_Rule.Yearly(), update_yearly)
            Agg_Rule.Monthly(update_monthly)
            Agg_Rule.Yearly(update_yearly)
        elif add_monthly != 0:
            new_value = Agg_Rule.Monthly() + add_monthly
            print 'Updating aggregation rule FltNbr %s. Monthly value --> %i to %i.' %(Agg_Rule.Fltnbr(), Agg_Rule.Monthly(), new_value)
            Agg_Rule.Monthly(new_value)
        Agg_Rule.Commit()
        print 'New values aggregation rule FltNbr %s. Monthly value --> %i. Yearly value ---> %i' %(Agg_Rule.Fltnbr(), Agg_Rule.Monthly(), Agg_Rule.Yearly())
