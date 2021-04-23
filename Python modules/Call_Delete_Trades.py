import ael

def deltrades(temp,trdnbr,*rest):
    t = ael.Trade[trdnbr]
    try:
        t.delete()
        print('Done' + (str)(trdnbr))
        return 'Done'
    except:
        print('Error' + (str)(trdnbr))
        return 'Error'
