'''----------------------------------------------------------------------
Project: Prime Brokerage Project
Department: Prime Services
Requester: Francois Henrion
Developer: Paul Jacot-Guillarmod
CR Number: 666125 (Initial Deployment)

----------------------------------------------------------------------
HISTORY
================================================================================
Date        Change no   Developer               Description
--------------------------------------------------------------------------------
            666125      Paul Jacot-Guillarmod   Initial Implementation
2011-06-29  699989      Rohan van der Walt      Add account name for cash transaction report
                                                Add report name
                                                Add row level colours
                                                Add column widths
2011-07-06  707904      Rohan van der Walt      Add Invoice Nr
                                                Add RunLocation
2011-07-15  713436      Rohan van der Walt      Filter out [] and NaN values in Cells
2011-08-03  XXXXXX      Rohan van der Walt      Replace any -0 or -0.00 values with 0 or 0.00
2011-09-13  768482      Rohan van der Walt      Remove Settled section instrument detail and remove LIVE grouping
2011-11-08  823082      Rohan van der Walt      Settled Grouping Rename
2013-03-19  883716      Phumzile Mgcima         Added Preprocessor to cater for Multiple dividends on PreProcessXML()
2013-03-19  2014795     Hynek Urban             Introduce PreprocessXMLSortBySettled.
2015-05-13  2833272     Peter Basista           Change the way how account name is obtained.
'''
import acm, re
from itertools import chain
from xml.etree import ElementTree

import at_logging


LOGGER = at_logging.getLogger()


def _addAccountName(xml, accName):
    ignored_statuses = ["Simulated", "Void"]
    try:
        rd = ReportData(xml)
        reports = rd.getDataAsArray()
        for report in reports:
            instrument_name = reports[report][len(reports[report]) - 1][0].text
            acm_instrument = acm.FInstrument[instrument_name]
            acm_trades = acm_instrument.Trades()
            relevant_trades = [trade for trade in acm_trades
                               if trade.Status() not in ignored_statuses]
            if len(relevant_trades) == 1:
                accName = relevant_trades[0].Name()
                break
            else:
                LOGGER.warning(("Could not find exactly one relevant trade on instrument '%s'."
                "Found %s relevant trades instead."), acm_instrument.Name(), len(relevant_trades))

        root = ElementTree.XML(xml)
        reports = []
        if root.tag == 'PRIMEReport':
            reports.append(root)
        else:
            reports = root.findall('PRIMEReport')

        for report in reports:
            reportParameters = report.find("ReportParameters")
            if not reportParameters:
                reportParameters = ElementTree.SubElement(report, "ReportParameters")
            ElementTree.SubElement(reportParameters, 'AccountName').text = accName

        return ElementTree.tostring(root)
    except:
        return xml

def _filterOutErrors(xml):
    try:
        rd = ReportData(xml)

        reports = rd.getDataAsArray()
        for report in reports:
            for row in reports[report]:
                for cell in row:
                    try:
                        if cell.text in ['[]', 'NaN', '#']:
                            LOGGER.info('OLD: %s\tNEW: ' , cell.text)
                            cell.text = ''
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
                for cell in row:
                    try:
                        myMatch = re.match(pattern, cell.text)
                        if myMatch:
                            new_text_val = cell.text.replace('-', '')
                            LOGGER.info('OLD: %s\tNEW: %s', cell.text, new_text_val)
                            cell.text = new_text_val
                    except:
                        continue
        return rd.toXML()
    except:
        return xml

def _getDate(dateStr, customDate):
    ''' Convert trading manager date strings to actual dates
    '''
    if dateStr == 'Custom Date':
        try:
            return acm.Time().AsDate(customDate)
        except:
            return None
    elif dateStr == 'Now':
        return acm.Time().DateNow()
    elif dateStr == 'TwoDaysAgo':
        return acm.Time().DateAddDelta(acm.Time().DateNow(), 0, 0, -2)
    elif dateStr == 'PrevBusDay':
        calendar = acm.FCurrency['ZAR'].Calendar()
        if calendar:
            return calendar.AdjustBankingDays(acm.Time().DateNow(), -1)
        else:
            return acm.Time().DateAddDelta(acm.Time().DateNow(), 0, 0, -1)
    elif dateStr == 'Yesterday':
        return acm.Time().DateAddDelta(acm.Time().DateNow(), 0, 0, -1)
    elif dateStr == 'First Of Month':
        return acm.Time().FirstDayOfMonth(acm.Time().DateNow())
    elif dateStr == 'First Of Year':
        return acm.Time().FirstDayOfYear(acm.Time().DateNow())
    else:
        return None


