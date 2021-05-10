""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/BankDebtWSO/etc/FWSOCashflowFactory.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FWSOCashflowFactory -

    (c) Copyright 2015 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION


-------------------------------------------------------------------------------------------------------"""


class CashflowFactory(object):
    ''' Creates a single cashflow for an FRN, based on an IPF-dict.
    '''
    
    def __init__(self, frn, ipfDict):
        self.frn = frn
        self.ipfDict = ipfDict
        self.leg = frn.FirstFloatLeg()
        
    def _IpfAttribute(self, key):
        return self.ipfDict.get(key)
    
    def _Spread(self):
        return 100*self._IpfAttribute('Spread')
    
    def _CreateCashflowFromIpfDict(self):
        cashflow = self.leg.CreateCashFlow()
        cashflow.CashFlowType(self._IpfAttribute('CashFlowType'))
        cashflow.FloatRateFactor(1.0)
        cashflow.StartDate(self._IpfAttribute('StartDate'))
        cashflow.EndDate(self._IpfAttribute('EndDate'))
        cashflow.PayDate(self._IpfAttribute('PayDate'))
        cashflow.NominalFactor(self._IpfAttribute('NominalFactor'))
        cashflow.Spread(self._Spread())
        return cashflow
    
    def Create(self):
        return self._CreateCashflowFromIpfDict()
