import ael

def ex_coupon_day(cf, ins, end_day, count, unit, calendar):
    if ins.category_chlnbr:
    	if ins.category_chlnbr.entry=='RSA':
    	    rolling=ins.legs()[0].rolling_period
    	    if rolling =='1y':
	    	ExCoup1= ins.add_info('ExCoup1')
		
		
	    if rolling =='6m':   
	    	ExCoup1= ins.add_info('ExCoup1')
		ExCoup2= ins.add_info('ExCoup2')
		
		CfMonth=cf.end_day.to_string()[5:7]
		CfYear=cf.end_day.to_string()[0:4]
    	    	
		ExCoupMonth1=ExCoup1[5:7]
		ExCoupMonth2=ExCoup2[5:7]
		
		if CfMonth >= ExCoupMonth1 and CfMonth < ExCoupMonth2:
		    ExDate=CfYear+'-'+ExCoup1[5:10]
		if CfMonth >= ExCoupMonth2:
		    ExDate=CfYear+'-'+ExCoup2[5:10]
		
		#print cf.end_day.to_string(), ExDate 
		
    return ael.date(ExDate)  
