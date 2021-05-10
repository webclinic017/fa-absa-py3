import acm


def amount(cfw, settlement, *rest):
    '''Computes the amount used in Call_volumes_report.asql
    
    If cash flow has a settlement, then the amount of the cash flow is given by
    the amount of the settlement. Otherwise, the function returns the
    calculated value defined in the Projected column from Cash Analysis Sheet.
    '''
    if settlement:
        return settlement.amount
    else:
        context = acm.GetDefaultContext()
        sheet_type = 'FMoneyFlowSheet'
        column_id = 'Cash Analysis Projected'
        cashflow = acm.FCashFlow[cfw.cfwnbr]
        calc_space = acm.Calculations().CreateCalculationSpace(context,
                                                               sheet_type)
        value = calc_space.CalculateValue(cashflow, column_id)
        return value.Value()
