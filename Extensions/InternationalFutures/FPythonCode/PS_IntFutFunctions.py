import acm
import ael
import re




def nonZarCallAccType(instrument):
    if instrument.ExternalId1().upper().endswith('LOCAL'):
        return 'LOCAL'
    elif instrument.ExternalId1().upper().endswith('BASE'):
        return 'BASE'
    return None

def GetMTMLeg(instrument, portfolioSwap):
    instrumentLegs = [leg for leg in portfolioSwap.Legs() if leg.IndexRef() == instrument and leg.LegType() == 'Total Return']
    if len(instrumentLegs) == 0:
        raise ValueError('No MTM leg data in portfolio swap for instrument %s' % instrument.Name())
    if len(instrumentLegs) != 1:
        raise ValueError('Ambiguous MTM leg data in portfolio swap for instrument %s' % instrument.Name())
    return instrumentLegs[0]


def GetFwdDatedCash(callAccount, date):
    amount = sum([cf.FixedAmount() for cf in callAccount.Legs()[0].CashFlows() if ((cf.PayDate() > date) and cf.CashFlowType() not in ('Call Fixed Rate Adjustable', 'Redemption Amount') and cf.add_info('PS_IntFutTradeDate') and cf.add_info('PS_IntFutTradeDate') <= date)])
    return acm.DenominatedValue(amount, callAccount.Currency(), date)

def GetMTMCashflow(instrument, portfolioSwap, cfType):
    mTMLeg = GetMTMLeg(instrument, portfolioSwap)
    cfs = [cf for cf in mTMLeg.CashFlows() if cf.AdditionalInfo().PS_FundWarehouse() == cfType]
    if len(cfs) > 1:
        raise ValueError('Ambiguous MTM cashflow data in portfolio swap for instrument %s %s' % (instrument.Name(), cfType))
    elif len(cfs) == 0:
        return None
    return cfs[0]

def ParentPortfolio(trade):
    links = acm.FPortfolioLink.Select('memberPortfolio = %s'% trade.Portfolio().Name())
    if len(links):
        return links[0].OwnerPortfolio()
    return None

def PSwapMTMAsOf(instrument, portfolioSwap, myDate):
    return GetPnLReset(instrument, portfolioSwap, myDate, 'UPL')

def PSwapRPLAsOf(instrument, portfolioSwap, myDate):
    return GetPnLReset(instrument, portfolioSwap, myDate, 'RPL')

def GetPnLReset(instrument, portfolioSwap, myDate, cfType):
    leg = GetMTMLeg(instrument, portfolioSwap)
    cashflow = GetMTMCashflow(instrument, portfolioSwap, cfType)
    if cashflow:
        daysResets = [reset for reset in cashflow.Resets() if reset.EndDate() >= myDate and reset.StartDate() <= myDate and reset.ResetType() == 'Return']
        if len(daysResets) > 1:
            raise ValueError('Check MTM reset data in portfolio swap for instrument %s for date %s' % (instrument.Name(), myDate))
        elif len(daysResets) == 0:
            return acm.DenominatedValue(0, leg.Currency(), None)
        return acm.DenominatedValue(daysResets[0].FixingValue(), daysResets[0].Leg().Currency(), None)
    return acm.DenominatedValue(0, leg.Currency(), None)

def PSwapTPLBetween(instrument, portfolioSwap, fromDate, toDate):
    if fromDate > toDate:
        raise ValueError('TPL period size negative: start %s end %s'%(fromDate, toDate))
    cashflow = GetMTMCashflow(instrument, portfolioSwap, 'UPL')
    rplTotal = RPLTotalBetween(instrument, portfolioSwap, fromDate, toDate)
    if cashflow:
        try:
            uplDiff = PSwapMTMAsOf(instrument, portfolioSwap, toDate) - PSwapMTMAsOf(instrument, portfolioSwap, fromDate)
            retVal = uplDiff + rplTotal
            return retVal
        except ValueError:
            acm.Log('MTM data for %s in PSwap %s for period %s to %s appears ambiguous. Please correct. Displaying RPL only.')
            return rplTotal
    else:
        return rplTotal

def DatesBetween(fromDate, toDate):
    currDate = fromDate
    while currDate <= toDate:
        yield currDate
        currDate = acm.Time().DateAddDelta(currDate, 0, 0, 1)

