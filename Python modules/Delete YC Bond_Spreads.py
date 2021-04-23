# once off script to delete a YC and the corresponding VPS curves of the curve 'Bond_Spreads'


import ael

yc = ael.YieldCurve['Bond_Spreads']

ref = yc.reference_in(1)

for b in ref:
    try:
        b.delete()
    except:
        print(b.display_id(), 'this yield curve could not be deleted')
  
try:
    yc.delete()
except:
    print(yc.yield_curve_name, 'current YC could not be delted')

        
yc_check = ael.YieldCurve['Bond_Spreads']        
if not yc_check:
    print(' the Bond_Spreads curve has been deleted')


