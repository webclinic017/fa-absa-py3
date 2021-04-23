""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/expiration/etc/FNewExpirationHelper.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
import acm
import ael


import FBDPCommon
import string
import FBDPInstrument
import FBDPCalculatePosition
import FNewExpirationUtility
import datetime

MAX_INS_NAME_LENGTH = FBDPCommon.getMaxNameLength(acm.FInstrument)

class _CPAndArchiveTrds(object):
    """
    Value object type containing an CP trades and
    its associated archiving trades.
    """

    def __init__(self, cpTrds, arcTrds):

        assert isinstance(arcTrds, list), (
            'The given archived trades must be a list, '
            'which contains a list of positions, but {0} is '
            'given'.format(arcTrds)
        )

        self.cpTrds = cpTrds
        self.arcTrds = arcTrds

class _GroupedTradesInPortfolio(object):
    def __init__(self, port):
        self.port = port
        self.trds = []
        self.groupedTrds = []

    def addTrades(self, trd):
        self.trds.append(acm.FTrade[trd])

    def applyGrouper(self, grouper):
        if self.port < 0:
            return

        calcSpace = acm.FCalculationSpace('FPortfolioSheet')
        topNode = calcSpace.InsertItem(acm.FPhysicalPortfolio[self.port])
        topNode.ApplyGrouper(grouper)
        calcSpace.Refresh()
        it = topNode.Iterator().FirstChild()
        self.groupedTrds = []
        while it:
            tree = it.Tree()
            item = tree.Item()
            trades = item.Trades().AsList()
            grpTrds = []
            for i in trades:
                if i in self.trds:
                    grpTrds.append(i)
            if grpTrds:
                self.groupedTrds.append(grpTrds)
            it = it.NextSibling()