def RPLTotalBetween(instrument, portfolioSwap, fromDate, toDate):
    leg = GetMTMLeg(instrument, portfolioSwap)
    total = acm.DenominatedValue(0, leg.Currency(), None)
    for date in DatesBetween(fromDate, toDate):
        total += PSwapRPLAsOf(instrument, portfolioSwap, date)
    total -= PSwapRPLAsOf(instrument, portfolioSwap, fromDate)
    return total

def GetCallAccountCashflowsByPSCashType(callAccount, cashTypes, fromDate, toDate):
    outFlows = []
    leg = callAccount.Legs()[0]
    #this should fix cashflows appearing 2 consecutive days
    fromDate = min(acm.Time.DateAddDelta(fromDate, 0, 0, 1), toDate)
    for cashFlow in leg.CashFlows():
    #check if date falls between the two dates
    #if it's greater than one date and smaller than the other
    #then the product of the differences is negative
        if acm.Time.DateDifference(fromDate, cashFlow.PayDate()) * \
           acm.Time.DateDifference(toDate, cashFlow.PayDate()) <= 0 and \
           cashFlow.add_info('PSCashType') in cashTypes:
            outFlows.append(cashFlow)

    return outFlows

def GetCallAccountNonZARFees(callAccount, fromDate, toDate):
    ''' Modified code from ABSAPSSweep
    '''
    total = 0
    feeFlows = GetCallAccountCashflowsByPSCashType(callAccount, ['NONZAR_FEES'], fromDate, toDate)

    for cashFlow in feeFlows:
        total = total + cashFlow.FixedAmount()

    return acm.DenominatedValue(total, callAccount.Currency(), toDate)

def GetCallAccountNonZARCarry(callAccount, date):
    tspec = acm.FTimeSeriesSpec['PS_MTDInterest_IFut']
    query = "recaddr=%i and timeSeriesSpec=%i and day=%s" % (
        callAccount.Oid(), tspec.Oid(), date)
    time_series = acm.FTimeSeries.Select01(query, '')
    if time_series:
        # Front Upgrade 2013.3 -- Value() changed to TimeValue(), semantics changed between versions
        return time_series.TimeValue()
    return 0.0

def convertDateToISO(date):
    """ Converts DD/MM/YYYY to ISO date YYYY-MM-DD
    """
    if re.search("^[0-9]{2}/[0-9]{2}/[0-9]{4}$", date):
        date = date[6:10] + "-" + date[3:5] + "-" + date[0:2]
    else:
        raise ValueError("Incorrect date format")
    return date


def GetLastFxRate_asql(curr, date, market):
    currOid = curr.Oid()
    marketOid = market.Oid()

    baseCurrOid = acm.FCurrency['USD'].Oid()

    if re.search("^[0-9]{2}/[0-9]{2}/[0-9]{4}$", date):
        date = convertDateToISO(date)

    if re.search("^[0-9]{4}-[0-9]{2}-[0-9]{2}$", date) \
    or re.search("^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}$", date):
        Query = acm.CreateFASQLQuery(acm.FPrice, 'AND')
        Query.AddAttrNode('Instrument.Oid', 'EQUAL', currOid)
        Query.AddAttrNode('Market.Oid', 'EQUAL', marketOid)
        Query.AddAttrNode('Currency.Oid', 'EQUAL', baseCurrOid)
        Query.AddAttrNode('Day', 'LESS_EQUAL', date)
        validPrices = Query.Select().SortByProperty('Day', False) # False = descending
        if validPrices:
            lastValidPrice = validPrices[0]
            return lastValidPrice.Settle()
        else:
            return None
    else:
        raise ValueError("Incorrect date format")

def AdjustFxRateSpot(curr, date):
    calendar = curr.Calendar()
    return calendar.AdjustBankingDays(date, curr.SpotBankingDaysOffset())