def _addDates(xml):
    try:
        root = ElementTree.XML(xml)
        reports = []
        if root.tag == 'PRIMEReport':
            reports.append(root)
        else:
            reports = root.findall('PRIMEReport')

        START_DATE = 'Portfolio Profit Loss Start Date'
        START_DATE_CUSTOM = 'Portfolio Profit Loss Start Date Custom'
        END_DATE = 'Portfolio Profit Loss End Date'
        END_DATE_CUSTOM = 'Portfolio Profit Loss End Date Custom'
        dict = {
            START_DATE: None,
            START_DATE_CUSTOM: None,
            END_DATE: None,
            END_DATE_CUSTOM: None
        }

        for report in reports:
            for group in report.findall('ReportContents/Table/Settings/Groups/Group'):
                label = group.find('Label')
                if not label is None and label.text == 'Profit/Loss':
                    columnId = None
                    for element in group:
                        if element.tag == 'Column':
                            columnIdElement = element.find('ColumnId')
                            if not columnIdElement is None:
                                columnId = columnIdElement.text
                            else:
                                columnId = None
                        elif element.tag == 'Cell':
                            data = element.find('RawData')
                            if not data is None:
                                data = data.text
                                if columnId == START_DATE:
                                    dict[START_DATE] = acm.FEnumeration['EnumPLStartDate'].Enumerator(data)
                                elif columnId == START_DATE_CUSTOM:
                                    dict[START_DATE_CUSTOM] = data
                                elif columnId == END_DATE:
                                    dict[END_DATE] = acm.FEnumeration['EnumPLEndDate'].Enumerator(data)
                                elif columnId == END_DATE_CUSTOM:
                                    dict[END_DATE_CUSTOM] = data
                            columnId = None
                        else:
                            columnId = None
                    break

            reportParameters = report.find("ReportParameters")
            if not reportParameters:
                reportParameters = ElementTree.SubElement(report, "ReportParameters")
            ElementTree.SubElement(reportParameters, 'PortfolioStartDate').text = _getDate(dict[START_DATE], dict[START_DATE_CUSTOM])
            ElementTree.SubElement(reportParameters, 'PortfolioEndDate').text = _getDate(dict[END_DATE], dict[END_DATE_CUSTOM])
            ElementTree.SubElement(reportParameters, 'DateToday').text = _getDate('Now', None)
        return ElementTree.tostring(root)
    except:
        return xml

def _addAddress(xml, partyName):
    ''' Add address elements to the report node
    '''
    try:
        root = ElementTree.XML(xml)
        reports = []
        if root.tag == 'PRIMEReport':
            reports.append(root)
        else:
            reports = root.findall('PRIMEReport')
        party = acm.FParty[partyName.upper()]
        for report in reports:
            reportParameters = report.find("ReportParameters")
            if not reportParameters:
                reportParameters = ElementTree.SubElement(report, "ReportParameters")
            clientDetails = reportParameters.find("ClientDetails")
            if not clientDetails:
                clientDetails = ElementTree.SubElement(reportParameters, "ClientDetails")
            ElementTree.SubElement(clientDetails, 'FullName').text = str(party.Fullname())
            ElementTree.SubElement(clientDetails, 'Address').text = str(party.Address())
            ElementTree.SubElement(clientDetails, 'City').text = str(party.City())
            ElementTree.SubElement(clientDetails, 'ZipCode').text = str(party.ZipCode())
            ElementTree.SubElement(clientDetails, 'Country').text = str(party.Country())

        return ElementTree.tostring(root)
    except:
        return xml

def _addColumnWidths(xml):
    '''
    Scans through the column data and automatically sets the column width wide enough
    OR reads from extension value?
    This will only work on single report xml files, NOT multireports
    '''
    try:
        SPACE_PER_CHAR = 2.8
        PAGE_WIDTH = 278
        rd = ReportData(xml)
        reports = rd.getDataAsArray()
        for report in reports:
            colWidths = {}
            colSpaces = {}
            for i in range(len(reports[report][0])):
                colWidths.setdefault(i, 5)
                colSpaces.setdefault(i, 0)
            for column in range(len(reports[report][0])):
                try:
                    spaceCount = reports[report][0][column].text.count(' ')
                except:
                    spaceCount = 0;
                colSpaces[column] = max([colSpaces[column], spaceCount])
                for row in range(len(reports[report])):
                    try:
                        cellText = reports[report][row][column].text if reports[report][row][column].text else ''
                    except:
                        cellText = ''
                    colWidths[column] = max([colWidths[column], len(cellText)])
                try:
                    colName = reports[report][0][column].text if reports[report][0][column].text else ''
                except:
                    colName = ''
                if colName == 'Issuer':
                    colWidths[column] = float(colWidths[column]) / 1.5
                elif colName == 'Date and Time':
                    colWidths[column] = float(colWidths[column]) / 1.5

            # Write Results
            report = rd.getReportNode(report)
            reportParameters = report.find("ReportParameters")
            if not reportParameters:
                reportParameters = ElementTree.SubElement(report, "ReportParameters")
            columnWidths = reportParameters.find("ColumnWidths")
            if not columnWidths:
                columnWidths = ElementTree.SubElement(reportParameters, "ColumnWidths")
            scaled = {}
            for key, val in colWidths.items():
                scaled[key] = float(val * SPACE_PER_CHAR) / 1.4 if colSpaces[key] >= 1 else val * SPACE_PER_CHAR
            total = sum(scaled[i] for i in scaled.keys())
            factor = PAGE_WIDTH / total
            for key, val in scaled.items():
                ElementTree.SubElement(columnWidths, 'c', attrib={'id':str(key)}).text = str(val * factor) + 'mm'

        return rd.toXML()
    except:
        return xml

