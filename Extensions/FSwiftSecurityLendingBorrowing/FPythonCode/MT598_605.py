
# C:\SWIFT\SwiftReader\XSD\MT598_605.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:96afad3d20bbfe8d040a1a097fa388d9fecd10e3
# Generated 2017-02-16 17:36:49.205000 by PyXB version 1.2.2
# Namespace http://www.w3schools.com

import pyxb
import pyxb.binding
import pyxb.binding.saxer
import StringIO
import pyxb.utils.utility
import pyxb.utils.domutils
import sys

# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:64fceb40-f440-11e6-b722-180373dbbcdf')

# Version of PyXB used to generate the bindings
_PyXBVersion = '1.2.6'
# Generated bindings are not compatible across PyXB versions
if pyxb.__version__ != _PyXBVersion:
    raise pyxb.PyXBVersionError(_PyXBVersion)

# Import bindings for namespaces imported into schema
import pyxb.binding.datatypes

# NOTE: All namespace declarations are reserved within the binding
Namespace = pyxb.namespace.NamespaceForURI('http://www.w3schools.com', create_if_missing=True)
Namespace.configureCategories(['typeBinding', 'elementBinding'])

def CreateFromDocument (xml_text, default_namespace=None, location_base=None):
    """Parse the given XML and use the document element to create a
    Python instance.
    
    @kw default_namespace The L{pyxb.Namespace} instance to use as the
    default namespace where there is no default namespace in scope.
    If unspecified or C{None}, the namespace of the module containing
    this function will be used.

    @keyword location_base: An object to be recorded as the base of all
    L{pyxb.utils.utility.Location} instances associated with events and
    objects handled by the parser.  You might pass the URI from which
    the document was obtained.
    """

    if pyxb.XMLStyle_saxer != pyxb._XMLStyle:
        dom = pyxb.utils.domutils.StringToDOM(xml_text)
        return CreateFromDOM(dom.documentElement)
    if default_namespace is None:
        default_namespace = Namespace.fallbackNamespace()
    saxer = pyxb.binding.saxer.make_parser(fallback_namespace=default_namespace, location_base=location_base)
    handler = saxer.getContentHandler()
    saxer.parse(StringIO.StringIO(xml_text))
    instance = handler.rootObject()
    return instance

def CreateFromDOM (node, default_namespace=None):
    """Create a Python instance from the given DOM node.
    The node tag must correspond to an element declaration in this module.

    @deprecated: Forcing use of DOM interface is unnecessary; use L{CreateFromDocument}."""
    if default_namespace is None:
        default_namespace = Namespace.fallbackNamespace()
    return pyxb.binding.basis.element.AnyCreateFromDOM(node, default_namespace)


# Atomic simple type: {http://www.w3schools.com}MT598_605_BCAS_GENL_22F_Type_Pattern
class MT598_605_BCAS_GENL_22F_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_605_BCAS_GENL_22F_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 3, 1)
    _Documentation = None
MT598_605_BCAS_GENL_22F_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_605_BCAS_GENL_22F_Type_Pattern._CF_pattern.addPattern(pattern='(:(INST)/STRA/(RATU))')
MT598_605_BCAS_GENL_22F_Type_Pattern._InitializeFacetMap(MT598_605_BCAS_GENL_22F_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_605_BCAS_GENL_22F_Type_Pattern', MT598_605_BCAS_GENL_22F_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_605_BCAS_GENL_28E_Type_Pattern
class MT598_605_BCAS_GENL_28E_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_605_BCAS_GENL_28E_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 15, 1)
    _Documentation = None
MT598_605_BCAS_GENL_28E_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_605_BCAS_GENL_28E_Type_Pattern._CF_pattern.addPattern(pattern='([0-9]{1,5}/(LAST|MORE|ONLY))')
MT598_605_BCAS_GENL_28E_Type_Pattern._InitializeFacetMap(MT598_605_BCAS_GENL_28E_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_605_BCAS_GENL_28E_Type_Pattern', MT598_605_BCAS_GENL_28E_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_605_BCAS_GENL_98C_Type_Pattern
class MT598_605_BCAS_GENL_98C_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_605_BCAS_GENL_98C_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 27, 1)
    _Documentation = None
