"""
Description
===========
Date                          :  2018-02-07
Purpose                       :  SBL Uploader
Department and Desk           :  SBL
Requester                     :  Natasha Williams
Developer                     :  Ondrej Bahounek

Details:
========
This script replaces extenal SBL Upload Sheet that used AMBA meesages.
The Uploader will be completely built into FA which allows faster booking
and better error handling.
Script expects input file in CSV or XSL format.
Result is one trade and one new instrument for every row of the file.

Changes:
========
2020-01-09  CHG0073639   Libor Svoboda    Set rolling period, pay day method 
                                          and settle category.
"""

from datetime import datetime
import xlrd
import acm
from at_ael_variables import AelVariableHandler
from at_logging import getLogger
from PS_Functions import modify_asql_query
import FRunScriptGUI
from at_feed_processing import (SimpleCSVFeedProcessor,
                                SimpleXLSFeedProcessor,
                                notify_log)
from at_email import EmailHelper

LOGGER = getLogger(__name__)
TODAY = acm.Time.DateToday()
CALENDAR = acm.FCalendar['ZAR Johannesburg']

SETTLE_CATEGORY = {
    "SWIFT": "SL_STRATE",
    "DOM": "SL_CUSTODIAN",
}
LENDER_SPLIT_FEE = {
    'SLL SASOL PENSION FUND': 0.6,
}


fileFilter = "CSV Files (*.csv)|*.csv|XLS Files (*.xls)|*.xls|XLSX Files (*.xlsx)|*.xlsx|"
inputFile = FRunScriptGUI.InputFileSelection(FileFilter=fileFilter)

ael_variables = AelVariableHandler()
ael_variables.add(
    'input_file',
    label = 'File',
    cls = inputFile,
    default = inputFile,
    #default=r'c:\DEV\Perforce\FA\features\ABITFA-5097 - SBL uploader.br\input\sl_upload_file_excel_test.xlsx',
    mandatory = True,
    multiple = True,
    alt = 'Input file in CSV or XLS format.'
    )

ael_variables.add(
        name="send_email",
        label="Send Email",
        cls="bool",
        collection=(True, False),
        default="bool",
        mandatory=False,
        multiple=False,
        alt="If you require a notification email for trades to be closed."
        )
        
#Parameters for sending emails
ael_variables.add(
    'email_recipients',
    label='Email Recipients',
    default='AbcapPrimeMO@absa.africa',
    multiple=True,
    mandatory=False,
    alt=('Email recipients')
    )
            
        
def to_html(rws):
    """Construct output email"""
    res_text = '<table width="200" border="1">'
    #Email table with its titled columns
    res_text += "<tr>" + "".join(map("<td><b>{0}</b></td>".format, ("Trade No.", "Trade Time"))) + "</tr>"
    for rows in rws:
        line = "<tr>" + "".join(map("<td>{0}</td>".format, rows)) + "</tr>"
        res_text += line
        
    return res_text + "</table>"
    
    
def construct_body(trades):
    """Construct output table rows given all the newly booked trades"""
    environment = acm.FDhDatabase['ADM'].InstanceName()
    
    msg = "The following script ran successfully: " + "<br>" +__name__ + "<br><br>"
    msg += "Please close the trades below in " + environment + ":"
    msg += "<br /><br />"
    rows = [(acm.FTrade[trade].Oid(), acm.FTrade[trade].TradeTime()) for trade in trades]
    msg += to_html(rows)
    
    msg += "<br /><br />"
    
    #msg += Regards, + "<br><br>"
    return msg

        
def send_email(subject, body, recipients):
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
        LOGGER.info("Email sent successfully.")
    except Exception as exc:
        LOGGER.exception(exc)
    

class Container(object):
    
    ADDINF_DELIM = ':'
    
    EXTRA_ALL_IN_PRC = 'All In Price'
    EXTRA_CLOSING_TRADE = 'Closing Trade'
    EXTRA_DATA_NAMES = (EXTRA_ALL_IN_PRC, EXTRA_CLOSING_TRADE, )
    def __init__(self):
        self.props = {}
        self.addinfs = {}
        self.extra_data = {}
        
    def add_prop(self, prop, val):
        if type(val) == unicode:
            val = str(val)
        prop_addinf = prop.split(self.ADDINF_DELIM)

        if len(prop_addinf) == 1:
            if prop in self.EXTRA_DATA_NAMES:
                self.extra_data.update({prop:val})  # obj property
            else:
                self.props.update({prop:val})  # extra data
        else:
            self.addinfs.update({prop_addinf[1]:val})  # addinfo
        
    def get_props(self):
        return self.props
        
    def get_addinfs(self):
        return self.addinfs


