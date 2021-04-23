import ael, math, string

def get_nomcurr(cpair):
    nomcur = {'XAUUSD':'XAU','USDXAU':'XAU','XAUZAR':'XAU','ZARXAU':'XAU','XAUXAU':'XAU','ZARZAR':'ZAR',
        'USDUSD':'USD','USDZAR':'USD','ZARUSD':'USD','EURUSD':'EUR','USDEUR':'EUR','EURZAR':'EUR',
        'ZAREUR':'EUR','GBPZAR':'GBP','ZARGBP':'GBP','GBPUSD':'GBP','USDGBP':'GBP','AUDUSD':'AUD',
        'USDAUD':'AUD','USDCHF':'USD','CHFUSD':'USD','JPYZAR':'ZAR','ZARJPY':'ZAR','USDJPY':'USD',
        'JPYUSD':'USD','AUDZAR':'AUD','ZARAUD':'AUD','CHFZAR':'CHF','ZARCHF':'CHF','XAGUSD':'XAG',
        'USDXAG':'XAG','XPTUSD':'XPT','USDXPT':'XPT','XPDUSD':'XPD','USDXPD':'XPD','XAGZAR':'XAG',
        'ZARXAG':'XAG','XPTZAR':'XPT','ZARXPT':'XPT','XPDZAR':'XPD','ZARXPD':'XPD','MALUSD':'MAL',
        'USDMAL':'MAL','MALZAR':'MAL','ZARMAL':'MAL','MCUUSD':'MCU','USDMCU':'MCU','MCUZAR':'MCU',
        'ZARMCU':'MCU','MNIUSD':'MNI','USDMNI':'MNI','MNIZAR':'MNI','ZARMNI':'MNI','MPBUSD':'MPB',
        'USDMPB':'MPB','MPBZAR':'MPB','ZARMPB':'MPB','MSNUSD':'MSN','USDMSN':'MSN','MSNZAR':'MSN',
        'ZARMSN':'MSN','MZNUSD':'MZN','USDMZN':'MZN','MZNZAR':'MZN','ZARMZN':'MZN','NGLDZAR':'ZAR',
        'ZARNGLD':'ZAR','BRT_CRD_OILUSD':'BRT_CRD_OIL','USDBRT_CRD_OIL':'BRT_CRD_OIL',
        'JET_FUELUSD':'JET_FUEL','USDJET_FUEL':'JET_FUEL','GAS_OILUSD':'GAS_OIL',
        'USDGAS_OIL':'GAS_OIL','DIESELUSD':'DIESEL','USDDIESEL':'DIESEL',
        'BRT_CRD_OILZAR':'BRT_CRD_OIL','ZARBRT_CRD_OIL':'BRT_CRD_OIL','JET_FUELZAR':'JET_FUEL',
        'ZARJET_FUEL':'JET_FUEL','GAS_OILZAR':'GAS_OIL','ZARGAS_OIL':'GAS_OIL','DIESELZAR':'DIESEL',
        'ZARDIESEL':'DIESEL','EURGBP':'EUR','GBPEUR':'EUR','EURJPY':'EUR','JPYEUR':'EUR',
        'USDNZD':'USD','NZDUSD':'USD','CADUSD':'USD','USDCAD':'USD','CADZAR':'CAD','ZARCAD':'CAD',
        'USDKES':'USD','KESUSD':'USD','USDZMK':'USD','ZMKUSD':'USD','USDBWP':'USD','BWPUSD':'USD',
        'USDNAD':'USD','NADUSD':'USD','USDNGN':'USD','NGNUSD':'USD','USDTZS':'USD','TZSUSD':'USD',
        'EURKES':'EUR','KESEUR':'EUR','EURZMK':'EUR','ZMKEUR':'EUR','EURBWP':'EUR','BWPEUR':'EUR',
        'EURNAD':'EUR','NADEUR':'EUR','EURNGN':'EUR','NGNEUR':'EUR','EURTZS':'EUR','TZSEUR':'EUR',
        'GBPKES':'GBP','KESGBP':'GBP','GBPZMK':'GBP','ZMKGBP':'GBP','GBPBWP':'GBP','BWPGBP':'GBP',
        'GBPNAD':'GBP','NADGBP':'GBP','GBPNGN':'GBP','NGNGBP':'GBP','GBPTZS':'GBP','TZSGBP':'GBP',
        'ZARKES':'ZAR','KESZAR':'ZAR','ZARZMK':'ZAR','ZMKZAR':'ZAR','ZARBWP':'ZAR','BWPZAR':'ZAR',
        'ZARNAD':'ZAR','NADZAR':'ZAR','ZARNGN':'ZAR','NGNZAR':'ZAR','ZARTZS':'ZAR','TZSZAR':'ZAR',
        'NZDZAR':'NZD','ZARNZD':'NZD','TRYJPY':'TRY','JPYTRY':'TRY','USDZMW':'USD','ZMWUSD':'USD',
        'EURZMW':'EUR','ZMWEUR':'EUR','GBPZMW':'GBP','ZMWGBP':'GBP','ZARZMW':'ZAR','ZMWZAR':'ZAR'}
    
    if cpair not in nomcur and len(cpair) % 2 == 0:  # check if curr pair consists of same currencies
        len_half = len(cpair) / 2
        curr1 = cpair[0:len_half]
        curr2 = cpair[len_half:len(cpair)]
        if curr1 == curr2:
            nc = curr1
        else:
            raise RuntimeError("Currency pair '%s' was not recognized." %cpair)
    else:
        nc = nomcur[cpair]
    
    currency = ael.Instrument[nc]
    return currency.insid
    
