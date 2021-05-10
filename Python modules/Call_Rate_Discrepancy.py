import ael

#Date           Who                     CR Number       What
#2008-07-16     Heinrich Cronje                         Create

#Description
#latestCallRate:  This function gives the current rate of a call account
#ratesNotChanged: This function returns a boolean. If the call account
#                 had a rate change on the specified date then a 0 is sent
#                 back other wise a 1 is sent back.
#dealer:          This function returns the dealer id of the last Fixed Amount

def latestCallRate(temp,trdnbr,*rest):
    t = ael.Trade[trdnbr]
    i = t.insaddr
    endDay = ael.date('1970-01-01')
    rate = 0
    
    if i.legs().members() != [] and i.legs()[0].type == 'Call Fixed Adjustable':
        for cf in i.legs()[0].cash_flows():
            if cf.type == 'Call Fixed Rate Adjustable':
                for r in cf.resets():
                    if r.end_day > endDay:
                        endDay = r.end_day
                        rate = r.value
    
    return rate

def ratesNotChanged(temp,trdnbr,date,*rest):
    t = ael.Trade[trdnbr]
    i = t.insaddr
    startDay = 0
    endDay = 0
    rate1 = 0
    rate2 = 0
    
    if i.legs().members() != [] and i.legs()[0].type == 'Call Fixed Adjustable':
        for cf in i.legs()[0].cash_flows():
            if cf.type == 'Call Fixed Rate Adjustable':
                for r in cf.resets():
                    if r.end_day == date:
                        endDay = 1
                        rate1 = r.value
                        
                    if r.start_day == date:
                        startDay = 1
                        rate2 = r.value
    
    if endDay and startDay and rate1 != rate2:
        return 0
        
    return 1

def dealer(temp,trdnbr,*rest):
    t = ael.Trade[trdnbr]
    i = t.insaddr
    
    payDay = ael.date('1970-01-01')
    dealer = ''
    
    if i.legs().members() != [] and i.legs()[0].type == 'Call Fixed Adjustable':
        for cf in i.legs()[0].cash_flows():
            if cf.type == 'Fixed Amount':
                if payDay < cf.pay_day:
                    payDay = cf.pay_day
                    dealer = cf.creat_usrnbr.userid
    
    return dealer
