"""----------------------------------------------------------------------------
MODULE
    pl_explain_dropped_deals - 

    Gino Bellato, FIS

DESCRIPTION

    This script takes the last 2 days of System PL files and 
    looks up the trade Ids that dropped off from previous business day to today.
    This script produces a Cancels PL output csv file in the required format to be uploaded to Adaptiv.
    Notes
    1. For Mark-To-Market Accounting portfolios, run this script with no standard user settings
    2. For Accrual Accounting portfolios, run this script with the ACCR_MM Workspace overrides.

----------------------------------------------------------------------------"""

import acm, ael
import csv
import os, os.path
import time
import datetime
from at_ael_variables import AelVariableHandler


today = acm.Time.DateToday()
format_Today = today.replace('-', '')
yesterday = acm.Time.DateAdjustPeriod(today, '-1d', 'ZAR Johannesburg', 'Preceding')
firstOfMonth = acm.Time.FirstDayOfMonth(today)
format_Yesterday = yesterday.replace('-', '')
AggregateTradeTypes = ('Aggregate', 'Cash Posting', 'FX Aggregate')

dateMappings = {"Today": today,
                "Yesterday": yesterday,
                }

default_input_path = "\\" + "\\zadalnmapp1154\Share\PnL_Explain\Extracts\\"
default_output_path = "\\" + "\\zadalnmapp1154\Share\PnL_Explain\Extracts\\"
default_fileName = 'PLE_System_PL_' + today +'.csv'
default_yesterdayFileName = 'PLE_System_PL_' + yesterday + '.csv'
default_output_fileName = 'PLE_CancelsPL_InternalNewTrades_' + today + '.csv'


'''................................................................................................................................
.................................................................................................................................'''

def _nowTime():
    """
    Returns a sting with current time in the format HH:MM:SS, for example:
    10:12:43
    """
    return time.strftime('%H:%M:%S', time.localtime(time.time()))
    

def _convertTimeInSecondsToHoursMinutesSeconds(timeInSeconds):
    timeInSeconds = int(timeInSeconds)
    mins = timeInSeconds // 60
    hrs = mins // 60
    return '{0:02d}:{1:02d}:{2:02d}'.format(hrs, mins % 60, timeInSeconds % 60)


'''................................................................................................................................
.................................................................................................................................'''


def parse_pnl_csv_file(input_path):
    new_data = {}
    with open(input_path) as csvfile:     
        reader = csv.DictReader(csvfile)
        print "***Reading data from input CSV file***"
        for row in reader:
            tradeID = str(row['Trade No'])
            portfolio = row['Portfolio']
            bookNode = row['Trade.Book Node']
            new_data[tradeID]=[tradeID, portfolio, bookNode] 
    return new_data
    
def getPositionTPL(tradeID, columnName):
    posObj = acm.FTrade[tradeID]
    if not posObj:
        return None
    if posObj.Status() == 'Void':
        clone = posObj.Clone()
        clone.Status("BO Confirmed")
        calcSpace = acm.FCalculationSpace('FPortfolioSheet')
        selectedNode = calcSpace.InsertItem(clone)
        calcSpace.Refresh()
        vals = calcSpace.CreateCalculation(selectedNode, columnName).Value().Number()
    else:
        calcSpace = acm.FCalculationSpace('FPortfolioSheet')
        selectedNode = calcSpace.InsertItem(posObj)
        calcSpace.Refresh()
        vals = calcSpace.CreateCalculation(selectedNode, columnName).Value().Number()
    return round(vals, 2)    


def filter_funding_trades(tradeID):
    trd_obj = acm.FTrade[tradeID]
    if not trd_obj:
        return True
    elif trd_obj:
        if trd_obj.AdditionalInfo().InsOverride() != 'Funding Allocation':
            return True
        elif trd_obj.AdditionalInfo().InsOverride() == 'Funding Allocation' and trd_obj.ExecutionDate() < firstOfMonth:
            return True
        else:
            return False
            
def check_accounting_treatment(tradeID):
    trd_obj = acm.FTrade[tradeID]
    if not trd_obj:
        return None
    elif trd_obj:
        if trd_obj.Portfolio():
            return trd_obj.Portfolio().TypeChlItem().Name()
        else:
            return None


