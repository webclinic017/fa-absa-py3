'''-----------------------------------------------------------------------------
PROJECT                 :  Spark Non ZAR Cashflow Feed
PURPOSE                 :  Feed non zar settlements to MidasPlus
DEPATMENT AND DESK      :  PCG/Ops
REQUESTER               :  Nick Bance
DEVELOPER               :  Anwar Banoo
CR NUMBER               :  XXXXXX
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date       Change no Developer                 Description
--------------------------------------------------------------------------------
2011-10-25 XXXXXX                              Initial Implementation
2012-08-22 ABITFA-1512 Anwar Banoo             Added support for FO and Terminated statuses as well as curr instrument
2013-04-05 C926384      Anwar Banoo            Add supression for scrip type cashflows
2015-02-23              Arthur Grace           Add client cfc for BARX PACE Money Market project
'''
import acm, ael, sys, FLogger, time, Spark_Nostro_MQConfig, os
import FOperationsUtils as Utils
import xml.dom.minidom as xml            

from PACE_MM_TAL_Override import PACE_MM_TAL_Override as TALOverride

from SAGEN_IT_Functions import get_lowest_settlement, set_AdditionalInfoValue_ACM
from xml.etree.ElementTree import Element, SubElement, dump, XML, tostring, ElementTree, parse, fromstring
#from Spark_Nostro_MQWrapper import MqMessenger as MqMessenger


MODULE_NAME = 'Spark_Nostro_Feed'
ACCOUNT_CODE = '1202'
#Arthur edited
GLOBAL_SUPPRESSIONS = ['Security Nominal', 'End Security', 'Credit Default', 'Redemption Amount', 'Interest Reinvestment']
DEPO_SUPPRESSIONS = ['Call Fixed Rate Adjustable', 'Fixed Rate Adjustable']
REPO_SUPPRESSIONS = ['Coupon', 'Coupon transfer']
calendar = acm.FCalendar['ZAR Johannesburg']
TODAY = acm.Time().DateToday()
PREVBUSDAY = calendar.AdjustBankingDays(TODAY, -1)
NEXTBUSDAY = calendar.AdjustBankingDays(TODAY, 1)
cs = acm.Calculations().CreateStandardCalculationsSpaceCollection()
configuration = None
logger = None
mqMessenger = None
posted = acm.FList()
fxTypeMapper = {4096:'FX Spot', 8192:'FX Forward', 16384:'FX Swap', 32768:'FX Swap'}

def __getReversalMessage(root):    
    retVal = Element("CashflowMessage")
    
    for node in root.getchildren():
        if node.tag not in ('Identifiers', 'Financials'):
            retVal.append(node)
        elif node.tag == 'Financials':
            Financials = Element("Financials")
            for child in node.getchildren():
                if child.tag == 'Amount':
                    SubElement(Financials, child.tag).text = str(float(child.text) * -1)
                else:
                    Financials.append(child)
            retVal.append(Financials)
        elif node.tag == 'Identifiers':
            Identifiers = Element("Identifiers")
            for child in node.getchildren():
                if child.tag == 'SettlementId':
                    SubElement(Identifiers, child.tag).text = "%s%s" %(child.text, "-Rev")
                else:
                    Identifiers.append(child)
            retVal.append(Identifiers)
    return tostring(retVal)
    
def __uniqueMessage(s, Root, objectName):
    diary = acm.FSettlementDiary[objectName]    
    if diary:
        tree = ElementTree(fromstring(diary.Text()))
        tracking = tree.find('Tracking')
        status = tracking.get('Status')

        root = tree.getroot()
        root.remove(tracking)
                
        if (status == 'Sent') or ((status == 'Success') and (tostring(root) == tostring(Root))):
            mess = 'Message has been processed previously for trade %s %s %s %s' %(s.Trade().Oid(), s.SourceObject().RecordType(), s.SourceObject().Oid(), objectName)
            logger.WLOG(mess)                        
            return False
        elif ((status == 'Success') and (tostring(root) != tostring(Root))):
            mess = 'Need to send update for trade %s %s %s %s' %(s.Trade().Oid(), s.SourceObject().RecordType(), s.SourceObject().Oid(), objectName)
            logger.WLOG(mess)
            nostroMessage = __getReversalMessage(root)
            if nostroMessage:
                #mqMessenger.Put(nostroMessage)
                f = open(r'c:\SPARKS\uniqueMessage_nostro'+ael.date_today().to_string('%Y%m%d')+'_'+str(s.Trade().Oid())+'.txt', 'w')
                f.write(nostroMessage)
                f.close()
                logger.DLOG('Reversal message published message to %s --> %s' %(configuration.QueueName, nostroMessage))            
            return True            
            
    return True
    
