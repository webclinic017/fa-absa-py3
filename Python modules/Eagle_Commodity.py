
import ael, string, acm

def InsCall(i,*rest):
    


    Instrument = acm.FInstrument[i.insaddr]
   
    CallOptionFLAG = Instrument.IsCallOption()

    return CallOptionFLAG

def InsAsian(i,*rest):
    


    Instrument = acm.FInstrument[i.insaddr]
        
    AsianOptionFLAG = Instrument.IsAsian()

    return AsianOptionFLAG
    
    
def OfSett(i,*rest):
        
    Unit = str(i.pay_day_offset)
    print(Unit)
    OffUnit = Unit + 'd' 
    print(OffUnit)
    return OffUnit