class LiveInstTrds:
    def __init__(self, inst, log):
        self.log = log
        self.inst = inst
        self.isCSPinsChecked = {}

    def GetLiveTrdsAndGenerateCPTrds(self, execParam, genCP):
        ins = acm.FInstrument[self.inst]
        if ins is None:
            self.log.logError('No instrument found on id %d.' % self.inst)
            return []

        archiveInstrument = execParam.get('alsoArchiveInstrument', 0)
        ports = execParam.get('TradingPortfolios', [])
        filters = execParam.get('TradeFilter', [])
        trdQuery = execParam.get('TradeQuery', [])
        cpInst = execParam.get('cp_instrument')
        if cpInst:
            cpInst = cpInst[0]
        else:
            cpInst = None

        cpUnderlying = execParam.get('cp_in_underlying', 0)
        preservePL = execParam.get('preservePL', 1)

        grouper = execParam.get('PortfolioGrouper')
        if grouper:
            if grouper.IsKindOf(acm.FStoredPortfolioGrouper):
                grouper = grouper.Grouper()
            elif not grouper.IsKindOf(acm.FChainedGrouper):
                grouper = None
        else:
            grouper = None

        instInfo = self._getInstInfo(
            archiveInstrument, ins, ports, filters, trdQuery,
            grouper, cpInst, cpUnderlying
        )
        if instInfo is None:
            return []

        cpInst = instInfo[0]
        trdsPortfs = instInfo[1]
        if genCP == 0:  # No Need to Generate CP trades
            arcTrds = []
            for portId in list(trdsPortfs.keys()):
                for trd in trdsPortfs[portId].trds:
                    arcTrds.append(trd)
            return [(None, arcTrds)]
        else:
            cspTrades = []
            if genCP == 1:
                cspTrades = self._generateCPTrdFallBack(
                    ins, cpInst, list(trdsPortfs.keys()), preservePL, cpUnderlying
                )
            elif genCP == 2:
                # Generate CP trade in new CalcPosisiton interface
                cspTrades = self._generateCPTrd(
                    ins, cpInst, trdsPortfs, grouper, preservePL, cpUnderlying
                )

            return cspTrades

    def _generateCPTrdFallBack(
        self, inst, cpInst, portfs, preservePL, cpUnderlying
    ):

        calcPositions = self._calcInstPosition(inst)
        abort = False
        if calcPositions:
            try:
                # cashPost also checks if a trade in the position has
                # acquire_day after instrument exp_day. When this
                # happens CalculatePosition will be called again
                ignoreMsg, cspTrades = self._cashPost(inst,
                    calcPositions,
                    cpInst,
                    portfs, preservePL, cpUnderlying)
                if ignoreMsg:
                    self.log.logWarning(ignoreMsg)
                    abort = True
            except Exception as ex:
                abort = True
                errorMsg = str(ex)
                self.log.logError(errorMsg)

            if not abort:
                return cspTrades
            else:
                return []
        else:
            self.log.logInfo(
                'For instrument %s, No positions were found. '
                'No trades will be archived or cashposted.' % inst.Name()
            )
            return []

    def _checkValidTrdPosition(self, inst, posName, preservePL, calcResult):
        if inst.InsType() not in ('Option', 'Warrant', 'Future/Forward') or \
            not preservePL:
            return True

        useCurrencyDependency = len(calcResult[0]) > 1
        trdPosition = 0
        if useCurrencyDependency:
            for trd in calcResult[0]:
                trdPosition += trd.Quantity()
        else:
            trd = calcResult[0][0]
            trdPosition = trd.Quantity()

        if not FBDPCommon.eps_compare(trdPosition):
            self.log.logWarning('Non-Zero Position in %s.' % posName)
            return False

        return True

    def _generateCPTrd(
        self, inst, cpInst, trdsInPortf, grouper, preservePL, cpUnderlying
    ):
        csp_trades = []
        insExpiryDate = inst.ExpiryDate()
        expiryDate = datetime.datetime.strptime(inst.ExpiryDate()[:10],
                                                     '%Y-%m-%d').date()
        maxDate = datetime.datetime.max.date()
        openEndExpiry = (maxDate - expiryDate).days == 0
        try:
            for portId in list(trdsInPortf.keys()):
                lastAcquireDay = "1900-01-01"
                for trd in trdsInPortf[portId].trds:
                    tradeAcquireDay = trd.AcquireDay()
                    if lastAcquireDay < tradeAcquireDay:
                        lastAcquireDay = tradeAcquireDay

                cashPostingDay = insExpiryDate
                if insExpiryDate is None or lastAcquireDay > insExpiryDate:
                    cashPostingDay = lastAcquireDay
                elif openEndExpiry:
                    cashPostingDay = acm.Time.DateToday()
                calcPosOnGrouper = self._calculatePositionUsingGrouper(
                    inst, trdsInPortf[portId], grouper,
                    start_date=None, end_date=cashPostingDay,
                    showSummary=False, hookArguments=None, usePlClearDate=1
                )
                if calcPosOnGrouper.dirty:
                    errorMsg = calcPosOnGrouper.errMsg
                    self.log.logError(errorMsg)
                    return []

                port = acm.FPhysicalPortfolio[portId]
                # port = None is converted to 'None'.
                portName = str(port and port.Name())
                posName = "[%s:%s]" % (portName, inst.Name())

                for calcResult in calcPosOnGrouper:
                    if not self._checkValidTrdPosition(
                            inst, posName, preservePL, calcResult
                    ):
                        return []

                    dependencyTrds = calcResult[1]
                    useCurrencyDependency = len(calcResult[0]) > 1
                    for trd in calcResult[0]:
                        if not trd.Payments() and \
                           FBDPCommon.eps_compare(trd.AggregatePl()) and \
                           preservePL:
                            self.log.logInfo(
                                'position %s has no P/L.' % posName
                            )

                        if useCurrencyDependency:
                            dependencyTrds = []
                            for trade in calcResult[1]:
                                if trade.Currency() == trd.Currency():
                                    dependencyTrds.append(trade)

                        cspTrade, lastPayDay = self._createCSPTrade(
                            inst, portName, trd, cpInst,
                            preservePL, cpUnderlying
                        )
                        csp_trades.append([cspTrade, dependencyTrds])
        except Exception as ex:
            errorMsg = str(ex)
            self.log.logError(errorMsg)

        return csp_trades
        #return cspTrades

    def _getInstInfo(
        self, archiveInstrument, ins, ports, filters,
        trdQuery, grouper, cpInst, cpUnderlying
    ):
        if self._checkforFutureTrades(ins):
            self.log.logWarning(
                'Ignore the instrument %s , '
                'as it has a trade in the future.' % ins.Name()
            )
            return None

        cp = self._getCashPostingInstrument(ins, cpInst, cpUnderlying)
        trdPortfs = self._getPortTrades(
            archiveInstrument, ins, ports, filters, trdQuery, grouper
        )

        return (cp, trdPortfs)

    def _calcInstPosition(self, ins):
        calcPositions = None
        try:
            cashPostingDay = ins.ExpiryDate()
            if not cashPostingDay:
                # If live instruments are allowed
                cashPostingDay = acm.Time.DateToday()
            calcPositions = \
                    FBDPCalculatePosition.CalculatePosition(
                            ins,
                            end_date=cashPostingDay,
                            showSummary=False,
                            hookArguments=None,  # self.ael_variables_dict,
                            usePlClearDate=1)
            if calcPositions.dirty:
                errorMsg = calcPositions.errMsg
                self.log.logError(errorMsg)
                abort = True

        except Exception as ex:
            errorMsg = str(ex)
            self.log.logError(errorMsg)

        return calcPositions

    def _cashPost(
        self, ins, calcPositions, cpIns, ports, preservePL, cpUnderlying
    ):
        csp_trades = []
        for calcPos in calcPositions:
            calcTrades = calcPos[0]
            posTrades = calcPos[1]
            lastAcquireDay = "1900-01-01"
            for trade in posTrades:
                if lastAcquireDay < trade.AcquireDay():
                    lastAcquireDay = trade.AcquireDay()
            errMsg = 'Calculation of Position failed.'

            if preservePL:
                if ins.ExpiryDate() == None:
                    errMsg = (
                        'Recalculation of a position failed because '
                        'the expiry date has not been set'
                    )
                    # We have used wrong end_date in
                    # ins.calculate_position for this
                    # position, we need to call calculate_position again
                    calcTrades = self._recalculatePosition(
                        posTrades[0], lastAcquireDay
                    )
                else:
                    if lastAcquireDay > ins.ExpiryDate():
                        errMsg = (
                            'Recalculation of a position failed because '
                            'the acquire date (' + lastAcquireDay + ') is '
                            'after the expiry date (' + ins.ExpiryDate() + ')'
                        )
                        # We have used wrong end_date in
                        # ins.calculate_position for this
                        # position, we need to call calculate_position again
                        calcTrades = self._recalculatePosition(
                            posTrades[0], lastAcquireDay
                        )

            if not calcTrades:
                self.log.logError(
                    'No CalcTrades. error message = %s' % errMsg
                )
                return (errMsg, csp_trades)

            if len(calcTrades) > 1:
                useCurrencyDependency = True
            else:
                useCurrencyDependency = False

            port = calcTrades[0].Portfolio()
            # port = None is converted to 'None'.
            portName = str(port and port.Name())
            posName = "[%s:%s]" % (portName, ins.Name())
            for trd in calcTrades:
                if ports and trd.Portfolio().Oid() not in ports:
                    continue
                if not FBDPCommon.eps_compare(trd.Quantity()):
                    if preservePL and ins.InsType() in (
                            'Option', 'Warrant', 'Future/Forward'
                    ):
                        msg = 'Non-Zero Position in %s.' % posName
                        return (msg, csp_trades)
                if not trd.Payments() and preservePL and \
                   FBDPCommon.eps_compare(trd.AggregatePl()):
                    self.log.logInfo('Position %s has no P/L.' % posName)

                dependentTrades = []
                if useCurrencyDependency:
                    for trade in posTrades:
                        if trade.Currency() == trd.Currency():
                            dependentTrades.append(trade)
                else:
                    for trade in posTrades:
                        dependentTrades.append(trade)
                cspTrade, lastPayDay = self._createCSPTrade(
                    ins, portName, trd, cpIns, preservePL, cpUnderlying
                )
                csp_trades.append([cspTrade, dependentTrades])
        return ('', csp_trades)

    def _getPortTrades(
        self, archiveInstrument, ins, ports, filters, trdQuery, grouper
    ):
        trds = []
        instTrds = ins.Trades()
        allowed_trades = getattr(self, 'allowed_trades', None)
        if allowed_trades:
            instTrds = [
                trd for trd in instTrds if trd.Oid() in allowed_trades
            ]

        if archiveInstrument:
            trds = instTrds

        elif ports:
            for trd in instTrds:
                trade_port = trd.Portfolio()
                if trade_port and trade_port.Oid() in ports:
                    trds.append(trd)

        elif filters:
            for tradesSelect in filters:
                snapShot = tradesSelect.Snapshot()
                for trdSelected in snapShot:
                    if trdSelected in instTrds:
                        trds.append(trdSelected)

        elif trdQuery:
            raise Exception('Not implemented')

        else:
            trds = instTrds

        trdPortfs = {}
        for trade in trds:
            port = trade.Portfolio()
            if port:
                port_id = trade.Portfolio().Oid()
            else:
                continue

            if port_id not in trdPortfs:
                trdsPort = _GroupedTradesInPortfolio(port_id)
                trdsPort.addTrades(trade.Oid())
                trdPortfs[port_id] = trdsPort
            else:
                trdPortfs[port_id].addTrades(trade.Oid())

        if grouper:
            for portId in list(trdPortfs.keys()):
                trdPortfs[portId].applyGrouper(grouper)

        return trdPortfs

    def _getOrCreateCSPInstrument(self, cp_instrument):
        #Returns the cash posting instrument. Creates if not exists.
        if cp_instrument:
            return cp_instrument
        else:
            # Default name on the cash positing instrument
            CSP = 'CashPosting'
            CSP_EXTID1 = '##(Fastolph Smallburrows)##'
            CSP_EXTID2 = '##(of Sandydowns)##'

            insid = CSP
            ext_id1 = CSP_EXTID1
            ext_id2 = CSP_EXTID2
            text = 'For CashPosting'
            cp_loop = [
                (insid, 'name'),
                (ext_id1, 'externalId1'),
                (ext_id2, 'externalId2')
            ]
            for t, c in cp_loop:
                i = acm.FInstrument.Select("%s='%s'" % (c, t))
                if i:
                    i = i[0]
                    _ext_id1 = i.ExternalId1()
                    _ext_id2 = i.ExternalId2()
                    if ext_id1 not in self.isCSPinsChecked and not \
                       (_ext_id1 == ext_id1 and _ext_id2 == ext_id2):
                        i2 = i.Clone()
                        i2.ExternalId1 = ext_id1
                        i2.ExternalId2 = ext_id2
                        if not self.log.isInTestMode():
                            FBDPCommon.commit(i2, i)

                        self.log.summaryAddOk(
                            i2.RecordType(), i.Oid(), 'UPDATE'
                        )

                        #Summary().ok(i, Summary().UPDATE)
                        self.isCSPinsChecked[ext_id1] = None
                        acm.PollDbEvents()
                        return i2
                    else:
                        self.isCSPinsChecked[ext_id1] = None
                        return i

            i = acm.FFreeDefinedCashFlow()
            i.Name = insid
            i.ExternalId1 = ext_id1
            i.ExternalId2 = ext_id2
            i.ContractSize = 1.0
            i.SpotBankingDaysOffset = 0
            i.FreeText = text[:19]
            i.CreateLeg(False)
            FNewExpirationUtility.performCommit(i, self.log)

            self.log.summaryAddOk(i.RecordType(), i.Oid(), 'CREATE')
            self.isCSPinsChecked[ext_id1] = None
            acm.PollDbEvents()
            return i

    def _createCSPTrade(
        self, ins, prfid, cp, cp_instrument, preservePL, cpUnderlying
    ):
        """ Creates a CSP Trade. """
        last_pay_day = ael.date_from_time(0)
        insid = ins.Name()
        csp = ael.Instrument[cp_instrument.Oid()]
        t = ael.Trade[cp.Oid()].new()
        t.insaddr = csp
        t.aggregate = 1
        t.type = 'Cash Posting'
        if len(insid) > MAX_INS_NAME_LENGTH:
            t.text1 = insid[:MAX_INS_NAME_LENGTH - 1] + '$'
        if len(prfid) > MAX_INS_NAME_LENGTH:
            t.text2 = prfid[:MAX_INS_NAME_LENGTH - 1] + '$'
        else:
            t.text1 = insid
            t.text2 = prfid
        t.quantity = 0.0
        t.price = 0.0
        t.premium = 0.0

        if not preservePL:
            t.aggregate_pl = 0
            if t.payments():
                for p in t.payments():
                    FNewExpirationUtility.performDelete(p, self.log)

            return (t, last_pay_day)

        # t.acquire_day = t.value_day = ael.date_from_time(
        #     t.time
        # ).add_banking_day(csp.curr, csp.spot_banking_days_offset)
        for p in t.payments():
            ptype = p.type
            if ptype != 'Aggregated Funding' and ptype != 'Aggregated Settled':
                p.payday = ael.date_from_time(t.time)
            if p.payday > last_pay_day:
                last_pay_day = p.payday

        self.log.logDebug('Expired Instrument Type %s' % ins.InsType())
        if ins.InsType() == 'Option':
            self.log.logDebug(
                'Underlying instrument Type %s' % ins.UnderlyingType()
            )
            isFXOption = ins.UnderlyingType() == 'Curr'
            if isFXOption and cpUnderlying:
                # Underlying instrument currency (strike curr)
                aelIns = FBDPCommon.acm_to_ael(ins)
                strikeCurr = FBDPCommon.acm_to_ael(ins).strike_curr
                self.log.logDebug(
                    'Cash Posting Trade Currency is %s' % t.curr.display_id()
                )
                if not strikeCurr:
                    self.log.logWarning('Missing Strike Currency')
                else:
                    self.log.logDebug(
                        'Underlying Instrument Strike Currency is %s' % (
                            strikeCurr.display_id()
                        )
                    )
                # Strike currency is cash posting trade currency case.
                if strikeCurr.insaddr == t.curr.insaddr:
                    t.premium = t.aggregate_pl
                    t.aggregate_pl = 0
                # Underlying currency is cash posting trade currency
                elif aelIns.und_insaddr == t.curr:
                    t.quantity = t.aggregate_pl
                    t.aggregate_pl = 0
                #3 currency
                elif strikeCurr.insaddr != t.curr.insaddr:
                    pAggPlToPrem = ael.Payment.new(t)
                    pAggPlToPrem.valid_from = ael.date_from_time(t.time)
                    pAggPlToPrem.payday = t.value_day
                    pAggPlToPrem.curr = t.curr
                    pAggPlToPrem.amount = t.aggregate_pl
                    pAggPlToPrem.type = 'Premium'
                    t.aggregate_pl = 0

                # Only update the currency of the cash posting trade
                # when the strike currency is different
                # from the trading currency of the trade to be archived.
                if strikeCurr.insaddr != t.curr.insaddr:
                    t.curr = strikeCurr
                    self.log.logDebug('strikeCurr.insaddr != t.curr.insaddr')
                else:
                    self.log.logDebug('strikeCurr.insaddr = t.curr.insaddr')

        self._logSpotOffSetWarning(
            insid, ins.SpotBankingDaysOffset(), cp_instrument.Name(),
            cp_instrument.SpotBankingDaysOffset()
        )

        return (t, last_pay_day)

    def _recalculatePosition(self, depTrade, endDate):
        recalcCpTrades = \
                FBDPCalculatePosition.CalculatePosition(
                                              depTrade.Instrument(),
                                              start_date=None,
                                              end_date=endDate,
                                              portfolio=[depTrade.Portfolio()],
                                              usePlClearDate=1)
        for pos in recalcCpTrades:
            calcTrades = pos[0]
            dependentTrades = pos[1]
            for trade in dependentTrades:
                if depTrade.Oid() == trade.Oid():
                    return calcTrades
        return []

    def _calculatePositionUsingGrouper(
        self, i, trdsInPortf, grouper, start_date=None,
        end_date=acm.Time.DateToday(), showSummary=True, hookArguments={},
        usePlClearDate=1
    ):

        if not start_date:
            start_date = "1970-01-01"

        cp = FBDPCalculatePosition.CalcTrades([])
        useSelectedFundingDay = FBDPCommon.getUseSelectedFundingDay()
        trds = []
        if trdsInPortf.groupedTrds:
            trds = trdsInPortf.groupedTrds
        else:
            trds.append(trdsInPortf.trds)
        dic = i.CalculatePositionUsingGrouper(
            start_date, end_date, acm.FPhysicalPortfolio[trdsInPortf.port],
            trds, grouper, useSelectedFundingDay, usePlClearDate
        )

        cp = FBDPCalculatePosition.CalcTrades(dic["calculatedPositions"])
        cp = FBDPCalculatePosition.checkForDirtyPositions(cp, showSummary)

        return cp

    def _getCashPostingInstrument(self, ins, cpInst, cpUnderlying):
        cpInstrument = cpInst
        if cpUnderlying and ins.Underlying():
            #cpInstrument = None
            cpInstrument_tmp = ins.Underlying()
            if cpInstrument_tmp.Notional() and cpInstrument_tmp.Underlying():
                cpInstrument_tmp = cpInstrument_tmp.Underlying()
            if FBDPInstrument.isTradable(cpInstrument_tmp):
                cpInstrument = cpInstrument_tmp
            else:
                self.log.logWarning(
                    "Cash posting in the Underlying %s is not possible "
                    "as it isn't tradable. Using alternative instrument."
                    % cpInstrument_tmp.Name(), 'WARNING'
                )

        return self._getOrCreateCSPInstrument(cpInstrument)

    def _checkforFutureTrades(self, ins):
        simulatedExist = False
        for trade in ins.Trades():
            if trade.AcquireDay() > acm.Time.DateToday():
                return True
            if trade.Status() == 'Simulate':
                simulatedExist = True
        if simulatedExist:
            vp = acm.UsedValuationParameters()
            if vp.IncludeSimulatedTrades():
                msg = (
                    'Instrument %s has simulated trades and '
                    '"Include Simulated Trades" toggled in ValuationParameter'
                    '\nProfit and Loss may differ.' % ins.Name()
                )
                self.log.logWarning(msg)
        return False

    def _logSpotOffSetWarning(self, insName, insSpot, cpInsName, cpInsSpot):
        if insSpot != cpInsSpot:
            msg = (
                'Trades of the instrument %s are cash posting to %s with '
                'different spot days offset (%d ->%d)'
                'The spot day difference does not affect cash posting.'
                'However, the Trading Manager may display slightly '
                'different funding-related profit and loss values, '
                'due to the change of valuation date.' % (
                    insName, cpInsName, insSpot, cpInsSpot
                )
            )
            self.log.logWarning(msg)

