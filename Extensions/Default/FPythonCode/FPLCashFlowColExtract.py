""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/pl_processing/etc/FPLCashFlowColExtract.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
from __future__ import print_function
"""----------------------------------------------------------------------------
MODULE
    FPLCashFlowColExtract

DESCRIPTION:
    This module is used for extracting P/L values or Cash Flow values using
    CalcSpace.  The higher level calling code can be written independent of
    the CalcSpace api.  Points PL and PL are obtained in the display currency
    for each time bucket from discrete columns.  The result is a dictionary
    for easy access by time bucket and Column.  Cash Flow is obtained for
    each time bucket in a vector column per Currency.
    The result is a dictionary for easy access by time bucket and Currency.
    (Note: 4.3 Sprint 2. Renamed from FPLXMLExtract, as XML removed.)

ENDDESCRIPTION
----------------------------------------------------------------------------"""


import inspect
import math


import ael
import acm


import FBDPCommon
import FBDPString
logme = FBDPString.logme

logmode = '2'


def getPrefDefaultContextName():

    acmserver = acm.FACMServer()
    pref = acmserver.GetUserPreferences()
    ctxName = pref.DefaultContext()
    return ctxName


class PCTException(Exception):
    pass


insertSheetType = 'FPortfolioSheet'  # Alt. insertSheetType = 'FTimeSheet'


tail = inspect.stack()[1][1][-7:]  # fname


class PL_CalcExtract():
    """
    PL report in CalcSpace.
    """

    def __init__(self, valuationParametersGUI, logmode):

        self.valuation_parameters = valuationParametersGUI
        self.reportName = 'PL3range'  # Mb 'CFxxx' or 'PLxxx'
        self.currencylist = None
        self.rparm = ReportParamCS(self.reportName, logmode)

    def perform_CalcExtract(self, sValCur, portfName, scanbegin_date, spotDays,
            overridePLUntilSpot=False):

        self.rparm.set1_ReportParams(None, sValCur)
        self.rparm.set2_ReportPortf_Flag(portfName, spotDays,
                overridePLUntilSpot)
        sheetType = 'FPortfolioSheet'
        self.rptPortfRowCol = ReportPortfTimeBucketColsCS(self.rparm)
        self.rptPortfRowCol.create_ReportExtractCS(self.reportName,
                self.currencylist, sheetType)
        spotAndForward = True  # PL in Forward is unrealized
        (self.rptPortfRowCol.
                set3_ReportToday_SpotAndForward_TimeBucketStringACM(
                scanbegin_date, spotAndForward))
        self.rptPortfRowCol.setReportTimeBucketsCols_TypeCS(
                self.rptPortfRowCol.columnNames, self.currencylist,
                sheetType, self.rptPortfRowCol.rparm.reportName)


class CashFlow_CalcExtract():
    """
    CashFlow report using CalcSpace
    """

    def __init__(self, valuationParametersUserVP, logmode, cellReCalc=False):

        self.valuation_parameters = valuationParametersUserVP
        self.reportName = 'CF3range_wo_forward'  # Mb 'CFxxx' or 'PLxxx'
        self.currencylist = None
        self.rparm = ReportParamCS(self.reportName, logmode)
        self.rparm.cellReCalc = cellReCalc
        self.allcurrencies = None  # oneshot

    def setCurrencyList(self, acurrencylist):  # vector cols only.

        self.currencylist = acurrencylist

    def gatherAllCurrencies_NonZero(self, trading_portfolio, scanbegin_date,
            rpt_days_range):

        if self.allcurrencies is None:  # oneshot
            self.allcurrencies = getAllCurrencies()
        self.rpt = self.genCalcExtract_NonZero(trading_portfolio,
                self.allcurrencies.keys(), scanbegin_date, None,
                rpt_days_range)  # cz _cp)
        currencies_nonzero = (
                self.rptPortfRowCol.colCS.currencies_detectNonZero.keys())
        return currencies_nonzero

    def genCalcExtract_NonZero(self, trading_portfolio, currencylist,
            scanbegin_date, roll_to_date_cp, rpt_days_range):

        # _NonZero pass2, subset <= N extract.
        self.setCurrencyList(currencylist)
        self.perform_CalcExtract(trading_portfolio.prfid, scanbegin_date,
                rpt_days_range)
        self.gen_dirty = False
        return self

    def perform_CalcExtract(self, portfName, scanbegin_date, spotDays):

        portf = acm.FPhysicalPortfolio[portfName]
        if portf:
            if portf.CurrencyPair() is not None:
                # reportName Mb 'CFxxx' or 'PLxxx'
                self.reportName = 'CFByCPair_3range_wo_forward'  # MMCase1
            else:
                self.reportName = 'CFByCurrn_3range_wo_forward'  # MMCase2
        self.rparm.set1_ReportParams(self.valuation_parameters.name)
        self.rparm.set2_ReportPortf_Flag(portfName, spotDays, None)
        sheetType = 'FPortfolioSheet'  # Alt. sheetType = 'FTimeSheet'
        self.rptPortfRowCol = ReportPortfTimeBucketColsCS(self.rparm)
        self.rptPortfRowCol.create_ReportExtractCS(self.reportName,
                self.currencylist, sheetType)
        spotAndForward = False  # CF spot separate.
        self.rptPortfRowCol.set3_ReportToday_SpotAndForward_TimeBucketString(
                scanbegin_date, spotAndForward)
        self.rptPortfRowCol.setReportTimeBucketsCols_TypeCS(
                self.rptPortfRowCol.columnNames, self.currencylist,
                sheetType, self.rptPortfRowCol.reportName)