def __hasAccountLinks(s):
    ruleCashAccount = ''
    for accLink in s.Trade().AccountLinks():
        for rule in accLink.SettleInstruction().Rules():
            if s.Type() == 'Fixed Amount':
                ruleCashAccount = rule.CashAccount().Account()
    return ruleCashAccount

def __hasSSI_clientCFC(s):
    clientCFC = ''
    validSSI = False
    clientCFC = __hasAccountLinks(s)
    if clientCFC!='':
        return clientCFC
    else:
        for acc in s.Trade().Counterparty().Accounts():
            if acc.Currency().Name() == s.Trade().Instrument().Currency().Name():
                if acc.Party().Type() in ['Counterparty', 'Client']:
                    clientCFC = acc.Account()
                    for si in s.Trade().Counterparty().SettleInstructions():
                        if s.Type() == si.CashSettleCashFlowType() and s.Trade().Instrument().Currency().Name()==si.Currency().Name():
                            if si.FromParty().Name()=='MONEY MARKET':
                                if s.Trade().Status()!='FO Confirmed':
                                    if s.Type()=='Fixed Amount':
                                        validSSI = True
        if validSSI:
            print 'The following CFC account was found to be used on external client', clientCFC
            return clientCFC
        else:
            return ''
    
def __simOutput(s, feedFile, desk, clientCFC):
    try:
        #if s not in posted:
            posted.Add(s)
            if not s.Trade().Portfolio().add_info('MIDAS_Customer_Num'):
                mess = 'MIDAS customer number add info value not set for portfolio: %s on trade: %s' %(s.Trade().Portfolio().Name(), s.Trade().Oid())
                logger.WLOG(mess)            
            else:
                #Anwar 20/11/2013 - fx trades need additional attention due to the instrument vs trade model

                objectRef = Spark_Nostro_MQConfig.map[s.SourceObject().RecordType()]
                if objectRef == 'TRD':
                    objectRef += s.Currency().Name()
                objectName = "%s%s%s_%s" %(s.Trade().Oid(), objectRef, s.SourceObject().Oid(), ael.date(s.PayDate()).to_string('%m%d'))
                rounding = 2
                if s.Currency().Name() == 'JPY':
                    rounding = 0
                posting = round(s.Calculation().Projected(cs).Number(), rounding)
                
                if posting != 0 or posting == 0:  
                    
                    internal = 'False'
                    accountSequence = '01'
                    #use DEF as default sequence if not 01
                    if 'DEF' in s.Trade().Portfolio().add_info('MIDAS_Acct_Seq'):
                        list = s.Trade().Portfolio().add_info('MIDAS_Acct_Seq').split(';')
                        for item in list:
                            if 'DEF' in item:
                                accountSequence = item.split('=')[1]
                    
                    accountNumber = s.Trade().Portfolio().add_info('MIDAS_Customer_Num')
                    
                    if s.Currency().Name() in s.Trade().Portfolio().add_info('MIDAS_Acct_Seq'):
                        list = s.Trade().Portfolio().add_info('MIDAS_Acct_Seq').split(';')
                        for item in list:
                            if s.Currency().Name() in item:
                                accountSequence = item.split('=')[1]                        
                    
                    #CFCAccount = accountNumber.zfill(6) + s.Currency().Name() + '1011' + '01'
                    if desk == 'InterDesk':
                        CFCAccount = accountNumber.zfill(6) + s.Currency().Name() + ACCOUNT_CODE + accountSequence.zfill(2)                    
                    elif desk == 'ClientCFC':
                        CFCAccount = clientCFC                   
                    
                    Root = Element("CashflowMessage")
                    Identifiers = SubElement(Root, "Identifiers")
                    
                    SubElement(Identifiers, "SettlementId").text = objectName
                    SubElement(Identifiers, "PaymentRef").text = "Trd%s" %str(s.Trade().Oid())
                    SubElement(Identifiers, "TradeNumber").text = str(s.Trade().Oid())
                    instrument = s.Trade().Instrument()
                    
                    insType = str(instrument.InsType())
                    if insType == 'Curr':
                        try:
                            insType = fxTypeMapper[s.Trade().TradeProcess()]
                           
                        except: 
                            print 'Exception'
                    elif insType == 'Option' and instrument.UnderlyingType() == 'Curr':
                        insType = 'FX Option'
                        
                    SubElement(Identifiers, "InstrumentType").text = insType

                    SubElement(Identifiers, "CFCAccount").text = str(CFCAccount)
                    Financials = SubElement(Root, "Financials")
                    
                    
                    if desk == 'InterDesk':
                        SubElement(Financials, "Amount").text = str(posting)
                    elif desk == 'ClientCFC':
                        SubElement(Financials, "Amount").text = str(posting*-1)
        
                    SubElement(Financials, "CurrencyName").text = str(s.Currency().Name())            
                    SubElement(Financials, "PayDate").text = str(s.PayDate())
                    
                    Acquirer = SubElement(Root, "Acquirer")
                    
                    SubElement(Acquirer, "AcquirerName").text = str(s.Trade().Acquirer().Name())
                    SubElement(Acquirer, "AcquirerNbr").text = str(s.Trade().Acquirer().Oid())
                    if s.Trade().Acquirer().add_info("BarCap_Eagle_SDSID"):
                        SubElement(Acquirer, "AcquirerSDSId").text = str(s.Trade().Acquirer().add_info("BarCap_Eagle_SDSID"))
                    else:
                        SubElement(Acquirer, "AcquirerSDSId").text = ''
                    SubElement(Acquirer, "AcquirerMidasCustomerNbr").text = str(accountNumber)
                    SubElement(Acquirer, "AcquirerPortfolio").text = str(s.Trade().Portfolio().Name())

                    Counterparty = SubElement(Root, "Counterparty")
                    
                    SubElement(Counterparty, "CounterpartyName").text = str(s.Trade().Counterparty().Name())
                    SubElement(Counterparty, "CounterpartyNbr").text = str(s.Trade().Counterparty().Oid())
                    if s.Trade().Counterparty().add_info("BarCap_Eagle_SDSID"):
                        SubElement(Counterparty, "CounterpartySDSId").text = str(s.Trade().Counterparty().add_info("BarCap_Eagle_SDSID"))
                    else:
                        SubElement(Counterparty, "CounterpartySDSId").text = ''            
                    
                    if s.Trade().Counterparty().Type() == 'Intern Dept': #internal department
                        internal = 'True'
                    SubElement(Counterparty, "InternalParty").text = str(internal)
                    
                    try:
                        #if __uniqueMessage(s, Root, objectName):
                            nostroMessage = tostring(Root)
                            #mqMessenger.Put(nostroMessage)     
                            f = open(r'c:\SPARKS\simOutput_nostro'+ael.date_today().to_string('%Y%m%d')+'_'+str(s.Trade().Oid())+'_'+str(feedFile)+'.txt', 'w')
                            f.write(nostroMessage)
                            f.close()
                            
                            diary = acm.FSettlementDiary[objectName]
                            if diary:
                                diary.Delete()
                            diary= acm.FSettlementDiary()
                            diary.Name(objectName)
                            
                            Tracking = SubElement(Root, "Tracking")
                            Tracking.set('Status', 'Sent')                            
                            diary.Text(tostring(Root))                            
                            diary.Commit()
                            
                        #else:
                         #   print 'This not in unique message consideration'

                    except Exception, e:
                        print str(e)

                else:
                    mess = 'Suppressing zero amount on trade %s' %s.Trade().Oid()
                    logger.WLOG(mess)                        
    except Exception, e:
        print str(e)


