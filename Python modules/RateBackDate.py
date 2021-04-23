import acm
import ABSABackDate
import ael

#Date           Who                         What              CR number                     
#2009-05-04     Willie van der Bank         Created           1369

def CallAccRateBackDate(temp,instl,date,rate,payd,*rest):
    try:
        dates = []
        rates = []
        inslist = []
        payday = []
        dates.append(ael.date(date))
        rates.append(rate)
        inslist.append(acm.FInstrument[instl])
        payday.append(ael.date(payd))
        ABSABackDate.backDateRate(inslist, dates, rates, payday)
        return 'Done'
    except AttributeError, err:
        return 'Not done'

#print CallAccRateBackDate('528695-ZAR-2201-01','29/05/2009',19,'29/05/2009')