#'NGLDZAR':'NGLD','ZARNGLD':'NGLD'    
    
def getcurrpair(obj,*rest):
    currpair = ''
    
    if obj.record_type == 'Instrument':
        ins = obj
        if ins.instype in ('FxSwap', 'Swap'):
            for l in ins.legs():
                currpair += l.curr.insid
        elif ins.instype == 'Option':
            currpair = ins.strike_curr.insid + ins.und_insaddr.curr.insid
        elif ins.instype == 'Stock':
            currpair = 'NGLDZAR'
        elif ins.instype == 'Future/Forward':
            splitstr = string.split(ins.und_insaddr.insid, '/')
            currpair = ins.curr.insid + splitstr[1]
        elif ins.instype == 'Deposit':
            currpair = ins.curr.insid + ins.curr.insid
    elif obj.record_type == 'Trade':
        ins = obj.insaddr
        if ins.instype == 'Curr':
            currpair = obj.curr.insid + obj.insaddr.insid
            
    nomcur = {'XAUUSD':'XAUUSD','USDXAU':'XAUUSD','XAUZAR':'XAUZAR','ZARXAU':'XAUZAR','XAUXAU':'XAUXAU',
        'ZARZAR':'ZARZAR','USDUSD':'USDUSD','USDZAR':'USDZAR','ZARUSD':'USDZAR','EURUSD':'EURUSD',
        'USDEUR':'EURUSD','EURZAR':'EURZAR','ZAREUR':'EURZAR','GBPZAR':'GBPZAR','ZARGBP':'GBPZAR',
        'GBPUSD':'GBPUSD','USDGBP':'GBPUSD','AUDUSD':'AUDUSD','USDAUD':'AUDUSD','USDCHF':'USDCHF',
        'CHFUSD':'USDCHF','JPYZAR':'JPYZAR','ZARJPY':'JPYZAR','USDJPY':'USDJPY','JPYUSD':'USDJPY',
        'AUDZAR':'AUDZAR','ZARAUD':'AUDZAR','CHFZAR':'CHFZAR','ZARCHF':'CHFZAR','XAGUSD':'XAGUSD',
        'USDXAG':'XAGUSD','XAGZAR':'XAGZAR','ZARXAG':'XAGZAR','XPTUSD':'XPTUSD','USDXPT':'XPTUSD',
        'XPTZAR':'XPTZAR','ZARXPT':'XPTZAR','XPDUSD':'XPDUSD','USDXPD':'XPDUSD','XPDZAR':'XPDZAR',
        'ZARXPD':'XPDZAR','MALUSD':'MALUSD','USDMAL':'MALUSD','MALZAR':'MALZAR','ZARMAL':'MALZAR',
        'MCUUSD':'MCUUSD','USDMCU':'MCUUSD','MCUZAR':'MCUZAR','ZARMCU':'MCUZAR','MNIUSD':'MNIUSD',
        'USDMNI':'MNIUSD','MNIZAR':'MNIZAR','ZARMNI':'MNIZAR','MNIUSD':'MNIUSD','USDMNI':'MNIUSD',
        'MNIZAR':'MNIZAR','ZARMNI':'MNIZAR','MPBUSD':'MPBUSD','USDMPB':'MPBUSD','MPBZAR':'MPBZAR',
        'ZARMPB':'MPBZAR','MSNUSD':'MSNUSD','USDMSN':'MSNUSD','MSNZAR':'MSNZAR','ZARMSN':'MSNZAR',
        'MZNUSD':'MZNUSD','USDMZN':'MZNUSD','MZNZAR':'MZNZAR','ZARMZN':'MZNZAR','NGLDZAR':'NGLDZAR',
        'ZARNGLD':'NGLDZAR','BRT_CRD_OILUSD':'BRT_CRD_OILUSD','USDBRT_CRD_OIL':'BRT_CRD_OILUSD',
        'JET_FUELUSD':'JET_FUELUSD','USDJET_FUEL':'JET_FUELUSD','GAS_OILUSD':'GAS_OILUSD',
        'USDGAS_OIL':'GAS_OILUSD','DIESELUSD':'DIESELUSD','USDDIESEL':'DIESELUSD',
        'BRT_CRD_OILZAR':'BRT_CRD_OILZAR','ZARBRT_CRD_OIL':'BRT_CRD_OILZAR',
        'JET_FUELZAR':'JET_FUELZAR','ZARJET_FUEL':'JET_FUELZAR','GAS_OILZAR':'GAS_OILZAR',
        'ZARGAS_OIL':'GAS_OILZAR','DIESELZAR':'DIESELZAR','ZARDIESEL':'DIESELZAR',
        'EURGBP':'EURGBP','GBPEUR':'EURGBP','EURJPY':'EURJPY','JPYEUR':'EURJPY','USDNZD':'USDNZD',
        'NZDUSD':'USDNZD','CADUSD':'USDCAD','USDCAD':'USDCAD','CADZAR':'CADZAR','ZARCAD':'CADZAR',
        'USDKES':'USDKES','KESUSD':'USDKES','EURKES':'EURKES','KESEUR':'EURKES','GBPKES':'GBPKES',
        'KESGBP':'GBPKES','ZARKES':'ZARKES','KESZAR':'ZARKES','USDZMK':'USDZMK','ZMKUSD':'USDZMK',
        'EURZMK':'EURZMK','ZMKEUR':'EURZMK','GBPZMK':'GBPZMK','ZMKGBP':'GBPZMK','ZARZMK':'ZARZMK',
        'ZMKZAR':'ZARZMK','USDBWP':'USDBWP','BWPUSD':'USDBWP','EURBWP':'EURBWP','BWPEUR':'EURBWP',
        'GBPBWP':'GBPBWP','BWPGBP':'GBPBWP','ZARBWP':'ZARBWP','BWPZAR':'ZARBWP','USDNAD':'USDNAD',
        'NADUSD':'USDNAD','EURNAD':'EURNAD','NADEUR':'EURNAD','GBPNAD':'GBPNAD','NADGBP':'GBPNAD',
        'ZARNAD':'ZARNAD','NADZAR':'ZARNAD','USDNGN':'USDNGN','NGNUSD':'USDNGN','EURNGN':'EURNGN',
        'NGNEUR':'EURNGN','GBPNGN':'GBPNGN','NGNGBP':'GBPNGN','ZARNGN':'ZARNGN','NGNZAR':'ZARNGN',
        'USDTZS':'USDTZS','TZSUSD':'USDTZS','EURTZS':'EURTZS','TZSEUR':'EURTZS','GBPTZS':'GBPTZS',
        'TZSGBP':'GBPTZS','ZARTZS':'ZARTZS','TZSZAR':'ZARTZS','NZDZAR':'NZDZAR','ZARNZD':'NZDZAR',
        'TRYJPY':'TRYJPY','JPYTRY':'TRYJPY','USDZMW':'USDZMW','ZMWUSD':'USDZMW','EURZMW':'EURZMW',
        'ZMWEUR':'EURZMW','GBPZMW':'GBPZMW','ZMWGBP':'GBPZMW','ZARZMW':'ZARZMW','ZMWZAR':'ZARZMW'}
    
