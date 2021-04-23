"""-----------------------------------------------------------------------------
PURPOSE              :  Client Valuation Statements Automation
                        Implementation of the business process logic used by
                        the Statements ATS's.
DESK                 :  PCG Collateral
DEVELOPER            :  Libor Svoboda
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date        Change no      Developer           Description
--------------------------------------------------------------------------------
2019-02-14  CHG1001362755  Libor Svoboda       Initial Implementation (FEC)
2019-03-14  CHG1001488095  Libor Svoboda       Enable Option statements
2019-04-12  CHG1001590405  Libor Svoboda       Enable Swap, Cap & Floor, and 
                                               Structured Deal statements
2019-06-14  CHG1001881233  Libor Svoboda       Update FEC layout
2020-06-03  CHG0103217     Libor Svoboda       Add SBL client statements
2020-06-23  CHG0108121     Libor Svoboda       Enable SBL Open Position XLSX
2020-10-20  CHG0132720     Libor Svoboda       Enable Deposit statements
"""
import datetime
import os
import re
import shutil
import smtplib
import time
from collections import defaultdict

import acm
import ael

import XMLReport
from at_email import EmailHelper
from at_logging import getLogger
from statements_calc import (CalcEngine, FECCalcEngine, OptionCalcEngine, 
                             SwapCalcEngine, ValuationsDefaultCalcEngine, 
                             StructuredCalcEngine, SBLFeeCalcEngine,
                             SBLMovementCalcEngine, SBLOpenPosCalcEngine,
                             SBLSummaryOpenPosCalcEngine,
                             SBLMarginCallCalcEngine,
                             SBLFinderFeeCalcEngine,
                             SBLDividendNotificationCalcEngine,
                             DepositCalcEngine, calc_trade_value)
from statements_params import (DATE_PATTERN_DOCS, FPARAMS, OUTPUT_DIR_PARAM, 
                               XSLT_NAME_DEFAULT, EMAIL_UNDELIVERED, EMAIL_CLIENT_VALUATIONS,
                               XSLT_NAME_WIDE, XSLT_NAME_SBL,
                               DATE_PATTERN_MONTH, LIVE_TRADE_PERIOD_DEFAULT,
                               PREVIEW_DIR_PARAM, LIVE_TRADE_PERIOD_SBL,
                               EMAIL_CLIENT_SBL, EMAIL_CLIENT_SBL_COLL,
                               SBL_FINDER_MAPPING, VALID_SBL_STATUS)
from statements_reports import (ValuationsReport, ReportBase, XLSXReportGenerator, 
                                SBLFeeReport, SBLMovementReport, SBLMovementXLSXGenerator,
                                SBLOpenPosCollReport, SBLOpenPosOpsReport,
                                SBLDividendNotificationReport,
                                SBLSummaryOpenPosReport,
                                SBLSummaryPosXLSXGenerator,
                                SBLMarginCallReport,
                                SBLFinderFeeReport, SBLFeeXLSXGenerator,
                                SBLOpenPosXLSXGenerator)
from statements_util import (format_date, get_param_value, 
                             get_first_step, get_last_step, get_steps,
                             date_to_dt,
                             first_day_of_month, last_day_of_month)
from SBL_Dividend_Summary_Report import CorporateActionsExtract, ProcessTrade


LOGGER = getLogger(__name__)
TODAY = acm.Time.DateToday()
ARCHIVED_CUTOFF_DEFAULT = acm.Time.DateAddDelta(TODAY, 0, 0, -LIVE_TRADE_PERIOD_DEFAULT)
ARCHIVED_CUTOFF_SBL = acm.Time.DateAddDelta(TODAY, 0, 0, -LIVE_TRADE_PERIOD_SBL)

PERMISSION_MODE = 0o775


def unix_chmod(path, mode):
    if os.name != 'nt':
        os.chmod(path, mode)


class EmptyTradeSelection(Exception):
    pass


