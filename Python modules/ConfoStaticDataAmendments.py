'''
Project               : Party Static Data 
Department and Desk   : 
Requester             :  
Developer             : Phumzile Mgcima
CR Number             : 

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
FILE_NAME       = 'ConfoStaticDataAmendments.xlsx'
SCRIPT_NAME     = __name__

directorySelection = FRunScriptGUI.DirectorySelection()
directorySelection.SelectedDirectory('F:\\')

# Variable Name, Display Name, Type, Candidate Values, Default,
# Mandatory, Multiple, Description, Input Hook, Enabled
ael_variables = FBDPGui.DefaultVariables(['fileName', 'File name', 'string', None, FILE_NAME,
            1, 0, 'File name prefix.', None, 1],
        ['filePath', 'Directory', directorySelection, None, directorySelection,
            1, 1, 'Directory where files will be uploaded from', None, 1])

def update_conformation_transport(partyName, instructName, transportType):
    party = acm.FParty[partyName]
    if party:
        partyClone = party.Clone()
        instructions = partyClone.ConfInstructions()
        for instruct in instructions:
        
            if instruct.Name() in instructName:
                transport = instruct.Transport()
                instruct.Transport(transportType)
                break
        party.Apply(partyClone)
        party.Commit()
    else:
        print partyName, ',', 'NOT FOUND'


def upload_party_static_data(input_file):
    workbook = xlrd.open_workbook(input_file)
    sheet = workbook.sheet_by_index(0)
    #Get number of rows excluding the header
    num_rows = sheet.nrows
    start_row = 2
    #Column number of instrument name
    ins_col = 0
    
    row = start_row
    while row < num_rows:
        partyName = str(sheet.cell(row, ins_col).value).strip()
        instructName = str(sheet.cell(row, ins_col+1).value).strip()
        transportType = str(sheet.cell(row, ins_col+2).value).strip()
        update_conformation_transport(partyName, instructName, transportType)
        row += 1
       
# ---------------------------------------  MAIN -------------------------------------------- #

def ael_main(dictionary):
                
   

    filepath  = dictionary['filePath'].SelectedDirectory().Text()
    filename  = dictionary['fileName']

    directory = os.path.join(filepath, filename)
    
    if os.path.exists(directory):
        upload_party_static_data(directory)
        print '%s completed successfully' % SCRIPT_NAME
    else:
        print 'File: %s does not exist' % directory 
        print '%s failed' % SCRIPT_NAME
    
    print 'FINISH'
