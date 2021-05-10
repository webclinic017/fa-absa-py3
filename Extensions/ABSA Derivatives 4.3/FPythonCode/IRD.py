
import acm

def floatRateCF(trade):
    ins = trade.Instrument()
    if ins.InsType()!='Swap':
        return 'Not a Swap'
    elif ins.InsType()=='Swap':
        if not ins.IsFixedFloatSwap():
            ml=[]
            all_legs = ins.Legs()
            for f in all_legs:
                ml.append(f.LegType())
            return ml[0]+ ' VS. ' + ml[1]+ ' Swap'
            
        elif ins.IsFixedFloatSwap():
            legs = ins.Legs()
            for l in legs:
                if l.LegType()=='Float' and (not l.PayLeg()) and trade.Quantity()>=0:
                    return 'Receive Floating'
                elif l.LegType()=='Float' and (l.PayLeg()) and trade.Quantity()>=0:
                    return 'Pay Floating'
                elif l.LegType()=='Float' and (not l.PayLeg()) and trade.Quantity()<0:
                    return 'Pay Floating'
                elif l.LegType()=='Float' and (l.PayLeg()) and trade.Quantity()<0:
                    return 'Receive Floating'
                
                
                
