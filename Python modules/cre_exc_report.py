"""----------------------------------------------------------------------------
PROJECT                 :  CRE into Front Arena
PURPOSE                 :  Exception report for PCG. The report flags FA trades
                           that did not receive valuations from CRE.
DEPATMENT AND DESK      :  PCG
DEVELOPER               :  Libor Svoboda
CR NUMBER               :  CHG1000032049
-------------------------------------------------------------------------------

HISTORY
===============================================================================
Date        Change no     Developer         Description
-------------------------------------------------------------------------------

"""
import acm
from at_email import EmailHelper
from at_logging import getLogger


LOGGER = getLogger('CRE_FA_valuations')
REPORT_NAME = 'CRE exception report'
TODAY = acm.Time.DateToday()


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
        </style>
        </head>
        <body>
        <h1>%(heading)s</h1>
        <table>
          <tr>
            <th></th>
            <th>Trade</th>
            <th>Instrument</th>
            <th>Portfolio</th>
            <th>Status</th>
            <th>Value Day</th>
          </tr>
    '''
    footer = '''</table>
        </body>
        </html>
    '''
    normal_row = '''<tr>
          <td>%(error)s</td>
          <td>%(trade)s</td>
          <td>%(instrument)s</td>
          <td>%(portfolio)s</td>
          <td>%(status)s</td>
          <td>%(value_day)s</td>
        </tr>
    '''
    
    def __init__(self, recipients, requested, processed, val_date):
        self._val_date = val_date
        self._ts_spec = acm.FTimeSeriesDvSpec['CRE_TheorVal']
        self._exc_trades = self._get_exc_trades(requested, processed)
        self._recipients = list(recipients)
        env = acm.FDhDatabase['ADM'].InstanceName()
        self._sender = 'FA %s' % env
        self._subject = REPORT_NAME
        self._heading = '%s, %s, %s' % (REPORT_NAME, env, TODAY)
        self._message = ''
    
    def _is_ins_valued(self, instrument):
        if not self._ts_spec:
            return False
        query = "timeSeriesDvSpecification=%s and recordAddress1=%s and storageDate='%s'" % (
                    self._ts_spec.Oid(), instrument.Oid(), self._val_date)
        ts = acm.FTimeSeriesDv.Select(query)
        if ts:
            return True
        return False
    
    def _get_exc_trades(self, requested, processed):
        missed_trades = sorted(list(set(requested) - set(processed)))
        exception_trades = []
        for trade_nbr in missed_trades:
            trade = acm.FTrade[trade_nbr]
            if (not trade or trade.Instrument().IsExpired() or 
                    trade.Status() in ['Simulated', 'Void']):
                continue
            if self._is_ins_valued(trade.Instrument()):
                continue
            exception_trades.append(trade)
        return exception_trades
    
    def create_report(self):
        if not self._exc_trades:
            self._message = ''
            return
        
        self._message += self.header % {'heading': self._heading}
        for trade in self._exc_trades:
            values = {
                'error': 'Missing CRE value in FA',
                'trade': str(trade.Oid()),
                'instrument': trade.Instrument().Name(),
                'portfolio': trade.Portfolio().Name(),
                'status': trade.Status(),
                'value_day': trade.ValueDay(),
            }
            row = self.normal_row % values
            self._message += row
        self._message += self.footer
    
    def send_report(self):
        if not self._message:
            LOGGER.info('No report to be sent.')
            return
        
        attachments = None
        email_type = 'html'
        email = EmailHelper(self._message, self._subject, self._recipients, 
                            self._sender, attachments, email_type)
        if str(acm.Class()) == 'FACMServer':
            email.sender_type = EmailHelper.SENDER_TYPE_SMTP
            email.host = EmailHelper.get_acm_host()
        try:
            email.send()
        except Exception as exc:
            LOGGER.exception('Error while sending report: %s' % str(exc))
        else:
            LOGGER.info('Report sent successfully.')