#    if ins.instype not in ('FxSwap', 'Swap', 'Stock', 'Deposit', 'Future/Forward'):
#     print ins.insid, ins.instype
    cpair = currpair
    if currpair in nomcur:
        cpair = nomcur[currpair]
    return cpair 
 
def get_nomcurr_final(ins,*rest):
    opt = getcurrpair(ins)
    return get_nomcurr(opt)
    
def get_vegacurr(ins,*rest):
    vegacurr = {'XAUUSD':'USD','USDXAU':'USD','XAUZAR':'ZAR','ZARXAU':'ZAR','XAUXAU':'XAU','ZARZAR':'ZAR',
        'USDUSD':'USD','USDZAR':'ZAR','ZARUSD':'ZAR','EURUSD':'USD','USDEUR':'USD','EURZAR':'ZAR',
        'ZAREUR':'ZAR','GBPZAR':'ZAR','ZARGBP':'ZAR','GBPUSD':'USD','USDGBP':'USD','AUDUSD':'AUD',
        'USDAUD':'AUD','USDCHF':'USD','CHFUSD':'USD','JPYZAR':'ZAR','ZARJPY':'ZAR','USDJPY':'JPY',
        'JPYUSD':'JPY','AUDZAR':'ZAR','ZARAUD':'ZAR','CHFZAR':'ZAR','ZARCHF':'ZAR','XAGUSD':'USD',
        'USDXAG':'USD','XPTUSD':'USD','USDXPT':'USD','XPDUSD':'USD','USDXPD':'USD','XAGZAR':'ZAR',
        'ZARXAG':'ZAR','XPTZAR':'ZAR','ZARXPT':'ZAR','XPDZAR':'ZAR','ZARXPD':'ZAR','MALUSD':'USD',
        'USDMAL':'USD','MALZAR':'USD','ZARMAL':'ZAR','MCUUSD':'USD','USDMCU':'USD','MCUZAR':'ZAR',
        'ZARMCU':'ZAR','MNIUSD':'USD','USDMNI':'USD','MNIZAR':'ZAR','ZARMNI':'ZAR','MPBUSD':'USD',
        'USDMPB':'USD','MPBZAR':'ZAR','ZARMPB':'ZAR','MSNUSD':'USD','USDMSN':'USD','MSNZAR':'ZAR',
        'ZARMSN':'ZAR','MZNUSD':'USD','USDMZN':'USD','MZNZAR':'ZAR','ZARMZN':'ZAR','NGLDZAR':'ZAR',
        'ZARNGLD':'ZAR','BRT_CRD_OILUSD':'USD','USDBRT_CRD_OIL':'USD','JET_FUELUSD':'USD',
        'USDJET_FUEL':'USD','GAS_OILUSD':'USD','USDGAS_OIL':'USD','DIESELUSD':'USD',
        'USDDIESEL':'USD','BRT_CRD_OILZAR':'ZAR','ZARBRT_CRD_OIL':'ZAR','JET_FUELZAR':'ZAR',
        'ZARJET_FUEL':'ZAR','GAS_OILZAR':'ZAR','ZARGAS_OIL':'ZAR','DIESELZAR':'ZAR',
        'ZARDIESEL':'ZAR','EURGBP':'GBP','GBPEUR':'GBP','EURJPY':'JPY','JPYEUR':'JPY',
        'USDNZD':'NZD','NZDUSD':'NZD','CADUSD':'CAD','USDCAD':'CAD','CADZAR':'ZAR','ZARCAD':'ZAR',
        'USDKES':'KES','KESUSD':'KES','USDZMK':'ZMK','ZMKUSD':'ZMK','USDBWP':'BWP','BWPUSD':'BWP',
        'USDNAD':'NAD','NADUSD':'NAD','USDNGN':'NGN','NGNUSD':'NGN','USDTZS':'TZS','TZSUSD':'TZS',
        'EURKES':'KES','KESEUR':'KES','EURZMK':'ZMK','ZMKEUR':'ZMK','EURBWP':'BWP','BWPEUR':'BWP',
        'EURNAD':'NAD','NADEUR':'NAD','EURNGN':'NGN','NGNEUR':'NGN','EURTZS':'TZS','TZSEUR':'TZS',
        'GBPKES':'KES','KESGBP':'KES','GBPZMK':'ZMK','ZMKGBP':'ZMK','GBPBWP':'BWP','BWPGBP':'BWP',
        'GBPNAD':'NAD','NADGBP':'NAD','GBPNGN':'NGN','NGNGBP':'NGN','GBPTZS':'TZS','TZSGBP':'TZS',
        'ZARKES':'KES','KESZAR':'KES','ZARZMK':'ZMK','ZMKZAR':'ZMK','ZARBWP':'BWP','BWPZAR':'BWP',
        'ZARNAD':'NAD','NADZAR':'NAD','ZARNGN':'NGN','NGNZAR':'NGN','ZARTZS':'TZS','TZSZAR':'TZS',
        'NZDZAR':'ZAR','ZARNZD':'ZAR','TRYJPY':'TRY', 'JPYTRY':'TRY','USDZMW':'ZMW','ZMWUSD':'ZMW',
        'EURZMW':'ZMW','ZMWEUR':'ZMW','GBPZMW':'ZMW','ZMWGBP':'ZMW','ZARZMW':'ZMW','ZMWZAR':'ZMW'}
    cpair = getcurrpair(ins)
    vc = vegacurr[cpair]
    currency = ael.Instrument[vc]
    return currency.insid
 
