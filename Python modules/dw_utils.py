import ael, time
debug = 0

# ---------------------------------------------------------------------------
# CS01_Choose the shift size - used for Attribute type curves such as CDISSUERCURVE_HR
# ---------------------------------------------------------------------------

def credspread_delta_shift(yc ,shiftsize, stf , syc , Party , *rest):

    #yc = ael.YieldCurve['CDIssuerCurve']
    yc=yc.clone()

    for member in yc.attributes().members():

    ###########    
        if (str)(member.issuer_ptynbr.display_id()) == Party:
    #########        
            #print dir(member.spreads().members())
            member.spreads().members().sort()
import acm
debug = 0


class CalcSpace(object):

    calcSpace = acm.Calculations().CreateStandardCalculationsSpaceCollection()

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
                if shifttype in ['delta_shift', 'delta']:
                    spreadClone.Spread=spreadClone.Spread()+shiftsize
                elif shifttype in ['deltapct', 'deltapct_shift']:
                    spreadClone.Spread=spreadClone.Spread()*shiftsize
                spread.Apply(spreadClone)
            
            #yc.SimulateCurve()
            pv1=tf_calc.PresentValue(CalcSpace.calcSpace).Number()
            pv01 = pv1-pv0
            yc.Undo()
            print Party, pv0, pv1, pv01
            return pv01
    

# ---------------------------------------------------------------------------
# CS01_Choose the shift size - used for Attribute type curves such as CDISSUERCURVE_HR
# ---------------------------------------------------------------------------
def credspread_delta_shift(yc ,syc, stf, ycname, Party , *rest):
    #ycname=yc.yield_curve_name
    shifttype='delta_shift'
    shiftsize=syc
    return credspread_delta_generic(ycname, shiftsize, stf, Party, shifttype)

# ---------------------------------------------------------------------------
# CS01 - used for Attribute type curves such as CDISSUERCURVE_HR
# ---------------------------------------------------------------------------    
def credspread_delta(yc ,syc, stf, ycname, Party , *rest):
    #ycname=yc.yield_curve_name
    shifttype='delta'
    shiftsize=0.0001
    return credspread_delta_generic(ycname, shiftsize, stf, Party, shifttype)

# ---------------------------------------------------------------------------
# CS1% - used for Attribute type curves such as CDISSUERCURVE_HR
# --------------------------------------------------------------------------- 
def credspread_deltapct(yc ,syc, stf, ycname, Party , *rest):
    #ycname=yc.yield_curve_name
    shifttype='deltapct'
    shiftsize=1.01
    return credspread_delta_generic(ycname, shiftsize, stf, Party, shifttype)

# ---------------------------------------------------------------------------
# CS1% - used for Attribute type curves such as CDISSUERCURVE_HR
# ---------------------------------------------------------------------------
def credspread_deltapct_shift(yc ,syc, stf, ycname, Party , *rest):
    #ycname=yc.yield_curve_name
    shifttype='deltapct_shift'
    shiftsize=syc
    return credspread_delta_generic(ycname, shiftsize, stf, Party, shifttype)


def insSpread_delta(yc, stf, Party, *rest):
    yc=acm.FYieldCurve[yc.yield_curve_name]
    for spread in yc.InstrumentSpreads():
        if spread.Instrument().Name()==Party:
            if debug == 1:
                print 'Initial Spread', spread.Spread()
            
            tf=acm.FTradeSelection[stf]
            if tf == None:
                print 'TradeFilter', "'" + stf + "'", 'not found. Note TradeFilter is case sensitive'

            tf_calc = tf.Calculation()
            pv0=tf_calc.PresentValue(CalcSpace.calcSpace).Number()
            
            spreadClone=spread.Clone()
            spreadClone.Spread=spread.Spread()+0.0001
            
            spread.Apply(spreadClone)
            
            if debug == 1:
                print 'Updated Spread', spread.Spread()
            
            pv1 = tf_calc.PresentValue(CalcSpace.calcSpace).Number()
            
            pv01 = pv1-pv0
            yc.Undo()
            
            print 'Instrument', spread.Instrument().Name(), 'pv0', pv0, 'pv1', pv1, 'pv01', pv01
            return pv01
            
            
#print credspread_deltapct(ael.YieldCurve['CDIssuerCurve_HR'],0.0001,'CredDer_All','BARLOWORLD LIMITED')