def instrumentQuery(instype=()):

    # Create empty question or get default question for certain class
    q = FBDPCommon.CreateFASQLQuery(acm.FInstrument, 'AND')
    #    q = CreateDefaultFASQLQuery(FInstrument)
    # Text field
    op = q.AddOpNode('OR')
    op.AddAttrNode('Name', 'RE_LIKE_NOCASE', None)
    # enum
    op = q.AddOpNode('OR')
    if instype:
        for i in instype:
            op.AddAttrNode('InsType', 'EQUAL',
                    ael.enum_from_string('InsType', i))
    return q


def getAllCurrencies():

    q = instrumentQuery(('Curr',))
    selcurrencies = q.Select()
    currencies = {}
    for currency in selcurrencies:
        if currency.Name() not in currencies:
            acurrency = ael.Instrument[currency.Name()]
            currencies[currency.Name()] = None
    return currencies


class ReportParamCS:

    def __init__(self, _reportName, logmode):

        self.reportName = _reportName
        self.logmode = logmode
        self.logTBPLbuckets = False
        if logmode > '6':  # TimeBuckets and PLBuckets and ctx
            self.logTBPLbuckets = True
        self.ctxName = getPrefDefaultContextName()

    def setAcctgParm_CalcExtractACM(self):

        try:
            currextattr = acm.GetStandardExtension('FExtensionAttribute',
                    'FCurrency', 'accountingCurrency')
            # AccountingCurrency is based on Standard Extension
            # 'accountingCurrency'.
            if currextattr is None:
                msg = ('Missing Extension Attribute. None returned from '
                        'GetStandardExtension(accountingCurrency) ')
                logme(msg, 'ERROR')
                raise PCTException(msg)
            av = acm.GetCalculatedValue(None, self.ctxName,
                    "accountingCurrency")
            if av is None:
                msg = ('None returned from GetCalculatedValue('
                        'accountingCurrency)')
                logme(msg, 'ERROR')
                raise PCTException(msg)
            else:
                self.accounting_currency = acm.FInstrument[av.Value().Name()]
            logme('Using extension attribute "accountingCurrency": "%s" '
                    'Context: "%s".' % (self.accounting_currency.Name(),
                    self.ctxName))
        except Exception as e:
            print(e)
            msg = ('Exception getting accountingCurrency, Context ' +
                   self.ctxName)
            logme(msg, 'ERROR')
            raise PCTException(msg)
        return self.accounting_currency

    def setAcctgParm_ValParm_CalcExtractACM(self, valuationParameters):

        self.valuation_parameters = valuationParameters
        try:
            self.setAcctgParm_CalcExtractACM()
            if valuationParameters:
                valpars_accounting_currency = (self.valuation_parameters.
                        AccountingCurrency())
                if (valpars_accounting_currency.Name() !=
                        self.accounting_currency.Name()):
                    logme('ExtensionAttribute accountingCurrency %s: '
                            'overrides Valuation Params Accounting Currency: '
                            '"%s".' % (self.accounting_currency.Name(),
                            valpars_accounting_currency.Name()), 'WARNING')
        except Exception as e:
            print(e)
            msg = ('Exception getting accountingCurrency, Context ' +
                   self.ctxName)
            logme(msg, 'ERROR')
            raise PCTException(msg)
        return self.accounting_currency

    def setAcctgParm_CalcExtract(self):

        try:
            currextattr = acm.GetStandardExtension('FExtensionAttribute',
                    'FCurrency', 'accountingCurrency')
            # AccountingCurrency is based on Standard Extension
            # 'accountingCurrency'.
            if currextattr is None:
                msg = ('Missing Extension Attribute. None returned from '
                       'GetStandardExtension(accountingCurrency) ')
                logme(msg, 'ERROR')
                raise PCTException(msg)
            av = acm.GetCalculatedValue(None, self.ctxName,
                    "accountingCurrency")
            if av is None:
                msg = ('None returned from GetCalculatedValue('
                       'accountingCurrency)')
                logme(msg, 'ERROR')
                raise PCTException(msg)
            else:
                self.accounting_currency = ael.Instrument[av.Value().Name()]
            logme('Using extension attribute "accountingCurrency": "%s" '
                    'Context: "%s".' % (self.accounting_currency.insid,
                    self.ctxName))
        except Exception as e:
            print(e)
            msg = ('Exception getting accountingCurrency, Context ' +
                   self.ctxName)
            logme(msg, 'ERROR')
            raise PCTException(msg)
        return self.accounting_currency

    def setAcctgParm_ValParm_CalcExtract(self, valuationParameters):

        self.valuation_parameters = valuationParameters
        try:
            self.setAcctgParm_CalcExtract()
            valpars_accounting_currency = (
                    self.valuation_parameters.accounting_currency)
            if (valpars_accounting_currency.insid !=
                    self.accounting_currency.insid):
                logme('ExtensionAttribute accountingCurrency %s: overrides '
                        'Valuation Params Accounting Currency: "%s".' %
                        (self.accounting_currency.insid,
                         valpars_accounting_currency.insid), 'WARNING')
        except Exception as e:
            print(e)
            msg = ('Exception getting accountingCurrency, Context ' +
                    self.ctxName)
            logme(msg, 'ERROR')
            raise PCTException(msg)
        return self.accounting_currency

    def set1_ReportParams(self, sValuationParam, _sValCurr=None):

        self.sValCurr = _sValCurr
        if not sValuationParam:
            self.valpar = None
        else:
            # Alt Override ParamMapping at User level
            self.valpar = acm.FValuationParameters[sValuationParam]

    def set2_ReportPortf_Flag(self, _portfName, arg_spot_days=2,
            _override_PLuntilSpot=None):

        self.override_PLuntilSpot = _override_PLuntilSpot
        self.portfName = _portfName
        self.acmportf = acm.FPhysicalPortfolio[self.portfName]
        if self.logmode > '5':
            logme('FPhysicalPortfolio  %s' % (self.acmportf))
        # N/A Override here. Only Collapse, one day only.
        # NAvalpar.PlUntilSpot('1')
        if not (self.reportName[:2] == 'PL' and self.override_PLuntilSpot):
            self.nDaysfPLuntilSpot = arg_spot_days
        else:
            # Override means Pgm override will collapse, Does NOT rely on
            # ValParams state.
            self.nDaysfPLuntilSpot = 0
            if self.logmode >= '3' and self.valpar:
                logme('set2 ValParm PlUntilSpot = %s ' %
                        (self.valpar.PlUntilSpot()))
        if self.logmode >= '3':
            logme('set2 Case1Override_PlUntilSpot = %s Calc Engine ndays = %i'
                    % (self.override_PLuntilSpot, self.nDaysfPLuntilSpot))


