'''----------------------------------------------------------------------
Project: Prime Portal Project
Department: Prime Services
Requester: Francois Henrion
Developer: Rohan vand der Walt
CR Number: 889960 (Initial Deployment)

----------------------------------------------------------------------
HISTORY
================================================================================
Date        Change no   Developer               Description
--------------------------------------------------------------------------------
            889960      Rohan vand der Walt     Initial Implementation
            XXXXX       Rohan vand der Walt     Cash Utilization Processing
'''
import acm, re
from pprint import pprint
from xml.etree import ElementTree

import at_logging


LOGGER = at_logging.getLogger()


def _copyFormattedToRaw(xml):
    try:
        rd = ReportData(xml)
        reports = rd.getDataAsArray()

        for report in reports:
            for row in reports[report]:
                for cell in row[1]:
                    try:
                        cell[0][1].text = cell[0][0].text
                    except Exception:
                        LOGGER.exception("Failed to copy text.")
                        continue
        return rd.toXML()
    except Exception:
        LOGGER.exception("Failed to get data.")
        return xml

def _filterOutErrors(xml):
    try:
        rd = ReportData(xml)

        reports = rd.getDataAsArray()
        for report in reports:
            for row in reports[report]:
                for cell in row[1]:
                    try:
                        if cell[0][0].text in ['[]', 'NaN', '#']:
                            LOGGER.info('OLD: %s\tNEW:', cell[0][0].text)
                            cell[0][0].text = ''
                    except:
                        continue
        return rd.toXML()
    except:
        return xml

def _fixFormattingErrors(xml):
    try:
        pattern = r'^(-(0)*(\.)?(0)*)$'
        rd = ReportData(xml)
        reports = rd.getDataAsArray()
        for report in reports:
            for row in reports[report]:
                for cell in row[1]:
                    try:
                        myMatch = re.match(pattern, cell[0][0].text)
                        if myMatch:
                            new_text_val = cell[0][0].text.replace('-', '')
                            LOGGER.info('OLD:%s\tNEW:%s', cell[0][0].text, new_text_val)
                            cell[0][0].text = new_text_val
                    except:
                        continue
        return rd.toXML()
    except:

        return xml

class ReportData():
    root = None
    def __init__(self, xml):
        self.root = ElementTree.XML(xml)

    def _addRows(self, row, results, reportName):
        results[reportName].append([row.find('Label'), [[[cell.find('FormattedData'), cell.find('RawData')]] for cell in row.findall('Cells/Cell')]])
        if len(row.findall('Rows/Row')) > 0:
            for r in row.findall('Rows/Row'):
                    results = self._addRows(r, results, reportName)
        return results

    @staticmethod
    def _flatten(x):
        """flatten(sequence) -> list

        Returns a single, flat list which contains all elements retrieved
        from the sequence and all recursively contained sub-sequences
        (iterables).

        Examples:
        >>> [1, 2, [3,4], (5,6)]
        [1, 2, [3, 4], (5, 6)]
        >>> flatten([[[1,2,3], (42,None)], [4,5], [6], 7, MyVector(8,9,10)])
        [1, 2, 3, 42, None, 4, 5, 6, 7, 8, 9, 10]"""

        result = []
        for el in x:
            # if isinstance(el, (list, tuple)):
            if hasattr(el, "__iter__") and not isinstance(el, basestring):
                result.extend(ReportData._flatten(el))
            else:
                result.append(el)
        return result

    def getDataAsArray(self):
        '''
        Returns data including headers and row labels as a 2-dim array
        for e.g. reports["PS_Finance_Report-Finance Report"][3][0] wil get the 3rd row's row label of the 1st report. All values stored as Element
        '''
        reports = []
        results = {}
        if self.root.tag == 'PRIMEReport':
            reports.append(self.root)
        else:
            reports = self.root.findall('PRIMEReport')

        for report in reports:
            reportName = report.find('Name').text
            results[reportName] = []
            # Set Column headers
            results[reportName].append(ReportData._flatten([ '', [ i.find('Label') for i in report.findall('ReportContents/Table/Columns/Column')] ]))
            node = report.find('ReportContents/Table')
            if len(node.findall('Rows/Row')) > 0:
                for row in node.findall('Rows/Row'):
                    results = self._addRows(row, results, reportName)
        return results

    def getReportNode(self, reportName):
        reports = []
        if self.root.tag == 'PRIMEReport':
            reports.append(self.root)
        else:
            reports = self.root.findall('PRIMEReport')
        for report in reports:
            if reportName == report.find('Name').text:
                return report
        return None

    def getTreeDepth(self, reportName):
        reportNode = self.getReportNode(reportName)
        depth = [0, ]
        if reportNode:
            table = reportNode.find('ReportContents/Table')
            depth = ReportData._checkDepth(table, depth)
        return max(depth)

    @staticmethod
    def _checkDepth(row, depthList, d=0):
        if len(row.findall('Rows/Row')) >= 1:
            depth = d + 1
            depthList.append(depth)
            for r in row.findall('Rows/Row'):
                depthList = ReportData._checkDepth(r, depthList, d=depth)
        else:
            depth = -1
        return depthList

    def _getNodeDepth(self, node):
        count = 0
        while node:
            node = node.find('../parent')
            count += 1
        return count

    def toXML(self):
        return ElementTree.tostring(self.root)

