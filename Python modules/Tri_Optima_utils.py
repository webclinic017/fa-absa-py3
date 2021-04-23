'''Tri_Optima_utils: last updated on Wed Aug 19 14:35:46 2009. Extracted by Stowaway on 9/2/2009.'''
import ael, acm, re

#periods = ['1d','1w','1m','2m','3m','4m','5m','6m','7m','8m','9m','10m','11m','1y','13m','14m','15m','16m','17m','18m','19m','20m','21m','22m','23m','2y','3y','4y','5y','6y','7y','8y','9y','10y','11y','12y','13y','14y','15y','20y','25y','Rest']
periods = "'1d' '1w' '1m' '2m' '3m' '4m' '5m' '6m' '7m' '8m' '9m' '10m' '11m' '1y' '13m' '14m' '15m' '16m' '17m' '18m' '19m' '20m' '21m' '22m' '23m' '2y' '3y' '4y' '5y' '6y' '7y' '8y' '9y' '10y' '11y' '12y' '13y' '14y' '15y' '20y' '25y' 'Rest'"
#periods = ['1w', '1m','2m','3m', '4m']
def get_day(ins,cal,nbr,*rest):
    spot = ins.curr.spot_date()
    day = spot.add_period(periods[nbr])
    day = day.adjust_to_banking_day(cal).to_string()
    return day

a = acm.Time().CreateTimeBuckets(0, periods, None, None, 0, 0, 0, 0, 0, 0)

#a = acm.FTimeBuckets()
#a.SpotDays(0)
#a.Commit()
#for n in range(len(periods)):
#    a.AddBuckets(periods[n], periods[n].upper())
#a.Commit()
#print a.Inspect()

#for num in range(0,(a.Size())):
    #print num
#    print 'Bucket: ', a.At(num).BucketName(),'Start Date: ', acm.FTmServer.DtUtcToLocal(a.At(num).StartDate()),'End Date: ', a.At(num).EndDate()

def get_delta(trd,num,*rest):
    cal = ael.Calendar['ZAR Johannesburg']
    if num != 42:
        st = 0
        ed = ael.BIG_DATE
        if a.At(num).StartDate() != "":
            st = (ael.date((a.At(num).StartDate())[0:10])).adjust_to_banking_day(cal)
        if a.At(num).EndDate() != acm.Time.BigDate():
            ed = (ael.date((a.At(num).EndDate())[0:10])).adjust_to_banking_day(cal)
        return trd.benchmark_price_delta(None, None, st, ed)
    else:
        return trd.benchmark_price_delta(None, None, ael.date_today(), ael.BIG_DATE)
#t = ael.Trade[806965]
#print get_delta(t,0)
#print ael.BIG_DATE