MT598_605_BCAS_GENL_98C_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_605_BCAS_GENL_98C_Type_Pattern._CF_pattern.addPattern(pattern='(:(PREP)//[0-9]{8}[0-9]{6})')
MT598_605_BCAS_GENL_98C_Type_Pattern._InitializeFacetMap(MT598_605_BCAS_GENL_98C_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_605_BCAS_GENL_98C_Type_Pattern', MT598_605_BCAS_GENL_98C_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_605_BCAS_CPRTDET_98A_Type_Pattern
class MT598_605_BCAS_CPRTDET_98A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_605_BCAS_CPRTDET_98A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 39, 1)
    _Documentation = None
MT598_605_BCAS_CPRTDET_98A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_605_BCAS_CPRTDET_98A_Type_Pattern._CF_pattern.addPattern(pattern='(:(STRT|ENDT)//[0-9]{8})')
MT598_605_BCAS_CPRTDET_98A_Type_Pattern._InitializeFacetMap(MT598_605_BCAS_CPRTDET_98A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_605_BCAS_CPRTDET_98A_Type_Pattern', MT598_605_BCAS_CPRTDET_98A_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_605_BCAS_CPRTDET_35B_Type_Pattern
class MT598_605_BCAS_CPRTDET_35B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_605_BCAS_CPRTDET_35B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 51, 1)
    _Documentation = None
MT598_605_BCAS_CPRTDET_35B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_605_BCAS_CPRTDET_35B_Type_Pattern._CF_pattern.addPattern(pattern='(ISIN {1}[A-Z0-9]{12}(\\n)?((.{1,35}\\n?){1,4})?)')
MT598_605_BCAS_CPRTDET_35B_Type_Pattern._InitializeFacetMap(MT598_605_BCAS_CPRTDET_35B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_605_BCAS_CPRTDET_35B_Type_Pattern', MT598_605_BCAS_CPRTDET_35B_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_605_BCAS_CPRTDET_14F_Type_Pattern
class MT598_605_BCAS_CPRTDET_14F_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_605_BCAS_CPRTDET_14F_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 63, 1)
    _Documentation = None
MT598_605_BCAS_CPRTDET_14F_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_605_BCAS_CPRTDET_14F_Type_Pattern._CF_pattern.addPattern(pattern='((ZAR)-(JIBAR1|JIBAR3|JIBAR6|JIBAR9|JIBAR12|CPI|PRIME|SREPO|SABOR)(-[A-Z0-9]{4})?)')
MT598_605_BCAS_CPRTDET_14F_Type_Pattern._InitializeFacetMap(MT598_605_BCAS_CPRTDET_14F_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_605_BCAS_CPRTDET_14F_Type_Pattern', MT598_605_BCAS_CPRTDET_14F_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_605_BCAS_GENL_23G_Type_Pattern
class MT598_605_BCAS_GENL_23G_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_605_BCAS_GENL_23G_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 89, 1)
    _Documentation = None
MT598_605_BCAS_GENL_23G_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_605_BCAS_GENL_23G_Type_Pattern._CF_pattern.addPattern(pattern='((NEWM))')
MT598_605_BCAS_GENL_23G_Type_Pattern._InitializeFacetMap(MT598_605_BCAS_GENL_23G_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_605_BCAS_GENL_23G_Type_Pattern', MT598_605_BCAS_GENL_23G_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_605_BCAS_CPRTDET_92A_Type_Pattern
class MT598_605_BCAS_CPRTDET_92A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_605_BCAS_CPRTDET_92A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 101, 1)
    _Documentation = None
MT598_605_BCAS_CPRTDET_92A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_605_BCAS_CPRTDET_92A_Type_Pattern._CF_pattern.addPattern(pattern='(:(INTR)//(N)?[0-9]{1,12},([0-9]{1,2})*)')
MT598_605_BCAS_CPRTDET_92A_Type_Pattern._InitializeFacetMap(MT598_605_BCAS_CPRTDET_92A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_605_BCAS_CPRTDET_92A_Type_Pattern', MT598_605_BCAS_CPRTDET_92A_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_605_20_Type_Pattern
class MT598_605_20_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_605_20_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 113, 1)
    _Documentation = None
