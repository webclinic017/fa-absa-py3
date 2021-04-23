import ael
import acm
'''--------------------------------------------------------------------------------------------------------------

--------------------------------------------------------------------------------------------------------------'''
class OrderBookSheetCalcSpace( object ):

    CALC_SPACE = acm.FCalculationSpace('FOrderBookSheet' )
  
    @classmethod
    def get_column_calc( cls, obj, column_id ):
        calc = OrderBookSheetCalcSpace.CALC_SPACE.CreateCalculation( obj, column_id )
        return calc
'''--------------------------------------------------------------------------------------------------------------

--------------------------------------------------------------------------------------------------------------'''
def getGreeks2(instr, context, column, *rest):
    
    '''M.KLIMKE Original Code
    adfl = 'object:*"%s"' % (column)
    context = context
    tag = acm.CreateEBTag()
    acm_ins = acm.FInstrument[instr.insid]
    eval = acm.GetCalculatedValueFromString(acm_ins, context, 'object:*"' + column + '"[useDatabasePrice=1,doSplitAll=0]',tag)
    return eval.Value()'''
    acm_ins = acm.FInstrument[instr.insid]
    calc    = OrderBookSheetCalcSpace.get_column_calc(acm_ins, column)
    return  calc.Value().Number()
'''--------------------------------------------------------------------------------------------------------------

--------------------------------------------------------------------------------------------------------------'''
def populateSpot(ins):

    #M.KLIMKE pval = getGreeks2(ins,'Standard','theor')
    pval = getGreeks2(ins, 'Standard', 'Price Theor')  #M.KLIMKE note uses the column id and not the extension attribute

    print pval
    for p in ins.prices():
        if p.ptynbr.ptyid == 'SPOT':
            pc = p.clone()
            pc.settle = pval
            pc.last = pval
            pc.day == ael.date_today()
            #print pc.pp()
            pc.commit()
    

populateSpot(ael.Instrument['QuantoHedge_Test'])    
