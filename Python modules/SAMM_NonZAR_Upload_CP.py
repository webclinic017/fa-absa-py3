import ael, string

def upload(name):
    filename = 'Y:\\Jhb\\Secondary Markets IT\DEPLOYMENTS\\Current\\385487 (Upload Non ZAR Counterparties) - hoonherm\\' + name +  '.csv'

    try:
        f = open(filename)
    except:
        print 'Could not open file'
        return
    
    spec = ael.AdditionalInfoSpec['Midas_Nbr'] 
    
    #read over first line
    line = f.readline()   
    for line in f:
        l = string.split(line, ',')
        
        ptyid = l[1]
        long  = l[2].rstrip('\n')
        if long != 'n/a':
            new_party = ael.Party.new()
            new_party.ptyid = ptyid
            new_party.type = 'Counterparty'
            new_party.fullname = long
            new_party.owner_usrnbr = 1296 #Ashleena
            try:
                new_party.commit()
            except:
                print ptyid, 'not commited'

        #Midas number
        value = l[0]
        c_p = ael.Party[ptyid].clone()
        new_add = ael.AdditionalInfo.new(c_p)
        new_add.addinf_specnbr = spec
        new_add.value = value
        try:
            new_add.commit()
        except:
            print value, 'not commited'


#upload('Counterparties')
