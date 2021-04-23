"""-----------------------------------------------------------------------------
PROJECT                 :  Security Borrowing and Lending
PURPOSE                 :  Sweeps long positions into short positions by booking
                           the required security loans
DEPATMENT AND DESK      :  Prime Services, Securities Lending
REQUESTER               :  Linda Breytenbach
DEVELOPER               :  Francois Truter
CR NUMBER               :  634060
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date       Change no Developer                 Description
--------------------------------------------------------------------------------
2010-03-11 243997    Francois Truter           Initial Implementation
2010-03-15 254192    Francois Truter           Allowed partial sweeping
2010-04-12 279300    Paul Jacot-Guillarmod     Trade time on future dated 
                                               trades is set to today 
2010-06-08 332128    Francois Truter           Allow Multiple Sweeping per day
2010-08-23 409966    Francois Truter           Using FInstrument.SLPrice() to 
                                               accommodate ETF as underlying
2010-11-16 494829    Francois Truter           Added CFD sweep functionality. 
                                               Changes to use sl_process_log, 
                                               sl_batch and sl_rates.
2010-12-14 524194    Francois Truter           Allocate held positions
2011-04-04 619099    Francois Truter           Allowed missing external rates -
                                               those instruments are skipped.
                                               Fixed bug: if SBL desk is short
                                               and no other desk is short, the
                                               SBL desk's position wasn't covered
                                               Added rate column parameter
2011-04-19 634060    Francois Truter           Setting Pay Calendar
2011-08-22 746813    Herman Hoon               Set the Rolling Base Date to the Start Date
2012-12-11 620455    Peter Fabian              Use rates from time-series in Front Arena instead those from a file
2013-09-09 1323778   Peter Fabian              Fix for non-external trade types and thus setting ref price
2013-09-18 1357158   Peter Fabian              Fix for non-external trade types -- back to considering them as external
2014-03-26 1839433   Ondrej Bahounek           Instrument add info SL_VAT set to False after booking new SL
2014-09-25 abcdef    Peter Fabian              Transformed class methods which create SLoans to static methods
2015-06-04 2860253   Ondrej Bahounek           Internal rates replaced by external ones.
                                               Add external rates' spreads.
                                               Add specific instruments' filtering.
2017-09-07 4822973   Ondrej Bahounek           Set zero fees on PS_Zero_Fees portfolios addinfo.
"""

from sl_batch import SblSweepBatch
import acm
import math
import decimal


newline = '\r\n'

def _isZero(number):
    return abs(number) < 0.0000001

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

def _toDecimal(value):
    if not isinstance(value, decimal.Decimal):
            value = decimal.Decimal(str(value))
    return value

def _boolToStr(value):
    return 'Yes' if value else 'No'

class SblPrices:

    def __init__(self, date=None):
        self._prices = {}
        self._date = date

    def Add(self, instrument, price):
        if _isNumber(price):
            self._prices[instrument] = float(price)

    def GetPrice(self, instrument):
        if self._prices.has_key(instrument):
            return self._prices[instrument]

        if not self._date or self._date == acm.Time.DateToday():
            price = instrument.SLPrice()
        else:
            price = instrument.HistoricalSLPrice(self._date)

        self._prices[instrument] = price
        return price


class Position(object):

    InternalExternal = {False: 'Internal', 
                        True: 'External', 
                        "No Collateral": "No Collateral",}

    def __init__(self, portfolio, instrument, quantity, external):
        self.portfolio = portfolio
        self.instrument = instrument
        self._quantity = _toDecimal(quantity)
        self.external = external
        self.notifyQuantityChanged = None

    def __str__(self):
        return 'Portfolio | %(portfolio)s | Instrument | %(instrument)s | Quantity | %(quantity)s | %(external)s' % \
        {'portfolio': self.portfolio.Name(), 'instrument': self.instrument.Name(), 'quantity': self.quantity, 'external': Position.InternalExternal[self.external]}

    def get_quantity(self):
        return self._quantity

    def set_quantity(self, value):
        quantityBefore = self._quantity
        self._quantity = _toDecimal(value)
        self.notifyQuantityChanged(self, quantityBefore, self._quantity)

    quantity = property(get_quantity, set_quantity)