class StatementProcess(object):
    
    invalid_chars = r'\/:*?"<>|'
    email_pattern = ('^[_a-zA-Z0-9-]+(\.[_a-zA-Z0-9-]+)*@[a-zA-Z0-9-]+'
                     '(\.[a-zA-Z0-9-]+)*(\.[a-zA-Z]+)$')
    generate_retries = 3
    statement_type = ''
    xlsx_report_gen = XLSXReportGenerator
    outputs = {
        'xml_string': {
            'calculator': CalcEngine,
            'xml_report': ReportBase,
            'formats': ['PDF', 'XLSX'], 
        },
    }
    landscape_pdf = True
    xslt_name = XSLT_NAME_DEFAULT
    doc_date_pattern = DATE_PATTERN_DOCS
    email_template = '%s %s'
    
    def __init__(self, business_process, statement_config):
        self._bp = business_process
        self._config = statement_config
        self._party = self._bp.Subject()
        self._party_id = self._bp.Subject().Oid()
        self._log_str = '%s, %s' % (self._bp.Subject().Name(), self._bp.Oid())
        self._trades = []
        self._error_msg = ''
        self._values = defaultdict(lambda: defaultdict(str))
    
    @staticmethod
    def get_emails(email_string):
        emails = []
        for email in email_string.split(','):
            if email.strip():
                emails.append(email.strip())
        return emails
    
    @staticmethod
    def create_dir(dirpath):
        try:
            os.makedirs(dirpath)
            unix_chmod(dirpath, PERMISSION_MODE)
        except OSError:
            if not os.path.isdir(dirpath):
                raise
    
    @staticmethod
    def is_valid(bp):
        val_date = bp.AdditionalInfo().BP_ValuationDate()
        if not val_date:
            return False
        if ((acm.ArchivedMode() and val_date >= ARCHIVED_CUTOFF_DEFAULT)
                or (not acm.ArchivedMode() and val_date < ARCHIVED_CUTOFF_DEFAULT)):
            return False
        return True
    
    @staticmethod
    def generate_pdf(output_formats):
        return 'PDF' in output_formats
    
    @staticmethod
    def generate_xlsx(output_formats):
        return 'XLSX' in output_formats
    
    @classmethod
    def get_output_dir(cls, val_date):
        output_root = get_param_value(FPARAMS, OUTPUT_DIR_PARAM)
        output_subpath = get_param_value(FPARAMS, '%s.Subpath' % cls.statement_type)
        output_dir = os.path.join(output_root, output_subpath)
        dt = datetime.datetime(*acm.Time.DateToYMD(val_date))
        return output_dir.format(dt)
    
    @classmethod
    def get_preview_dir(cls, val_date):
        preview_root = get_param_value(FPARAMS, PREVIEW_DIR_PARAM)
        preview_subpath = get_param_value(FPARAMS, '%s.Subpath' % cls.statement_type).replace('/', '\\')
        preview_dir = os.path.join(preview_root, preview_subpath)
        dt = datetime.datetime(*acm.Time.DateToYMD(val_date))
        return preview_dir.format(dt)
    
    @classmethod
    def get_email_sender(cls):
        return get_param_value(FPARAMS, '%s.Sender' % cls.statement_type)
    
    @classmethod
    def get_email_cc(cls):
        return get_param_value(FPARAMS, '%s.CC' % cls.statement_type)
    
    @classmethod
    def get_email_bcc(cls):
        return get_param_value(FPARAMS, '%s.BCC' % cls.statement_type)
    
    @classmethod
    def email_valid(cls, email):
        return re.match(cls.email_pattern, email)
    
    @classmethod
    def get_doc_title(cls):
        return cls.statement_type
    
    @classmethod
    def get_doc_date(cls, acm_date):    
        return format_date(acm_date, cls.doc_date_pattern)
    
    @classmethod
    def get_all_output_formats(cls):
        output_formats = []
        for output_params in list(cls.outputs.values()):
            output_formats.extend(output_params['formats'])
        return output_formats
    
    def _is_adhoc(self):
        ready_step = get_first_step(self._bp, 'Ready')
        params = ready_step.DiaryEntry().Parameters()
        adhoc = params.HasKey('user')
        LOGGER.info('%s: Adhoc "%s".' % (self._log_str, adhoc))
        return adhoc
    
    def _is_recalculated(self):
        calc_steps = get_steps(self._bp, 'Calculated')
        recalculated = len(calc_steps) > 1
        LOGGER.info('%s: Recalculated "%s".' % (self._log_str, recalculated))
        return recalculated
    
    def _is_stp(self):
        if self._is_adhoc() or self._is_recalculated():
            return get_param_value(FPARAMS, '%s.STP.Adhoc' % self.statement_type) == '1'
        return get_param_value(FPARAMS, '%s.STP' % self.statement_type) == '1'
    
    def _get_title(self, acm_date):
        doc_date = self.get_doc_date(acm_date)
        fullname = ' '.join(self._party.FullName().split())
        if not fullname:
            msg = 'Counterparty Full Name not specified.'
            self._error_msg = msg
            raise RuntimeError(msg)
        title = '%s %s %s' % (self.get_doc_title(), fullname, doc_date)
        return ''.join(char for char in title if char not in self.invalid_chars)
    
    def _get_valuation_date(self):
        val_date = self._bp.AdditionalInfo().BP_ValuationDate()
        if not val_date:
            msg = 'Valuation date not specified on BP %s.' % self._bp.Oid()
            self._error_msg = msg
            raise RuntimeError(msg)
        return val_date
    
    def _get_contact(self):
        contact = self._bp.AdditionalInfo().BP_ExternalId()
        if not contact:
            msg = 'Contact ID not specified on BP %s.' % self._bp.Oid()
            self._error_msg = msg
            raise RuntimeError(msg)
        return acm.FContact[int(contact)]
    
    def _force_bp_to_state(self, state, reason='', params=None, params_state=''):
        acm.BeginTransaction()
        try:
            self._bp.ForceToState(state, reason)
            self._bp.Commit()
            if params:
                current_step = self._bp.CurrentStep()
                if params_state:
                    current_step = get_last_step(self._bp, params_state)
                diary_entry = current_step.DiaryEntry()
                diary_entry.Parameters(params)
                diary = self._bp.Diary()
                diary.PutEntry(self._bp, current_step, diary_entry)
                diary.Commit()
            acm.CommitTransaction()
        except Exception as exc:
            acm.AbortTransaction()
            LOGGER.exception('%s: Failed to force %s to "%s".' 
                             % (self._log_str, self._bp.Oid(), state))
        else:
            LOGGER.info('%s: %s forced to "%s".' 
                        % (self._log_str, self._bp.Oid(), state))
    
    def _handle_event(self, event, params):
        try:
            self._bp.HandleEvent(event, params)
            self._bp.Commit()
        except Exception as exc:
            LOGGER.exception('%s: BP %s failed to handle "%s".' 
                             % (self._log_str, self._bp.Oid(), event))
        else:
            LOGGER.info('%s: BP %s handled event "%s".' 
                        % (self._log_str, self._bp.Oid(), event))
    
    def _get_contact_rule_acquirers(self):
        contact = self._get_contact()
        acquirers = [] 
        for rule in contact.ContactRules():
            if self._config.matches(rule):
                if not rule.Acquirer():
                    return []
                acquirers.append(rule.Acquirer())
        return acquirers
    
    def _select_additional_trades(self, val_date):
        return []
    
    def _extend_trade_query(self, query, val_date):
        acquirers = self._get_contact_rule_acquirers()
        if not acquirers: 
            return
        LOGGER.info('%s: Extending trade query, Acquirer: %s.' 
                    % (self._log_str, ' OR '.join([acq.Name() for acq in acquirers])))
        or_node = query.AddOpNode('OR')
        for acquirer in acquirers:
            or_node.AddAttrNode('Acquirer.Oid', 'EQUAL', acquirer.Oid())
    
    def _select_trades(self, val_date):
        query = acm.FStoredASQLQuery[self._config.trade_query].Query()
        query.AddAttrNode('TradeTime', 'LESS_EQUAL', val_date)
        query.AddAttrNode('Counterparty.Oid', 'EQUAL', self._party_id)
        self._extend_trade_query(query, val_date)
        self._trades = list(query.Select())
        additional_trades = self._select_additional_trades(val_date)
        self._trades.extend(additional_trades)
        self._trades.sort(key=lambda t: t.Oid(), reverse=True)
        LOGGER.info('%s: Selected %s trades.' 
                    % (self._log_str, len(self._trades)))
    
    def _calculate_values(self):
        contact = self._get_contact()
        val_date = self._get_valuation_date()
        generate_date = acm.Time.DateToday()
        acm.PollDbEvents()
        self._select_trades(val_date)
        if not self._trades:
            msg = 'No valid trades found.'
            self._error_msg = msg
            raise EmptyTradeSelection(msg)
        params = acm.FDictionary()
        params['generate_date'] = generate_date
        for xml_param, output_params in self.outputs.items():
            Calculator = output_params['calculator']
            XmlReport = output_params['xml_report']
            calc = Calculator(self._trades, val_date, self._bp)
            values = calc.calculate()
            report = XmlReport(self.statement_type, self._party, contact, values, 
                               generate_date, val_date)
            xml_string = report.create_report()
            params[xml_param] = xml_string
        return params
    
    def _generate_documents(self):
        calc_step = get_last_step(self._bp, 'Pending Calculation')
        calc_params = calc_step.DiaryEntry().Parameters()
        val_date = self._get_valuation_date()
        title = self._get_title(val_date)
        filename = '%s_%s' % (title, int(time.time()))
        output_dir = self.get_output_dir(val_date)
        self.create_dir(output_dir)
        params = acm.FDictionary()
        for xml_param, output_params in self.outputs.items():
            formats = output_params['formats']
            xml_string = calc_params[xml_param]
            if self.generate_pdf(formats):
                gen = XMLReport.XMLReportGenerator(output_dir, self.xslt_name)
                if self.landscape_pdf:
                    gen.set('Landscape', 'true') 
                pdf_path = gen.create(xml_string, filename)
                unix_chmod(pdf_path, PERMISSION_MODE)
                LOGGER.info('%s: PDF generated %s.' % (self._log_str, pdf_path))
                params['pdf_file'] = filename + '.pdf'
            if self.generate_xlsx(formats):
                xlsx_gen = self.xlsx_report_gen(output_dir)
                xlsx_path = xlsx_gen.create(xml_string, filename)
                unix_chmod(xlsx_path, PERMISSION_MODE)
                LOGGER.info('%s: XLSX generated %s.' % (self._log_str, xlsx_path))
                params['xlsx_file'] = filename + '.xlsx'
        return params
    
    def _get_email_body_undelivered(self, recipients):
        msg = '%s undelivered to %s.' % (self.get_doc_title(), 
                                         ', '.join(recipients))
        return EMAIL_UNDELIVERED % msg
    
    def _send_delivery_failure(self, result):
        val_date = self._get_valuation_date()
        title = self._get_title(val_date)
        recipients = list(result.keys())
        subject = 'RE: %s' % title
        email_body = self._get_email_body_undelivered(recipients)
        sender = self.get_email_sender()
        message = EmailHelper(email_body, subject, [sender],
                              sender, [],
                              sender_type=EmailHelper.SENDER_TYPE_SMTP,
                              host=EmailHelper.get_acm_host())
        try:
            message.send()
        except Exception as exc:
            LOGGER.exception('%s: Failed to send Delivery Failure message.' 
                             % self._log_str)
    
    def _get_email_body(self):
        val_date = self._get_valuation_date()
        email_date = self.get_doc_date(val_date)
        return self.email_template % (self.get_doc_title(), email_date)
    
    def _send_documents(self):
        val_date = self._get_valuation_date()
        contact = self._get_contact()
        recipients = self.get_emails(contact.Email())
        if not recipients:
            msg = 'Contact does not contain any emails.'
            raise RuntimeError(msg)
        invalid_recipients = [email for email in recipients 
                              if not self.email_valid(email)]
        if invalid_recipients:
            msg = ('Contact includes invalid emails: %s.' 
                   % ', '.join(invalid_recipients))
            self._error_msg = msg
            raise RuntimeError(msg)
        title = self._get_title(val_date)
        output_dir = self.get_output_dir(val_date)
        generated_step = get_last_step(self._bp, 'Generated')
        params = generated_step.DiaryEntry().Parameters()
        attachments = []
        output_formats = self.get_all_output_formats()
        for output_format in output_formats:    
            file_extension = output_format.lower()
            file_path = os.path.join(output_dir, title + '.' + file_extension)
            temp_file_path = os.path.join(output_dir, params['%s_file' % file_extension])
            shutil.copyfile(temp_file_path, file_path)
            attachments.append(file_path)
        email_body = self._get_email_body()
        sender = self.get_email_sender()
        cc = self.get_emails(self.get_email_cc())
        bcc = self.get_emails(self.get_email_bcc())
        message = EmailHelper(email_body, title, recipients,
                              sender, attachments,
                              sender_type=EmailHelper.SENDER_TYPE_SMTP,
                              host=EmailHelper.get_acm_host(),
                              mail_cc=cc, mail_bcc=bcc)
        result = message.send()
        return result
    
    def _process_pending_calculation(self):
        LOGGER.info('%s: Processing state "Pending Calculation".' 
                    % self._log_str)
        try:
            params = self._calculate_values()
        except EmptyTradeSelection as exc:
            LOGGER.info('%s: No valid trades found.' % self._log_str)
            error_msg = self._error_msg if self._error_msg else str(exc)
            self._error_msg = ''
            self._force_bp_to_state('Complete', error_msg)
            return
        except Exception as exc:
            LOGGER.exception('%s: Failed to calculate values.' 
                             % self._log_str)
            error_msg = self._error_msg if self._error_msg else str(exc)
            self._error_msg = ''
            self._force_bp_to_state('Calculate Failed', error_msg)
            return
        LOGGER.info('%s: Values calculated successfully.' 
                    % self._log_str)
        self._force_bp_to_state('Calculated', params=params, 
                                params_state='Pending Calculation')
    
    def _process_pending_generation(self):
        LOGGER.info('%s: Processing state "Pending Generation".' 
                    % self._log_str)
        try:
            params = self._generate_documents()
        except Exception as exc:
            LOGGER.exception('%s: Failed to generate documents.' 
                             % self._log_str)
            error_msg = self._error_msg if self._error_msg else str(exc)
            self._error_msg = ''
            self._force_bp_to_state('Generate Failed', error_msg)
            return
        LOGGER.info('%s: Documents generated successfully.' % self._log_str)
        self._handle_event('Generate Success', params)
    
    def _process_generated(self):
        LOGGER.info('%s: Processing state "Generated".' % self._log_str)
        if self._is_stp():
            self._force_bp_to_state('Pending Send')
        else:
            self._force_bp_to_state('Hold')
    
    def _process_hold(self):
        LOGGER.info('%s: Processing state "Hold".' % self._log_str)
        if (self._is_stp() 
                and acm.Time.DateFromTime(self._bp.UpdateTime()) == acm.Time.DateToday()):
            self._force_bp_to_state('Pending Send')
    
    def _process_pending_send(self):
        LOGGER.info('%s: Processing state "Pending Send".' % self._log_str)
        result = None
        try:
            result = self._send_documents()
        except smtplib.SMTPRecipientsRefused as exc:
            result = exc.recipients
            error_msg = 'Failed to send documents, all recipients were refused.'
            LOGGER.exception('%s: %s' % (self._log_str, error_msg))
            self._force_bp_to_state('Complete', error_msg)
        except Exception as exc:
            LOGGER.exception('%s: Failed to send documents.' % self._log_str)
            error_msg = self._error_msg if self._error_msg else str(exc)
            self._error_msg = ''
            self._force_bp_to_state('Send Failed', error_msg)
        else:
            LOGGER.info('%s: Documents sent successfully.' % self._log_str)
            self._force_bp_to_state('Sent')
        if result:
            self._send_delivery_failure(result)
    
    def _process_sent(self):
        LOGGER.info('%s: Processing state "Sent".' % self._log_str)
        self._force_bp_to_state('Complete')
    
    def _process_calculated(self):
        LOGGER.info('%s: Processing state "Calculated".' % self._log_str)
        self._force_bp_to_state('Pending Generation')
    
    def _process_generate_failed(self):
        LOGGER.info('%s: Processing state "Generate Failed".' 
                    % self._log_str)
        steps = get_steps(self._bp, 'Generate Failed')
        if len(steps) < self.generate_retries:
            LOGGER.info('%s: Retrying to generate documents.' 
                        % self._log_str)
            self._force_bp_to_state('Pending Generation')
            return
        LOGGER.info('%s: Reached maximum number of generate retries.' 
                    % self._log_str)
    
    def process_states(self):
        current_state = self._bp.CurrentStep().State().Name()
        if current_state == 'Pending Calculation':
            self._process_pending_calculation()
        elif current_state == 'Calculated':
            self._process_calculated()
        elif current_state == 'Pending Generation':
            self._process_pending_generation()
        elif current_state == 'Generated':
            self._process_generated()
        elif current_state == 'Hold':
            self._process_hold()
        elif current_state == 'Pending Send':
            self._process_pending_send()
        elif current_state == 'Sent':
            self._process_sent()
        elif current_state == 'Generate Failed':
            self._process_generate_failed()


