"""-----------------------------------------------------------------------------
PROJECT                 :  Security Borrowing and Lending
PURPOSE                 :  Script that automatically returns security loan 
                           trades that arent necessary to cover short positions
DEPATMENT AND DESK      :  Prime Services, Securities Lending
REQUESTER               :  Linda Breytenbach
DEVELOPER               :  Francois Truter
CR NUMBER               :  511966
-----------------------------------------------------------------------------

HISTORY
=============================================================================
Date       Change no Developer          Description
-----------------------------------------------------------------------------
2010-11-16 494829    Francois Truter    Initial Implementation
2010-11-23 502781    Francois Truter    Added additional validation
2010-12-07 511966    Francois Truter    Added StartDate >= today validation
2011-02-18 580224    Francois Truter    _validateTrade to exclude negative trades 
                                        from return process
2011-03-22 602241    Francois Truter    added _getQuantity to clean invalid 
                                        values from calculation space
2011-04-04 619099    Francois Truter    added Rate Column parameter
2012-12-11 620455    Peter Fabian       Uses rates stored in Front instead of SBL_Rates file, 
                                        returns from second portfolio as well (agency to principal migration)
2013-04-02 951379    Peter Fabian       For trades not suitable for auto return changed warnings 
                                        to info message types. Fixed wording of the error when a corresponding 
                                        trade is not found. 
                                        For equitity positions changed column and grouping
                                        used to calculate positions to be in line 
                                        with remote sheet and business spec
2014-04-03 1854818   Peter Fabian       Exclude No Collateral trades from auto returning
2014-05-20 abcdef    Peter Fabian       Adjsut direction of agency trades (they are no more -1 * qty)
2017-07-18 4656410   Ondrej Bahounek    Change quantity to return condition.
"""

import acm
import at
import sl_partial_returns
from decimal import Decimal
from sl_rates import SblTimeSeriesRates
from sl_batch import SblAutoReturnBatch

NEWLINE = '\r\n'

def ToAcmDate(aelDate):
    [y, m, d] = aelDate.to_ymd()
    return acm.Time().DateFromYMD(y, m, d)

def _floatToStr(f):
    f = float(f)
    if f == round(f, 0):
        return '%i' % f
    else:
        return '%.2f' % f

def _isNumber(object):
    try:
        if object != object:
            isNumber = False
        else:
            object = float(object)
            isNumber = True
    except:
        isNumber = False

    return isNumber

def _getQuantity(object):
    if _isNumber(object):
        return Decimal(str(object))
    else:
        try:
            tObject = object[0]
            return _getQuantity(tObject)
        except Exception as ex:
            return None

