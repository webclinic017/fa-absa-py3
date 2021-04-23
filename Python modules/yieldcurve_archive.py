import ael


ycs = ael.YieldCurve.select()
cnt = 0
for yc in ycs:
    if yc.yield_curve_name.find('2017-') >1:
        ycc = yc.clone()
        
        ycc.archive_status = 1
        ycc.commit()
        print yc.yield_curve_name, '..done'
        cnt+=1
        
print '...', cnt