class ArchivedInstTrds:
    def __init__(self, inst, log):
        self.inst = inst
        self.log = log

    def GetArchivedTrdsAndItsCPTrds(self, execParam, getCSPTrds):

        ports = execParam.get('TradingPortfolios', [])
        filters = execParam.get('TradeFilter', [])
        trdQuery = execParam.get('TradeQuery', [])
        allowed_trades = getattr(self, 'allowed_trades', None)

        sql_archivedTrades = (
            "select trdnbr from trade where archive_status = 1"
        )

        sql_ins = ("and insaddr = %s " % self.inst)
        sql_archivedTrades = sql_archivedTrades + sql_ins

        if len(ports):
            sql_ports = ("and prfnbr in %s " % ports)
            sql_archivedTrades = sql_archivedTrades + sql_ports

        if allowed_trades:
            sql_allowed_trades = ('and trdnbr in (%s)' % ','.join(
                str(oid) for oid in allowed_trades
            ))
            sql_archivedTrades = sql_archivedTrades + sql_allowed_trades

        sql_archivedTrades = string.replace(sql_archivedTrades, "[", "(")
        sql_archivedTrades = string.replace(sql_archivedTrades, "]", ")")

        selectedTrds = FBDPCommon.get_result_in_list(
            ael.dbsql(sql_archivedTrades)
        )

        trdSelectedFromFilter = []
        if len(filters):
            acmTrds = []
            for id in selectedTrds:
                acmTrade = FBDPCommon.ael_to_acm(ael.Trade[id])
                acmTrade.ArchiveStatus(0)
                acmTrds.append(acmTrade)

            for tradesSelect in filters:
                snapShot = tradesSelect.Snapshot()
                for trd in snapShot:
                    oid = trd.Oid()
                    if oid in selectedTrds:
                        trdSelectedFromFilter.append(oid)

            for acmTrade in acmTrds:
                acmTrade.ArchiveStatus(1)
                FNewExpirationUtility.performCommit(acmTrade, self.log)

        if len(trdSelectedFromFilter):
            selectedTrds = trdSelectedFromFilter

        # TODO for store folder
        #Find the cashposting trade.
        if len(selectedTrds):
            sql_cashpostingTrades = (
                "select distinct aggregate_trdnbr from trade where "
                "trdnbr in %s" % selectedTrds
            )
            sql_cashpostingTrades = string.replace(
                sql_cashpostingTrades, "[", "("
            )
            sql_cashpostingTrades = string.replace(
                sql_cashpostingTrades, "]", ")"
            )
            cpTrades = FBDPCommon.get_result_in_list(
                ael.dbsql(sql_cashpostingTrades)
            )

            finalDeArchivedTrds = selectedTrds
            cpArcTrdsList = []
            if len(cpTrades):
                # from the cpTrades, find the final trades that needs to
                # be dearchived.
                for cpId in cpTrades:
                    cpTrade = ael.Trade[cpId]
                    if not cpTrade or cpTrade.type != 'Cash Posting':
                        continue

                    sql_finalTrades = (
                        "select trdnbr from trade where "
                        "aggregate_trdnbr = %s" % cpId
                    )
                    finalDeArchivedTrds = FBDPCommon.get_result_in_list(
                        ael.dbsql(sql_finalTrades)
                    )
                    if getCSPTrds:
                        cpAndArchiveTrds = _CPAndArchiveTrds(
                            cpTrds=cpId, arcTrds=finalDeArchivedTrds
                        )
                    else:
                        cpAndArchiveTrds = _CPAndArchiveTrds(
                            cpTrds=None, arcTrds=finalDeArchivedTrds
                        )
                    cpArcTrdsList.append(cpAndArchiveTrds)
            else:
                self.log.logError(
                    'No archived trades will be de-archived or deleted, '
                    'as we can not find any CSP trades associated with '
                    'the selected trades.'
                )
                return None

            return cpArcTrdsList

        else:
            self.log.logInfo(
                'No archived trades were found to be de-archived or deleted.'
            )
            return None