class ValuationStatementProcess(StatementProcess):
    
    email_template = EMAIL_CLIENT_VALUATIONS
    
    @classmethod
    def get_doc_title(cls):
        return '%s Valuation Statement' % cls.statement_type


class FECStatementProcess(ValuationStatementProcess):
    
    statement_type = 'FEC'
    xslt_name = XSLT_NAME_WIDE
    outputs = {
        'xml_string': {
            'calculator': FECCalcEngine,
            'xml_report': ValuationsReport,
            'formats': ['PDF', 'XLSX'], 
        },
    }
    
    def _exclude_cash_payments(self):
        trades = []
        for trade in self._trades:
            if not trade.CurrencyPair():
                LOGGER.info('%s: Excluding cash payment %s.' 
                            % (self._log_str, trade.Oid()))
                continue
            trades.append(trade)
        self._trades = trades
    
    def _run_midas_query(self, val_date, midas_nbr):
        query = acm.FStoredASQLQuery[self._config.additional_trade_query].Query()
        query.AddAttrNode('ValueDay', 'GREATER', val_date)
        query.AddAttrNode('TradeTime', 'LESS_EQUAL', val_date)
        if not acm.ArchivedMode():
            query.AddAttrNode('AdditionalInfo.Source_Ctpy_Id', 'EQUAL', midas_nbr)
            query.AddAttrNode('AdditionalInfo.Source_Trade_Type', 'NOT_EQUAL', 'SH')
        return list(query.Select())
    
    def _select_additional_trades(self, val_date):
        if not self._config.additional_trade_query:
            return []
        acquirers = self._get_contact_rule_acquirers()
        midas_dual_key = acm.FParty['MIDAS DUAL KEY']
        if acquirers and not midas_dual_key in acquirers:
            LOGGER.info('%s: Midas selection skipped. %s not selected' 
                        % (self._log_str, midas_dual_key.Name()))
            return []
        sdsid = self._party.AdditionalInfo().BarCap_Eagle_SDSID()
        midas_nbr = ''
        try:
            midas_nbr = get_param_value('MidasMapping', sdsid)
            LOGGER.info('%s: Midas number %s.' % (self._log_str, midas_nbr))
        except Exception:
            LOGGER.exception('%s: Failed to select Midas number.' 
                             % self._log_str)
        if not midas_nbr:
            return []
        trades = self._run_midas_query(val_date, midas_nbr)
        midas_trades = []
        if not acm.ArchivedMode():
            midas_trades = trades
        else:
            for trade in trades:
                add_info = trade.AdditionalInfo()
                if (add_info.Source_Ctpy_Id() == midas_nbr 
                        and not add_info.Source_Trade_Type() == 'SH'):
                    midas_trades.append(trade)
        LOGGER.info('%s: Selected %s Midas trades.' 
                     % (self._log_str, len(midas_trades)))
        return midas_trades
    
    def _extend_trade_query(self, query, val_date):
        super(FECStatementProcess, self)._extend_trade_query(query, val_date)
        query.AddAttrNode('ValueDay', 'GREATER', val_date)
    
    def _select_trades(self, val_date):
        super(FECStatementProcess, self)._select_trades(val_date)
        self._exclude_cash_payments()


