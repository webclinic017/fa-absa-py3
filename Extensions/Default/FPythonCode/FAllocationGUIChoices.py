"""----------------------------------------------------------------------------
    
    MODULE: FAllocationGUIChoices
    
    DECRIPTION: 
    Utility functions for populating GUI controls.

----------------------------------------------------------------------------"""
import acm
import FAllocationUtils

def ruleDimensionChoices():
    return acm.FAllocationDimension.Select('')

def bucketDimensionChoices(bucket):
    dim = bucket.Rule().Dimension()
    if dim:
        return dim.AvailableValues()
    return []

def allocationDefinitionChoices():
    ext = acm.GetDefaultContext().GetAllExtensions('FAllocationDefinition', 'FObject', True, True)
    return ext

def templateRuleChoices():
    template_rules = acm.FAllocationRule.Select('isTemplate=True and isScheme=False')
    return template_rules

def tradePropertyNameChoices():
    return FAllocationUtils.get_attribute_names()
