"""
--------------------------------------------------------------------------------------------------------------------------------------------------------------------
MODULE
    JSE FX Futures Close Out Script
    
DESCRIPTION
    Date                    : 2020-10-01
    Purpose                 : FX desk requested that we build a script thats going to close out futures at portfolio level by currency pair
    Department and Desk     : FX Desk
    Requester               : Ross Long and Kgothatso Baloyi
    Developer               : Kabelo Rasethetho
    CR Number               :  
    

HISTORY
====================================================================================================================================================
Date              CR Number        Developer              Description
----------------------------------------------------------------------------------------------------------------------------------------------------
2020-10-01                         Kabelo Rasethetho      Initial Implementation.
2021-01-22                         Kabelo Rasethetho      Excluding manully closed out trades 
----------------------------------------------------------------------------------------------------------------------------------------------------
"""

import acm, csv
from at_email import EmailHelper
from at_time import acm_date
from at_logging import getLogger
from at_ael_variables import AelVariableHandler
from at import TP_FX_SPOT
from FAFOUtils import CreateFXTrade, wipe_payments, get_FX_rate, get_currPair_price, WriteCSVFile

LOGGER = getLogger(__name__)
ael_variables = AelVariableHandler()

ael_variables.add('acquirer',
                  label='TradeAcquirer',
                  cls=acm.FParty,
                  default=acm.FParty['IRD DESK'],
                  mandatory=True)
                  
ael_variables.add('path',
                  label='Report_Path',
                  default='C:\\Temp\\',
                  mandatory=True)

ael_variables.add('filter',
                  label='TradeFilter',
                  cls=acm.FTradeSelection,
                  default=acm.FTradeSelection['Futures_Close_Out'],
                  mandatory=True)

ael_variables.add('default',
                  label='Default Counterparty',
                  cls=acm.FParty,
                  default=acm.FParty['FX SPOT'],
                  mandatory=True)
                  
ael_variables.add('deltaport',
                  label='Delta Portfolio',
                  cls=acm.FPhysicalPortfolio,
                  default=acm.FPhysicalPortfolio['FXY'],
                  mandatory=True)
                  
ael_variables.add('portfolio',
                  label='CounterParty Portfolio',
                  cls=acm.FPhysicalPortfolio,
                  default=acm.FPhysicalPortfolio['RND'],
                  mandatory=True)

ael_variables.add('trader',
                  label='Trader',
                  cls=acm.FUser,
                  default=acm.FUser['AB0104Q'],
                  mandatory=True)

ael_variables.add('status',
                  label='Trade Status',
                  default='FO confirmed',
                  collection=['Simulated', 'FO confirmed'],
                  mandatory=True)
                  
ael_variables.add('delta',
                  label='FX Delta Trade',
                  default='Book',
                  collection=['Book', 'Do not Book'],
                  mandatory=True)
                  
ael_variables.add('market',
                  label='Market',
                  default='EQ_CLOSEOUT',
                  collection=['SPOT', 'EQ_CLOSEOUT'],
                  mandatory=True)

ael_variables.add('period',
                  label='Close Out period',
                  cls = 'string',
                  default='2d',
                  mandatory=True)
                  
ael_variables.add("email_recipients",
                  label="Email Recipients",
                  default="xraFTPFunding1@absa.africa",
                  multiple=True,
                  mandatory=False,
                  alt=("Email recipients. Use comma seperated email addresses "
                       "if you want to send report to multiple users. "
                       "Leave blank if no email needs to be sent."))
                    
ael_variables.add("cc_recipients",
                  label="cc recipients",
                  default="Abcap-IT-Front-Arena-Front-Office@absa.africa",
                  multiple=True,
                  mandatory=False,
                  alt=("Email recipients. Use comma seperated email addresses "
                       "if you want to send report to multiple users. "
                       "Leave blank if no email needs to be sent."))
                                              
ael_variables.add("sender_email",
                  label="sender email",
                  default="Abcap-IT-Front-Arena-Front-Office@absa.africa",
                  multiple=False,
                  mandatory=False,
                  alt=("Email recipients. Use comma seperated email addresses "
                       "if you want to send report to multiple users. "
                       "Leave blank if no email needs to be sent."))
                  
                  
