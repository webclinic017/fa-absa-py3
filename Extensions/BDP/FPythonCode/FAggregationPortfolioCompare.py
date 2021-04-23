""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/aggr_arch/etc/FAggregationPortfolioCompare.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
    FAggregationPortfolioCompare

DESCRIPTION
    This module includes methods for comparing Profit and Loss values before
    and after aggregation has been performed. Uses the module FReporting for
    generating reports on P/L values and the module FPortfolioComparison for
    comparing the generated reports.

NOTE
    The modules uses the aggregation rules set up in the PRIME Explorer, BDP,
    Aggregation Rules.


ENDDESCRIPTION
----------------------------------------------------------------------------"""

import collections
import string


import acm


import FPortfolioComparison
import importlib
importlib.reload(FPortfolioComparison)
import FReporting
importlib.reload(FReporting)
from FBDPCurrentContext import Logme

CURRENCY_DISPLAY_LABEL = 'DispCurr'

#orig_len are the original column width
_ColumnProps = collections.namedtuple(
    'ColumnProperties', 'dict_name col_name orig_len'
)
_columnProperties = (
    _ColumnProps(dict_name='column', col_name='Column Name', orig_len=15),
    _ColumnProps(dict_name='old_val', col_name='Value Before', orig_len=21),
    _ColumnProps(dict_name='new_val', col_name='Value After', orig_len=21),
    _ColumnProps(dict_name='abs_diff', col_name='Absolute Difference',
        orig_len=21),
    _ColumnProps(dict_name='rel_diff', col_name='Relative Difference',
        orig_len=21),
    _ColumnProps(dict_name='currency', col_name='Currency', orig_len=3),
)

allBuiltInPortfolioGroupers = acm.Risk.GetAllBuiltInPortfolioGroupers()


groupingCriteriaGroupers = {
    'Acquirer': acm.FAttributeGrouper('Trade.Acquirer'),
    'Counterparty': acm.FAttributeGrouper('Trade.Counterparty'),
    'Market': acm.FAttributeGrouper('Trade.Market'),
    'Trader': acm.FAttributeGrouper('Trade.Trader'),
    'Broker': acm.FAttributeGrouper('Trade.Broker'),
    'Trade Currency': acm.FAttributeGrouper('Trade.Currency'),
    'Contract Trade': acm.FAttributeGrouper('Trade.ContractTrdnbr'),
    'Trade Key 1': acm.FAttributeGrouper('Trade.OptKey1'),
    'Trade Key 2': acm.FAttributeGrouper('Trade.OptKey2'),
    'Trade Key 3': acm.FAttributeGrouper('Trade.OptKey3'),
    'Trade Key 4': acm.FAttributeGrouper('Trade.OptKey4'),
    'Buy/Sell': allBuiltInPortfolioGroupers.At('Trade BuySell')
}


# (for run_portfolio_reports())
_DEFAULT_COLUMN_NAMES = [
    'Portfolio Position',
    'Portfolio Average Price',
    'Portfolio Mean',
    'Portfolio Total Profit and Loss',
    'Portfolio Realized Profit and Loss',
    'Portfolio Unrealized Profit and Loss',
    'Portfolio Fees',
    'Portfolio Dividends',
    'Portfolio Funding',
    'Portfolio Accrued Interest',
    'Portfolio Settled Interest'
]


def _getGroupingNames(aggRule):
    """
    Given the aggregation rule, look up the grouping criteria, then put them
    into a list.
    """

    # Must at least contain the trade portfolio as a grouper.
    groupingNames = ['Trade.Portfolio']
    # Get the name list from the grouping criteria.
    groupingStr = aggRule.GroupingCriteria()
    groupingStr = groupingStr.strip('\"')
    if groupingStr:
        groupingList = groupingStr.split(',')
        groupingNames += [g.strip(' \"') for g in groupingList]
    # Make the list unique
    uniqueList = []
    for g in groupingNames:
        if g not in uniqueList:
            uniqueList.append(g)
    groupingNames = uniqueList
    return groupingNames


def _getAllAggRuleNameFilterGroupingNamesList():
    """
    Find all aggregation rules and return a list of tuples which consists of:
        (1) aggregation rule number/name (an integer string)
        (2) aggregation filter
        (3) the grouping names for the aggregation rule
    Note, this funciton relies on acm.FAggregationRule.Instances() to generate
    a list which is in the ascending order of aggregation rule numbers/names.
    """
    allAggRuleNameFilterNameGroupingNamesList = []
    aggRules = acm.FAggregationRule.Instances()
    for aggRule in aggRules:
        aggRuleName = aggRule.Name()  # is an integer string
        aggRuleFilterNumber = aggRule.Fltnbr()
        aggRuleFilter = acm.FTradeSelection[aggRuleFilterNumber]
        groupingNames = _getGroupingNames(aggRule)
        allAggRuleNameFilterNameGroupingNamesList.append(
                (aggRuleName, aggRuleFilter, groupingNames))
    return allAggRuleNameFilterNameGroupingNamesList


def _getRepresentingGrouper(groupingNames):
    """
    Given the grouperNames, return a representing grouper for the default
    or built-in groupers specified in the list.
    """

    # Transform grouping name list into grouper list
    grouperList = []
    for g in groupingNames:
        if g == 'Trade.Portfolio':
            grouperList.append(acm.FAttributeGrouper('Trade.Portfolio'))
        elif g in groupingCriteriaGroupers:
            grouperList.append(groupingCriteriaGroupers[g])
        else:
            raise ValueError('Unable to find default or built-in grouper for '
                             '%s in %s' % (g, groupingNames))

    # Return the only grouper or the synthesised chained grouper from the list.
    if len(grouperList) == 1:
        return grouperList[0]
    return acm.CreateWithParameter('FChainedGrouper', grouperList)


def _getAggRuleNameToGroupingNamesMap():
    """
    Find all aggregation rule and return a dict that maps
        from (a) aggregation rule number/name (an integer string)
        to   (b) the grouping names for the aggregation rule.
    """
    aggRuleNameToGroupingNamesMap = {}
    aggRules = acm.FAggregationRule.Instances()
    for aggRule in aggRules:
        aggRuleName = aggRule.Name()  # is an integer string
        groupingNames = _getGroupingNames(aggRule)
        aggRuleNameToGroupingNamesMap[aggRuleName] = groupingNames
    return aggRuleNameToGroupingNamesMap


def _getAggRuleFilterNameToAggRuleNameMap():
    """
    Find all aggregation rule and return a dict that mpas
        from (a) aggregation rule filter name
        to   (b) aggregation rule number/name (an integer string).
    """
    aggRuleFilterNameToAggRuleNameMap = {}
    aggRules = acm.FAggregationRule.Instances()
    for aggRule in aggRules:
        aggRuleName = aggRule.Name()
        aggRuleFilterNumber = aggRule.Fltnbr()
        aggRuleFilter = acm.FTradeSelection[aggRuleFilterNumber]
        aggRuleFilterName = aggRuleFilter.Name()
        aggRuleFilterNameToAggRuleNameMap[aggRuleFilterName] = aggRuleName
    return aggRuleFilterNameToAggRuleNameMap


def _getAggRuleFltnbrToReprGrouperMap():
    """
    Find all aggregation rules and return a dict that maps
        from (a) aggregation rule filter number
        to   (b) the representing grouper for grouping criteria.
    """
    aggRuleFltnbrToReprGrouperMap = {}
    aggRules = acm.FAggregationRule.Instances()
    for aggRule in aggRules:
        aggRuleFilterNumber = aggRule.Fltnbr()
        groupingNames = _getGroupingNames(aggRule)
        reprGrouper = _getRepresentingGrouper(groupingNames)
        aggRuleFltnbrToReprGrouperMap[aggRuleFilterNumber] = reprGrouper
    return aggRuleFltnbrToReprGrouperMap


def _sortDiffResult(diffResult):
    """
    Sort the diff result into our format.  The diffResult passed in is a dict
    that key'ed on the column.  We need to transform it so the returned dict
    is key'ed on the position instead.
    """
    currencies = []
    currencyResults = diffResult.pop(CURRENCY_DISPLAY_LABEL, None)
    if currencyResults:
        for diffList in currencyResults:
            if diffList[-1] != diffList[-2]:
                msg = 'Currencies differ: %s before vs %s after' % \
                    diffList[-2:]
                raise Exception(msg)

            currencies.append(diffList[-1])

    posDict = {}
    for (column, diffLists) in diffResult.iteritems():
        for i, diffList in enumerate(diffLists):
            valueDict = {}
            posName = diffList[0]
            valueDict['column'] = column
            valueDict['abs_diff'] = diffList[1]
            valueDict['rel_diff'] = diffList[2]
            valueDict['new_val'] = diffList[3]
            valueDict['old_val'] = diffList[4]
            valueDict['currency'] = currencies[i] if currencies else None
            # For new posName, create a entry with empty list to append.
            if posName not in posDict:
                posDict[posName] = []
            posDict[posName].append(valueDict)
    # The return dict is now key'ed on the position.
    return posDict


def _getAggRuleNameOrFilterNameSuffix(filterName,
                                       aggRuleFilterNameToAggRuleNameMap):
    if filterName in aggRuleFilterNameToAggRuleNameMap:
        aggRuleName = aggRuleFilterNameToAggRuleNameMap[filterName]
        suffix = '_Rule' + str(aggRuleName)
    else:
        suffix = '_Filter' + str(filterName)
    return suffix


def _getAggRuleNameOrFilterNameText(filterName,
                                     aggRuleFilterNameToAggRuleNameMap):
    if filterName in aggRuleFilterNameToAggRuleNameMap:
        aggRuleName = aggRuleFilterNameToAggRuleNameMap[filterName]
        text = 'Aggregation Rule ' + str(aggRuleName)
    else:
        text = 'Filter ' + str(filterName)
    return text


def _getDiffResultTitleString(filterName, aggRuleFilterNameToAggRuleNameMap,
                               groupingNames):
    """
    Given the filter name, and the corresponding grouping name list,
    synthesise the title string.
    The aggregation rule name will be used if the filer belongs to an
    aggregation rule, otherwise the filter name will be used instead.
    """
    titleString = ('P/L values in the following positions differ before and '
                   'after aggregation according to ')
    titleString += '\n' + _getAggRuleNameOrFilterNameText(filterName,
                                     aggRuleFilterNameToAggRuleNameMap)
    # Note that the groupingNames' first grouper is always the
    # 'Trade.Portfolio'.  It should not be counted, as it is not part of the
    # grouper in the aggregation rule.
    if len(groupingNames) <= 1:
        return titleString
    # Quote the grouping names and separate them with comma, finally add it to
    # the title string.
    quotedGroupingNames = ['\'' + name + '\'' for name in groupingNames[1:]]
    titleString += ', grouping by ' + string.join(quotedGroupingNames, ', ')
    return titleString


def _getDiffResultPosNameString(portName, grouperNames, insName):
    """
    Given the portfolio name, grouper names and instrument name, synthesise
    the position name string.
    """

    posNameString = '\n\n '
    # For portfolio name, grouper names and instrument name, synthesise each
    # string independently if the name is present, and put the synthesised
    # string into a list.
    synthStringList = []
    if portName:
        synthStringList.append('  Portfolio: \'' + portName + '\'')
    if grouperNames:
        quotedGrouperNames = ['\'' + name + '\'' for name in grouperNames]
        synthStringList.append('  Grouping: ' +
                               string.join(quotedGrouperNames, ' '))
    if insName:
        synthStringList.append('  Instrument: \'' + insName + '\'')
    # Joining the synthesised string list with comma.
    posNameString += string.join(synthStringList, ',') + '\n'
    return posNameString


def _getDiffResultTableString(valueDicts):
    """
    Given the table values (in dicts), synthesise the value table.

    The table roughly resembles the following:

        Column     WWWWwwww    XXXXxxxx    YYYYyyyy    ZZZZzzzz
        -------    --------    --------    --------    --------
        Row1       value       value       value       value
        Row2       value       value       value       value

    Note, if the printed value is wider then the original designated column
    width, the column width extends automatically to accommodate the whole
    printed value.
    """
    # Scan the table to extends column width.
    fieldWidths = []
    dictNames = []
    colNames = []
    for cp in _columnProperties:
        maxLength = max(len(str(dct[cp.dict_name])) for dct in valueDicts)
        fieldWidths.append(max(maxLength, cp.orig_len, len(cp.col_name)))
        dictNames.append(cp.dict_name)
        colNames.append(cp.col_name)

    # Create the template from column widths
    resultTableTemplateString = '\n      '
    for i, fw in enumerate(fieldWidths):
        resultTableTemplateString += '{%d:<%d} ' % (i, fw)

    resultTableTemplateString.rstrip()
    resultTableHeaderString1 = resultTableTemplateString.format(*colNames)
    underlinings = ['-' * len(cn) for cn in colNames]
    resultTableHeaderString2 = resultTableTemplateString.format(*underlinings)
    tableString = resultTableHeaderString1 + resultTableHeaderString2
    # Put in table values.
    for valueDict in valueDicts:
        result = [valueDict[dn] for dn in dictNames]
        tableString += resultTableTemplateString.format(*result)

    return tableString


def _getDiffResultString(diffResult, aggRuleFilterNameToAggRuleNameMap,
                          aggRuleNameToGroupingNamesMap):
    """
    For the given diff result, first transform the table from column based
    tables into position based tables, then each position is iterated through,
    and the results are printed as tables into the string.
    """

    # Transform the diff result into the format we need.
    posDict = _sortDiffResult(diffResult)

    isTitlePrinted = False
    result_string = ""
    for (posName, valueDicts) in posDict.iteritems():
        # The following shows some example of position name:
        #      *  ~AggRule_1296806791.9^ALEARO00^AB Industrivarden^LMOld
        #      *  ~AggRule_1298291459.69^HMCFD^HM-BMW-CFD
        #      *  ~AggRule_1298022537.29^FX-EUR-JPY^USD/JPY
        # It is a '^' separated list, consists of:
        #     (1) Filter name
        #     (2) Portfolio name
        #     (3) Zero or more grouping name(s)
        #     (4) Instrument name (optinal)
        posNameList = posName.split('^')
        # Find (1) aggregation rule filter name
        filterName = posNameList.pop(0)  # pop from front
        if filterName in aggRuleFilterNameToAggRuleNameMap:
            aggRuleName = aggRuleFilterNameToAggRuleNameMap[filterName]
            groupingNames = aggRuleNameToGroupingNamesMap[aggRuleName]
        else:
            aggRuleName = None
            groupingNames = None

        # Find (2) portfolio name
        portName = None
        if posNameList:
            portName = posNameList.pop(0)  # pop from front
        # Find (4) instrument names
        insName = None
        if posNameList:
            lastItem = posNameList[-1]
            if lastItem and (acm.FInstrument[lastItem] or
                             acm.FCurrencyPair[lastItem]):
                insName = posNameList.pop()  # pop from back
        # Find (3) grouper names
        grouperNames = None
        if posNameList:
            grouperNames = posNameList
        # Now all the parameters are found.
        # Print the title string (just once)
        if not isTitlePrinted:
            result_string = _getDiffResultTitleString(
                                    filterName,
                                    aggRuleFilterNameToAggRuleNameMap,
                                    groupingNames)
            isTitlePrinted = True
        # Print the rest of parameter
        if portName or grouperNames or insName:
            result_string += _getDiffResultPosNameString(portName,
                                                          grouperNames,
                                                          insName)
            result_string += _getDiffResultTableString(valueDicts)

    return (result_string + '\n\n\n') if result_string else ""


def get_aggregation_rule_fltnbr_grouper_pair_list(aggRuleFltnbrList):
    """
    Given a list of aggregation rules' filter numbers, find the representing
    grouper for the rules' grouping criteria, and return in a list of
    pairs of aggregation rule filter number and representing grouper.
    """
    aggRuleFltnbrToReprGrouperMap = _getAggRuleFltnbrToReprGrouperMap()
    aggRuleFltnbrReprGrouperList = []
    for fltnbr in aggRuleFltnbrList:
        if fltnbr not in aggRuleFltnbrToReprGrouperMap:
            raise ValueError('Filter number {0} does not belongs to any '
                             'aggregation rule'.format(fltnbr))
        aggRuleFltnbrReprGrouperList.append(
            (fltnbr, aggRuleFltnbrToReprGrouperMap[fltnbr]))
    return aggRuleFltnbrReprGrouperList


def run_portfolio_reports(fltnbrGrouperPairList, filePath, fileName,
                          usedContext, sheets,
                          name="Aggregation Portfolio Report",
                          snapshot=1):
    """
    Given the filter/grouper pair list, iterate through the list and run
    create portfolio report on each of them.
    """

    # Pre calculate look-up maps.
    aggRuleFilterNameToAggRuleNameMap = \
        _getAggRuleFilterNameToAggRuleNameMap()
    # Define the columns
    columns = []
    if sheets:
        createContext = acm.FColumnCreatorCreateContext(usedContext)
        for s in sheets:
            cc = [str(c.ColumnId()) for c in s.ColumnCollection(createContext)
                                    if not str(c.ColumnId()) in columns]
            columns.extend(cc)
    else:
        columns = _DEFAULT_COLUMN_NAMES

    if 'Portfolio Currency' not in columns:
        columns.append('Portfolio Currency')

    # Iterate the list and create reports.
    for (fltnbr, grouper) in fltnbrGrouperPairList:
        fltr = acm.FTradeSelection[fltnbr]
        filterName = fltr.Name()
        # If possible, use the aggregation rule name instead of filter name.
        suffix = _getAggRuleNameOrFilterNameSuffix(
                         filterName,
                         aggRuleFilterNameToAggRuleNameMap)
        suffixAppendedFileName = fileName + suffix
        # Now run the report
        FReporting.createPortfolioReport(
            columns,
            [fltr],
            grouperNames=[grouper],  # This function allows the client code to
                                     # specify the groupers by passing these
                                     # groupers by using one representing
                                     # grouper in a single element list.
            context=usedContext,
            filePath=filePath,
            fileName=suffixAppendedFileName,
            name=name,
            createDateDirectory=0,
            includeExpired=1,
            xmlToFile=True,
            htmlToFile=True,
            snapshot=snapshot,
            matchPerPortfolio=1)
    return


def compare_reports(fltnbrGrouperPairList, filePath, fileName1, fileName2,
                    absPrec=0.0001, relPrec=0.0001,
                    ignorePrecsion=0):
    """
    Given the filter/grouper pair list, iterate through the list and run
    diff on the portfolio report of each of them.
    """
    result_string = ""
    # Pre calculate look-up maps.
    aggRuleFilterNameToAggRuleNameMap = \
        _getAggRuleFilterNameToAggRuleNameMap()
    aggRuleNameToGroupingNamesMap = _getAggRuleNameToGroupingNamesMap()
    # Iterate the list and create reports.
    for (fltnbr, grouper) in fltnbrGrouperPairList:
        fltr = acm.FTradeSelection[fltnbr]
        filterName = fltr.Name()
        # If possible, use the aggregation rule name instead of filter name.
        suffix = _getAggRuleNameOrFilterNameSuffix(
                         filterName,
                         aggRuleFilterNameToAggRuleNameMap)
        reportName1 = filePath + fileName1 + suffix + '.xml'
        reportName2 = filePath + fileName2 + suffix + '.xml'
        outputFile = filePath + 'diff_portfolio_report' + suffix
        requiredCols = [CURRENCY_DISPLAY_LABEL]
        diffResult = FPortfolioComparison.diff(reportName1, reportName2,
                                               outputFile, bool(grouper),
                                               absPrec, relPrec,
                                               ignorePrecsion,
                                               requiredCols=requiredCols)
        if diffResult:
            diff_string = _getDiffResultString(
                                 diffResult,
                                 aggRuleFilterNameToAggRuleNameMap,
                                 aggRuleNameToGroupingNamesMap)
            if diff_string:
                result_string += diff_string
                Logme()(
                    'Found a difference before and after aggregation in ' +
                    _getAggRuleNameOrFilterNameText(
                          filterName, aggRuleFilterNameToAggRuleNameMap),
                    'DEBUG')
    return result_string
