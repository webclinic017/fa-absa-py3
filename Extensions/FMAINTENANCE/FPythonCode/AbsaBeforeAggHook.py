import acm
#This was needed since Absa has an override for Dividend comparison method.  
#[ABSA Specific 4.3]FUndefinedObject:pLDividendComparisonMethodOverride = var("Trade day vs ex div day", "enum(DividendComparisonMethod)");
#They compare the TradeTime + spot days to the ex-div day to determine if a stock trade will get a dividend.
#However the Aggregation always uses the default, i.e. comparing the acquire day to the ex-div day
#Some old trades (before 2009) did not follow the spot day convention, i.e. trade=value=acquire day.
#For these trades the aggregation would cause differences.
#This script updates the val/acq dates to follow the spot day convention, in which case the two
#dividend comparison methods are equivalent and therefore agg is not causing diffs.


def absa_before_agg_hook(filters):
    for filter in filters:
        f = acm.FTradeSelection[filter]
        if f:
            print '\nStarting to check trades in Filter:', f.Name()
            trades = f.Trades()  
            fixed={}

            cnt=0
            for t in trades:
                ins = t.Instrument()
                ins_name=ins.Name()
                if ins.InsType() == 'Stock':

                    tobe = ins.Currency().Legs()[0].PayCalendar().AdjustBankingDays(t.TradeTime(), ins.SpotBankingDaysOffset()) 
                    if tobe <> t.ValueDay() or tobe <> t.AcquireDay():
                    
                        if ins_name in fixed: fixed[ins_name] = fixed[ins_name] +1
                        else: fixed[ins_name] = 1
                        
                        print '*'*5, 'Updated Val and/or Acquire day:', t.Oid(), t.ValueDay(), t.AcquireDay(), ' --> ', tobe
                        t.ValueDay(tobe) 
                        t.AcquireDay(tobe)
                        
                        cnt+=1
                        try:
                            t.Commit()
                        except Exception, e:
                            print '------ERROR commiting this trade:', t.Oid()
                            print e
                            raise
                
            
            print '\nSummary for filter %s :' %f.Name()
            if len(fixed.keys()) ==0: print 'No updates done for this filter'
            for k in sorted(fixed):
                print k, fixed[k]

    print 'Done updating Val/Acquire dates'

