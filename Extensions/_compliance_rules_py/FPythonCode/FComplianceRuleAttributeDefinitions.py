""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/ComplianceRules/./etc/FComplianceRuleAttributeDefinitions.py"
"""--------------------------------------------------------------------------
MODULE
    FComplianceRuleAttributeDefinitions

    (c) Copyright 2018 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    
-----------------------------------------------------------------------------"""


import acm
import re
from DealPackageDevKit import Object, CompositeAttributeDefinition

def CreateAttributeLabel(attrName):
    attrName = attrName.split('_')[-1]
    return re.sub( r"([A-Z])", r" \1", attrName).title()

class ComplianceRuleDefinition(CompositeAttributeDefinition):
    
    def OnInit(self, definition, **kwargs):
        self._definition = definition
            
    def Methods(self):
        for association in self.DefinitionClass().MethodsPerClass():
            if association.Key() is acm.FObject:
                continue
            for method in association.Value():
                if type(method) is acm._pyClass("FAccessGetMethod"):
                    yield method
    
    def DefinitionClass(self):
        return self._definition.Class()
    
    def AttributeNames(self):
        return [str(m.Name()) for m in self.Methods()]
            
    def Attributes(self):
        attributes = dict()
        for method in self.Methods():
            methodName = str(method.Name())
            attributes[methodName] = Object(label=CreateAttributeLabel(methodName), 
                                            objMapping=self.UniqueCallback('SafeDefinition')+'.'+methodName)
        return attributes
        
    def Rule(self):
        return self.Owner().Rule()
    
    def IsApplicable(self, *args):
        definition = self.Rule().Definition()
        if not definition:
            return False
        return definition.Class() is self.DefinitionClass()
        
    def SafeDefinition(self):
        if self.IsApplicable():
            return self.Rule().Definition()
        else:
            return self._definition
    
    def GetRuleLayout(self):
        layout = 'vbox(;\n'
        for m in self.AttributeNames():
            layout += str(m) + ';\n'
        layout += ');'
        return layout

    def GetLayout(self):
        layout = self.GetRuleLayout()
        return self.UniqueLayout(layout)
    
    def PaneDisplayName(self):
        return 'Rule Definition'

def GetRuleInterface(ruleDefinitionClass):
    ruleDefinition = acm.Create(ruleDefinitionClass)
    interface = ruleDefinitionClass.Interface()    
    if interface:
        try:
            module, className = interface.split('.')
            func = getattr(__import__(module), className)
            return func().CreateCompositeAttributes(ruleDefinition)
        except Exception:
            pass
    return ComplianceRuleDefinition(ruleDefinition)
