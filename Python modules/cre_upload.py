"""----------------------------------------------------------------------------
PROJECT                 :  CRE into Front Arena
PURPOSE                 :  This module takes care of processing CRE output
                           file, and uploading CRE data to time series.
DEPATMENT AND DESK      :  Middle Office, FX Trading
DEVELOPER               :  Libor Svoboda
CR NUMBER               :  CHNG0003040071
-------------------------------------------------------------------------------

HISTORY
===============================================================================
Date        Change no     Developer         Description
-------------------------------------------------------------------------------
18/02/2018  CHG1000032049 Libor Svoboda     Updated logging.

"""
import acm
import os
import csv
import shutil
import re
import at_timeSeriesDv as at_ts
from at_collections import OrderedDict
from at_logging import getLogger


LOGGER = getLogger('CRE_FA_valuations')


class ColumnSpecs(object):
    
    """Class holding parameters describing CRE output file structure.
    
    Instance variables:
        trade_index - index of column with trade numbers
        ts_specs - dictionary specifying columns related to time series
        ts_no_scaling - list of time series names whose values should
            not be scaled
        curr_specs - dictionary specifying columns related to currencies
    
    Public methods:
        parse_column_specs - return a dictionary describing columns
    """
    
    def __init__(self, trade_index, ts_specs, ts_no_scaling=[], curr_specs=''):
        self.trade_index = trade_index
        self.ts_specs = self.parse_column_specs(ts_specs)
        self.ts_no_scaling = ts_no_scaling
        self.curr_specs = self.parse_column_specs(curr_specs)
    
    @classmethod
    def parse_column_specs(cls, input_string):
        """Return a dictionary describing columns.
        
        Arguments:
            input_string - string to be parsed
        """
        specs_dict = OrderedDict()
        pairs = input_string.split(',')
        for pair in pairs:
            try:
                key, value = pair.split(':')
                specs_dict[key.strip()] = int(value)
            except ValueError:
                pass
        return specs_dict

    
class FileProcessor(object):
    
    """Process CRE output file.
    
    Instance variables:
        _cre_path - path to CRE output file
        _temp_path - path to temporary copy of CRE output file
        date - valuation date
        ts_specs - dictionary specifying columns related to time series
        curr_specs - dictionary specifying columns related to currencies
        ts_no_scaling - list of time series names whose values should
            not be scaled
        trade_index - index of column with trade number
    
    Public methods:
        run - start CRE output file processor
    """
    
    def __init__(self, cre_path, val_date, column_specs, trade_qf=None):
        self._cre_path = cre_path
        self._temp_path = self._get_temp_path(cre_path)
        self._trade_numbers = []
        self.date = val_date
        self.ts_specs = column_specs.ts_specs
        self.curr_specs = column_specs.curr_specs
        self.ts_no_scaling = column_specs.ts_no_scaling
        self.trade_index = column_specs.trade_index
        self.trade_qf = trade_qf

    @staticmethod  
    def _get_temp_path(orig_path):
        """Return temporary path."""
        orig_dir, orig_file = os.path.split(orig_path)
        time_now = acm.Time.TimeNow().replace(' ', '_').replace(':', '')
        temp_file = 'Temp_' + time_now + orig_file
        return os.path.join(orig_dir, temp_file)
    
    def _create_temp_file(self):
        """Create temporary copy of the CRE output file."""
        try:
            # Create a temporary copy of the original file
            shutil.copyfile(self._cre_path, self._temp_path)
        except IOError as err:
            LOGGER.exception('Creating temporary file failed: %s' % err)
            return False
        return True
    
    def _process_file(self):
        """Process CRE output file."""
        self._trade_numbers = []
        with open(self._temp_path, 'rb') as csvfile:
            rows = csv.reader(csvfile, delimiter=',')
            header = next(rows)
            for row in rows:
                row_processor = RowProcessor(self, row, header)
                row_processor.run()
                trade_nbr = row_processor.get_trade_number()
                if trade_nbr:
                    self._trade_numbers.append(trade_nbr)
    
    def get_trade_numbers(self):
        return self._trade_numbers
    
    def run(self):
        """Start CRE output processor."""
        LOGGER.info('Starting %s file processing.' % self._cre_path)
        if not self._create_temp_file():
            LOGGER.info('Processing %s file finished.' % self._cre_path)
            return
        
        try:
            self._process_file()
        finally:
            os.remove(self._temp_path)
            LOGGER.info('Processing %s file finished.' % self._cre_path)


