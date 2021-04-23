""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/SecuritiesLending/etc/FSecLendTests.py"

"""--------------------------------------------------------------------------
MODULE
    FSecLendTests

    (c) Copyright 2018 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    Test script to be run for verifying if all views start with their panels

---------------------------------------------------------------------------"""

import ael
import acm
import unittest
import FIntegratedWorkbench as iw
import FUxCore

def CreateApplicationInstance():
    return FSecLendTestsApplication()

def ReallyStartApplication(shell, count):
    acm.UX().SessionManager().StartApplication('FSecLendTests', None)

def StartApplication(eii):
    shell = eii.ExtensionObject().Shell()
    ReallyStartApplication(shell, 0);

class FSecLendTestsApplication(FUxCore.LayoutApplication, object):
    def __init__(self):
        self._testsStarted = False

    def HandleCreate(self, creationInfo):
        self.EnableOnIdleCallback(True)

    def HandleOnIdle(self):
        if not self._testsStarted:
            self._testsStarted = True
            ael_main( 0 )

ael_variables = []
params = []
def ael_main(params): 
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSecLendOrdersView)
    unittest.TextTestRunner().run(suite)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSecLendClientView)
    unittest.TextTestRunner().run(suite)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSecLendInventoryView)
    unittest.TextTestRunner().run(suite)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSecLendPortfolioView)
    unittest.TextTestRunner().run(suite)

class TestSecLendOrdersView(unittest.TestCase):

    def setUp(self):
        myView            = 'SecLendOrdersView'
        self.app          = iw.LaunchView(myView)
        self.view         = iw.GetView(self.app)
        self.panels       = self.view.Panels()
        
    def tearDown(self):
        self.app.Close('DontSave')
        
    def test_OrderPanelsAvailable(self):
        print('Validating SecLendOrdersWorkbookPanel..')
        thePanel = self.view.Panel('SecLendOrdersWorkbookPanel')
        self.assertIsNotNone(thePanel)
        
        print('Validating SecLendOrdersBlotterTodayPanel..')
        thePanel = self.view.Panel('SecLendOrdersBlotterTodayPanel')
        self.assertIsNotNone(thePanel)
        
        print('Validating SecLendOrdersBlotterYesterdayPanel..')
        thePanel = self.view.Panel('SecLendOrdersBlotterYesterdayPanel')
        self.assertIsNotNone(thePanel)
        
        print('Validating SecLendOrdersBlotterMonthPanel..')
        thePanel = self.view.Panel('SecLendOrdersBlotterMonthPanel')
        self.assertIsNotNone(thePanel)
        
        print('Validating SecLendOrdersBlotterPositionsPanel..')
        thePanel = self.view.Panel('SecLendOrdersBlotterPositionsPanel')
        self.assertIsNotNone(thePanel)
        
        print('Validating SecLendOrdersBlotterFilterPanel..')
        thePanel = self.view.Panel('SecLendOrdersBlotterFilterPanel')
        self.assertIsNotNone(thePanel)
        
        print('Validating SecLendOrdersOrderCapturePanel..')
        thePanel = self.view.Panel('SecLendOrdersOrderCapturePanel')
        self.assertIsNotNone(thePanel)
        

class TestSecLendClientView(unittest.TestCase):

    def setUp(self):
        myView            = 'SecLendClientView'
        self.app          = iw.LaunchView(myView)
        self.view         = iw.GetView(self.app)
        self.panels       = self.view.Panels()
        
    def tearDown(self):
        self.app.Close('DontSave')
        
    def test_ClientPanelsAvailable(self):
        print('Validating SecLendClientPositionsPanel..')
        thePanel = self.view.Panel('SecLendClientPositionsPanel')
        self.assertIsNotNone(thePanel)
        
        print('Validating SecLendClientFilterPanel..')
        thePanel = self.view.Panel('SecLendClientFilterPanel')
        self.assertIsNotNone(thePanel)
        
        print('Validating SecLendClientDetailsPanel..')
        thePanel = self.view.Panel('SecLendClientDetailsPanel')
        self.assertIsNotNone(thePanel)
        
        print('Validating SecLendClientPositionsFilterPanel..')
        thePanel = self.view.Panel('SecLendClientPositionsFilterPanel')
        self.assertIsNotNone(thePanel)
        
        print('Validating SecLendClientTradesPanel..')
        thePanel = self.view.Panel('SecLendClientTradesPanel')
        self.assertIsNotNone(thePanel)
        
        print('Validating SecLendReratePanel..')
        thePanel = self.view.Panel('SecLendReratePanel')
        self.assertIsNotNone(thePanel)
        
        
class TestSecLendInventoryView(unittest.TestCase):

    def setUp(self):
        myView            = 'SecLendInventoryView'
        self.app          = iw.LaunchView(myView)
        self.view         = iw.GetView(self.app)
        self.panels       = self.view.Panels()
        
    def tearDown(self):
        self.app.Close('DontSave')
        
    def test_InventoryPanelsAvailable(self):
        print('Validating SecLendInventoryWorkbookPanel..')
        thePanel = self.view.Panel('SecLendInventoryWorkbookPanel')
        self.assertIsNotNone(thePanel)
        
        print('Validating SecLendInventoryFilterPanel..')
        thePanel = self.view.Panel('SecLendInventoryFilterPanel')
        self.assertIsNotNone(thePanel)
        
        print('Validating SecLendInventoryActivePanel..')
        thePanel = self.view.Panel('SecLendInventoryActivePanel')
        self.assertIsNotNone(thePanel)
        
        print('Validating SecLendInventoryPendingPanel..')
        thePanel = self.view.Panel('SecLendInventoryPendingPanel')
        self.assertIsNotNone(thePanel)
        
        print('Validating SecLendInventoryInternalPanel..')
        thePanel = self.view.Panel('SecLendInventoryInternalPanel')
        self.assertIsNotNone(thePanel)
        
        print('Validating SecLendInventoryInstrumentDetailsPanel..')
        thePanel = self.view.Panel('SecLendInventoryInstrumentDetailsPanel')
        self.assertIsNotNone(thePanel)
        
        print('Validating SecLendInventoryExternalPanel..')
        thePanel = self.view.Panel('SecLendInventoryExternalPanel')
        self.assertIsNotNone(thePanel)
        
class TestSecLendPortfolioView(unittest.TestCase):

    def setUp(self):
        myView            = 'SecLendPortfolioView'
        self.app          = iw.LaunchView(myView)
        self.view         = iw.GetView(self.app)
        self.panels       = self.view.Panels()
        
    def tearDown(self):
        self.app.Close('DontSave')
        
    def test_PortfolioPanelsAvailable(self):
        print('Validating SecLendPortfolioWorkbookPanel..')
        thePanel = self.view.Panel('SecLendPortfolioWorkbookPanel')
        self.assertIsNotNone(thePanel)

        print('Validating SecLendReratePanel..')
        thePanel = self.view.Panel('SecLendReratePanel')
        self.assertIsNotNone(thePanel)