class ReportPortfTimeBucketColsCS:

    def __init__(self, rparm):

        self.rparm = rparm
        self.dlist = None
        self.datelist = None
        self.tbgrouper = None
        self.verboseCalc = False
        self.logSetf = False
        if self.rparm.reportName[:2] == 'PL':
            self.colCS = DiscreteColCalcSpace()
        elif self.rparm.cellReCalc:
            self.colCS = VectorColReCalcCalcSpace()
            self.colCS.setReCalcCell()
        else:
            self.colCS = VectorColCalcSpace()
        if self.rparm.logmode >= '6':
            self.logSetf = True
            self.colCS.verboseCalc = True

    def create_ReportExtractCS(self, _reportName, currencylist,
            _sheetType='FPortfolioSheet'):
        self.reportName = _reportName
        insertSheetType = _sheetType
        # Preset col_keys and columnNames are f(reportName[:2], sheetType)
        # set up here.
        if self.reportName[:2] == 'PL':
            if insertSheetType != 'FTimeSheet':
                self.sheetType = 'FPortfolioSheet'
                self.columnNames = ['Portfolio Points Profit And Loss',
                        'Portfolio Profit And Loss']
                self.colKeysRpt = ('Portfolio Points Profit And Loss',
                        'Portfolio Profit And Loss')
            else:
                self.sheetType = 'FTimeSheet'
                self.columnNames = ['Portfolio Points Profit And Loss',
                        'Portfolio Profit And Loss']  # TimeSheet
                self.colKeysRpt = ('Portfolio Points Profit And Loss',
                        'Portfolio Profit And Loss')
        if self.reportName[:2] == 'CF':
            # Alt. self.sheetType = 'FTimeSheet'
            self.sheetType = 'FPortfolioSheet'
            if self.reportName == 'CFByCPair_3range_wo_forward':
                    self.columnNames = [                             # NO DASH
                            'Portfolio Projected Payments Currency Pair']
                    self.colKeysRpt = (
                            'Portfolio Projected Payments Currency Pair',)
            else:
                    # NO DASH. # 'CFByCurrn_3range_wo_forward'
                    self.columnNames = ['Portfolio Projected per Currency']
                    # (tuple0, REDUNDANT COMMA)
                    self.colKeysRpt = ('Portfolio Projected Payments',)
        return

    def set3_ReportToday_SpotAndForward_TimeBucketStringACM(
            self, _scanbegin_date, spotAndForward=True):
        """
        SpotAndForward vs Spot single day
        """

        self.datelist = []
        self.dlist = []
        self.scanbegin_date = _scanbegin_date
        iteratorDate = acm.Time().AsDate(self.scanbegin_date)
        mdi = -self.rparm.nDaysfPLuntilSpot  # dependency
        while mdi < + 1:
            if mdi == 0 and spotAndForward:
                #Must use BIG bucket. just TODAY, NG_dlist.append('0' + 'd')
                self.dlist.append(str(10000) + 'm')
            else:
                self.dlist.append(str(mdi) + 'd')
            self.datelist.append(iteratorDate)
            iteratorDate = acm.Time().DateAddDelta(iteratorDate, 0, 0, 1)
            mdi += 1
        if self.rparm.logTBPLbuckets:
            logme('Time bucket days, dates %s %s' %
                    (self.dlist, self.datelist))
        return

    def set3_ReportToday_SpotAndForward_TimeBucketString(self, _scanbegin_date,
            spotAndForward=True):  # SpotAndForward vs Spot single day
        self.datelist = []
        self.dlist = []
        self.scanbegin_date = _scanbegin_date
        iteratorDate = ael.date(self.scanbegin_date)
        mdi = -self.rparm.nDaysfPLuntilSpot  # dependency
        while mdi < + 1:
            if mdi == 0 and spotAndForward:
                # Must use BIG bucket.#just TODAY#NG_dlist.append('0' + 'd')
                self.dlist.append(str(10000) + 'm')
            else:
                self.dlist.append(str(mdi) + 'd')
            self.datelist.append(iteratorDate)
            iteratorDate = iteratorDate.add_days(1)
            mdi += 1
        if self.rparm.logTBPLbuckets:
            logme('Time bucket days, dates %s %s' % (self.dlist,
                    self.datelist))
        return

    def setReportTimeBucketsCols_TypeCS(self, colNames, currencylist,
            sheetType, reportName):
        if self.rparm.logmode >= '3':
            logme('TimeBuckets Cols CurrencyList %s %s %s' % (self.dlist,
                    colNames, currencylist))
        shsettingsD = {}
        if self.logSetf:
            logme('getSheetSettingsDictionary = %s' % (shsettingsD))

        mybucks = "'"
        for b in self.dlist:
            mybucks = mybucks + b + "' '"
        mybucks = [mybucks[:len(mybucks) - 2]]
        if self.logSetf:
            print(('mybucks {0}'.format(mybucks)))

        bucks = acm.Time().CreateTimeBuckets(self.scanbegin_date, mybucks,
                mybucks, None, self.rparm.nDaysfPLuntilSpot, False, False,
                False, True, False)
        if self.logSetf:
            logme('bucks SpotDays = %s' % (bucks.GetSpotDays()))

        self.tbgrouper = acm.FTimeBucketGrouper(bucks)
        if self.logSetf:
            prtFTimeBuckets(bucks)
            logme('FTimeBucketGrouper %s' % (self.tbgrouper))

        if reportName[:2] == 'PL':
            colNames = ["Portfolio Points Profit And Loss",
                    "Portfolio Profit And Loss"]
            # PL, Set DispCurr to PL curr if it differs
            colNames.append('Portfolio Currency')
            try:
                self.colCS.createCalcSpace_SheetType(sheetType)
            except Exception as e:
                print(e)
                logme('Exception self.colCS.createCalcSpace_SheetType()',
                       'ERROR')
                raise e
            try:
                self.colCS.dictCalcPortfTBGXDiscreteCol(self.rparm,
                        self.rparm.portfName, self.tbgrouper, colNames,
                        'Portfolio Currency', self.rparm.sValCurr)
            except Exception as e:
                print(e)
                logme('Exception self.colCS.dictCalcPortfTBGXDiscreteCol(,,,)',
                        'ERROR')
                raise e
        else:
            colName = "Portfolio Projected Payments"
            self.colCS.createCalcSpace_SheetType(sheetType)
            self.colCS.createVectorCol__SubcolList(colName,
                    currencylist)  # alt colList)
            self.colCS.dictCalcPortfTBGXVectorCol(self.rparm.portfName,
                    self.tbgrouper)
        if self.logSetf:
            logme(' Report Name = %s' % (reportName))
            logme(' Sheet Type = %s' % (sheetType))

    def lookupDateToTB(self, date):
        try:
            ix = self.datelist.index(date)
            tb = self.dlist[ix]
        except:
            tb = -99999
        return tb

    def getPortfRowDateCurr_ColCS(self, kPortf, kRow, kCurr):
        try:
            k = kCurr + "^" + kRow  # CashFlow has instrument key EUR^tb
            if self.verboseCalc:
                logme("col key: %s %s" % (kCurr, k))
            v = self.colCS.vdict[k]
        except:
            v = 'NotFound'
        if self.verboseCalc:
            print(('getPortfRowDateCurr_ColCS self.colCS.vdict[k] {0} {1} '
                    '{2}'.format(kCurr, k, v)))
        return v

    def getPortfRowCol(self, kPortf, kRow, kCol):
        try:
            k = kCol + "^" + kRow
            if self.verboseCalc:
                logme("col key: %s %s" % (kCol, k))
            v = self.colCS.vdict[k]
        except:
            v = 'NotFound'
        if self.verboseCalc:
            print(('getPortfRowCol self.colCS.vdict[k] {0} {1} {2}'.format(
                    kCol, k, v)))
        return v


