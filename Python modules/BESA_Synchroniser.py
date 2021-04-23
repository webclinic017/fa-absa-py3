'''
Implementation of the BESA Synchronizer script.

Updates the Settle Category and Exchange Additional Info of Bonds, extracted from BESA file

Project               : BESA Synchronizer 
Department and Desk   : 
Requester             :  
Developer             : Nico Louw
CR Number             : CHNG0002212487

HISTORY
=============================================================================================
Date        CR number   Developer       Description
---------------------------------------------------------------------------------------------
 
---------------------------------------------------------------------------------------------
 
'''

import ael, acm, xlrd, os
import FRunScriptGUI
import FBDPGui
import FBDPString

logme = FBDPString.logme

FILE_NAME       = 'BESA.xlsx'
SCRIPT_NAME     = __name__

directorySelection = FRunScriptGUI.DirectorySelection()
directorySelection.SelectedDirectory('F:\\')

# Variable Name, Display Name, Type, Candidate Values, Default,
# Mandatory, Multiple, Description, Input Hook, Enabled
ael_variables = FBDPGui.LogVariables(['fileName', 'File name', 'string', None, FILE_NAME,
            1, 0, 'File name prefix. Will be followed by the date specifieds', None, 1],
        ['filePath', 'Directory', directorySelection, None, directorySelection,
            1, 1, 'Directory where files will be uploaded from', None, 1])

def update_exchange(ins, spec, value):
    '''
        This method updates and saves the additional info field of the instrument.
    '''
    spec = acm.FAdditionalInfoSpec[spec]
    addInfo = acm.FAdditionalInfo.Select01('recaddr = ' + str(ins.Oid()) + ' and addInf = ' + str(spec.Oid()), '')
        
    if addInfo == None:
        addInfo = acm.FAdditionalInfo() 
        addInfo.AddInf(spec)
        addInfo.Recaddr(ins.Oid())
        addInfo.FieldValue(value)
        addInfo.Commit() 

def upload_BESA_exchange(input_file):
    '''
        This method extracts the BESA information and updates the settlement category of instruments, based on
        whether they are price traded or yield traded. The method also updates the instrument's additional info 
        "Exchange" field to BESA
    '''
    priceTraded = acm.FChoiceList['PriceTraded']
    besa_exchange = acm.FChoiceList['BESA']
    
    workbook = xlrd.open_workbook(input_file)
    sheet = workbook.sheet_by_index(0)
    #Get number of rows excluding the header
    num_rows = sheet.nrows
    start_row = 4
    #Column number of instrument name
    ins_col = 0
    #Column number of settlement category
    traded_col = 33
    
    row = start_row
    while row < num_rows:
        insName = 'ZAR/' + str(sheet.cell(row, ins_col).value).strip()
        tradeType = str(sheet.cell(row, traded_col).value).strip()
        
        ins = acm.FInstrument[insName]
        if ins:
            try:
                if ins.AdditionalInfo().Exchange() != besa_exchange:
                    update_exchange(ins, 'Exchange', besa_exchange)

                if tradeType == 'PRICE':
                    #Change settle category to priceTraded
                    ins.SettleCategoryChlItem(priceTraded)
                    ins.Commit()
                
                logme('Instrument %s updated' % insName)
           
            except Exception:
                #Revert changes made to instrument if an error occurred
                ins.Undo()
                logme('Instrument %s not updated, Unhandled Instrument type: %s' % (insName, ins.InsType())  )
        else:
            logme('Instrument %s found in BESA, but not in Front Arena.' % insName)
        
        row += 1


# ---------------------------------------  MAIN -------------------------------------------- #

def ael_main(dictionary):

    logme.setLogmeVar(SCRIPT_NAME,
                      dictionary['Logmode'],
                      dictionary['LogToConsole'],
                      dictionary['LogToFile'],
                      dictionary['Logfile'],
                      dictionary['SendReportByMail'],
                      dictionary['MailList'],
                      dictionary['ReportMessageType'])

    filepath  = dictionary['filePath'].SelectedDirectory().Text()
    filename  = dictionary['fileName']

    directory = os.path.join(filepath, filename)
    
    if os.path.exists(directory):
        #call function with input file selected
        upload_BESA_exchange(directory)
        print '%s completed successfully' % SCRIPT_NAME
    else:
        logme('File: %s does not exist' % directory, 'ERROR')
        print '%s failed' % SCRIPT_NAME
    
    logme(None, 'FINISH')
