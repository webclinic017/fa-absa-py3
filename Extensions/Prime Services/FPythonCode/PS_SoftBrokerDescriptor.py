'''
-----------------------------------------------------------------------------
PROJECT                 :  Prime Services
PURPOSE                 :  Generates the descriptor file for the reports for a party
                            after all pdf files have been dumped to the canned report
                            landing area for soft broker
DEPATMENT AND DESK      :  
REQUESTER               :  
DEVELOPER               :  Rohan van der Walt
CR NUMBER               :  699989
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date       Change no Developer                 Description
--------------------------------------------------------------------------------
2011-06-30 699989    Rohan van der Walt        Initial Implementation
2011-07-07 707904    Rohan van der Walt        Use PrevBusinessDay as report date in descriptor
'''

import os
import xml.etree.ElementTree, datetime, time, acm


def getUniqueKey():
    time.sleep(0.01)
    return str(datetime.datetime.now()).replace(':', '').replace('-', '').replace('.', '').replace(' ', '')[:-12]

class DescriptorFile():
    def __init__(self):
        self.root = xml.etree.ElementTree.XML('<GeneralStorageImportSchema></GeneralStorageImportSchema>')
        self.count = 0

    def addReport(self, detailsDict):
        xml.etree.ElementTree.SubElement(self.root, 'ContractNote', attrib=detailsDict)
        self.count = self.count + 1

    def __str__(self):
        return xml.etree.ElementTree.tostring(self.root)

    def getReportCount(self):
        return self.count


ael_variables = [
['accId', 'Soft Broker AccountID', 'string', None, None, 1, 0, 'Account ID that will have access to these reports', None, 1],
['date', 'Date', 'string', None, None, 0, 0, 'Date that will be but in descriptor files - Report Date - If blank, will use current date', None, 1],
['OutputPath', 'OutputPath', 'string', None, 'C:\\', 1, 0, 'Directory where output file should be written', None, 1]
]

ael_gui_parameters = {'windowCaption':'Generate Descriptor file for Soft Broker'}

def ael_main(dict):
    '''
    Script inputs:
        Party for who to generate descriptor file
    '''

    reportDescriptions = {'PS_Cash_Trans_Report.pdf':('Margin Call Statement', 'PB_MCS_'),
                            'PS_Corporate_Actions_Report.pdf':('Distributions', 'PB_CAS_'),
                            'PS_EQ_Trade_Activity_Report.pdf':('Equity Trade Activity', 'PB_EQT_'),
                            'PS_FI_Position_Summary_Report.pdf':('Fixed Income Position Summary', 'PB_FIP_'),
                            'PS_FI_Trade_Activity_Report.pdf':('Fixed Income Trade Activity', 'PB_FIT_'),
                            'PS_EQ_Position_Summary_Report.pdf':('Equity Position Summary', 'PB_EQP_'),
                            'PS_Hist_Perf_Summary_Report.pdf':('Historical Performance Summary', 'PB_HPS_'),
                            'PS_Daily_Perf_Summary_Report.pdf':('Daily Performance Summary', 'PB_DPS_'),
                            'PS_Voided_Trade_Report.pdf':('Voided Trade Report', 'PB_VTR_'),
                            'PS_Finance_Report.pdf':('Finance Report', 'PB_FNR_')}

    print 'Starting:::'
    dict['OutputFile'] = 'PB_CR_' + getUniqueKey() + '.xml'
    nst = acm.Time()
    if dict['date'] == "":
        cal = acm.FCalendar['ZAR Johannesburg']
        today = acm.Time().DateToday()
        dict['date'] = first = cal.AdjustBankingDays(today, -1)
    outFilePath = dict['OutputPath'] + dict['OutputFile']
    df = DescriptorFile()
    details = {}

    #Settings constant properties
    details['AcctID'] = dict['accId']   #Registered account on SoftBroker that can view this report
    details['Date'] = dict['date']
    details['FileType'] = 'PDF'

    for filename in os.listdir(dict['OutputPath']):
        (name, ext) = os.path.splitext(filename)
        if ext.lower().endswith("pdf"):
            if filename in reportDescriptions:
                print "FOUND %s - Processing" % filename
                details['Description'] =  '%s - %s' % (reportDescriptions[filename][0], details['Date'])
                details['Filename'] = filename
                details['UniqueKey'] = reportDescriptions[filename][1] + getUniqueKey()
                df.addReport(details)
            else:
                print "File %s not one of expected reports" % filename
        elif ext.lower().endswith(".fo"):
            file_path = os.path.join(dict['OutputPath'], filename)
            os.unlink(file_path)

    if df.getReportCount() > 0:
        with open(outFilePath, 'w') as csvFile:
            csvFile.write(str(df))
        print 'Wrote secondary output to:::', outFilePath
    print 'Completed Successfully:::'
