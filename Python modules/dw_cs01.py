import ael, time


# ---------------------------------------------------------------------------
# CS01
# ---------------------------------------------------------------------------

def credspread_delta(yc , stf , syc , Party , *rest):
    #yc = ael.YieldCurve['CDIssuerCurve']
    for member in yc.attributes().members():
    ###########    
        if (str)(member.issuer_ptynbr.display_id()) == Party:
    #########        
            #print dir(member.spreads().members())
            member.spreads().members().sort()

            tf = ael.TradeFilter[stf] 
            if tf == None:
                print 'TradeFilter', "'" + stf + "'", 'not found. Note TradeFilter is case sensitive'
                return -99999999999.0
            
            pv0 = tf.present_value()
            
            
            for SpreadMember in member.spreads().members():
                Test1 = SpreadMember.clone()
                #print Test1.spread        
            for SpreadMember in member.spreads().members():
                Test1 = SpreadMember.clone()
                Test1.spread = Test1.spread + 0.0001
                Test1.apply()
                #print Test1.spread
            
            #yc.calculate()
            yc.simulate()  
            
            pv1 = tf.present_value()
            pv01 = pv1 - pv0
            
            for SpreadMember in member.spreads().members():
                Test2 = SpreadMember.clone()
                Test2.spread = Test2.spread - 0.0001
                Test2.apply()
                #print Test2.spread

            #yc.calculate()
            yc.simulate()
            pv2 = tf.present_value()  
            pv02 = pv2 - pv0
            print (str)(member.issuer_ptynbr.display_id()), pv0, pv1, pv01, pv02
    return pv01
        
# ---------------------------------------------------------------------------
# CS1%
# ---------------------------------------------------------------------------
        
def credspread_deltapct(yc , stf , syc , Party , *rest):
    #yc = ael.YieldCurve['CDIssuerCurve']

    for member in yc.attributes().members():
    ###########    
        if (str)(member.issuer_ptynbr.display_id()) == Party:
    #########        
            #print dir(member.spreads().members())
            member.spreads().members().sort()
            
            tf = ael.TradeFilter[stf] 
            if tf == None:
                print 'TradeFilter', "'" + stf + "'", 'not found. Note TradeFilter is case sensitive'
                return -99999999999.0
            
            pv0 = tf.present_value()
            
            
            for SpreadMember in member.spreads().members():
                Test1 = SpreadMember.clone()
                #print Test1.spread        
            for SpreadMember in member.spreads().members():
                Test1 = SpreadMember.clone()
                Test1.spread = Test1.spread * 1.01
                Test1.apply()
                #print Test1.spread
            
            #yc.calculate()
            yc.simulate()  
            
            pv1 = tf.present_value()
            pv01 = pv1 - pv0
            

            for SpreadMember in member.spreads().members():
                Test2 = SpreadMember.clone()
                Test2.spread = Test2.spread / 1.01
                Test2.apply()
                #print Test2.spread
            
            #yc.calculate()
            yc.simulate()
            pv2 = tf.present_value()  
            pv02 = pv2 - pv0
            print (str)(member.issuer_ptynbr.display_id()), pv0, pv1, pv01, pv02
    return pv01        
