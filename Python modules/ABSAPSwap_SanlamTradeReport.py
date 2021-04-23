"""-----------------------------------------------------------------------
MODULE
    ABSAPSwap_SanlamTradeReport

DESCRIPTION
    Date                : 2010-12-07
    Purpose             : Custom CSV report for Sanlam's CFD underlying equity trades.
    Department and Desk : Prime Services
    Requester           : Francois Henrion
    Developer           : Herman Hoon
    CR Number           : 517043

ENDDESCRIPTION
-----------------------------------------------------------------------"""

import csv
import ael
import FRunScriptGUI

HEADINGS = ['ENTITE', 'PF_COD', 'INST_COD', 'INST_QTY', 'INST_PRICE', 'XACT_TYP', 'CUR_COD', 'XACT_DAT', 'SETTLE_DAT', 'BROKER_COD']


def write_file(name, data):
    print name
    try:
        f = file(name, 'wb')
        c = csv.writer(f, dialect = 'excel')
        c.writerows(data)
        print 'INFO: %s has been created' %(name)
    except Exception, err:
        print 'ERROR: %s has been not been created: %s' %(name, err)
    finally:
        f.close()
    

def getPortfolioData(list, portName, startDate, endDate):
    port = ael.Portfolio[portName]
    
    for trade in port.trades():
        tradeDate = ael.date_from_time(trade.creat_time)
        if tradeDate >= startDate and tradeDate <= endDate:
            ins = trade.insaddr
            insName = ins.insid[4:7] + 'CFD'

            tradeQuant = int(trade.quantity)
            tradePrice = trade.price
            
            buySell = ''
            if tradeQuant >= 0:    
                buySell = 'BOC'
            else:
                buySell = 'SOC'
                
            tradeValueDate = trade.value_day
            
            list.append(['ID_XACT', 'ASACFD', insName, abs(tradeQuant), tradePrice, buySell, 'CEN', tradeDate, tradeValueDate, 'JFC'])
    
    return list


today           = ael.date_today()
TODAY           = today.to_string(ael.DATE_ISO)
YESTERDAY       = today.add_days(-1)
TWODAYSAGO      = today.add_days(-2)
PREVBUSDAY      = today.add_banking_day(ael.Calendar['ZAR Johannesburg'], -1)
TWOBUSDAYSAGO   = today.add_banking_day(ael.Calendar['ZAR Johannesburg'], -2)

dateList     = {'Today':TODAY,
                'TwoDaysAgo':TWODAYSAGO,
                'PrevBusDay':PREVBUSDAY,
                'Yesterday':YESTERDAY,
                'Custom Date':TODAY}
                
dateKeys = dateList.keys()
dateKeys.sort()


def enableCustomFromDate(index, fieldValues):
    ael_variables[2][9] = (fieldValues[1] == 'Custom Date')
    return fieldValues

def enableCustomToDate(index, fieldValues):
    ael_variables[4][9] = (fieldValues[3] == 'Custom Date')
    return fieldValues

portfolioList = []
for portfolio in ael.Portfolio.select():
    portfolioList.append(str(portfolio.prfid))

directorySelection=FRunScriptGUI.DirectorySelection()

#Variable Name, Display Name, Type, Candidate Values, Default, Mandatory, Multiple, Description, Input Hook, Enabled
ael_variables = [   
                    ['PortName', 'Portfolio Name', 'string', portfolioList, 'Sanlam Gen X EqHedge', 1, 0, 'Stock Portfolio for which the report will be generated.'],
                    ['FromDate', 'From Date', 'string', dateKeys, 'Today', 1, 0, 'Date from which trades will be selected.', enableCustomFromDate, 1],
                    ['FromDateCustom', 'From Date Custom', 'string', None, TODAY, 0, 0, 'Custom from date', None, 0],
                    ['ToDate', 'To Date', 'string', dateKeys, 'Today', 1, 0, 'Date to which trades will be selected.', enableCustomToDate, 1],
                    ['ToDateCustom', 'To Date Custom', 'string', None, TODAY, 0, 0, 'Custom to date', None, 0],
                    ['FileDir', 'File Directory', directorySelection, None, directorySelection, 1, 1, 'File directory.'],
                    ['FileName', 'File Name', 'string', None, 'Sanlam_CFD_Trade_Report_', 1, 0, 'File Name']
                ]

def ael_main(ael_dict):

    portName = ael_dict['PortName']
    
    if ael_dict['FromDate'] == 'Custom Date':
        fromDate = ael_dict['FromDateCustom']
    else:
        fromDate = str(dateList[ael_dict['FromDate']])
        
    if ael_dict['ToDate'] == 'Custom Date':
        toDate = ael_dict['ToDateCustom']
    else:
        toDate = str(dateList[ael_dict['ToDate']])
        
    fromDate = ael.date_from_string(fromDate)
    toDate   = ael.date_from_string(toDate)
    
    list = []
    list.append(HEADINGS)
    list = getPortfolioData(list, portName, fromDate, toDate)
    
    fileName = str(ael_dict['FileDir']) + '//' + ael_dict['FileName'] + TODAY + '.csv'
    
    write_file(fileName, list)