class ReturnPosition:

    def __init__(self, instrument, returnDate, quantityToReturn, 
                 expiryDateBarier, returnCostBarier, exclude_lenders=None, exclude_borrowers=None):
        self._instrument = instrument
        self._returnDate = returnDate
        self._quantityToReturn = Decimal('%.10f' % quantityToReturn)
        self._expiryDateBarier = expiryDateBarier
        self._returnCostBarier = returnCostBarier
        self._trades = []
        self._agencyTrades = []
        self._quantityReturnedFromBorrower = Decimal('%.10f' % 0)
        self._exclude_lenders = exclude_lenders if exclude_lenders else []
        self._exclude_borrowers = exclude_borrowers if exclude_borrowers else []

    def __str__(self):
        output = '%s: %i' % (self._instrument.Name(), self._quantityToReturn) + NEWLINE
        output += '-' * len(output) + NEWLINE
        for trade in self._trades:
            output += '%i: %i' % (trade.Oid(), trade.QuantityInUnderlying()) + NEWLINE
        return output

    def _cost(self, trade):
        instrument = trade.Instrument()
        return trade.RefPrice() * instrument.Underlying().Quotation().QuotationFactor() * instrument.FirstFixedLeg().FixedRate() / 100.0 / 365.0

    def _cmpExpiryDate(self, x, y):
        daysX = x.DaysToOneYearExpiry()
        daysY = y.DaysToOneYearExpiry()
        if daysX > self._expiryDateBarier and daysY > self._expiryDateBarier:
            return 0
        else:
            return daysX - daysY

    def _cmpCost(self, x, y):
        costX = self._cost(x)
        costY = self._cost(y)
        if costX < costY:
            return 1
        elif costX > costY:
            return -1
        else:
            return 0

    def _cmpQuantity(self, x, y):
        quantityX = x.QuantityInUnderlying()
        quantityY = y.QuantityInUnderlying()
        if quantityX < quantityY:
            return -1
        elif quantityX > quantityY:
            return 1
        else:
            return 0

    def _cmpReturn(self, x, y):
        expiryDateResult = self._cmpExpiryDate(x, y)
        if expiryDateResult != 0:
            return expiryDateResult

        costResult = self._cmpCost(x, y)
        if costResult != 0:
            return costResult

        return self._cmpQuantity(x, y)

    def _sortTradesForReturn(self):
        self._trades.sort(cmp=self._cmpReturn)

    def _validateAgencyTrade(self, trade, log):
        instrument = trade.Instrument()
        today = acm.Time().DateNow()
        if trade.Aggregate() != 0 or trade.ArchiveStatus() != 0 or instrument.ArchiveStatus() !=0:
             log.Information('Trade [%(trade)i] cannot be considered for auto return to Lender, it is archived or aggregated.' % \
                {'trade': trade.Oid()})
        if instrument.InsType() != 'SecurityLoan':
            log.Information('Trade [%(trade)i] cannot be considered for auto return to Lender, it is a [%(type)s]. Only Security Loan instruments can be returned.' % \
                {'trade': trade.Oid(), 'type': instrument.InsType()})
        elif trade.QuantityInUnderlying() <= 0:
            log.Information('Trade [%(trade)i] cannot be considered for auto return to Lender, it must have a positive trade quantity: %(quantity)f' % \
                {'trade': trade.Oid(), 'quantity': trade.QuantityInUnderlying()})
        elif trade.Status() in ['Simulated', 'Void', 'FO Confirmed', 'Terminated']:
            log.Information('Trade [%(trade)i] cannot be considered for auto return to Lender, it has a status of [%(status)s]. Trade status must be BO Confirmed at a minimum in order to return.' % \
                {'trade': trade.Oid(), 'status': trade.Status()})
        elif instrument.OpenEnd() != 'Open End':
            log.Information('Trade [%(trade)i] cannot be considered for auto return to Lender, it has an open end status of [%(status)s]. Only open ended trades can be returned.' % \
                {'trade': trade.Oid(), 'status': instrument.OpenEnd()})
        elif instrument.StartDate() > self._returnDate:
            log.Information('Trade [%(trade)i] cannot be returned to Lender on %(returnDate)s, it only starts on %(startDate)s.' % \
                {'trade': trade.Oid(), 'returnDate': self._returnDate, 'startDate': instrument.StartDate()})
        elif instrument.StartDate() >= today:
            log.Information('Trade [%(trade)i] cannot be returned to Lender today [%(today)s], it only starts on %(startDate)s.' % \
                {'trade': trade.Oid(), 'today': today, 'startDate': instrument.StartDate()})
        elif trade.AdditionalInfo().SL_G1Counterparty1() in self._exclude_borrowers:
            log.Information('Trade [%(trade)i] cannot be returned to Lender, borrower "%(borrower)s" excluded.'
                % {'trade': trade.Oid(), 'borrower': trade.AdditionalInfo().SL_G1Counterparty1()})
        elif trade.AdditionalInfo().SL_G1Counterparty2() in self._exclude_lenders:
            log.Information('Trade [%(trade)i] cannot be returned to Lender, lender "%(lender)s" excluded.'
                % {'trade': trade.Oid(), 'lender': trade.AdditionalInfo().SL_G1Counterparty2()})
        else:
            return True
        return False
    
    def _validateTrade(self, trade, log):
        if not self._validateAgencyTrade(trade, log):
            return False
        instrument = trade.Instrument()
        if at.addInfo.get_value(instrument, 'SL_ExternalInternal') == "No Collateral":
            log.Information('Trade [%(trade)i] cannot be considered for auto return, it is flagged as "No Collateral".'
                % {'trade': trade.Oid()})
            return False
        return True

    @property
    def Instrument(self):
        return self._instrument

    @property
    def QuantityToReturn(self):
        return self._quantityToReturn

    def AddTrades(self, trades, log):
        for trade in trades:
            if self._validateTrade(trade, log):
                self._trades.append(trade)


    def AddAgencyTrades(self, portfolio, SLUnderlyingIns, log):
        insTrades = []
        
        query = acm.CreateFASQLQuery(acm.FTrade, 'AND')
        query.AddAttrNode('Portfolio.Name', 'EQUAL', portfolio.Name())
        query.AddAttrNode('Instrument.InsType', 'EQUAL', 'SecurityLoan')
        query.AddAttrNode('Instrument.Underlying.Name', 'EQUAL', SLUnderlyingIns.Name())
        query.AddAttrNode('Instrument.OpenEnd', 'EQUAL', 'Open End')
        
        trades = query.Select()

        for trade in trades:
            if self._validateAgencyTrade(trade, log):
                self._agencyTrades.append(trade)


    def _findCorrespondingAgencyTrade(self, origTrade, origQty, log):
        candidateTrades = []
        try:
            for agTrade in self._agencyTrades:
                agencyTradeQty = Decimal('%.10f' % agTrade.QuantityInUnderlying())

                if agencyTradeQty == origQty:
                    candidateTrades.append(agTrade)
        except Exception as e:
            log.Error(str(e))

        if candidateTrades:
            # since the quantity is the same, we can safely use the same function
            # to compare expiry date and price
            candidateTrades.sort(cmp=self._cmpReturn)
            return candidateTrades[0]


        log.Information("Corresponding agency trade for %s not found" % origTrade.Oid())

    def ReturnToLender(self, origTrade, origQty, returnedQty, batch, log):
        agencyTrade = self._findCorrespondingAgencyTrade(origTrade, origQty, log)
        if not agencyTrade:
            # add to some list to print at the end...
            log.Warning("No corresponding second leg trade for trade [%(trade)i] found" % \
                      {'trade': origTrade.Oid()})
            return

        agencyTradeQty = Decimal('%.10f' % agencyTrade.QuantityInUnderlying())
        # log.Information("found agency trade %s qty %f" % (agencyTrade.Oid(), agencyTrade.QuantityInUnderlying()))
        qtyToReturn = returnedQty
        try:
            if returnedQty == origQty:
                # full return
                batch.StampBatchNumber(agencyTrade)
                sl_partial_returns.partial_return(agencyTrade, self._returnDate, float(qtyToReturn))
                log.Information('[%(prf)s] Trade [%(trade)i] returned on %(date)s: %(instrument)s %(quantity)s.' % \
                    {'prf': agencyTrade.Portfolio().Name(), 'trade': agencyTrade.Oid(), 'date': str(self._returnDate), 'instrument': self._instrument.Name(), 'quantity': _floatToStr(qtyToReturn)})
            else:
                # partial return
                batch.StampBatchNumber(agencyTrade)
                newTrade = sl_partial_returns.partial_return(agencyTrade, self._returnDate, float(qtyToReturn))

                log.Information('[%(prf)s] Trade [%(trade)i] partially returned %(ret_qty)s on %(date)s: %(instrument)s orig qty: %(quantity)s.' % \
                    {'prf': agencyTrade.Portfolio().Name(), 'trade': agencyTrade.Oid(), 'ret_qty': _floatToStr(qtyToReturn), 'date': str(self._returnDate), 'instrument': self._instrument.Name(), 'quantity': _floatToStr(agencyTradeQty)})
                log.Information('Trade [%(trade)i] replaced by [%(newTrade)i]: %(quantity)s.' % \
                    {'trade': agencyTrade.Oid(), 'newTrade': newTrade.Oid(), 'quantity': _floatToStr(newTrade.QuantityInUnderlying())})
        except Exception as ex:
            raise Exception('An error occurred while processing trade %i: %s' % (agencyTrade.Oid(), ex))

    def ReturnTrades(self, batch, log):
        if round(self._quantityToReturn, 6) <= 0.00:
            log.Information('Nothing needs be returned for %s.' % self._instrument.Name())
            return

        if not self._trades:
            log.Information('No trades to return for %(instrument)s. Quantity to return %(quantity)s.' % \
                    {'instrument': self._instrument.Name(), 'quantity': _floatToStr(self._quantityToReturn)})
            return

        self._sortTradesForReturn()

        quantityLeftToReturn = self._quantityToReturn
        log.Information('Returning %(quantity)s of %(instrument)s:' % {'quantity': _floatToStr(self._quantityToReturn), 'instrument': self._instrument.Name()})
        for trade in self._trades:
            try:
                if quantityLeftToReturn == 0:
                    break
                tradeQuantity = Decimal('%.10f' % trade.QuantityInUnderlying())
                if tradeQuantity <= quantityLeftToReturn:
                    batch.StampBatchNumber(trade)
                    sl_partial_returns.partial_return(trade, self._returnDate, float(tradeQuantity))

                    quantityLeftToReturn -= tradeQuantity
                    self._quantityReturnedFromBorrower += tradeQuantity
                    log.Information('[%(prf)s] Trade [%(trade)i] returned on %(date)s: %(instrument)s %(quantity)s. Still to return %(left)s.' % \
                        {'prf': trade.Portfolio().Name(), 'trade': trade.Oid(), 'date': str(self._returnDate), 'instrument': self._instrument.Name(), 'quantity': _floatToStr(tradeQuantity), 'left': _floatToStr(quantityLeftToReturn)})

                    # return from the other portfolio
                    self.ReturnToLender(trade, tradeQuantity, tradeQuantity, batch, log)
                else:
                    costPerDay = self._cost(trade) * float(quantityLeftToReturn)
                    if costPerDay > self._returnCostBarier:
                        batch.StampBatchNumber(trade)
                        newTrade = sl_partial_returns.partial_return(trade, self._returnDate, float(quantityLeftToReturn))

                        self._quantityReturnedFromBorrower += quantityLeftToReturn

                        log.Information('[%(prf)s] Trade [%(trade)i] partially returned %(ret_qty)s on %(date)s: %(instrument)s orig qty: %(quantity)s.' % \
                            {'prf': trade.Portfolio().Name(), 'trade': trade.Oid(), 'ret_qty': _floatToStr(quantityLeftToReturn), 'date': str(self._returnDate), 'instrument': self._instrument.Name(), 'quantity': _floatToStr(tradeQuantity)})
                        log.Information('Trade [%(trade)i] replaced by [%(newTrade)i]: %(quantity)s.' % \
                            {'trade': trade.Oid(), 'newTrade': newTrade.Oid(), 'quantity': _floatToStr(newTrade.QuantityInUnderlying())})

                        # return from the other portfolio
                        self.ReturnToLender(trade, tradeQuantity, quantityLeftToReturn, batch, log)

                        quantityLeftToReturn = Decimal('0')
                    else:
                        log.Information('[%(prf)s] Trade [%(trade)i] will not be partially returned as the cost does not exceed the cost barrier: %(value).2f <= %(barrier).2f' % \
                            {'prf': trade.Portfolio().Name(), 'trade': trade.Oid(), 'value': costPerDay, 'barrier': self._returnCostBarier})
                        break
            except Exception as ex:
                raise Exception('An error occurred while processing trade %i: %s' % (trade.Oid(), ex))
        log.Information('Returned %(quantity)s of %(instrument)s, %(left)s left' % {'quantity': _floatToStr(self._quantityReturnedFromBorrower), 'instrument': self._instrument.Name(), 'left': _floatToStr(quantityLeftToReturn)})


