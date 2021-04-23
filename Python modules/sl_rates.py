"""-----------------------------------------------------------------------------
PROJECT                 :  Security Borrowing and Lending
PURPOSE                 :  Rates class used by Security Borrowing and Lending's
                           sweeping and auto return processes. It reads a csv 
                           file and stores the information in the SblRates 
                           class.
DEPATMENT AND DESK      :  Prime Services, Securities Lending
REQUESTER               :  Linda Breytenbach
DEVELOPER               :  Francois Truter
CR NUMBER               :  494829
-----------------------------------------------------------------------------

HISTORY
=============================================================================
Date       Change no Developer          Description
-----------------------------------------------------------------------------
2010-11-16 494829    Francois Truter    Initial Implementation
2011-04-04 619099    Francois Truter    Allowed many rate columns in a file
2012-12-11 620455    Peter Fabian       Added common parent class, added class to store rates in time-series
2015-06-04 2860253   Ondrej Bahounek    Internal rates replaced by external ones.
                                        Add external rates' spreads.
"""

import acm
import csv
import string
import PS_TimeSeriesFunctions


class SblRateTuple:
    def __str__(self):
        return '(%f, %s)' % (self.rate, self.autoReturn)

    def __init__(self, rate, autoReturn):
        self.rate = rate
        self.autoReturn = autoReturn

class SblRates(object):
    _INTERNAL_KEY = '<<Internal>>'
    _SPREAD_KEY = '<<Spread>>'
    _BUY_SPREAD_KEY = 'Buy_Spread'
    _SELL_SPREAD_KEY = 'Sell_Spread'
    _SBL_RATE_KEY = "SBL_Rate"
    _SBL_HELD_KEY = "SBL_Held"

    _DEFAULT_INTERNAL_RATE = 0.35
    _DEFAULT_SPREAD = 0.01
    _DEFAULT_BUY_SPREAD = 0.05
    _DEFAULT_SELL_SPREAD = 0.02

    def __init__(self):
        self._rates = {
                       SblRates._INTERNAL_KEY: SblRateTuple(self._DEFAULT_INTERNAL_RATE, False),
                       SblRates._SPREAD_KEY: SblRateTuple(self._DEFAULT_SPREAD, False),
                       SblRates._BUY_SPREAD_KEY: SblRateTuple(self._DEFAULT_BUY_SPREAD, False),
                       SblRates._SELL_SPREAD_KEY: SblRateTuple(self._DEFAULT_SELL_SPREAD, False),
                       }

    @property
    def InternalRate(self):
        return self._rates[self._INTERNAL_KEY].rate
    
    @property
    def InernalSpread(self):
        return self._rates[self._SPREAD_KEY].rate
    
    @property
    def BuySpread(self):
        return self._rates[self._BUY_SPREAD_KEY].rate
    
    @property
    def SellSpread(self):
        return self._rates[self._SELL_SPREAD_KEY].rate
        
    def CanAutoReturn(self, instrument):
        """
            Tests whether the specified instrument can be auto-returned
            
            :param instrument: Tested instrument
            :type  instrument: acm.FInstrument
            :returns: True if instrument can be auto-returned, false otherwise
        """
        raise NotImplementedError("Should have implemented CanAutoReturn")

    def HasExternalRate(self, instrument):
        """
            Tests whether the specified instrument has external rate
            
            :param instrument: Tested instrument
            :type  instrument: acm.FInstrument
            :returns: True if instrument has external rate, false otherwise
        """
        raise NotImplementedError("Should have implemented HasExternalRate")

    def NoExternalRateMessage(self, instrument):
        """
            Returns an error string which can be used when requested external rate
            for the specified instrument cannot be found 
            
            :param instrument: Instrument used in output string
            :type  instrument: acm.FInstrument
            :returns: Error string
        """
        raise NotImplementedError("Should have implemented NoExternalRateMessage")

    def GetRate(self, instrument, external, spread=False):
        """
            
        """
        raise NotImplementedError("Should have implemented GetRate")