class DiscreteColCalcSpace():
    def __init__(self):
        self.verboseCalc = False

    def createCalcSpace_SheetType(self, csSheet):
        self.csSheet = csSheet
        self.cs = acm.FCalculationSpace(csSheet)

    def dictCalcPortfTBGXDiscreteCol(self, rparm, portfName, timeBucketGroup,
            colNames, simName=None, simValue=None):
        self.vdict = {}
        portf = acm.FPhysicalPortfolio[portfName]
        self.top_node = self.cs.InsertItem(portf)
        self.top_node.ApplyGrouper(timeBucketGroup)
        coli = 0
        # Normal convention vs sim
        if simName and simName == 'Portfolio Currency':
            if simValue is None:
                simValue = 'None'
            if self.verboseCalc:
                print(('simName, simValue {0} {1}'.format(simName, simValue)))
            self.cs.SimulateValue(portf, simName, simValue)
        try:
            # PL uses TimeSheetSettings for PL date. M/b consistent with
            # valpar.PlUntilSpot.
            # Only Case1.
            # Alt.
            # if rparm.override_PLuntilSpot or not rparm.valpar.PlUntilSpot():
            # override or user pass thru
            if rparm.override_PLuntilSpot:
                if self.verboseCalc:
                    print('before self.cs.SimulateGlobalValue(xPL Valuation '
                            'Datex, 1)')
                    # Self.cs.SimulateGlobalValue('PL Valuation Date', 'Today')
                    #TimeSheetSetting PL date
            else:
                pass
                # Self.cs.SimulateGlobalValue('PL Valuation Date',
                #        'Portfolio Spot')  #PLUntilSpot
        except Exception as e:
            logme('Exception self.cs.SimulateGlobalValue(PL Valuation Date, '
                    '1)', 'ERROR')
            raise e

        treeIterator = self.top_node.Iterator()  # Bucket Row. Iterator
        if treeIterator.HasChildren():
            childIterator = treeIterator.FirstChild()  # get first bucket
            while (childIterator):
                try:
                    ctifchiFTIter_FTreePx = childIterator.Tree()
                    tn = ctifchiFTIter_FTreePx.Item()
                    tnSK = tn.StringKey()
                    if tnSK[:4] != '1000':
                        calcChildnx = self.cs.CreateCalculation(
                                childIterator.Tree(), colNames[0])
                    else:
                        # Spot And Fwd in last bucket. Special cell is
                        # calculated using other colName.
                        coli += 1
                        calcChildnx = self.cs.CreateCalculation(
                                childIterator.Tree(), colNames[1])
                    fvn = calcChildnx.Value().Number()
                    if fvn != 0.0:
                        # key colName_tb
                        self.vdict[colNames[coli] + '^' + tnSK] = fvn
                        if self.verboseCalc:
                            print((self.vdict))
                except Exception as e:
                    raise e
                childIterator = childIterator.NextSibling()
        if self.verboseCalc:
            print((self.vdict))


