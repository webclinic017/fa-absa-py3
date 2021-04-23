"""-----------------------------------------------------------------------
MODULE
    ABSAPSwap_SanlamMTDReport

DESCRIPTION
    Date                : 2010-12-07
    Purpose             : Custom CSV report for Sanlam's Month TO Date CFD positions.
    Department and Desk : Prime Services
    Requester           : Francois Henrion
    Developer           : Herman Hoon
    CR Number           : 517043

ENDDESCRIPTION
-----------------------------------------------------------------------"""


import csv
import ael
import acm
import FRunScriptGUI

HEADINGS = ['CFD Name', 'Start Date', 'End Date', 'Position', 'Total Profit and Loss', 'Mtm TPL', 'Execution Premium TPL', 'Short Premium TPL', 'Overnigth Premiumium TPL', 'Dividends TPL']

calcSpace = acm.Calculations().CreateCalculationSpace( acm.GetDefaultContext(), 'FPortfolioSheet')

def write_file(name, data):
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
    compPort = acm.FCompoundPortfolio[portName]
    if compPort:
        ports = compPort.AllPhysicalPortfolios()

        calcSpace.SimulateGlobalValue('Portfolio Profit Loss Start Date', 'Custom Date')
        calcSpace.SimulateGlobalValue('Portfolio Profit Loss End Date', 'Custom Date')
        calcSpace.SimulateGlobalValue('Portfolio Profit Loss Start Date Custom', startDate)
        calcSpace.SimulateGlobalValue('Portfolio Profit Loss End Date Custom', endDate)

        for port in ports:

            topnode = calcSpace.InsertItem(port)

            portfolioIter = topnode.Iterator()
            
            while portfolioIter:
            
                proxy       = portfolioIter.Tree()
                cfdName     = proxy.Item().Portfolio().Name()
                pos         = calcSpace.CalculateValue(proxy, 'Portfolio Profit Loss Period Position')
                tpl         = calcSpace.CalculateValue(proxy, 'Portfolio Total Profit and Loss')
                mtmTpl      = calcSpace.CalculateValue(proxy, 'Portfolio Swap Mtm TPL')
                epTpl       = calcSpace.CalculateValue(proxy, 'Portfolio Swap Execution Premium TPL')
                spTpl       = calcSpace.CalculateValue(proxy, 'Portfolio Swap Short Premium TPL')
                onTpl       = calcSpace.CalculateValue(proxy, 'Portfolio Swap Overnight Premium TPL')
                divTpl      = calcSpace.CalculateValue(proxy, 'Portfolio Dividends')
                
                try:
                    list.append([cfdName, startDate, endDate, pos, tpl.Number(), mtmTpl.Number(), epTpl.Number(), spTpl.Number(), onTpl.Number(), divTpl.Number()])
                except:
                    return ''
                    
                portfolioIter = portfolioIter.NextSibling()
   
        calcSpace.RemoveGlobalSimulation('Portfolio Profit Loss Start Date')
        calcSpace.RemoveGlobalSimulation('Portfolio Profit Loss End Date')
        calcSpace.RemoveGlobalSimulation('Portfolio Profit Loss Start Date Custom')
        calcSpace.RemoveGlobalSimulation('Portfolio Profit Loss End Date Custom')
   
        return list
    else:
        return ''

        
#================================================================================#
INCEPTION       = ael.date('1970-01-01').to_string(ael.DATE_ISO)
today           = ael.date_today()
TODAY           = today.to_string(ael.DATE_ISO)
FIRSTOFYEAR     = today.first_day_of_year().to_string(ael.DATE_ISO)
FIRSTOFMONTH    = today.first_day_of_month().to_string(ael.DATE_ISO)
YESTERDAY       = today.add_days(-1).to_string(ael.DATE_ISO)
TWODAYSAGO      = today.add_days(-2).to_string(ael.DATE_ISO)
PREVBUSDAY      = today.add_banking_day(ael.Calendar['ZAR Johannesburg'], -1).to_string(ael.DATE_ISO)
TWOBUSDAYSAGO   = today.add_banking_day(ael.Calendar['ZAR Johannesburg'], -2).to_string(ael.DATE_ISO)
 
fromDateList   = {'Inception':INCEPTION,'First Of Year':FIRSTOFYEAR,'First Of Month':FIRSTOFMONTH,'PrevBusDay':PREVBUSDAY,'TwoBusinessDaysAgo':TWOBUSDAYSAGO,'TwoDaysAgo':TWODAYSAGO,'Yesterday':YESTERDAY,'Custom Date':TODAY,'Now':TODAY} 
toDateList     = {'Now':TODAY,'TwoDaysAgo':TWODAYSAGO,'PrevBusDay':PREVBUSDAY,'Yesterday':YESTERDAY,'Custom Date':TODAY}
               
fromDateKeys = fromDateList.keys()
fromDateKeys.sort()

toDateKeys = toDateList.keys()
toDateKeys.sort()

def enableCustomFromDate(index, fieldValues):
    ael_variables[2][9] = (fieldValues[1] == 'Custom Date')
    return fieldValues

def enableCustomToDate(index, fieldValues):
    ael_variables[4][9] = (fieldValues[3] == 'Custom Date')
    return fieldValues

portfolioList = []
for portfolio in acm.FCompoundPortfolio.Select(''):
    portfolioList.append(str(portfolio.Name()))

portfolioList.sort()

directorySelection=FRunScriptGUI.DirectorySelection()

#Variable Name, Display Name, Type, Candidate Values, Default, Mandatory, Multiple, Description, Input Hook, Enabled
ael_variables = [   
                    ['PortName', 'Portfolio Name', 'string', portfolioList, 'Sanlam Gen X PSwap', 1, 0, 'Compound Stock Portfolio for which the report will be generated.'],
                    ['FromDate', 'From Date', 'string', fromDateKeys, 'First Of Month', 1, 0, 'Date from which trades will be selected.', enableCustomFromDate, 1],
                    ['FromDateCustom', 'From Date Custom', 'string', None, TODAY, 0, 0, 'Custom from date', None, 0],
                    ['ToDate', 'End Date', 'string', toDateKeys, 'Now', 1, 0, 'Date to which trades will be selected.', enableCustomToDate, 1],
                    ['ToDateCustom', 'To Date Custom', 'string', None, TODAY, 0, 0, 'Custom to date', None, 0],
                    ['FileDir', 'File Directory', directorySelection, None, directorySelection, 1, 1, 'File directory.'],
                    ['FileName', 'File Name', 'string', None, 'Sanlam_CFD_MTD_Report_', 1, 0, 'File Name']
                ]

def ael_main(ael_dict):

    portName = ael_dict['PortName']
    
    if ael_dict['FromDate'] == 'Custom Date':
        fromDate = ael_dict['FromDateCustom']
    else:
        fromDate = str(fromDateList[ael_dict['FromDate']])
        
    if ael_dict['ToDate'] == 'Custom Date':
        toDate = ael_dict['ToDateCustom']
    else:
        toDate = str(toDateList[ael_dict['ToDate']])
        
    fromDate = ael.date_from_string(fromDate)
    toDate   = ael.date_from_string(toDate)
    
    list = []
    list.append(HEADINGS)
    list = getPortfolioData(list, portName, fromDate, toDate)
    
    fileName = str(ael_dict['FileDir']) + '//' + ael_dict['FileName'] + TODAY + '.csv'
    
    if list != '':
        write_file(fileName, list)
    else:
        print 'INFO: %s has not been created' %(fileName)
