import acm
import FInstrumentCACashflow
from datetime import datetime
from at_logging import  getLogger
LOGGER = getLogger()

from at_email import EmailHelper

TODAY = acm.Time.DateToday()
ACCOUNT_TRADE_FILTER= acm.FTradeSelection['FxClientDeposits']
FX_SALES_TRADE_FILTER = acm.FTradeSelection['ZarFxPnL_ALL']
CALC_SPACE = acm.Calculations().CreateStandardCalculationsSpaceCollection()

def GetSpotRate(trade): 
    trade_currency = trade.Currency()
    trade_instrument = trade.Instrument()
    CurrencyPair = trade_instrument.CurrencyPair(trade_currency)
    return trade_currency.Calculation().FXRate(CALC_SPACE, trade_instrument, TODAY)    
    
                
def getTradingBalance(trade):
    call_balance = CALC_SPACE.CalculateValue(trade, "Deposit balance").Number()
    return call_balance

def getTotalPositions(trade):
    client_name = trade.Counterparty().Name()
    query = acm.CreateFASQLQuery(acm.FTrade, 'AND')
    query.AddAttrNode('Counterparty.Name', 'EQUAL', client_name)
    query.AddAttrNode('Instrument.InsType', 'EQUAL', 'Curr')
    return query.Select()

def getExposureForClient(trade):
    nominal = []
    for conn_trade in getTotalPositions(trade):
        if conn_trade.Status() in ("BO Confirmed", "BO-BO Confirmed"):
            nominal.append(conn_trade.Nominal())
    return sum(nominal)*GetSpotRate(trade)

def callBalance(trade):   
    instrument = trade.Instrument()
    redAmnt = -1*FInstrumentCACashflow.caRedemption(instrument)   
    return redAmnt

def mapAccountToFxPosition(trade):     
    for account in ACCOUNT_TRADE_FILTER.Trades():        
        if trade.Counterparty() == account.Counterparty():           
           return account
   

def getNetBalance(trade):    
    fx_account = mapAccountToFxPosition(trade)
    account_balance = callBalance(fx_account)
    fx_exposure = getExposureForClient(trade)
    net_balance = account_balance + fx_exposure  
    return net_balance
  
def shouldSendEmail(trade):
    net_balance = getNetBalance(trade)
    if net_balance < 0:
        return True
    return False

def breach_status(trade):
    if shouldSendEmail(trade):
        return 'Breached'
    else:
        return 'OK'
     
def to_html(rws):
    """Construct output email"""
    res_text = '<table width="1800" border="1">'
    #Email table with its titled columns
    res_text += "<tr>" + "".join(map("<td><b>{0}</b></td>".format, ("Trade Number", "Client Name", "Trading Balance", "Current Exposure", "Status"))) + "</tr>"
    for rows in rws:
        line = "<tr>" + "".join(map("<td>{0}</td>".format, rows)) + "</tr>"
        res_text += line
    return res_text + "</table>"
    
def message():
    l = []
    for x in range(10):
        msg = '%s ' %x
        l.append(msg)
    return ('Please see attached report of limits breached')
                
def construct_body(tradeList):
    """"""   
    msg = "<br /><br />"
    rows = [(trade.Oid(), trade.Counterparty().Name(), format(int(callBalance(mapAccountToFxPosition(trade))), ',d'), 
                format(int(getExposureForClient(trade)), ',d'),
                    breach_status(trade)) for trade in tradeList]
    msg += to_html(rows)
    
    msg += "<br /><br />"
    return msg
                    
def bookingTimePassage(trade, threshold):
    FMT = '%H:%M:%S'
    time_now = acm.Time.TimeOnlyMs()[0:8]  
    trade_time = trade.ExecutionTime()[-8:] 
    tdelta = datetime.strptime(time_now, FMT) - datetime.strptime(trade_time, FMT)
    time_passage = tdelta.seconds
    if time_passage <= threshold:
        return True
    return False    
    
def send_report(subject, body, recipients):
    """Email sender"""
    environment = acm.FDhDatabase['ADM'].InstanceName()
    subject = "{0} {1} ({2})".format(subject, acm.Time.DateToday(), environment)
    email_helper = EmailHelper(
            body,
            subject,
            recipients,
            "Front Arena {0}".format(environment),
            None,
            "html"
        )
        
    if str(acm.Class()) == "FACMServer":
        email_helper.sender_type = EmailHelper.SENDER_TYPE_SMTP
        email_helper.host = EmailHelper.get_acm_host()

    try:
        email_helper.send()
    except Exception as exc:
        LOGGER.exception("Error while sending e-mail: %s", exc)
    LOGGER.info("Email sent successfully.")
     

trade_list = []
for trade in FX_SALES_TRADE_FILTER.Trades():
    if trade is not None:        
        account = mapAccountToFxPosition(trade)       
    if account is not None:        
        if  shouldSendEmail(trade) and bookingTimePassage(trade, 60):    
            trade_list.append(trade)            

if len(trade_list) > 0:            
    body = construct_body(trade_list)   
    send_report('Daily Limits Breach Report', body, ['mighty.mkansi@Absacapital.com', 'bridgett.bakermoonsamy@absacapital.com', 'ABCapFlowFxSales@barclayscapital.com' ])


        
  

