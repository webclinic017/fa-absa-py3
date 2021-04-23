'''
P A C K A G E   I N S T A L L E R   R  E F E R E N C E S
Copyright (C) 2015 by SunGard Front Arena AB.
All rights reserved.

Author: Michael Gogins

This is a configurable template. To change the default behavior, edit 
this module and save it under the name PackageInstallerReferences.
'''

import acm

valuationParameterInformation = acm.FACMServer().GetFunction("valuationParameterInformation", 3)
spaceCollection = acm.FCalculationMethods().CreateStandardCalculationsSpaceCollection()

'''
Returns True if the "part" of an FObject should be kept as part of the AMBA 
message, False otherwise. If the "part" is removed, then in order to register 
the actual data dependencies, its references out should be treated as 
references out of the "part's" parent object. The default should be True. 

An example of a "part" that should NOT be removed is an FLeg in an ????????? Richard & Tarik
FInstrument.Legs() collection.

PLEASE NOTE: the list of items that return False here should be in a 
one-to-one correspondence with the list of items that return False from 
the should_remove_sub_message() function.
'''
def should_remove_part(object, part):
    #return True # Test

    if object.IsKindOf(acm.FInstrument) and part.IsKindOf(acm.FLeg):
        return True
    if part.IsKindOf(acm.FAdditionalInfo):
        return False
    if part.IsKindOf(acm.FMoneyMarketDecomposition):
        return False
    if part.IsKindOf(acm.FCalendarDate):
        return False
    
    return False
    
'''
Returns True if the child message should be removed from its parent, or False 
otherwise. 

PLEASE NOTE: the list of items that return False here should be in a 
one-to-one correspondence with the list of items that return False from 
the should_remove_part() function.
'''
def should_remove_sub_message(parent, child):
    #return False # Test
    
    if child == 'LEG':
        return False
    if child == 'ADDITIONALINFO':
        return False
    if child == 'MONEYMARKETDECOMP':
        return False
    if child == 'CALENDARDATE':
        return False
    return True

'''
Returns True if the reference out should be included in the dependency graph,
or False otherwise. There may be more than one required reference out for the 
same object. More derived classes should be tested first in the code. The 
default value must be True. Null references are not followed, and cause a 
warning.
'''
def should_follow_reference_out(object, reference_out):
    if reference_out == None:
        print('Warning: reference_out is:', reference_out)
        return False
    if object.IsKindOf(acm.FCommonObject):
        if reference_out.IsKindOf(acm.FUser):
            return False
        if reference_out.IsKindOf(acm.FPartyAlias):
            return False
        if reference_out.IsKindOf(acm.FInstrAliasType):
            return False
            
    if object.IsKindOf(acm.FContextLink):
        return False
            
    return True

'''
Returns True if the reference in should be included in the dependency graph,
or False otherwise. There may be more than one required reference in for the 
same object. More derived classes should be tested first in the code. The 
default value must be False. Null references are not followed, and cause a 
warning.
'''
def should_follow_reference_in(object, reference_in):
    if reference_in is None:
        print('Warning: reference_in is:', reference_in)
        return False
    """
    if object.Parts():
        for parts in object.Parts():
            if (not parts is None) and (reference_in in parts):
                return True
    return False
    """
    
    if object.IsKindOf(acm.FParty):
        if reference_in.IsKindOf(acm.FParty):
            return True
        if reference_in.IsKindOf(acm.FAdditionalInfo):
            return True
        if reference_in.IsKindOf(acm.FPartyAlias):
            return True
        if reference_in.IsKindOf(acm.FContact):
            return True
    if object.IsKindOf(acm.FInstrument):
        if reference_in.IsKindOf(acm.FCombInstrMap):# or reference_in.IsKindOf(acm.FLeg):
            return True
        if reference_in.IsKindOf(acm.FAdditionalInfo):
            return True
    if object.IsKindOf(acm.FBenchmark):
        if reference_in.IsKindOf(acm.FInstrument):
            return True
        if reference_in.IsKindOf(acm.FAdditionalInfo):
            return True
    if object.IsKindOf(acm.FYieldPoint):
        if reference_in.IsKindOf(acm.FInstrument):
            return True
        if reference_in.IsKindOf(acm.FAdditionalInfo):
            return True
    if object.IsKindOf(acm.FPhysicalPortfolio):
        if reference_in.IsKindOf(acm.FTrade):
            return True
        if reference_in.IsKindOf(acm.FAdditionalInfo):
            return True
    if object.IsKindOf(acm.FYieldCurve):
        if reference_in.IsKindOf(acm.FBenchmark):
            return True
        if reference_in.IsKindOf(acm.FAdditionalInfo):
            return True
    if object.IsKindOf(acm.FYieldCurve):
        if reference_in.IsKindOf(acm.FYieldPoint):
            return True    
        if reference_in.IsKindOf(acm.FAdditionalInfo):
            return True
    if object.IsKindOf(acm.FYieldCurve):
        if reference_in.IsKindOf(acm.FInstrument):
            return True    
        if reference_in.IsKindOf(acm.FAdditionalInfo):
            return True
    if object.IsKindOf(acm.FCalendar):
        if reference_in.IsKindOf(acm.FCalendarDate):
            return True    
    if object.IsKindOf(acm.FVolatilityStructure):
        if reference_in.IsKindOf(acm.FVolatilityPoint):
            return True
    if object.IsKindOf(acm.FVolatilityStructure):
        if reference_in.IsKindOf(acm.FVolatilitySkew):
            return True
    return False
    
