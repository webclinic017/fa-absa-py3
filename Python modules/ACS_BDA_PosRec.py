
'''-----------------------------------------------------------------------
MODULE
    iMatch feed file for ACS Stock/ETF positions

DESCRIPTION


    Date                : 2010-10-14, 2010-10-21, 2011-01-20, 2011-08-23
    Purpose             : iMatch stock recon feed for ACS
                          Removed the adding of the date to the filename input parameter - was causing RTB scripts to fail on backend when moving file
                          Corrected the pickup of outstanding dividends to sum if more than one declaration for a date - was only returning the last one previously
                          Changed the calculation of the fwdInt column - information supplied by Marli regarding what reports they use to recon and how that particular
                            figure is calculated.
                          Minor adjustment post upgrade where calc_space has to be recreated before the valuation override would take effect
                          PS Desk strategies include strategy name in the assign info - recon requires just the bda code for this column
                          Pulling Settled and Unsettled dividends from calculation space (ACSSettledDividends, ACSUnsettledDividends).
    Department and Desk : PCG Equities
    Requester           : Andrew Nobbs, Marli Penzhorn, Reletile Kekana
    Developer           : Anwar Banoo, Jan Sinkora
    CR Number           : 464804, 470929, 551711, 702999, 746813, PSB-216, 1965671

ENDDESCRIPTION
-----------------------------------------------------------------------'''
import acm, ael

today = ael.date_today()
expDivDict = acm.FDictionary()
endPriceDict = acm.FDictionary()
outputList = acm.FDictionary()

ael_variables = [ ['Filter', 'Select Filter', 'string', None, 'IMATCH_ACS', 1],
                  ['Date', 'Date', 'string', ael.date_today(), ael.date_today()],
                  ['Filename', 'File Name', 'string', None, 'ACS_BDA_PosRec', 1],
                  ['Filepath', 'File Path', 'string', None, 'F:\\', 1]]



vp_eq = acm.FValuationParameters.Select01('name = VP_EQ', '')
vp_std = acm.FValuationParameters.Select01('name = PROPOSED_VP_bonds', '')


