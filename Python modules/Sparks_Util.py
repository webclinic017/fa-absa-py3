
'''-----------------------------------------------------------------------------
TASK                    :  Spark Code Optimization
PURPOSE                 :  To improve performance and memory usage of the process
DEPATMENT AND DESK      :  PCG/Ops
REQUESTER               :  Richard Gwilt\Linda Breytenbach
DEVELOPER               :  Paseka Motsoeneng
CR NUMBER               :  ABITFA-4028
--------------------------------------------------------------------------------
HISTORY
================================================================================
Date        Change no      Developer               Description
--------------------------------------------------------------------------------
??????????  ??????????                             Initial Implementation
2018-07-19  CHG1000679237  Libor Svoboda           Fix the Front - Sparks
'''
import sys
import time
import datetime
import acm
import ael
from collections import OrderedDict
import xml.etree.ElementTree as etree
from xml.etree.ElementTree import Element, SubElement, tostring, fromstring
from Spark_Nostro_MQWrapper import MqMessenger
from Sparks_Config import SparksConfig
from at_logging import getLogger

# Dashboard Settings/imports ---------------------------------------------------------
mongo_egg_path = 'c:\\Python27\\lib\\site-packages\\pymongo-3.3.0-py2.7-win-amd64.egg'
xml_egg_path = 'c:\\Python27\\lib\\site-packages\\xmltodict-0.10.2-py2.7.egg'
sys.path.append(mongo_egg_path)
sys.path.append(xml_egg_path)
from pymongo import MongoClient
import xmltodict
import requests

LOGGER = getLogger(__name__)

ACCOUNT_CODE = '1202'
GLOBAL_SUPPRESSIONS = (
    'Security Nominal',
    'End Security',
    'Credit Default',
    'Interest Reinvestment',
)
PAYMENT_SUPPRESSIONS = (
    'CFC Interest',
)
FUTUREFWARD_SUPPRESSIONS = (
    'Future',
)
#AMFD-96/111
DEPO_SUPPRESSIONS = (
    'Call Fixed Rate Adjustable',
    'Fixed Rate Adjustable',
    'Call Float Rate',
    'Call Fixed Rate',
    'Call Fixed Rate Adjustable'
)
OPENEND_DEPO_SUPPRESSSIONS = (
    'Redemption Amount',
)
REPO_SUPPRESSIONS = (
    'Coupon',
    'Coupon transfer',
)
CURR_NO_CENTS = (
    'JPY', 
    'UGX',
)
CURRENCY_MAPPINGS = {
    'MZM': 'MZN',
}
SUPPRESSED_CURR = (
    'ZAR',
    'XAU',
    'XPD',
    'XPT',
    'XAG',
)
CALENDAR = acm.FCalendar['ZAR Johannesburg']
CALC_SPACE = acm.Calculations().CreateStandardCalculationsSpaceCollection()
MONEYFLOW_MAPPINGS = {
    'CashFlow': 'CF', 
    'Dividend': 'DIV', 
    'Payment': 'PMT', 
    'Trade': 'TRD', 
    'Instrument': 'INS', 
    'Coupon': 'CP', 
    'Coupon transfer': 'CPT',
    'Fixed Amount': 'FA',
    'Redemption': 'RD',
    'Fixed Amount Transfer': 'FAT',
    'Security Nominal': 'SN',
    'End Security': 'ES',
}
FO_ID_PREFIX = 'SPX_'
FO_ID_FLAG = {
    'task': 'T',
    'listener': 'L',
    'default': 'D',
}

''' AMD-346. '''
SUPPRESSED_INSTRUMENT_OPEN_END = (
    'Open End',
    'Terminated'
)


