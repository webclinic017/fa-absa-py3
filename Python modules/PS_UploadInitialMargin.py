"""-----------------------------------------------------------------------
MODULE
    PS_UploadInitialMargin

DESCRIPTION
    Date                : 2011-07-01
    Purpose             : Upload the initial margins values from SAFEX into a Call Account.
    Department and Desk : Prime Services
    Requester           : Francois Henrion
    Developer           : Herman Hoon
    CR Number           : 699989

HISTORY
================================================================================
Date       Change no    Developer          Description
--------------------------------------------------------------------------------
2011-07-01 699989       Herman Hoon        Initial Implementation
2014-11-20 2450799      Libor Svoboda      Updated logging end error checking.
2016-10-18 4035664      Libor Svoboda      Email report and refactoring.
2020-01-09 FAPE-181     Iryna Shcherbina   Use default sender email address.
-----------------------------------------------------------------------"""
import acm
import csv
import os

import FBDPGui
import FBDPString
import FCallDepositFunctions
import FRunScriptGUI
from PS_CallAccountSweeperFunctions import IsCurrentInterestPeriod
from PS_FundingSweeper import TradingManagerSweeper
from at_logging import getLogger, bp_start
from at_ael_variables import AelVariableHandler
from at_email import EmailHelper


LOGGER = getLogger()

logme = FBDPString.logme

CALENDAR = acm.FCalendar['ZAR Johannesburg']
TODAY = acm.Time.DateToday()
FILE_NAME = 'IMR_'
SCRIPT_NAME = 'PS_UploadInitialMargin'
FAIL_INFO = 'no initial margins will be uploaded'


def get_start_day_config():
    """Generate date options to be used as drop downs in the GUI."""
    return {
        'Inception': acm.Time.DateFromYMD(1970, 1, 1),
        'First Of Year': acm.Time.FirstDayOfYear(TODAY),
        'First Of Month': acm.Time.FirstDayOfMonth(TODAY),
        'PrevBusDay': CALENDAR.AdjustBankingDays(TODAY, -1),
        'TwoBusinessDaysAgo': CALENDAR.AdjustBankingDays(TODAY, -2),
        'TwoDaysAgo': acm.Time.DateAddDelta(TODAY, 0, 0, -2),
        'Yesterday': acm.Time.DateAddDelta(TODAY, 0, 0, -1),
        'Custom Date': TODAY,
        'Now': TODAY,
    }


def enable_custom_start_date(ael_var):
    for var in ael_variables:
        if var[0] == 'dateCustom':
            var.enabled = ael_var.value == 'Custom Date'


def enable_mail_list(ael_var):
    for var in ael_variables:
        if var[0] == 'mail_list':
            var.enabled = ael_var.value


def get_ael_variables():
    directory_selection = FRunScriptGUI.DirectorySelection()
    directory_selection.SelectedDirectory(
            'F:\\Book of Work\\2 Analysis\Futures Upload\\Test')
    variables = AelVariableHandler()
    variables.add('date',
        label='Date',
        collection=sorted(get_start_day_config().keys()),
        default='Now',
        alt='Date for witch the file should be selected.',
        hook=enable_custom_start_date
    )
    variables.add('dateCustom',
        label='Date Custom',
        default=TODAY,
        mandatory=False,
        alt='Custom date',
        enabled=False
    )
    variables.add('tradeFilter',
        label='Trade Filter',
        alt='The Trade Filter that returns trades for the SAFEX Call Accounts.',
        cls='FTradeSelection',
        default= acm.FTradeSelection['PB_SAFEX_CallAccounts']
    )
    variables.add('fileName',
        label='File name',
        default=FILE_NAME,
        alt='File name prefix. Will be followed by the specified date.'
    )
    variables.add('filePath',
        label='Directory',
        cls=directory_selection,
        default=directory_selection,
        multiple=True,
        alt='Directory where files will be uploaded from. \n'
            'A date subfolder in the form yyyy-mm-dd will '
            'be automatically added.'
    )
    variables.add_bool('send_report',
        label='Send Report',
        default=False,
        hook=enable_mail_list
    )
    variables.add('mail_list',
        label='Emails',
        default='PrimeServicesPCG@barclayscapital.com',
        multiple=True,
        mandatory=False,
        enabled=False
    )
    variables.extend(FBDPGui.LogVariables())
    return variables


ael_variables = get_ael_variables()