def _produceTMSheet(filter, fileName, runDate):

    GROUPER_NAME = ['Trade Portfolio']
    SHEET_TYPE = 'FPortfolioSheet'
    INSTRUMENTNAME = 'Instrument Name'
    POSITIONEND = 'Portfolio Profit Loss Position End'
    TOTALVALEND = 'Total Val End'
    INSVALEND = 'InsValEnd'
    OSCASH = 'O/S_Cash'
    FEES = 'Portfolio Fees'
    DIVIDEND = 'Portfolio Dividends'
    ACSDIVIDEND = 'ACSDividend'
    UNSETTLEDEXERCISECASH = 'ACSUnsettledExerciseCash'
    CASHEND = 'Portfolio Cash End'
    PLPERIODSTART = 'PLPeriodStart'
    PLPERIODEND = 'PLPeriodEnd'
    TYPE = 'Instrument Type'
    USEDPRICEEND = 'Portfolio Profit Loss Price End Date'
    REALISEDFEES = 'Portfolio Fees Realized'
    ACSSETTLEDDIVIDEND = 'ACSSettledDividends'
    ACSUNSETTLEDDIVIDEND = 'ACSUnsettledDividends'
    ACSPVUNSETTLEDDIVIDEND = 'ACSPVUnsettledDividends'
    ACSPVUNSETTLEDEXERCISECASH = 'ACSPVUnsettledExerciseCash'

    tradeFilter = acm.FTradeSelection[filter]
    context = acm.GetDefaultContext()
    calc_space = acm.Calculations().CreateCalculationSpace(context, SHEET_TYPE)

    def getColumn(node, column_name):
        return calc_space.CalculateValue(node, column_name)

    def createSheet():
        calc_space.Clear()
        top_node = calc_space.InsertItem(tradeFilter)
        top_node.ApplyGrouper(acm.Risk().GetGrouperFromName(GROUPER_NAME))
        applyGlobalSimulation()

    def applyGlobalSimulation():
        calc_space.SimulateGlobalValue('Portfolio Profit Loss End Date', 'Custom Date')
        calc_space.SimulateGlobalValue('Portfolio Profit Loss End Date Custom', runDate)
        calc_space.Refresh()

    def clearGlobalSimulation():
        calc_space.RemoveGlobalSimulation('Portfolio Profit Loss End Date')
        calc_space.RemoveGlobalSimulation('Portfolio Profit Loss End Date Custom')
        calc_space.Refresh()

    def getPositionAtDate(node, column_name, date):
        calc_space.SimulateGlobalValue('Portfolio Profit Loss End Date', 'Custom Date')
        calc_space.SimulateGlobalValue('Portfolio Profit Loss End Date Custom', date)
        calc_space.Refresh()
        try:
            retVal = getColumn(node, column_name)
            applyGlobalSimulation()
            return retVal
        except:
            applyGlobalSimulation()
            return 0

    def getDividendOutstanding(Instrument):
        divVal = acm.FDictionary()

        selection = "instrument = '%s' and payDay > '%s' and exDivDay <= '%s'" %(Instrument, runDate, runDate)
        dividends = acm.FDividend.Select(selection)
        for div in dividends:
            if divVal.HasKey(div.ExDivDay()):
                divVal[div.ExDivDay()] += div.Amount()
            else:
                divVal[div.ExDivDay()] = div.Amount()

        return divVal

    def getExpectedDividend(node, expDivDict):
        expDiv = 0
        aelIns = ael.Instrument[Instrument]
        aelPort = ael.Portfolio[portfolioName]
        for date in expDivDict.Keys():
            positionDate = ael.date_from_string(date).add_days(-1)
            positionAtDate = getPositionAtDate(node, POSITIONEND, positionDate)
            expDiv += positionAtDate * expDivDict[date]

        return expDiv

    def update_vp_ws_override(vp):
        u = acm.User().Oid()
        exist = False
        for pm in acm.FParameterMapping.Select('user = %i' %u):
            if pm.OverrideLevel() == 'Workspace' :
                for i in pm.ParMappingInstances():
                    if i.ParameterType() == 'Valuation Par':
                        exist = True
                        i.ValuationParameters(vp)
                        try:
                            i.Commit()
                        except Exception, e:
                            ael.log('Could not change workspace parameter override: ' + e.message)


        if not exist:
            pm_new = acm.FParameterMapping()
            pm_new.OverrideLevel('Workspace')
            pmi_new = acm.FParMappingInstance(pm_new)
            pmi_new.ParameterType('Valuation Par')
            pmi_new.ValuationParameters(vp)
            try:
                pmi_new.Commit()
            except Exception, e:
                ael.log('Could not change workspace parameter override: ' + e.message)



    outfile = open(fileName, 'a')

    createSheet()

    tradeFilterIterator = calc_space.RowTreeIterator().FirstChild()
    child_iter = tradeFilterIterator.FirstChild()

    update_vp_ws_override(vp_std)

    count = 0
    periodStart = None
    periodEnd = None

    while child_iter:
        portfolioName = child_iter.Tree().Item().StringKey()
        if portfolioName:
            portfolio = acm.FPhysicalPortfolio[portfolioName]
            assignInfo = portfolio.AdditionalInfo().Prt_BDA_AccountNum() if portfolio.AdditionalInfo().Prt_BDA_AccountNum() not in (None, '') else portfolio.AssignInfo()

            item = child_iter.Tree().Iterator().FirstChild()
            while item:
                Instrument = getColumn(item.Tree(), INSTRUMENTNAME)
                posEnd =  getColumn(item.Tree(), POSITIONEND)
                try:
                    valEnd =  getColumn(item.Tree(), TOTALVALEND).Number()
                except Exception, e:
                    ael.log('Error on valEnd: ' + str(e) + ' - default to zero')
                    valEnd = 0

                try:
                    insValEnd =  getColumn(item.Tree(), INSVALEND).Number()
                except Exception, e:
                    ael.log('Error on insValEnd: ' + str(e) + ' - default to zero')
                    insValEnd = 0

                try:
                    osCash =  getColumn(item.Tree(), OSCASH).Number()
                except Exception, e:
                    ael.log('Error on osCash: ' + str(e) + ' - default to zero')
                    osCash = 0

                try:
                    fees =  getColumn(item.Tree(), FEES).Number()
                except Exception, e:
                    ael.log('Error on fees: ' + str(e) + ' - default to zero')
                    fees = 0

                try:
                    acsdividend =  getColumn(item.Tree(), ACSDIVIDEND)
                except Exception, e:
                    ael.log('Error on dividend using ACS Dividend: ' + str(e))
                    try:
                        acsdividend =  getColumn(item.Tree(), DIVIDEND).Number()
                    except Exception, e:
                        ael.log('Error on dividend(acs) using Portfolio Dividend: ' + str(e) + ' - defaulting dividend to zero')
                        ascdividend = 0
                try:
                    dividend =  getColumn(item.Tree(), DIVIDEND).Number()
                except Exception, e:
                    ael.log('Error on dividend(core) using Portfolio Dividend: ' + str(e) + ' - defaulting dividend to zero')
                    dividend = 0


                try:
                    cashEnd =  getColumn(item.Tree(), CASHEND).Number()
                except Exception, e:
                    ael.log('Error on cashEnd: ' + str(e) + ' - default to zero')
                    cashEnd = 0

                if periodStart == None:
                    periodStart = getColumn(item.Tree(), PLPERIODSTART)
                    periodEnd = getColumn(item.Tree(), PLPERIODEND)

                instrumentType = getColumn(item.Tree(), TYPE)

                if not endPriceDict.HasKey(Instrument):
                    try:
                        endPriceDict[Instrument] = getColumn(item.Tree(), USEDPRICEEND).Number()
                    except Exception, e:
                        ael.log('Error on usedPriceEnd(1): ' + str(e) + ' - proceed to get float value')
                        try:
                            endPriceDict[Instrument] = getColumn(item.Tree(), USEDPRICEEND)
                        except Exception, e:
                            ael.log('Error on usedPriceEnd(2): ' + str(e) + ' - default price to zero')
                            endPriceDict[Instrument] = 0

                usedPriceEnd = endPriceDict[Instrument]
                try:
                    cleanPV = posEnd * usedPriceEnd / 100
                except Exception, e:
                    ael.log('Error on cleanPV: ' + str(e) + ' - default to zero')
                    cleanPV = 0

                try:
                    fwdInt = insValEnd - cleanPV
                except Exception, e:
                    ael.log('Error on fwdInt: ' + str(e) + ' - default to zero')
                    fwdInt = 0

                try:
                    feesRealised =  getColumn(item.Tree(), REALISEDFEES).Number()
                except Exception, e:
                    ael.log('Error on feesRealised: ' + str(e) + ' - default to zero')
                    feesRealised = 0

                try:
                    expectedFees = fees - feesRealised
                except Exception, e:
                    ael.log('Error on expectedFees: ' + str(e) + ' - default to zero')
                    expectedFees = 0

                if not expDivDict.HasKey(Instrument):
                    expDivDict[Instrument] = getDividendOutstanding(Instrument)

                try:
                    unsettledExerciseCash =  getColumn(item.Tree(), UNSETTLEDEXERCISECASH)
                except Exception, e:
                    ael.log('Error on unsettledExerciseCash: ' + str(e) + ' - default to zero')
                    unsettledExerciseCash = 0

                try:
                    expectedDividend = getColumn(item.Tree(), ACSUNSETTLEDDIVIDEND)
                except Exception, e:
                    ael.log('Error on expectedDividend: ' + str(e) + ' - default to zero')
                    expectedDividend = 0

                try:
                    unsettledExerciseCashPV =  getColumn(item.Tree(), ACSPVUNSETTLEDEXERCISECASH)
                except Exception, e:
                    ael.log('Error on unsettledExerciseCashPV: ' + str(e) + ' - default to zero')
                    unsettledExerciseCashPV = 0

                try:
                    unsettledDividendPV =  getColumn(item.Tree(), ACSPVUNSETTLEDDIVIDEND)
                except Exception, e:
                    ael.log('Error on unsettledDividendPV: ' + str(e) + ' - default to zero')
                    unsettledDividendPV = 0

                try:
                    expectedDividendPV = getColumn(item.Tree(), ACSPVUNSETTLEDDIVIDEND)
                except Exception, e:
                    ael.log('Error on expectedDividendPV: ' + str(e) + ' - default to zero')
                    expectedDividendPV = 0

                try:
                    paidDividend = getColumn(item.Tree(), ACSSETTLEDDIVIDEND)
                except Exception, e:
                    ael.log('Error on paidDividend: ' + str(e) + ' - default to zero')
                    paidDividend = 0

                try:
                    cleanCash = cashEnd - paidDividend - feesRealised
                except Exception, e:
                    ael.log('Error on cleanCash: ' + str(e) + ' - default to zero')
                    cleanCash = 0

                key = portfolioName + Instrument
                outputList[key] = ['%s,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%s,%s,%s,%s,%.2f,%s,%.2f' %(Instrument, posEnd, valEnd, insValEnd, osCash,
                              fees, feesRealised, expectedFees, dividend, acsdividend, paidDividend, expectedDividend, expectedDividendPV, cashEnd, periodStart, periodEnd,
                              instrumentType, portfolioName, usedPriceEnd, assignInfo, cleanPV), cleanCash, valEnd, cashEnd]

                item = item.NextSibling()

        child_iter = child_iter.NextSibling()


    update_vp_ws_override(vp_eq)

    calc_space = acm.Calculations().CreateCalculationSpace(context, SHEET_TYPE)
    createSheet()

    tradeFilterIterator = calc_space.RowTreeIterator().FirstChild()
    child_iter = tradeFilterIterator.FirstChild()

    while child_iter:
        portfolioName = child_iter.Tree().Item().StringKey()
        if portfolioName:
            item = child_iter.Tree().Iterator().FirstChild()
            while item:
                Instrument = getColumn(item.Tree(), INSTRUMENTNAME)
                try:
                    _valEnd =  getColumn(item.Tree(), TOTALVALEND).Number()
                except Exception, e:
                    ael.log('Error on _valEnd: ' + str(e) + ' - default to zero')
                    _valEnd = 0

                try:
                    _cashEnd =  getColumn(item.Tree(), CASHEND).Number()
                except Exception, e:
                    ael.log('Error on _cashEnd: ' + str(e) + ' - default to zero')
                    _cashEnd = 0

                key = portfolioName + Instrument
                lineItem = outputList[key]

                fwdInt = (lineItem[2] + lineItem[3]) - (_cashEnd + _valEnd)
                cleanCash = lineItem[1]

                outfile.write(lineItem[0] + ',%.2f,%.2f\n' %(fwdInt, cleanCash))

                item = item.NextSibling()

        child_iter = child_iter.NextSibling()

    update_vp_ws_override(vp_std)

    outfile.close()
    clearGlobalSimulation()


def ael_main(parameter):
    tradeFilter = parameter['Filter']
    outputName = parameter['Filename']
    outputPath = parameter['Filepath']
    try:
        if parameter['Date'].upper() == 'TODAY':
            runDate = ael.date_today()
        else:
            runDate = ael.date(parameter['Date'])
    except Exception, e:
        ael.log('Error parsing date input:' + str(e))
        raise Exception('Error parsing date input:' + str(e))

    fileName = outputPath + outputName

    outfile = open(fileName, 'w')
    outfile.write('Instrument, Pos End, Val End, Ins Val End, OS Cash, Fees, Fees Settled, Fees Unsettled, Dividend, ACS Dividend, ACSSettledDividends, ACSUnsettledDividends, ACSPVUnsettledDividends, Cash End, Period Start, Period End, Instrument Type, Portfolio Name, Price End, Assign Info, CleanPV, Fwd Int, Clean Cash\n')
    outfile.close()

    _produceTMSheet(tradeFilter, fileName, runDate)

    ael.log('Wrote secondary output to:::' + fileName)