def InitializeModule():
    global configuration, logger#, mqMessenger

    configuration = Spark_Nostro_MQConfig.MqXmlConfig(Spark_Nostro_MQConfig.NOSTRO_SEND_NODE, Spark_Nostro_MQConfig.config)
    logFileName = "%s%s%s.log" % (configuration.LogPath, MODULE_NAME, time.strftime('%Y%m%d'))
    logger = FLogger.FLogger(MODULE_NAME, configuration.LogLevel, True, False, True, True, logFileName)
    #mqMessenger = MqMessenger(configuration, logger)
    #if not os.path.exists(path):
    #    os.mkdir(path) 


def productMovementSuppressed(m):
    if (m.Trade().Instrument().InsType() == 'Repo/Reverse' and m.Type() in REPO_SUPPRESSIONS):
        return True
    elif (m.Trade().Instrument().InsType() == 'Deposit' and m.Type() in DEPO_SUPPRESSIONS):
        return True
        

def validateSelection(trades, currency, runDate):
    validEntries = acm.FList()
    for t in trades:
        valid = [m for m in t.MoneyFlows(runDate, runDate) if m.Currency() == currency]
        #print 'Length of valid entries',len(valid),runDate,t.Oid()
        for m in valid:
            print 'Reading ***', m
            #certain flows like tho se that represent scrip are not meant to flow as amounts to the CFC accounts
            if (m.Type() in GLOBAL_SUPPRESSIONS):
                logger.WLOG('Suppressing global flow on trade %s of type: %s' %(m.Trade().Oid(), m.Type()))
            elif (productMovementSuppressed(m)):
                logger.WLOG('Suppressing flow on trade %s of type: %s on %s' %(m.Trade().Oid(), m.Type(), m.Trade().Instrument().InsType()))
            else:
                #print 'Found valid entry for trade',m.Trade().Oid(),m.Type(),m.Trade().Instrument().InsType()
                #print 'Directory money flow'
                validEntries.Add(m)
    return validEntries

    