class SparksUtil(object):

    def __init__(self, run_date, id_flag='task'):
        self._run_date = run_date
        self._next_bus_day = CALENDAR.AdjustBankingDays(run_date, 1)
        
        self._id_flag = (FO_ID_FLAG[id_flag] if id_flag in FO_ID_FLAG 
                            else FO_ID_FLAG['default'])
        
        self._config = SparksConfig('Send') 
        self._next_day_curr = self._config.next_day_currencies
        
        client = MongoClient(self._config.mongo_db_repl_set_conn_str)
        db = client.spark_db
        self._posts = db.posts
    
    @classmethod
    def get_moneyflow_id(cls, mf):
        source_ref = MONEYFLOW_MAPPINGS[mf.SourceObject().RecordType()]
        if mf.Type() in MONEYFLOW_MAPPINGS.keys():
            source_ref = MONEYFLOW_MAPPINGS[mf.Type()]
 
        currency_name = mf.Currency().Name()
        if currency_name in CURRENCY_MAPPINGS.keys():
            currency_name = CURRENCY_MAPPINGS[currency_name] 
        
        if source_ref == 'TRD':
            source_ref += currency_name
        
        return "%s%s%s_%s" % (mf.Trade().Oid(), 
                              source_ref, 
                              mf.SourceObject().Oid(), 
                              ael.date(mf.PayDate()).to_string('%m%d'))
    
    @classmethod
    def get_last_id(cls, pymongo_cursor, mf_id):
        ids = {}
        for doc in pymongo_cursor:
            if doc['_id'] == mf_id:
                key = 0
            else:
                key = int(doc['_id'].split('_')[-1])
            ids[key] = doc['_id']
        return ids[max(ids.keys())]
    
    @classmethod
    def get_new_id(cls, mf_id, last_id=''):
        if not last_id:
            return mf_id
        if mf_id == last_id:
            return '%s_1' % mf_id
        last_id_split = last_id.split('_')
        index = int(last_id_split[-1]) + 1
        return '_'.join(last_id_split[:-1] + [str(index)])
    
    @classmethod
    def product_movement_suppressed(cls, mf):
        if (mf.Trade().Instrument().InsType() == 'Deposit' 
                and mf.Type() in DEPO_SUPPRESSIONS 
                and mf.SourceObject().RecordType() == 'CashFlow' 
                and mf.SourceObject().Leg().Reinvest()):
			return True
        if (mf.Trade().Instrument().InsType() == 'Deposit'
                and mf.Trade().Instrument().OpenEnd() in SUPPRESSED_INSTRUMENT_OPEN_END
                and mf.Type() in OPENEND_DEPO_SUPPRESSSIONS):
            return True
        if (mf.Trade().Instrument().InsType() == 'Future/Forward' 
                and mf.Type() in FUTUREFWARD_SUPPRESSIONS):
            return True
        return False
    
    @classmethod
    def is_moneyflow_valid(cls, mf):
        trade = mf.Trade()
        if mf.Currency().Name() in SUPPRESSED_CURR:
            msg = 'Suppressing flow on trade %s, MF currency: %s.'
            LOGGER.info(msg % (trade.Oid(), mf.Currency().Name()))
            return False
        if (mf.Type() in GLOBAL_SUPPRESSIONS 
                or mf.Type() in PAYMENT_SUPPRESSIONS):
            msg = 'Suppressing flow on trade %s of type: %s.'
            LOGGER.info(msg % (trade.Oid(), mf.Type()))
            return False
        if cls.product_movement_suppressed(mf):
            msg = 'Suppressing flow on trade %s of type: %s on %s.'
            LOGGER.info(msg % (trade.Oid(), mf.Type(), trade.Instrument().InsType()))
            return False
        #AMFD-93
        ins = trade.Instrument()
        today_str = datetime.datetime.today().strftime('%Y-%m-%d')
        if mf.PayDate() < today_str and ins.InsType() in ('Bill', 'Bond') and trade.Type() == 'Aggregate':
            msg = 'Suppressing flow on trade %s. Pay date: %s. Instrument type: %s. Trade type: %s.'
            LOGGER.info(msg % (trade.Oid(), mf.PayDate(), ins.InsType(), trade.Type()))
            return False
        return True
    
    @classmethod
    def get_message_counterparty(cls, mf):
        if (mf.SourceObject().RecordType() == 'Payment'
                and mf.SourceObject().Party()):
            return mf.SourceObject().Party()
        if mf.Counterparty():
            return mf.Counterparty()
        return mf.Trade().Counterparty()
    
    @classmethod
    def get_reversal_message(cls, original, mode):    
        retVal = Element("CashflowMessage")
        for node in original.getchildren():
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
                        SubElement(Identifiers, child.tag).text = "%s%s" %(child.text, mode)
                    else:
                        Identifiers.append(child)
                retVal.append(Identifiers)
        return retVal
    
    ''' Static method that takes the external id (optional key) and slices it to only take the the first 16 characters,
        if the external id is longer than that. '''
    @staticmethod
    def slice_external_id(optional_key):
        if optional_key != None and len(optional_key) > 0 : 
            optional_key = optional_key[0:16]  
            LOGGER.info('ExternalId field %s.'%optional_key)
        else:
            LOGGER.info('Empty ExternalId field found, %s'%optional_key)
        return optional_key
            
    @classmethod
    def create_message(cls, mf, mf_id=''):
        root = Element("CashflowMessage")
        if not cls.is_moneyflow_valid(mf):
            return root
        mf_currency_name = mf.Currency().Name()
        mf_id = mf_id if mf_id else cls.get_moneyflow_id(mf)
        trade = mf.Trade()
        internal = 'False'
        account_seq = '01'
        rounding = 2
        if mf_currency_name in CURR_NO_CENTS:
            rounding = 0
        try:
            posting = round(mf.Calculation().Projected(CALC_SPACE).Number(), rounding)
        except Exception as exc:
            msg = 'Failed to calculate projected value for %s: %s'
            LOGGER.exception(msg % (mf_id, str(exc)))
            posting = 0
        
        if not posting:
            LOGGER.info('Suppressing zero amount on trade %s.' % trade.Oid()) 
            return root
        
        midas_acct_seq = trade.Portfolio().add_info('MIDAS_Acct_Seq')
        #use DEF as default sequence if not 01
        if mf_currency_name in midas_acct_seq:
            list = midas_acct_seq.split(';')
            for item in list:
                if mf_currency_name in item:
                    account_seq = item.split('=')[1] 
        elif 'DEF' in midas_acct_seq:
            list = midas_acct_seq.split(';')
            for item in list:
                if 'DEF' in item:
                    account_seq = item.split('=')[1]

        account_num = trade.Portfolio().add_info('MIDAS_Customer_Num')
        
        if mf_currency_name in CURRENCY_MAPPINGS.keys():
            mf_currency_name = CURRENCY_MAPPINGS[mf_currency_name]
        
        CFC_account = account_num.zfill(6) + mf_currency_name + ACCOUNT_CODE + account_seq.zfill(2)                    
        
        Identifiers = SubElement(root, "Identifiers")
        
        SubElement(Identifiers, "SettlementId").text = mf_id
        SubElement(Identifiers, "PaymentRef").text = "Trd%s" %str(trade.Oid())
        SubElement(Identifiers, "TradeNumber").text = str(trade.Oid())
        
        #Slice the external id if needs be
        optional_key = str(trade.OptionalKey())
        SubElement(Identifiers, "ExternalId").text = SparksUtil.slice_external_id(optional_key)
        
        SubElement(Identifiers, "DefaultNostro").text = ''
        
        instrument = trade.Instrument()
        
        ins_type = str(instrument.InsType())
        if ins_type == 'Curr':
            if trade.IsFxSwapFarLeg():
                ins_type = 'FX Swap'
            elif trade.IsFxSwapNearLeg():
                ins_type = 'FX Swap'
            elif trade.IsFxForward():
                ins_type = 'FX Forward'
            elif trade.IsFxSpot():
                ins_type = 'FX Spot'
                
        elif ins_type == 'Option' and instrument.UnderlyingType() == 'Curr':
            ins_type = 'FX Option'
            
        SubElement(Identifiers, "InstrumentType").text = ins_type

        ''' AMD-456. '''
        SubElement(Identifiers, "ISINUndISINName").text = (str(instrument.ISIN_UndISIN_Name()))[0:16]
        SubElement(Identifiers, "PortfolioNumber").text = (str(mf.Trade().Portfolio().Oid()))[0:16]

        SubElement(Identifiers, "CFCAccount").text = str(CFC_account)
        Financials = SubElement(root, "Financials")
        SubElement(Financials, "Amount").text = str(posting)

        SubElement(Financials, "CurrencyName").text = str(mf_currency_name)            
        SubElement(Financials, "PayDate").text = str(mf.PayDate())

        ''' AMD-456. '''
        SubElement(Financials, "CashFlowType").text = (str(mf.Type()))[0:16]
        
        Acquirer = SubElement(root, "Acquirer")
        
        SubElement(Acquirer, "AcquirerName").text = str(trade.Acquirer().Name())
        SubElement(Acquirer, "AcquirerNbr").text = str(trade.Acquirer().Oid())
        if trade.Acquirer().add_info("BarCap_Eagle_SDSID"):
            SubElement(Acquirer, "AcquirerSDSId").text = str(trade.Acquirer().add_info("BarCap_Eagle_SDSID"))
        else:
            SubElement(Acquirer, "AcquirerSDSId").text = ''
        SubElement(Acquirer, "AcquirerMidasCustomerNbr").text = str(account_num)
        SubElement(Acquirer, "AcquirerPortfolio").text = str(trade.Portfolio().Name())

        Counterparty = SubElement(root, "Counterparty")
        ctpy = cls.get_message_counterparty(mf)
        SubElement(Counterparty, "CounterpartyName").text = str(ctpy.Name())
        SubElement(Counterparty, "CounterpartyNbr").text = str(ctpy.Oid())
        if ctpy.add_info("BarCap_Eagle_SDSID"):
            SubElement(Counterparty, "CounterpartySDSId").text = str(ctpy.add_info("BarCap_Eagle_SDSID"))
        else:
            SubElement(Counterparty, "CounterpartySDSId").text = ''            
        if ctpy.Type() == 'Intern Dept': #internal department
            internal = 'True'
        SubElement(Counterparty, "InternalParty").text = str(internal)
        return root
    
    def generate_fo_tran_id(self):
        """Generate unique ID for each message for Midas.
        Maximum length is 20 characters.
        """
        time_now = time.time()
        time_now_fraction = int((time_now - int(time_now)) * 1e6)
        time_now_fraction_hex = hex(time_now_fraction)[2:]
        return (FO_ID_PREFIX + time_now_fraction_hex 
                + str(int(time_now)) + self._id_flag)
    
    def _send_and_commit_message(self, message, mf_id, resend=False):
        fo_id = self.generate_fo_tran_id()
        Tracking = SubElement(message, "Tracking")
        Tracking.set('Status', 'Sent')
        Tracking.set('APFOTRANID', fo_id)         
	
        document = xmltodict.parse(tostring(message))
        document['_id'] = mf_id
        document['Timestamp'] = time.time()
        
        id_filter = {'_id': mf_id}
        diary = self._posts.find_one(id_filter)
        if diary:
            if not resend:
                LOGGER.info('Moneyflow object %s already in Db.' % mf_id)
                return
            self._posts.delete_one(id_filter)
        try:
            self._posts.insert_one(document)
            LOGGER.info('Moneyflow object %s commited to Db.' % mf_id)
            
            msg = tostring(message)
            web_api_end_point = self._config.web_api_end_point
            requests.post(web_api_end_point, {"Message":msg})
            LOGGER.info('Calling Web API with the message: %s' % tostring(message))
            
        except Exception as exc:
            msg = 'Failed to call the end point with the moneyflow object id %s: \nError: %s'
            LOGGER.exception(msg % (mf_id, str(exc)))
    
    
    def _process_moneyflow(self, mf):
        if mf.Trade().Status() == 'Void':
            mf_id = self.get_moneyflow_id(mf)
            self.reverse(mf_id, True)
        else:
            self.post(mf)
            
    
    def _is_future_mf(self, mf):
        curr = mf.Currency().Name()
        end_date = self._next_bus_day if curr in self._next_day_curr else self._run_date
        if mf.PayDate() > end_date:
            msg = 'Invalid moneyflow (%s, %s), future pay date: %s.'
            LOGGER.info(msg % (mf.Trade().Oid(), mf.Type(), mf.PayDate()))
            return True
        return False
    
    def connect_queue_manager(self):
        try:
            self._mq_messenger = MqMessenger(self._config)  
        except Exception as exc:
            LOGGER.exception('Failed to connect to queue: %s' % str(exc))
            raise
    
    def disconnect_queue_manager(self):
        if not self._mq_messenger:
            return
        try:
            self._mq_messenger.DisconnectQueueManager()
        except Exception as exc:
            LOGGER.exception('Failed to disconnect from queue: %s' % str(exc))
    
    def process_trades(self, trades):
        for trade in trades:
            if type(trade) in (str, int):
                trade = acm.FTrade[trade]
            if not trade:
                continue
            if trade.MidasSettlement():
                LOGGER.info('Trade suppressed MSI = True: %s.' % trade.Oid())
                continue
            moneyflows = []
            for mf in trade.MoneyFlows(self._run_date, self._next_bus_day):
                if (mf.PayDate() == self._next_bus_day 
                        and mf.Currency().Name() in self._next_day_curr):
                    moneyflows.append(mf)
                elif mf.PayDate() == self._run_date:
                    moneyflows.append(mf)
            
            for mf in moneyflows:
                try:
                    self._process_moneyflow(mf)
                except Exception as exc:
                    LOGGER.exception('Error on trade %s: %s' % (trade.Oid(), str(exc)))
    
    def messagesDiffer(self, original_message, new_message):
        original_xml_message = original_message
        new_xml_message = new_message
            
        for child in original_xml_message.getchildren():
            for inner_child in child.getchildren():
                value_in_original_mess = inner_child.text
                value_in_new_mess = new_xml_message.find('%s/%s'%(child.tag, inner_child.tag)).text
                
                if value_in_original_mess != value_in_new_mess:
                    '''AMFD-65'''
                    if inner_child.tag == 'CashFlowType':
                        if value_in_original_mess == value_in_new_mess[:15]:
                            continue
                    if (inner_child.tag == 'ExternalId' and value_in_original_mess is None) or (inner_child.tag == 'DefaultNostro' and value_in_original_mess > 0):
                        continue
                    return True
        return False

    
    def reverse(self, mf_id, void=False):
        orig_filter = {'_id': {'$regex': '^%s(_[0-9]+|)$' % mf_id}}
        orig_docs = self._posts.find(orig_filter)
        if not orig_docs.count():
            msg = 'Reverse: Original diary %s does not exist.' % mf_id
            LOGGER.info(msg)
            return
        last_diary_id = self.get_last_id(orig_docs, mf_id)
        void_diary_id = '%s-V' % last_diary_id
        rev_diary_id = '%s-Rev' % last_diary_id
        if (self._posts.find_one({'_id': void_diary_id})
                or self._posts.find_one({'_id': rev_diary_id})):
            msg = 'Reverse: Original message %s already reversed.' % last_diary_id
            LOGGER.info(msg)
            return
        diary = self._posts.find_one({'_id': last_diary_id})
        del diary['CashflowMessage']['Tracking']
        del diary['_id']
        del diary['Timestamp']
        diary_message = fromstring(xmltodict.unparse(diary, full_document=False))
        
        default_nostro_element = etree.Element("DefaultNostro")
        identifiers = diary_message.find('Identifiers') 
		
        external_id_element = etree.Element("ExternalId") #Creates a new xml tag
        external_id_element.text = '' #external_id_element: empty string for starters
        
        if identifiers.find("ExternalId") == None: #if there's no external id in the message
            trade_number = identifiers.find('TradeNumber').text
            trade = acm.FTrade[trade_number] 
            if str(type(trade)) == "<type 'FTrade'>":
                external_ref = SparksUtil.slice_external_id(trade.OptionalKey())
                external_id_element.text = external_ref    
            
            identifiers.append(external_id_element)  
            
        if identifiers.find("DefaultNostro") == None:
            identifiers.append(default_nostro_element)
            
        rev_id = void_diary_id if void else rev_diary_id
        rev_mode = '-V' if void else '-Rev'
        msg = 'Reverse: Processing reversal for %s.' % rev_id
        LOGGER.info(msg)
        rev_message = self.get_reversal_message(diary_message, rev_mode)
        self._send_and_commit_message(rev_message, rev_id)

                
    def post(self, mf):
        mf_id = self.get_moneyflow_id(mf)
        orig_filter = {'_id': {'$regex': '^%s(_[0-9]+|)$' % mf_id}}
        orig_docs = self._posts.find(orig_filter)
        last_diary_id = ''
        if orig_docs.count():
            last_diary_id = self.get_last_id(orig_docs, mf_id)
            void_diary_id = '%s-V' % last_diary_id
            rev_diary_id = '%s-Rev' % last_diary_id
            diary = self._posts.find_one({'_id': last_diary_id})
            del diary['CashflowMessage']['Tracking']
            del diary['_id']
            del diary['Timestamp']
            diary_message = fromstring(xmltodict.unparse(diary, full_document=False))
            message = self.create_message(mf, last_diary_id)
            
            if len(message) and not self.messagesDiffer(diary_message, message) and not (self._posts.find_one({'_id': void_diary_id}) or self._posts.find_one({'_id': rev_diary_id})):
                msg = 'Post: Message already sent %s.' % mf_id
                LOGGER.info(msg)
                return
            
            self.reverse(mf_id)
        new_id = self.get_new_id(mf_id, last_diary_id)
        new_message = self.create_message(mf, new_id)
        if not len(new_message) or self._is_future_mf(mf):
            msg = 'Post: Invalid moneyflow %s.' % mf_id
            LOGGER.info(msg)
            return
        msg = 'Post: Processing message %s.' % new_id
        LOGGER.info(msg)
        self._send_and_commit_message(new_message, new_id)
    
    
    def resend_failed_messages(self, acm_run_date=''):
        if acm_run_date:
            run_dt_date = datetime.datetime.strptime(acm_run_date, '%Y-%m-%d').date()
        else:
            run_dt_date = datetime.datetime.now().date()
        run_dt_min = datetime.datetime.combine(run_dt_date, datetime.time.min)
        run_dt_max = datetime.datetime.combine(run_dt_date, datetime.time.max)
        run_time_min = time.mktime(run_dt_min.timetuple())
        run_time_max = time.mktime(run_dt_max.timetuple())
        
        failed_docs = self._posts.find({
            'Timestamp': {'$gt': run_time_min, '$lt': run_time_max}, 
            'CashflowMessage.Tracking.@Status': {'$in': ['Failure', 'Exception']}
        })
        for diary in failed_docs:
            diary_id = diary['_id']
            del diary['CashflowMessage']['Tracking']
            del diary['_id']
            del diary['Timestamp']
            diary_message = fromstring(xmltodict.unparse(diary, full_document=False))
            LOGGER.info('Resending failure/exception for %s' % diary_id)
            self._send_and_commit_message(diary_message, diary_id, True)

