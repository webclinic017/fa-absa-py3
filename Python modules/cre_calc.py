"""----------------------------------------------------------------------------
PROJECT                 :  CRE into Front Arena
PURPOSE                 :  This module takes care of calling CRE 
                           CalculationRunner web service, and provides 
                           functionality for selecting trades for valuations.
DEPATMENT AND DESK      :  Middle Office, FX Trading
DEVELOPER               :  Libor Svoboda
CR NUMBER               :  CHNG0003040071
-------------------------------------------------------------------------------

HISTORY
===============================================================================
Date        Change no     Developer         Description
-------------------------------------------------------------------------------
18/01/2018  CHG1000032049 Libor Svoboda     Updated logging and trade selection.
20/02/2018  CHG1000166547 Libor Svoboda     Logging in line with backend 
                                            standards.
"""
import acm
import csv
from time import sleep
from suds.client import Client
from at_time import to_datetime
from at_logging import getLogger


CALC_RUNNER_HEADERS = {'Content-Type': 'text/xml; charset=utf-8'}
TODAY = acm.Time.DateToday()
MONTH_AGO = acm.Time.DateAddDelta(TODAY, 0, -1, 0)
WEEK_AGO = acm.Time.DateAddDelta(TODAY, 0, 0, -7)
LOGGER = getLogger('CRE_FA_valuations')


class TradeFileGenerator(object):
    
    """Select CRE-valued trades and save them to a file.
    
    Instance variables:
        _val_group - Val Group
        _instruments - instruments with the above Val Group
        _trades - trades of the above instruments
    
    Public methods:
        save_file - generate trade file and save it
    """
    
    def __init__(self, val_group, include_ext_val_trades=False, additional_trades=None):
        self._val_group = val_group
        self._ext_val = include_ext_val_trades
        self._additional_trades = additional_trades
        self._instruments = self._get_instruments()
        self._trade_numbers = self._get_trade_numbers()
        
    def _get_instruments(self):
        """Return instruments corresponding to the Val Group."""
        query = acm.CreateFASQLQuery('FInstrument', 'AND')
        query.AddAttrNode('ValuationGrpChlItem.Name',
                          'EQUAL', self._val_group.Name())
        instruments = query.Select()
        if not instruments:
            LOGGER.warning('No instruments in the specified ValGroup.')
        return instruments
    
    def _get_ext_val_trades(self):
        add_infos = acm.FAdditionalInfo.Select(
                        'addInf="ExternalVal" and updateTime>"%s"' % MONTH_AGO)
        return [ai.Recaddr() for ai in add_infos]
    
    def _get_trade_numbers(self, ins_trades_only=False):
        """Return trades belonging to the selected instruments."""
        trade_numbers = []
        for ins in self._instruments:
            trade_numbers.extend([trade.Oid() for trade in ins.Trades()])
            if not ins.Trades():
                LOGGER.warning("Instrument '%s' contains no trades." % ins.Name())
        
        if not trade_numbers:
            LOGGER.warning('Selected instruments contain no trades.')
        
        if ins_trades_only:
            return [t for t in sorted(list(set(trade_numbers))) 
                    if acm.FTrade[t].Instrument().ExpiryDateOnly() > WEEK_AGO]
        
        if self._ext_val:
            ext_val_trades = self._get_ext_val_trades()
            trade_numbers.extend(ext_val_trades)
        
        if self._additional_trades:
            add_trades = [t.Oid() for t in self._additional_trades]
            trade_numbers.extend(add_trades)
        
        return [t for t in sorted(list(set(trade_numbers))) 
                if acm.FTrade[t].Instrument().ExpiryDateOnly() > WEEK_AGO]
    
    def get_trade_numbers(self):
        return self._get_trade_numbers(True)
    
    def save_file(self, trade_path):
        """Generate trade file and save it.
        
        Arguments:
            trade_path - trade file path
        """
        try:
            with open(trade_path, 'wb') as trade_file:
                trade_file.write('trdnbr\n\n')
                trade_file.write('\n'.join([str(t) for t in self._trade_numbers]))
                trade_file.write('\n\n%s\n' % len(self._trade_numbers))
        except IOError as err:
            LOGGER.exception('Generating trade file (%s) failed: %s'
                             % (trade_path, err))
            raise
        
        LOGGER.info('Wrote secondary output to: %s' % trade_path)


class CalculationRunner(object):
    
    """Handle CRE Calculation Runner.
    
    Instance variables:
        _wsdl - Calculation Runner service
        _val_date - valuation date
        _risk - CRE calculation risk type
        _error_path - path to CRE error file
        _error_msg - error message
    
    Public methods:
        run - run CRE calculations
    """
    
    def __init__(self, wsdl, val_date, risk, error_path=''):
        self._wsdl = wsdl
        self._val_date = val_date
        self._risk = risk
        self._error_path = error_path
        self._error_msg = ''
    
    def _call_calc_runner(self):
        """Call CRE Calculation Runner web service."""
        date = to_datetime(self._val_date)
        client = Client(self._wsdl, headers=CALC_RUNNER_HEADERS)
        
        # Start risk calculations
        risk_id = client.service.GenerateRisk(self._risk, '', date, date)
        LOGGER.info('CalculationRunner status: Calculating...')
        while True:
            status = client.service.GetCalculationStatus(risk_id)
            if status == 'Calculating':
                sleep(5)
                continue
            LOGGER.info('CalculationRunner status: %s.' % status)
            # Save output files
            client.service.GenerateReports(risk_id)
            sleep(5)
            break

    def _process_error_file(self):
        """Process csv error file generated by Calculation Runner."""
        try:
            with open(self._error_path, 'rb') as error_file:
                rows = csv.reader(error_file, delimiter=',')
                labels = next(rows)
                for row in rows:
                    self._error_msg += ('\n\t' + 
                                        '; '.join(map(': '.join, list(zip(labels, row)))))
        except IOError as err:
            LOGGER.warning('Processing error file (%s) failed: %s'
                           % (self._error_path, err))

    def run(self):
        """Run calculations."""
        LOGGER.info('Starting CRE CalculationRunner (%s) for %s.'
                    % (self._wsdl, self._val_date))

        try:
            self._call_calc_runner()
        except Exception as exc:
            LOGGER.exception("CRE CalculationRunner failed: %s" % exc)
            raise
        
        if self._error_path:
            self._process_error_file()
        
        if self._error_msg:
            LOGGER.error('CRE CalculationRunner finished with errors: %s'
                         % self._error_msg)
            self._error_msg = ''
        else:
            LOGGER.info('CRE CalculationRunner finished.')