ael_gui_parameters = { 'windowCaption':'Spark Settlement Feed'}
#Variable Name, Display Name, Type, Candidate Values, Default, Mandatory, Multiple, Description, Input Hook, Enabled
ael_variables = [ ('Currency', 'Currency: ', 'FCurrency', None, None, 1, 1, 'Currency'),    
                  ('Date', 'Date', 'string', ['TODAY', 'PREVBUSDAY', 'NEXTBUSDAY'], 'TODAY', 1, 0, 'Date', None, 1) ]

def ael_main(parameter):    
    currencies = parameter['Currency']
    feedFile = 0
    #desk = parameter['Portfolio']
    desk = acm.FArray()
    physicalPorts = acm.FPhysicalPortfolio.Select('name = "Call_Unallocated_Pace"')
    for prt in physicalPorts:
        if prt.add_info('MIDAS_Customer_Num'):
            addInfo = acm.FAdditionalInfo.Select('recaddr = %i' %prt.Oid())
            desk.Add(prt)
            
    print ('Run for desks %s and currencies %s' %(desk, currencies))
    
    try:
        if parameter['Date'].upper() == 'TODAY':
            runDate = TODAY
        elif parameter['Date'].upper() == 'PREVBUSDAY':
            runDate = PREVBUSDAY 
        elif parameter['Date'].upper() == 'NEXTBUSDAY':
            runDate = NEXTBUSDAY
        else:
            runDate = ael.date(parameter['Date'])
            runDate = parameter['Date']            
    except Exception, e:
        ael.log('Error parsing date input:' + str(e))
        raise Exception('Error parsing date input:' + str(e))

    if currencies:
        try:
            InitializeModule()
            FLogger.FLogger('Initialized the SPARKS adapter....')
            EXPIRYWINDOW = calendar.AdjustBankingDays(runDate, -5)
            for c in currencies:
                for d in desk:
                    print '------------------------------------------------------------------'
                    print 'Trade selection start for ' + d.Name() + ' for currency ' + c.Name()
                    print '------------------------------------------------------------------'
                    Query = acm.CreateFASQLQuery(acm.FTrade, 'AND')
                    Query.AddAttrNode('Portfolio.Name', 'EQUAL', d.Name())
                    Query.AddAttrNode('Instrument.Otc', 'EQUAL', True)
                    #Query.AddAttrNode('Oid','EQUAL',42958576)
                    expiry = Query.AddOpNode('OR')
                    expiry.AddAttrNode('Instrument.ExpiryDate', 'GREATER_EQUAL', EXPIRYWINDOW)
                    expiry.AddAttrNode('Instrument.ExpiryDate', 'LESS_EQUAL', acm.Time().SmallDate())
                    tradeStatus = Query.AddOpNode('OR')
                    tradeStatus.AddAttrNode('Status', 'EQUAL', Utils.GetEnum('TradeStatus', 'BO Confirmed'))
                    tradeStatus.AddAttrNode('Status', 'EQUAL', Utils.GetEnum('TradeStatus', 'BO-BO Confirmed'))
                    tradeStatus.AddAttrNode('Status', 'EQUAL', Utils.GetEnum('TradeStatus', 'FO Confirmed'))
                    tradeStatus.AddAttrNode('Status', 'EQUAL', Utils.GetEnum('TradeStatus', 'Terminated'))
                    trades = Query.Select()
                    validEntries = validateSelection(trades, c, runDate)
                    
                    for t in trades:
                        print 'Found trade_________________', t.Oid()
                    
                    for m in validEntries:
                        clientCFC = __hasSSI_clientCFC(m)
                        print 'money valid entries', m
                        __simOutput(m, feedFile, 'InterDesk', clientCFC)
                        
                        if clientCFC!='':
                            print '************** 1', clientCFC
                            if m.Trade().Instrument().Currency().Name()!='ZAR':
                                __simOutput(m, feedFile+1, 'ClientCFC', clientCFC)
                    print '------------------------------------------------------------------'
                    print 'Settlement selection done - now process postings for %s for %s' %(d.Name(), c.Name())
                    print '------------------------------------------------------------------'
                    print ''

            
            #mqMessenger.DisconnectQueueManager()
        except Exception, e:
            print 'Error processing module: %s' %str(e)
