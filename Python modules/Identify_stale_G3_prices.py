'''

CHG0078548    2020-02-04   Anil Parbhoo   Script to identify stale prices of G3 cureves which are meant to update every minute

'''



import acm
import datetime
import time



benchmark_yield_curves = []
all_yield_curves = acm.FYieldCurve.Select('')
for yc in all_yield_curves:
    if yc.Type()=='Benchmark':
        benchmark_yield_curves.append(yc.Name())
        
ael_variables = [ ['Benchmark_Yield_Curves', 'Benchmark Yield Curves', 'string', benchmark_yield_curves, 'USD-SWAP', 1, 1, 'list of yield curves of typpe benchmark'],
['Delay_in_seconds', 'Delay in seconds', 'int', None,  300, 1, 0, 'delay between now and the price update time to sent e-mail']]


def ael_main(dict):

    now = datetime.datetime.fromtimestamp(time.time())
    problem_prices = []
    
    for yc_name in dict["Benchmark_Yield_Curves"]:      
        bms = acm.FYieldCurve[yc_name].Benchmarks()
        for b in bms:
            ins = b.Instrument()
            if ins.InsType() != 'RateIndex':
                for p in ins.Prices():
                    if p.Market().Name() == 'SPOT':
                        ut_delay = (datetime.datetime.fromtimestamp(p.UpdateTime())) + datetime.timedelta(seconds = dict["Delay_in_seconds"])
                        #print yc_name, ins.Name(), ins.InsType(), p.Day(), round(p.Settle(),5), p.Oid(), ut_delay, now, now > ut_delay
                        if now > ut_delay:
                            problem_prices.append(p.Oid())
    MessageTop = 'please check for possible stale prices compared to current time of email   <br /><br />'
    Message = ''
    subject = 'G3 benchmarks - Latest SPOT settle prices in Front Arena may be stale'
    if len(problem_prices) >= 1:
        from at_email import EmailHelper
        import sys
        import os
        import ael
        TESTMESSAGES = True
        for item in ael.ServerData.select():
            if item.customer_name == 'Production':
                TESTMESSAGES = False
        environment = 'TEST' if TESTMESSAGES else 'PROD'
        if environment == 'PROD':  
            for prinbr in problem_prices:
                lp = acm.FPrice[prinbr]
                Message = Message + ('Instrument : %s , Latest update time for SPOT market : %s , Latest Settle price for SPOT market : %s <br /><br />' % (lp.Instrument().Name(), (datetime.datetime.fromtimestamp(lp.UpdateTime())).strftime("%Y-%m-%d  %H:%M"), str(round(lp.Settle(), 5))))
  
            MessageTotal = MessageTop + '\n' + '\n' + Message
            body = MessageTotal
                

            mail_to = ['Anil.Parbhoo@absa.africa', 'DL-Mopane_Analysts@ABSACORP.onmicrosoft.com', 'AbcapMarketFeedsSup@absa.africa', 'Andrew.Duncan2@absa.africa']
            EMAIL_FROM = 'ABCapITRTBFrontArena@absa.africa'
            email = EmailHelper(body, subject, mail_to, EMAIL_FROM)
            email.sender_type = EmailHelper.SENDER_TYPE_SMTP
            email.host = EmailHelper.get_acm_host()

            try:
                email.send()
            except Exception as e:
                acm.Log("!!! Exception: {0}\n".format(e))
                acm.Log(traceback.format_exc())
                exc_type, _exc_obj, exc_tb = sys.exc_info()
                filename = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                acm.Log("%s %s %s" % (exc_type, filename, exc_tb.tb_lineno))              
        
            
            
        