class PositionCollectionIterator:

    def __init__(self, positionCollection):
        self.index = -1
        self.positionCollection = positionCollection

    def __next__(self):
        self.index = self.index + 1
        if self.index >= len(self.positionCollection):
            raise StopIteration
        return self.positionCollection[self.index]

    def ItemRemoved(self, removedIndex):
        if removedIndex <= self.index:
            self.index -= 1

class PositionCollection:

    def __init__(self):
        self.positionList = []
        self.instrumentQuantities = {}
        self.iterators = []

    def __iter__(self):
        iterator = PositionCollectionIterator(self)
        self.iterators.append(iterator)
        return iterator

    def __str__(self):
        output = 'Length: %(len)i' % {'len': len(self)} + newline
        for position in self:
            output = output + str(position) + newline
        return output

    def __len__(self):
        return len(self.positionList)

    def __getitem__(self, key):
        return self.positionList[key]

    def _hasExternalPosition(self):
        for position in self.positionList:
            if position.external:
                return True
        return False

    def positionQuantityChanged(self, position, quantityBefore, quantityAfter):
        self.instrumentQuantities[position.instrument] = self.instrumentQuantities[position.instrument] + quantityAfter - quantityBefore

    def _add(self, position):
        if self.Exists(position.portfolio, position.instrument, position.external):
            type_ = Position.InternalExternal[position.external]
            raise Exception("An %(type)s position for portfolio [%(portfolio)s] and instrument [%(instrument)s] already exists." % \
                {'portfolio': position.portfolio.Name(), 'instrument': position.instrument.Name(), 'type': type_})
        else:
            position.notifyQuantityChanged = self.positionQuantityChanged
            self.positionList.append(position)

        instrument = position.instrument
        self.instrumentQuantities[instrument] = self.GetQuantity(instrument) + position.quantity

    def Add(self, portfolio, instrument, quantity, external):
        position = self.GetPosition(portfolio, instrument, external)
        position.quantity = position.quantity + _toDecimal(quantity)

    def Instruments(self):
        return self.instrumentQuantities.keys()

    def GetQuantity(self, instrument):
        if instrument in self.instrumentQuantities:
            return self.instrumentQuantities[instrument]
        else:
            zero = decimal.Decimal('0')
            self.instrumentQuantities[instrument] = zero
            return zero

    def GetPositionsForInstrument(self, instrument):
        newPositions = PositionCollection()
        for position in self:
            if position.instrument == instrument:
                newPositions._add(position)

        return newPositions

    def GetDistinctPortfolios(self):
        portfolios = set()
        for position in self.positionList:
            portfolios.add(position.portfolio)

        return portfolios

    def Exists(self, portfolio, instrument, external):
        for position in self:
            if position.portfolio == portfolio and position.instrument == instrument and position.external == external:
                return True
        return False

    def GetPosition(self, portfolio, instrument, external):
        for position in self:
            if position.portfolio == portfolio and position.instrument == instrument and position.external == external:
                return position

        newPosition = Position(portfolio, instrument, 0, external)
        self._add(newPosition)
        return newPosition

    def RemovePosition(self, position):
        if position in self.positionList:
            index = self.positionList.index(position)
            for iterator in self.iterators:
                iterator.ItemRemoved(index)
            self.instrumentQuantities[position.instrument] = self.instrumentQuantities[position.instrument] - position.quantity
            self.positionList.pop(index)

    def _validateRateAndPrice(self, underlying, external, applySpread, rates, prices, log):
        try:
            referencePrice = prices.GetPrice(underlying)
            rate = rates.GetRate(underlying, external, applySpread)

            if referencePrice == 0:
                raise Exception('Security Loan cannot have a zero reference price, underlying instrument: %(underlying)s.' % {'underlying': underlying.Name()})
        except Exception, ex:
            log.Exception(str(ex))

    @staticmethod
    def createAndCommitSecurityLoan(batchNumber, openEnd, underlying, startDate, tradeQuantity, external, rate, referencePrice, bookCfd):
        zarCalendar = acm.FCalendar['ZAR Johannesburg']
        endDate = zarCalendar.AdjustBankingDays(startDate, 1)
        slInstrument = acm.FSecurityLoan()
        slInstrument.RegisterInStorage()
        slInstrument.Quotation('Clean')
        slInstrument.QuoteType('Clean')
        #referencePrice = prices.GetPrice(underlying)
        quotationFactor = slInstrument.Quotation().QuotationFactor()
        #rate = rates.GetRate(underlying, external, applySpread)

        if referencePrice == 0:
            raise Exception('Security Loan [%(slInstrument)s] cannot have a zero reference price [%(underlying)s].' % {'slInstrument': slInstrument.Name(), 'underlying': underlying.Name()})
        if quotationFactor == 0:
            raise Exception('Security Loan cannot have a zero quotation factor: ' + slInstrument.Name())

        acm.BeginTransaction()
        try:
            slInstrument.StartDate(startDate)
            slInstrument.OpenEnd(openEnd)
            slInstrument.UnderlyingType(underlying.InsType())
            slInstrument.Underlying(underlying)
            slInstrument.RefPrice(referencePrice)
            slInstrument.RefValue(slInstrument.ContractSize() / (slInstrument.RefPrice() * quotationFactor))
            slInstrument.ExpiryDate(endDate)
            slInstrument.SpotBankingDaysOffset(0)

            leg = slInstrument.CreateLeg(True)
            leg.StartDate(startDate)
            leg.EndDate(endDate)
            leg.LegType('Fixed')
            leg.DayCountMethod('Act/365')
            leg.FixedRate(rate)
            leg.PayCalendar(zarCalendar)
            leg.RollingPeriodBase(startDate)

            slInstrument.Commit()
            leg.Commit()
            
            slInstrument.AdditionalInfo().SL_ExternalInternal(Position.InternalExternal[external])
            slInstrument.AdditionalInfo().SL_SweepingBatchNo(batchNumber)
            slInstrument.AdditionalInfo().SL_CFD(bookCfd)
            slInstrument.AdditionalInfo().SL_VAT(False)

            acm.CommitTransaction()
        except Exception, ex:
            acm.AbortTransaction()
            raise Exception('Security Loan was not created: ' + str(ex))

        return slInstrument

    @classmethod
    def bookSecurityLoan(cls, batchNumber, openEnd, acquirerPortfolio, instrument, quantity, startDate, counterpartyPortfolio, external, rate, referencePrice, bookCfd):
        quantity = float(quantity)
        instrument = cls.createAndCommitSecurityLoan(batchNumber, openEnd, instrument, startDate, quantity, external, rate, referencePrice, bookCfd)
        refValue = instrument.RefValue()
        tradeTime = min(startDate, acm.Time.DateToday())
        if refValue == 0:
            raise Exception('Security Loan cannot have a zero reference value: ' + instrument.Name())

        trade = acm.FTrade()
        trade.Instrument(instrument)
        trade.Currency(instrument.Currency())
        trade.TradeTime(tradeTime)
        trade.Acquirer(acquirerPortfolio.PortfolioOwner())
        trade.Portfolio(acquirerPortfolio)
        trade.Counterparty(counterpartyPortfolio.PortfolioOwner())
        trade.AcquireDay(startDate)
        trade.ValueDay(startDate)
        trade.Quantity(quantity / refValue)
        trade.HaircutType('Discount')
        trade.Status('BO Confirmed')
        trade.Type('PL Sweep')
        trade.MirrorPortfolio(counterpartyPortfolio)
        trade.Trader(acm.User())
        trade.Commit()

        return trade.Oid()

    def Cover(self, log, batchNumber, shortPositions, coverDate, thirdPositionsToAdjust, validationMode, rates, prices, applySpread=False, allowPartialSweeping=False, isCfdSweep=False, allocateHeldPositions=False, specificInstruments=None):
        try:
            for instrument in self.Instruments():
                if specificInstruments:
                    if not instrument.Name() in specificInstruments:
                        continue
                
                referencePrice = prices.GetPrice(instrument)
                if _isZero(referencePrice):
                    log.Warning('Instrument {0} will not be swept as there is'\
                                ' no price defined for it.' \
                                .format(instrument.Name()))
                    continue

                instrumentLongPositions = self.GetPositionsForInstrument(instrument)
                instrumentShortPositions = shortPositions.GetPositionsForInstrument(instrument)
                totalLongPosition = instrumentLongPositions.GetQuantity(instrument)
                totalShortPosition = instrumentShortPositions.GetQuantity(instrument) * -1
                allocateHeld = allocateHeldPositions and not rates.CanAutoReturn(instrument)
                if totalLongPosition > 0 and totalShortPosition > 0:

                    if instrumentLongPositions._hasExternalPosition() and not rates.HasExternalRate(instrument):
                        log.Warning(rates.NoExternalRateMessage(instrument) + (': Short of %f will not be covered.' % totalShortPosition))
                        continue

                    available = totalShortPosition
                    if totalLongPosition < totalShortPosition or allocateHeld:
                        available = totalLongPosition
                        if round(totalLongPosition, 7) < round(totalShortPosition, 7):
                            log.Warning('Long position of %(long)f is not enough to cover a short of %(short)f for instrument %(instrument)s. %(instrument)s will not be swept.' % \
                                {'long': totalLongPosition, 'short': totalShortPosition, 'instrument': instrument.Name()})
                    
                    if allowPartialSweeping or totalLongPosition >= totalShortPosition:
                        log.Information('Covering short position of | %(short)f | for %(instrument)s: ' \
                            % {'short': shortPositions.GetQuantity(instrument), 'instrument': instrument.Name()})
                        for longPosition in instrumentLongPositions:
                            if longPosition.quantity > 0:
                                availableLong = longPosition.quantity / totalLongPosition * available
                                availableLong = min(available, longPosition.quantity, availableLong)
                                totalShortPosition = instrumentShortPositions.GetQuantity(instrument) * -1
                                if totalShortPosition > 0 or allocateHeld:
                                    for shortPosition in instrumentShortPositions:
                                        shortQuantity = shortPosition.quantity * -1
                                        coverQuantity = decimal.Decimal(str(math.ceil(shortQuantity / totalShortPosition * availableLong)))
                                        coverQuantity = min(coverQuantity, shortQuantity, longPosition.quantity)

                                        if not validationMode and round(coverQuantity, 7) != 0.0:
                                            if (shortPosition.portfolio.AdditionalInfo().SL_Zero_Fees() or 
                                                longPosition.portfolio.AdditionalInfo().SL_Zero_Fees()):
                                                rate = 0
                                            else:
                                                rate = rates.GetRate(instrument, longPosition.external, applySpread)
                                            
                                            openEnd = "None"
                                            try:
                                                trdnbr = self.bookSecurityLoan(batchNumber, openEnd, shortPosition.portfolio, instrument, coverQuantity, coverDate, longPosition.portfolio, longPosition.external, rate, referencePrice, isCfdSweep)
                                            except Exception as e:
                                                log.Warning('Failed to book loan: {0}'.format(str(e)))
                                                continue
                                            log.Information(("Trade: %(trdnbr)10i | borrowing: %(coverQuantity)15.0f | " \
                                                             "for: [%(shortPortfolio)s] | from: [%(longPortfolio)s].") \
                                                             % {'trdnbr': trdnbr, 
                                                                'coverQuantity': coverQuantity,
                                                                'shortPortfolio': shortPosition.portfolio.Name(),
                                                                'longPortfolio': longPosition.portfolio.Name()})
                                        elif validationMode:
                                            self._validateRateAndPrice(instrument, longPosition.external, applySpread, rates, prices, log)
                                        self.Add(longPosition.portfolio, longPosition.instrument, -coverQuantity, longPosition.external)
                                        shortPositions.Add(shortPosition.portfolio, shortPosition.instrument, coverQuantity, shortPosition.external)
                                        if thirdPositionsToAdjust != None:
                                            thirdPositionsToAdjust.Add(shortPosition.portfolio, shortPosition.instrument, coverQuantity, shortPosition.external)
        except Exception, ex:
            log.RaiseException('Exception in PositionCollection.Cover: ' + str(ex), not validationMode)