'''
Customize this to not import link table objects when 
one end of the link is in the parent AMBA message,
and the other end of the link is a separate AMBA message,
as that would be redundant and could cause key errors on 
import.
'''
def should_import_link_record(object):
    return True
    
'''
Returns all context links for the instrument.
'''    
def get_context_links(instrument):
    context_links = []
    for context_link in acm.FContextLink.Select("instrument='%s'" % instrument.Name()):
        context_links.append(context_link)
    valuation_group = instrument.ValuationGrpChlItem()
    if valuation_group != None:
        valuation_group_name = valuation_group.Name()
        for context_link in acm.FContextLink.Select("mappingType='Val Group' and currency='%s'" % instrument.Currency().Name()):
            context_links.append(context_link)
    underlying = instrument.Underlying()
    if underlying != None:
        for context_link in acm.FContextLink.Select("instrument='%s'" % underlying.Name()):
            context_links.append(context_link)
        valuation_group = underlying.ValuationGrpChlItem()
        if valuation_group != None:
            valuation_group_name = valuation_group.Name()
            for context_link in acm.FContextLink.Select("mappingType='Val Group' and currency='%s'" % underlying.Currency().Name()):
                context_links.append(context_link)
    return context_links 
    
'''
Customize this to follow non-database dependencies, for example, to include 
prices or valuation parameters required by instruments. Be careful! This can 
greatly expand the dependency tree.
'''
def non_database_dependencies(object):
    dependencies = []
    if object.IsKindOf(acm.FInstrument) and False: # temporarly deactivated
        if object.IsKindOf(acm.FFuture):
            for price in object.Prices():
                dependencies.append(price)
        source = object.Calculation().TheoreticalValueSource(spaceCollection)
        dictionary = valuationParameterInformation(source, "", acm.GetDefaultContext())
        if dictionary != None:
            for key in dictionary.Keys():
                values = dictionary.At(key)
                for value in values:
                    if str(type(value)) == "<type 'FIrCurveInformation'>":
                        yield_curve = value.YieldCurve()
                        if yield_curve != None:
                            dependencies.append(yield_curve)
                        underlying_yield_curve = value.UnderlyingYieldCurve()
                        if underlying_yield_curve != None:
                            dependencies.append(underlying_yield_curve)   
            volatilitylink = object.MappedVolatilityLink()
            if volatilitylink != None:
                link = volatilitylink.Link()
                if link != None:
                    #print('link: %s %s' % (type(link), link))
                    structure = link.VolatilityStructure()
                    if structure != None:
                        dependencies.append(structure)
    return dependencies
'''
Returns a specialized FAMBADefinition for the specified class. More derived 
classes must be tested first. The default value must be 'ExportDefault.'
'''
def amba_definition_for_class(classname):
    amba_definition = acm.GetDefaultContext().GetExtension('FAMBADefinition', str(classname), 'PackageExport')
    if not amba_definition:
        amba_definition = acm.GetDefaultContext().GetExtension('FAMBADefinition', 'FObject', 'PackageExport')
    '''
    if classname == 'MyClassname':
        return acm.GetDefaultContext().GetExtension('FAMBADefinition', 'MyClassname', 'MyAmbaDefinitionName').Value()
    '''
    return amba_definition.Value()