class VectorColCalcSpace():

    def __init__(self):

        self.verboseCalc = False

    def createVectorCol__SubcolList(self, colName, subcolList):

        self.currencies_detectNonZero = {}
        self.colName = colName
        self.subcolList = subcolList
        self.colDataParamsList = []  # Sep colData reqd
        for i in range(0, len(subcolList)):
            colDataT = self.paymentsCol_AddPaymentsBucket(None,
                    [subcolList[i]], self.csSheet)  # Ctx out
            self.colDataParamsList.append(colDataT)

    def dictCalcPortfTBGXVectorCol(self, portfName, timeBucketGroup):

        # MM See calcSpace.Refresh()
        self.vdict = {}
        self.top_node = self.cs.InsertItem(acm.FPhysicalPortfolio[portfName])
        try:
            self.top_node.ApplyGrouper(timeBucketGroup)
            # Must Refresh() after insert.
            # Execute all outstanding background work.
            self.cs.Refresh()
            # Create a real-time updated calculation
            for i in range(0, len(self.colDataParamsList)):
                config = acm.Sheet().Column().ConfigurationFromVector(
                        self.colDataParamsList[i])
                calc = self.cs.CreateCalculation(self.top_node, self.colName,
                        config)  # Must do here to get tb
                fvn = calc.Value().Number()

            treeIterator = self.top_node.Iterator()  # Bucket Row. Iterator
            if treeIterator.HasChildren():
                childIterator = treeIterator.FirstChild()  # get first bucket
                while (childIterator):  # Sparse buckets PortfSheet.
                    try:
                        ctifchiFTIter_FTreePx = childIterator.Tree()
                        tn = ctifchiFTIter_FTreePx.Item()
                        tnSK = tn.StringKey()
                        for i in range(0, len(self.colDataParamsList)):
                            config = (acm.Sheet().Column().
                                    ConfigurationFromVector(
                                    self.colDataParamsList[i]))
                            calcChildnx = self.cs.CreateCalculation(
                                    childIterator.Tree(), self.colName, config)
                            val = calcChildnx.Value()
                            if val.Unit().Text() != self.subcolList[i]:
                                # Check denom unit against col
                                print(('Unit() differs from column {0} '
                                        '{1}'.format(val.Unit(),
                                        self.subcolList[i])))
                                raise Exception('ee')
                            fvn = calcChildnx.Value().Number()
                            if self.verboseCalc:
                                print(('Calc Key val float {0} {1} {2}'.format(
                                        tnSK, val, fvn)))
                            subcolcurr = self.subcolList[i]
                            priorHitCurrNonZeroOnward = (subcolcurr in
                                    self.currencies_detectNonZero)
                            # MM ReCalc needs calccelldict, hitNz onward.
                            if (math.fabs(fvn) > 0.0001 or
                                    priorHitCurrNonZeroOnward):
                                # key curr_tb
                                self.vdict[self.subcolList[i] + '^' +
                                        tnSK] = fvn
                                if not priorHitCurrNonZeroOnward:
                                    self.currencies_detectNonZero[
                                            subcolcurr] = subcolcurr
                    except Exception as e:
                        raise e
                    childIterator = childIterator.NextSibling()
        except Exception as e:
            logme(e)
            raise e
        if self.verboseCalc:
            print((self.vdict))

    def createCalcSpace_SheetType(self, csSheet):

        self.csSheet = csSheet
        self.cs = acm.FCalculationSpace(csSheet)

    def addPaymentsBucket(self, projPaymentsData, currency):

        # Vector col for cashflows
        projPaymentsDataBucket = acm.FNamedParameters()
        # 'currency' is the same key used in the column definition
        projPaymentsDataBucket.AddParameter('currency',
                acm.FCurrency[currency])
        projPaymentsData.Add(projPaymentsDataBucket)

    def paymentsCol_AddPaymentsBucket(self, colNames, currencyL, sheetType):

        # Vector col for cashflows
        projPaymentsData = acm.FArray()
        for i in range(len(currencyL)):
            self.addPaymentsBucket(projPaymentsData, currencyL[i])
        return projPaymentsData