class OptionStatementProcess(ValuationStatementProcess):
    
    statement_type = 'Option'
    outputs = {
        'xml_string': {
            'calculator': OptionCalcEngine,
            'xml_report': ValuationsReport,
            'formats': ['PDF', 'XLSX'], 
        },
    }
    
    def _extend_trade_query(self, query, val_date):
        super(OptionStatementProcess, self)._extend_trade_query(query, val_date)
        or_node = query.AddOpNode('OR')
        or_node.AddAttrNode('ValueDay', 'GREATER', val_date)
        or_node.AddAttrNode('Instrument.ExpiryDate', 'GREATER', val_date)


class SwapStatementProcess(ValuationStatementProcess):
    
    statement_type = 'Swap'
    outputs = {
        'xml_string': {
            'calculator': SwapCalcEngine,
            'xml_report': ValuationsReport,
            'formats': ['PDF', 'XLSX'], 
        },
    }
    
    def _extend_trade_query(self, query, val_date):
        super(SwapStatementProcess, self)._extend_trade_query(query, val_date)
        or_node = query.AddOpNode('OR')
        or_node.AddAttrNode('ValueDay', 'GREATER', val_date)
        or_node.AddAttrNode('Instrument.ExpiryDate', 'GREATER', val_date)


class CapFloorStatementProcess(ValuationStatementProcess):
    
    statement_type = 'Cap & Floor'
    outputs = {
        'xml_string': {
            'calculator': ValuationsDefaultCalcEngine,
            'xml_report': ValuationsReport,
            'formats': ['PDF', 'XLSX'], 
        },
    }
    
    def _extend_trade_query(self, query, val_date):
        super(CapFloorStatementProcess, self)._extend_trade_query(query, val_date)
        query.AddAttrNode('Instrument.ExpiryDate', 'GREATER', val_date)