MT598_605_20_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_605_20_Type_Pattern._CF_pattern.addPattern(pattern='(.{1,16})')
MT598_605_20_Type_Pattern._InitializeFacetMap(MT598_605_20_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_605_20_Type_Pattern', MT598_605_20_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_605_BCAS_GENL_95R_Type_Pattern
class MT598_605_BCAS_GENL_95R_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_605_BCAS_GENL_95R_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 125, 1)
    _Documentation = None
MT598_605_BCAS_GENL_95R_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_605_BCAS_GENL_95R_Type_Pattern._CF_pattern.addPattern(pattern='(:(ISSA|CSDP|XNNA|TRDR)/STRA/[A-Z]{2}[0-9]{6})')
MT598_605_BCAS_GENL_95R_Type_Pattern._InitializeFacetMap(MT598_605_BCAS_GENL_95R_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_605_BCAS_GENL_95R_Type_Pattern', MT598_605_BCAS_GENL_95R_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_605_BCAS_GENL_LINK_20C_Type_Pattern
class MT598_605_BCAS_GENL_LINK_20C_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_605_BCAS_GENL_LINK_20C_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 137, 1)
    _Documentation = None
MT598_605_BCAS_GENL_LINK_20C_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_605_BCAS_GENL_LINK_20C_Type_Pattern._CF_pattern.addPattern(pattern='(:(PREV)//.{1,16})')
MT598_605_BCAS_GENL_LINK_20C_Type_Pattern._InitializeFacetMap(MT598_605_BCAS_GENL_LINK_20C_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_605_BCAS_GENL_LINK_20C_Type_Pattern', MT598_605_BCAS_GENL_LINK_20C_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_605_16R_Type
class MT598_605_16R_Type (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_605_16R_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 149, 1)
    _Documentation = None
MT598_605_16R_Type._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'MT598_605_16R_Type', MT598_605_16R_Type)

# Complex type {http://www.w3schools.com}MT598_605_77E_Type with content type SIMPLE
class MT598_605_77E_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_605_77E_Type with content type SIMPLE"""
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_605_77E_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 75, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.string
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_605_77E_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='77E')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 78, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 78, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_605_77E_Type', MT598_605_77E_Type)


# Complex type {http://www.w3schools.com}MT598_605_12_Type with content type SIMPLE
class MT598_605_12_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_605_12_Type with content type SIMPLE"""
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_605_12_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 82, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.string
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_605_12_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='12')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 85, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 85, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_605_12_Type', MT598_605_12_Type)


