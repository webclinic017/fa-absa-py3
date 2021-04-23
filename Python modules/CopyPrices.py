'''
CHG0078251   Anil Parbhoo    2020-01-30   send e-mail for possible stale prices of index member stocks identified in an asql

'''

import acm
import ael
import datetime
from at_email import EmailHelper
import sys
import os

def ListPrices(c , *rest):
    acm.Log("System Path: %s" % sys.path)
    subject = "Please check index member for possible stale price to reuters"
    ins = acm.FInstrument[c.insaddr]
    
    if ins.Prices():
        for p in ins.Prices():
            if p.Market().Name() == 'SPOT':
                for pld in acm.FPriceLinkDefinition.Select(''):
                    if pld.Instrument().Oid() == ins.Oid():
                        if pld.PriceDistributor().Name() == 'REUTERS_FEED':
                            ric = pld.IdpCode()
                Message = 'Price update time of this index member stock may relate to a stale price.<br /><br /> Please compare last price to Reuters FID: TRDPRC_1 <br /><br />   Instrument: %s  <br /><br />  RIC code: %s  <br /><br />  SPOT price update time : %s  <br /><br />  Last SPOT price = %s' %( p.Instrument().Name(), ric, str(datetime.datetime.fromtimestamp(p.UpdateTime())), str(p.Last()))

            TESTMESSAGES = True
            for item in ael.ServerData.select():
                if item.customer_name == 'Production':
                    TESTMESSAGES = False
            environment = 'TEST' if TESTMESSAGES else 'PROD'
            if environment == 'PROD':
	
                body = Message
                print body

                mail_to = ['Anil.Parbhoo@absa.africa', 'Ridwaan.Arbee@absa.africa', 'Jakub.Tomaga@absa.africa', 'CIBAfricaFrontCore@absa.africa']
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
                                   
                    
            return ins.Name()
