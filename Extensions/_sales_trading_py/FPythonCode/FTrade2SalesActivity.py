""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/SalesTrading/./etc/FTrade2SalesActivity.py"
"""--------------------------------------------------------------------------
MODULE
    FTrade2SalesActivity

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-----------------------------------------------------------------------------"""
import acm
import math

from FSalesTradingLogging import logger
from FParameterSettings import ParameterSettingsCreator
from FIntegratedWorkbenchUtils import RemoveDuplicates

SalesActivityIgnored = 'ignored'
SalesActivityInserted = 'inserted'
SalesActivityUpdated = 'updated'
SalesActivityError = 'error'

class Trade2SalesActivity(object):
    def __init__(self, rootPageGroup=None, forceUpdate=False, logLevel=None, __date=None):
        """
            @param pageGroup A FPageGroup that contains all instruments to check
            @param forceUpdate If True, existing FSalesActivity will be overwritten
            @param logLevel Level of colsole printing
            @param date The trade and valuation date
        """
        self._forceUpdate = forceUpdate
        self._logLevel = logLevel
        self._date = __date
        self._settings = self._GetSettings()
        self._pageGroup = rootPageGroup if (rootPageGroup != None) else self._GetRootPageGroup(self._settings)
        self._spaceCollection = acm.Calculations().CreateCalculationSpaceCollection()
        if self._logLevel != None:
            logger.Reinitialize(self._logLevel)

    # ---- Public methods ----

    def OnTrade(self, acmTrade, eventType):
        """
            Called for every new or updated trade.
            Check that the trade instrument (or underlying instrument if instype is Option, see GetInstrument)
            is in the root Page Group or any of its children.
        """
        if not eventType in ['insert', 'update']:
            return

        instr = self._GetInstrument(acmTrade)

        # Make sure the trade instrument (or its underlying) is in the page group hierarchy
        if not self._pageGroup.IncludesRecursively(instr):
            logger.debug("Trade2SalesActivity.OnTrade() Ignoring trade with Oid: %s, not in page group '%s'" % (acmTrade.Oid(), self._pageGroup.Name()))
        else:
            self._OnValidTrade(acmTrade, eventType)

    def UpdateTrade2SalesActities(self):
        """
            The method expects a collection of instruments and it will make sure
            that all trades made at a given date have corresponding SalesActivity entries.
        """
        instruments = RemoveDuplicates(self._pageGroup.InstrumentsRecursively())

        # determine date
        dateStr = ''
        dateVal = self._date
        if dateVal == None or dateVal == '':
            dateStr = 'TODAY'
            dateVal = '0d'
        else:
            dateStr = dateVal

        logger.info("Trade2SalesActivity.UpdateTrade2SalesActitivyToday() "
                    "%d instruments in FPageGroup '%s' date: '%s'" % (len(instruments), self._pageGroup.Name(), dateStr))

        for ins in instruments:
            insTrades = self._TradesForInstrument(ins, dateVal)

            if insTrades:
                ignoredSAct = 0
                insertedSAct = 0
                updatedSAct = 0
                failedSAct = 0
                # For each trade, try to get a SalesActivity, if there is none, create
                for trade in insTrades:
                    status = SalesActivityIgnored
                    try:
                        if self._forceUpdate:
                            logger.debug("Trade2SalesActivity.UpdateTrade2SalesActitivyToday() "
                                    "forcing update of SalesActivities for trade: %d" % trade.Oid())
                            status = self._OnValidTrade(trade, 'update')
                        else:
                            salesAct = acm.FSalesActivity.Select("trade=%d" % trade.Oid())
                            logger.debug("Trade2SalesActivity.UpdateTrade2SalesActitivyToday() "
                                         "%d SalesActivities for trade: %d" % (salesAct.Size(), trade.Oid()))
                            if salesAct.Size() == 0:
                                status = self._OnValidTrade(trade, 'insert')
                    except Exception as stderr:
                        logger.error("Trade2SalesActivity.UpdateTrade2SalesActitivyToday() Exception while handling trade:"
                                        " %d for instrument: %s" % (trade.Oid(), ins.Name()))
                        logger.error(stderr, exc_info=True)
                        status = SalesActivityError
                    # Counting
                    if status == SalesActivityIgnored:
                        ignoredSAct += 1
                    elif status == SalesActivityInserted:
                        insertedSAct += 1
                    elif status == SalesActivityUpdated:
                        updatedSAct += 1
                    else:
                        failedSAct += 1
                logger.info("Trade2SalesActivity.UpdateTrade2SalesActitivyToday() %d trades for instrument: %s."
                            " %d ignored, %d inserted, %d updated and %d failed"
                            % (len(insTrades), ins.Name(), ignoredSAct, insertedSAct, updatedSAct, failedSAct))

    @classmethod
    def GetPageGroups(cls):
        """
            Return a list of all page groups below the root node, including the root
        """
        root = cls.GetPageGroupRoot()
        groups = [root]
        cls._AddSubGroups(root, groups)
        return groups

    @classmethod
    def GetPageGroupRoot(cls):
        settings = cls._GetSettings()
        return cls._GetRootPageGroup(settings)

    # ---- Protected methods ----

    @staticmethod
    def _TradesForInstrument(ins, dateVal):
        """
            Get all trades in the instrument today
        """
        insTrades = None
        try:
            tradeQry = acm.CreateFASQLQuery(acm.FTrade, 'AND')
            tradeInsNode = tradeQry.AddOpNode('OR')
            tradeInsNode.AddAttrNode('Instrument.Oid', 'EQUAL', ins.Oid())
            tradeInsUnderNode = tradeInsNode.AddOpNode('AND')
            tradeInsUnderNode.AddAttrNode('Instrument.Underlying.Oid', 'EQUAL', ins.Oid())
            tradeInsUnderNode.AddAttrNode('Instrument.InsType', 'EQUAL', 'Option')
            tradeQry.AddAttrNode('TradeTime', 'GREATER_EQUAL', dateVal)
            tradeQry.AddAttrNode('TradeTime', 'LESS_EQUAL', dateVal)

            insTrades = tradeQry.Select()
            logger.debug("Trade2SalesActivity._TradesForInstrument() %d trades for instrument: %s" % (len(insTrades), ins.Name()))
        except Exception as stderr:
            logger.error("Trade2SalesActivity._TradesForInstrument() Exception while handling instrument: %s" % (ins.Name()))
            logger.error(stderr, exc_info=True)
        return insTrades

    @classmethod
    def _AddSubGroups(cls, page, groups):
        """
            Recursively add the page groups in page to the list of groups
        """
        for sg in page.SubGroups():
            groups.append(sg)
            cls._AddSubGroups(sg, groups)

    @staticmethod
    def _GetSettings():
        """
            Get FParameters called CTSTradeHook
        """
        return ParameterSettingsCreator.FromRootParameter('CTSTradeHook')

    @classmethod
    def _GetRootPageGroup(cls, settings):
        """
            Get the page group root node given by the parameter "RootPageGroupName"
        """
        rootPageGroupName = settings.RootPageGroupName()
        rootPageGroup = acm.FPageGroup[rootPageGroupName]
        if not rootPageGroup:
            logger.error("Trade2SalesActivity._GetRootPageGroup() Unknown PageGroup '%s'" % (rootPageGroupName))
            return None
        return rootPageGroup

    @staticmethod
    def _GetInstrument(acmTrade):
        """
            Determine what instrument to use for the trade
            @param acmTrade The trade
        """
        if acmTrade.Instrument().InsType() == 'Option':
            return acmTrade.Instrument().Underlying()
        else:
            return acmTrade.Instrument()

    def _OnValidTrade(self, acmTrade, eventType):
        """
            Insert or Update FSalesActivity
            Locate FSalesActivity by trade Oid, if more than one FSalesActivity,
            warn and update the first, if none create new
            @param acmTrade The trade
            @param eventType 'insert' or 'update'
            @return Status (updated, inserted, ignored or error)
        """
        try:
            # Only include MasterTrades
            if acmTrade.MasterTrade().Oid() != acmTrade.Oid():
                logger.debug("Trade2SalesActivity._OnValidTrade() Ignoring non master trade with Oid: %s instrument: %s" %
                    (acmTrade.Oid(), acmTrade.Instrument().Name()))
                return SalesActivityIgnored
            logger.debug("Trade2SalesActivity._OnValidTrade() Trade with Oid: %s instrument: %s" %
                    (acmTrade.Oid(), acmTrade.Instrument().Name()))

            originalSalesActivity = None
            salesActivity = None

            doInsert = False
            res = acm.FSalesActivity.Select('trade=%d' % acmTrade.Oid())
            if (res == None) or (res.Size() == 0):
                logger.debug('Trade2SalesActivity._OnValidTrade() Creating Sales Activity from trade with oid: %d' % acmTrade.Oid())
                salesActivity = acm.FSalesActivity()
                doInsert = True
            else:
                if eventType == 'insert':
                    logger.warn('Trade2SalesActivity._OnValidTrade() Trade with Oid %d already has a Sales Activity' % acmTrade.Oid())
                if res.Size() > 1:
                    logger.warn('Trade2SalesActivity._OnValidTrade() More than one Sales Activity for trade with oid: %s, updating the first Sales Activity' % acmTrade.Oid())
                originalSalesActivity = res.First()
                salesActivity = originalSalesActivity.Clone()
                logger.debug("Trade2SalesActivity._OnValidTrade() Updating Sales Activity with Oid: %s from trade with Oid: %s" % (salesActivity.Oid(), acmTrade.Oid()))

            if not self._InitSalesActivityFromTrade(acmTrade, salesActivity):
                logger.error("Trade2SalesActivity._OnValidTrade() Failed to create Sales Activity for trade with Oid: %s" % (acmTrade.Oid()))
                return SalesActivityError

            # Validate
            isValid = True
            try:
                import FCTSTradeHookValidation
                isValid = FCTSTradeHookValidation.Validate(salesActivity)
            except Exception as stderr:
                logger.error("Trade2SalesActivity._OnValidTrade() Exception while validating Sales Activity for trade %d" % acmTrade.Oid())
                logger.error(stderr, exc_info=True)
                return SalesActivityError

            if not isValid:
                logger.debug("Trade2SalesActivity._OnValidTrade() Sales Activity from trade with Oid: %s rejected by validation hook" % acmTrade.Oid())
                return SalesActivityIgnored

            # Save FSalesActivity
            if doInsert:
                try:
                    salesActivity.Commit()
                    logger.info("Trade2SalesActivity._OnValidTrade() Created new Sales Activity for trade with Oid: %s" % (acmTrade.Oid()))
                    return SalesActivityInserted
                except Exception as stderr:
                    logger.error("Trade2SalesActivity._OnValidTrade() Exception while commiting new Sales Activity for trade %d" % acmTrade.Oid())
                    logger.error(stderr, exc_info=True)
                    return SalesActivityError
            else:
                try:
                    originalSalesActivity.Apply(salesActivity)
                    originalSalesActivity.Commit()
                    logger.info("Trade2SalesActivity._OnValidTrade() Updated Sales Activity for trade with Oid: %s" % (acmTrade.Oid()))
                    return SalesActivityUpdated
                except Exception as stderr:
                    logger.error("Trade2SalesActivity._OnValidTrade() Exception while commiting updated Sales Activity for trade %d" % acmTrade.Oid())
                    logger.error(stderr, exc_info=True)
                    return SalesActivityError
        except Exception as stderr:
            logger.error("Trade2SalesActivity._OnValidTrade() Exception for trade %d" % acmTrade.Oid())
            logger.error(stderr, exc_info=True)
        return SalesActivityError

    def _InitSalesActivityFromTrade(self, acmTrade, salesActivity):
        """
            Set attributes of a FSalesActivity from column values,
            evaluated for the trade on a FTradeSheet.
        """
        sheetClass = 'FTradeSheet'
        cs = self._spaceCollection.GetSpace(sheetClass, acm.GetDefaultContext())

        if self._date != None:
            logger.debug("Trade2SalesActivity._InitSalesActivityFromTrade() Trade: %d, simulating valuation date: %s" % (acmTrade.Oid(), self._date))
            cs.SimulateGlobalValue('Valuation Date', self._date)

        salesActivity.Trade(acmTrade)
        attribs = self._settings.SalesActivityAttributes()
        hasError = False
        for attr in attribs:
            # Make sure there is a mapping from attribute to column in the FParameters
            if not hasattr(self._settings, attr):
                logger.error("Trade2SalesActivity._InitSalesActivityFromTrade() A parameter '%s' is required" % attr)
                return False
            # Make sure that FSalesActivity has the attribute
            if not hasattr(salesActivity, attr):
                logger.error("Trade2SalesActivity._InitSalesActivityFromTrade() Attribute '%s' not defined for FSalesActivity" % attr)
                hasError = True
                break

            value = None
            try:
                colId = getattr(self._settings, attr)()
                value = cs.CalculateValue(acmTrade, colId)
            except Exception as stderr:
                logger.error("Trade2SalesActivity._InitSalesActivityFromTrade() Exception while getting "
                             "attribute '%s' of trade %d" % (attr, acmTrade.Oid()))
                logger.error(stderr, exc_info=True)

            try:
                if (value == None) and (attr in self._settings.RequiredAttributes()):
                    logger.error("Trade2SalesActivity._InitSalesActivityFromTrade() Value for Required column '%s' (attribute '%s') is None" % (colId, attr))
                    hasError = True
                    break
                # check if the attribute is a float, and if so check for NaN
                method = acm.FSalesActivity.GetMethod(attr, 0)
                if method:
                    domain = method.Domain()
                    if domain.IsKindOf(acm.FDoubleDomain) and ((value == None) or math.isnan(float(value)) or math.isinf(float(value))):
                        value = 0.0
                        logger.warn("Trade2SalesActivity._InitSalesActivityFromTrade() Value for column '%s' "
                                     "(attribute '%s' with domain '%s' for trade %d) is NaN/None/Inf, setting to 0.0"
                                     % (colId, attr, domain, acmTrade.Oid()))

                if hasattr(value, 'Name'):
                    # pylint: disable-msg=E1101
                    presValue = value.Name()
                else:
                    presValue = value
                logger.debug("Trade2SalesActivity._InitSalesActivityFromTrade() Attribute '%s' "
                             "column '%s' value: %s type: %s" % (attr, colId, presValue, type(value)))
                getattr(salesActivity, attr)(value)
            except Exception as stderr:
                logger.error("Trade2SalesActivity._InitSalesActivityFromTrade() Exception while setting "
                             "attribute '%s' of trade %d" % (attr, acmTrade.Oid()))
                logger.error(stderr, exc_info=True)
                hasError = True
                break

        if self._date != None:
            cs.RemoveGlobalSimulation('Valuation Date')

        return not hasError