class SblSweeper:
    
    def __init__(self, sweepDate, tradeFilter, sblPortfolio, isCfdSweep, log, 
                 validationMode, partialSweeping, sl_rates,
                 allocateHeldPositions=False, specificInstruments=None):
        self._validatePortfolioWithException(sblPortfolio)
        self.sweepDate = sweepDate
        self.tradeFilter = tradeFilter
        self.sblPortfolio = sblPortfolio
        self._isCfdSweep = isCfdSweep
        self._deskFeePortfolios = {}
        self._rates = sl_rates
        self._prices = SblPrices(sweepDate)
        self._log = log
        self._validationMode = validationMode
        self._partialSweeping = partialSweeping
        self._allocateHeldPositions = allocateHeldPositions
        self._specificInstruments = specificInstruments

        self.shortPositions = PositionCollection()
        self.longPositions = PositionCollection()
        self.sblPositions = PositionCollection()

    def _getDeskFeePortfolio(self, tradingDesk):
        if len(self._deskFeePortfolios) == 0:
            query = acm.CreateFASQLQuery('FPhysicalPortfolio', 'AND')
            op = query.AddOpNode('AND')
            op.AddAttrNode('AdditionalInfo.SL_Portfolio_Type', 'EQUAL', 'Fee')
            op.AddAttrNode('AdditionalInfo.SL_AllocatedDesk', 'NOT_EQUAL', None)
            op.AddAttrNode('AdditionalInfo.SL_Sweeping', 'EQUAL', True)
            for portfolio in query.Select():
                self._deskFeePortfolios[portfolio.AdditionalInfo().SL_AllocatedDesk()] = portfolio
        if self._deskFeePortfolios.has_key(tradingDesk):
            return self._deskFeePortfolios[tradingDesk]
        else:
            return None

    @staticmethod
    def _getQuantity(object):
        if _isNumber(object):
            return decimal.Decimal(str(object))
        else:
            try:
                tObject = object[0]
                return SblSweeper._getQuantity(tObject)
            except Exception, ex:
                return None

    def _validatePortfolioWithException(self, portfolio):
        owner = portfolio.PortfolioOwner()
        if owner:
            ownerType = owner.Type()
            if  ownerType != 'Intern Dept':
                raise Exception("Portfolio [%(portfolio)s], owned by [%(owner)s] of type [%(ownerType)s], is not valid. It is not owned by an internal department. The portfolio owner must be of type 'Intern Dept'" % \
                    {'portfolio': portfolio.Name(), 'owner': owner.Name(), 'ownerType': ownerType})
        else:
            raise Exception("Portfolio [%s] is not valid, since it has no owner." % portfolio.Name())

    def _buildPositions(self):
        portfolioGrouper = acm.FAttributeGrouper('Trade.Portfolio')
        underlyingGrouper = acm.FAttributeGrouper('Instrument.SLUnderlying')
        internalExternalGrouper = acm.FAttributeGrouper('Instrument.AdditionalInfo.SL_ExternalInternal')
        tradingDeskGrouper = acm.FAttributeGrouper('Trade.Portfolio.AdditionalInfo.SL_AllocatedDesk')
        calc_space = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), 'FPortfolioSheet')
        calc_space.SimulateGlobalValue('Portfolio Profit Loss Start Date', 'Inception')
        calc_space.SimulateGlobalValue('Portfolio Profit Loss End Date', 'Custom Date')
        calc_space.SimulateGlobalValue('Portfolio Profit Loss End Date Custom', self.sweepDate)

        top_node = calc_space.InsertItem(self.tradeFilter)
        top_node.ApplyGrouper(acm.FChainedGrouper([tradingDeskGrouper, underlyingGrouper, portfolioGrouper]))
        sbl_node = calc_space.InsertItem(self.sblPortfolio)
        sbl_node.ApplyGrouper(acm.FChainedGrouper([internalExternalGrouper, underlyingGrouper]))
        calc_space.Refresh()

        positionColumn = 'SL Portfolio Position'
        priceColumn = 'SL Avg Ref Price'
        time_buckets = acm.Time.CreateTimeBuckets(self.sweepDate, "'0d'", None, None, 0, True, False, False, False, False)
        column_config = acm.Sheet.Column().ConfigurationFromTimeBuckets(time_buckets)

        tempPositions = PositionCollection()
        deskIterator = top_node.Iterator().FirstChild()
        while deskIterator:
            desk = deskIterator.Tree().Item().StringKey()
            deskPortfolio = self._getDeskFeePortfolio(desk)
            if deskPortfolio != None:
                self._validatePortfolioWithException(deskPortfolio)
                deskPortfolioNode = calc_space.InsertItem(deskPortfolio)
                deskPortfolioNode.ApplyGrouper(acm.FChainedGrouper([underlyingGrouper]))
                calc_space.Refresh()
                instrumentIterator = deskIterator.Clone().FirstChild()
                while instrumentIterator:
                    instrument = acm.FInstrument[instrumentIterator.Tree().Item().StringKey()]
                    if not self._specificInstruments or instrument.Name() in self._specificInstruments:
                        deskPortfolioPosition = deskPortfolioNode.Iterator().Find(instrument)
                        if deskPortfolioPosition:
                            readQuantity = calc_space.CreateCalculation(deskPortfolioPosition.Tree(), positionColumn, column_config).Value()
                            quantity = SblSweeper._getQuantity(readQuantity)
                            if quantity:
                                tempPositions.Add(deskPortfolio, instrument, quantity, False)
                        portfolioIterator = instrumentIterator.Clone().FirstChild()
                        while portfolioIterator:
                            portfolio = acm.FPhysicalPortfolio[portfolioIterator.Tree().Item().StringKey()]
                            if portfolio.AdditionalInfo().SL_Sweeping() == True and portfolio.AdditionalInfo().SL_Portfolio_Type() == 'Equity':
                                readQuantity = calc_space.CreateCalculation(portfolioIterator.Tree(), positionColumn, column_config).Value()
                                quantity = SblSweeper._getQuantity(readQuantity)
                                if quantity == None:
                                    self._log.Warning('Position [%(quantity)s] for portfolio [%(portfolio)s], instrument [%(instrument)s] ignored.' \
                                        % {'portfolio': portfolio.Name(), 'instrument': instrument.Name(), 'quantity': str(readQuantity)})
                                elif portfolio.AdditionalInfo().SL_ReservedStock() != True or quantity < 0:
                                    tempPositions.Add(deskPortfolio, instrument, quantity, False)
                            portfolioIterator = portfolioIterator.NextSibling()
                    instrumentIterator = instrumentIterator.NextSibling()
            else:
                message = 'No Fee portfolio found for trading desk [%(desk)s].' % {'desk': desk}
                self._log.Warning(message)

            deskIterator = deskIterator.NextSibling()

        for position in tempPositions:
            if position.quantity < 0 and round(position.quantity, 7) != 0.0:
                self.shortPositions.Add(position.portfolio, position.instrument, position.quantity, position.external)
            elif position.quantity > 0 and round(position.quantity, 7) != 0.0:
                self.longPositions.Add(position.portfolio, position.instrument, position.quantity, position.external)

        tempPositions = PositionCollection()
        externalInternalIterator = sbl_node.Iterator().FirstChild()
        while externalInternalIterator:
            # treat all other choice list possibilities (No Collateral & Equity Collateral) as external
            external = True
            sl_ExternalInternal = externalInternalIterator.Tree().Item().StringKey()
            if sl_ExternalInternal == 'Internal':
                external = False
            instrumentIterator = externalInternalIterator.Clone().FirstChild()
            while instrumentIterator:
                instrument = acm.FInstrument[instrumentIterator.Tree().Item().StringKey()]
                if not self._specificInstruments or instrument.Name() in self._specificInstruments:
                    quantity = SblSweeper._getQuantity(calc_space.CreateCalculation(instrumentIterator.Tree(), positionColumn, column_config).Value())
                    if quantity != None and quantity != 0:
                        tempPositions.Add(self.sblPortfolio, instrument, quantity, external)
                        if (not self._isCfdSweep) and sl_ExternalInternal == 'External':
                            price = calc_space.CalculateValue(instrumentIterator.Tree(), priceColumn)
                            if _isNumber(price):
                                self._prices.Add(instrument, price)
                instrumentIterator = instrumentIterator.NextSibling()
            externalInternalIterator = externalInternalIterator.NextSibling()
        
        # filtering can't be done while iterating, because there might be some 
        # External qty, some No Collateral qty and we need to see how it adds
        # up in total
        for position in tempPositions:
            if position.quantity > 0 and round(position.quantity, 7) != 0.0:
                self.sblPositions.Add(position.portfolio, position.instrument, position.quantity, position.external)

        self._log.Information("Short Positions")
        self._log.Information(str(self.shortPositions))
        self._log.Information("Long Positions")
        self._log.Information(str(self.longPositions))
        self._log.Information("SBL Positions")
        self._log.Information(str(self.sblPositions))
        
        

    def _addPositionsToAllocateHeldInstruments(self):
        shortPortfolios = self.shortPositions.GetDistinctPortfolios()
        if not shortPortfolios:
            self._log.Warning('No portfolios to allocate held postions to.')
            return

        for instrument in self.sblPositions.Instruments():
            held = not self._rates.CanAutoReturn(instrument)
            if not held:
                continue

            shortPositions = self.shortPositions.GetPositionsForInstrument(instrument)
            if shortPositions:
                continue

            positions = self.longPositions.GetPositionsForInstrument(instrument)
            longPortfolios = positions.GetDistinctPortfolios()

            for position in positions:
                if position.portfolio not in shortPortfolios:
                    positions.RemovePosition(position)

            for portfolio in shortPortfolios:
                if portfolio not in longPortfolios:
                    positions.Add(portfolio, instrument, 0, False)

            quantityHeld = self.sblPositions.GetQuantity(instrument)
            haveAllPositionsToAllocate = False
            totalQuantity = 0
            quantityPerPortfolio = 0
            while not haveAllPositionsToAllocate and positions:
                totalQuantity = quantityHeld + positions.GetQuantity(instrument)
                quantityPerPortfolio = _toDecimal(math.ceil(totalQuantity / len(positions)))
                removed = False

                for position in positions:
                    if position.quantity > quantityPerPortfolio:
                        positions.RemovePosition(position)
                        removed = True

                if not removed:
                    haveAllPositionsToAllocate = True

            totalQuantity = _toDecimal(totalQuantity)
            for position in positions:
                quantityToAllocate = quantityPerPortfolio - position.quantity
                self.shortPositions.Add(position.portfolio, instrument, quantityToAllocate * -1, False)
                totalQuantity -= quantityToAllocate
                quantityPerPortfolio = min(totalQuantity, quantityPerPortfolio)

    def _borrowInternallyForSblPortfolio(self, batchNumber):
        try:
            self._log.Information('SBL Sweeping: Borrowing from internal portfolios')
            positionsToBorrow = PositionCollection()
            for instrument in set(self.shortPositions.Instruments() + self.sblPositions.Instruments()):
                shortPosition = self.shortPositions.GetQuantity(instrument)
                sblPosition = self.sblPositions.GetQuantity(instrument)
                if shortPosition < 0:
                    quantityToCover = sblPosition + shortPosition
                else:
                    quantityToCover = sblPosition
                if quantityToCover < 0:
                    positionsToBorrow.Add(self.sblPortfolio, instrument, quantityToCover, False)
            if len(positionsToBorrow) > 0:
                applySpread = False
                self.longPositions.Cover(self._log, batchNumber, positionsToBorrow, self.sweepDate, self.sblPositions, self._validationMode, self._rates, self._prices, applySpread, self._partialSweeping, self._isCfdSweep, specificInstruments=self._specificInstruments)
        except Exception, ex:
            self._log.RaiseException('Exception while borrowing for SBL portfolio: ' + str(ex), not self._validationMode)

    def _coverPositions(self, batchNumber):
        try:
            applySpread = True
            self._log.Information('SBL Sweeping: Lending from SBL portfolio')
            self.sblPositions.Cover(self._log, batchNumber, self.shortPositions, self.sweepDate, None, self._validationMode, self._rates, self._prices, applySpread, self._partialSweeping, self._isCfdSweep, self._allocateHeldPositions, specificInstruments=self._specificInstruments)
        except Exception, ex:
            self._log.RaiseException('Exception while covering positions: ' + str(ex), not self._validationMode)

    def Sweep(self):
        batch = None
        batchNumber = None
        try:
            self._log.Information('CFD Sweep: ' + _boolToStr(self._isCfdSweep))
            self._log.Information('Sweep Date: ' + str(self.sweepDate))
            self._log.Information('Positions Filter: ' + self.tradeFilter.Name())
            self._log.Information('Specific instruments: ' + ','.join(self._specificInstruments))
            self._log.Information('SBL Portfolio: ' + self.sblPortfolio.Name())
            self._log.Information('Validation Mode: ' + _boolToStr(self._validationMode))
            self._log.Information('Allow Partial Sweeping: ' + _boolToStr(self._partialSweeping))
            self._log.Information('Allocate Held Positions: ' + _boolToStr(self._allocateHeldPositions))
            self._log.Information('Internal Rate: ' + str(self._rates.InternalRate))
            self._log.Information('Internal Spread: ' + str(self._rates.InernalSpread))
            self._log.Information('Buy Spread: ' + str(self._rates.BuySpread))
            self._log.Information('Sell Spread: ' + str(self._rates.SellSpread))

            self._buildPositions()
            if self._allocateHeldPositions:
                self._addPositionsToAllocateHeldInstruments()

            if not self._validationMode:
                batch = SblSweepBatch.CreateBatch(self.sweepDate)
                batchNumber = batch.BatchNumber

            self._borrowInternallyForSblPortfolio(batchNumber)
            self._coverPositions(batchNumber)

        except Exception, ex:
            if batch:
                batch.VoidBatch(self._log)
            self._log.Exception(str(ex))
        else:
            if batch:
                self._log.Information('Sweeping batch [%i] completed successfully.' % batch.BatchNumber)
            else:
                self._log.Information('The process completed successfully. No sweeping batch was created.')
        finally:
            if self._validationMode:
                if self._log.HasErrors():
                    self._log.Warning('The validation returned problems, please review the log messages and correct them before running the sweeping process.')
                else:
                    self._log.Information('The validation returned without problems, the sweeping process can be run.')