def GetIntFutFxRate(curr1, curr2, date):
    ''' Improvising a function for fx rate
    '''
    if not curr1.IsKindOf(acm.FCurrency)\
        or not curr2.IsKindOf(acm.FCurrency)\
        or not date:
        return None

    if curr1 == curr2:
        return acm.DenominatedValue(1, curr2, AdjustFxRateSpot(curr2, date))

    baseCurrId = 'USD'
    baseCurr = acm.FCurrency[baseCurrId]
    market = acm.FParty['INT_FUT']
    try:
        if curr1.Name() != baseCurr.Name():
            fxRate = GetLastFxRate_asql(curr1, date, market)
            if fxRate:
                fxRateCurr1 = fxRate
            else:
                raise RuntimeError("Fx rate for curr %s vs %s does not exist"
                        % (curr1.Name(), baseCurrId))
        else:
            fxRateCurr1 = 1

        if curr2.Name() != baseCurr.Name():
            fxRate = GetLastFxRate_asql(curr2, date, market)
            if fxRate:
                fxRateCurr2 = 1/fxRate
            else:
                raise RuntimeError("Fx rate for curr %s vs %s does not exist"
                        % (curr2.Name(), baseCurrId))
        else:
            fxRateCurr2 = 1

        if fxRateCurr1 and fxRateCurr2:
            rate = fxRateCurr2 * fxRateCurr1
            # + spot offset curr2 calendar adjust
            return acm.DenominatedValue(rate, curr2, AdjustFxRateSpot(curr2, date))
        else:
            return None
    except Exception as e:
        import traceback
        traceback.print_exc()
        print("Fx Rate fetch failed: %s" % str(e))
        return None



PSCashTypeFor = {
                'grossPnl': ['GROSS_PROFIT_AND_LOSS'],
                'fees': ['TOTAL_COMMISSIONS_AND_FEES', 'COMMISSIONS_AND_FEES', 'POSTED_OPTION_PREMIUM'],
                'capitalisedInterest': [],
                'cashPosting': ['CASH_POSTED'],
                'fwdDatedCash': ['FORWARD_DATED_CASH'],
                'adjustments': ['ADJUSTMENTS'],
                #'NONZAR_FEES'         : ['NONZAR_FEES'],
                }


def CallAcc_SumCFsWithPSCashTypeForDate(instrument, PSCashType, pnlStartDate, pnlEndDate):
    cashFlows = GetCallAccountCashflowsByPSCashType(instrument, PSCashTypeFor[PSCashType], pnlStartDate, pnlEndDate)
    totalAmount = 0
    for cf in cashFlows:
        totalAmount += cf.FixedAmount()
    return acm.DenominatedValue(totalAmount, instrument.Currency(), pnlEndDate)


def CallAccCapitalisedInterest(instrument, pnlStartDate, pnlEndDate):
    return CallAcc_SumCFsWithPSCashTypeForDate(instrument, 'capitalisedInterest', pnlStartDate, pnlEndDate)

def CallAccCashPostings(instrument, pnlStartDate, pnlEndDate):
    return CallAcc_SumCFsWithPSCashTypeForDate(instrument, 'cashPosting', pnlStartDate, pnlEndDate)

def CallAccAdjustments(instrument, pnlStartDate, pnlEndDate):
    return CallAcc_SumCFsWithPSCashTypeForDate(instrument, 'adjustments', pnlStartDate, pnlEndDate)

def CallAccGrossPnL(instrument, pnlStartDate, pnlEndDate):
    return CallAcc_SumCFsWithPSCashTypeForDate(instrument, 'grossPnl', pnlStartDate, pnlEndDate)

def CallAccBarclaysFees(instrument, pnlStartDate, pnlEndDate):
    return CallAcc_SumCFsWithPSCashTypeForDate(instrument, 'fees', pnlStartDate, pnlEndDate)


def CallAccSundryCharges(instrument, pnlStartDate, pnlEndDate):
    totalSundry = 0
    otherRowTypes = [str(item) for sublist in PSCashTypeFor.values() for item in sublist]
    pnlStartDate = min(acm.Time.DateAddDelta(pnlStartDate, 0, 0, 1), pnlEndDate)
    for cf in instrument.Legs()[0].CashFlows():
        #check if date falls between the two dates
        #if it's greater than one date and smaller than the other
        #then the product of the differences is negative
        if cf.CashFlowType() == 'Fixed Amount'\
        and acm.Time.DateDifference(pnlStartDate, cf.PayDate()) * \
            acm.Time.DateDifference(pnlEndDate, cf.PayDate()) <= 0:
            if not cf.add_info('PSCashType') or cf.add_info('PSCashType') in otherRowTypes:
                # will be part of another row
                pass
            else:
                #print cf.Oid(), cf.FixedAmount()
                totalSundry += cf.FixedAmount()

    return acm.DenominatedValue(totalSundry, instrument.Currency(), pnlEndDate)

