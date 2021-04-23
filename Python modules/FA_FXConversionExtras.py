import ael, acm

def trx_copy(oldtrades):
    #oldtrades=acm.FTrade.Select('trxTrade>0')

    for ot in oldtrades:
        print ot.TrxTrade().Oid()
        if ot.Instrument().InsType()=='FxSwap':
            trdnbr=str(ot.Oid())
            #print trdnbr
            newtrades=acm.FTrade.Select('hedgeTrade='+trdnbr)
            #print newtrades
            acm.BeginTransaction()
            for nt in newtrades:
                #Transaction Ref
                if ot.TrxTrade().Oid()==ot.Oid():
                    nt.TrxTrade=nt.Oid()
                elif ot.TrxTrade().Instrument().InsType()!='FxSwap':
                    nt.TrxTrade=ot.TrxTrade()
                else:
                    ot_trx=str(ot.TrxTrade().Oid())
                    newtrx=acm.FTrade.Select('hedgeTrade='+ot_trx)
                    if len(newtrx)>1:
                        if newtrx[0].Oid()>newtrx[1]:
                            nt.TrxTrade=newtrx[1]
                        else:
                            nt.TrxTrade=newtrx[0]
                    elif len(newtrx)>0:
                        nt.TrxTrade=newtrx[0]
                nt.Commit()
                if nt.TrxTrade():
                    print 'Transaction ref %i added to Trade %i' % (nt.TrxTrade().Oid(), nt.Oid())
            acm.CommitTransaction()
        else:
            if ot.TrxTrade():
                if ot.TrxTrade().Instrument().InsType()=='FxSwap':
                    ot_trx=str(ot.TrxTrade().Oid())
                    newtrx=acm.FTrade.Select('hedgeTrade='+ot_trx)
                    if len(newtrx)>1:
                        if newtrx[0].Oid()>newtrx[1]:
                            ot.TrxTrade=newtrx[1]
                        else:
                            ot.TrxTrade=newtrx[0]
                    elif len(newtrx)>0:
                        ot.TrxTrade=newtrx[0]
                    ot.Commit()
                    print 'Transaction ref %i changed on Trade %i' % (+ot.TrxTrade().Oid(), ot.Oid())

def optional_key_copy():
    instruments=acm.FFxSwap.Select('')
    for instrument in instruments:
    #trades=[acm.FTrade[4709832]]
        for ot in instrument.Trades():
            if ot.OptionalKey():
                trdnbr=str(ot.Oid())
                newtrades=acm.FTrade.Select('hedgeTrade='+trdnbr)
                #print newtrades
                opt_key=ot.OptionalKey()
                ot.OptionalKey='#'+opt_key
                ot.Commit()
                acm.BeginTransaction()
                for nt in newtrades:
                    print nt.Oid()
                    if nt.ConnectedTrade()==nt:
                        nt.OptionalKey=opt_key
                    else:
                        nt.OptionalKey=opt_key+'#2'
                    nt.Commit()
                try:    
                    acm.CommitTransaction()
                except Exception, e:
                    acm.AbortTransaction()
                    print e, 'Failed on Old trade', trdnbr
    '''       
    trade=acm.FTrade[6383429]
    if acm.FTtrade.ConnectedTrade()==trade:
        if len(acm.FTtrade.ConnectedTrade()==trade:
        if trade.HedgeTrade():
            oldtrade=trade.HedgeTrade()
            opt_key=oldtrade.OptionalKey()
            oldtrade.OptionalKey='#'+opt_key
            oldtrade.Commit()
            trade.OptionalKey=opt_key
            trade.Commit()
     '''           
optional_key_copy()

#trades=acm.FStoredASQLQuery['FXTrxTrades'].Query().Select()
#trades=[acm.FTrade[4709832]]
#trx_copy(trades)

