import ael

insRUT = ael.Instrument['ZAR/RUT_dummy_test']
RUTPrice = insRUT.used_price(ael.date_today(), insRUT.curr.insid)
insSWIX = ael.Instrument['ZAR/SWIX_3pm_price']
SWIXPrice = 0

for p in insSWIX.historical_prices():
    if p.ptynbr.ptyid == 'NON_STD_Market':    
        if p.day == ael.date_today().add_banking_day(ael.Instrument[insSWIX.curr.insid], -1):
            SWIXPrice = p.settle  
            
i = ael.Instrument['ZAR/RUT']           #This instrument's PriceLink will be updated with the calculated factor
defi = ael.PriceDefinition.select("insaddr = %d" % i.insaddr)

for m in defi.members():

    factor = 0
    v = getattr(m, 'data[0]')
    pos = v.find('*')
    pos += 1 
    
    try:
        factor = str(round((RUTPrice/SWIXPrice)/(100), 10))  
        NewFactor = v[:pos] + ' ' + (str)(factor)
        mc = m.clone()
        setattr(mc, 'data[0]', NewFactor)
        mc.commit()
        ael.poll()
        print getattr(m, 'data[0]')
    except:
        print'Problem - ZAR/SWIX do not have a price for yesterday where the the Market equals the EquitiesMTM'