class EmailReport(object):

    header = '''<!DOCTYPE html>
        <html>
        <head>
        <style>
        body {
            font-family: Verdana, Arial, Helvetica, sans-serif;
        }
        h1 {
            font-size: 20;
        }
        table {
            width:100%%;
            font-size: 11;
        }
        table, th, td {
            border: 1px solid black;
            border-collapse: collapse;
        }
        th, td {
            padding: 5px;
            text-align: left;
        }
        th {
            background-color: black;
            color: white;
        }
        #error {
            background-color: red;
        }
        #warning {
            background-color: orange;
        }
        </style>
        </head>
        <body>
        <h1>%(heading)s</h1>
        <table>
          <tr>
            <th></th>
            <th>Client Code</th>
            <th>Portfolio</th>
            <th>Trade</th>
            <th>Status</th>
            <th>Reason</th>
          </tr>
    '''
    footer = '''</table>
        </body>
        </html>
    '''
    cells = '''<td>%(index)s</td>
        <td>%(code)s</td>
        <td>%(portfolio)s</td>
        <td>%(trade)s</td>
        <td>%(status)s</td>
        <td>%(reason)s</td>
    '''
    error_row = '''<tr id="error">
            %s
        </tr>
    ''' % cells
    warning_row = '''<tr id="warning">
            %s
        </tr>
    ''' % cells
    normal_row = '''<tr>
            %s
        </tr>
    ''' % cells

    def __init__(self, content, recipients):
        self._content = content
        self._recipients = recipients
        env = acm.FDhDatabase['ADM'].InstanceName()
        self._subject = '%s report' % SCRIPT_NAME
        self._heading = '%s, %s, %s' % (SCRIPT_NAME, env, TODAY)
        self._message = ''

    def create_report(self):
        self._message += self.header % {'heading': self._heading}
        for index, entry in enumerate(self._content, start=1):
            entry['index'] = index
            if entry['status'] == 'Error':
                row = self.error_row % entry
            elif entry['status'] == 'Warning':
                row = self.warning_row % entry
            else:
                row = self.normal_row % entry
            self._message += row
        self._message += self.footer

    def send_report(self):
        email = EmailHelper(self._message, self._subject, self._recipients)
        if str(acm.Class()) == 'FACMServer':
            email.sender_type = EmailHelper.SENDER_TYPE_SMTP
            email.host = EmailHelper.get_acm_host()
        try:
            email.send()
        except Exception as exc:
            LOGGER.exception('Error while sending report: %s' % str(exc))
        else:
            LOGGER.info('Report sent successfully.')