class StructuredStatementProcess(ValuationStatementProcess):
    
    statement_type = 'Structured Deal'
    outputs = {
        'xml_string': {
            'calculator': StructuredCalcEngine,
            'xml_report': ValuationsReport,
            'formats': ['PDF', 'XLSX'], 
        },
    }
    
    def _extend_trade_query(self, query, val_date):
        super(StructuredStatementProcess, self)._extend_trade_query(query, val_date)
        query.AddAttrNode('Instrument.ExpiryDate', 'GREATER', val_date)


class DepositStatementProcess(ValuationStatementProcess):
    
    statement_type = 'Deposit'
    xslt_name = XSLT_NAME_WIDE
    outputs = {
        'xml_string': {
            'calculator': DepositCalcEngine,
            'xml_report': ValuationsReport,
            'formats': ['PDF', 'XLSX'], 
        },
    }
    
    def _extend_trade_query(self, query, val_date):
        super(DepositStatementProcess, self)._extend_trade_query(query, val_date)
        query.AddAttrNode('Instrument.ExpiryDate', 'GREATER', val_date)


class SBLStatementProcess(StatementProcess):
    
    landscape_pdf = False
    xslt_name = XSLT_NAME_SBL
    email_template = EMAIL_CLIENT_SBL
    
    @staticmethod
    def is_valid(bp):
        val_date = bp.AdditionalInfo().BP_ValuationDate()
        if not val_date:
            return False
        if ((acm.ArchivedMode() and val_date >= ARCHIVED_CUTOFF_SBL)
                or (not acm.ArchivedMode() and val_date < ARCHIVED_CUTOFF_SBL)):
            return False
        return True
    
    @staticmethod
    def is_loan_settled(trade):
        settlements = acm.FSettlement.Select('trade=%s and type in ("Security Nominal", "End Security")'
                                             % trade.Oid())
        if not settlements:
            LOGGER.info('Trade %s does not have any "Security" settlements.' % trade.Oid())
            return False
        if any([settlement.Status() == 'Settled' for settlement in settlements]):
            return True
        LOGGER.info('"Security" settlement of trade %s not settled.' % trade.Oid())
        return False
    
    @staticmethod
    def is_coll_settled(trade):
        if trade.Instrument().InsType() == 'Deposit':
            return True
        settlements = acm.FSettlement.Select('trade=%s' % trade.Oid())
        if not settlements:
            LOGGER.info('Trade %s does not have any settlements.' % trade.Oid())
            return False
        if any([settlement.Status() == 'Settled' for settlement in settlements]):
            return True
        LOGGER.info('Trade %s does not have any settled settlements.' % trade.Oid())
        return False
    
    def _get_email_body(self):
        val_date = self._get_valuation_date()
        email_date = self.get_doc_date(val_date)
        msg = '%s as at %s' % (self.get_doc_title(), email_date)
        return self.email_template % msg
    
    def _get_title(self, acm_date):
        doc_date = self.get_doc_date(acm_date)
        fullname = ' '.join(self._party.FullName().split())
        if not fullname:
            msg = 'Counterparty Full Name not specified.'
            self._error_msg = msg
            raise RuntimeError(msg)
        lb_code = self._party.AdditionalInfo().SL_CptyType()
        if not lb_code:
            msg = 'Counterparty SL_CptyType add info not specified.'
            self._error_msg = msg
            raise RuntimeError(msg)
        title = ' '.join([self.get_doc_title(), fullname, lb_code.upper(), doc_date])
        return ''.join(char for char in title if char not in self.invalid_chars)
    
    def _extend_trade_query(self, query, val_date):
        query.AddAttrNode('Instrument.StartDate', 'LESS_EQUAL', val_date)
        query.AddAttrNode('ValueDay', 'LESS_EQUAL', val_date)
        or_node = query.AddOpNode('OR')
        sub_and_node = or_node.AddOpNode('AND')
        or_node.AddAttrNode('Instrument.ExpiryDate', 'GREATER', val_date)
        sub_and_node.AddAttrNode('Instrument.ExpiryDate', 'EQUAL', val_date)
        sub_and_node.AddAttrNode('Instrument.OpenEnd', 'NOT_EQUAL', 'Terminated')
    
    def _select_trades(self, val_date):
        lb_code = self._party.AdditionalInfo().SL_CptyType()
        if not lb_code in ('Borrower', 'Lender'):
            msg = 'Counterparty SL_CptyType add info has to be either Borrower or Lender.'
            self._error_msg = msg
            raise RuntimeError(msg)
        query = acm.FStoredASQLQuery[self._config.trade_query].Query()
        query.AddAttrNode('TradeTime', 'LESS_EQUAL', val_date)
        self._extend_trade_query(query, val_date)
        party_name = self._party.Name()
        if not acm.ArchivedMode():
            if lb_code == 'Borrower':
                query.AddAttrNode('AdditionalInfo.SL_G1Counterparty1', 'EQUAL', party_name)
            else:
                query.AddAttrNode('AdditionalInfo.SL_G1Counterparty2', 'EQUAL', party_name)
            self._trades = list(query.Select())
        else:
            self._trades = []
            if lb_code == 'Borrower':
                ai_spec = acm.FAdditionalInfoSpec['SL_G1Counterparty1']
            else:
                ai_spec = acm.FAdditionalInfoSpec['SL_G1Counterparty2']
            add_infos = acm.FAdditionalInfo.Select("addInf=%s and fieldValue='%s'" 
                                                   % (ai_spec.Oid(), party_name))
            if add_infos:
                or_node = query.AddOpNode('OR')
                for add_info in add_infos:
                    or_node.AddAttrNode('Oid', 'EQUAL', add_info.Recaddr())
                self._trades = list(query.Select())
        additional_trades = self._select_additional_trades(val_date)
        self._trades.extend(additional_trades)
        self._trades.sort(key=lambda t: t.Oid(), reverse=True)
        LOGGER.info('%s: Selected %s trades.' 
                    % (self._log_str, len(self._trades)))