class SblFileRates(SblRates):

    def __init__(self, rateFilepath, rateColumn):
        super(SblFileRates, self).__init__()
        self._readFlag = False
        self._rateFilepath = rateFilepath
        self._rateColumn = rateColumn

    @property
    def Filepath(self):
        return self._rateFilepath

    def _validateRateColumn(self):
        if self._rateColumn < 3 or self._rateColumn % 2 != 1:
            raise Exception('Rates cannot be stored in column %i. Column 1 should contain the instrument code, even columns (2, 4, 6, etc) should contain the Auto Return marker and rates should be stored in uneven columns (3, 5, 7, etc).' % self._rateColumn)

    @staticmethod
    def GetValidRateColumns(maxCol):
        i = 3
        rateColumns = []
        while i <= maxCol:
            rateColumns.append(i)
            i += 2

        return rateColumns

    def _readRates(self):
        self._validateRateColumn()
        with open(self._rateFilepath, "rb") as rateFile:
            reader = csv.reader(rateFile)
            for row in reader:
                if reader.line_num > 2 and len(row) >= self._rateColumn - 1:
                    instrumentName = string.strip(str(row[0]))
                    autoReturn = string.strip(str(row[self._rateColumn - 2])) == ''
                    rateStr = ''
                    if len(row) >= self._rateColumn:
                        rateStr = string.strip(str(row[self._rateColumn - 1]))
                    rate = None
                    if rateStr:
                        try:
                            rate = float(rateStr)
                        except Exception, ex:
                            raise Exception('The rate [%(rate)s] for [%(instrument)s] in column [%(column)i] is invalid, please correct it in the file [%(filepath)s]: %(exception)s' % \
                                {'rate': rateStr, 'instrument': instrumentName, 'column': self._rateColumn, 'filepath': self._rateFilepath, 'exception': str(ex)})
                    if not self._rates.has_key(instrumentName) or rate:
                        self._rates[instrumentName] = SblRateTuple(rate, autoReturn)
            self._readFlag = True

    def NoExternalRateMessage(self, instrument):
        return 'No external rate was found for [%(instrument)s] in column [%(column)i], please correct it in the file [%(filepath)s]' % \
            {'instrument': instrument.Name(), 'column': self._rateColumn, 'filepath': self._rateFilepath}

    def HasExternalRate(self, instrument):
        if not self._readFlag:
            self._readRates()

        key = instrument.Name()
        if self._rates.has_key(key) and self._rates[key].rate:
            return True

        return False

    def GetRate(self, instrument, external, spread=False):
        if not self._readFlag:
            self._readRates()

        key = instrument.Name()
        if external:
            if self._rates.has_key(key) and self._rates[key].rate:
                return self._rates[key].rate
            else:
                raise Exception(self.NoExternalRateMessage(instrument))
        elif spread:
            return self._rates[SblRates._INTERNAL_KEY].rate + self._rates[SblRates._SPREAD_KEY].rate
        else:
            return self._rates[SblRates._INTERNAL_KEY].rate

    def CanAutoReturn(self, instrument):
        if not self._readFlag:
            self._readRates()

        key = instrument.Name()
        if self._rates.has_key(key):
            return self._rates[key].autoReturn
        else:
            return True