def get_instrument(curr_pair, ins_list):
    for ins in ins_list:
        if ins.Underlying().Name() == curr_pair.Currency1().Name() and ins.Currency().Name() == curr_pair.Currency2().Name():
            return ins
            

def get_original_trade(key_split):
    ins = acm.FInstrument[key_split[1]]
    if ins:
        trades = ins.Trades()
        if len(trades) >= 1:
            for trd in trades:
                if trd.Portfolio().Name() == key_split[0]:
                    return trd
                    
                    
def book_unwind_trade(original_trade, close_out_price, close_out_date, trd_nominal, status, trader):   
    unwind_trade = original_trade.Clone()
    unwind_trade.ReferencePrice(close_out_price)
    unwind_trade.Price(close_out_price)
    unwind_trade.MirrorTrade = None
    unwind_trade.Status = status
    unwind_trade.OptionalKey = ''
    unwind_trade.ConnectedTrade = None
    unwind_trade.Contract = None
    unwind_trade.ContractTrdnbr = None
    unwind_trade.TrxTrade = None
    unwind_trade.ValueDay = close_out_date
    unwind_trade.AcquireDay = close_out_date
    unwind_trade.TradeTime = acm.Time.TimeNow()
    unwind_trade.Trader(trader.Name())
    unwind_trade.Text2('AUTOCLOSE')
    unwind_trade.Type('Closing')
    try:
        unwind_trade.Quantity = (trd_nominal/original_trade.Instrument().ContractSize())* -1.0
        unwind_trade.Commit()
        if(original_trade.CounterPortfolio() is not None):
            wipe_payments(unwind_trade.MirrorTrade())
            wipe_payments(unwind_trade)
            return unwind_trade
        else:
           wipe_payments(unwind_trade)
           return unwind_trade
        LOGGER.info("Successfully booked trade: %s", unwind_trade.Name())
    except Exception as exc:
        LOGGER.exception("Error while committing the trade: %s", exc)
        
        
def get_instument_names_for_closed_trades(trade_list):
    instrument_names = [trade.Instrument().Name() for trade in trade_list if trade.Type() == 'Closing']
    return instrument_names
    
    
def get_positions(trade_filter, task_exeuction_time):
    positions = {}
    trades = trade_filter.Trades()
    today_expiries = [trade for trade in trades if acm.Time.AsDate(trade.Instrument().ExpiryDate()) == acm.Time.DateToday()]
    closed_instruments = get_instument_names_for_closed_trades(today_expiries)
    if len(closed_instruments) >= 1:
       trades = [trade for trade in today_expiries if trade.Instrument().Name() not in closed_instruments]
    else:
        trades = today_expiries
    for trade in trades:
        key = trade.Portfolio().Name()+'_'+trade.Instrument().Name()+'_'+trade.Instrument().Underlying().Name()+'/'+trade.Currency().Name()
        if key not in positions.keys():
            positions[key] = trade.Nominal()
            
        else:
            positions[key] += trade.Nominal()
    return positions
    
    
def closing_out_futures(tf, cpty_name, cpty_prf, trade_status, acquirer, market, book_delta_trade, delta_prf, period, trader, TP_FX_SPOT):
    task_exeuction_time = acm.Time.TimeNow()
    results = get_positions(tf, task_exeuction_time)
    report_results = []
    tf_name = delta_prf.Name()+'_'+'FXFCO'
    trds_list = []
    if results:
        keyslist = []
        [keyslist.append(key) for key in results.keys() if key not in keyslist]
        for key in results.keys():
            key_split = key.split('_')
            if len(key_split) == 3 and abs(results[key]) > 0:
                try:
                    curr_pair = acm.FCurrencyPair[key_split[2]]
                    closing_price = get_FX_rate(curr_pair, market)
                    close_out_date = acm_date('0d')
                    original_trade = get_original_trade(key_split)
                    trd_nominal = results[key] 
                    unwind_trade = book_unwind_trade(original_trade, closing_price, close_out_date, trd_nominal, trade_status, trader)
                    LOGGER.info('unwind trade is {}'.format(unwind_trade.Name()))
                    trds_list.append(unwind_trade.Name())
                    if book_delta_trade == 'Book':
                        if period == '2d':
                            vdays = 2
                        create_trd = CreateFXTrade(delta_prf, results[key], acquirer, curr_pair, closing_price, cpty_name, cpty_prf, vdays, trade_status, trader, TP_FX_SPOT)
                        close_out_fxdelta_trd = create_trd._process_record()
                        mirror_trade = close_out_fxdelta_trd.MirrorTrade()
                        if mirror_trade:
                            mirror_trade.Trader(trader)
                            mirror_trade.Commit()
                        fxdelta_trdnbr = close_out_fxdelta_trd.Name()
                        trds_list.append(fxdelta_trdnbr)
                    else:
                        fxdelta_trdnbr = ''
                        
                    prf = unwind_trade.Portfolio().Name()
                    net_position = trd_nominal+unwind_trade.Nominal()
                    report_results.append([prf, curr_pair.Name(), trd_nominal, unwind_trade.Nominal(), net_position,\
                                           unwind_trade.Name(), fxdelta_trdnbr])
                    LOGGER.info('Successfully closed out the {} position from the {} portfolio'.format(curr_pair.Name(), key_split[0]))
                except Exception as e:
                    LOGGER.error('Failed while trying to close out the {} postion from the {} portfolio due to the following error: {}'.format(curr_pair.Name(), key_split[0], e))
        return report_results
                
    else:
        LOGGER.info('There are no FX futures with  expiry date less than the task execution time of {} '.format(task_exeuction_time))
        
        
