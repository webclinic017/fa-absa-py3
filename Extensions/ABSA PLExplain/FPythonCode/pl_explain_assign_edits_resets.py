"""-------------------------------------------------------------------------------------------------------
MODULE
    pl_explain_assign_edits_resets - 

    Gino Bellato, FIS

DESCRIPTION

    This script takes the Total SOB & COB PL files and calculates and assigns the Amendment P&L.
    This script produces a Amendment P&L output csv file in the required format to be uploaded to Adaptiv.
    

---------------------------------------------------------------------------------------------------------"""
import acm
import csv
import os, os.path
from at_ael_variables import AelVariableHandler
import time
import datetime


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
default_SOB_fileName = 'PLE_TotalPL_SOB_' + today + '.csv'
default_COB_fileName = 'PLE_TotalPL_COB_' + today + '.csv'
default_fileName = 'PLE_AmendmentPL_' + today + '.csv'
default_output_fileName = 'PLE_AmendmentPL_Updates_' + today + '.csv'


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

output_data = []

def checkAggregateTrade(trade):
    if not trade.Type() in AggregateTradeTypes:
        return True
    elif trade.Type() in AggregateTradeTypes and trade.ExecutionDate() < yesterday:
        return True
    else:
        return False

def COB_read_Amend_PL_csv_file(file_inputPath):
    testData = {}
    with open(file_inputPath) as csvfile:  
        reader = csv.DictReader(csvfile)
        for row in reader:
            insName = row['Trade.Reference']
            tradeID = row['Trade No']
            insType =row['Instrument Type']
            portfolio = row['Portfolio']
            bookNode = row['Trade.Book Node']
            cobPL = row['Total PL COB']
            testData[tradeID]=[insName, tradeID, insType, portfolio, bookNode, cobPL, 0.00, 0.00, 0.00]
    return testData
    
def SOB_read_Amend_PL_csv_file(file_inputPath, testData):
    with open(file_inputPath) as csvfile:  
        reader = csv.DictReader(csvfile)
        for row in reader:
            insName = row['Trade.Reference']
            tradeID = row['Trade No']
            insType =row['Instrument Type']
            portfolio_sob = row['Portfolio']
            bookNode = row['Trade.Book Node']
            sobPL = row['Total PL SOB']
            if tradeID in testData:
                testData[tradeID][6]=sobPL
                testData[tradeID][3]=portfolio_sob
    return testData
    
def assign_amendmentPL(combinedData):
    exportData = {}
    for item in combinedData:
        insName = combinedData[item][0]
        tradeID = combinedData[item][1]
        insType = combinedData[item][2]
        portfolio = combinedData[item][3]
        bookNode = combinedData[item][4]
        COB_PL = combinedData[item][5]
        SOB_PL = combinedData[item][6]
        if SOB_PL != 0.00:
            amendmentPL = round((float(COB_PL) - float(SOB_PL)), 2)
            if amendmentPL != 0.00:
                trade = acm.FTrade[tradeID]
                if trade and checkAggregateTrade(trade):
                    tradeUpdateDate = trade.UpdateDay()
                    tradeUpdateUser = trade.UpdateUser().Name()
                    insUpdateDate = trade.Instrument().UpdateDay()
                    insUpdateUser = trade.Instrument().UpdateUser().Name()
                    if trade.Instrument().InsType() == 'Deposit' and trade.Instrument().OpenEnd() == 'Open End': #Funding Collateral PL
                        exportData[tradeID]=[insName, tradeID, insType, portfolio, bookNode, None, None, None, amendmentPL]
                    elif (tradeUpdateDate == today) or (insUpdateDate == today):
                        if (tradeUpdateUser == 'ATS') or (insUpdateUser == 'ATS'): #Resets PL
                            exportData[tradeID]=[insName, tradeID, insType, portfolio, bookNode, None, amendmentPL, None, None]
                        else: #Edits PL 
                            exportData[tradeID]=[insName, tradeID, insType, portfolio, bookNode, amendmentPL, None, None, None]
                    else: #Amendment Residual
                        exportData[tradeID]=[insName, tradeID, insType, portfolio, bookNode, None, None, amendmentPL, None]
    return exportData
       
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
        #col_Names = ['Trade.Instrument Name','Trade.Reference','Trade.Instrument Type','Trade.Portfolio','Edits PL', 'Resets PL', 'Amendment Residual', 'Funding Collateral PL']
        col_Names = ['Trade.Reference', 'Trade No', 'Instrument Type', 'Portfolio', 'Trade.Book Node', 'Edits PL', 'Resets PL', 'Amendment Residual', 'Funding Collateral PL']
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
                      'windowCaption': 'PL Explain Amendment PL Allocation'}

ael_variables = [ ['inputDatefolder', 'Input Date Folder', 'string', days, 'Today', 0],
                  ['inputPathSOB', 'Input Path SOB', 'string', None, default_input_path, 0],
                  ['input_fileNameSOB', 'Input File Name SOB', 'string', None, default_SOB_fileName, 0],
                  ['inputPathCOB', 'Input Path COB', 'string', None, default_input_path, 0],
                  ['input_fileNameCOB', 'Input File Name COB', 'string', None, default_COB_fileName, 0],
                  ['outputPath', 'Output Path', 'string', None, default_output_path, 0],
                  ['output_fileName', 'Output File Name', 'string', None, default_output_fileName, 0]]


       

def ael_main(ael_dict):
    date = os.path.join(ael_dict['inputDatefolder'])
    dateFolder = dateMappings[date]
    inputPathCOB = os.path.join(ael_dict['inputPathCOB'], dateFolder, ael_dict['input_fileNameCOB'])
    inputPathSOB = os.path.join(ael_dict['inputPathSOB'], dateFolder, ael_dict['input_fileNameSOB'])
    print("STARTED {0} {1}".format(today, _nowTime()))
    start_time = time.time()
    try:
        COB_Data = COB_read_Amend_PL_csv_file(inputPathCOB)
        SOB_Data = SOB_read_Amend_PL_csv_file(inputPathSOB, COB_Data)
        fileData = assign_amendmentPL(SOB_Data)
        if len(fileData) > 0:
            outputPath = os.path.join(ael_dict['outputPath'], dateFolder)
            write_outputPath = os.path.join(ael_dict['outputPath'])
            file = ael_dict['output_fileName']
            write_output_path(write_outputPath)
            write_output_csv(outputPath, file, fileData)
        else:
            print "No data to write to CSV file"
    except Exception as e:
        print 'Exception Raised: %s'%(e)
    end_time = time.time()
    duration = end_time - start_time
    print("Execution time (hh:mm:ss): {0}".format(_convertTimeInSecondsToHoursMinutesSeconds(duration)))
    print("FINISHED {0} {1}".format(today, _nowTime()))
    print ('Total Clock-Time: ' + str(datetime.timedelta(seconds=time.clock())))
