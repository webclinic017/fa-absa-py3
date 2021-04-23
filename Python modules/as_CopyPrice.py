import ael

'''
Purpose:        Copies yesterdays price to today
Developer:      Aaeda Salejee
Date:           June 2007

History:
When:       CR Number:      Who:                    Requester:              What:
Jan 2008                    Aaeda Salejee                                   Copies SPOT to SOB.
            C581033         Heinrich Cronje         Khunal Ramesar - MO     The Mtm From Feed needs to be turned off for Currency Future Forwards which comes from YIELDX.
2012-07-06  C318884         Nidheesh Sharma                                 Added a condition to the if statement to keep the MTM from feed on for MTM instruments.
2014-05-27  CHNG1993933     Anil Parbhoo            Elaine Naidoo + JP      removed - The Mtm From Feed needs to be turned off for Currency Future Forwards which comes from YIELDX.
                                                                            as the yield X currency futures will not be 'mtm from feed' but priced theoretically as from 18 March 2014.        

'''


def PriceKeeper(temp, i, *rest):

    yesterday = ael.date_today().add_days(-1)
    flag = 0
    sobflag = 0
    mtmFlag = 0
    err = ''
    for p in i.prices():
        if p.ptynbr != None:
            if p.ptynbr.ptyid == 'SPOT':
                if p.day == ael.date_today():
                    err = err + ' SPOT price already exists for today'
                elif p.day <= i.maturity_date:
                    p_clone = p.clone()
                    p_clone.day = ael.date_today()                    
                    try:
                        p_clone.commit()
                        flag = 1
                    except:
                        err = err + ' Could not copy SPOT price for today'                        
                
                #SPOT to SOB                    
                fnd_sob = 0                
                for prc in i.prices():
                    if prc.ptynbr != None:            
                        if prc.ptynbr.ptyid == 'SPOT_SOB' and p.curr == prc.curr:
                            fnd_sob = 1
                            psob = prc

                if fnd_sob == 1:
                    if psob.day <= i.maturity_date:               
                        sob_clone = psob.clone()
                        sob_clone.bid = p.bid
                        sob_clone.ask = p.ask
                        sob_clone.settle = p.settle
                        sob_clone.last = p.last
                        sob_clone.day = ael.date_today()
                    else:
                        err = err + ' SOB price already exists'	

                else:
                    sob_clone = p.new()
                    sob_clone.ptynbr = ael.Party['SPOT_SOB']                        
                    sob_clone.day = ael.date_today()              

                try:
                    sob_clone.commit()
                    sobflag = 1
                except:
                    err = err + ' Could not copy SPOT to SOB'

                
                        
            # SPOT_BESA
            if p.ptynbr.ptyid == 'SPOT_BESA':
                if p.day == ael.date_today():
                    err = err + ' SPOT_BESA price already exists for today'
                if p.day == yesterday:
                    pb_clone = p.clone()
                    pb_clone.day = ael.date_today()                    
                    try:
                        pb_clone.commit()
                        flag = 1   
                    except:
                        err = err + ' Could not copy SPOT_BESA price for today'                     

        else:
            print(i.insid)

       
    if flag == 1 and sobflag == 1:
        return 'Success'
    else:
        return err
                




#       Dirk Strauss
#       Nov 07
#       Copies PRD curve to the _SOB curve

def CopyBasisCurvesToSOB(temp, crv, *rest):

    #crvs = ('ZAR-BASIS', 'ZAR-PRIME', 'GBP-BASIS-SOB', 'EUR-BASIS-SOB')
    #for crv in crvs:
    print('\n ----------------', crv)
    # get spreads from prod curve
    yc = ael.YieldCurve[crv]
    sprd = {}
    
    for p in yc.points():
        ps = ael.YCSpread.select('point_seqnbr = ' + str(p.seqnbr))            
        if len(ps) > 0:
            sprd[p.date_period] = ps[0].spread
        else:
            print('no stored spread found in ' + crv + ' for point:', p.date_period)

    pnts = sprd.keys()    
    
    # write spreads to sob curve
    yc = ael.YieldCurve[crv + '-SOB']
    for p in yc.points():
        ps = ael.YCSpread.select('point_seqnbr = ' + str(p.seqnbr))
        if len(ps) > 0:
            psc = ps[0].clone()
            t = p.date_period
            print('checking - ', t)
            if t in pnts:
                print('found - ', t)
                psc.spread = sprd[t]
                try:
                    psc.commit()
                    print('commited -', t, '\n')
                except:
                    err = 'Unable to commit YieldCurve ' + crv
                    print(err)
            else:
                print(t, ' not found in prod curve')
        else:
            print('no stored spread found in ' + crv + '-SOB for point:', p.date_period)

    return 'complete'
















def PriceTestKeeper(temp, i, *rest):

    yesterday = ael.date_today().add_days(-1)
    flag = 0
    sobflag = 0
    err = ''
    for p in i.prices():
        if p.ptynbr != None:
            if p.ptynbr.ptyid == 'SPOT':
                #SPOT to PRICETEST                    
                fnd_sob = 0                
                for prc in i.prices():
                    if prc.ptynbr != None:            
                        if prc.ptynbr.ptyid == 'PRICETEST' and p.curr == prc.curr:
                            fnd_sob = 1
                            psob = prc

                if fnd_sob == 1:
                    if psob.day <= i.maturity_date:               
                        sob_clone = psob.clone()
                        sob_clone.bid = p.bid
                        sob_clone.ask = p.ask
                        sob_clone.settle = p.settle
                        sob_clone.last = p.last
                        sob_clone.day = ael.date_today()
                    else:
                        err = err + ' PRICETEST price already exists'	

                else:
                    sob_clone = p.new()
                    sob_clone.ptynbr = ael.Party['PRICETEST']                        
                    sob_clone.day = ael.date_today()              

                try:
                    sob_clone.commit()
                    sobflag = 1
                except:
                    err = err + ' Could not copy SPOT to PRICETEST'
                    
        else:
            print(i.insid)
        
    if flag == 1 and sobflag == 1:
        return 'Success'
    else:
        return err
                