def ael_main(ael_dict):
    tf = ael_dict['filter']
    trd_acquirer = ael_dict['acquirer']
    cpty = ael_dict['default']
    cp_prf = ael_dict['portfolio']
    trd_status = ael_dict['status']
    price_market = ael_dict['market']
    outputFileLocation = ael_dict['path']
    book_delta_trade = ael_dict['delta']
    delta_prf = ael_dict['deltaport']
    period = ael_dict['period']
    trader = ael_dict['trader']
    sender_email = ael_dict['sender_email']
    receipents = list(ael_dict["email_recipients"])
    cc_email = list(ael_dict["cc_recipients"])
    date_today = acm.Time.DateToday()
    email_header = 'Futures Close Out' + '_'+date_today 
    file_name = delta_prf.Name()+'_'+'Recon_Report_'+date_today+'.csv'
    file_path = outputFileLocation+file_name
    report_headers = ['Portfolio Name', 'Currency Pair Name', 'Position',\
                      'Close Out Position', 'Net Position', 'Close Out Trade', 'FX Delta Trade' ]
    try:
        output = closing_out_futures(tf, cpty.Name(), cp_prf.Name(), trd_status, trd_acquirer.Name(), price_market, book_delta_trade, delta_prf, period, trader, TP_FX_SPOT)
        if output:
            LOGGER.info('Creating recon report')
            WriteCSVFile(outputFileLocation, file_name, output, report_headers)
            LOGGER.info('Report created.')
            msg = "Hi, <br /><br />"
            msg += "Please find attached recorn report for trade filter {}.".format(tf.Name())
            msg += "<br /><br />"
            msg += "Best regards,<br />{0}".format(
                "Abcap-IT-Front-Arena-Front-Office")
            msg += "<br /><br /><br /><small>This is an automated message from '%s'</small>" % __name__
            email_helper = EmailHelper(
            msg,
            email_header,
            receipents,
            sender_email,
            [file_path],
            "html",
            "SMTP"
            )
            email_helper.host = email_helper.get_acm_host()
            email_helper.send()
            LOGGER.info("Notification email was sent out.")
        else:
            LOGGER.info('There are no futures expiring today...')
        LOGGER.info('Task completed successfully')
    except Exception as e:
        LOGGER.info('Task failed due to the following error: {}'.format(e))
        msg = "Hi FAFO Team, <br /><br />"
        msg += "Please note that the futures close-out task failed for trade filter: {}.".format(tf.Name())
        msg += "<br /><br />"
        msg += "Best regards,<br />{0}".format(
            "Abcap-IT-Front-Arena-Front-Office")
        msg += "<br /><br /><br /><small>This is an automated message from '%s'</small>" % __name__
        email_helper = EmailHelper(
        msg,
        email_header,
        cc_email,
        sender_email,
        None,
        "html",
	"SMTP"  
        )
        email_helper.mail_cc = receipents
	email_helper.host = email_helper.get_acm_host()
        email_helper.send()
        LOGGER.error("Task failed.")
        LOGGER.info(e)