class MainProcessor(object):

    PROP_DELIMITER = ':'
    NAME_TRD = 'trade'
    NAME_INS = 'ins'
    NAME_LEG = 'leg'
    
    SPECIAL_MAPPING = {
        'Fee':"%s%s%s"%(NAME_LEG, PROP_DELIMITER, "FixedRate"),
        'Price':"%s%s%s"%(NAME_INS, PROP_DELIMITER, "RefPrice"),
        'CP_Portfolio':"%s%s%s"%(NAME_TRD, PROP_DELIMITER, "MirrorPortfolio"),
        'All In Price':"%s%s%s"%(NAME_INS, PROP_DELIMITER, "All In Price"),
        'Closing Trade':"%s%s%s"%(NAME_INS, PROP_DELIMITER, "Closing Trade")
        #'StartDate':"%s%s%s"%(NAME_INS, PROP_DELIMITER, "StartDate"),
        #'ExpiryDate':"%s%s%s"%(NAME_INS, PROP_DELIMITER, "ExpiryDate"),
        }
        
    def __init__(self):
        self.eof = False
        self._properties = []
        self.calc_space = acm.Calculations().CreateStandardCalculationsSpaceCollection()
        self.closing_trades = []
        
    def _process_record(self, record, dry_run):
        (_index, record_data) = record
        
        if self.eof:
            return
        
        if not self._properties:
            self._properties = record_data.keys()
            LOGGER.info("Reading properties: %s" % ", ".join(map(str, self._properties)))
        
        if not record_data['ins:Underlying']:
            self.eof = True
            return
        
        LOGGER.info("LINE #%d: %s" % (_index, record_data))
        ins_container = Container()
        leg_container = Container()
        trd_container = Container()
        
        try:
            for prop, val in record_data.items():
                props = self.SPECIAL_MAPPING.get(prop, prop)
                splits = props.split(self.PROP_DELIMITER, 1)
                if len(splits) > 1:
                    prop_type = splits[0]
                    prop_name = splits[1]
                    if prop_type == self.NAME_INS:
                        ins_container.add_prop(prop_name, val)
                    elif prop_type == self.NAME_LEG:
                        leg_container.add_prop(prop_name, val)
                    elif prop_type == self.NAME_TRD:
                        trd_container.add_prop(prop_name, val)
                
            lender = (trd_container.get_addinfs()['SL_G1Counterparty2']
                      if 'SL_G1Counterparty2' in trd_container.get_addinfs()
                      else '')
            instr = self.create_instrument(ins_container, leg_container, lender)
            LOGGER.info("Created new instrument: '%s'" % instr.Name())
            
            trade = self.create_trade(instr, trd_container, lender)
            LOGGER.info("Created new trade: %s" % trade.Name())
            
            if ins_container.EXTRA_CLOSING_TRADE in record_data.keys():
                self.closing_trade_list(ins_container)
            
        except Exception as exc:
            LOGGER.exception(exc)
            raise
            
    def _format_date(self, the_date, format="%Y-%m-%d"):
        if type(the_date) == float:
            the_date = str(xlrd.xldate.xldate_as_datetime(the_date, 0).date())
        
        if '/' in the_date:
            dt = datetime.strptime(the_date, '%d/%m/%Y')
        else:
            dt = datetime.strptime(the_date, '%Y-%m-%d')
        return dt.strftime(format)
            
    def get_name(self, prop_container):
        start_date = self._format_date(prop_container.get_props()['StartDate'], format='%y%m%d')
        end_date = self._format_date(prop_container.get_props()['ExpiryDate'], format='%y%m%d')
        name = "%(underlying)s/%(start_date)s/%(end_date)s" %{
            'underlying':prop_container.get_props()['Underlying'],
            'start_date':start_date,
            'end_date':end_date}
        return name

    def sl_construct_name(self, name):
        sl = acm.FSecurityLoan[name]
        if not sl:
            return name
        i = 1
        while True:
            test_name = "{0}/#{1}".format(name, i)
            if not acm.FSecurityLoan[test_name]:
                return test_name
            i += 1
            if i > 100:
                raise RuntimeError("Instrument name index too high: %d" %i)
                
    def sl_construct_name2(self, name):
        """ First run of this function is quite slow. """
        sls = acm.FSecurityLoan.Select("name like '%s*'" %name)
        if not sls:
            return name
        
        max_oid = max(sl.Oid() for sl in sls)
        ins_name = acm.FInstrument[max_oid].Name()
        hash = ins_name.find("#")
        if hash == -1:
            return "{0}/#{1}".format(name, 1)
        
        last_num = int(ins_name[hash+1:])
        return "{0}/#{1}".format(name, last_num+1)
        
    def _get_roll_base_day(self, calendar, period, star_date):
        if period == '0d':
            return star_date
        if period == '1d':
            return star_date
        elif period == '1w':
            # next Monday
            next_week = acm.Time.DateAdjustPeriod(star_date, '1w')
            monday = acm.Time.FirstDayOfWeek(next_week)
            #bus_day_monday = calendar.AdjustBankingDays(
            #    calendar.AdjustBankingDays(monday, -1), 1)
            return monday
        elif period == '1m':
            next_month = acm.Time.DateAdjustPeriod(star_date, '1m')
            first_of_month = acm.Time.FirstDayOfMonth(next_month)
            #bus_day_month = calendar.AdjustBankingDays(
            #    calendar.AdjustBankingDays(first_of_month, -1), 1)
            return first_of_month
        else:
            raise ValueError("Unrecognised period: '%s'" % period)        

    def create_instrument(self, ins_container, leg_container, lender=''):
        # always create a new instrument
        ins_base_name = self.get_name(ins_container)
        ins_name = self.sl_construct_name(ins_base_name)
            
        sl_ins = acm.FSecurityLoan()
        sl_ins.RegisterInStorage()
        sl_ins.Quotation('Clean')
        sl_ins.QuoteType('Clean')
        quotationFactor = sl_ins.Quotation().QuotationFactor()
        
        acm.BeginTransaction()
        try:
            sl_ins.Currency('ZAR')
            underlying = acm.FInstrument[ins_container.get_props()['Underlying']]
            sl_ins.UnderlyingType(underlying.InsType())  # check if needed
            sl_ins.OpenEnd('Open End')
            sl_ins.SpotBankingDaysOffset(1)
            start_date = self._format_date(ins_container.get_props()['StartDate'])
            expiry_date = self._format_date(ins_container.get_props()['ExpiryDate'])
            if CALENDAR.IsNonBankingDay(None, None, start_date):
                raise Exception("Start date {date} must be a banking day".format(date=start_date))
            sl_ins.StartDate(start_date)
            sl_ins.ExpiryDate(expiry_date)
            
            for property, value in ins_container.get_props().items():
                sl_ins.SetProperty(property, value)
            
            leg = sl_ins.CreateLeg(True)
            
            leg.StartDate(start_date)
            leg.EndDate(expiry_date)
            leg.LegType('Fixed')
            leg.DayCountMethod('Act/365')
            leg.PayCalendar('ZAR Johannesburg')
            
            for property, value in leg_container.get_props().items():
                if property == 'FixedRate' and lender in LENDER_SPLIT_FEE:
                    value = float(value) * LENDER_SPLIT_FEE[lender]
                leg.SetProperty(property, value)
            
            leg.PayDayMethod('None')
            sl_cfd = ('SL_CFD' in ins_container.get_addinfs() 
                      and ins_container.get_addinfs()['SL_CFD'] == 'Yes')
            if sl_cfd:
                leg.RollingPeriod('1d')
            else:
                leg.RollingPeriod('1m')
                
            roll_day = self._get_roll_base_day(leg.PayCalendar(), leg.RollingPeriod(), leg.StartDate())
            leg.RollingPeriodBase(roll_day)
            
            all_in_prc = ins_container.extra_data[ins_container.EXTRA_ALL_IN_PRC]
            
            if all_in_prc != '':
                all_in_prc = float(all_in_prc)
            
            if all_in_prc != '':
                ref_price = sl_ins.RefPrice()
                if underlying.InsType() in ('Bond', 'IndexLinkedBond'):
                    ref_price = all_in_prc
                
                if sl_ins.RefValue() == 0:
                    ref_price = underlying.Calculation().PriceConvert(
                        self.calc_space, ref_price, 'Pct of Nominal', underlying.Quotation(), start_date)
                    sl_ins.RefPrice(ref_price)
                    ref_val = sl_ins.ContractSize() / (all_in_prc * quotationFactor)
                    sl_ins.RefValue(ref_val)
                    
            else:
                to_dirty = False
                ref_price = ins_container.get_props()['RefPrice']
                sl_ins.RefPrice(ref_price)
                
                calc = underlying.Calculation().PriceToUnitValue(
                    self.calc_space, sl_ins.RefPrice(), underlying.Quotation(), start_date, to_dirty)
                all_in_price = round(calc.Number() * 100, 5)
                
                if sl_ins.RefValue() == 0:
                
                    ref_val = sl_ins.ContractSize() / (all_in_price * quotationFactor)
                    sl_ins.RefValue(ref_val)
                
                
            sl_ins.Commit()

            add_infs = sl_ins.AdditionalInfo()
            for property, value in ins_container.get_addinfs().items():
                if value != "":
                    if property == "SL_RecallDate":
                        value = self._format_date(value)
                    add_infs.SetProperty(property, value)
                
            acm.CommitTransaction()
        except Exception as exc:
            acm.AbortTransaction()
            LOGGER.exception(exc)
            raise
        
        return sl_ins

    def create_trade(self, instr, trd_container, lender=''):
        trd = acm.FTrade()
        trd.Instrument(instr)
        trd.Currency(instr.Currency())
        trd.Status('Simulated')
        trd.ValueDay(instr.StartDate())
        trd.AcquireDay(instr.StartDate())
        trd.HaircutType('Discount')
        
        for property, value in trd_container.get_props().items():
            if value == "":
                continue
                
            if property == "TradeTime":
                value = self._format_date(value)
            trd.SetProperty(property, value)
        
        trd.Quantity(trd.Quantity() / instr.RefValue())
        
        trd.RegisterInStorage()
        
        add_infs = trd.AdditionalInfo()
        for property, value in trd_container.get_addinfs().items():
        
            if property == "SL_SWIFT" and value == "":
                add_infs.SetProperty(property, "SWIFT")
                
            if value != "":
                if property == "SL_SWIFT" and value in SETTLE_CATEGORY:
                    trd.SettleCategoryChlItem(SETTLE_CATEGORY[value])
                if property == 'SL_G1Fee2' and lender in LENDER_SPLIT_FEE:
                    value = float(value) * LENDER_SPLIT_FEE[lender]
                add_infs.SetProperty(property, value)
            
        trd.Commit()
        return trd


    def closing_trade_list(self, ins_container):
        closing_trade = ins_container.extra_data[ins_container.EXTRA_CLOSING_TRADE]
        self.closing_trades.append(int(closing_trade))


