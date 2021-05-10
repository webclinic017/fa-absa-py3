'''

Used to return the value of a spread from the yield curve definition = 'ZAR-CORPBONDS-SPREADS' 
or None if the spraed has not been defined

Change          Date            Coded By


CHNG0003808399  19 July 2016    Anil Parbhoo




'''

import acm
sp = []

for i in acm.FInstrumentSpread.Select(''):
    if i.Curve().Name()== 'ZAR-CORPBONDS-SPREADS':
        sp.append ((i.Instrument().Name(), str(i.Spread()*100)))
        
def corres_spread(i):
    for s in sp:
        if i == s[0]:
            return s[1]