#Old 3.2.2. code no longer working in 4.3
# ---------------------------------------------------------------------------
# CS01_Choose the shift size - used for Attribute type curves such as CDISSUERCURVE_HR
# ---------------------------------------------------------------------------
'''
def credspread_delta_shift(yc ,shiftsize, stf , syc , Party , *rest):
    #yc = ael.YieldCurve['CDIssuerCurve']
    yc=yc.clone()
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
                Test1.spread = Test1.spread + shiftsize
                Test1.apply()
                #print Test1.spread
            
            #yc.calculate()
            yc.simulate()  
            
            pv1 = tf.present_value()
            pv01 = pv1 - pv0
            
            for SpreadMember in member.spreads().members():
                Test2 = SpreadMember.clone()
                Test2.spread = Test2.spread - shiftsize
                Test2.apply()
                #print Test2.spread

            #yc.calculate()
            yc.simulate()
            pv2 = tf.present_value()  
            pv02 = pv2 - pv0
            print (str)(member.issuer_ptynbr.display_id()), pv0, pv1, pv01 , pv02
    return pv01
        

# ---------------------------------------------------------------------------
# CS01 - used for Attribute type curves such as CDISSUERCURVE_HR
# ---------------------------------------------------------------------------

def credspread_delta(yc , stf , syc , Party , *rest):
    #yc = ael.YieldCurve['CDIssuerCurve']
    yc=yc.clone()
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
            print (str)(member.issuer_ptynbr.display_id()), pv0, pv1, pv01 , pv02
    return pv01
        
# ---------------------------------------------------------------------------
# CS1% - used for Attribute type curves such as CDISSUERCURVE_HR
# ---------------------------------------------------------------------------
        
def credspread_deltapct(yc , stf , syc , Party , *rest):
    #yc = ael.YieldCurve['CDIssuerCurve']
    yc=yc.clone()
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
            print (str)(member.issuer_ptynbr.display_id()), pv0, pv1, pv01 , pv02
    return pv01        

# ---------------------------------------------------------------------------
# CS1% - used for Attribute type curves such as CDISSUERCURVE_HR
# ---------------------------------------------------------------------------
        
def credspread_deltapct_shift(yc ,shiftsize, stf , syc , Party , *rest):
    #yc = ael.YieldCurve['CDIssuerCurve']
    yc=yc.clone()
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
                Test1.spread = Test1.spread * shiftsize
                Test1.apply()
                #print Test1.spread
            
            #yc.calculate()
            yc.simulate()  
            
            pv1 = tf.present_value()
            pv01 = pv1 - pv0
            

            for SpreadMember in member.spreads().members():
                Test2 = SpreadMember.clone()
                Test2.spread = Test2.spread / shiftsize
                Test2.apply()
                #print Test2.spread
            
            #yc.calculate()
            yc.simulate()
            pv2 = tf.present_value()  
            pv02 = pv2 - pv0
            print (str)(member.issuer_ptynbr.display_id()), pv0, pv1, pv01 , pv02
    return pv01        



# ---------------------------------------------------------------------------
# CS01 for Instrument Spread curves i.e. ABACAS
# ---------------------------------------------------------------------------

def insSpread_delta(yc , stf ,  Party , *rest):
    yc=yc.clone()
    #yc = ael.YieldCurve['PM-SWAP_CS']
    #stf = 'MR_Abacas_All'
    #Party = 'AUTO44-Spec'
    
    #print ' Begin'
    #print dir(yc)
    #print dir(yc.instrument_spreads)
    #print yc.pp()
    #print yc.instrument_spreads().pp()
    for member1 in yc.instrument_spreads().members():
        if Party == member1.instrument.insid:
            if debug == 1:
                print 'Initial Spread', member1.spread
            
            tf = ael.TradeFilter[stf] 
            if tf == None:
                print 'TradeFilter', "'" + stf + "'", 'not found. Note TradeFilter is case sensitive'
                #return -99999999999.0
            
            pv0 = tf.present_value()        
            
            Test1 = member1.clone()
            Test1.spread = Test1.spread + 0.0001
            
            Test1.apply()
            #yc.calculate()
            yc.simulate() 
            if debug == 1:  
                print 'Updated Spread',Test1.spread
            
            pv1 = tf.present_value()        
       
            Test1.spread = Test1.spread - 0.0001
            Test1.apply()
            #yc.calculate()
            yc.simulate()        
    
            if debug == 1:  
                print 'Updated 2 Spread',Test1.spread
            
            pv01 = pv1 - pv0
            print 'Instrument',member1.instrument.insid,'pv0',pv0,'pv1',pv1,'pv01',pv01
            return pv01


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
                Test1.spread = Test1.spread + shiftsize
                Test1.apply()
                #print Test1.spread
            
            #yc.calculate()
            yc.simulate()  
            
            pv1 = tf.present_value()
            pv01 = pv1 - pv0
            
            for SpreadMember in member.spreads().members():
                Test2 = SpreadMember.clone()
                Test2.spread = Test2.spread - shiftsize
                Test2.apply()
                #print Test2.spread

            #yc.calculate()
            yc.simulate()
            pv2 = tf.present_value()  
            pv02 = pv2 - pv0
            print (str)(member.issuer_ptynbr.display_id()), pv0, pv1, pv01 , pv02
    return pv01
        

# ---------------------------------------------------------------------------
# CS01 - used for Attribute type curves such as CDISSUERCURVE_HR
# ---------------------------------------------------------------------------

def credspread_delta(yc , stf , syc , Party , *rest):
    #yc = ael.YieldCurve['CDIssuerCurve']
    yc=yc.clone()
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
            print (str)(member.issuer_ptynbr.display_id()), pv0, pv1, pv01 , pv02
    return pv01
        
# ---------------------------------------------------------------------------
# CS1% - used for Attribute type curves such as CDISSUERCURVE_HR
# ---------------------------------------------------------------------------
    
def credspread_deltapct(yc , stf , syc , Party , *rest):

    #yc = ael.YieldCurve['CDIssuerCurve']
    yc = yc.clone()

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
            print (str)(member.issuer_ptynbr.display_id()), pv0, pv1, pv01 , pv02

    return pv01        

# ---------------------------------------------------------------------------
# CS1% - used for Attribute type curves such as CDISSUERCURVE_HR
# ---------------------------------------------------------------------------
        
def credspread_deltapct_shift(yc ,shiftsize, stf , syc , Party , *rest):
    #yc = ael.YieldCurve['CDIssuerCurve']
    yc=yc.clone()
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
                Test1.spread = Test1.spread * shiftsize
                Test1.apply()
                #print Test1.spread
            
            #yc.calculate()
            yc.simulate()  
            
            pv1 = tf.present_value()
            pv01 = pv1 - pv0
            

            for SpreadMember in member.spreads().members():
                Test2 = SpreadMember.clone()
                Test2.spread = Test2.spread / shiftsize
                Test2.apply()
                #print Test2.spread
            
            #yc.calculate()
            yc.simulate()
            pv2 = tf.present_value()  
            pv02 = pv2 - pv0
            print (str)(member.issuer_ptynbr.display_id()), pv0, pv1, pv01 , pv02
    return pv01        



# ---------------------------------------------------------------------------
# CS01 for Instrument Spread curves i.e. ABACAS
# ---------------------------------------------------------------------------

def insSpread_delta(yc , stf ,  Party , *rest):
    yc=yc.clone()
    #yc = ael.YieldCurve['PM-SWAP_CS']
    #stf = 'MR_Abacas_All'
    #Party = 'AUTO44-Spec'
    
    #print ' Begin'
    #print dir(yc)
    #print dir(yc.instrument_spreads)
    #print yc.pp()
    #print yc.instrument_spreads().pp()
    for member1 in yc.instrument_spreads().members():
        if Party == member1.instrument.insid:
            if debug == 1:
                print 'Initial Spread', member1.spread
            
            tf = ael.TradeFilter[stf] 
            if tf == None:
                print 'TradeFilter', "'" + stf + "'", 'not found. Note TradeFilter is case sensitive'
                #return -99999999999.0
            
            pv0 = tf.present_value()        
            
            Test1 = member1.clone()
            Test1.spread = Test1.spread + 0.0001
            
            Test1.apply()
            #yc.calculate()
            yc.simulate() 
            if debug == 1:  
                print 'Updated Spread',Test1.spread
            
            pv1 = tf.present_value()        
       
            Test1.spread = Test1.spread - 0.0001
            Test1.apply()
            #yc.calculate()
            yc.simulate()        
    
            if debug == 1:  
                print 'Updated 2 Spread',Test1.spread
            
            pv01 = pv1 - pv0
            print 'Instrument',member1.instrument.insid,'pv0',pv0,'pv1',pv1,'pv01',pv01
            return pv01
'''