class CSVCreator(MainProcessor, SimpleCSVFeedProcessor):
  
    def __init__(self, file_path):
        MainProcessor.__init__(self)
        SimpleCSVFeedProcessor.__init__(self, file_path, do_logging=False)


class XLSCreator(MainProcessor, SimpleXLSFeedProcessor):
  
    def __init__(self, file_path):
        
        MainProcessor.__init__(self)
        SimpleXLSFeedProcessor.__init__(self, file_path, sheet_index=0, sheet_name=None)


def ael_main(ael_dict):
    file_path = str(ael_dict['input_file'])
    LOGGER.info("Input file: %s", file_path)

    if ael_dict["send_email"]:
        
        #Set the list of email recipients
        recipients = list(ael_dict["email_recipients"])
        if len(recipients) == 0:
            msg = 'Missing email adddress. Trades not booked.'
            print msg
            raise Exception(msg)
        else:
            if file_path.endswith(".csv"):
                proc = CSVCreator(file_path)
            else:
                proc = XLSCreator(file_path)
    
            proc.add_error_notifier(notify_log)
            proc.process(False)
        
            #Set the subject of the email
            subject = "Trades to close"
            
            #Construct the email output to be sent
            body = construct_body(proc.closing_trades)
            
            #Call email sender
            send_email(subject, body, recipients)
        
    else:
        if file_path.endswith(".csv"):
            proc = CSVCreator(file_path)
        else:
            proc = XLSCreator(file_path)
    
        proc.add_error_notifier(notify_log)
        proc.process(False)
    
    LOGGER.info("Completed successfully.")
