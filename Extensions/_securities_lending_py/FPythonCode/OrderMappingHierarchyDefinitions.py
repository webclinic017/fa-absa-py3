""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/SecuritiesLending/etc/OrderMappingHierarchyDefinitions.py"
"""------------------------------------------------------------------------------------------------
MODULE
    OrderMappingHierarchyDefinitions

    (c) Copyright 2018 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    Hierarchy Definitions

------------------------------------------------------------------------------------------------"""


def Prefix(s) :
    P = 'SecLending'                                   # A prefix added to all the names below
    return P + s

class Names :
    HierarchyInstance = Prefix('FileExport')      # The name of the Hierarchy instance (including prefix the name will be "SecLendingFileExport")
    HierarchyType =     Prefix('Definition')        # The name of the Hierarchy type 

class ChoiceListNames :
    FileDestination =   Prefix('FileDestination')       # Choice list created to capture the various types of source file types (including prefix the choice list name will be SecLendingFileDestinationTypes)
    OutputTemplates =   Prefix('OutputTemplates')       # Choice list to capture the valid XSL Templates used to create the output file
    FileTypes =         Prefix('FileTypes')             # Choice list to capture the valid file types

class ChoiceListDefs :
    Def = [ 
           {'Name':      ChoiceListNames.FileDestination,
            'Values':    ['FTP Service', 'E-mail Service', 'Clipboard']},   # Choice list values for the FileDestinationTypes

           {'Name':      ChoiceListNames.OutputTemplates,
            'Values':    ['CommaSeparatedReportTemplate', 'SemicolonSeparatedReportTemplate', 'CommaSeparatedNoLabelRow']}, # Choice list values for the OutputTemplates

           {'Name':      ChoiceListNames.FileTypes,
            'Values':    ['.txt', '.csv']}              # Choice list values for the FileTypes
          ]
          
class ColumnDefs :
    Def = [ 
           {'Name':                 'Counterparty',     # Hierarchy column to specify the Counterparty
            'TypeGroup':            'RecordRef',  
            'TypeString':           'Party', 
            'TypeInfo':             '', 
            'LeavesOnly':           False, 
            'Description':          'The counterparty of the order'},

           {'Name':                 'Destination', # Hierarchy column to specify the File Destination
            'TypeGroup':            'RecordRef',  
            'TypeString':           'ChoiceList', 
            'TypeInfo':             ChoiceListNames.FileDestination, 
            'LeavesOnly':           True, 
            'Description':          'The destination of the file, FTP or mail'},

           {'Name':                 'Report Name', # Hierarchy column to specify name of the Report (please note that date and time stamp wil be added)
            'TypeGroup':            'Standard',  
            'TypeString':           'String', 
            'TypeInfo':             '', 
            'LeavesOnly':           False, 
            'Description':          'The name of the report created'},

           {'Name':                 'Output Template',  # Hierarchy column to specify the Output XSL Template
            'TypeGroup':            'RecordRef',  
            'TypeString':           'ChoiceList', 
            'TypeInfo':             ChoiceListNames.OutputTemplates, 
            'LeavesOnly':           False, 
            'Description':          'The XSL Template used'},

           {'Name':                 'Trade Sheet Template', # Hierarchy column to specify the Trade Sheet Template
            'TypeGroup':            'Standard',  
            'TypeString':           'String', 
            'TypeInfo':             '', 
            'LeavesOnly':           False, 
            'Description':          'The name of the trade sheet template'},

           {'Name':                 'Output Path',      # Hierarchy column to specify where the report file will be stored on disk
            'TypeGroup':            'Standard',  
            'TypeString':           'String', 
            'TypeInfo':             '', 
            'LeavesOnly':           False, 
            'Description':          'The path to the directory the output is stored in'},

           {'Name':                 'File Type',        # Hierarchy column to specify the report file type
            'TypeGroup':            'RecordRef',  
            'TypeString':           'ChoiceList', 
            'TypeInfo':             ChoiceListNames.FileTypes, 
            'LeavesOnly':           False, 
            'Description':          'The type of the file produced'}
         ]


class DefaultReportingSheet:
    Name = Prefix('GeneralExportTemplate')
    SheetType = "FTradeSheet"
    Columns = [ "Security Loan Quantity",\
                "Security Loan Orders Rate",\
                "Security Loan Security",\
                "Trade Value Day",\
                "Instrument End Date"]

class Hierarchy:
    Def = [
          {'DisplayName':        'File Export', 
           'Children': [
                       {'DisplayName':        'DEFAULT',
                        'Children': [
                                    {'Destination':         'Clipboard',
                                     'Output Template':     'CommaSeparatedNoLabelRow',
                                     'Trade Sheet Template': DefaultReportingSheet.Name
                                    }
                                    ]
                        }
                        ]
            }
            ]
        
