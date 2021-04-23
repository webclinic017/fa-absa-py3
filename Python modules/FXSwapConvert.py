'''
Description
This code is called by the ASQL FXSwapConvert. It converts all the FX Swaps specified in the filter to future/forward trades.

Date            Who                     What
01/10/2009      Willie van der Bank     Created
'''

import ael

def doFXSwapConvert(temp,trdnbr,*rest):
    try:
        dooFXSwapConvert(temp, trdnbr, *rest)
        return 'Success'
    except Exception, e:
        return 'Error'

def dooFXSwapConvert(temp,trdnbr,*rest):
    month = {'01':'JAN','02':'FEB','03':'MAR','04':'APR','05':'MAY','06':'JUN','07':'JUL','08':'AUG','09':'SEP','10':'OCT','11':'NOV','12':'DEC'}
    trd = ael.Trade[trdnbr]
    ins = trd.insaddr
    legs = ins.legs()
    for i in legs:
        cf = i.cash_flows()
        if i.payleg == 0:
            rAmount = cf[0].projected_cf()
            rCurr = i.curr.insid
        elif i.payleg == 1:
            pAmount = cf[0].projected_cf()
            pCurr = i.curr.insid
    outright_date = cf[0].pay_day

    #Delete empty add_infos
    clntrd = trd.clone()
    for ai in clntrd.additional_infos():
        if ai.value == '':
            ai.delete()
    clntrd.commit()
    ael.poll()

    newtrd = trd.new()
    newins = ael.Instrument.new('Future/Forward')
    rate = abs(pAmount / rAmount)
    if rCurr == 'MNI' and pCurr == 'USD':    
        print '1', trd.trdnbr, rAmount, rate, outright_date, trd.prfnbr.prfid, trd.counterparty_ptynbr.ptyid, trd.acquirer_ptynbr.ptyid
        newins.und_insaddr = 31115  #ZZUSD/MNI/ZEROSPOTDAYS
        newins.curr = 1             #USD
    elif rCurr == 'MPB' and pCurr == 'USD':
        print '2', trd.trdnbr, rAmount, rate, outright_date, trd.prfnbr.prfid, trd.counterparty_ptynbr.ptyid, trd.acquirer_ptynbr.ptyid
        newins.und_insaddr = 31128  #ZZUSD/MPB/ZEROSPOTDAYS
        newins.curr = 1             #USD
    elif rCurr == 'MZN' and pCurr == 'USD':
        print '3', trd.trdnbr, rAmount, rate, outright_date, trd.prfnbr.prfid, trd.counterparty_ptynbr.ptyid, trd.acquirer_ptynbr.ptyid
        newins.und_insaddr = 31150  #ZZUSD/MZN/ZEROSPOTDAYS
        newins.curr = 1             #USD
    elif rCurr == 'MZN' and pCurr == 'ZAR':
        print '4', trd.trdnbr, rAmount, rate, outright_date, trd.prfnbr.prfid, trd.counterparty_ptynbr.ptyid, trd.acquirer_ptynbr.ptyid
        newins.und_insaddr = 31150  #ZZUSD/MZN/ZEROSPOTDAYS
        newins.curr = 2             #ZAR
        newtrd.curr = 2             #ZAR
        
    #InsID = pCurr + "/FWD/" + rCurr + "/" + ins.exp_day.to_string('%d') + month[ins.exp_day.to_string('%m')] + ins.exp_day.to_string('%Y')[2:4]
    InsID = pCurr + "/FWD/" + rCurr + "/" + outright_date.to_string('%d') + month[outright_date.to_string('%m')] + outright_date.to_string('%Y')[2:4]
    try:
        newins.insid = InsID
        newins.exp_day = ins.exp_day
        newins.product_chlnbr = 2177        #Val Group = AC_GLOBAL_Basis
        newins.commit()
        newinsaddr = newins.insaddr
    except Exception, e:
        print e
        newinsaddr = ael.Instrument[InsID].insaddr
        
    print 'New insid: ', newins.insid
    newtrd.insaddr = newinsaddr
    newtrd.quantity = rAmount
    newtrd.price = rate
    newtrd.hedge_trdnbr = trd.trdnbr
    newtrd.commit()
    print 'New trd number: ', newtrd.trdnbr
    ct = trd.clone()
    ct.status = 'Void'
    ct.commit()
    ael.poll()
    print 'Trade ' + str(trd.trdnbr) + ' voided.'

#doFXSwapConvert(1,6228859)
