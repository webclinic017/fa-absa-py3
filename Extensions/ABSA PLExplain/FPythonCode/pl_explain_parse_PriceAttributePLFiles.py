"""----------------------------------------------------------------------------
MODULE
    pl_explain_parse_PriceAttributePLFiles - 

    Gino Bellato, FIS

DESCRIPTION

    This script takes the Higher Order Close-of-business ("COB") and Start-of-business ("SOB") P&L files
    and filters out COB and SOB P&L for New Trade Ids (trades executed on attribution run date).
    1. It also looks up the SOB P&L for Cancelled/Dropped Deals using the SPOT_SOB workspace for 
    2. MarktoMarket Accounting Treatment portfolios and SPOT_SOB_ACCR_MM workspace for Accrual Accounting Treatment portfolios.
    3. This script produces a Price Attribute SOB & COB P&L csv output file in the required format to be uploaded to Adaptiv.

----------------------------------------------------------------------------"""
import acm
import csv
import time
import datetime
import os, os.path
from os import path
from at_ael_variables import AelVariableHandler


today = acm.Time.DateToday()
format_Today = today.replace('-', '')
yesterday = acm.Time.DateAdjustPeriod(today, '-1d', 'ZAR Johannesburg', 'Preceding')
format_Yesterday = yesterday.replace('-', '')
AggregateTradeTypes = ('Aggregate', 'Cash Posting', 'FX Aggregate')

dateMappings = {"Today": today,
                "Yesterday": yesterday,
                }


default_input_path = "\\" + "\\zadalnmapp1154\Share\PnL_Explain\Extracts\\"
default_output_path = "\\" + "\\zadalnmapp1154\Share\PnL_Explain\Extracts\\"
default_SOB_fileName = 'PLE_System_PL_HigherOrder_SOB_'+ today + '.csv'
default_COB_fileName = 'PLE_System_PL_'+ today + '.csv'
default_CancelNewTradesfileName = 'PLE_CancelsPL_InternalNewTrades_' + today + '.csv'
default_PriceAttr_output_fileName = 'PLE_System_PL_PriceAttributePL_' + today + '.csv'

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


def getTradeIDs(file_inputPath, tradeList):
    with open(file_inputPath) as csvfile:     
        reader = csv.DictReader(csvfile)
        print "***Reading data from input Cancel/New Trades CSV file***"
        for row in reader:
            tradeId = row['Trade No']
            tradeList.append(tradeId)
    return tradeList
    
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
    
def getCancelAndNewTradeIDs(file_inputPath):
    FilterTradeIds = {}
    with open(file_inputPath) as csvfile:     
        reader = csv.DictReader(csvfile)
        print "***Reading data from input Cancel/New Trades CSV file***"
        for row in reader:
            tradeId = row['Trade No']
            portfolio = row['Portfolio']
            newTradePL = row['New Trades PL']
            cancelsPL = row['Cancels PL']
            if cancelsPL:
                FilterTradeIds[tradeId]=[tradeId, portfolio]
    return FilterTradeIds
    
def check_for_aggregateTrades(tradeID):
    trade = acm.FTrade[tradeID]
    if trade and ((trade.Type() in AggregateTradeTypes) or (trade.AdditionalInfo().InsOverride() !='Funding Allocation')):
        if trade.ExecutionDate() <= today and trade.ExecutionDate() > yesterday:
            return None
        else:
            return trade.Oid()
    elif trade:
        return trade.Oid()
    else:
        return tradeID
        
def check_accounting_treatment(tradeID):
    trd_obj = acm.FTrade[tradeID]
    if not trd_obj:
        return None
    elif trd_obj:
        if trd_obj.Portfolio():
            return trd_obj.Portfolio().TypeChlItem().Name()
        else:
            return None

def read_higherOrder_SOB_PL_csv_file(file_inputPath, tradeData):
    output_data = {}
    with open(file_inputPath) as csvfile:  
        reader = csv.DictReader(csvfile)
        print "***Reading data from input SOB PL CSV file***"
        for row in reader:
            insName = row['Trade.Reference']
            tradeID = row['Trade No'] 
            insType =row['Instrument Type']
            portfolio = row['Portfolio']
            bookNode = row['Trade.Book Node']
            sobPL = row['Total PL HO SOB']
            if float(sobPL) != 0:
                #if tradeID in tradeData:
                #    cancelPL_port = tradeData[tradeID][1]
                #    output_data[tradeID]=[insName,tradeID,insType,cancelPL_port,sobPL]                  
                #elif tradeID not in tradeData:
                if check_for_aggregateTrades(tradeID):
                    output_data[tradeID]=[insName, tradeID, insType, portfolio, bookNode, sobPL]
    return output_data
    
def read_higherOrder_COB_PL_csv_file(file_inputPath, sob_data):
    with open(file_inputPath) as csvfile:  
        reader = csv.DictReader(csvfile)
        print "***Reading data from input COB PL CSV file***"
        for row in reader:
            tradeID = row['Trade No']
            cobCash = row['Total Cash']
            cobPV = row['Total PV']
            cobPL = float(cobCash) + float(cobPV)
            if tradeID in sob_data:
                sob_data[tradeID].append(cobPL)
    return sob_data
	

