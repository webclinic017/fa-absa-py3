import ael, acm
debug = 0

class CalcSpace(object):

    calcSpace = acm.Calculations().CreateStandardCalculationsSpaceCollection()

def credspread_delta_bucket_generic(yc, shiftsize, stf, Party, dcount, dunit, shifttype):
    #print (str)(dcount) + (str)(dunit[0])

    pv1 = 0
    pv0 = 0
    #print yc,shiftsize,stf,syc,Party,dcount,dunit,rest
    for attribute in yc.Attributes():
        
        if str(attribute.AttributeName()) == Party:
    #########        

            tf=acm.FTradeSelection[stf]
            if tf == None:
                print 'TradeFilter', "'" + stf + "'", 'not found. Note TradeFilter is case sensitive'
                return -99999999999.0
            print str(attribute.AttributeName())
            
            tf_calc = tf.Calculation()
            pv0=tf_calc.PresentValue(CalcSpace.calcSpace).Number()
                  
#            for SpreadMember in member.spreads().members():
#                Test1 = SpreadMember.clone()
#                #print Test1.spread        
            
            for spreadMember in attribute.Spreads():
                if (str)(spreadMember.Point().DatePeriod()) == (str)(dunit):
                    spreadClone = spreadMember.Clone()
                    spr0 = spreadClone.Spread()
                    if shifttype == 'Delta':
                        spreadClone.Spread = spreadClone.Spread() + shiftsize
                    elif shifttype == 'Deltapct':
                        spreadClone.Spread = spreadClone.Spread() * shiftsize
                    spreadMember.Apply(spreadClone)
                    pv1=tf_calc.PresentValue(CalcSpace.calcSpace).Number()
                    spreadMember.Undo()
                    print 'Issuer ', (str)(attribute.AttributeName()), ' pv0 ', pv0, ' pv1 ', pv1, ' dunit = ', dunit, ' date_period = ', spreadMember.Point().DatePeriod(), ' spr0 = ', spr0, ' spr1 = ', spreadClone.Spread()
#                    Test1
            pv01 = pv1 - pv0
            
#            for SpreadMember in member.spreads().members():
#                Test2 = SpreadMember.clone()
#                Test2.spread = Test2.spread - shiftsize
#                Test2.apply()
#                #print Test2.spread

            #yc.calculate()
#            yc.simulate()
#            pv2 = tf.present_value()  
#            pv02 = pv2 - pv0
#            print (str)(member.issuer_ptynbr.display_id()), ',pv0 = ,', pv0, ',pv1 = ,', pv1, ',pv01 = ,', pv01
#pv02
    return pv01
        
# ---------------------------------------------------------------------------
# CS01_Choose the shift size - used for Attribute type curves such as CDISSUERCURVE_HR
# ---------------------------------------------------------------------------
def credspread_delta_shift(yc ,shiftsize, stf , syc , Party , dcount, dunit,*rest):
    yc=acm.FYieldCurve[syc]
    shifttype='Delta'
    return credspread_delta_bucket_generic(yc, shiftsize, stf, Party, dcount, dunit, shifttype)
    
# ---------------------------------------------------------------------------
# CS1% - used for Attribute type curves such as CDISSUERCURVE_HR
# ---------------------------------------------------------------------------
        
def credspread_deltapct_shift(yc ,shiftsize, stf , syc , Party , dcount, dunit,*rest):
    yc=acm.FYieldCurve[syc]
    shifttype='Deltapct'
    return credspread_delta_bucket_generic(yc, shiftsize, stf, Party, dcount, dunit, shifttype)
    
#print credspread_deltapct_shift('yc' ,1.01, 'CredDer_All' , 'CDIssuerCurve_HR' , 'ANGLO AMERICAN PLC ISSUER' , 1, '1y')


def credspread_delta_generic(ycname, shiftsize, stf, Party, shifttype):

    yc=acm.FYieldCurve[ycname]
    
    for attribute in yc.Attributes():
        
        if str(attribute.AttributeName()) == Party:
            
            
            tf=acm.FTradeSelection[stf]
            if tf == None:
                print 'TradeFilter', "'" + stf + "'", 'not found. Note TradeFilter is case sensitive'
                return -99999999999.0
            
            tf_calc = tf.Calculation()
            pv0=tf_calc.PresentValue(CalcSpace.calcSpace).Number()
            
            for spread in attribute.Spreads():
                spreadClone=spread.Clone()
                if shifttype == 'Delta':
                    spreadClone.Spread=spreadClone.Spread()-shiftsize
                elif shifttype == 'Deltapct':
                    spreadClone.Spread=spreadClone.Spread()*shiftsize
                spread.Apply(spreadClone)
            
            #yc.SimulateCurve()
            pv1=tf_calc.PresentValue(CalcSpace.calcSpace).Number()
            pv01 = pv1-pv0
            yc.Undo()
            print Party, pv0, pv1, pv01
            return pv01
# ---------------------------------------------------------------------------
# CS01 - used for Attribute type curves such as CDISSUERCURVE_HR
# ---------------------------------------------------------------------------

def credspread_delta(yc , stf , syc , Party , *rest):
    shiftsize = 0.0001
    shifttype = 'Delta'
    return credspread_delta_generic(syc, shiftsize, stf, Party, shifttype)
    
# ---------------------------------------------------------------------------
# CS1% - used for Attribute type curves such as CDISSUERCURVE_HR
# ---------------------------------------------------------------------------
        
def credspread_deltapct(yc , stf , syc , Party , *rest):
    shiftsize = 0.99
    shifttype = 'Deltapct'
    return credspread_delta_generic(syc, shiftsize, stf, Party, shifttype)


# ---------------------------------------------------------------------------
# CS01 for Instrument Spread curves i.e. ABACAS
# ---------------------------------------------------------------------------

def insSpread_delta(yc , stf ,  Party , *rest):
    for spread in yc.InstrumentSpreads():
        if debug == 1:
            print 'Initial Spread', spread.Spread()
        
        tf=acm.FTradeSelection[stf]
        if tf == None:
            print 'TradeFilter', "'" + stf + "'", 'not found. Note TradeFilter is case sensitive'

        tf_calc = tf.Calculation()
        pv0=tf_calc.PresentValue(CalcSpace.calcSpace).Number()
        
        spreadClone=spread.Clone()
        spreadClone.Spread=spread.Spread()-0.0001
        
        spread.Apply(spreadClone)
        
        if debug == 1:
            print 'Updated Spread', spread.Spread()
        
        pv1 = tf_calc.PresentValue(CalcSpace.calcSpace).Number()
        
        pv01 = pv1-pv0
        yc.Undo()
        
        print 'Instrument', spread.Instrument.Name(), 'pv0', pv0, 'pv1', pv1, 'pv01', pv01
        return pv01