# Complex type {http://www.w3schools.com}MT598_605_BCAS_GENL with content type ELEMENT_ONLY
class MT598_605_BCAS_GENL (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_605_BCAS_GENL with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_605_BCAS_GENL')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 152, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}PageNumberContinuationIndicator uses Python identifier PageNumberContinuationIndicator
    __PageNumberContinuationIndicator = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PageNumberContinuationIndicator'), 'PageNumberContinuationIndicator', '__httpwww_w3schools_com_MT598_605_BCAS_GENL_httpwww_w3schools_comPageNumberContinuationIndicator', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 154, 3), )

    
    PageNumberContinuationIndicator = property(__PageNumberContinuationIndicator.value, __PageNumberContinuationIndicator.set, None, None)

    
    # Element {http://www.w3schools.com}FunctionOfMessage uses Python identifier FunctionOfMessage
    __FunctionOfMessage = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'FunctionOfMessage'), 'FunctionOfMessage', '__httpwww_w3schools_com_MT598_605_BCAS_GENL_httpwww_w3schools_comFunctionOfMessage', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 155, 3), )

    
    FunctionOfMessage = property(__FunctionOfMessage.value, __FunctionOfMessage.set, None, None)

    
    # Element {http://www.w3schools.com}PreparationDateAndTime uses Python identifier PreparationDateAndTime
    __PreparationDateAndTime = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PreparationDateAndTime'), 'PreparationDateAndTime', '__httpwww_w3schools_com_MT598_605_BCAS_GENL_httpwww_w3schools_comPreparationDateAndTime', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 156, 3), )

    
    PreparationDateAndTime = property(__PreparationDateAndTime.value, __PreparationDateAndTime.set, None, None)

    
    # Element {http://www.w3schools.com}TypeOfInstructionIndicator uses Python identifier TypeOfInstructionIndicator
    __TypeOfInstructionIndicator = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'TypeOfInstructionIndicator'), 'TypeOfInstructionIndicator', '__httpwww_w3schools_com_MT598_605_BCAS_GENL_httpwww_w3schools_comTypeOfInstructionIndicator', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 157, 3), )

    
    TypeOfInstructionIndicator = property(__TypeOfInstructionIndicator.value, __TypeOfInstructionIndicator.set, None, None)

    
    # Element {http://www.w3schools.com}IssueAgentCSDParticipantCodeNNADirectTraderBPID uses Python identifier IssueAgentCSDParticipantCodeNNADirectTraderBPID
    __IssueAgentCSDParticipantCodeNNADirectTraderBPID = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'IssueAgentCSDParticipantCodeNNADirectTraderBPID'), 'IssueAgentCSDParticipantCodeNNADirectTraderBPID', '__httpwww_w3schools_com_MT598_605_BCAS_GENL_httpwww_w3schools_comIssueAgentCSDParticipantCodeNNADirectTraderBPID', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 158, 3), )

    
    IssueAgentCSDParticipantCodeNNADirectTraderBPID = property(__IssueAgentCSDParticipantCodeNNADirectTraderBPID.value, __IssueAgentCSDParticipantCodeNNADirectTraderBPID.set, None, None)

    
    # Element {http://www.w3schools.com}LINK uses Python identifier LINK
    __LINK = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'LINK'), 'LINK', '__httpwww_w3schools_com_MT598_605_BCAS_GENL_httpwww_w3schools_comLINK', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 159, 3), )

    
    LINK = property(__LINK.value, __LINK.set, None, None)

    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_605_BCAS_GENL_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='16R')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 161, 2)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 161, 2)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        __PageNumberContinuationIndicator.name() : __PageNumberContinuationIndicator,
        __FunctionOfMessage.name() : __FunctionOfMessage,
        __PreparationDateAndTime.name() : __PreparationDateAndTime,
        __TypeOfInstructionIndicator.name() : __TypeOfInstructionIndicator,
        __IssueAgentCSDParticipantCodeNNADirectTraderBPID.name() : __IssueAgentCSDParticipantCodeNNADirectTraderBPID,
        __LINK.name() : __LINK
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_605_BCAS_GENL', MT598_605_BCAS_GENL)


# Complex type {http://www.w3schools.com}MT598_605_BCAS with content type ELEMENT_ONLY
class MT598_605_BCAS (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_605_BCAS with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_605_BCAS')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 163, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}GENL uses Python identifier GENL
    __GENL = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'GENL'), 'GENL', '__httpwww_w3schools_com_MT598_605_BCAS_httpwww_w3schools_comGENL', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 165, 3), )

    
    GENL = property(__GENL.value, __GENL.set, None, None)

    
    # Element {http://www.w3schools.com}CPRTDET uses Python identifier CPRTDET
    __CPRTDET = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CPRTDET'), 'CPRTDET', '__httpwww_w3schools_com_MT598_605_BCAS_httpwww_w3schools_comCPRTDET', True, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 166, 3), )

    
    CPRTDET = property(__CPRTDET.value, __CPRTDET.set, None, None)

    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_605_BCAS_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='16R')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 168, 2)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 168, 2)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        __GENL.name() : __GENL,
        __CPRTDET.name() : __CPRTDET
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_605_BCAS', MT598_605_BCAS)


