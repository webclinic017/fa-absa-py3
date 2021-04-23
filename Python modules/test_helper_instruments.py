"""-----------------------------------------------------------------------------
PROJECT                 :  N/A
PURPOSE                 :  FInstrument unit test helper classes
DEPATMENT AND DESK      :  N/A
REQUESTER               :  N/A
DEVELOPER               :  Francois Truter
CR NUMBER               :  526074
-----------------------------------------------------------------------------

HISTORY
=============================================================================
Date       Change no Developer          Description
-----------------------------------------------------------------------------
2010-11-16 494829    Francois Truter    Initial implementation
2010-12-17 526074    Francois Truter    Updated
"""

import acm
import uuid
import ael
import sl_functions
import test_helper_general

class SlBatchType:
    Sweeping = 0
    AutoReturn = 1

class InstrumentHelper:

    stock = None
    defaultUnderlying = None

    @staticmethod
    def _getDefaultUnderlying():
        if InstrumentHelper.defaultUnderlying == None:
            InstrumentHelper.defaultUnderlying = InstrumentHelper.CreatePersistantStock()
        return InstrumentHelper.defaultUnderlying
   
    @classmethod
    def _getStock(cls):
        if cls.stock == None:
            stocks = acm.FStock.Select('oid > 0')
            cls.stock = stocks.First()
        return cls.stock
        
    @staticmethod
    def CreateSecurityLoanFromUnderlying(underlying, refPrice, rate, slIntExt, startDate, slBatchType, batchNo, endDate = None):
        acm.BeginTransaction()
        slInstrument = acm.FSecurityLoan()
        if not endDate:
            endDate = acm.FCalendar['ZAR Johannesburg'].AdjustBankingDays(startDate, 1)
        try:
            slInstrument.StartDate(startDate)
            slInstrument.OpenEnd('Open End')
            slInstrument.UnderlyingType(underlying.InsType())
            slInstrument.Underlying(underlying)
            slInstrument.RefPrice(refPrice)
            slInstrument.RefValue(slInstrument.ContractSize() / (slInstrument.RefPrice() * slInstrument.Quotation().QuotationFactor()))
            slInstrument.SpotBankingDaysOffset(0)
                     
            leg = slInstrument.CreateLeg(True)
            leg.StartDate(startDate)
            leg.EndDate(endDate)
            leg.LegType('Fixed')
            leg.DayCountMethod('Act/365')
            leg.FixedRate(rate)
            
            slInstrument.Commit()
            leg.Commit()
            slInstrument.AdditionalInfo().SL_ExternalInternal(slIntExt)
            if batchNo != None:
                if slBatchType == SlBatchType.Sweeping:
                    slInstrument.AdditionalInfo().SL_SweepingBatchNo(batchNo)
                elif slBatchType == SlBatchType.AutoReturn:
                    slInstrument.AdditionalInfo().SL_ReturnBatchNo(batchNo)
                else:
                    raise Exception('Unknown batch type')
                    
            acm.CommitTransaction()
        except Exception as ex:
            acm.AbortTransaction()
            raise ex
            
        return slInstrument
    
    @staticmethod
    def CreatePersistantOpenEndedSecurityLoan(startDate, endDate):
        underlying = InstrumentHelper._getDefaultUnderlying()
        rollingBaseDay = acm.Time().FirstDayOfMonth(acm.Time().DateAddDelta(startDate, 0, 1, 0))
        acm.BeginTransaction()
        try:
            instrument = acm.FSecurityLoan()
            instrument.StartDate(startDate)
            instrument.OpenEnd('Open End')
            instrument.Underlying(underlying)
            instrument.RefPrice(1)
            instrument.RefValue(1)
            instrument.SpotBankingDaysOffset(1)
            instrument.ExpiryDate(endDate)
             
            leg = instrument.CreateLeg(True)
            leg.StartDate(startDate)
            leg.EndDate(endDate)
            leg.LegType('Fixed')
            leg.DayCountMethod('Act/365')
            leg.FixedRate(1)
            leg.RollingPeriodBase(rollingBaseDay)
            leg.RollingPeriodUnit('Months')
            leg.RollingPeriodCount(1)
            leg.FixedCoupon(True)
            
            instrument.Commit()
            leg.Commit()
            acm.CommitTransaction()
            
        except Exception as ex:
            acm.AbortTransaction()
            raise ex
        return instrument
    
    @staticmethod
    def CreateTemporaryStock():
        instrument = acm.FStock()
        instrument.Name(str(uuid.uuid4()))
        return instrument
    
    @staticmethod    
    def CreatePersistantStock(price = 1):
        stock = InstrumentHelper._getStock()
        instrument = stock.Clone()
        instrument.Name(str(uuid.uuid4()))
        instrument.Commit()
        if price:
            test_helper_general.PriceHelper.CreatePrice(instrument, price)
        return instrument
    
    @staticmethod    
    def CreatePersistantCFDStock(startDate, endDate):
        assert startDate <= endDate
        
        stock = InstrumentHelper._getStock()
        instrument = stock.Clone()
        instrument.Name(str(uuid.uuid4()))
        instrument.Commit()
        
        startDate = acm.FCalendar['ZAR Johannesburg'].AdjustBankingDays(startDate, -1)
        nextDate = startDate
        count = 0
        while nextDate <= endDate:
            count += 1
            price = 1 + count%2
            test_helper_general.PriceHelper.CreatePrice(instrument, price, nextDate, acm.FParty['internal'])
            nextDate = acm.Time().DateAddDelta(nextDate, 0, 0, 1)
            
        return instrument
    
    @staticmethod    
    def CreatePersistantCFDSecurityLoan(startDate, endDate):
        instrument = InstrumentHelper.CreatePersistantOpenEndedSecurityLoan(startDate, endDate)
        underlying = InstrumentHelper.CreatePersistantCFDStock(startDate, endDate)
        instrument.Underlying(underlying)
        
        leg = instrument.Legs().At(0)
        leg.RollingPeriodBase(startDate)
        leg.RollingPeriodUnit('Days')
        leg.RollingPeriodCount(1)
        
        instrument.Commit()
        leg.Commit()
        
        acm.PollDbEvents()
        rate = leg.FixedRate()
        leg.GenerateCashFlows(rate)
        
        sl_functions.set_additional_info(instrument, 'SL_CFD', 'Yes')
        
        return instrument
    
    @staticmethod
    def CreatePersistantSecurityLoan(slBatchType = None, batchNo = None):
        startDate = acm.Time().DateNow()
        endDate = acm.FCalendar['ZAR Johannesburg'].AdjustBankingDays(startDate, 1)
        underlying = InstrumentHelper._getDefaultUnderlying()
        return InstrumentHelper.CreateSecurityLoanFromUnderlying(underlying, 1, 1, 'Internal', startDate, slBatchType, batchNo)
        
    @staticmethod
    def CreatePersistantEtf(underlying, price = 1):
        instrument = acm.FETF()
        instrument.Name(str(uuid.uuid4()))
        instrument.Underlying(underlying)
        instrument.Commit()
        test_helper_general.PriceHelper.CreatePrice(instrument, price)
        return instrument
    
    @staticmethod
    def GetInstrumentCount():
        result = ael.asql('SELECT COUNT(*) FROM Instrument')
        return result[1][0][0][0]
        
    @staticmethod
    def GetInventoryPosition(portfolio, instrument, date):
        underlyingGrouper = acm.FAttributeGrouper('Underlying')
        calc_space = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), 'FPortfolioSheet')
        calc_space.SimulateGlobalValue('Portfolio Profit Loss Start Date', 'Inception')
        calc_space.SimulateGlobalValue('Portfolio Profit Loss End Date', 'Custom Date')
        calc_space.SimulateGlobalValue('Portfolio Profit Loss End Date Custom', date)
            
        top_node = calc_space.InsertItem(portfolio)
        top_node.ApplyGrouper(acm.FChainedGrouper([underlyingGrouper]))
        calc_space.Refresh()
            
        positionColumn = 'SL Portfolio Position'
        time_buckets = acm.Time.CreateTimeBuckets(date, "'0d'", None, None, 0, True, False, False, False, False)
        column_config = acm.Sheet.Column().ConfigurationFromTimeBuckets(time_buckets)
            
        instrumentIterator = top_node.Iterator().FirstChild()
        while instrumentIterator:
            readInstrument = instrumentIterator.Tree().Item().StringKey()
            if readInstrument == instrument.Name():
                return round(calc_space.CreateCalculation(instrumentIterator.Tree(), positionColumn, column_config ).Value(), 10)
            instrumentIterator = instrumentIterator.NextSibling()
        
        return 0
        
    @staticmethod
    def AssertInventoryPosition(testCase, portfolio, instrument, date, expected, message):
        actual = InstrumentHelper.GetInventoryPosition(portfolio, instrument, date)
        testCase.assertEqual(expected, actual, message % {'expected': expected, 'actual': actual})
        
    @staticmethod
    def ClearSlBatchNumber(slBatchType, batchNo):
        if slBatchType == SlBatchType.Sweeping:
            addInfo = 'SL_SweepingBatchNo'
        elif slBatchType == SlBatchType.AutoReturn:
            addInfo = 'SL_ReturnBatchNo'
        else:
            raise Exception('Unknown batch type')
            
        query = acm.CreateFASQLQuery('FAdditionalInfo', 'AND')
        
        op = query.AddOpNode('AND')
        op.AddAttrNode('AddInf.FieldName', 'EQUAL', addInfo)
        op.AddAttrNode('FieldValue', 'EQUAL', batchNo)
        
        for addInfo in query.Select().AsArray():
            addInfo.Delete()
            
