import acm

calc_space = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), 'FDealSheet')

def get_Ins_Accrued(obj):
    i = obj.Instrument()
    column_id = 'Portfolio Accrued Interest'
    
    top_node = calc_space.InsertItem(i)  
    calc_space.SimulateValue( top_node, 'Portfolio Edit', 'CD_COLLATERAL' )      
    calc_space.Refresh()
    calculation = calc_space.CreateCalculation( top_node, column_id )
    calc = calculation.Value()
    
    val = 1.0 + calc.Number() / i.NominalAmount()

    return val

