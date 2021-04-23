"""-----------------------------------------------------------------------------
PROJECT                 :  Security Borrowing and Lending
PURPOSE                 :  Batch class used by Security Borrowing and Lending's
                           sweeping and auto return processes
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
"""


from sl_process_log import ProcessLog
import acm
import ael
import sl_partial_returns

class SblBatch:
    _timeSeriesSpec = None
    _recAddr = acm.FAel['sl_batch'].Oid()
    _additionalInfoName = None

    @staticmethod
    def _getBatchNumber(date, runNo):
        dateparts = acm.Time().DateToYMD(date)
        return '%(year)04i%(month)02i%(day)02i%(run)i' % {'year': dateparts[0], 'month': dateparts[1], 'day': dateparts[2], 'run': runNo}
    
    @staticmethod
    def _setAdditionalInfo(object, additionalInfoName, value):
        spec = acm.FAdditionalInfoSpec[additionalInfoName]
        if not spec:
            raise Exception('Could not load FAdditionalInfo [%s].' % additionalInfoName)

        query = 'addInf = %i and recaddr = %i' % (spec.Oid(), object.Oid())
        additionalInfo = acm.FAdditionalInfo.Select01(query, 'More than one FAdditionalInfo returned for ' + query)
        if not additionalInfo:
            additionalInfo = acm.FAdditionalInfo()
            additionalInfo.AddInf(spec)
            additionalInfo.Recaddr(object.Oid())
        # Front Upgrade 2013.3 -- Value to FieldValue
        additionalInfo.FieldValue(value)
        additionalInfo.Commit()

    @classmethod
    def _getRunNoAndValue(cls, date):
        series = acm.FTimeSeries.Select('recaddr = %(recAddr)i and timeSeriesSpec = %(timeSeriesSpec)i and day = %(day)s' % \
            {'recAddr': cls._recAddr, 'timeSeriesSpec': cls._timeSeriesSpec.Oid(), 'day': str(date)})
        maxRunNo = 0
        for s in series:
            if s.RunNo() > maxRunNo:
                maxRunNo = s.RunNo()

        runNo = maxRunNo + 1
        return runNo, cls._getBatchNumber(date, runNo)
        

    @classmethod
    def CreateBatch(cls, date):
        runNo, value = cls._getRunNoAndValue(date)
        timeSeries = acm.FTimeSeries()
        timeSeries.TimeSeriesSpec(cls._timeSeriesSpec)
        timeSeries.Recaddr(cls._recAddr)
        timeSeries.RunNo(runNo)
        timeSeries.Day(date)
        timeSeries.TimeValue(value)
        timeSeries.Commit()
        
        return cls(timeSeries)
        
    @classmethod
    def LoadBatch(cls, date, runNo):
        series = acm.FTimeSeries.Select01('recaddr = %(recAddr)i and timeSeriesSpec = %(timeSeriesSpec)i and runNo = %(run)i and day = %(day)s' % \
            {'recAddr': cls._recAddr, 'timeSeriesSpec': cls._timeSeriesSpec.Oid(), 'day': str(date), 'run': runNo}, \
            "More than one '%(spec)s' batch exist for %(day)s run number %(run)i." % \
                {'spec': cls._timeSeriesSpec, 'day': str(date), 'run': runNo})
        
        if not series:
            raise Exception("No '%(spec)s' batch exist for %(day)s run number %(run)i." % \
                {'spec': cls._timeSeriesSpec.FieldName(), 'day': str(date), 'run': runNo})

        return cls(series)
        
    def __init__(self, timeSeries):
        self._timeSeries = timeSeries
        
    def __cmp__(self, other):
        return self._timeSeries == other._timeSeries
        
    @property
    def BatchNumber(self):
        return int(self._timeSeries.TimeValue())
        
    @property
    def NumberOfTrades(self):
        cls = self.__class__
        query = r'''
            SELECT  COUNT(trdnbr)
            FROM    Trade,
                    Instrument,
                    AdditionalInfoSpec,
                    AdditionalInfo
            WHERE   Trade.insaddr = Instrument.insaddr
            AND     AdditionalInfoSpec.specnbr = AdditionalInfo.addinf_specnbr
            AND     AdditionalInfoSpec.field_name = '%s'
            AND     AdditionalInfo.recaddr = Instrument.insaddr
            AND     AdditionalInfo.value = %i''' % (cls._additionalInfoName, self.BatchNumber)
        
        result = ael.asql(query)[1][0]
        if not result:
            return 0
        else:
            return int(result[0][0])
        
    def _getSecurityLoans(self):
        cls = self.__class__
        query = acm.CreateFASQLQuery('FSecurityLoan', 'AND')
        op = query.AddOpNode('AND')
        op.AddAttrNode('AdditionalInfo.' + cls._additionalInfoName, 'EQUAL', self._timeSeries.TimeValue())
        return query.Select()
        
    def StampBatchNumber(self, object):
        if object.IsKindOf(acm.FTrade):
            object = object.Instrument()
        elif not object.IsKindOf(acm.FInstrument):
            raise Exception('Batch number can only be stamped on Trades and Instruments.')
        
        cls = self.__class__
        SblBatch._setAdditionalInfo(object, cls._additionalInfoName, self.BatchNumber)

