import ael


def terminate_Trade(tf, *rest):
    tf = ael.TradeFilter[tf].trades()

    for trd in tf:
        trdc = trd.clone()
    	trdc_eao = trd.new()
        trdc_eao.quantity = trdc_eao.quantity * -1 
    	trdc.status = 'Terminated'
    	trdc_eao.status = 'BO Confirmed'
    	trdc_eao.optional_key = ''
    	trdc_eao.value_day = ael.date_today()
    	trdc_eao.acquire_day = ael.date_today() 
    	print trdc.pp()
    	print trdc_eao.pp()
    	trdc.commit()
    	trdc_eao.commit()
    	trdc_eao = trdc_eao.clone()
    	trdc_eao.status = 'Terminated'   
    	trdc_eao.commit() 
    	print trdc_eao.pp()



ael_variables = [('tradefilter', 'TradeFilter', 'string',)]

def ael_main(dict):
    tf = dict["tradefilter"] 
    print '....Starting Termination....'   
    terminate_Trade(tf)