def _addGroupLevelColours(xml):
    '''
    read extensionValue to set group level background colours
    '''
    try:
        rd = ReportData(xml)
        reports = rd.getDataAsArray()
        for report in reports:
            treeDepth = rd.getTreeDepth(report)
            report = rd.getReportNode(report)
            reportParameters = report.find("ReportParameters")
            if not reportParameters:
                reportParameters = ElementTree.SubElement(report, "ReportParameters")
            groupingLevelBackgroundColour = reportParameters.find("GroupingLevelBackgroundColour")
            if not groupingLevelBackgroundColour:
                groupingLevelBackgroundColour = ElementTree.SubElement(reportParameters, "GroupingLevelBackgroundColour")
            # print 'Found tree depth of', treeDepth
            if treeDepth == 1:
                ElementTree.SubElement(groupingLevelBackgroundColour, 'colour1').text = '#ffffff'
                ElementTree.SubElement(groupingLevelBackgroundColour, 'colour2').text = '#ffffff'
                ElementTree.SubElement(groupingLevelBackgroundColour, 'colour3').text = '#ffffff'
                ElementTree.SubElement(groupingLevelBackgroundColour, 'colour4').text = '#ffffff'
            elif treeDepth == 2:
                ElementTree.SubElement(groupingLevelBackgroundColour, 'colour1').text = '#d1d1d1'
                ElementTree.SubElement(groupingLevelBackgroundColour, 'colour2').text = '#ffffff'
                ElementTree.SubElement(groupingLevelBackgroundColour, 'colour3').text = '#ffffff'
                ElementTree.SubElement(groupingLevelBackgroundColour, 'colour4').text = '#ffffff'
            elif treeDepth == 3:
                ElementTree.SubElement(groupingLevelBackgroundColour, 'colour1').text = '#d1d1d1'
                ElementTree.SubElement(groupingLevelBackgroundColour, 'colour2').text = '#e1e1e1'
                ElementTree.SubElement(groupingLevelBackgroundColour, 'colour3').text = '#ffffff'
                ElementTree.SubElement(groupingLevelBackgroundColour, 'colour4').text = '#ffffff'
            elif treeDepth == 4:
                ElementTree.SubElement(groupingLevelBackgroundColour, 'colour1').text = '#d1d1d1'
                ElementTree.SubElement(groupingLevelBackgroundColour, 'colour2').text = '#e1e1e1'
                ElementTree.SubElement(groupingLevelBackgroundColour, 'colour3').text = '#e8e8e8'
                ElementTree.SubElement(groupingLevelBackgroundColour, 'colour4').text = '#ffffff'
            elif treeDepth == 5:
                ElementTree.SubElement(groupingLevelBackgroundColour, 'colour1').text = '#d1d1d1'
                ElementTree.SubElement(groupingLevelBackgroundColour, 'colour2').text = '#d9d9d9'
                ElementTree.SubElement(groupingLevelBackgroundColour, 'colour3').text = '#e1e1e1'
                ElementTree.SubElement(groupingLevelBackgroundColour, 'colour4').text = '#e8e8e8'
                ElementTree.SubElement(groupingLevelBackgroundColour, 'colour5').text = '#ffffff'
        return rd.toXML()
    except:
        return xml


def _addReportParameter(xml, name, value):
    '''
    add a node to reportParameters
    '''
    try:
        root = ElementTree.XML(xml)
        reports = []
        if root.tag == 'PRIMEReport':
            reports.append(root)
        else:
            reports = root.findall('PRIMEReport')

        for report in reports:
            reportParameters = report.find("ReportParameters")
            if not reportParameters:
                reportParameters = ElementTree.SubElement(report, "ReportParameters")
            ElementTree.SubElement(reportParameters, name).text = value
        return ElementTree.tostring(root)
    except:
        return xml


class ReportData():
    root = None

    def __init__(self, xml):
        self.root = ElementTree.XML(xml)

    def _addRows(self, row, results, reportName):
        results[reportName].append(ReportData._flatten([ row.find('Label') , [ cell.find('FormattedData') for cell in row.findall('Cells/Cell')] ]))
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