def PreProcessXML(reportObj, param, xml):
    ''' Pre-Process the xml for the Prime Brokergae reports by adding elements for the portfolio start and end date and the party address.
        The party name is entered in the parameter field of the Processing tab.
        param = comma seperated values
        param[0] - Party name to extract address details...
        param[1] - Report name
        param[2] - (optional) Account name
    '''

    xml = _filterOutErrors(xml)
    xml = _fixFormattingErrors(xml)
    xml = _copyFormattedToRaw(xml)

    return xml


def returnTMValues(node, calc_space, column_id, prepend=""):
    results = {}
    def recurse_tree(node, calc_space, column_id, prepend):
        try:
            results[prepend + node.Item().StringKey()] = calc_space.CalculateValue(node, column_id).Number()
        except:
            results[prepend + node.Item().StringKey()] = calc_space.CalculateValue(node, column_id)
        if node.NumberOfChildren():
            child_iter = node.Iterator().FirstChild()
            while child_iter:
                recurse_tree(child_iter.Tree(), calc_space, column_id, prepend=prepend + node.Item().StringKey() + ';')
                child_iter = child_iter.NextSibling()
    recurse_tree(node, calc_space, column_id, prepend)
    return results


def _AddPnLToColumn(xml, tradeFilter):
    try:
        context = acm.GetDefaultContext()
        sheet_type = 'FPortfolioSheet'
        calc_space = acm.Calculations().CreateCalculationSpace(context, sheet_type)
        column_id = 'Client Daily TPL'
        grouper_name = 'Instrument Type'
        groupers = [ acm.Risk().GetGrouperFromName(grouper_name) ]
        chained_grouper = acm.FChainedGrouper(groupers)
        treeProxy = calc_space.InsertItem(acm.FTradeSelection[tradeFilter])
        treeProxy.ApplyGrouper(chained_grouper)
        portfolio_iter = calc_space.RowTreeIterator().FirstChild()
        result = returnTMValues(portfolio_iter.Tree(), calc_space, column_id)
        dailyPnl = result[tradeFilter]
        LOGGER.info('PnL: %s', dailyPnl)
        rd = ReportData(xml)
        reports = rd.getDataAsArray()
        for report in reports:
            for row in reports[report][1:]:
                row[1][2][0][1].text = str(dailyPnl)  # raw
        return rd.toXML()
    except Exception:
        LOGGER.exception('Error: Cash Utilization Live View Bombed - Daily PnL not added to Cash Balance.')
        return xml

def CashUtilization(reportObj, param, xml):
    ''' Pre-Process the xml for the Cash Utilization Live view
            Adds the daily pnl for the CR portfolio to the emtpy field in Client Daily TPL
            Must be in 3rd column
    '''
    xml = _AddPnLToColumn(xml, param)
    return xml


