import ael, math
def get_variance(i,*rest):
    exev = i.exotic_events()
    totlist = []
    for e in exev:
        elist = []
        if e.value != -1:
            elist.append(ael.date(e.date))
            elist.append(e.value)
            totlist.append(elist)
    totlist.sort()
    totlist.reverse()
    i = 0
    sum = 0
    while i < (len(totlist) - 1):
        r = math.log(totlist[i][1] / totlist[i+1][1])
        rr = r * r
#        print rr,';',totlist[i][0],';',totlist[i+1][0]
        sum = sum + rr
        i = i + 1    
    i = i + 1
#    print sum, i
    return sum / i
    
#print 'Result = ', get_variance(ael.Instrument['NO ID2/#192'])

def create_strikes(i, strike):
    call = []
    put = []
    i = 0
    while i <= 25:
        call.append(strike * (1 + (i * 0.02)))
        put.append(strike * (1 - (i * 0.02)))
        i = i + 1
    return call, put

def f_weight(strike, days, spot):
    return 2/days * ((strike-spot)/spot - math.log(strike/spot))

def timefromstart(i,*rest):
    exev = i.exotic_events()
    j = 0.00
    k = 0.00
    z = 0.01
    for e in exev:
        k = k + 1
        if e.value != -1:
            j = j + 1
    if j !=k:
        z = (j+1)/k
    else:
        z = j/k
    #print j, ' ',k,' ',z
    return z
    
def timetoend(i,*rest):
    exev = i.exotic_events()
    j = 0.00
    k = 0.00
    z = 0.01
    for e in exev:
        k = k + 1
        if e.value == -1:
            j = j + 1
    if j == 0:
        z = j/k
    else:
        z = (j-1)/k
    #print j, ' ',k,' ',z
    return z
    
def calc_fk(i, list, spot):
    days = ael.date_today().days_between(i.exp_day, 'Act/365')
    days = days / 365.000
    k = 0
    #print 'Strike      ', 'FK'
    matrix = []
    row = []
    while k < len(list):
        fk = f_weight(list[k], days, spot)
        #print list[k],fk
        row.append(list[k])
        row.append(fk)
        matrix.append(row)
        row = []
        k = k + 1
    return matrix
    
def calc_wc(matrix, put):
    l = 0
    sum = 0
    finmatrix = []
 #   print 'Strike              ', 'FK             ','OWC           ','WC'
    while l < (len(matrix)-1):
        #print 'l+1val ',matrix[l+1][1],'lval ',matrix[l][1],'lstrike ',matrix[l][0],'l+1strike ',matrix[l+1][0]
        if put == 1:
            #print 'if'
            wc = (matrix[l+1][1] - matrix[l][1]) / (matrix[l][0] - matrix[l+1][0]) * 10000
        else:
            #print 'else',(matrix[l+1][1] - matrix[l][1]),'2de', (matrix[l+1][0] - matrix[l][0])
            wc = (matrix[l+1][1] - matrix[l][1]) / (matrix[l+1][0] - matrix[l][0]) * 10000
        owc = wc
        wc = wc - sum
        sum = sum + wc
#        print matrix[l],';',owc,';',wc
        finmatrix.append([matrix[l][0], matrix[l][1], wc])
        l = l + 1
    return finmatrix

def create_Output(tf, outfile):
    try:
        f = open(outfile, 'w')
    except:
        print 'Could not open the output file.'
        return
    f.write('TradeNumber;TradeId;Currency;ValueDay;ExpiryDay;Counterparty;Portfolio;Trader;ContractSize;Underlying;UnderlyingType;Quantity;Nominal;OptionType;OptionStrike;NumberofOptions;RealisedVariance;TimeFromStart;TimeToEnd;UnderlyingVolSurface;Status;UnderlyingStrike;BusinessDate\n')
    f.write('\n')
    for t in ael.TradeFilter[tf].trades():
        timeFrmStrt = (str)(timefromstart(t.insaddr)) #t.value_day.days_between(ael.date_today(),'Act/365') / 365.00
        timeToExp = (str)(timetoend(t.insaddr)) #ael.date_today().days_between(t.insaddr.exp_day,'Act/365') / 365.00
        
        #date formats
        val_date = t.value_day.to_string('%Y-%m-%d')
        exp_date = t.insaddr.exp_day.to_string('%Y-%m-%d')
        bus_date = ael.date_today().to_string('%Y-%m-%d')
        
        #print dir(t.insaddr)
        #print t.trdnbr, t.insaddr.used_und_price(),'tfs ',timeFrmStrt,' tte ',timeToExp    
        opt_strikes = create_strikes(t.insaddr, t.insaddr.used_und_price())
        matc = calc_fk(t.insaddr, opt_strikes[0], t.insaddr.used_und_price())
        matp = calc_fk(t.insaddr, opt_strikes[1], t.insaddr.used_und_price())
        volsurface = t.insaddr.used_volatility().vol_name
        #print matc
        #print matp
        #print '*****Call******'
        cfin = calc_wc(matc, 0)
        relvar = (str)(get_variance(t.insaddr))
        if t.prfnbr:
            port = t.prfnbr.prfid
        else:
            port = 'NoPortfolio'
        for c in cfin:
            f.write((str)(t.trdnbr) + ';' + (str)(t.insaddr.insid) + ';' + (str)(t.insaddr.curr.insid) + ';' + val_date + ';' + exp_date + ';' + (str)(t.counterparty_ptynbr.ptyid) + ';' + port + ';'  + (str)(t.trader_usrnbr.userid) + ';' + (str)(t.insaddr.contr_size) + ';' + t.insaddr.und_insaddr.insid + ';'  + t.insaddr.und_instype + ';'  + (str)(t.quantity) + ';' + (str)(t.nominal_amount()) + ';Call;' + (str)(c[0]) + ';' + (str)(c[2]) + ';' + relvar + ';' + (str)(timeFrmStrt) + ';' + (str)(timeToExp) + ';' + volsurface + ';' + (str)(t.status) + ';' + (str)(t.price) + ';' + bus_date + '\n')
        #+ t.prfnbr.prfid
        #print cfin
        #print '*****Put******'
        pfin = calc_wc(matp, 1)
        for p in pfin:
            f.write((str)(t.trdnbr) + ';' + (str)(t.insaddr.insid) + ';'+ (str)(t.insaddr.curr.insid) + ';' + val_date + ';' + exp_date + ';' + (str)(t.counterparty_ptynbr.ptyid) + ';' + port + ';'  + (str)(t.trader_usrnbr.userid) + ';' + (str)(t.insaddr.contr_size) + ';'  + t.insaddr.und_insaddr.insid + ';' + t.insaddr.und_instype + ';'  + (str)(t.quantity) + ';' + (str)(t.nominal_amount()) + ';Put;' + (str)(p[0]) + ';' + (str)(p[2]) + ';' + relvar + ';' + (str)(timeFrmStrt) + ';' + (str)(timeToExp) + ';' + volsurface + ';' + (str)(t.status) + ';' + (str)(t.price) + ';' + bus_date + '\n')
        #+ t.prfnbr.prfid 
        #print pfin
    f.close()
#create_Output('MR_VARSWAP','f:/SAMR_VARIANCESWAP.CSV') #/services/front/scripts/dart/ERM/SAMR_VARIANCESWAP.CSV')