class AutoReturn:

    def __init__(self, positionFilter, sblPortfolio, agencyPortfolio, returnDate, 
                 daysToOneYearExpiryBarrier, costBarrier, exclude_lenders=None, exclude_borrowers=None):
        self._positionFilter = positionFilter
        self._sblPortfolio = sblPortfolio
        self._agencyPortfolio = agencyPortfolio
        self._returnDate = returnDate
        self._daysToOneYearExpiryBarrier = daysToOneYearExpiryBarrier
        self._costBarrier = costBarrier
        self._exclude_lenders = exclude_lenders if exclude_lenders else []
        self._exclude_borrowers = exclude_borrowers if exclude_borrowers else []

    def _setPositionsToReturn(self, positionsToReturn, log):
        """ Accumulate all trades that can be returned.
        
            positionsToReturn - list of positions which will contain trades to autoreturn.
                Trades are placed in lists: _trades, _agencyTrades
        
        """
        underlyingGrouper = acm.FAttributeGrouper('Instrument.SLUnderlying')
        SL_Underlyng_PrtflGrouper = acm.Risk.GetGrouperFromName('SL.Undrlyng_Prtfl')
        calc_space = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), 'FPortfolioSheet')
        calc_space.SimulateGlobalValue('Portfolio Profit Loss Start Date', 'Inception')
        calc_space.SimulateGlobalValue('Portfolio Profit Loss End Date', 'Custom Date')
        calc_space.SimulateGlobalValue('Portfolio Profit Loss End Date Custom', self._returnDate)

        posNode = calc_space.InsertItem(self._positionFilter)
        posNode.ApplyGrouper(SL_Underlyng_PrtflGrouper)
        sblNode = calc_space.InsertItem(self._sblPortfolio)
        sblNode.ApplyGrouper(underlyingGrouper)
        calc_space.Refresh()

        eqPositionColumn = 'SL Portfolio Position'
        positionColumn = 'SL Inventory Position'
        time_buckets = acm.Time.CreateTimeBuckets(self._returnDate, "'0d'", None, None, 0, True, False, False, False, False)
        column_config = acm.Sheet.Column().ConfigurationFromTimeBuckets(time_buckets)

        positions = {}
        instrumentIterator = posNode.Iterator().FirstChild()
        while instrumentIterator:
            instrumentName = instrumentIterator.Tree().Item().StringKey()
            instrument = acm.FInstrument[instrumentName]
            if not instrument:
                log.RaiseException('Could not load instrument [%s].' % instrumentName)
            readQuantity = calc_space.CreateCalculation(instrumentIterator.Tree(), eqPositionColumn, column_config).Value()
            quantity = _getQuantity(readQuantity)
            if quantity:
                positions[instrument] = quantity

            instrumentIterator = instrumentIterator.NextSibling()

        instrumentIterator = sblNode.Iterator().FirstChild()
        while instrumentIterator:
            node = instrumentIterator.Tree().Item()
            instrumentName = node.StringKey()
            instrument = acm.FInstrument[instrumentName]
            if not instrument:
                log.RaiseException('Could not load instrument [%s].' % instrumentName)
            readQuantity = calc_space.CreateCalculation(instrumentIterator.Tree(), positionColumn, column_config).Value()
            sl_quantity = _getQuantity(readQuantity)  # SL positions
            if not sl_quantity:
                sl_quantity = 0

            posQuantity = 0
            if instrument in positions:
                posQuantity = positions[instrument]  # equity position
                
            quantityToReturn = sl_quantity + posQuantity
            log.Information("'%s': EQ quantity: %f, SL quantity: %f, to return: %f" 
                %(instrumentName, posQuantity, sl_quantity, quantityToReturn))
            
            if quantityToReturn > 0:
                position = ReturnPosition(instrument, self._returnDate, quantityToReturn, 
                                          self._daysToOneYearExpiryBarrier, self._costBarrier, 
                                          self._exclude_lenders, self._exclude_borrowers)
                position.AddTrades(node.Trades().AsArray(), log)  # add only valid trades that can be autoreturned
                # add candidates for auto return from the second portfolio as well
                position.AddAgencyTrades(self._agencyPortfolio, instrument, log)
                positionsToReturn.append(position)

            instrumentIterator = instrumentIterator.NextSibling()

    def ReturnTrades(self, log, internalRate, spread):
        # use internal rate and spread from task parameters
        rates = SblTimeSeriesRates(log, internalRate, spread)
        log.Information('Position Filter: ' + self._positionFilter.Name())
        log.Information('Sbl Portfolio: ' + self._sblPortfolio.Name())
        log.Information('Agency Portfolio: ' + self._agencyPortfolio.Name())
        log.Information('Return Date: ' + str(self._returnDate))
        log.Information('Days to One Year Exipry Barrier: %i' % self._daysToOneYearExpiryBarrier)
        log.Information('Cost Barrier: %f' % self._costBarrier)
        log.Information('Internal Rate: ' + str(internalRate))
        log.Information('Internal Spread: ' + str(spread))

        batch = SblAutoReturnBatch.CreateBatch(self._returnDate)
        log.Information('Batch Number: %i' % batch.BatchNumber)

        positionsToReturn = []
        self._setPositionsToReturn(positionsToReturn, log)
        positionsToReturn.sort(key=lambda position: position.Instrument.Name())

        for position in positionsToReturn:
            if rates.CanAutoReturn(position.Instrument):
                try:
                    position.ReturnTrades(batch, log)
                except Exception as ex:
                    log.Exception(str(ex))
            else:
                log.Information('Instrument [%(instrument)s] is set to not auto return in the SBL_Held additional info. Quantity to return: %(quantity)s' % \
                    {'instrument': position.Instrument.Name(), 'quantity': _floatToStr(position.QuantityToReturn)})
        log.Information('Auto return completed. %i trades returned' % batch.NumberOfTrades)