def filter_dropped_deals_csv_file(input_path, tradeData):
    droppedDeals = []
    with open(input_path) as csvfile:     
        reader = csv.DictReader(csvfile)
        print "***Reading data from input CSV file***"
        for row in reader:
            tradeID = row['Trade No']
            instrument = row['Trade.Reference']
            insType = row['Instrument Type']
            portfolio = row['Portfolio']
            bookNode = row['Trade.Book Node']
            if str(tradeID) not in tradeData: # Archived Deals/Trades
                if filter_funding_trades(tradeID):
                    if (check_accounting_treatment(tradeID) == 'Mark to Market') or (check_accounting_treatment(tradeID) == None):
                        cancelsPL = float(getPositionTPL(tradeID, "Portfolio Total Profit and Loss")) * (-1)
                    if check_accounting_treatment(tradeID) == 'Accrual':
                        cancelsPL = float(getPositionTPL(tradeID, "Portfolio Total Profit and Loss Accrual")) * (-1)
                    droppedDeals.append((instrument, tradeID, insType, portfolio, bookNode, cancelsPL, None))
            elif str(tradeID) in tradeData:
                currentPortfolio = tradeData[tradeID][1]
                currentBookNode = tradeData[tradeID][2]
                if currentPortfolio!=portfolio: #inter portfolio trade amendments
                    if filter_funding_trades(tradeID):
                        if (check_accounting_treatment(tradeID) == 'Mark to Market') or (check_accounting_treatment(tradeID) == None):
                            cancelsPL = float(getPositionTPL(tradeID, "Portfolio Total Profit and Loss")) * (-1)
                            newDealsPL = float(cancelsPL) * (-1)
                        if check_accounting_treatment(tradeID) == 'Accrual':
                            cancelsPL = float(getPositionTPL(tradeID, "Portfolio Total Profit and Loss Accrual")) * (-1)
                            newDealsPL = float(cancelsPL) * (-1)
                        droppedDeals.append((instrument, tradeID, insType, portfolio, bookNode, cancelsPL, None))
                        droppedDeals.append((instrument, tradeID, insType, currentPortfolio, currentBookNode, None, newDealsPL))
    return droppedDeals


def write_output_path(path):
    outputPath_final = path + '/' + str(today) + '/'
    print "**** Check if output folder exists ****"
    if not os.path.exists(path):
        print ("**** Output folder does not exist, writing new folder {0} ****".format(path))
        try:
            os.mkdir(path)
        except Exception as e:
            if not os.path.exists(path):
                print ("Problem creating output directory: {0}".format(str(e)))
            else:
                print ("Directory already exists: {0}".format(path))
    if not os.path.exists(outputPath_final):
        print ("**** Output folder does not exist, writing new folder {0} ****".format(outputPath_final))
        try:
            os.mkdir(outputPath_final)
        except Exception as e:
            if not os.path.exists(outputPath_final):
                print ("Problem creating output directory: {0}".format(str(e)))
            else:
                print ("Directory already exists: {0}".format(outputPath_final))
                        
    

def write_output_csv(path, outputFileName, outputData):
    OutputfilePath = os.path.join(path, outputFileName)
    with open(OutputfilePath, 'wb') as csvOutput:
        writer = csv.writer(csvOutput)
        #col_Names = ['Trade.Instrument Name','Trade.Reference','Trade.Instrument Type','Trade.Portfolio','Cancels PL', 'New Trades PL']
        col_Names = ['Trade.Reference', 'Trade No', 'Instrument Type', 'Portfolio', 'Trade.Book Node', 'Cancels PL', 'New Trades PL']
        writer.writerow([i for i in col_Names])
        print ("***Writing Data to Output CSV file***")
        print ("Output file writted to: {0}".format(OutputfilePath))
        for line in outputData:
            writer.writerow(line)


"""---------------------------------------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------------------------------------------------------"""


days = ['Today', 'Yesterday']
ael_gui_parameters = {'hideExtracControls': True,
                      'windowCaption': 'PL Explain Cancelled/Dropped Deals'}

ael_variables = [ ['inputDatefolder', 'Input Run Date Folder', 'string', days, 'Today', 0],
                  ['inputPath', 'Input Path', 'string', None, default_input_path, 0],
                  ['input_fileName', 'Input File Name', 'string', None, default_fileName, 0],
                  ['inputPrevDatefolder', 'Input Previous Date Folder', 'string', days, 'Yesterday', 0],
                  ['yesterday_input_fileName', 'Yesterday Input File Name', 'string', None, default_yesterdayFileName, 0],
                  ['outputPath', 'Output Path', 'string', None, default_output_path, 0],
                  ['output_fileName', 'Output File Name', 'string', None, default_output_fileName, 0]]
       

def ael_main(ael_dict):
    runDate = os.path.join(ael_dict['inputDatefolder'])
    previousDate = os.path.join(ael_dict['inputPrevDatefolder'])
    runDateFolder = dateMappings[runDate]
    prevDateFolder = dateMappings[previousDate]
    inputPath = os.path.join(ael_dict['inputPath'], runDateFolder, ael_dict['input_fileName'])
    yesterday_inputPath = os.path.join(ael_dict['inputPath'], prevDateFolder, ael_dict['yesterday_input_fileName'])
    outputPath = os.path.join(ael_dict['outputPath'], runDateFolder)
    write_outputPath = os.path.join(ael_dict['outputPath'])
    file = ael_dict['output_fileName']
    print("STARTED {0} {1}".format(today, _nowTime()))
    start_time = time.time()
    try:
        todaysTradeIDs = parse_pnl_csv_file(inputPath)
        CSV_data = filter_dropped_deals_csv_file(yesterday_inputPath, todaysTradeIDs)
        if len(CSV_data) > 0:
            write_output_path(write_outputPath)
            write_output_csv(outputPath, file, CSV_data)
        else: 
            print "No data to write to CSV file"
    except Exception as e:
        print 'Exception Raised: %s'%(e)
    end_time = time.time()
    duration = end_time - start_time
    print("Execution time (hh:mm:ss): {0}".format(_convertTimeInSecondsToHoursMinutesSeconds(duration)))
    print("FINISHED {0} {1}".format(today, _nowTime()))
    print ('Total Clock-Time: ' + str(datetime.timedelta(seconds=time.clock())))



