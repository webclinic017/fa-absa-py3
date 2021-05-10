""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/ComplianceRuleDefinitionsStandard/./etc/FExposureRuleAttributeDefinitions.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FExposureRuleAttributeDefinitions

    (c) Copyright 2018 FIS FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""
import acm
from FComplianceRuleAttributeDefinitions import ComplianceRuleDefinition
from DealPackageDevKit import Action, UXDialogsWrapper, DealPackageChoiceListSource, Object
import DealPackageBase
from FAdvancedRuleFilter import AdvancedFilter

class ExposureRuleDefinition(ComplianceRuleDefinition):
    
    EXPOSURE = acm.FRuleDefinitionInfo['Exposure']

    def OnInit(self, definition):
        ComplianceRuleDefinition.OnInit(self, definition)
        self._columnChoices = DealPackageChoiceListSource()
        self._grouperChoices = DealPackageChoiceListSource()
        self._selectedQuery = None
    
    def OnOpen(self):
        if not self.Owner().Object().DecoratedObject().Originator().IsInfant():
            rule = self.Owner().Rule()
            if rule and rule.Definition():
                definitionInfo = acm.FRuleDefinitionInfo[rule.DefinitionInfo()]
                if definitionInfo == self.EXPOSURE or definitionInfo in self.EXPOSURE.Subclasses():
                    self.UpdateFields()
    
    def Attributes(self):
        self.GetMethod('RegisterCallbackOnAttributeChanged')(self.UpdateQueryString)
        attributes = ComplianceRuleDefinition.Attributes(self)
        attributes['selectColumn'] =            Action(label='Select', 
                                                   visible=self.UniqueCallback("@SelectColumnVisible"),
                                                   dialog=self.UniqueCallback("@SelectColumnDialog"),
                                                   action=self.UniqueCallback("@SetColumn"),)
        attributes['selectRelativeToColumn'] =  Action(label='Select', 
                                                   visible=self.UniqueCallback("@SelectRelativeToColumnVisible"),
                                                   dialog=self.UniqueCallback("@SelectColumnDialog"),
                                                   action=self.UniqueCallback("@SetRelativeToColumn"),)
        attributes['selectForEachGrouper'] =    Action(label='Select', 
                                                   visible=self.UniqueCallback("@SelectForEachGrouperVisible"),
                                                   dialog=self.UniqueCallback("@SelectGrouperDialog"),
                                                   action=self.UniqueCallback("@SetForEachGrouper"),)
        attributes['selectQuery'] =             Action(label='Select', 
                                                   visible=self.UniqueCallback("@SelectQueryVisible"),
                                                   dialog=self.UniqueCallback("@ShowSelectQueryFolderDialog"),
                                                   action=self.UniqueCallback("@SelectQuery"),)
        attributes['addQuery'] =                Action(label='Add',
                                                    dialog=self.UniqueCallback("@ShowSelectQueryFolderDialog"),
                                                    action=self.UniqueCallback("@AddQuery"),
                                                    visible=self.UniqueCallback("@CompoundQueryVisible"))
        attributes['removeQuery'] =             Action(label='Remove',
                                                    action=self.UniqueCallback("@RemoveQuery"),
                                                    visible=self.UniqueCallback("@CompoundQueryVisible"))
        attributes['queryString'] =             Object(label='in trade set',
                                                    visible=self.UniqueCallback("@QueryStringVisible"))
        attributes['advancedFilterChoices'] =   Object(label='Advanced filters',
                                                    choiceListSource=self.UniqueCallback('@AdvancedFilterChoices'),
                                                    visible=self.UniqueCallback("@AdvancedFilterChoicesVisible"))
        return attributes
       
    def AttributeOverrides(self, overrideAccumulator):
        overrideDict = {
                'Column':            dict(label='Calculate',
                                        choiceListSource=self.UniqueCallback('@ColumnChoices')),
                'FilterQuery':       dict(label='in trade set',
                                        elementDomain='FStoredASQLQuery',
                                        onSelectionChanged=self.UniqueCallback('@SetSelectedQuery'),
                                        columns=self.UniqueCallback('@ListColumns'),
                                        visible=self.UniqueCallback("@FilterQueryVisible")),
                'ForEach':           dict(label='for each',
                                        choiceListSource=self.UniqueCallback('@ForEachChoices')),
                'RelativeTo':        dict(label='as percentage of'),
                'RelativeToColumn':  dict(label='total',
                                        visible=self.UniqueCallback("@RelativeToColumnVisible"),
                                        choiceListSource=self.UniqueCallback('@ColumnChoices')),
                'PythonFilterMethodName':       dict(label='Python filter',
                                                    choiceListSource=self.UniqueCallback('@PythonFilterChoices'),
                                                    visible=self.UniqueCallback("@PythonFilterChoicesVisible")),
                'CompoundQueryLogicalOperator': dict(label='Operator',
                                                     visible=self.UniqueCallback("@CompoundQueryVisible"))
                            }
        overrideAccumulator(overrideDict)

    def GetRuleLayout(self):
        return """vbox(;
                    hbox(;
                        Column;
                        selectColumn;
                        );
                    hbox(;
                        ForEach;
                        selectForEachGrouper;
                        );
                    hbox(;
                        queryString;
                        selectQuery;
                        );
                    advancedFilterChoices;
                    PythonFilterMethodName;
                    FilterQuery;
                    hbox(;
                        addQuery;
                        removeQuery;
                        CompoundQueryLogicalOperator;
                        );
                    RelativeTo;
                    hbox(;
                        RelativeToColumn;
                        selectRelativeToColumn;
                        );
                );"""
    
    
    # ----------------------- Actions -----------------------
    
    def SelectColumnDialog(self, *args):
        return UXDialogsWrapper(acm.UX().Dialogs().SelectColumns, acm.FColumnCreators(), acm.FPortfolioSheet, '', '', None, True)
        
    def SelectGrouperDialog(self, *args):
        return UXDialogsWrapper(acm.UX().Dialogs().SelectGrouper, acm.FInstrumentAndTradesGrouperSubject, False)
    
    def SetForEachGrouper(self, attrName, grouper):
        if grouper:
            self.ForEach = grouper.Name()
            self.UpdateGrouperChoices()
            
    def SetColumn(self, attrName, columnCreators):
        columnId = self._SelectedColumnId(columnCreators)
        if columnId:
            self.Column = columnId
            self.UpdateColumnChoices()
    
    def SetRelativeToColumn(self, attrName, columnCreators):
        columnId = self._SelectedColumnId(columnCreators)
        if columnId:
            self.RelativeToColumn = columnId
            self.UpdateColumnChoices()
    
    @staticmethod
    def _SelectedColumnId(columnCreators):
        try:
            return columnCreators.At(0).ColumnId()
        except RuntimeError: #No column selected
            return None
            
    def SetSelectedQuery(self, attributeName, selectedObj):
        self._selectedQuery = selectedObj
    
    @staticmethod
    def _QueryClass():
        return acm.FTrade
    
    def _FirstQuery(self):
        try:
            return self.FilterQuery.At(0)
        except (AttributeError, RuntimeError):
            return None
    
    def ShowSelectQueryFolderDialog(self, *args):
        return UXDialogsWrapper(acm.UX().Dialogs().SelectStoredASQLQuery, self._QueryClass(), self._FirstQuery())
    
    def SelectQuery(self, attrName, query):
        if query:
            if self.FilterQuery is None:
                self.FilterQuery = acm.FArray()
            self.FilterQuery.Clear()
            self.FilterQuery.Add(query)
            self._TouchRule()
    
    def AddQuery(self, attrName, query):
        if query:
            if self.FilterQuery is None:
                self.FilterQuery = acm.FArray()
            self.FilterQuery.Add(query)
            self._TouchRule()

    def RemoveQuery(self, *args):
        if self._selectedQuery:
            self.FilterQuery.Remove(self._selectedQuery)
            self._selectedQuery = None
            self._TouchRule()
            
    def _TouchRule(self):
        self.Owner().Rule().Touch()
        self.Owner().Rule().Changed()
        self.UpdateQueryString()
    
    def ListColumns(self, *args):
        return [{'methodChain': 'Name', 'label': 'Name'}]
        
    
    # ----------------------- Update choices -----------------------
    
    def UpdateColumnChoices(self):
        columns = {str(column.Name()) for column in self._DefaultColumnChoices()}
        if self.SafeDefinition().Column():
            columns.add(self.SafeDefinition().Column())
        if self.SafeDefinition().RelativeToColumn():
            columns.add(self.SafeDefinition().RelativeToColumn())
        self._columnChoices.Clear()
        self._columnChoices.AddAll(list(columns))

    def UpdateGrouperChoices(self, *args):
        groupers = {str(grouper.Name()) for grouper in self._ForEachGroupers()}
        groupers.add('Instrument')
        groupers.add('')
        if self.SafeDefinition().ForEach():
            groupers.add(self.SafeDefinition().ForEach())
        self._grouperChoices.Clear()
        self._grouperChoices.AddAll(list(groupers))
        
    
    # ----------------------- Populate choices -----------------------
    
    def ForEachChoices(self, *args):
        if self._grouperChoices.IsEmpty():
            self.UpdateGrouperChoices()
        return self._grouperChoices
    
    def ColumnChoices(self, *args):
        if self._columnChoices.IsEmpty():
            self.UpdateColumnChoices()
        return self._columnChoices
    
    def AdvancedFilterChoices(self, *args):
        return ['', 'Compound query', 'Python filter']
        
    def PythonFilterChoices(self, *args):
        methods = AdvancedFilter.GetFilterMethods()
        methodNames = ['{0}.{1}'.format(m.__module__, m.__name__) for m in methods]
        methodNames.append('')
        return methodNames
    
    @classmethod
    def _DefaultColumnChoices(cls):
        return cls._PublishedExtensions(acm.FColumnDefinition, 'FTradingSheet', 'exposure columns')
    
    @classmethod
    def _ForEachGroupers(cls):
        return cls._PublishedExtensions(acm.FExtensionValue, 'FInstrumentAndTradesGrouperSubject', 'for each groupers')
        
    @staticmethod
    def _PublishedExtensions(type_, className, item):
        return acm.GetDefaultContext().GetAllExtensions(type_, 
                                                        className,
                                                        True, True,
                                                        'active rules',
                                                        item,
                                                        False)
    
    def UpdateQueryString(self, *args):
        res = [query.Name() for query in self.FilterQuery or []]
        if self.PythonFilterMethodName:
            res.append(self.PythonFilterMethodName.split('.')[1])
        operator = str(self.CompoundQueryLogicalOperator)
        text = ' {0} '.format(operator).join(res)
        self.queryString = text
    
    def UpdateFields(self, *args):
        self.UpdateQueryString()
        if self.queryString and self.queryString.find(' AND '):
            if self.PythonFilterMethodName:
                self.advancedFilterChoices = 'Python filter'
            else:
                self.advancedFilterChoices = 'Compound query'
                
    
    # ----------------------- Visibility methods -----------------------
    
    def RelativeToColumnVisible(self, *args):
        return self.RelativeTo

    def SelectColumnVisible(self, *args):
        return self.IsShowModeDetail() and self.IsApplicable()
   
    def SelectRelativeToColumnVisible(self, *args):
        return self.IsShowModeDetail() and self.IsApplicable() and self.RelativeToColumnVisible()
        
    def SelectForEachGrouperVisible(self, *args):
        return self.IsShowModeDetail() and self.IsApplicable()
    
    def QueryStringVisible(self, *args):
        return self.IsApplicable()
    
    def FilterQueryVisible(self, *args):
        return self.IsShowModeDetail() and self.advancedFilterChoices == 'Compound query'
    
    def SelectQueryVisible(self, *args):
        return self.IsApplicable()
    
    def CompoundQueryVisible(self, *args):
        return self.IsApplicable() and self.IsShowModeDetail() and self.advancedFilterChoices == 'Compound query'
    
    def AdvancedFilterVisible(self, *args):
        return self.IsApplicable() and self.IsShowModeDetail()
        
    def AdvancedFilterChoicesVisible(self, *args):
        return self.IsApplicable() and self.IsShowModeDetail()
        
    def PythonFilterChoicesVisible(self, *args):
        return self.IsApplicable() and self.IsShowModeDetail() and self.advancedFilterChoices == 'Python filter'
