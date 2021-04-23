import ael, acm
debug = 0

class CalcSpace(object):

    calcSpace = acm.Calculations().CreateStandardCalculationsSpaceCollection()
    
# ---------------------------------------------------------------------------
# CS01_Choose the shift size - used for Attribute type curves such as CDISSUERCURVE_HR
# ---------------------------------------------------------------------------

def credspread_delta_shift_pv0(yc ,shiftsize, stf , syc , Party , dcount, dunit,*rest):
    #print (str)(dcount) + (str)(dunit[0])
    #yc = ael.YieldCurve['CDIssuerCurve']
    yc=acm.FYieldCurve[syc]
    pv = 0

    for attribute in yc.Attributes():
    ###########  
        if str(attribute.AttributeName()) == Party:
    #########        
            #print dir(member.spreads().members())
            #member.spreads().members().sort()

            tf=acm.FTradeSelection[stf] 
            if tf == None:
                print 'TradeFilter', "'" + stf + "'", 'not found. Note TradeFilter is case sensitive'
                return -99999999999.0
#            print (str)(member.issuer_ptynbr.display_id())
            tf_calc = tf.Calculation()
            pv=tf_calc.PresentValue(CalcSpace.calcSpace).Number()
                  

    return pv
        

# ---------------------------------------------------------------------------
# CS1% - used for Attribute type curves such as CDISSUERCURVE_HR
# ---------------------------------------------------------------------------
        
def credspread_deltapct_shift_pv0(yc ,shiftsize, stf , syc , Party , dcount, dunit,*rest):
    #print (str)(dcount) + (str)(dunit[0])
    #yc = ael.YieldCurve['CDIssuerCurve']
    yc=acm.FYieldCurve[syc]
    pv = 0

    for attribute in yc.Attributes():
    ###########  
        if str(attribute.AttributeName()) == Party:
    #########        
            #print dir(member.spreads().members())
            #member.spreads().members().sort()

            tf=acm.FTradeSelection[stf]
            if tf == None:
#                print 'TradeFilter', "'" + stf + "'", 'not found. Note TradeFilter is case sensitive'
                return -99999999999.0
#            print (str)(member.issuer_ptynbr.display_id())
            tf_calc = tf.Calculation()
            pv=tf_calc.PresentValue(CalcSpace.calcSpace).Number()
                  
    return pv


debug = 0

# ---------------------------------------------------------------------------
# CS01_Choose the shift size - used for Attribute type curves such as CDISSUERCURVE_HR
# ---------------------------------------------------------------------------

def credspread_delta_shift_generic(yc, shiftsize, stf, Party, dcount, dunit, shifttype):

    for attribute in yc.Attributes():
    ###########  
        if str(attribute.AttributeName()) == Party:
    #########        
            #print dir(member.spreads().members())
            #member.spreads().members().sort()

            tf=acm.FTradeSelection[stf]
            if tf == None:
#                print 'TradeFilter', "'" + stf + "'", 'not found. Note TradeFilter is case sensitive'
                return -99999999999.0
                
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
                        print 'Delta Shift*****************************************'
                        spreadClone.Spread = spreadClone.Spread() + shiftsize
                    elif shifttype == 'Deltapct':
                        spreadClone.Spread = spreadClone.Spread() * shiftsize
                        print 'Deltapct shift*********************************'
                    spreadMember.Apply(spreadClone)
                    pv=tf_calc.PresentValue(CalcSpace.calcSpace).Number()
                    spreadMember.Undo()
#                   print 'Issuer ',(str)(member.issuer_ptynbr.display_id()),' pv0 ', pv0, ' pv1 ', pv1,' dunit = ' , dunit, ' date_period = ', SpreadMember.point_seqnbr.date_period,' spr0 = ',spr0, ' spr1 = ', Test1.spread
    return pv
        
# ---------------------------------------------------------------------------
# CS01_Choose the shift size - used for Attribute type curves such as CDISSUERCURVE_HR
# ---------------------------------------------------------------------------

def credspread_delta_shift_pv1(yc ,shiftsize, stf , syc , Party , dcount, dunit,*rest):
    yc=acm.FYieldCurve[syc]
    shifttype='Delta'
    return credspread_delta_shift_generic(yc, shiftsize, stf, Party, dcount, dunit, shifttype)
    
# ---------------------------------------------------------------------------
# CS1% - used for Attribute type curves such as CDISSUERCURVE_HR
# ---------------------------------------------------------------------------
        
def credspread_deltapct_shift_pv1(yc ,shiftsize, stf , syc , Party , dcount, dunit,*rest):
    yc=acm.FYieldCurve[syc]
    shifttype='Deltapct'
    return credspread_delta_shift_generic(yc, shiftsize, stf, Party, dcount, dunit, shifttype)
import ael, time
debug = 0

# ---------------------------------------------------------------------------
# CS01_Choose the shift size - used for Attribute type curves such as CDISSUERCURVE_HR
# ---------------------------------------------------------------------------