class VectorColReCalcCalcSpace():
    """
    Note: Normal Spot has -2d -1d 0d time buckets. When max_date is used in the
    all currency approach, the negative date buckets may have lower tags such
    as -5d -4d -3d -2d -1d 0d.
    CashFlow calculations inside currency Spot are OK as they are inside
    max_date, not a f(0d) ref point.
    """

    def __init__(self):

        self.verboseCalc = False

    def createVectorCol__SubcolList(self, colName, subcolList):

        self.reCalcCell = False
        self.subcolReCalcGenDirtyDict = {}

        self.currencies_detectNonZero = {}
        self.colName = colName
        self.subcolList = subcolList
        self.colDataParamsList = []  # Sep colData reqd
        self.colDataParamsDict = {}
        for i in range(0, len(subcolList)):
            colDataT = self.paymentsCol_AddPaymentsBucket(None,
                    [subcolList[i]], self.csSheet)  # Ctx out
            self.colDataParamsList.append(colDataT)
            self.colDataParamsDict[subcolList[i]] = colDataT
            self.subcolReCalcGenDirtyDict[subcolList[i]] = False

    def dictCalcPortfTBGXVectorCol(self, portfName, timeBucketGroup):

        # MM See calcSpace.Refresh()
        self.reCalcCellDict = {}
        self.vdict = {}
        self.top_node = self.cs.InsertItem(acm.FPhysicalPortfolio[portfName])
        try:
            self.top_node.ApplyGrouper(timeBucketGroup)
            # Must Refresh() after insert.
            # Execute all outstanding background work.
            self.cs.Refresh()
            # Create a real-time updated calculation
            for i in range(0, len(self.colDataParamsList)):
                config = acm.Sheet().Column().ConfigurationFromVector(
                        self.colDataParamsList[i])
                calc = self.cs.CreateCalculation(self.top_node, self.colName,
                        config)  # Must do here to get tb
                fvn = calc.Value().Number()
            # Bucket Row. Iterator
            treeIterator = self.top_node.Iterator()
            if treeIterator.HasChildren():
                childIterator = treeIterator.FirstChild()
                # Get first bucket
                # TB Sparse #Sparse buckets PortfSheet. Cannot save empty Zero
                # cells for MM recalc.
                while (childIterator):
                    try:
                        ctifchiFTIter_FTreePx = childIterator.Tree()
                        tn = ctifchiFTIter_FTreePx.Item()
                        tnSK = tn.StringKey()
                        for i in range(0, len(self.colDataParamsList)):
                            config = (acm.Sheet().Column().
                                    ConfigurationFromVector(
                                    self.colDataParamsList[i]))
                            calcChildnx = self.cs.CreateCalculation(
                                    childIterator.Tree(), self.colName, config)
                            val = calcChildnx.Value()
                            # Check denom unit against col
                            if val.Unit().Text() != self.subcolList[i]:
                                print(('Unit() differs from column {0} '
                                        '{1}'.format(val.Unit(),
                                        self.subcolList[i])))
                                raise Exception('ee')
                            fvn = calcChildnx.Value().Number()
                            if self.verboseCalc:
                                print(('{0} {1} {2}'.format(tnSK, val, fvn)))
                            subcolcurr = self.subcolList[i]
                            priorHitCurrNonZeroOnward = (subcolcurr in
                                    self.currencies_detectNonZero)
                            # MM ReCalc needs calccelldict, hitNz onward.
                            if (math.fabs(fvn) > 0.0001 or
                                    priorHitCurrNonZeroOnward):
                                # Key curr_tb
                                k = self.subcolList[i] + '^' + tnSK
                                self.reCalcCellDict[k] = calcChildnx
                                self.vdict[k] = fvn
                                if not priorHitCurrNonZeroOnward:
                                    # Subcolcurr
                                    self.currencies_detectNonZero[
                                            subcolcurr] = True
                    except Exception as e:
                        raise e
                    childIterator = childIterator.NextSibling()
        except Exception as e:
            logme(e)
            raise e
        if self.verboseCalc:
            print((self.vdict))

    def dictCalcReDoEmptyBucketPortfTBGAtVectorCol(self, portfName, tbSK,
            kCurr):

        # MM See calcSpace.Refresh()
        try:
            ael.poll()  # 'Port ACM Roll, replace ael.poll()'
            # Must Refresh() after insert. #Execute all outstanding
            # background work.
            self.cs.Refresh()
            # Bucket Row. Iterator
            treeIterator = self.top_node.Iterator()
            if treeIterator.HasChildren():
                # Get first bucket
                childIterator = treeIterator.FirstChild()
                while (childIterator):
                    # TB Sparse
                    # Sparse buckets PortfSheet. Cannot save empty Zero cells
                    # for MM recalc.
                    try:
                        ctifchiFTIter_FTreePx = childIterator.Tree()
                        tn = ctifchiFTIter_FTreePx.Item()
                        tnSK = tn.StringKey()
                        if tnSK != tbSK:
                            # Spin, N ReCalc
                            childIterator = childIterator.NextSibling()
                            continue
                        else:
                            # Previously TB t + 1 was empty w/o trades. Now
                            # TB t + 1 exists non-empty, has MM trades.
                            # Must CreateCalc on curr in this tb row.
                            colDataT = self.colDataParamsDict[kCurr]
                            config = (acm.Sheet().Column().
                                    ConfigurationFromVector(colDataT))
                            calcChildnx = self.cs.CreateCalculation(
                                    childIterator.Tree(), self.colName, config)
                            ael.poll()  # 'Port ACM, replace ael.poll()'
                            # ngself.cs.Refresh()  #Must Refresh() < before
                            # iter, after insert. #Execute all outstanding
                            # background work.
                            val = calcChildnx.Value()
                            if val.Unit().Text() != kCurr:
                                # Check denom unit against col
                                print(('Unit() differs from column {0} '
                                      '{1}'.format(val.Unit(), kCurr)))
                                raise Exception('ee')
                            fvn = calcChildnx.Value().Number()
                            k = kCurr + '^' + tnSK  # Key curr tb
                            if self.verboseCalc:
                                print(('ReDoEmptyBucket reCalcCellDict {0} {1} '
                                        '{2} {3} {4}'.format(k, calcChildnx,
                                        tnSK, val, fvn)))
                            # MM ReCalc needs calccelldict, hitNz onward.
                            self.reCalcCellDict[k] = calcChildnx
                            self.vdict[k] = fvn
                    except Exception as e:
                        raise e
                    childIterator = None  # break
        except Exception as e:
            logme(e)
            raise e
        if self.verboseCalc:
            print((self.vdict))
        return fvn

    def setReCalcCell(self):
        self.reCalcCell = True

    def setReCalcGenDirtyDict(self, kRow, kCurr):
        self.subcolReCalcGenDirtyDict[kCurr] = True

    def getPortfRowDateCurr_ColReCalcCS(self, kPortf, kRow, kCurr):
        k = kCurr + "^" + kRow
        # Handle recalc, also consider tree nodes sparse.
        if self.subcolReCalcGenDirtyDict[kCurr]:
            try:
                # Sparse.
                # Prevously TB t + 1 was empty w/o trades. Now TB t + 1
                # exists non-empty, has MM trades .
                if k not in self.reCalcCellDict:
                    if self.verboseCalc:
                        print(('ReDoEmptyBucket {0}'.format(k)))
                    fvn = self.dictCalcReDoEmptyBucketPortfTBGAtVectorCol(None,
                            kRow, kCurr)
                    # Verify, value s/b t + 1 with new trade in previously
                    # empty bucket.
                    return fvn
                else:
                    # Sparse, here row exists
                    calcChildnx = self.reCalcCellDict[k]
                    val = calcChildnx.Value()
                    # Verify, val s/b t + 1 with additional trade in existing
                    # bucket.
                    fvn = calcChildnx.Value().Number()
                    if self.verboseCalc:
                        logme("ReCalc col node key val fvn: %s %s %s %s" %
                               (calcChildnx, k, val, fvn))
            except:
                fvn = 'NotFound'  # Weekend
                if self.verboseCalc:
                    print(('ReCalc NotFound {0} {1} {2}'.format(k, fvn,
                            self.reCalcCellDict)))
            return fvn
        else:
            try:
                if self.verboseCalc:
                    logme("col key: %s %s" % (kCurr, k))
                # Verify, value s/b t + 1 with new trade in previously empty
                # bucket.
                v = self.vdict[k]
            except:
                v = 'NotFound'
            if self.verboseCalc:
                print(('ReCalc get value of key {0} {1} {2}'.format(kCurr, k,
                        v)))
            return v

    def createCalcSpace_SheetType(self, csSheet):

        self.csSheet = csSheet
        self.cs = acm.FCalculationSpace(csSheet)

    def addPaymentsBucket(self, projPaymentsData, currency):

        # vector col for cashflows
        projPaymentsDataBucket = acm.FNamedParameters()
        projPaymentsDataBucket.AddParameter('currency',
                acm.FCurrency[currency])
        # 'currency' is the same key used in the column definition
        projPaymentsData.Add(projPaymentsDataBucket)

    def paymentsCol_AddPaymentsBucket(self, colNames, currencyL, sheetType):
        # vector col for cashflows
        projPaymentsData = acm.FArray()
        for i in range(len(currencyL)):
            self.addPaymentsBucket(projPaymentsData, currencyL[i])
        return projPaymentsData


def prtFTimeBuckets(bucks):

    print(('FTimeBuckets Properties {0}'.format(bucks.Properties())))
    print(('SpotDays {0} {1} StartDate {2}'.format(bucks, bucks.GetSpotDays(),
            bucks.GetStartDate())))
    print(('DefaultStartDate {0} CalendarSources {1}'.format(
            bucks.IsUsingDefaultStartDate(), bucks.GetCalendarSources())))
    print(('BucketNames {0} BucketSpecs {1}'.format(bucks.GetBucketNames(),
            bucks.GetBucketSpecs())))


def dumpDList(rptPfrc, portfName, dlist, col):

    for di in range(len(dlist)):
        ds = dlist[di]
        rptPfrc.getPortfRowCol(portfName, ds, col)


def displayTreeNode(tn):
    try:
        print(("tn {0} {1}".format(tn.Builder(), tn.Trades())))
        print(("tn {0} {1} {2} {3} {4}".format(tn.Value(), tn,
                tn.IsEvaluator(), tn.Elements(), tn.IsSimulated())))
        print(("tn {0} {1} {2}".format(tn.StringKey(), tn.DotString(),
                tn.Children())))
    except Exception:
        pass
