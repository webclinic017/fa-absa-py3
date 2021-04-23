"""-----------------------------------------------------------------------------
PROJECT                 :  Prime Services
PURPOSE                 :  
DEPATMENT AND DESK      :  Prime Services
REQUESTER               :  Francois Henrion
DEVELOPER               :  Herman Hoon
CR NUMBER               :  759616
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date       Change no Developer                 Description
--------------------------------------------------------------------------------
2011-07-13 759616    Herman Hoon               Initial Implementation
2012-02-08 889960    Rohan van der Walt        Integration with ReportController
2012-11-21 620753    Hynek Urban               Descriptor generation refactor.
2013-06-18 1106832   Hynek Urban               Remove descriptor-related logic.
2014-06-05 2018619   Libor Svoboda             Handling errors in PB overnight batch correctly
                                               Update of writeFile method (try/except removed)
"""

import csv
import os

import acm
import ael 
import ABSA_Rate

from PS_FormUtils import DateField


class CurvePublication():

    def __init__(self, yieldCurve):
        '''Initialises the variables and value dictionary based on the set columns and sections
        '''        
        self.bmList     = []
        self.yieldCurve = yieldCurve
        self.Headings = [('YieldCurve', 'Benchmark', 'Date', 'Price', 'Discount Factor')]

    def _getPrice(self, ins, market, date):
        '''Returns the price of the instrument
        '''
        prices = ins.Prices()
        for p in prices:
            if p.Market().Name() == market:
                return p.Settle()
        return ''
        
    def _populateBenchmarkList(self):
        '''Populates the Benchmark list
        '''
        date    = ael.date_today()
        acmDate = acm.Time.DateNow()
        MARKET  = 'SPOT' 
        for bm in self.yieldCurve.BenchmarkInstruments():
            expiryDate = bm.ExpiryDateOnly()
            price      = self._getPrice(bm, MARKET, acmDate)
            rate       = ABSA_Rate.ABSA_yc_rate('temp', self.yieldCurve.Name(), date,  ael.date(expiryDate), 'Annual Comp', 'Act/365', 'Discount', bm.Name())
            values     = self.yieldCurve.Name(), bm.Name(), expiryDate, price, rate
            self.bmList.append(values)
        self.bmList = sorted(self.bmList, key = lambda (v, w, x, y, z): (x, v, w, y, z))
    
    def writeFile(self, filepath, fullname):
        '''Writes the file
        '''
        directory = os.path.join(filepath, fullname)
        with open(directory, 'wb') as ofile:
            writer = csv.writer(ofile, dialect='excel') 
            writer.writerows(self.Headings)
            writer.writerows(self.bmList)
            print 'Wrote secondary output to: %s' %(directory)


FILE_NAME  = 'PS_CurvePublication'
FILE_TYPES = ['csv']

ael_variables = [
    ['OutputPath', 'Output Path', 'string', None, 'F:\\', 1, 0, 'Where reports will be generated', None, 1],
    ['fileName', 'File name', 'string', None, FILE_NAME, 1, 0, 'File name prefix. Will be followed by the yield curve name.', None, 1],
    ['fileType', 'File type', 'string', FILE_TYPES, 'csv', 1, 0, 'File name prefix. Will be followed by the yield curve name.', None, 1],                   
    ['yieldCurves', 'Yield Curves', acm.FYieldCurve, acm.FYieldCurve.Select(''), 'ZAR-SWAP, ZAR-BOND', 0, 1, 'For each of these Yield Curves a curve publication report will be generated.', None, 1],
]

def _convertToParamDictionary(config, reportName):
    '''
    Gets called from report controller on custom reports to return a compatible report dictionary
    '''
    result = {
        'OutputPath': config['OutputPath'],
        'fileType': 'csv',
    }
    if 'yieldCurves_' + reportName in config: # Old ReportController.
        result['yieldCurves'] = config['yieldCurves_' + reportName]
        result['fileName'] = config['fileID_SoftBroker'] + '_' +\
                config['Filename_' + reportName] + '_%s'
    else: # PS_ReportController2 - allows for a single yieldcurve only and supplies a date suffix.
        result['yieldCurves'] = [config['yieldCurve_' + reportName],]
        date_suffix = DateField.read_date(config['date_SoftBroker'],
            default=acm.Time.DateToday()).replace('-', '')
        result['fileName'] = config['fileID_SoftBroker'] + '_' +\
                config['Filename_' + reportName] + '_%s_' + date_suffix
    # The %s placeholder in the filename will be replaced by the yieldcurve name.
    
    return result

def ael_main(dict):
    print 'Starting report generation'
    yieldCurves = dict['yieldCurves']
    filenames = []
    print yieldCurves
    for yieldCurve in yieldCurves:
        curvePub = CurvePublication(yieldCurve)
        curvePub._populateBenchmarkList()
        fileName = dict['fileName']
        fileType = dict['fileType']
        try:
            fullName = ''.join([fileName % yieldCurve.Name(), '.', fileType])
        except TypeError: # Filename doesn't contain a yieldcurve name placeholder.
            fullName = ''.join([fileName, '_', yieldCurve.Name(), '.', fileType])
        curvePub.writeFile(dict['OutputPath'], fullName)
        filenames.append(fullName)
        
    print 'Finished'
    print 'Completed Successfully'
    return filenames

