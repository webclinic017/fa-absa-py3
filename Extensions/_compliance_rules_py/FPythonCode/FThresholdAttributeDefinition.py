""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/ComplianceRules/./etc/FThresholdAttributeDefinition.py"
"""--------------------------------------------------------------------------
MODULE
    FThresholdAttributeDefinition

    (c) Copyright 2018 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    
-----------------------------------------------------------------------------"""

import acm
from DealPackageDevKit import CompositeAttributeDefinition, Action, Object, AttributeDialog, Float, Str, DealPackageUserException
from ChoicesExprCommon import listChoicesWithEmpty

class ThresholdDefinition(CompositeAttributeDefinition):
    
    def OnInit(self, rule, **kwargs):
        self._rule = rule
        self._extraArguments = kwargs
    
    def Attributes(self):
        return {'thresholdValue'    : Float(    label='Threshold Value'),
                'type'              : Str(      label='Threshold Type',
                                                domain='FChoiceList',
                                                transform=self.UniqueCallback('@TransformToDomain'),
                                                choiceListSource = self.ThresholdTypeChoices()),
                'comparisonType'    : Str(      label='Comparison Type',
                                                domain='enum(ComparisonType)',
                                                defaultValue='Greater'),
                'description'       : Str(      label='Description'),
                'thresholdList'     : Object(   label='',
                                                objMapping='Rule.Thresholds',
                                                domain="FPersistentSet",
                                                elementDomain='FThreshold',
                                                columns=self.UniqueCallback('@ListColumns'),
                                                onSelectionChanged=self.UniqueCallback('@SetSelectedThreshold')),
                'add'               : Action(   label='Add',
                                                action=self.UniqueCallback("@AddThreshold")),
                'remove'            : Action(   label='Remove',
                                                action=self.UniqueCallback("@RemoveThreshold")),
                'update'            : Action(   label='Update',
                                                action=self.UniqueCallback("@UpdateThreshold")),
                'selectedThreshold' : Object(   domain='FThreshold',
                                                transform=self.UniqueCallback('@TransformToDomain'),
                                                onChanged=self.UniqueCallback('@SetFieldsFromSelectedThreshold')),
                'dialogButton'      : Action(   label=self.UniqueCallback('@ButtonLabel'),
                                                dialog=AttributeDialog(label='Thresholds',  
                                                                       customPanes=self.UniqueCallback('@GetThresholdPanes')),
                                                                       **self._extraArguments)
            }
        
    
    def Rule(self):
        return self.GetMethod(self._rule)()
        
    # ************************* Attribute Callbacks *************************
    def SetSelectedThreshold(self, attributeName, selectedObj):
        self.selectedThreshold = selectedObj
        
    def ButtonLabel(self, *args):        
        return 'Thresholds...*' if self.thresholdList else 'Thresholds...'
    
    def TransformToDomain(self, attrName, value):
        if value and isinstance(value, str):
            domain = self.GetMethod("GetAttributeMetaData")(attrName, "domain")()
            try:
                value = domain[value]
            except:
                pass
        return value
    
    def ThresholdTypeChoices(self, *args):
        return listChoicesWithEmpty("Threshold Type")
    
    def AddThreshold(self, *args):
        self._CreateOrUpdateThreshold()
    
    def RemoveThreshold(self, *args):
        if self.HasSelectedThreshold():
            selected = self.selectedThreshold
            self.selectedThreshold = None
            selected.Unsimulate()
            
    def UpdateThreshold(self, *args):
        if self.HasSelectedThreshold():
            self._CreateOrUpdateThreshold(self.selectedThreshold)
        
    def SetFieldsFromSelectedThreshold(self, *args):
        selectedThreshold = self.selectedThreshold
        if selectedThreshold:
            self.thresholdValue = selectedThreshold.ThresholdValue()
            self.type = selectedThreshold.Type()
            self.comparisonType = selectedThreshold.ComparisonType()
            self.description = selectedThreshold.Description()
            self.type = selectedThreshold.Type()
        
    def ListColumns(self, *args):
        return [{'methodChain': 'ThresholdValue', 'label': 'Threshold Value'},
                {'methodChain': 'ComparisonType', 'label': 'Comparison Type'},
                {'methodChain': 'Type', 'label': 'Type'},
                {'methodChain': 'Description', 'label': 'Description'}]
   
    
    # ************************* Convenience Methods  *************************
    def SelectedThreshold(self):
        return self.selectedThreshold

    def _CreateOrUpdateThreshold(self, threshold=None):
        if not self.type:
            raise DealPackageUserException('Type required')
        if not self.comparisonType:
            raise DealPackageUserException('Comparison type required')
        if not threshold:
            threshold = acm.FThreshold()
            threshold.ComplianceRule(self.Rule())
            threshold.RegisterInStorage()
        threshold.ThresholdValue(self.thresholdValue)
        threshold.Type(self.type)
        threshold.ComparisonType(self.comparisonType)
        threshold.Description(self.description)
        return threshold
    
    def HasSelectedThreshold(self, *args):
        return True if self.selectedThreshold else False
    
    def GetThresholdLayout(self):
        return self.UniqueLayout("""
                    hbox[;
                        thresholdList;
                        vbox(;
                            add;
                            update;
                            remove;
                        );
                    );
                    hbox(;
                        hbox(;
                            thresholdValue;
                            comparisonType;
                            description;
                            type;
                        );
                    );
               """)
        
    def GetThresholdPanes(self, *args):
        return [{'Create': self.GetThresholdLayout()}]
        
    def GetLayout(self):
        return self.UniqueLayout("""
                    hbox(;
                    fill;
                    dialogButton;
                    );
               """)
        
        