# Complex type {http://www.w3schools.com}MT598_605_BCAS_CPRTDET with content type ELEMENT_ONLY
class MT598_605_BCAS_CPRTDET (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_605_BCAS_CPRTDET with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_605_BCAS_CPRTDET')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 170, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}IdentificationOfSecurities uses Python identifier IdentificationOfSecurities
    __IdentificationOfSecurities = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'IdentificationOfSecurities'), 'IdentificationOfSecurities', '__httpwww_w3schools_com_MT598_605_BCAS_CPRTDET_httpwww_w3schools_comIdentificationOfSecurities', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 172, 3), )

    
    IdentificationOfSecurities = property(__IdentificationOfSecurities.value, __IdentificationOfSecurities.set, None, None)

    
    # Element {http://www.w3schools.com}CouponRateSource uses Python identifier CouponRateSource
    __CouponRateSource = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CouponRateSource'), 'CouponRateSource', '__httpwww_w3schools_com_MT598_605_BCAS_CPRTDET_httpwww_w3schools_comCouponRateSource', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 173, 3), )

    
    CouponRateSource = property(__CouponRateSource.value, __CouponRateSource.set, None, None)

    
    # Element {http://www.w3schools.com}CurrentCouponRate uses Python identifier CurrentCouponRate
    __CurrentCouponRate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CurrentCouponRate'), 'CurrentCouponRate', '__httpwww_w3schools_com_MT598_605_BCAS_CPRTDET_httpwww_w3schools_comCurrentCouponRate', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 174, 3), )

    
    CurrentCouponRate = property(__CurrentCouponRate.value, __CurrentCouponRate.set, None, None)

    
    # Element {http://www.w3schools.com}CouponResetStartEndDate uses Python identifier CouponResetStartEndDate
    __CouponResetStartEndDate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CouponResetStartEndDate'), 'CouponResetStartEndDate', '__httpwww_w3schools_com_MT598_605_BCAS_CPRTDET_httpwww_w3schools_comCouponResetStartEndDate', True, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 175, 3), )

    
    CouponResetStartEndDate = property(__CouponResetStartEndDate.value, __CouponResetStartEndDate.set, None, None)

    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_605_BCAS_CPRTDET_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='16R')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 177, 2)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 177, 2)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        __IdentificationOfSecurities.name() : __IdentificationOfSecurities,
        __CouponRateSource.name() : __CouponRateSource,
        __CurrentCouponRate.name() : __CurrentCouponRate,
        __CouponResetStartEndDate.name() : __CouponResetStartEndDate
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_605_BCAS_CPRTDET', MT598_605_BCAS_CPRTDET)


# Complex type {http://www.w3schools.com}MT598_605_BCAS_GENL_LINK with content type ELEMENT_ONLY
class MT598_605_BCAS_GENL_LINK (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_605_BCAS_GENL_LINK with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_605_BCAS_GENL_LINK')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 179, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}PreviousReference uses Python identifier PreviousReference
    __PreviousReference = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PreviousReference'), 'PreviousReference', '__httpwww_w3schools_com_MT598_605_BCAS_GENL_LINK_httpwww_w3schools_comPreviousReference', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 181, 3), )

    
    PreviousReference = property(__PreviousReference.value, __PreviousReference.set, None, None)

    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_605_BCAS_GENL_LINK_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='16R')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 183, 2)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 183, 2)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        __PreviousReference.name() : __PreviousReference
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_605_BCAS_GENL_LINK', MT598_605_BCAS_GENL_LINK)


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 186, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}TransactionReference uses Python identifier TransactionReference
    __TransactionReference = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'TransactionReference'), 'TransactionReference', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comTransactionReference', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 188, 4), )

    
    TransactionReference = property(__TransactionReference.value, __TransactionReference.set, None, None)

    
    # Element {http://www.w3schools.com}SubMessageType uses Python identifier SubMessageType
    __SubMessageType = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SubMessageType'), 'SubMessageType', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comSubMessageType', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 189, 4), )

    
    SubMessageType = property(__SubMessageType.value, __SubMessageType.set, None, None)

    
    # Element {http://www.w3schools.com}ProprietaryMessage uses Python identifier ProprietaryMessage
    __ProprietaryMessage = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ProprietaryMessage'), 'ProprietaryMessage', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comProprietaryMessage', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 190, 4), )

    
    ProprietaryMessage = property(__ProprietaryMessage.value, __ProprietaryMessage.set, None, None)

    
    # Element {http://www.w3schools.com}BCAS uses Python identifier BCAS
    __BCAS = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'BCAS'), 'BCAS', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comBCAS', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 191, 4), )

    
    BCAS = property(__BCAS.value, __BCAS.set, None, None)

    _ElementMap.update({
        __TransactionReference.name() : __TransactionReference,
        __SubMessageType.name() : __SubMessageType,
        __ProprietaryMessage.name() : __ProprietaryMessage,
        __BCAS.name() : __BCAS
    })
    _AttributeMap.update({
        
    })



