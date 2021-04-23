'''-----------------------------------------------------------------------
MODULE
    SAGEN_SpotPriceCopy

DESCRIPTION
    This script copies the SPOT (bid, ask, last, settle) price from one instrument to other instruments 

    Date                : 2010-05-25
    Purpose             : Copies the SPOT (bid, ask, last, settle) price from the bond instrument to the  replica instrument
    Department and Desk : PCG SM Middle Office
    Requester           : Dumisani Mkhonza
    Developer           : Herman Hoon
    CR Number           : 329827

ENDDESCRIPTION
-----------------------------------------------------------------------'''
import ael, acm


def update_price(fromName,toList,date,*rest):
    '''Copies the SPOT (bid, ask, last, settle) price from one instrument to other instruments '''

    fromIns = ael.Instrument[fromName]
    for p in fromIns.prices():
        if p.ptynbr.ptyid == 'SPOT':
            if p.day == date:
                bidPrice = p.bid
                askPrice = p.ask
                lastPrice = p.last
                settlePrice = p.settle
                currPrice = p.curr
                
    for i in range(len(toList)):
        toName = toList[i].Name()
        toIns = ael.Instrument[toName]
        for p in toIns.prices():
            if p.ptynbr.ptyid == 'SPOT':
                if p.day == date:
                    p_clone = p.clone()
                    p_clone.bid = bidPrice
                    p_clone.ask = askPrice
                    p_clone.last = lastPrice
                    p_clone.settle = settlePrice
                    p_clone.curr = currPrice
                    try:
                        p_clone.commit()
                        print 'INFO:' + fromName + ' spot price was copied to ' +  toName
                    except Exception, err:
                        print 'WARNING:' + toName + ' spot price not commited: ' + str(err)
    return
         
'''----------------------------------------------------------------------------------------------------------------------------------

----------------------------------------------------------------------------------------------------------------------------------'''
# main
today = ael.date_today()

fromInsDefault = 'ZAR/R197'
toInsDefault   = 'ZAR/R197/StructDepo,ZZ/R197'

fromDesc = 'The spot prices of this instrument will be copied.'
toDesc = 'The spot prices of these instruments will be updated.'

ael_variables = [   
                    ['Date', 'Date', 'date', None, today, 0, 0, 'Date for which the spot prices will be copied.'],
                    ['FromInstrument', 'FromInstrument', 'FInstrument', None,  fromInsDefault, 1, 1, fromDesc],
                    ['ToInstruments', 'ToInstruments', 'FInstrument', None,  toInsDefault, 1, 1, toDesc]
                ]

def ael_main(ael_dict):
    getDate = ael_dict['Date']
    if getDate == None:
        date = ael.date_today()
    else:    
        date = ael.date_from_string(getDate, '%Y-%m-%d')
    
    fromList = ael_dict['FromInstrument']
    toList   = ael_dict['ToInstruments']

    update_price(fromList[0].Name(), toList, date)