def get_continuos_rate(i,ccy,days,*rest):
    lgs = i.legs()
    for l in lgs:
        if (l.curr.insid == ccy):
            curleg = l.curr.legs()[0]
            base = (int)(curleg.daycount_method.lstrip('Act/'))
            cf = l.cash_flows()
            c = cf[0]
            dscfctr = c.discount_factor()
            dob = 1.0 * days/base
            bod = 1.0 * base/days
            naca = (pow(dscfctr, (-1.0 * bod)) - 1)
            power = pow((1.0 + naca), dob)
            cont = bod * (math.log(power)) * 100
     #print 'cont ', cont
    return cont 
     
def get_nomcurr_rate(ins):
    basecurr = get_nomcurr_final(ins)
    if ins.instype == 'FxSwap':
        for l in ins.legs():
            if l.curr.insid == basecurr:
                rate = 1/l.nominal_factor
                return rate
    elif ins.instype not in ('FxSwap'):
        return ''
     
     
def delta_fwd(i,ccy,fcurr_rate,d,*rest):
    lgs = i.legs()
    B = 1
    deltaA = 0
    for l in lgs:
        if (l.curr.insid == ccy):
            curleg = l.curr.legs()[0]
            B = (int)(curleg.daycount_method.lstrip('Act/'))
            deltaA = pow(math.e, (-1 * fcurr_rate / 100.0 * (1.0 * d/B)))
            