# Complex type {http://www.w3schools.com}MT598_605_BCAS_GENL_22F_Type with content type SIMPLE
class MT598_605_BCAS_GENL_22F_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_605_BCAS_GENL_22F_Type with content type SIMPLE"""
    _TypeDefinition = MT598_605_BCAS_GENL_22F_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_605_BCAS_GENL_22F_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 8, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_605_BCAS_GENL_22F_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_605_BCAS_GENL_22F_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='22F')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 11, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 11, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_605_BCAS_GENL_22F_Type', MT598_605_BCAS_GENL_22F_Type)


# Complex type {http://www.w3schools.com}MT598_605_BCAS_GENL_28E_Type with content type SIMPLE
class MT598_605_BCAS_GENL_28E_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_605_BCAS_GENL_28E_Type with content type SIMPLE"""
    _TypeDefinition = MT598_605_BCAS_GENL_28E_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_605_BCAS_GENL_28E_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 20, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_605_BCAS_GENL_28E_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_605_BCAS_GENL_28E_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='28E')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 23, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 23, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_605_BCAS_GENL_28E_Type', MT598_605_BCAS_GENL_28E_Type)


# Complex type {http://www.w3schools.com}MT598_605_BCAS_GENL_98C_Type with content type SIMPLE
class MT598_605_BCAS_GENL_98C_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_605_BCAS_GENL_98C_Type with content type SIMPLE"""
    _TypeDefinition = MT598_605_BCAS_GENL_98C_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_605_BCAS_GENL_98C_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 32, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_605_BCAS_GENL_98C_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_605_BCAS_GENL_98C_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='98C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 35, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 35, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_605_BCAS_GENL_98C_Type', MT598_605_BCAS_GENL_98C_Type)


# Complex type {http://www.w3schools.com}MT598_605_BCAS_CPRTDET_98A_Type with content type SIMPLE
class MT598_605_BCAS_CPRTDET_98A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_605_BCAS_CPRTDET_98A_Type with content type SIMPLE"""
    _TypeDefinition = MT598_605_BCAS_CPRTDET_98A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_605_BCAS_CPRTDET_98A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 44, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_605_BCAS_CPRTDET_98A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_605_BCAS_CPRTDET_98A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='98A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 47, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 47, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_605_BCAS_CPRTDET_98A_Type', MT598_605_BCAS_CPRTDET_98A_Type)


# Complex type {http://www.w3schools.com}MT598_605_BCAS_CPRTDET_35B_Type with content type SIMPLE
class MT598_605_BCAS_CPRTDET_35B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_605_BCAS_CPRTDET_35B_Type with content type SIMPLE"""
    _TypeDefinition = MT598_605_BCAS_CPRTDET_35B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_605_BCAS_CPRTDET_35B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 56, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_605_BCAS_CPRTDET_35B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_605_BCAS_CPRTDET_35B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='35B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 59, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 59, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_605_BCAS_CPRTDET_35B_Type', MT598_605_BCAS_CPRTDET_35B_Type)


# Complex type {http://www.w3schools.com}MT598_605_BCAS_CPRTDET_14F_Type with content type SIMPLE
class MT598_605_BCAS_CPRTDET_14F_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_605_BCAS_CPRTDET_14F_Type with content type SIMPLE"""
    _TypeDefinition = MT598_605_BCAS_CPRTDET_14F_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_605_BCAS_CPRTDET_14F_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 68, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_605_BCAS_CPRTDET_14F_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_605_BCAS_CPRTDET_14F_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='14F')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 71, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 71, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_605_BCAS_CPRTDET_14F_Type', MT598_605_BCAS_CPRTDET_14F_Type)


