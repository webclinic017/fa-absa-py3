""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/reconciliation/./etc/FManualMatchReconciliation.py"
"""--------------------------------------------------------------------------
MODULE
    FManualMatchReconciliation

    (c) Copyright 2018 FRONT CAPITAL SYSTEMS. All rights reserved.

DESCRIPTION

-----------------------------------------------------------------------------"""


import acm
from FReconciliationMenuItem import FReconciliationMenuItem
from ACMPyUtils import Transaction

def ManualMatch(eii):
    return ManualMatchMenuItem(eii)
    
class ManualMatchMenuItem(FReconciliationMenuItem):
    
    def SubjectIsTrade(self, bps):
        return all(bp.Subject().SubjectType() == 'Trade' for bp in bps)
        
    def Invoke(self, eii):
        bps = self.BusinessProcesses()
        caption = "Manual match"
        shell = eii.Parameter('shell')
                
        unidentified = [bp for bp in bps if bp.CurrentStep().State().Name() == 'Unidentified']
        missing = [bp for bp in bps if bp.CurrentStep().State().Name() == 'Missing in document']
        
        relevantBps = unidentified + missing

        if not relevantBps:
            acm.UX().Dialogs().MessageBoxInformation(shell, "No 'Unidentified' nor 'Missing in document' BPs selected.", caption)
            return
        
        notOkReson = self.VerifySpec([bp.Subject() for bp in relevantBps])
        if notOkReson:
            acm.UX().Dialogs().MessageBoxInformation(shell, notOkReson, caption)
            return
        
        spec = self._ReconciliationSpecification(relevantBps[0].Subject(), False)
        quantityKey = self.GetKeyForQuantity(spec)
        
        question = ''
        if quantityKey:
            difference = self.QuantityDifference(unidentified, missing, quantityKey)
            if difference:
                question = '''Quantities of these items do not net.
(sum of the {0} missing - sum of the {1} unidentified = {2}).
Do you still want to match them?'''.format(len(missing), len(unidentified), difference)
            else:
                question = 'The quantities of these items net exactly. Do you want to manually match them?'
        else:
            question = 'No quantity attribute found. Do you still want to manually match them?'
           
        reply = acm.UX().Dialogs().MessageBoxOKCancel(shell, 'Question', question, caption)
        if reply != 'Button1': #answer is not 'ok'
            return    

        self.CloseReconItemGroup(relevantBps)
        

    def VerifySpec(self, reconItems):
        
        firstItem = reconItems[0]
        spec = self._ReconciliationSpecification(firstItem, False)
        
        if not spec:
            return 'No Reconciliation Specification for this BP found!'
        
        if not firstItem.ReconciliationDocument():
            return 'No Reconciliation Document for this BP found!'        
        
        if not firstItem.ReconciliationDocument().ObjectType() == "Trade":
            return 'Only trade reconciliation may be manually matched! Not {0}.'.format(firstItem.ReconciliationDocument().ObjectType())              
        
        if not spec.ReconciliationSpecification():
            return 'You do not have the Reconciliation Specification "{0}" in your context.'.format(spec.Name())
        
        if not all([self._ReconciliationSpecification(r, False).Name() == spec.Name() for r in reconItems]):
            return 'All these Business Processes do not belong to the same Reconciliation Specification'         
        
        if spec.Upload():
            return 'Business Data Uploads cannot be manually matched'      
        
        return None

  

    def CloseReconItemGroup(self, BPs):
        reason = ['Manually matched with reconciliation item(s) {0}'.format([item.Subject().Name() for item in BPs])]
        parameters = {'MatchedReconciliationItems':[item.Subject() for item in BPs]}
        with Transaction():
            for bp in BPs:
                bp.HandleEvent('Closed', parameters, reason)
                bp.Commit()
    
    def Enabled(self):
        return bool(self.BusinessProcesses())
    
       
    
    def QuantityDifference(self, unidentified, missing, quantityKey):
        

        
        missingSum = sum([bp.Subject().Subject().Quantity() for bp in missing])
        
        unidentifiedSum = sum([bp.Subject().ExternalValues().At(quantityKey) for bp in unidentified])
        
        return missingSum - unidentifiedSum
            
        
    def GetKeyForQuantity(self, spec):
        for k, v in spec.ExternalAttributeMap().iteritems():
            if v == "Quantity":
                return k

        