def _addInvoiceNr(xml):
    '''
    adds invoice nr - The first trade number that appears in report, if empty, dont show invoice nr label.
    '''
    try:
        rd = ReportData(xml)
        reports = rd.getDataAsArray()
        for report in reports:
            if len(reports[report]) > 2:
                invoiceTag = 'Tax Invoice Nr: ' + reports[report][2][0].text
            else:
                invoiceTag = ''

        root = ElementTree.XML(xml)
        reports = []
        if root.tag == 'PRIMEReport':
            reports.append(root)
        else:
            reports = root.findall('PRIMEReport')
        for report in reports:
            reportParameters = report.find("ReportParameters")
            if not reportParameters:
                reportParameters = ElementTree.SubElement(report, "ReportParameters")

            ElementTree.SubElement(reportParameters, 'InvoiceNr').text = invoiceTag
        return ElementTree.tostring(root)
    except:
        return xml

def _addRunLocation(xml):
    '''
    adds invoice nr - The first trade number that appears in report, if empty, dont show invoice nr label.
    '''
    try:
        root = ElementTree.XML(xml)
        reports = []
        if root.tag == 'PRIMEReport':
            reports.append(root)
        else:
            reports = root.findall('PRIMEReport')
        for report in reports:
            reportParameters = report.find("ReportParameters")
            if not reportParameters:
                reportParameters = ElementTree.SubElement(report, "ReportParameters")

            ElementTree.SubElement(reportParameters, 'RunLocation').text = "FrontEnd" if str(acm.Class()) == "FTmServer" else "BackEnd"

        return ElementTree.tostring(root)
    except:
        return xml

def _removeSettledInstrumentRows(xml):
    try:
        root = ElementTree.XML(xml)
        parent_map = dict((c, p) for p in root.getiterator() for c in p)
        for node in root.findall('.//Label'):
            if node.text == 'Expired or Closed Out':
                parent = parent_map[node]
                rows = parent_map[parent]
                parent.remove(parent.find('Rows'))
                rows.remove(parent)
                rows.append(parent)
        return ElementTree.tostring(root)
    except:
        return xml

def _moveLiveInstrumentRows(xml):
    try:
        root = ElementTree.XML(xml)
        parent_map = dict((c, p) for p in root.getiterator() for c in p)
        for node in root.findall('.//Label'):
            if node.text == 'Live':
                parent = parent_map[node]
                rows = parent_map[parent]
                for liveInstrumentRow in parent.findall('./Rows/Row'):
                    rows.append(liveInstrumentRow)
                rows.remove(parent)
        return ElementTree.tostring(root)
    except:
        return xml

def PreProcessXML(reportObj, param, xml, keep_settled=False):
    ''' Pre-Process the xml for the Prime Brokergae reports by adding elements for the  portfolio start and end date and the party address.
        The party name is entered in the parameter field of the Processing tab.
        param = comma seperated values
        param[0] - Party name to extract address details...
        param[1] - Report name
        param[2] - (optional) Account name
        param[3] - (optional) Version of the reporting framework that generated the report
    '''

    param = param.split(',')
    xml = _addDates(xml)
    xml = _addAddress(xml, param[0])
    xml = _addReportParameter(xml, 'ReportName', param[1])
    xml = _addRunLocation(xml)
    if len(param) > 2 and param[2]:
        xml = _addAccountName(xml, param[2])
    if len(param) > 3 and param[3]:
        xml = _addReportParameter(xml, 'FrameworkVersion', param[3])
    xml = _addInvoiceNr(xml)
    xml = _filterOutErrors(xml)
    xml = _fixFormattingErrors(xml)
    if not keep_settled:
        xml = _moveLiveInstrumentRows(xml)
        xml = _removeSettledInstrumentRows(xml)
    xml = _addGroupLevelColours(xml)

    return xml


def PreProcessXMLSortBySettled(reportObj, param, xml):
    """Show the "Live" records before the "Expired" ones."""
    xml = PreProcessXML(reportObj, param, xml, keep_settled=True)
    root = ElementTree.XML(xml)
    rows_elements = root.findall('.//Rows')
    for rows_element in rows_elements:
        live_rows = []
        expired_rows = []
        rest = []
        for row in rows_element:
            if row.find('Label').text == 'Live':
                live_rows.append(row)
            elif row.find('Label').text == 'Expired or Closed Out':
                expired_rows.append(row)
            else:
                rest.append(row)
        if not live_rows and not expired_rows:
            continue  # Nothing to reorder here.
        for row in chain(live_rows, expired_rows, rest):
            # In this way, all rows are gradually moved to the end in the sorted
            # order.
            rows_element.remove(row)
            rows_element.append(row)
    return ElementTree.tostring(root)