# Complex type {http://www.w3schools.com}MT598_605_BCAS_GENL_23G_Type with content type SIMPLE
class MT598_605_BCAS_GENL_23G_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_605_BCAS_GENL_23G_Type with content type SIMPLE"""
    _TypeDefinition = MT598_605_BCAS_GENL_23G_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_605_BCAS_GENL_23G_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 94, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_605_BCAS_GENL_23G_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_605_BCAS_GENL_23G_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='23G')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 97, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 97, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_605_BCAS_GENL_23G_Type', MT598_605_BCAS_GENL_23G_Type)


# Complex type {http://www.w3schools.com}MT598_605_BCAS_CPRTDET_92A_Type with content type SIMPLE
class MT598_605_BCAS_CPRTDET_92A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_605_BCAS_CPRTDET_92A_Type with content type SIMPLE"""
    _TypeDefinition = MT598_605_BCAS_CPRTDET_92A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_605_BCAS_CPRTDET_92A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 106, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_605_BCAS_CPRTDET_92A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_605_BCAS_CPRTDET_92A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='92A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 109, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 109, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_605_BCAS_CPRTDET_92A_Type', MT598_605_BCAS_CPRTDET_92A_Type)


# Complex type {http://www.w3schools.com}MT598_605_20_Type with content type SIMPLE
class MT598_605_20_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_605_20_Type with content type SIMPLE"""
    _TypeDefinition = MT598_605_20_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_605_20_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 118, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_605_20_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_605_20_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='20')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 121, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 121, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_605_20_Type', MT598_605_20_Type)


# Complex type {http://www.w3schools.com}MT598_605_BCAS_GENL_95R_Type with content type SIMPLE
class MT598_605_BCAS_GENL_95R_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_605_BCAS_GENL_95R_Type with content type SIMPLE"""
    _TypeDefinition = MT598_605_BCAS_GENL_95R_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_605_BCAS_GENL_95R_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 130, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_605_BCAS_GENL_95R_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_605_BCAS_GENL_95R_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='95R')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 133, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 133, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_605_BCAS_GENL_95R_Type', MT598_605_BCAS_GENL_95R_Type)