class SBLFeeStatementProcess(SBLStatementProcess):
    
    statement_type = 'SBL Fee'
    doc_date_pattern = DATE_PATTERN_MONTH
    xlsx_report_gen = SBLFeeXLSXGenerator
    outputs = {
        'xml_string': {
            'calculator': SBLFeeCalcEngine,
            'xml_report': SBLFeeReport,
            'formats': ['PDF', 'XLSX'], 
        },
    }
    
    @staticmethod
    def is_valid(bp):
        val_date = bp.AdditionalInfo().BP_ValuationDate()
        if not val_date:
            return False
        fom_date = first_day_of_month(val_date)
        start_date = acm.Time.DateAddDelta(fom_date, 0, 0, -1)
        if ((acm.ArchivedMode() and start_date >= ARCHIVED_CUTOFF_SBL)
                or (not acm.ArchivedMode() and start_date < ARCHIVED_CUTOFF_SBL)):
            return False
        return True
    
    @classmethod
    def get_doc_title(cls):
        return 'Fee Statement'
    
    def _get_email_body(self):
        val_date = self._get_valuation_date()
        email_date = self.get_doc_date(val_date)
        msg = '%s for %s' % (self.get_doc_title(), email_date)
        return self.email_template % msg
    
    def _extend_trade_query(self, query, val_date):
        fom_date = first_day_of_month(val_date)
        lom_date = last_day_of_month(val_date)
        start_date = acm.Time.DateAddDelta(fom_date, 0, 0, -1)
        end_date = acm.Time.DateAddDelta(lom_date, 0, 0, 1)
        or_node = query.AddOpNode('OR')
        sub_and_node_1 = or_node.AddOpNode('AND')
        sub_and_node_2 = or_node.AddOpNode('AND')
        sub_and_node_3 = or_node.AddOpNode('AND')

        sub_and_node_1.AddAttrNode('Instrument.ExpiryDate', 'GREATER', start_date)
        sub_and_node_1.AddAttrNode('Instrument.ExpiryDate', 'LESS', end_date)

        sub_and_node_2.AddAttrNode('ValueDay', 'GREATER', start_date)
        sub_and_node_2.AddAttrNode('ValueDay', 'LESS', end_date)
        
        sub_and_node_3.AddAttrNode('Instrument.ExpiryDate', 'GREATER_EQUAL', end_date)
        sub_and_node_3.AddAttrNode('ValueDay', 'LESS_EQUAL', start_date)


class SBLFinderFeeStatementProcess(SBLFeeStatementProcess):
    
    statement_type = 'SBL Finder Fee'
    outputs = {
        'xml_string': {
            'calculator': SBLFinderFeeCalcEngine,
            'xml_report': SBLFinderFeeReport,
            'formats': ['PDF', 'XLSX'], 
        },
    }
    
    @classmethod
    def get_doc_title(cls):
        return 'Finder Fee Statement'
    
    def _get_title(self, acm_date):
        doc_date = self.get_doc_date(acm_date)
        fullname = ' '.join(self._party.FullName().split())
        if not fullname:
            msg = 'Counterparty Full Name not specified.'
            self._error_msg = msg
            raise RuntimeError(msg)
        title = ' '.join([self.get_doc_title(), fullname, doc_date])
        return ''.join(char for char in title if char not in self.invalid_chars)
    
    def _get_mapped_party_name(self):
        try:
            return SBL_FINDER_MAPPING[self._party]
        except KeyError:
            msg = 'Finder mapping not found for the counterparty.'
            self._error_msg = msg
            raise RuntimeError(msg)
    
    def _select_trades(self, val_date):
        query = acm.FStoredASQLQuery[self._config.trade_query].Query()
        query.AddAttrNode('TradeTime', 'LESS_EQUAL', val_date)
        self._extend_trade_query(query, val_date)
        party_name = self._get_mapped_party_name()
        self._trades = []
        ai_spec = acm.FAdditionalInfoSpec['SL_G1FinderCode']
        add_infos = acm.FAdditionalInfo.Select("addInf=%s and fieldValue='%s'" 
                                               % (ai_spec.Oid(), party_name))
        if add_infos:
            or_node = query.AddOpNode('OR')
            for add_info in add_infos:
                or_node.AddAttrNode('Oid', 'EQUAL', add_info.Recaddr())
            self._trades = list(query.Select())
        additional_trades = self._select_additional_trades(val_date)
        self._trades.extend(additional_trades)
        self._trades.sort(key=lambda t: t.Oid(), reverse=True)
        LOGGER.info('%s: Selected %s trades.' 
                    % (self._log_str, len(self._trades)))


