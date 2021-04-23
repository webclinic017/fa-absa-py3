import ael

##########################################################################################
# 
#
#
##########################################################################################


def tf_ai(tf):

# get additional infos on the tradefilter
 
    MA = ''
    for addinfo in tf.additional_infos():
	if addinfo.addinf_specnbr.field_name == 'Millenium Acc':
	    MA = tf.add_info('Millenium Acc')
#	    print 'MA is', MA, 'line 29'
    if not MA:
    	raise "Trade Filter has empty Millenium Acc additional info"
    return MA
    
def pop_MIT(t, value):


#    print 'line 26', t.trdnbr, value
    saved = 0 
    for addinfo in t.additional_infos():
    	if addinfo.addinf_specnbr.field_name == 'Millenium Acc No':
    	    if value:
	    	ai=ael.AdditionalInfoSpec['Millenium Acc No']    
		addinfoclone = addinfo.clone()
    	    	t_c = ael.Trade[t.trdnbr].clone()
		addinfoclone.value= value
	    	addinfoclone.commit() 
    	    	saved = 1
    if saved == 0:    
	t_c = ael.Trade[t.trdnbr].clone()
	x = ael.AdditionalInfo.new(t_c)
	x.recaddr = t.trdnbr
	value_str = str(value)
	x.value = value_str
	ai = ael.AdditionalInfoSpec['Millenium Acc No']
	x.addinf_specnbr = ai.specnbr
	x.commit()

def MAE(tf, *rest):

    MA = tf_ai(tf)
    trades = tf.trades()
#    print trades
    if len(trades) > 0:
    	for t in trades:
	    pop_MIT(t, MA)
    return len(trades)


#MAE(ael.TradeFilter['Millenium_9802_TB'])