# Complex type {http://www.w3schools.com}MT598_605_BCAS_GENL_LINK_20C_Type with content type SIMPLE
class MT598_605_BCAS_GENL_LINK_20C_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_605_BCAS_GENL_LINK_20C_Type with content type SIMPLE"""
    _TypeDefinition = MT598_605_BCAS_GENL_LINK_20C_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_605_BCAS_GENL_LINK_20C_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 142, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_605_BCAS_GENL_LINK_20C_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_605_BCAS_GENL_LINK_20C_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='20C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 145, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 145, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_605_BCAS_GENL_LINK_20C_Type', MT598_605_BCAS_GENL_LINK_20C_Type)


MT598_605 = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'MT598_605'), CTD_ANON, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 185, 1))
Namespace.addCategoryObject('elementBinding', MT598_605.name().localName(), MT598_605)



MT598_605_BCAS_GENL._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PageNumberContinuationIndicator'), MT598_605_BCAS_GENL_28E_Type, scope=MT598_605_BCAS_GENL, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 154, 3)))

MT598_605_BCAS_GENL._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'FunctionOfMessage'), MT598_605_BCAS_GENL_23G_Type, scope=MT598_605_BCAS_GENL, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 155, 3)))

MT598_605_BCAS_GENL._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PreparationDateAndTime'), MT598_605_BCAS_GENL_98C_Type, scope=MT598_605_BCAS_GENL, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 156, 3)))

MT598_605_BCAS_GENL._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TypeOfInstructionIndicator'), MT598_605_BCAS_GENL_22F_Type, scope=MT598_605_BCAS_GENL, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 157, 3)))

MT598_605_BCAS_GENL._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'IssueAgentCSDParticipantCodeNNADirectTraderBPID'), MT598_605_BCAS_GENL_95R_Type, scope=MT598_605_BCAS_GENL, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 158, 3)))

MT598_605_BCAS_GENL._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'LINK'), MT598_605_BCAS_GENL_LINK, scope=MT598_605_BCAS_GENL, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 159, 3)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 159, 3))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT598_605_BCAS_GENL._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PageNumberContinuationIndicator')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 154, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT598_605_BCAS_GENL._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'FunctionOfMessage')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 155, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT598_605_BCAS_GENL._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PreparationDateAndTime')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 156, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT598_605_BCAS_GENL._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'TypeOfInstructionIndicator')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 157, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT598_605_BCAS_GENL._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'IssueAgentCSDParticipantCodeNNADirectTraderBPID')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 158, 3))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(MT598_605_BCAS_GENL._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'LINK')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 159, 3))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
         ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
         ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
         ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_5._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
MT598_605_BCAS_GENL._Automaton = _BuildAutomaton()




MT598_605_BCAS._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'GENL'), MT598_605_BCAS_GENL, scope=MT598_605_BCAS, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 165, 3)))

MT598_605_BCAS._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CPRTDET'), MT598_605_BCAS_CPRTDET, scope=MT598_605_BCAS, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 166, 3)))

def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT598_605_BCAS._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'GENL')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 165, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT598_605_BCAS._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CPRTDET')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 166, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
MT598_605_BCAS._Automaton = _BuildAutomaton_()




MT598_605_BCAS_CPRTDET._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'IdentificationOfSecurities'), MT598_605_BCAS_CPRTDET_35B_Type, scope=MT598_605_BCAS_CPRTDET, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 172, 3)))

MT598_605_BCAS_CPRTDET._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CouponRateSource'), MT598_605_BCAS_CPRTDET_14F_Type, scope=MT598_605_BCAS_CPRTDET, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 173, 3)))

MT598_605_BCAS_CPRTDET._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CurrentCouponRate'), MT598_605_BCAS_CPRTDET_92A_Type, scope=MT598_605_BCAS_CPRTDET, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 174, 3)))

MT598_605_BCAS_CPRTDET._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CouponResetStartEndDate'), MT598_605_BCAS_CPRTDET_98A_Type, scope=MT598_605_BCAS_CPRTDET, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 175, 3)))

def _BuildAutomaton_2 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_2
    del _BuildAutomaton_2
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT598_605_BCAS_CPRTDET._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'IdentificationOfSecurities')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 172, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT598_605_BCAS_CPRTDET._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CouponRateSource')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 173, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT598_605_BCAS_CPRTDET._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CurrentCouponRate')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 174, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT598_605_BCAS_CPRTDET._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CouponResetStartEndDate')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 175, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
         ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
         ]))
    st_3._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
MT598_605_BCAS_CPRTDET._Automaton = _BuildAutomaton_2()




MT598_605_BCAS_GENL_LINK._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PreviousReference'), MT598_605_BCAS_GENL_LINK_20C_Type, scope=MT598_605_BCAS_GENL_LINK, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 181, 3)))

def _BuildAutomaton_3 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_3
    del _BuildAutomaton_3
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT598_605_BCAS_GENL_LINK._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PreviousReference')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 181, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
MT598_605_BCAS_GENL_LINK._Automaton = _BuildAutomaton_3()




CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TransactionReference'), MT598_605_20_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 188, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SubMessageType'), MT598_605_12_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 189, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ProprietaryMessage'), MT598_605_77E_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 190, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'BCAS'), MT598_605_BCAS, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 191, 4)))

def _BuildAutomaton_4 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_4
    del _BuildAutomaton_4
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'TransactionReference')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 188, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SubMessageType')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 189, 4))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ProprietaryMessage')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 190, 4))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'BCAS')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_605.xsd', 191, 4))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
         ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    st_3._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON._Automaton = _BuildAutomaton_4()