class SBLMovementStatementProcess(SBLStatementProcess):
    
    email_template = EMAIL_CLIENT_SBL_COLL
    statement_type = 'SBL Movement'
    xlsx_report_gen = SBLMovementXLSXGenerator
    outputs = {
        'xml_string': {
            'calculator': SBLMovementCalcEngine,
            'xml_report': SBLMovementReport,
            'formats': ['PDF', 'XLSX'], 
        },
    }
    
    @staticmethod
    def is_valid(bp):
        val_date = bp.AdditionalInfo().BP_ValuationDate()
        if not val_date:
            return False
        start_date = bp.AdditionalInfo().BP_FromDate()
        if not start_date:
            return False
        if ((acm.ArchivedMode() and start_date >= ARCHIVED_CUTOFF_SBL)
                or (not acm.ArchivedMode() and start_date < ARCHIVED_CUTOFF_SBL)):
            return False
        return True
    
    @classmethod
    def get_doc_title(cls):
        return 'Movement Report'
    
    def _get_start_date(self):
        return self._bp.AdditionalInfo().BP_FromDate()
    
    def _get_end_date(self):
        return self._bp.AdditionalInfo().BP_ToDate()
    
    def _get_email_body(self):
        start_date = self._get_start_date()
        start_date = self.get_doc_date(start_date)
        end_date = self._get_end_date()
        end_date = self.get_doc_date(end_date)
        msg = '%s from %s to %s' % (self.get_doc_title(), start_date, end_date)
        return self.email_template % msg
    
    def _get_title(self, acm_date):
        start_date = self._get_start_date()
        start_date = self.get_doc_date(start_date)
        end_date = self.get_doc_date(acm_date)
        fullname = ' '.join(self._party.FullName().split())
        if not fullname:
            msg = 'Counterparty Full Name not specified.'
            self._error_msg = msg
            raise RuntimeError(msg)
        lb_code = self._party.AdditionalInfo().SL_CptyType()
        if not lb_code:
            msg = 'Counterparty SL_CptyType add info not specified.'
            self._error_msg = msg
            raise RuntimeError(msg)
        title = ' '.join([self.get_doc_title(), fullname, lb_code.upper(), 
                          start_date, end_date])
        return ''.join(char for char in title if char not in self.invalid_chars)
    
    def _extend_trade_query(self, query, val_date):
        start_date = self._get_start_date()
        query.AddAttrNode('ValueDay', 'GREATER_EQUAL', start_date)
        end_date = self._get_end_date()
        query.AddAttrNode('ValueDay', 'LESS_EQUAL', end_date)
    
    def _select_additional_trades(self, _val_date):
        start_date = self._get_start_date()
        end_date = self._get_end_date()
        query = acm.FStoredASQLQuery[self._config.additional_trade_query].Query()
        query.AddAttrNode('TradeTime', 'LESS_EQUAL', end_date)
        query.AddAttrNode('ValueDay', 'LESS_EQUAL', end_date)
        query.AddAttrNode('Counterparty.Oid', 'EQUAL', self._party_id)
        or_node = query.AddOpNode('OR')
        sub_and_node_1 = or_node.AddOpNode('AND')
        sub_and_node_2 = or_node.AddOpNode('AND')
        sub_and_node_1.AddAttrNode('Instrument.InsType', 'EQUAL', 'Deposit')
        sub_and_node_2.AddAttrNode('Instrument.InsType', 'NOT_EQUAL', 'Deposit')
        sub_and_node_2.AddAttrNode('ValueDay', 'GREATER_EQUAL', start_date)
        return list(query.Select())
    
    def _select_trades(self, val_date):
        super(SBLMovementStatementProcess, self)._select_trades(val_date)
        LOGGER.info('%s: Filtering selected trades.' % self._log_str)
        filtered_trades = []
        for trade in self._trades:
            if trade.Instrument().InsType() == 'SecurityLoan':
                if not self.is_loan_settled(trade):
                    LOGGER.info('%s: Excluding unsettled loan %s.' 
                                % (self._log_str, trade.Oid()))
                    continue
            else:
                if not self.is_coll_settled(trade):
                    LOGGER.info('%s: Excluding unsettled collateral %s.' 
                                % (self._log_str, trade.Oid()))
                    continue
            filtered_trades.append(trade)
        self._trades = filtered_trades


