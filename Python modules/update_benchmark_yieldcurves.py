import acm, datetime

#Due to a bug - see AR 666511 / SPR 341880, we can not have Benchmark curves set to realtime updated
# (if there is a spread curve that depends on it)
#It was decided to keep it simple and set all benchmark curves to realtime updated = False and
#recalculate them periodically with this script.



def calc_all_benchmark_curves_with_updates():
    print 'Updating/re-calculating all Benchmark curves where a benchmark instrument had a price update after the curve was Calculated.\n\n'
    failed = []
    for yc in acm.FBenchmarkCurve.Select(''):
        for bm in yc.Benchmarks():
            bmi = bm.Instrument()
            for p in  bmi.Prices():
                if p.UpdateTime() > yc.UpdateTime():
                    print 'Need to recalc yc (%s), benchmark instrument (%s) had a price update @ %s.' % (yc.Name(), bmi.Name(), str(datetime.datetime.fromtimestamp(p.UpdateTime())) ),
                    try:
                        yc.RealTimeUpdated(False)
                        yc.Calculate()
                        yc.Commit()
                        print 'Updated OK.'
                    except Exception, e:
                        print '\nError re-caclcing yc (%s)' % (yc.Name())
                        print e
                        failed.append(yc.Name())
                        
    if len(failed) >0:
        print '\n\nThese curves could not re-calc and/or commit the save:'
        for ycname in failed:
            print ycname
        msg = 'Some YCs could not recalc/update, please check.  More detail in log above.'
        print msg
        raise Exception(msg)
            
    print '\nDone with all required re-calcs'
                    
ael_variables=[]

def ael_main(dict):
    calc_all_benchmark_curves_with_updates()
