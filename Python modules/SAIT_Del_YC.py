import ael
 

#print dir(ael)
 
#def yc_del(temp, y, *rest):
count = 0
ycs = ael.YieldCurve #Volatility
for y in ycs:
    #if y.vol_name[0] + y.vol_name[1] + y.vol_name[2] == 'TBR':
    #if y.yield_curve_name[0] + y.yield_curve_name[1] + y.yield_curve_name[2] + y.yield_curve_name[3] == 'TBR_B':
    if y.yield_curve_name == 'TBR_ZAR-SWAP1': #in ('TBR_ZAR-SWAP-LIN','TBR_USD-SWAP-LIN','TBR_ZAR-SWAP-lin RT','TBR_ZAR-SWAP-cubic'):
        print(y.yield_curve_name)
        #print dir(y)
        
        #YieldCurvePoint
        #Benchmarks
        
        yc = y.clone()
        
        for b in yc.benchmarks():
            b.delete()
            print('deleted')
            
        for p in yc.points():
            p.delete()
            pass
            
        
        yc.commit()
 
        for x in y.reference_in():
            print('xxxxxxx111111111', x.pp())
        
            if x.record_type == 'YieldCurve':
                if x.yield_curve_name.find('ZAR-SWAP1') != -1:
                #if x.yield_curve_name == 'ZAR-SWAP1':
                    x.delete()
                    #pass
                    print(x.yield_curve_name)
            else:
                print('xxxxx', x.pp())
        
        for z in y.reference_out():
            print('zzzzzzz', z.pp())
        #y.delete()
        try:
            n = y.yield_curve_name
            y.delete()
            print(n, ' HAS BEEN DELETED')
            count = count + 1
        except:
            print('could not delete ', y.yield_curve_name)
 
        '''
        try:
            y.delete()
            count = count + 1
        except:
            print 'Cannot delete YC ', y.yield_curve_name
        '''
        
print(count, 'curves updated')
        
        
    
    