class SBLMarginCallStatementProcess(SBLStatementProcess):
    
    statement_type = 'SBL Margin Call'
    xlsx_report_gen = SBLSummaryPosXLSXGenerator
    email_template = EMAIL_CLIENT_SBL_COLL
    outputs = {
        'xml_string_pdf': {
            'calculator': SBLMarginCallCalcEngine,
            'xml_report': SBLMarginCallReport,
            'formats': ['PDF'], 
        },
        'xml_string_xlsx': {
            'calculator': SBLSummaryOpenPosCalcEngine,
            'xml_report': SBLSummaryOpenPosReport,
            'formats': ['XLSX'], 
        },
    }
    balance_threshold = 0.1
    
    @staticmethod
    def get_last_trade(trade):
        contract = trade.Contract().Oid()
        trades = [t for t in acm.FTrade.Select('contract=%s' % contract) 
                  if t.Status() in VALID_SBL_STATUS]
        trades.sort(key = lambda t: (t.Instrument().StartDate(), t.Oid()))
        if trades:
            if not trade in trades:
                return trades[-1]
            index = trades.index(trade)
            try:
                return trades[index+1]
            except IndexError:
                return trades[-1]
        return None
    
    @staticmethod
    def get_party_groups(party):
        group = acm.FPartyGroup[party.Name()]
        if not group:
            return [party]
        parties = [link.Party() for link in group.Parties()]
        if party in parties:
            return parties
        return [party]
    
    @staticmethod
    def deposit_trades_only(trades):
        for trade in trades:
            if trade.Instrument().InsType() != 'Deposit':
                return False
        return True
    
    @classmethod
    def get_doc_title(cls):
        return 'Margin Call'
    
    def _extend_trade_query(self, query, val_date):
        query.AddAttrNode('Instrument.Legs.EndDate', 'GREATER_EQUAL', val_date)
        query.AddAttrNode('Instrument.Legs.StartDate', 'LESS_EQUAL', val_date)
        query.AddAttrNode('ValueDay', 'LESS_EQUAL', val_date)
    
    def _select_additional_trades(self, val_date):
        query = acm.FStoredASQLQuery[self._config.additional_trade_query].Query()
        query.AddAttrNode('TradeTime', 'LESS_EQUAL', val_date)
        parties = self.get_party_groups(self._party)
        if len(parties) > 1:
            LOGGER.info('%s: Using additional counterparties %s.' 
                        % (self._log_str, ', '.join([party.Name() for party in parties])))
            or_node = query.AddOpNode('OR')
            for party in parties:
                or_node.AddAttrNode('Counterparty.Oid', 'EQUAL', party.Oid())
        else:
            query.AddAttrNode('Counterparty.Oid', 'EQUAL', self._party_id)
        return list(query.Select())
    
    def _select_trades(self, val_date):
        super(SBLMarginCallStatementProcess, self)._select_trades(val_date)
        LOGGER.info('%s: Filtering selected trades.' % self._log_str)
        filtered_trades = []
        for trade in self._trades:
            if trade.Instrument().InsType() == 'SecurityLoan':
                settled = self.is_loan_settled(trade)
                if not settled:
                    LOGGER.info('%s: Excluding unsettled loan %s.' 
                                % (self._log_str, trade.Oid()))
                    continue
                if trade.Instrument().OpenEnd() != 'Terminated':
                    filtered_trades.append(trade)
                    continue
                if trade.Instrument().ExpiryDateOnly() > val_date:
                    filtered_trades.append(trade)
                    continue
                last_trade = self.get_last_trade(trade)
                if (last_trade and trade != last_trade 
                        and not self.is_loan_settled(last_trade)):
                    filtered_trades.append(trade)
                    continue
                LOGGER.info('%s: Excluding terminated loan %s.' 
                            % (self._log_str, trade.Oid()))
            else:
                settled = self.is_coll_settled(trade)
                if trade.Text1() in ('PARTIAL_RETURN', 'FULL_RETURN'):
                    if not settled:
                        LOGGER.info('%s: Including unsettled collateral return %s.' 
                                    % (self._log_str, trade.Oid()))
                        filtered_trades.append(trade)
                    continue
                if settled:
                    filtered_trades.append(trade)
                    continue
                LOGGER.info('%s: Excluding unsettled collateral %s.' 
                            % (self._log_str, trade.Oid()))
        if filtered_trades and self.deposit_trades_only(filtered_trades):
            LOGGER.info('%s: Only deposit trades found: %s.' 
                        % (self._log_str, 
                           ', '.join([str(trade.Oid()) for trade in filtered_trades])))
            balance = 0.0
            for trade in filtered_trades:
                try:
                    balance += abs(float(calc_trade_value(trade, val_date, 'Deposit balance')))
                except:
                    LOGGER.exception('%s: Failed to calculate Deposit balance for trade %s.'
                                     % (self._log_str, trade.Oid()))
            if balance < self.balance_threshold:
                LOGGER.info('%s: Filtering out deposit trades, total balance less than %s.'
                            % (self._log_str, self.balance_threshold))
                self._trades = []
                return
        self._trades = filtered_trades


class SBLOpenPosCollStatementProcess(SBLMarginCallStatementProcess):
    
    statement_type = 'SBL Open Position Coll'
    email_template = EMAIL_CLIENT_SBL_COLL
    xlsx_report_gen = SBLOpenPosXLSXGenerator
    outputs = {
        'xml_string': {
            'calculator': SBLOpenPosCalcEngine,
            'xml_report': SBLOpenPosCollReport,
            'formats': ['PDF', 'XLSX'],
        },
    }
    
    @classmethod
    def get_doc_title(cls):
        return 'Open Position Report'


class SBLOpenPosOpsStatementProcess(SBLOpenPosCollStatementProcess):
    
    statement_type = 'SBL Open Position Ops'
    email_template = EMAIL_CLIENT_SBL
    outputs = {
        'xml_string': {
            'calculator': SBLOpenPosCalcEngine,
            'xml_report': SBLOpenPosOpsReport,
            'formats': ['PDF', 'XLSX'], 
        },
    }


class SBLDividendNotificationProcess(SBLStatementProcess):

    statement_type = 'SBL Dividend Notification'
    xlsx_report_gen = SBLSummaryPosXLSXGenerator
    email_template = EMAIL_CLIENT_SBL_COLL
    outputs = {
        'xml_string_pdf': {
            'calculator': SBLDividendNotificationCalcEngine,
            'xml_report': SBLDividendNotificationReport,
            'formats': ['PDF'], 
        },
    }

    @classmethod
    def get_doc_title(cls):

        return 'SBL Dividend Notification Statement'

    def _select_additional_trades(self, val_date):

        corp_actions = CorporateActionsExtract.get_corporate_actions(val_date)

        ca_extract = CorporateActionsExtract()
        return ca_extract.get_trades(corp_actions, val_date)

    def _select_trades(self, val_date):

        trades = []

        ca_extract = CorporateActionsExtract()
        self._trades = self._select_additional_trades(val_date)

        for trade in self._trades:
            if ProcessTrade.true_counterparty(trade) and ProcessTrade.true_counterparty(trade).Name() == self._party.Name():
                trades.append(trade)

            if (CorporateActionsExtract._is_sec_loan(trade) and ProcessTrade.true_counterparty(trade, "party2") and
                ProcessTrade.true_counterparty(trade, "party2").Name() == self._party.Name()):
                trades.append(trade)
        self._trades = trades

