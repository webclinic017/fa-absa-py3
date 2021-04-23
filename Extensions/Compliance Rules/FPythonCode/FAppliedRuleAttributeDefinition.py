""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/ComplianceRules/./etc/FAppliedRuleAttributeDefinition.py"
"""--------------------------------------------------------------------------
MODULE
    FAppliedRuleAttributeDefinition

    (c) Copyright 2018 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    
-----------------------------------------------------------------------------"""

import acm
from DealPackageDevKit import (CompositeAttributeDefinition, 
                               Action, 
                               Object, 
                               UXDialogsWrapper, 
                               ContextMenu, 
                               ContextMenuCommand, 
                               ReturnDomainDecorator)


class AppliedRuleAttributeDefinition(CompositeAttributeDefinition):
    
    def OnInit(self, rule):
        self._rule = rule
        self._appliedRules = None
    
    def Attributes(self):
        return {
                'appliedRuleslist': Object( label='',
                                                objMapping='Rule.AppliedRules',
                                                elementDomain='FAppliedRule',
                                                columns=self.UniqueCallback('@ListColumns'),
                                                onSelectionChanged=self.UniqueCallback('@SetSelectedAppliedRule'),
                                                onRightClick=ContextMenu(self.UniqueCallback('@EnableAppliedRuleCB'),
                                                                         self.UniqueCallback('@RemoveAppliedRuleCB'),
                                                                         )),
                'dialogButton': Action( label='Apply to...',
                                                action=self.UniqueCallback("@ApplySelectedItems"),
                                                dialog=self.UniqueCallback("@ShowSelectQueryFolderDialog"),
                                                enabled=self.UniqueCallback('@HasPersistedComplianceRule')),
                'removeAppliedRule': Action( action=self.UniqueCallback('@DoRemoveAppliedRule'),
                                                enabled=self.UniqueCallback('@HasSelectedAppliedRule')),
                'enableAppliedRule': Action( action=self.UniqueCallback('@EnableAppliedRule'),
                                                enabled=self.UniqueCallback('@HasSelectedAppliedRule')),
                'selectedAppliedRule': Object( domain='FAppliedRule'),
            }
    
    def Rule(self):
        return self.GetMethod(self._rule)()
        
    def Original(self):
        return self.Rule().DecoratedObject().Originator()
        
    # ************************* Attribute Callbacks *************************
    def ApplySelectedItems(self, *args):
        items = args[1]
        if items != None:
            for item in items:
                if item not in self.GetTargets():
                    self.CreateAppliedRule(item)
    
    def HasPersistedComplianceRule(self, *args):
        return False if self.Rule().DecoratedObject().Originator().IsInfant() else True
    
    def ListColumns(self, *args):
        return [{'methodChain': 'Target', 'label': 'Target'},
                {'methodChain': 'Target.RecordType', 'label': 'Target type'},
                {'methodChain': 'ActiveAsString', 'label': 'Active/Inactive'}]
        
    def RemoveAppliedRuleCB(self, attrName):
        return ContextMenuCommand(commandPath='Applied Rule/Remove', 
                                  invoke=self.UniqueCallback('@DoRemoveAppliedRule'),
                                  enabled=self.UniqueCallback('@HasSelectedAppliedRule'),
                                  default=False)
    
    def EnableAppliedRuleCB(self, attrName):
        return ContextMenuCommand(commandPath='Applied Rule/' + self.EnableAppliedRuleLabel(), 
                                  invoke=self.UniqueCallback('@EnableAppliedRule'),
                                  enabled=self.UniqueCallback('@HasSelectedAppliedRule'),
                                  default=False)
        
    def DoRemoveAppliedRule(self, *args):
        if self.selectedAppliedRule != None:
            self.Rule().AppliedRules().Remove(self.selectedAppliedRule)
            self.selectedAppliedRule.Unsimulate()
    
    def EnableAppliedRuleLabel(self, *args):
        return 'Activate' if self.selectedAppliedRule.Inactive() else 'Inactivate'        
        
    def EnableAppliedRule(self, *args):     
        if self.selectedAppliedRule.Inactive():
            self.selectedAppliedRule.Inactive(False)
        else:
            self.selectedAppliedRule.Inactive(True)
        self.Rule().Changed()
                
    def SetSelectedAppliedRule(self, attrName, selectedObj, *rest):
        self.selectedAppliedRule = selectedObj
    
    def HasSelectedAppliedRule(self, *args):
        return self.selectedAppliedRule != None
    
    # ************************* Convenience Methods  *************************
    def CreateAppliedRule(self, target):
        appliedRule = acm.FAppliedRule()
        appliedRule.ComplianceRule(self.Rule())
        appliedRule.Target(target)
        appliedRule.RegisterInStorage()
        self.Rule().AppliedRules().Add(appliedRule)
        return appliedRule
    
    def ShowSelectQueryFolderDialog(self, *args):
        return UXDialogsWrapper(acm.UX().Dialogs().SelectObjectsInsertItemsWithProviders, self.GetInsertItems(), True)
    
    def GetTargets(self):
        return [appliedRule.Target() for appliedRule in self.Rule().AppliedRules()]
        
    def GetInsertItems(self):
        arr = acm.FArray()
        for clsObject in self.Rule().Definition().Class().ApplicableTo():
            arr.Add(clsObject)
        return arr
    
    def GetLayout(self):
        return self.UniqueLayout("""
                    vbox(;
                        appliedRuleslist;
                        dialogButton;
                    );
               """)
               

def ActiveAsString(appliedRule):
    return 'Inactive' if appliedRule.Inactive() else 'Active'