def add_cancelPL(file_inputPath, ho_data):
    with open(file_inputPath) as csvfile:  
        reader = csv.DictReader(csvfile)
        print "***Reading data from input Cancel/New Trades CSV file***"
        for row in reader:
            insName = row['Trade.Reference']
            tradeID = row['Trade No']
            insType = row['Instrument Type']
            portfolio = row['Portfolio']
            bookNode = row['Trade.Book Node']
            cancelPL_COB = row['Cancels PL'] 
            if cancelPL_COB:
                cancelpl_COB_float = ((float(cancelPL_COB))*(-1))
                if (check_accounting_treatment(tradeID) == 'Mark to Market') or (check_accounting_treatment(tradeID) == None):
                    cancelPL_SOB = getPositionTPL(tradeID, "Portfolio Total Profit and Loss")
                if check_accounting_treatment(tradeID) == 'Accrual':
                    cancelPL_SOB = getPositionTPL(tradeID, "Portfolio Total Profit and Loss Accrual")
                ho_data[tradeID] = [insName, tradeID, insType, portfolio, bookNode, cancelPL_SOB, cancelpl_COB_float]
    return ho_data

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
        #col_Names = ['Trade.Instrument Name','Trade.Reference','Trade.Instrument Type','Trade.Portfolio','Total PL HO SOB', 'Total PL HO COB']
        col_Names = ['Trade.Reference', 'Trade No', 'Instrument Type', 'Portfolio', 'Trade.Book Node', 'Total PL HO SOB', 'Total PL HO COB']
        writer.writerow([i for i in col_Names])
        print ("***Writing Data to Output CSV file***")
        print ("Output file writted to: {0}".format(OutputfilePath))
        for line in outputData:
            writer.writerow(outputData[line])

"""---------------------------------------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------------------------------------------------------"""

days = ['Today', 'Yesterday']
ael_gui_parameters = {'hideExtracControls': True,
                      'windowCaption': 'PL Explain Price Attribute PL Calculation'}

ael_variables = [ ['inputDatefolder', 'Input Date Folder', 'string', days, 'Today', 0],
                  ['inputPathSOB', 'Input Path SOB', 'string', None, default_input_path, 0],
                  ['input_SOB_fileName', 'Input File Name SOB', 'string', None, default_SOB_fileName, 0],
                  ['inputPathCOB', 'Input Path COB', 'string', None, default_input_path, 0],
                  ['input_COB_fileName', 'Input File Name COB', 'string', None, default_COB_fileName, 0],
                  ['inputPathCancels', 'Input Path Cancel/NewTrades', 'string', None, default_input_path, 0],
                  ['input_CancelNewTradesfileName', 'Input File Name Cancel/New Trades', 'string', None, default_CancelNewTradesfileName, 0],
                  ['outputPath', 'Output Path', 'string', None, default_output_path, 0],
                  ['outputfileName', 'Output File Name', 'string', None, default_PriceAttr_output_fileName, 0]]

def ael_main(ael_dict):
    date = os.path.join(ael_dict['inputDatefolder'])
    dateFolder = dateMappings[date]
    inputPathCOB = os.path.join(ael_dict['inputPathCOB'], dateFolder, ael_dict['input_COB_fileName'])
    inputPathSOB = os.path.join(ael_dict['inputPathSOB'], dateFolder,  ael_dict['input_SOB_fileName'])
    inputPathCancelNew = os.path.join(ael_dict['inputPathCancels'], dateFolder, ael_dict['input_CancelNewTradesfileName'])
    print("STARTED {0} {1}".format(today, _nowTime()))
    start_time = time.time()
    print ("Checking if Cancel/New Trade CSV file exists: " + str(path.isfile(inputPathCancelNew)))
    if path.isfile(inputPathCancelNew):
        try:
            NewTradeIds = getCancelAndNewTradeIDs(inputPathCancelNew)            
            SOB_data = read_higherOrder_SOB_PL_csv_file(inputPathSOB, NewTradeIds)
            COB_data = read_higherOrder_COB_PL_csv_file(inputPathCOB, SOB_data)
            exportData = add_cancelPL(inputPathCancelNew, COB_data)
            outputPath = os.path.join(ael_dict['outputPath'], dateFolder)
            write_outputPath = os.path.join(ael_dict['outputPath'])
            output_file = ael_dict['outputfileName']
            write_output_path(write_outputPath)
            write_output_csv(outputPath, output_file, exportData)
        except Exception as e:
            print 'Exception Raised: %s'%(e)
    else: 
        NewTradeIds = {}
        try:
            SOB_data = read_higherOrder_SOB_PL_csv_file(inputPathSOB, NewTradeIds)
            COB_data = read_higherOrder_COB_PL_csv_file(inputPathCOB, SOB_data)
            outputPath = os.path.join(ael_dict['outputPath'], dateFolder)
            write_outputPath = os.path.join(ael_dict['outputPath'])
            output_file = ael_dict['outputfileName']
            write_output_path(write_outputPath)
            write_output_csv(outputPath, output_file, COB_data)
        except Exception as e:
            print 'Exception Raised: %s'%(e)
    end_time = time.time()
    duration = end_time - start_time
    print("Execution time (hh:mm:ss): {0}".format(_convertTimeInSecondsToHoursMinutesSeconds(duration)))
    print("FINISHED {0} {1}".format(today, _nowTime()))
    print ('Total Clock-Time: ' + str(datetime.timedelta(seconds=time.clock())))