class SblSweepBatch(SblBatch):
    _timeSeriesSpec = acm.FTimeSeriesSpec['SBL Sweeping Batch']
    _additionalInfoName = 'SL_SweepingBatchNo'
        
    def VoidBatch(self, log = None):
        if not log:
            log = ProcessLog('Void SBL Sweeping Batch')
        log.Information('Batch Number: %i' % self.BatchNumber)
        acm.BeginTransaction()
        try:
            numSecuritiesTerminated = 0
            numTradesVoided = 0
            for securityLoan in self._getSecurityLoans():
                for trade in securityLoan.Trades():
                    if trade.Status() != 'Void' and trade.MirrorTrade() != None:
                        trade.Status('Void')
                        trade.Commit()
                        numTradesVoided = numTradesVoided + 1
                        log.Information('Trade %i voided.' % trade.Oid())
                
                for trade in securityLoan.Trades():
                    if trade.Status() != 'Void':
                        trade.Status('Void')
                        trade.Commit()
                        numTradesVoided = numTradesVoided + 1
                        log.Information('Trade %i voided.' % trade.Oid())
                        
                if securityLoan.OpenEnd() != 'Terminated':
                    securityLoan.OpenEnd('Terminated')
                    securityLoan.Commit()
                    numSecuritiesTerminated = numSecuritiesTerminated + 1
                    log.Information('Security loan %s terminated.' % securityLoan.Name())

            acm.CommitTransaction()
        except Exception, ex:
            acm.AbortTransaction()
            log.Exception('Could not void batch %(batchNumber)s: ' % {'batchNumber': self.BatchNumber} + str(ex))
        else:
            log.Information('Batch %(batchNumber)i successfully voided. %(securities)i security loans were terminated and %(trades)i trades were voided.' \
                % {'batchNumber': self.BatchNumber, 'securities': numSecuritiesTerminated, 'trades': numTradesVoided})
        finally:
            print(log)
                
class SblAutoReturnBatch(SblBatch):
    _timeSeriesSpec = acm.FTimeSeriesSpec['SBL Return Batch']
    _additionalInfoName = 'SL_ReturnBatchNo'
    
    def VoidBatch(self):
        log = ProcessLog('Void SBL Auto Return Batch')
        try:
            log.Information('Batch Number: %i' % self.BatchNumber)
            numSecurities = 0
            numTrades = 0
            for securityLoan in self._getSecurityLoans():
                for trade in securityLoan.Trades():
                    if trade.Instrument().OpenEnd() == 'Terminated':
                        sl_partial_returns.revert_return(trade)
                        log.Information('Trade %i reinstated.' % trade.Oid())
                        numTrades += 1
        except Exception, ex:
            log.Exception('Could not void batch %(batchNumber)s: ' % {'batchNumber': self.BatchNumber} + str(ex))
        else:
            log.Information('Batch %(batchNumber)i successfully voided: %(trades)i trades were re-opened.' \
                % {'batchNumber': self.BatchNumber, 'securities': numSecurities, 'trades': numTrades})
        finally:
            print(log)
