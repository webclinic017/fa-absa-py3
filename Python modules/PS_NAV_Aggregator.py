"""-----------------------------------------------------------------------------
PURPOSE                 :  This script looks at the generated NAV report xml files for previous business day,
                           Then aggregates all the NAV values into a csv file.
DEPATMENT AND DESK      :  Prime Services Dashboard + Market Risk NAV Feed
REQUESTER               :  Prime Services and Rishaan Ramnarain
DEVELOPER               :  Rohan van der Walt
CR NUMBER               :  2371269
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date        Change no  Developer                 Description
--------------------------------------------------------------------------------
2014-10-16  2371269    Rohan vd Walt             Initial Implementation
2014-11-26  2476290    Rohan vd Walt             Updated to run on new reports
"""

import xml.etree.ElementTree as ET
import unicodedata
import os
import csv
import at_time
import acm

from at_ael_variables import AelVariableHandler

ael_variables = AelVariableHandler()
ael_variables.add('ReportRootLocation',
                  mandatory=True,
                  label='NAV Report Location')
ael_variables.add('OutputLocation',
                  mandatory=True,
                  label='Report Output Location')
ael_variables.add('ReportName',
                  mandatory=True,
                  label='Output Filename')
ael_variables.add('isNewReport',
                  mandatory=True,
                  label='NAV Report 2?',
                  collection=['Yes', 'No'],
                  default='Yes',
                  alt='Yes = New NAV Report 2 file to be searched for\nNo = Old NAV report file name to be searched for'
                  )

def findValuationReports(reportRoot, isNewReport = 'Yes'):
    '''
    returns list of full paths to valuation files that need to be processed
    isNewReport = 'Yes' - Look for new NAV report format (includes date)
             'No' - Look for old NAV report format
    '''
    reportList = []
    reportDate = at_time.to_date('PREVBUSDAY')
    dirdate = reportDate.strftime("%Y-%m-%d")
    clientDirs = os.walk(reportRoot).next()[1]
    for clientDir in clientDirs:
        print 'Checking Dir:', os.sep.join([reportRoot, clientDir, dirdate])
        if os.path.isdir(os.sep.join([reportRoot, clientDir, dirdate])):
            try:
                for f in os.listdir(os.sep.join([reportRoot, clientDir, dirdate])):
                    #Old NAV report e.g. ABAXFIT_PS_Valuations_Report.xml
                    if isNewReport == 'No':
                        if f.endswith('PS_Valuations_Report.xml'):
                            reportList.append(os.sep.join([reportRoot, clientDir, dirdate, f]))
                            
                    #New NAV report e.g. ABAXFIT_Report_Valuations_20141008.xml
                    if isNewReport == 'Yes':
                        yyyyMMdd = reportDate.strftime("%Y%m%d")
                        if f.endswith('Report_Valuations_' + yyyyMMdd + '.xml'):
                            reportList.append(os.sep.join([reportRoot, clientDir, dirdate, f]))
            except Exception, e:
                print 'Something went wrong while trying to process:', os.sep.join([reportRoot, clientDir, dirdate])
    return reportList
    
def ael_main(params):
    results = []
    reportDate = at_time.to_date('PREVBUSDAY')
    for f in findValuationReports(params['ReportRootLocation'], params['isNewReport']):
        try:
            print 'Processing:', f
            tree = ET.parse(f)
            root = tree.getroot()
            PortfolioName = tree.find('./ReportParameters/PortfolioName').text
            PortfolioOID = tree.find('./ReportParameters/PortfolioOID').text
            clientDict = {'PortfolioName':PortfolioName, 'PortfolioOID':PortfolioOID}
            for repSec in root.findall("./ReportDetail/ReportSection"):
                if repSec.attrib['Name'] == 'NAV':
                    for row in repSec:
                        if row.attrib['Label'] == 'Total':
                            if params['isNewReport'] == 'No':
                                NavNetExp = row.find("./NetExposure").text
                                if isinstance(NavNetExp, unicode):
                                    NavNetExp = unicodedata.normalize('NFKD', NavNetExp).encode('ascii', 'ignore').replace(' ', '')
                                else: #NavNetExp is string
                                    NavNetExp = NavNetExp.replace(' ', '').replace(',', '')
                                clientDict['NavNetExp'] = NavNetExp
                            else:
                                FairValueNAV = row.find("./FairValueNAV").text
                                AccruedValueNAV = row.find("./AccruedValueNAV").text
                                if isinstance(FairValueNAV, unicode):
                                    FairValueNAV = unicodedata.normalize('NFKD', FairValueNAV).encode('ascii', 'ignore').replace(' ', '')
                                else: #NavNetExp is string
                                    FairValueNAV = FairValueNAV.replace(' ', '').replace(',', '')
                                if isinstance(AccruedValueNAV, unicode):
                                    AccruedValueNAV = unicodedata.normalize('NFKD', AccruedValueNAV).encode('ascii', 'ignore').replace(' ', '')
                                else: #NavNetExp is string
                                    AccruedValueNAV = AccruedValueNAV.replace(' ', '').replace(',', '')    
                                clientDict['FairValueNAV'] = FairValueNAV
                                clientDict['AccruedValueNAV'] = AccruedValueNAV
            clientDict['PortfolioCurr'] = acm.FCompoundPortfolio[PortfolioName].Currency().Name()
            clientDict['Date'] = reportDate
            results.append(clientDict)
        except Exception, e:
            print 'ERROR while processing NAV file: ', f, '\n', e, '\nIt will be excluded from NAV_Summary.csv'
    try:
        print 'Writing results to file'
        outFile = open(os.sep.join([params['OutputLocation'], params['ReportName'] + '.csv']), 'wb')
        myWriter = csv.writer(outFile)
        keyList = [k for k in clientDict.keys()]
        myWriter.writerow(keyList)
        for row in results:
            myWriter.writerow([row[k] for k in keyList])
        outFile.close()
        print 'Wrote secondary output to::: ' + outFile.name
    except Exception, e:
        print 'ERROR while opening/writing to file: ', '\n', e
