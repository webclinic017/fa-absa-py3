import ael


def terminate_Trade(file,*rest):
    try:
    	f = open(file)
    except:
    	print 'File could not be found or opened'
    line = f.readline()
    line = f.readline()
    while line:
    	l = []
    	#print line
	line = line.rstrip()
	l = line.split(',')
	#if l[13] == '0':
        print l[0]
        trd = ael.Trade[(int)(l[0])]
        trdc = trd.clone()
        trdc_eao = trd.new()
        trdc_eao.quantity = trdc_eao.quantity * -1 
        trdc.status = 'Terminated'
        trdc_eao.status = 'BO Confirmed'
        trdc_eao.optional_key = ''
        trdc_eao.value_day = ael.date_today()
        trdc_eao.acquire_day = ael.date_today() 
        #print trdc.pp()
        #print trdc_eao.pp()
        try:
            trdc.commit()
            trdc_eao.commit()
            trdc_eao = trdc_eao.clone()
            trdc_eao.status = 'Terminated'   
            trdc_eao.commit() 
        except:
            print 'cannot commit ', trdc.trdnbr
        #print trdc_eao.pp()
        '''
        paym = ael.Payment.new(trdc_eao)
        paym.type = 'Termination Fee'
        paym.amount = (float)(l[14])
        paym.payday = ael.date_today()
        paym.commit()
        print paym.pp()
        '''
        line = f.readline()
    f.close()

ael_variables = [('filename', 'File Location', 'string',)]

def ael_main(dict):
    filenm = dict["filename"] 
    print '....Starting Termination....'   
    terminate_Trade(filenm)
    print '....Termination ended....'
    
