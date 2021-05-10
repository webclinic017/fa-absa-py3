import ael

def ycp(pyc):
    yc = pyc[0][0]
    s = ''
    lst = []
    MyYc=ael.YieldCurve[yc]
    pts = MyYc.points()    
    for y in pts:
        lst.append(y.date_period)    
    
    for p in lst:
        if s == '':
            s = s + p
        else:
            s = s + ', ' + p
            
    return s

"""  
parm = [['ZAR-SWAP']]
print ycp(parm)
"""
