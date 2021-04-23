"""-----------------------------------------------------------------------------
PROJECT                 : ACS SBL Migragtion
PURPOSE                 : Creates a update file to load in Global 1, that will update the FA trade ref number on the global one trades.
                            Global 1 trade numbers must be in text1 and text2 fields on trades.
                            Use ASQL to get list of trades, and save them to CSV for input to this file
DEPATMENT AND DESK      : Prime Services, Securities Lending
REQUESTER               : Linda Breytenbach
DEVELOPER               : Francois Truter, R vd W
CR NUMBER               : 450056, 824046
--------------------------------------------------------------------------------
"""

from datetime import date
from datetime import datetime
from decimal import Decimal
from sl_global_one_upload_file import GlUploadFile
import acm
import string
import csv
import sl_functions
import FRunScriptGUI
import time

G1_Lender_FILEPATH = 'F:\\update_lender_trades_in_g1.txt'

G1_Borrower_FILEPATH = 'F:\\update_borrower_trades_in_g1.txt'

G1_Fund_FILEPATH = 'F:\\update_fund_trades_in_g1.txt'

def getTradeCategory(trade):
    '''
        (if rolling period 1d) = MD   Mark Daily: Trade to be M-T-M daily on or after settlement date is reached.
        (if rolling period 1w and rolling base day is Monday)MM   Mark Monday: Trade to be M-T-M weekly every Monday on or after settlement date is reached. If Monday is a holiday then the trade will be M-T-M on the following Friday.
        (if rolling period 1w and rolling base day is Friday) MF   Mark Friday: Trade to be M-T-M weekly every Friday after on or settlement date is reached. If Friday is a holiday then the trade will be M-T-M on the following Monday.
    '''
    nst = acm.Time()
    rollingPeriod = trade.Instrument().PayLeg().RollingPeriod()
    if str(rollingPeriod).upper() == '1D':
        return 'MD'     #MARK DAILY
    elif str(rollingPeriod).upper() == '1W':
        rollingBase = trade.Instrument().PayLeg().RollingPeriodBase()
        dow = nst.DayOfWeek(rollingBase)
        if dow == 'Monday':
            return 'MM'
        elif dow == 'Friday':
            return 'MF'
    return None

def _addUploadRecord(uploadFile, trade, g1Ref, faRef):
    record = uploadFile.CreateRecord(trade)
    record.Status.Value('U')
    record.TransactionType.Value('T')
    
    record.GlobalOneTradeReference.Value(g1Ref)
    record.OwnContractReference.Value(faRef)
    record.TradeCategory.Value(getTradeCategory(trade))
    record.CollateralType.Value('')
    
def lender(filepath):
    g1UploadFile = GlUploadFile() 
    reader = csv.reader(open(filepath, "rb"))
    for row in reader:
        if reader.line_num >= 1:
            t = string.strip(str(row[0]))#given that the 1st column in the csv file is the FA trade number
            print 'trdnbr', t
            g1TradeL = string.strip(str(row[1]))#given that the 2nd column in the csv file is the g1 trade reference of the lender record
            print 'g1TradeL', g1TradeL
            #g1TradeB = string.strip(str(row[2]))#given that the 3rd column in the csv file is the g1 trade reference of the borrower record
            #print 'g1TradeB',g1TradeB
    
            frontTrade = acm.FTrade[t]

            _addUploadRecord(g1UploadFile, frontTrade, g1TradeL, str(frontTrade.Oid()) + 'L')

        g1UploadFile.WriteFile(G1_Lender_FILEPATH, None, False)

def borrower(filepath):
    g1UploadFile = GlUploadFile() 
    reader = csv.reader(open(filepath, "rb"))
    for row in reader:
        if reader.line_num >= 1:
            t = string.strip(str(row[0]))#given that the 1st column in the csv file is the FA trade number
            print 'trdnbr', t
            #g1TradeL = string.strip(str(row[1]))#given that the 2nd column in the csv file is the g1 trade reference of the lender record
            #print 'g1TradeL',g1TradeL
            g1TradeB = string.strip(str(row[2]))#given that the 3rd column in the csv file is the g1 trade reference of the borrower record
            print 'g1TradeB', g1TradeB

            frontTrade = acm.FTrade[t]
            
            _addUploadRecord(g1UploadFile, frontTrade, g1TradeB, str(frontTrade.Oid()) + 'B')

        g1UploadFile.WriteFile(G1_Borrower_FILEPATH, None, False)

def fund(filepath):
    g1UploadFile = GlUploadFile() 
    reader = csv.reader(open(filepath, "rb"))
    for row in reader:
        if reader.line_num >= 1:
            t = string.strip(str(row[0])) #given that the 1st column in the csv file is the FA trade number
            print 'trdnbr', t
            g1Trade = string.strip(str(row[1]))#given that the 2nd column in the csv file is the g1 trade reference of fund trade and that the 3rd column is blank
            print 'g1Trade', g1Trade

            frontTrade = acm.FTrade[t]

            _addUploadRecord(g1UploadFile, frontTrade, g1Trade, frontTrade.Oid())

        g1UploadFile.WriteFile(G1_Fund_FILEPATH, None, False)

fileSelection = FRunScriptGUI.InputFileSelection("All Files (*.*)|*.*||")
fileKey = '0'

ael_variables = [
    [fileKey, 'Input File', fileSelection, None, fileSelection, 1, 1, 'The file containing the Global One trades.', None, 1],
    ['lender', 'Lender', 'string', ['No', 'Yes'], 'No', 1, 0, 'Generate Global one Lender trade update file for these Front Arena trades', None, 1],
    ['borrower', 'Borrower', 'string', ['No', 'Yes'], 'No', 1, 0, 'Generate Global one Borrower trade update file for these Front Arena trades', None, 1],
    ['fund', 'Fund', 'string', ['No', 'Yes'], 'No', 1, 0, 'Generate Global one Fund trade update file for these Front Arena trades', None, 1],
    ]

def ael_main(parameters):
    
    logFile = parameters[fileKey]        
    if parameters['lender'] == 'Yes':
        lender(logFile.SelectedFile().Text())
    if parameters['borrower'] == 'Yes':
        borrower(logFile.SelectedFile().Text())
    if parameters['fund'] == 'Yes':
        fund(logFile.SelectedFile().Text())
