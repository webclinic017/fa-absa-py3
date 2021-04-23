""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/ExclusionList/etc/FExclusionRuleAttributeDefinitions.py"

"""-------------------------------------------------------------------------------------------------------
MODULE
    FExclusionRuleAttributeDefinitions

    (c) Copyright 2018 FIS FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""
import acm
from FComplianceRuleAttributeDefinitions import ComplianceRuleDefinition
from DealPackageDevKit import Action, UXDialogsWrapper, DealPackageChoiceListSource

class ExclusionRuleDefinition(ComplianceRuleDefinition):

    def OnInit(self, definition):
        ComplianceRuleDefinition.OnInit(self, definition)
        self._aliasTypeChoices = DealPackageChoiceListSource()
        self._identifierListChoices = DealPackageChoiceListSource()
        self._listTypeChoices = DealPackageChoiceListSource()
        self._queryChoices = DealPackageChoiceListSource()
        self._pageGroupChoices = DealPackageChoiceListSource()
    
    def Attributes(self):
        attributes = ComplianceRuleDefinition.Attributes(self)
        attributes['selectQuery'] =     Action(label='Select', 
                                               visible=self.UniqueCallback("@QueryVisible"),
                                               dialog=self.UniqueCallback("@ShowSelectQueryFolderDialog"),
                                               action=self.UniqueCallback("@SetQueryFolder"))
        
        return attributes
       
    def AttributeOverrides(self, overrideAccumulator):
        overrideDict = {
                'AliasType':            dict(visible=self.UniqueCallback("@AliasTypeVisible"),
                                             choiceListSource = self.UniqueCallback('@AliasTypeChoices')),
                            
                'ExclusionTarget':      dict(onChanged=self.UniqueCallback("@UpdateChoices|ClearParameters")),
                                            
                'IdentifierList':       dict(visible=self.UniqueCallback("@IdentifierListVisible"),
                                             choiceListSource = self.UniqueCallback('@IdentifierListChoices')),
                                            
                'BlacklistOrWhitelist': dict(label='Blacklist/Whitelist'),
                
                'ListType':             dict(visible=self.UniqueCallback("@ListTypeVisible"),
                                            onChanged=self.UniqueCallback("@ClearParameters"),
                                            choiceListSource=self.UniqueCallback('@ListTypeChoices')),
                                              
                'PageGroup':            dict(visible=self.UniqueCallback("@PageGroupVisible"),
                                             choiceListSource = self.UniqueCallback('@PageGroupChoices')),

                'PartyGroup':           dict(visible=self.UniqueCallback('@PartyGroupVisible')),
                
                'FilterQuery':          dict(visible=self.UniqueCallback("@QueryVisible"),
                                             choiceListSource = self.UniqueCallback('@QueryChoices')),
                
                'IgnoreFXSpot':         dict(label='Ignore spot dated',
                                            visible=self.UniqueCallback("@IgnoreFXSpotVisible")),
                            }
        overrideAccumulator(overrideDict)
    
    #Actions
    def SetQueryFolder(self, attrName, query):
        if query:
            if query.User() == None:
                self.UpdateQueryChoices()
                self.FilterQuery = query
            else:
                self.FilterQuery = None
                print('Query must be shared')
                
    def ShowSelectQueryFolderDialog(self, *args):
        if self.IsInstrumentList():
            return UXDialogsWrapper(acm.UX().Dialogs().SelectStoredASQLQuery, acm.FInstrument, self.FilterQuery)
        elif self.IsFxList():
            return UXDialogsWrapper(acm.UX().Dialogs().SelectStoredASQLQuery, acm.FCurrencyPair, self.FilterQuery)
            
    
    #VisibilityCallbacks
    
    def ListTypeVisible(self, *args):
        return bool(self.ExclusionTarget) and self.ExclusionTarget not in ('FX')

    def AliasTypeVisible(self, *args):
        return self.ListType in ['Alias']
    
    def IdentifierListVisible(self, *args):
        return self.ListType in ['Alias', 'Identifiers']

    def PageGroupVisible(self, *args):
        return self.ListType in ['PageGroup']
        
    def PartyGroupVisible(self, *args):
        return self.ListType in ['PartyGroup']
    
    def QueryVisible(self, *args):
        return True if self.ExclusionTarget in ('FX') else self.ListType in ['Query']
    
    def IgnoreFXSpotVisible(self, *args):
        return bool(self.ExclusionTarget) and self.ExclusionTarget  in ('FX')
        
    def ClearParameters(self, *args):
        self.FilterQuery = None
        self.PartyGroup = None
        self.PageGroup = None
        self.IdentifierList = None
        self.AliasType = None
        
    #Update choices

    def UpdateChoices(self,*args):
        self.UpdateListTypeChoices()
        self.UpdateAliasTypeChoice()
        self.UpdateQueryChoices()
        self.UpdateIdentifierListChoices()
        self.UpdatePageGroupChoices()
  
    def UpdateListTypeChoices(self, *args):
        self._listTypeChoices.Clear()
        if self.IsInstrumentList():
            self._listTypeChoices.AddAll(['Query', 'Identifiers', 'Alias', 'PageGroup'])
        elif self.IsIssuerList():
            self._listTypeChoices.AddAll(['Identifiers', 'Alias', 'PartyGroup'])
            
    def UpdateAliasTypeChoice(self, *args):
        self._aliasTypeChoices.Clear()
        if self.IsInstrumentList():
            self._aliasTypeChoices.AddAll(acm.FInstrAliasType.Select(None))
        elif self.IsIssuerList():
            self._aliasTypeChoices.AddAll(acm.FPartyAliasType.Select(None))
               
    def UpdateQueryChoices(self, *args):
        self._queryChoices.Clear()
        if self.IsInstrumentList():
            self._queryChoices.AddAll(acm.FStoredASQLQuery.Select('subType = "FInstrument" and user = 0'))
        elif self.IsFxList():
            self._queryChoices.AddAll(acm.FStoredASQLQuery.Select('subType = "FCurrencyPair" and user = 0'))
 
    def UpdateIdentifierListChoices(self, *args):
        self._identifierListChoices.Clear()
        if self.IsInstrumentList():
            for extension in acm.GetDefaultContext().GetAllExtensions("FExtensionValue", "FObject", True, True, "exclusion list", "instrument", False):
                self._identifierListChoices.Add(extension.Name())
 
        elif self.IsIssuerList():
            for extension in acm.GetDefaultContext().GetAllExtensions("FExtensionValue", "FObject", True, True, "exclusion list", "issuer", False):
                self._identifierListChoices.Add(extension.Name())
 
    def UpdatePageGroupChoices(self, *args):
        self._pageGroupChoices.Clear()
        master = acm.FPageGroup['ExclusionList']
        if master:
            return self._pageGroupChoices.AddAll(acm.GetFunction('exclusionListPageGroups', 1)(master))
            
    
    #Utils
    def IsInstrumentList(self):
        return self.ExclusionTarget == 'Instrument'
 
    def IsIssuerList(self):
        return self.ExclusionTarget == 'Issuer'
 
    def IsFxList(self):
        return self.ExclusionTarget == 'FX'
 
    #Choices:
 
    def AliasTypeChoices(self, *args):
        if self._aliasTypeChoices.IsEmpty():
            self.UpdateAliasTypeChoice()
        return self._aliasTypeChoices
    
    def IdentifierListChoices(self, *args):
        if self._identifierListChoices.IsEmpty():
            self.UpdateIdentifierListChoices()
        return self._identifierListChoices
    
    def ListTypeChoices(self, *args):
        if self._listTypeChoices.IsEmpty():
            self.UpdateListTypeChoices()
        return self._listTypeChoices
    
    def QueryChoices(self, *args):
        if self._queryChoices.IsEmpty():
            self.UpdateQueryChoices()
        return self._queryChoices

    def PageGroupChoices(self, *args):
        if self._pageGroupChoices.IsEmpty():
            self.UpdatePageGroupChoices()
        return self._pageGroupChoices
    
    def GetRuleLayout(self):
        return """vbox(;
                    hbox(;
                            ExclusionTarget;
                            BlacklistOrWhitelist;
                        );    
                    ListType;  
                    AliasType;                              
                    IdentifierList;        
                    PageGroup;                   
                    PartyGroup;
                    hbox(;
                        FilterQuery;
                        selectQuery;
                        );
                    hbox(;
                        IgnoreFXSpot;
                    );
                );"""
