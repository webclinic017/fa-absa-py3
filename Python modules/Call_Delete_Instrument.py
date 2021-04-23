import ael

def delins(temp,insid,*rest):
    t = ael.Instrument[insid]
    try:
        t.delete()
        print('Done' + insid)
        return 'Done'
    except:
        print('Error' + insid)
        return 'Error'