class MarginUploader(object):

    code_index = 2
    margin_index = 4
    pnl_eps = 0.001
    margin_eps = 0.009

    def __init__(self, filepath, trades, date):
        self._path = filepath
        self._trades = trades
        self._date = date
        self._call_accounts = {}
        self._call_account_trades = {}
        self._margins = {}
        self._status = []

    def get_margins(self):
        with open(self._path, 'r') as file:
            rows = csv.reader(file)
            next(rows)
            for row in rows:
                if not row:
                    continue
                try:
                    client_code = row[self.code_index]
                    init_margin = float(row[self.margin_index])
                    if client_code in self._margins:
                        self._margins[client_code] += init_margin
                    else:
                        self._margins[client_code] = init_margin
                except Exception as exc:
                    msg = 'Failed to read initial margin for row %s: %s' % (
                        row, exc)
                    LOGGER.exception(msg)
                    logme(msg, 'WARNING')

    def get_call_accounts(self):
        if not self._margins:
            msg = 'No margins returned from file %s, %s.' % (
                self._path, FAIL_INFO)
            LOGGER.error(msg)
            logme(msg, 'ERROR')
            return

        for trade in self._trades:
            ins = trade.Instrument()
            if (trade.Status() in ['Simulated', 'Void'] or
                    not ins.InsType() == 'Deposit'):
                continue
            client_code = ins.ExternalId1()
            if client_code:
                self._call_accounts[client_code] = ins
                self._call_account_trades[client_code] = trade
            else:
                msg = ('No client code specified in the ExternalId1 field for'
                       ' call account %s.' % ins.Name())
                LOGGER.warning(msg)
                logme(msg, 'WARNING')

    def _get_current_margin(self, call_account):
        cash_flows = call_account.Legs()[0].CashFlows()
        total = 0
        for cf in cash_flows:
            if (cf.PayDate() == self._date and
                    cf.CashFlowType() == 'Fixed Amount'):
                total += round(cf.FixedAmount(), 6)
        return total

    def set_cash_flow(self, code):
        call_account = self._call_accounts[code]
        trade = self._call_account_trades[code]
        margin = self._margins[code]
        current_margin = self._get_current_margin(call_account)
        margin = margin - current_margin
        status = {
            'code': code,
            'portfolio': trade.Portfolio().Name(),
            'trade': trade.Oid(),
            'reason': ''
        }

        if abs(margin) < self.margin_eps:
            msg = ('Initial margin already updated to %s for call account %s.'
                    % (current_margin, call_account.Name()))
            LOGGER.info(msg)
            logme(msg)
            status['status'] = "Can't upload"
            status['reason'] = 'Initial margin already updated.'
            self._status.append(status)
            return

        cash_flow = None
        if IsCurrentInterestPeriod(call_account, self._date):
            cash_flow = FCallDepositFunctions.adjust(call_account, margin, self._date,
                                                    "Prevent Settlement", None, None, 1)
        else:
            cash_flow = FCallDepositFunctions.backdate(call_account, margin, self._date,
                                                       acm.Time.DateToday(),
                                                       "Prevent Settlement", None, None, 1)
        if cash_flow:
            msg = ('Updated initial margin to %s for call account %s.'
                   % (margin, call_account.Name()))
            LOGGER.info(msg)
            logme(msg)
            status['status'] = 'Success'
        else:
            status['status'] = 'Error'
            status['reason'] = "Cashflow wasn't created."
        self._status.append(status)

    def _get_pnl_change(self, portfolio):
        tpl_columns = ['Client TPL']
        query = acm.CreateFASQLQuery('FTrade', 'AND')
        query.AddAttrNode('Portfolio.Name', 'EQUAL', portfolio.Name())
        query.AddAttrNode('Status', 'NOT_EQUAL',
                          acm.EnumFromString('TradeStatus', 'Simulated'))
        pnl_change = 0
        if not CALENDAR.IsNonBankingDay(None, None, self._date):
            tpl_dict = TradingManagerSweeper(query, self._date,
                                             tpl_columns, True)
            pnl_change = sum([val for vals in tpl_dict.values()
                              for val in vals])
        return pnl_change

    def _is_margin_needed(self, call_account):
        add_info_spec = acm.FAdditionalInfoSpec['PS_SafexAccount']
        add_infos = acm.FAdditionalInfo.Select('addInf=%s and fieldValue="%s"' % (
                                                add_info_spec.Oid(), call_account.Name()))
        prfs = [acm.FPhysicalPortfolio[oid] for oid in
                [ai.Recaddr() for ai in add_infos]]
        total_pnl_change = sum([self._get_pnl_change(prf) for prf in prfs])
        return abs(total_pnl_change) > self.pnl_eps

    def set_margins(self):
        if not self._call_accounts:
            msg = 'No valid call account selected, %s.' % FAIL_INFO
            LOGGER.error(msg)
            logme(msg, 'ERROR')
            return

        for code, call_account in self._call_accounts.iteritems():
            if code in self._margins:
                self.set_cash_flow(code)
            else:
                msg = ('No initial margin found for call '
                       'account %s with client code %s in %s.'
                       % (call_account.Name(), code, self._path))
                if self._is_margin_needed(call_account):
                    LOGGER.warning(msg)
                    logme(msg, 'WARNING')
                else:
                    LOGGER.info(msg)
                    logme(msg, 'INFO')
                trade = self._call_account_trades[code]
                status = {
                    'code': code,
                    'portfolio': trade.Portfolio().Name(),
                    'trade': trade.Oid(),
                    'status': 'Warning',
                    'reason': 'Margin not found in the file.'
                }
                self._status.append(status)

    def get_status(self):
        return self._status


def ael_main(dictionary):
    process_name = "ps_upload_initial_margin"
    with bp_start(process_name):
        logme.setLogmeVar(SCRIPT_NAME,
                          dictionary['Logmode'],
                          dictionary['LogToConsole'],
                          dictionary['LogToFile'],
                          dictionary['Logfile'],
                          dictionary['SendReportByMail'],
                          dictionary['MailList'],
                          dictionary['ReportMessageType'])

        if dictionary['date'] == 'Custom Date':
            date = dictionary['dateCustom']
        else:
            date = get_start_day_config()[dictionary['date']]

        tradefilter = dictionary['tradeFilter']
        trades = tradefilter.Trades()
        directory = dictionary['filePath'].SelectedDirectory().Text()
        filename = dictionary['fileName']
        filename = ''.join([filename, date.replace('-', ''), '.csv'])
        filepath = os.path.join(directory, date, filename)

        LOGGER.info("Loading initial margins from: %s", filepath)
        margin_uploader = MarginUploader(filepath, trades, date)
        try:
            margin_uploader.get_margins()
        except Exception as exc:
            msg = 'Failed to read file %s, %s: %s' % (filepath, FAIL_INFO, exc)
            LOGGER.exception(msg)
            logme(msg, 'ERROR')
            logme(None, 'FINISH')
            raise
        margin_uploader.get_call_accounts()
        margin_uploader.set_margins()

        if dictionary['send_report']:
            mail_list = dictionary['mail_list']
            content = margin_uploader.get_status()
            report = EmailReport(content, list(mail_list))
            report.create_report()
            report.send_report()

        if not any(['ERROR' in msg for msg in logme.LogBuffert]):
            LOGGER.info('completed successfully')

        logme(None, 'FINISH')

