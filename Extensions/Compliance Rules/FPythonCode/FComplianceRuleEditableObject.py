""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/ComplianceRules/./etc/FComplianceRuleEditableObject.py"
"""--------------------------------------------------------------------------
MODULE
    FComplianceRuleEditableObject

    (c) Copyright 2018 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    
-----------------------------------------------------------------------------"""


import acm
from DealPackageDevKit import DealPackageChoiceListSource, Object, Str, Text, ReturnDomainDecorator, CompositeAttributeDefinition, NoOverride
from EditableObjectDevKit import EditableObjectDefinition
from ChoicesExprCommon import listChoicesWithEmpty
from FComplianceRuleAttributeDefinitions import GetRuleInterface
from FThresholdAttributeDefinition import ThresholdDefinition
from FAppliedRuleAttributeDefinition import AppliedRuleAttributeDefinition


class RuleDefinition(CompositeAttributeDefinition):
    
    def OnInit(self, definitionInfos, **kwargs):
        self._definitionInfos = definitionInfos
        
    def Attributes(self):
        attributes = dict()
        for info in self.DefinitionInfos():
            attributes[info.Name()] = GetRuleInterface(info.ClassObject())
        return attributes
    
    def AttributeOverrides(self, overrideAccumulator):
        overrideDict = {}
        for k, v in self.Attributes().iteritems():            
            for attrname in v.AttributeNames():
                attrName = k + '_' + attrname
                overrideDict[attrName] = dict(visible = self.UniqueCallback("@RuleVisibilityController"))
        overrideAccumulator(overrideDict)
        
    def DefinitionInfoIsSelected(self, definitionInfoName):
        if self.Owner().Rule():
            return self.Owner().Rule().DefinitionInfo() == definitionInfoName
        return False
    
    def GetLayout(self):
        layout = 'vbox(;\n'
        for k, v in self.Attributes().iteritems():
            layout += 'hbox[{0};\n'.format(v.PaneDisplayName())
            layout += k + ';\n'
            layout += '];\n'
        layout += ');'
        return self.UniqueLayout(layout)
                                 
    def DefinitionInfos(self):
        return self.GetMethod(self._definitionInfos)()
    
    def RuleVisibilityController(self, sender):
        definitionInfoName = self.GetDefinitionInfoName(sender)
        return NoOverride if self.DefinitionInfoIsSelected(definitionInfoName) else False
        
    @staticmethod
    def GetDefinitionInfoName(sender):
        return sender.split('_')[1]


class Rule(CompositeAttributeDefinition):
        
    def Attributes(self):
        return {'name':        Str(    label='Name',
                                        objMapping="Rule.Name"),
                'description': Text(   objMapping="Rule.Description",
                                        visible=self.UniqueCallback("@IsShowModeDetail"),
                                        onChanged=self.UniqueCallback('@OnDescriptionChanged'),
                                        height=120),
                'category':    Object( label='Rule Category',
                                        objMapping="Rule.RuleCategory",
                                        choiceListSource = self.RuleCategoryChoices()),
               }
        
    def GetLayout(self):
        return self.UniqueLayout(""" 
                                 vbox(;
                                    name;
                                    hbox{Description;
                                        description;
                                    );
                                    category;
                                 );
                                 """)
    
    def RuleCategoryChoices(self, *args):
        return listChoicesWithEmpty("Compliance Rule Category")
    
    def OnDescriptionChanged(self, *args):
        self.Owner().Rule().Touch()
        self.Owner().Rule().Changed()
    

class EditableCompliancRuleDefinition(EditableObjectDefinition):
        
    def OnInit(self):
        EditableObjectDefinition.OnInit(self)
        self._definitionInfos = None
        original = self.Rule().Original()
        if original:
            for rule in original.AppliedRules():
                ruleEdit = rule.StorageNew() if rule.IsInfant() else rule.StorageImage()
                ruleEdit.ComplianceRule = self.Rule()
                self.Rule().AppliedRules().Add(ruleEdit)
            
    rule = Rule()
    ruleDefinition = RuleDefinition(definitionInfos='RegisteredDefinitionInfos')
    definitionInfo = Object(label="Rule Type",
                            objMapping="DefinitionInfo",
                            choiceListSource="@DefinitionInfoChoices")
    thresholds = ThresholdDefinition(rule="Rule")
    appliedRules = AppliedRuleAttributeDefinition(rule="Rule")
    
    def DefinitionInfoChoices(self, *args):
        if self._definitionInfos is None:
            self._definitionInfos = DealPackageChoiceListSource()
            self._definitionInfos.AddAll([info.Name() for info in self.RegisteredDefinitionInfos()])
            self._definitionInfos.AtInsert(0, '')
        return self._definitionInfos
       
    @ReturnDomainDecorator('string')
    def DefinitionInfo(self, value='NoValue'):
        if value != 'NoValue':
            self.Rule().DefinitionInfo(value)
        return self.Rule().DefinitionInfo()
        
    def Rule(self):
        return self.Object()
        
    def DefinitionInfos(self):
        return acm.GetDefaultContext().GetAllExtensions("FRuleDefinitionInfo", "FObject", True, True, 'active rules')
    
    def RegisteredDefinitionInfos(self):
        return [info for info in self.DefinitionInfos() if self.IsRegistered(info)]
        
    @staticmethod
    def IsRegistered(definitionInfo):
        try:
            return bool(definitionInfo.ClassObject())
        except:
            return False
    
    def Originator(self):
        return self.Rule().DecoratedObject().Originator()
    
    def RulesToDelete(self):
        newRules = [r.Originator() for r in self.Object().AppliedRules()]
        rulesToDelete = []
        for rule in self.Object().Originator().AppliedRules():
            if rule not in newRules:
                rulesToDelete.append(rule)
        return rulesToDelete
        
    def OnSave(self, saveConfig):
        return {'commit':self.Object().AppliedRules().AsArray(),
                'delete': self.RulesToDelete()}
        
    def CustomPanes(self):
        return [{'General':"""
                        vbox(;
                            rule;
                            definitionInfo;
                            ruleDefinition;
                            fill;
                            thresholds;
                            );
                        """},
                {'Targets':"""
                        vbox(;
                            appliedRules;
                            );
                        """}]
