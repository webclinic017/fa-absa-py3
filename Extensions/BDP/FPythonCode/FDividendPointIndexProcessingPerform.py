""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/fixing/FDividendPointIndexProcessingPerform.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
    FDividendPointIndexProcessingPerform - Called from FDividendPointIndexProcessing

DESCRIPTION
    Main module for processing dividend point index instruments. 

----------------------------------------------------------------------------"""


import acm, ael
import FBDPCommon

from FBDPCurrentContext import Summary
from FBDPCurrentContext import Logme



def perform(dictionary):
    Logme()('Dividend Point Index Processing 1.0.1')
    day = acm.Time().DateToday()
    Logme()('Processing date: %s' % str(day))
    processor = FDividendPointIndexProcessor()
    processor.performProcess(dictionary)
    Summary().log(dictionary)
    Logme()(None, 'FINISH')
    

class FDividendPointIndexProcessor(object):
           
    def readArguments(self, dictionary):
        self.testmode = True
        if 'Testmode' in dictionary and dictionary['Testmode']:
            self.testmode = dictionary['Testmode']
        
        self.updateATMRef = False
        if 'StartDate' in dictionary and dictionary['StartDate']:
            self.StartDate = FBDPCommon.toDate(dictionary['StartDate'])
        
        if 'EndDate' in dictionary and dictionary['StartDate']:
            self.EndDate = FBDPCommon.toDate(dictionary['EndDate'])
        
        self.instruments = acm.FArray()
        if 'Instruments' in dictionary and dictionary['Instruments']:
            self.moveTo = self.instruments.AddAll(dictionary['Instruments'])
            
    def performProcess(self, dictionary):
        Logme()('Perform process', 'INFO')
        self.readArguments(dictionary)
        for instrument in self.instruments:
            Logme()('Processing dividend point index ' + instrument.Name(), 'INFO')
            instrument.RegenerateDividendCashFlows(self.StartDate, self.EndDate)
            if not self.testmode:
                instrument.Commit()
            Logme()('Processed dividend point index ' + instrument.Name(), 'INFO')

