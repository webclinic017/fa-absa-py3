""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/AMUtils/./etc/FGrouperUtils.py"
from __future__ import print_function
"""--------------------------------------------------------------------------
MODULE
    FGrouperUtils

    (c) Copyright 2016 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    Functionality for handling groupers

-----------------------------------------------------------------------------"""
import acm


GROUPER_SUBJECTS = {
    # Default subject is acm.FInstrumentAndTradesGrouperSubject; map others
    acm.FLimitSplitGrouper: acm.FLimitGrouperSubject,
    }

def GetGrouper(name, sheetClass):
    subjectClass = GetGrouperSubjectClassFromSheetClass(sheetClass)
    if subjectClass:
        if isinstance(subjectClass, basestring):
            subjectClass = acm.FClass[subjectClass]
        return (GetGrouperFromStoredGroupers(name, subjectClass) or
                acm.Risk.GetGrouperFromName(name, subjectClass) or
                GetGrouperFromMethodName(name, subjectClass))
    else:
        return None

def GetGrouperSubjectClassFromSheetClass(sheetClass):
    subjectClass = None
    try:
        subjectClass = acm.Sheet.GetSheetDefinition(sheetClass).GrouperSubjectClass()
    except AttributeError as e:
        print(("Failed to get GrouperSubjectClass from sheet {0} of type {1}: {2}".format(sheetClass, type(sheetClass), e)))
    return subjectClass

def GetGrouperFromStoredGroupers(name, subjectClass):
    grouper = None
    storedName = str(name)[:31]
    storedGroupers = acm.FStoredPortfolioGrouper.Select('')
    for sg in storedGroupers.SortByProperty('CreateTime'):
        if (sg.Name() == storedName and
            GetGrouperSubjectClass(sg.Grouper()) == subjectClass):
            grouper = sg.Grouper()
            if sg.User() == acm.User():
                break
    return grouper

def GetGrouperFromMethodName(name, subjectClass):
    try:
        if IsValidMethodChain(name, subjectClass):
            grouper = acm.FAttributeGrouper()
            grouper.SubjectClass(subjectClass)                
            grouper.Method(name)
            grouper.Label(name)
            return grouper
    except RuntimeError:
        pass

def IsValidMethodChain(methodChain, subjectClass):
    try:
        acmClass = subjectClass
        methodChain = methodChain.split('.')
        
        for m in methodChain:
            method = acmClass.GetMethod(m, 0)
            if method:
                acmClass = method.Domain()
            else:
                raise ValueError
    except Exception:
        return False
    return True        

def GetGrouperSubjectClass(grouper):
    subjectClass = None
    if grouper.IsKindOf(acm.FChainedGrouper):
        for g in grouper.Groupers():
            if hasattr(g, 'SubjectClass'):
                subjectClass = g.SubjectClass()
            else:
                subjectClass = GROUPER_SUBJECTS.get(g, None)
            if subjectClass:
                break
    if not subjectClass:
        if hasattr(grouper, 'SubjectClass'):
            subjectClass = grouper.SubjectClass()
    return subjectClass

def GetGrouperName(grouper):
    attributes = ['Label', 'Method', 'DisplayName']
    labels = [getattr(grouper, attr)() for attr in attributes if hasattr(grouper, attr)]
    labels = [str(l) for l in labels if l]
    return labels[0] if labels else ''
    
def GroupingValueReference(groupingNode):
    groupingValueRef = None
    if groupingNode.IsKindOf(acm.FInstrument) or groupingNode.IsKindOf(acm.FInstrumentPair):
        groupingValueRef = groupingNode
    elif groupingNode.IsKindOf(acm.FPortfolio):
        groupingValueRef = GroupingValueRefForPortfolio(groupingNode)
    return groupingValueRef
        
def GroupingValueRefForPortfolio(groupingNode):
    prtfGroupingValueRef = None
    currencyPair = groupingNode.CurrencyPair()
    if currencyPair:
        prtfGroupingValueRef = currencyPair
    else:
        portfCurrency = groupingNode.Currency()
        if portfCurrency:
            prtfGroupingValueRef = portfCurrency
        else:
            prtfGroupingValueRef = acm.ObjectServer().UsedValuationParameters().AccountingCurrency()
    return prtfGroupingValueRef

def SpotGroupingReferenceFallback(multiInsAndTradesObj):
    return GroupingValueRefForPortfolio(multiInsAndTradesObj.Portfolio())
    
def DepthFirstGroupingStructure(multiInsAndTradesObj):
    return multiInsAndTradesObj.Grouping().GroupingValues()

def SpotGroupingReference(multiInsAndTradesObj):
    groupingNodeStructure = DepthFirstGroupingStructure(multiInsAndTradesObj)
    groupingValueRef = None
    for groupingNode in groupingNodeStructure:
        if not hasattr(groupingNode, 'IsKindOf'):
            continue
        groupingValueRef = GroupingValueReference(groupingNode)
        if groupingValueRef:
            break
    return groupingValueRef if groupingValueRef else SpotGroupingReferenceFallback(multiInsAndTradesObj)