class SblTimeSeriesRates(SblRates):
    """
        Storing rates and 'held' info in time series is a little bit trickier 
        than storing it in add info or some static data storage, because once the 
        rate is no longer valid, we have to invalidate it, but we don't want to remove
        any information. 
        
        My solution is to store RateDeleted() and HeldDeleted() values in time-series
        to mark the rate as 'not present/deleted', which makes the logic a little bit 
        more complicated.
        
    """
    @staticmethod
    def RateDeleted():
        return -1

    @staticmethod
    def HeldDeleted():
        return -1

    def instrumentDeleted(self, instrument):
        if instrument:
            insName = instrument.Name()
            if not insName in self._rates:
                self._addRate(instrument)

            if int(round(self._rates[insName].rate)) == SblTimeSeriesRates.RateDeleted():
                return True
        return False

    def __init__(self, log, internalRate, internalSpread,
                 buySpread=SblRates._DEFAULT_BUY_SPREAD,
                 sellSpread=SblRates._DEFAULT_SELL_SPREAD):
        super(SblTimeSeriesRates, self).__init__()
        self._rates[SblRates._INTERNAL_KEY] = SblRateTuple(internalRate, False)
        self._rates[SblRates._SPREAD_KEY] = SblRateTuple(internalSpread, False)
        self._rates[SblRates._BUY_SPREAD_KEY] = SblRateTuple(buySpread, False)
        self._rates[SblRates._SELL_SPREAD_KEY] = SblRateTuple(sellSpread, False)
        self._log = log

    def _updateInternalRate(self, internalRate=None, spread=None):
        if internalRate:
            self._rates[SblRates._INTERNAL_KEY].rate = internalRate
        if spread:
            self._rates[SblRates._SPREAD_KEY] = SblRateTuple(spread, False)

    def _addRate(self, instrument):
        """
            Adds rate to cache
            
        """
        rateTimeSeries = PS_TimeSeriesFunctions.GetTimeSeries(self._SBL_RATE_KEY, instrument)
        if rateTimeSeries:
            # Front Upgrade 2013.3 -- Value amended to TimeValue; method name changed
            rate = PS_TimeSeriesFunctions.GetTimeSeriesPoint(rateTimeSeries, acm.Time().DateNow()).TimeValue()
        else:
            rate = SblTimeSeriesRates.RateDeleted()
        autoReturnTimeSeries = PS_TimeSeriesFunctions.GetTimeSeries(self._SBL_HELD_KEY, instrument)
        if autoReturnTimeSeries:
            # Front Upgrade 2013.3 -- Value amended to TimeValue; method name changed
            SblHeld = int(round(PS_TimeSeriesFunctions.GetTimeSeriesPoint(autoReturnTimeSeries, acm.Time().DateNow()).TimeValue()))
        else:
            SblHeld = 0
        # if rate and autoReturn equals -1, that means removed instrument
        if rate != SblTimeSeriesRates.RateDeleted() and SblHeld != SblTimeSeriesRates.HeldDeleted():
            autoReturn = SblHeld == 0
            self._rates[instrument.Name()] = SblRateTuple(rate, autoReturn)
        else:
            self._rates[instrument.Name()] = SblRateTuple(SblTimeSeriesRates.RateDeleted(), True)

    def CanAutoReturn(self, instrument):
        try:
            insName = instrument.Name()
        except:
            raise Exception("Instrument '%s' does not exist" % str(instrument))

        # if we already have it cached, return cached value
        if insName in self._rates:
            # just to be sure, check that the instrument is not in the deleted state in time series
            # although it's true that all the instruments that are not in the file can be returned
            # so this is, strictly speaking, not really necessary I think
            if not self.instrumentDeleted(instrument):
                return (self._rates[insName].autoReturn == 1)
            else:
                return True
        # or create new cached value and return it
        elif PS_TimeSeriesFunctions.GetTimeSeries(self._SBL_RATE_KEY, instrument):
            self._addRate(instrument)
            if not self.instrumentDeleted(instrument):
                return (self._rates[insName].autoReturn == 1)
            else:
                return True
        # or return the default value
        else:
            return True

    def HasExternalRate(self, instrument):
        try:
            insName = instrument.Name()
        except:
            raise Exception("Instrument '%s' does not exist" % str(instrument))

        if insName in self._rates and self._rates[insName].rate:
            # if the rate is not "deleted"
            if not self.instrumentDeleted(instrument):
                return True
        elif PS_TimeSeriesFunctions.GetTimeSeries(self._SBL_RATE_KEY, instrument):
            self._addRate(instrument)
            if not self.instrumentDeleted(instrument):
                return True

        return False

    def NoExternalRateMessage(self, instrument):
        return ("No external rate was found for [%(instrument)s], "
            "please check upload file and upload the rates to Front Arena. "
            "Using internal rates instead." % \
            {'instrument': instrument.Name()})

    def GetInternalRate(self, insName, use_spread):
        if use_spread:
            return self._rates[SblRates._INTERNAL_KEY].rate + self._rates[SblRates._SPREAD_KEY].rate
        return self._rates[SblRates._INTERNAL_KEY].rate 
        
    def GetRate(self, instrument, is_external, use_spread=False):
        """ Getting rates only from external rates file.
        If no external rate is present in file
        (rate has to be uploaded via the sl_upload_SBL_Rates script),
        the internal rates will be used instead (warning displayed).   
        """
        try:
            insName = instrument.Name()
        except:
            raise Exception("Instrument '%s' does not exist" % str(instrument))
        
        if not insName in self._rates:
            if PS_TimeSeriesFunctions.GetTimeSeries(self._SBL_RATE_KEY, instrument):
                self._addRate(instrument)
            else:
                self._log.Warning(self.NoExternalRateMessage(instrument))
                return self.GetInternalRate(insName, use_spread)

        if self.instrumentDeleted(instrument):
            self._log.Warning(self.NoExternalRateMessage(instrument))
            return self.GetInternalRate(insName, use_spread)
        
        # getting rates only from rates file
        rate = self._rates[insName].rate
        if is_external:
            # external trade: SBL Portfolio -> Short portfolio
            return rate
               
        if use_spread:  
            # SELL trade's rate
            # internal trade: SBL Portfolio -> Short portfolio
            return rate - self._rates[SblRates._SELL_SPREAD_KEY].rate
        else:
            # BUY trade's rate
            # internal trade: Long portfolio -> SBL Portfolio
            return rate - self._rates[SblRates._BUY_SPREAD_KEY].rate
        
        
        
