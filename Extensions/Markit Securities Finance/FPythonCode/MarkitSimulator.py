""" Compiled: 2020-09-18 10:38:56 """

#__src_file__ = "extensions/MarkitSecuritiesFinance/etc/MarkitSimulator.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    MarkitSimulator - script creates file which is simulation to the real Markit rates. 
    The file is zipped and in TSV(tab separated values) so it can be imported back into PRIME wihouth any modifications. 

    (c) Copyright 2018 FIS FRONT ARENA. All rights reserved.

-------------------------------------------------------------------------------------------------------"""

import acm
import FRunScriptGUI
import os
import random
import zipfile
import RandomMarkitFileCreation
from FOperationsIO import GetDefaultPath

class MarkitSimulator(FRunScriptGUI.AelVariablesHandler):

    def __init__(self):
        dirSelectionFile = FRunScriptGUI.DirectorySelection()
        dirSelectionFile.SelectedDirectory(str(GetDefaultPath()))
        variables = [
            #['exp_path', 'Export Path', 'string', None, 'C:\Temp',1 , 1, 'Enter the path where tsv file should be saved', None, 1],
            ['exp_path', 'Export Path', dirSelectionFile, None, dirSelectionFile, 1, 1, 'Enter the path where tsv file should be saved', None, None],
            ['file_name', 'File Name', 'string', None, 'MarkitRates', 1, 1, 'Enter fixed part of the file name. Full file name also have the current date and a random part.', None, 1]
        ]
    
        FRunScriptGUI.AelVariablesHandler.__init__(self, variables)
        
ael_variables = MarkitSimulator()

def ael_main(params):
    #define file name and path
    dt = acm.Time.DateToday()
    rint = random.randint(1, 1001)
    filePath = str(params['exp_path'])
    fileName = '{0}-{1}-{2}.tsv'.format(str(params['file_name'][0]), dt, rint)
    fileNameZip = '{0}-{1}-{2}.zip'.format(str(params['file_name'][0]), dt, rint)
    fullPath = os.path.join(filePath, fileName)
        
    #generate dictionary
    sLoans, list, dict = RandomMarkitFileCreation.CreateRandomMarkitFile()
    len = sLoans.Size()
    #create file from dictionary
    with open(fullPath, 'wb') as f: 
        for l in list:
            f.write(l)
            if l != list[-1]:
                f.write("\t")
        f.write('\n')
        
        for i in range(len):
            for l in list:
                f.write(str(dict[l][i]))
                if l != list[-1]:
                    f.write("\t")
            f.write('\n')

    #temp_path = os.getcwd()
    os.chdir(filePath)
    zf = zipfile.ZipFile(fileNameZip, mode='w') 
    zf.write(fileName) 
    zf.close()

    os.remove(fileName)

    #os.chdir(temp_path)