#    print math.e, delta
    return deltaA
 
    
    
def delta_fwd_fut(i,ccy,fcurr_rate,qcurr_rate, d,*rest):
#    B = (int)(i.daycount_method.lstrip('Act/'))
    B = 360
    delta = pow(math.e, (((qcurr_rate/100.0)-1 * (fcurr_rate / 100.0)) * (1.0 * d/B)))
#    print math.e, delta
    return delta    
    
 

def DeltaFwd_ADFL(i, request, *rest):
    
    
    NomCurr = get_nomcurr_final(i)
    #print 'NomCurr', NomCurr
 
    #DaysToExpiry = ael.date_today().days_between(i.exp_day.add_banking_day(ael.Instrument[NomCurr], i.spot_banking_days_offset), 'Act/365')
    #print DaysToExpiry
    
    #BaseCurrRate = get_continuos_rate(i, NomCurr, DaysToExpiry)
    #print 'BaseCurrRate', BaseCurrRate
 
    '''
    value = delta_fwd(i, NomCurr, BaseCurrRate, DaysToExpiry)
    #print value
    
    #return value
    '''
    dscfctr = 0.0
    deltaNominal = 0.0
    
    lgs = i.legs()
    flag = 0
    if i.instype == 'FxSwap':
        
        if len(lgs[0].cash_flows()) == 2:
            if lgs[0].start_day <= ael.date_today() and lgs[0].end_day >= ael.date_today():
                flag = 1
                
    
    for l in lgs:
        if (l.curr.insid == NomCurr):
            deltaNominal = l.nominal_amount()
            curleg = l.curr.legs()[0]
            base = (int)(curleg.daycount_method.lstrip('Act/'))
            cf = l.cash_flows()
            
            if flag == 1:
                c = cf[1]
            else:
                c = cf[0]
            dscfctr = c.discount_factor()

     
    
    if request == 'delta':
        return dscfctr
    elif request == 'Nominal':
        return deltaNominal
    elif request == 'deltaNominal':
        return deltaNominal * dscfctr
    elif request == 'NominalCurr':
        return NomCurr
    else:
        return 0.0
        
 
    
   
#i = ael.Instrument['USD-NZD/FXS/070911-070918']
#print DeltaFwd_ADFL(i, 'delta')
#print DeltaFwd_ADFL(i, 'Nominal')
#print DeltaFwd(i)
 
         
         
         
 
     
#fx = getcurrpair(ael.Instrument['ZAR/FX/CAD/C/080326/8.2275'])
#print 'fxs: ',fx,' ',get_nomcurr(fx).insid
#print get_nomcurr_final(ael.Instrument['ZAR/FX/CAD/C/080326/8.2275'])
#print get_vegacurr(ael.Instrument['ZAR/FX/CAD/C/080326/8.2275'])
#print getcurrpair(ael.Instrument['ZAR/FX/CAD/C/080326/8.2275'])
 
#get_continuos_rate(ael.Instrument['USD-ZAR_051003_8.025_P-USD -15000000'],'ZAR',249)
#get_continuos_rate(ael.Instrument['USD-ZAR_051003_8.025_P-USD -15000000'],'USD',249)



