import ael, string, glob
from xml.dom import minidom
def initial_margin(val, deposit, payday):
    Add_additional_CF(deposit, val, payday)
    print 'Added the Fixed Amount Cashflow'

def bookingfee(file):
    print 'init'


def commision_F(val, deposit, payday):
    trade = deposit.trades()[0]
    type= 'Cash'
    freetext = 'commision'
    Add_additional_payments(trade, type, freetext, val, payday)
    print 'Added additional payment'

def Add_additional_payments(trade, type, freetext, amount, payday):
    """ 
    	This will add the additional payment for whatever type specified per trade specified
    	trade --    The trade entity
	type --     The type of payment requiered in a string format like 'Cash' or 'Broker Fee'
	freetext -- Any comments or text needed
	amount --   The value that must be added for the payment        
	payday --   This is the date for when the payment is effective
    """
    trdclone = trade.clone()
    print trade.trdnbr
    paym = ael.Payment.new(trdclone)
    paym.amount = amount
    paym.payday = payday
    paym.valid_from = payday
    paym.type = type
    paym.text = freetext
    try:
    	paym.commit()
    	print 'Additional Payment has been made' 
    except:
    	print 'Payment has not been booked'
    
def Add_additional_CF(inst, amount, payday):
    leg = inst.legs()[0].clone()
    cf_new = ael.CashFlow.new(leg)
    cf_new.type = 'Fixed Amount'
    cf_new.pay_day = payday
    cf_new.fixed_amount = amount / inst.contr_size
    cf_new.nominal_factor = 1
    cf_new.pp()
    cf_new.commit()

def readrtffile(filename, payday, deposit):
    try:
    	f=open(filename)
    except:
    	print 'error'
    line = f.readline()
    count = 0
    list = []
    size = []
    count = 0
    while line:
    	res = line.find('Total')
	if res >= 0:
	    totalline = line.rstrip('\n')
	    count = count + 1
	if count == 2:
	    break
	line = f.readline()
    totalline = totalline.replace(' ', '')
    print totalline
    list = []
    list = string.split(totalline, ',')
    print list
    comm = list[2]
    margin = list[3]
    f.close() 
    initial_margin((int)(margin), deposit, payday)
    commision_F((int)(comm), deposit, payday)
    
    
def readxml(file, payday):
    doc = minidom.parse('C:\\safex_ascii\\ABL001.xml')
    bookinglist = doc.getElementsByTagName('Transaction')
    for tr in bookinglist:
    	bookfee = tr.getElementsByTagName('BookingFee')[0].firstChild.data
    	reference = tr.getElementsByTagName('Reference')[0].firstChild.data
	reflist = string.split(reference, ' ')
	print reflist
	bookfee = bookfee.rstrip()
    	bookfee = bookfee.lstrip()
    	for trans in reflist:
	    reference = trans.rstrip()
	    reference = reference.lstrip()
	    if reference[0] == 'G':
	    	print reference
		trad = ael.Trade.read('optional_key="%s"' % reference)
		if trad:
		    Add_additional_payments(trad, 'Cash', 'Bookingfees', (float)(bookfee), payday)
		else:
		    print 'Critical: Could not find trade with this reference', reference
    	print '------------'

def build_deplist():
    	list = []
    	ins = ael.Instrument.select('instype = "Deposit"')
	for i in ins:
	    list.append(i.insid)
	return list
	
def build_csvfile():
    files = glob.glob('\\\\atlasprd\\AIS_FILES\\*.csv')
    return files    
def build_xmlfile():
    files = glob.glob('\\\\atlasprd\\AIS_FILES\\*.xml')
    return files    	
    
ael_variables = [('pday', 'Pay_day', 'date', None, 'TODAY', 1, 0), ('ins', 'Call Deposit', 'string', build_deplist(), 'ZAR/INITIALMARGIN/ABL/TEST', 1, 0), ('rtffiles', 'InitMandComm_file', 'string', build_csvfile(), '', 1, 1), ('xmlfile', 'Bookingfee_File', 'string', build_xmlfile(), '', 1, 1)]    
    
def ael_main(dict):
    pdate = dict['pday']
    ins = dict['ins']
    file = dict['rtffiles']
    xfile = dict['xmlfile']
    date = pdate
    deposit = ael.Instrument[ins]
    for f in file:
    	readrtffile(f, date, deposit)
    for x in xfile:
    	
	readxml(x, date)
