'''-----------------------------------------------------------------------
MODULE
    SND_Mismatch

DESCRIPTION
    Date                : 2010-03-31
    Purpose             : Insert the get_dd_delta function
    Department and Desk : PCG SM SND
    Requester           : Dumisani Mkhonza
    Developer           : Ickin Vural
    CR Number           : 269951 (2343)

END DESCRIPTION
-----------------------------------------------------------------------'''

import ael, acm, time




#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def get_ValEnd(t, start, end, val, *rest):
	return get_Value(t, start, end, val, rest)
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def get_Accrued(t, start, end, val, *rest):
	return get_Value(t, start, end, val, rest)
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def get_Interest(t, start, end, val, *rest):
	return get_Value(t, start, end, val, rest)
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def get_TPL(t, start, end, val, *rest):
	return get_Value(t, start, end, val, rest)
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def get_Value_Old(t, start, end, val, *rest):
	
    ael.poll()
    
    t = acm.FTrade[t.trdnbr]

    tr = acm.CreateTradeRow(t, 1)
    tag = acm.CreateEBTag()

    d = '"' + start.to_string() + '"'
    d2 = '"' + end.to_string() + '"'
		
		
    evaluator = acm.GetCalculatedValueFromString(0, 'Standard', "showWhatStartDate", tag)
    evaluator.Simulate(6, 0)	#M.KLIMKE  Make this custom date etc
    
    evaluator = acm.GetCalculatedValueFromString(0, 'Standard', "showWhatEndDate", tag)
    evaluator.Simulate(4, 0) 	#M.KLIMKE 
    
	
    evaluator = acm.GetCalculatedValueFromString(0, 'Standard', "customPLStartDate", tag)
    evaluator.Simulate(d, 0)
	
    evaluator = acm.GetCalculatedValueFromString(0, 'Standard', "customPLEndDate", tag)
    evaluator.Simulate(d2, 0)
	
	
    s = 'object:*"' + str(val) + '"'
    v = acm.GetCalculatedValueFromString(tr, 'Standard', s, tag)

    return v.Value()
	
    
#print get_Accrued(ael.Trade[754437], ael.date('2009-10-29'), ael.date('2009-10-30'), 'Portfolio Accrued Interest')

'''++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'''
def get_Value(t, start, end, column_id,  *rest):

    
    t           = acm.FTrade[t.trdnbr]
    d           = '"' + start.to_string() + '"'
    
    d2          = '"' + end.to_string() + '"'
    calc_space  = acm.Calculations().CreateCalculationSpace('Standard', 'FPortfolioSheet')
    Value       = 0

    try:
	calc_space.SimulateGlobalValue('Portfolio Profit Loss Start Date', 'Custom Date')
	calc_space.SimulateGlobalValue('Portfolio Profit Loss End Date', 'Custom Date')
	calc_space.SimulateGlobalValue('Portfolio Profit Loss Start Date Custom', d)
	calc_space.SimulateGlobalValue('Portfolio Profit Loss End Date Custom', d2)
        Calc  = calc_space.CalculateValue(t, column_id)
	Value = Calc.Value().Number()

    finally:
        calc_space.RemoveGlobalSimulation('Portfolio Profit Loss Start Date')
        calc_space.RemoveGlobalSimulation('Portfolio Profit Loss End Date')
        calc_space.RemoveGlobalSimulation('Portfolio Profit Loss Start Date Custom')
        calc_space.RemoveGlobalSimulation('Portfolio Profit Loss End Date Custom')
        
	return Value
	
class SheetCalcSpace( object ):
    CALC_SPACE = acm.FCalculationSpace('FPortfolioSheet' )
    @classmethod
    def get_column_calc( cls, obj, column_id ):
        calc = SheetCalcSpace.CALC_SPACE.CreateCalculation( obj, column_id )
        return calc

def get_bm_delta(t, *rest):
    '''
Retruns the Trading Manager instrument benchmark delta column 
    '''

    column_id       = 'Flat Benchmark Delta'
    trade           = acm.FTrade[t.trdnbr]

    calc = SheetCalcSpace.get_column_calc(trade, column_id)
    Value = calc.Value().Number()
    
    return Value
    
    
def get_dd_delta(t, *rest):
    '''
Retruns the Trading Manager instrument discount delta column 
    '''

    column_id       = 'Portfolio Delta Discount'
    trade           = acm.FTrade[t.trdnbr]

    calc = SheetCalcSpace.get_column_calc(trade, column_id)
    Value = calc.Value().Number()
    
    return Value

#print get_Value(ael.Trade[3113724],ael.date('2008-01-01'),ael.date('2009-01-01'),'Portfolio Value End')

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def change_par_override_Old(temp, new_po, *rest):

    ael.poll()
    u = ael.user().usrnbr
    old = -1

    for pm in ael.ParameterMapping.select('usrnbr = %i' % u):
        
        if pm.override_level == 'Workspace':
            for i in pm.par_mapping_instances():
                if i.parameter_type == 'Context Par':
                    old = i.context_seqnbr.seqnbr
                    
                    ic = i.clone()            
                    ic.context_seqnbr = ael.Context[new_po]
                    try:
                        ic.commit()
                        ael.poll()
                        #print 'changed'
                        return old
                    except:
                        print 'could not change workspace parameter override'
                        return old

    print 'Existing override not found, set workspace override to ACMB Global'
    
    return old


def change_par_override(temp, new_po, *rest):

    ael.poll()
    u = ael.user().usrnbr
    old = -1

    for pm in acm.FParameterMapping.Select('user = %i' %u):
        if pm.OverrideLevel()  == 'Workspace':
            for i in pm.ParMappingInstances():
                if i.ParameterType() == 'Context Par':
                    old = i.Context().Oid()
                    try:
                        i.Context(acm.FContext.Select('oid = %i' %new_po))
                        i.Commit()
                        return old
                    except:
                        print 'could not change workspace parameter override'
                        return old

    print 'Existing override not found, set workspace override to ACMB Global'
    
    return old