def credspread_delta_shift_pv0(yc ,shiftsize, stf , syc , Party , dcount, dunit,*rest):
    #print (str)(dcount) + (str)(dunit[0])
    #yc = ael.YieldCurve['CDIssuerCurve']
    ael.poll()
    pv = 0
    yc=yc.clone()
    for member in yc.attributes().members():
    ###########  
        if (str)(member.issuer_ptynbr.display_id()) == Party:
    #########        
            #print dir(member.spreads().members())
            #member.spreads().members().sort()

            tf = ael.TradeFilter[stf] 
            if tf == None:
                print 'TradeFilter', "'" + stf + "'", 'not found. Note TradeFilter is case sensitive'
                return -99999999999.0
#            print (str)(member.issuer_ptynbr.display_id())
            pv = tf.present_value()
                  

    return pv
        

# ---------------------------------------------------------------------------
# CS1% - used for Attribute type curves such as CDISSUERCURVE_HR
# ---------------------------------------------------------------------------
        
def credspread_deltapct_shift_pv0(yc ,shiftsize, stf , syc , Party , dcount, dunit,*rest):
    #print (str)(dcount) + (str)(dunit[0])
    #yc = ael.YieldCurve['CDIssuerCurve']
    ael.poll()
    pv = 0
    yc=yc.clone()
    for member in yc.attributes().members():
    ###########  
        if (str)(member.issuer_ptynbr.display_id()) == Party:
    #########        
            #print dir(member.spreads().members())
            #member.spreads().members().sort()

            tf = ael.TradeFilter[stf] 
            if tf == None:
#                print 'TradeFilter', "'" + stf + "'", 'not found. Note TradeFilter is case sensitive'
                return -99999999999.0
#            print (str)(member.issuer_ptynbr.display_id())
            pv = tf.present_value()
                  
    return pv

import ael, time
debug = 0

# ---------------------------------------------------------------------------
# CS01_Choose the shift size - used for Attribute type curves such as CDISSUERCURVE_HR
# ---------------------------------------------------------------------------

def credspread_delta_shift_pv1(yc ,shiftsize, stf , syc , Party , dcount, dunit,*rest):
    #print (str)(dcount) + (str)(dunit[0])
    #yc = ael.YieldCurve['CDIssuerCurve']
    ael.poll()
    pv = 0
    pv0 = 0
    yc=yc.clone()
    for member in yc.attributes().members():
    ###########  
        if (str)(member.issuer_ptynbr.display_id()) == Party:
    #########        
            #print dir(member.spreads().members())
            #member.spreads().members().sort()

            tf = ael.TradeFilter[stf] 
            if tf == None:
#                print 'TradeFilter', "'" + stf + "'", 'not found. Note TradeFilter is case sensitive'
                return -99999999999.0
#            print (str)(member.issuer_ptynbr.display_id())
            pv0 = tf.present_value()
                  
#            for SpreadMember in member.spreads().members():
#                Test1 = SpreadMember.clone()
#                #print Test1.spread        
            
            for SpreadMember in member.spreads().members():
                if (str)(SpreadMember.point_seqnbr.date_period) == (str)(dunit):
                    Test1 = SpreadMember.clone()
                    spr0 = Test1.spread
                    Test1.spread = Test1.spread + shiftsize
                    Test1.apply()
                    yc.simulate()
                    pv = tf.present_value()
                    Test1.revert_apply()
                    yc.unsimulate()
#                    print 'Issuer ',(str)(member.issuer_ptynbr.display_id()),' pv0 ', pv0, ' pv1 ', pv1,' dunit = ' , dunit, ' date_period = ', SpreadMember.point_seqnbr.date_period,' spr0 = ',spr0, ' spr1 = ', Test1.spread

    return pv
        

# ---------------------------------------------------------------------------
# CS1% - used for Attribute type curves such as CDISSUERCURVE_HR
# ---------------------------------------------------------------------------
        
def credspread_deltapct_shift_pv1(yc ,shiftsize, stf , syc , Party , dcount, dunit,*rest):
    #print (str)(dcount) + (str)(dunit[0])
    #yc = ael.YieldCurve['CDIssuerCurve']
    ael.poll()
    pv = 0
    pv0 = 0
    yc=yc.clone()
    for member in yc.attributes().members():
    ###########  
        if (str)(member.issuer_ptynbr.display_id()) == Party:
    #########        
            #print dir(member.spreads().members())
            #member.spreads().members().sort()

            tf = ael.TradeFilter[stf] 
            if tf == None:
                print 'TradeFilter', "'" + stf + "'", 'not found. Note TradeFilter is case sensitive'
                return -99999999999.0
#            print (str)(member.issuer_ptynbr.display_id())
            pv0 = tf.present_value()
                  
#            for SpreadMember in member.spreads().members():
#                Test1 = SpreadMember.clone()
#                #print Test1.spread        
            
            for SpreadMember in member.spreads().members():
                if (str)(SpreadMember.point_seqnbr.date_period) == (str)(dunit):
                    Test1 = SpreadMember.clone()
                    spr0 = Test1.spread
                    Test1.spread = Test1.spread * shiftsize
                    Test1.apply()
                    yc.simulate()
                    pv = tf.present_value()
                    Test1.revert_apply()
                    yc.unsimulate()
#                    print 'Issuer ',(str)(member.issuer_ptynbr.display_id()),' pv0 ', pv0, ' pv1 ', pv1,' dunit = ' , dunit, ' date_period = ', SpreadMember.point_seqnbr.date_period,' spr0 = ',spr0, ' spr1 = ', Test1.spread

    return pv