class RowProcessor(object):
    
    """Process row of CRE output file.
    
    Instance variables:
        _row - row of CRE output file
        _header - header of CRE output file
        _ts_specs - dictionary specifying columns related to time series
        _curr_specs - dictionary specifying columns related to currencies
        _ts_no_scaling - list of time series names whose values should
            not be scaled
        _trade_index - index of column with trade number
        _date - valuation date
        _trade - trade corresponding to a trade number given in the row
        _instrument - instrument of the above trade
    
    Public methods:
        run - start CRE output row processor
    """
    
    def __init__(self, file_processor, row, header):
        self._row = row
        self._header = header
        self._ts_specs = file_processor.ts_specs
        self._ts_no_scaling = file_processor.ts_no_scaling
        self._curr_specs = file_processor.curr_specs
        self._trade_index = file_processor.trade_index
        self._date = file_processor.date
        self._trade_qf = file_processor.trade_qf
        self._instrument = None
        self._trade = None
     
    def _validate_trade(self):
        """Validate trade number given in the row."""
        self._trade = acm.FTrade[self._row[self._trade_index]]
        try:
            self._instrument = self._trade.Instrument()
        except AttributeError:
            LOGGER.warning("Invalid trade number: '%s'."
                           % self._row[self._trade_index])
            return False
        
        if self._trade_qf and not self._trade_qf.Query().IsSatisfiedBy(self._trade):
            return False
        return True
    
    def _scale_value(self, index):
        """Scale row value form an instrument level to a trade level.
        
        Arguments:
            index - index specifying row position  
        """
        return float(self._row[index]) / (self._trade.Quantity() * 
                                          self._instrument.ContractSize())
    
    def _get_currency(self, index):
        """Return currency of a row value.
        
        Arguments:
            index - index specifying row position 
        """
        try:
            match = re.search('\[(.*)\]', self._header[index]).group(1)
        except AttributeError:
            return ''
         
        if acm.FCurrency[match]:
            return match
         
        try:
            return self._row[self._curr_specs[match]]
        except KeyError:
            return ''
    
    def _get_value(self, ts_name, index):
        """Return row value.
        
        Arguments:
            ts_name - time series name corresponding to the value
            index - index specifying row position
        """
        try:
            if ts_name in self._ts_no_scaling:
                return float(self._row[index])
            else:
                return self._scale_value(index)
        except ValueError:
            LOGGER.warning("Invalid field encountered for column %s and"
                           " trade %s." % (index, self._trade.Oid()))
        except IndexError:
            LOGGER.error("No record found for column %s and trade %s. "
                         "Please check Calculation Runner settings."
                         % (index, self._trade.Oid()))
        return None
    
    def _update_time_series(self, ts_name, value):
        """Update time series.
        
        Arguments:
            ts_name - time series name
            value - time series value
        """
        try:
            at_ts.update_time_series_value(ts_name, self._instrument.Oid(),
                                           None, self._date, value)
        except ValueError as err:
            LOGGER.exception("Updating time series for %s failed: %s"
                             % (self._instrument.Name(), err))
             
        LOGGER.info("%s value '%s' updated for %s."
                    % (ts_name, value, self._instrument.Name()))
    
    def get_trade_number(self):
        trade = acm.FTrade[self._row[self._trade_index]]
        if trade:
            return trade.Oid()
        return None
    
    def run(self):
        """Start CRE output row processor."""
        if not self._validate_trade():
            return
        
        for ts_name, index in self._ts_specs.items():
            value = self._get_value(ts_name, index)
            if value is None:
                continue
            currency = self._get_currency(index)
            dv = acm.DenominatedValue(value, currency, self._date)
            self._update_time_series(ts_name, dv)
