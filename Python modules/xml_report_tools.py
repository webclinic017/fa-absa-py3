'''----------------------------------------------------------------------
Project: Prime Brokerage Project
Department: Prime Services
Requester: Francois Henrion
Developer: Paul Jacot-Guillarmod
CR Number: 666125 (Initial Deployment)
----------------------------------------------------------------------'''

from xml.etree import ElementTree
import acm

def _getDate(dateStr, customDate):
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
        calendar = acm.FCurrency['ZAR']
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

def AddDates(reportObj, param, xml):
    print('======================================================')
    print('parameter:', param)
    print('======================================================')
    
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
    
    root = ElementTree.XML(xml)
    reports = []
    if root.tag == 'PRIMEReport':
        reports.append(root)
    else:
        reports = root.findall('PRIMEReport')
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
        ElementTree.SubElement(report, 'PortfolioStartDate').text = _getDate(dict[START_DATE], dict[START_DATE_CUSTOM])
        ElementTree.SubElement(report, 'PortfolioEndDate').text = _getDate(dict[END_DATE], dict[END_DATE_CUSTOM])
    return ElementTree.tostring(root)
