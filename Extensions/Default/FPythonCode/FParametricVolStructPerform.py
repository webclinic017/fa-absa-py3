""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/mark_to_market/etc/FParametricVolStructPerform.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
    FParametricVolStructPerform - Called from FParametricVolStruct

DESCRIPTION
    Main module for calculating volatility structures. 

----------------------------------------------------------------------------"""


import acm, ael

from FBDPCurrentContext import Summary
from FBDPCurrentContext import Logme

import moveVolatilityStructureToLast
import moveVolatilityStructureToMid
import moveVolatilityStructureToCallPut


def perform(dictionary):
    Logme()('Calculate Volatility Structures 1.0.1')
    day = acm.Time().DateToday()
    Logme()('Calculation date: %s' % str(day))
    processor = ParametricVolStructureProcessor()
    processor.performProcess(dictionary)
    Summary().log(dictionary)
    Logme()(None, 'FINISH')
    

class ParametricVolStructureProcessor(object):
           
    def readArguments(self, dictionary):
        self.testmode = True
        if 'Testmode' in dictionary and dictionary['Testmode']:
            self.testmode = dictionary['Testmode']
        
        self.updateATMRef = False
        if 'UpdateATMRef' in dictionary and dictionary['UpdateATMRef']:
            self.updateATMRef = dictionary['UpdateATMRef']
        
        self.volStructures = acm.FArray()
        if 'VolStructures' in dictionary and dictionary['VolStructures']:
            self.volStructures.AddAll(dictionary['VolStructures'])
        
        if 'MoveTo' in dictionary and dictionary['MoveTo']:
            self.moveTo = dictionary['MoveTo']
        
        if self.moveTo == 'Mid':
            self.MoveSkew = moveVolatilityStructureToMid.MoveSkewToMid
        elif self.moveTo == 'Last':
            self.MoveSkew = moveVolatilityStructureToLast.MoveSkewToLast
        elif self.moveTo == 'Call/Put':
            self.MoveSkew = moveVolatilityStructureToCallPut.MoveSkewToCallPut
            
    def performProcess(self, dictionary):
        Logme()('Perform process', 'INFO')
        self.readArguments(dictionary)
        self.getVolManagerSettings()
        for volStructure in self.volStructures:
            Logme()('Processing volatility structure ' + volStructure.Name(), 'INFO')
            if self.updateATMRef:
                #check for reference instrument
                if not volStructure.ReferenceInstrument():
                    Logme()('Vol Structure has no reference instrument',
                            'WARN')
                #then
                #update underlying refs
                volStructure.UpdateUnderlyingForwards()
            self.moveVolStructure(volStructure)
            if not self.testmode:
                volStructure.Commit()
    
    def getVolManagerSettings(self):
        #Fetch the Volatility Manager Settings
        Logme()('Getting Volatility Manager Settings', 'INFO')
        preferences = acm.FACMServer().GetUserPreferences()
        volPreferences = preferences.VolMgrPreferences()

        self.excludeBidAskZeros = volPreferences.At(2)
        self.useVolumeWeightedMid = volPreferences.At(15)
        self.excludeOutliers = volPreferences.At(16)
        self.outlierPercentage = volPreferences.At(17)
    
    def getVolStructureFilter(self, volStructure):
        # get the volatility structure filter
        Logme()('Getting volatility structure Filter', 'INFO')
        name = volStructure.Name()
        volStructureFilter = acm.FStoredASQLQuery[name + '_PlotFilter']
        if not volStructureFilter:
            volStructureFilter = acm.FStoredASQLQuery[name]
        
        if not volStructureFilter:
            Logme()('Failed to get volatility structure filter', 'ERROR')
        
        return volStructureFilter
    
    def getOrderBooks(self, volStructure):
        volStructureFilter = self.getVolStructureFilter(volStructure)
        query = volStructureFilter.Query()
        results = query.Select()
        expiryDates = {}
        for instrument in results:
            if instrument.IsKindOf(acm.FInstrument):
                orderbook = instrument.DefaultOrderBook()
            else:
                orderbook = instrument
            
            if instrument.ActualExpiryDay() not in list(expiryDates.keys()):
                books = acm.FArray()
                books.Add(orderbook)
                expiryDates[instrument.ActualExpiryDay()] = books
            else:
                expiryDates[instrument.ActualExpiryDay()].Add(orderbook)
        
        return expiryDates
    
    def getOrderBooksForSkew(self, skew, expiryDates):
        orderbooks = expiryDates[skew.ExpiryDay()]
        return orderbooks
        
    def moveVolStructure(self, volStructure):
        expiryDates = self.getOrderBooks(volStructure)
        skews = volStructure.Skews()
        for skew in skews:
            orderbooks = expiryDates[skew.ExpiryDay()]
            Logme()('Processing skew ' + skew.ExpiryDay())
            # Create an IVPCollectio using the Instrument Order Books
            impVols = acm.FIVPCollection()
            impVols.CreateOrderBookDependent(orderbooks)
            impVols.UpdateImpVolas(orderbooks, acm.GetDefaultContext())
            self.MoveSkew(volStructure,
                             skew,
                             orderbooks,
                             impVols,
                             self.excludeBidAskZeros,
                             self.useVolumeWeightedMid,
                             self.excludeOutliers,
                             self.outlierPercentage)
