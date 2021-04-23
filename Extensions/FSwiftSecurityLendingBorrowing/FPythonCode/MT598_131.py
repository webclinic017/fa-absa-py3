
# C:\Swift\Templates\MT598_131.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:96afad3d20bbfe8d040a1a097fa388d9fecd10e3
# Generated 2019-09-13 19:02:36.719000 by PyXB version 1.2.2
# Namespace http://www.w3schools.com

import pyxb
import pyxb.binding
import pyxb.binding.saxer
import StringIO
import pyxb.utils.utility
import pyxb.utils.domutils
import sys

# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:f30e6c4f-d62a-11e9-9ec5-8851fb4dff7a')

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


# Atomic simple type: {http://www.w3schools.com}MT598_131_SEQUENCE_30P_Type_Pattern
class MT598_131_SEQUENCE_30P_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_131_SEQUENCE_30P_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 3, 1)
    _Documentation = None
MT598_131_SEQUENCE_30P_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_131_SEQUENCE_30P_Type_Pattern._CF_pattern.addPattern(pattern='([0-9]{1,8})')
MT598_131_SEQUENCE_30P_Type_Pattern._InitializeFacetMap(MT598_131_SEQUENCE_30P_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_131_SEQUENCE_30P_Type_Pattern', MT598_131_SEQUENCE_30P_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_131_18A_Type_Pattern
class MT598_131_18A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_131_18A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 24, 1)
    _Documentation = None
MT598_131_18A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_131_18A_Type_Pattern._CF_pattern.addPattern(pattern='([0-9]{1,5})')
MT598_131_18A_Type_Pattern._InitializeFacetMap(MT598_131_18A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_131_18A_Type_Pattern', MT598_131_18A_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_131_SEQUENCE_82B_Type_Pattern
class MT598_131_SEQUENCE_82B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_131_SEQUENCE_82B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 37, 1)
    _Documentation = None
MT598_131_SEQUENCE_82B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_131_SEQUENCE_82B_Type_Pattern._CF_pattern.addPattern(pattern='([A-Z]{1,2}[0-9]{1,6})')
MT598_131_SEQUENCE_82B_Type_Pattern._InitializeFacetMap(MT598_131_SEQUENCE_82B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_131_SEQUENCE_82B_Type_Pattern', MT598_131_SEQUENCE_82B_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_131_20_Type_Pattern
class MT598_131_20_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_131_20_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 50, 1)
    _Documentation = None
MT598_131_20_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_131_20_Type_Pattern._CF_pattern.addPattern(pattern="(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,16})")
MT598_131_20_Type_Pattern._InitializeFacetMap(MT598_131_20_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_131_20_Type_Pattern', MT598_131_20_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_131_SEQUENCE_35A_Type_Pattern
class MT598_131_SEQUENCE_35A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_131_SEQUENCE_35A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 63, 1)
    _Documentation = None
MT598_131_SEQUENCE_35A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_131_SEQUENCE_35A_Type_Pattern._CF_pattern.addPattern(pattern='([A-Z]{1,3}[0-9]{1,15})')
MT598_131_SEQUENCE_35A_Type_Pattern._InitializeFacetMap(MT598_131_SEQUENCE_35A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_131_SEQUENCE_35A_Type_Pattern', MT598_131_SEQUENCE_35A_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_131_SEQUENCE_26H_Type_Pattern
class MT598_131_SEQUENCE_26H_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_131_SEQUENCE_26H_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 76, 1)
    _Documentation = None
MT598_131_SEQUENCE_26H_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_131_SEQUENCE_26H_Type_Pattern._CF_pattern.addPattern(pattern='(([A-Z]{1,2}[0-9]{1,6})?/[0-9]{1,10})')
MT598_131_SEQUENCE_26H_Type_Pattern._InitializeFacetMap(MT598_131_SEQUENCE_26H_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_131_SEQUENCE_26H_Type_Pattern', MT598_131_SEQUENCE_26H_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_131_SEQUENCE_87C_Type_Pattern
class MT598_131_SEQUENCE_87C_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_131_SEQUENCE_87C_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 89, 1)
    _Documentation = None
MT598_131_SEQUENCE_87C_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_131_SEQUENCE_87C_Type_Pattern._CF_pattern.addPattern(pattern='(/[A-Z]{1,2}[0-9]{1,6})')
MT598_131_SEQUENCE_87C_Type_Pattern._InitializeFacetMap(MT598_131_SEQUENCE_87C_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_131_SEQUENCE_87C_Type_Pattern', MT598_131_SEQUENCE_87C_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_131_SEQUENCE_35B_Type_Pattern
class MT598_131_SEQUENCE_35B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_131_SEQUENCE_35B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 102, 1)
    _Documentation = None
MT598_131_SEQUENCE_35B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_131_SEQUENCE_35B_Type_Pattern._CF_pattern.addPattern(pattern='((ISIN {1}[A-Z0-9]{12})?)')
MT598_131_SEQUENCE_35B_Type_Pattern._InitializeFacetMap(MT598_131_SEQUENCE_35B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_131_SEQUENCE_35B_Type_Pattern', MT598_131_SEQUENCE_35B_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_131_SEQUENCE_30F_Type_Pattern
class MT598_131_SEQUENCE_30F_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_131_SEQUENCE_30F_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 115, 1)
    _Documentation = None
MT598_131_SEQUENCE_30F_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_131_SEQUENCE_30F_Type_Pattern._CF_pattern.addPattern(pattern='([0-9]{1,8})')
MT598_131_SEQUENCE_30F_Type_Pattern._InitializeFacetMap(MT598_131_SEQUENCE_30F_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_131_SEQUENCE_30F_Type_Pattern', MT598_131_SEQUENCE_30F_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_131_SEQUENCE_23_Type_Pattern
class MT598_131_SEQUENCE_23_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_131_SEQUENCE_23_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 128, 1)
    _Documentation = None
MT598_131_SEQUENCE_23_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_131_SEQUENCE_23_Type_Pattern._CF_pattern.addPattern(pattern='((DVP|DFP|RVP|RFP|PMO|RMO)(/[A-Z]{1,2}([0-9]{1,1})?)?)')
MT598_131_SEQUENCE_23_Type_Pattern._InitializeFacetMap(MT598_131_SEQUENCE_23_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_131_SEQUENCE_23_Type_Pattern', MT598_131_SEQUENCE_23_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_131_SEQUENCE_32B_Type_Pattern
class MT598_131_SEQUENCE_32B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_131_SEQUENCE_32B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 141, 1)
    _Documentation = None
MT598_131_SEQUENCE_32B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_131_SEQUENCE_32B_Type_Pattern._CF_pattern.addPattern(pattern='([A-Z]{1,3}[0-9]{1,15})')
MT598_131_SEQUENCE_32B_Type_Pattern._InitializeFacetMap(MT598_131_SEQUENCE_32B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_131_SEQUENCE_32B_Type_Pattern', MT598_131_SEQUENCE_32B_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_131_SEQUENCE_79_Type_Pattern
class MT598_131_SEQUENCE_79_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_131_SEQUENCE_79_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 162, 1)
    _Documentation = None
MT598_131_SEQUENCE_79_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_131_SEQUENCE_79_Type_Pattern._CF_pattern.addPattern(pattern='((/(LOANTAX)/(Y|N))?(\\n)?/(GRPREF)/[A-Z]{1,2}[0-9]{1,6}/[0-9]{1,7}(\\n)?/(SLBIND)/(LOAN|RETN|DEPO|WITH)(\\n)?(/(LOANREF)/[A-Z]{1,2}[0-9]{1,6}/[0-9]{1,10})?(\\n)?(/(POOLREF)/[A-Z]{1,2}[0-9]{1,6}/[A-Z0-9]{1,1}/[0-9]{1,10})?)')
MT598_131_SEQUENCE_79_Type_Pattern._InitializeFacetMap(MT598_131_SEQUENCE_79_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_131_SEQUENCE_79_Type_Pattern', MT598_131_SEQUENCE_79_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_131_16R_Type
class MT598_131_16R_Type (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_131_16R_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 175, 1)
    _Documentation = None
MT598_131_16R_Type._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'MT598_131_16R_Type', MT598_131_16R_Type)

# Complex type {http://www.w3schools.com}MT598_131_77E_Type with content type SIMPLE
class MT598_131_77E_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_131_77E_Type with content type SIMPLE"""
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_131_77E_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 16, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.string
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_131_77E_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='77E')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 19, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 19, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT598_131_77E_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 20, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 20, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
Namespace.addCategoryObject('typeBinding', 'MT598_131_77E_Type', MT598_131_77E_Type)


# Complex type {http://www.w3schools.com}MT598_131_12_Type with content type SIMPLE
class MT598_131_12_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_131_12_Type with content type SIMPLE"""
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_131_12_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 154, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.string
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_131_12_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='12')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 157, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 157, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT598_131_12_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 158, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 158, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
Namespace.addCategoryObject('typeBinding', 'MT598_131_12_Type', MT598_131_12_Type)


# Complex type {http://www.w3schools.com}MT598_131_SEQUENCE with content type ELEMENT_ONLY
class MT598_131_SEQUENCE (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_131_SEQUENCE with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_131_SEQUENCE')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 178, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}FurtherIdentification uses Python identifier FurtherIdentification
    __FurtherIdentification = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'FurtherIdentification'), 'FurtherIdentification', '__httpwww_w3schools_com_MT598_131_SEQUENCE_httpwww_w3schools_comFurtherIdentification', False, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 180, 3), )

    
    FurtherIdentification = property(__FurtherIdentification.value, __FurtherIdentification.set, None, None)

    
    # Element {http://www.w3schools.com}SettlementDate uses Python identifier SettlementDate
    __SettlementDate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SettlementDate'), 'SettlementDate', '__httpwww_w3schools_com_MT598_131_SEQUENCE_httpwww_w3schools_comSettlementDate', False, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 181, 3), )

    
    SettlementDate = property(__SettlementDate.value, __SettlementDate.set, None, None)

    
    # Element {http://www.w3schools.com}TradeDate uses Python identifier TradeDate
    __TradeDate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'TradeDate'), 'TradeDate', '__httpwww_w3schools_com_MT598_131_SEQUENCE_httpwww_w3schools_comTradeDate', False, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 182, 3), )

    
    TradeDate = property(__TradeDate.value, __TradeDate.set, None, None)

    
    # Element {http://www.w3schools.com}QuantityOfSecurities uses Python identifier QuantityOfSecurities
    __QuantityOfSecurities = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'QuantityOfSecurities'), 'QuantityOfSecurities', '__httpwww_w3schools_com_MT598_131_SEQUENCE_httpwww_w3schools_comQuantityOfSecurities', False, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 183, 3), )

    
    QuantityOfSecurities = property(__QuantityOfSecurities.value, __QuantityOfSecurities.set, None, None)

    
    # Element {http://www.w3schools.com}IdentificationOfSecurities uses Python identifier IdentificationOfSecurities
    __IdentificationOfSecurities = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'IdentificationOfSecurities'), 'IdentificationOfSecurities', '__httpwww_w3schools_com_MT598_131_SEQUENCE_httpwww_w3schools_comIdentificationOfSecurities', False, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 184, 3), )

    
    IdentificationOfSecurities = property(__IdentificationOfSecurities.value, __IdentificationOfSecurities.set, None, None)

    
    # Element {http://www.w3schools.com}SettlementAmount uses Python identifier SettlementAmount
    __SettlementAmount = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SettlementAmount'), 'SettlementAmount', '__httpwww_w3schools_com_MT598_131_SEQUENCE_httpwww_w3schools_comSettlementAmount', False, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 185, 3), )

    
    SettlementAmount = property(__SettlementAmount.value, __SettlementAmount.set, None, None)

    
    # Element {http://www.w3schools.com}Narrative uses Python identifier Narrative
    __Narrative = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Narrative'), 'Narrative', '__httpwww_w3schools_com_MT598_131_SEQUENCE_httpwww_w3schools_comNarrative', False, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 186, 3), )

    
    Narrative = property(__Narrative.value, __Narrative.set, None, None)

    
    # Element {http://www.w3schools.com}SAFIRESLoanReference uses Python identifier SAFIRESLoanReference
    __SAFIRESLoanReference = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SAFIRESLoanReference'), 'SAFIRESLoanReference', '__httpwww_w3schools_com_MT598_131_SEQUENCE_httpwww_w3schools_comSAFIRESLoanReference', False, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 187, 3), )

    
    SAFIRESLoanReference = property(__SAFIRESLoanReference.value, __SAFIRESLoanReference.set, None, None)

    
    # Element {http://www.w3schools.com}TradingParty uses Python identifier TradingParty
    __TradingParty = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'TradingParty'), 'TradingParty', '__httpwww_w3schools_com_MT598_131_SEQUENCE_httpwww_w3schools_comTradingParty', False, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 188, 3), )

    
    TradingParty = property(__TradingParty.value, __TradingParty.set, None, None)

    
    # Element {http://www.w3schools.com}CounterParty uses Python identifier CounterParty
    __CounterParty = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CounterParty'), 'CounterParty', '__httpwww_w3schools_com_MT598_131_SEQUENCE_httpwww_w3schools_comCounterParty', False, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 189, 3), )

    
    CounterParty = property(__CounterParty.value, __CounterParty.set, None, None)

    _ElementMap.update({
        __FurtherIdentification.name() : __FurtherIdentification,
        __SettlementDate.name() : __SettlementDate,
        __TradeDate.name() : __TradeDate,
        __QuantityOfSecurities.name() : __QuantityOfSecurities,
        __IdentificationOfSecurities.name() : __IdentificationOfSecurities,
        __SettlementAmount.name() : __SettlementAmount,
        __Narrative.name() : __Narrative,
        __SAFIRESLoanReference.name() : __SAFIRESLoanReference,
        __TradingParty.name() : __TradingParty,
        __CounterParty.name() : __CounterParty
    })
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', 'MT598_131_SEQUENCE', MT598_131_SEQUENCE)


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 193, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}TransactionReference uses Python identifier TransactionReference
    __TransactionReference = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'TransactionReference'), 'TransactionReference', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comTransactionReference', False, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 195, 4), )

    
    TransactionReference = property(__TransactionReference.value, __TransactionReference.set, None, None)

    
    # Element {http://www.w3schools.com}SubMessageType uses Python identifier SubMessageType
    __SubMessageType = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SubMessageType'), 'SubMessageType', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comSubMessageType', False, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 196, 4), )

    
    SubMessageType = property(__SubMessageType.value, __SubMessageType.set, None, None)

    
    # Element {http://www.w3schools.com}ProprietaryMessage uses Python identifier ProprietaryMessage
    __ProprietaryMessage = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ProprietaryMessage'), 'ProprietaryMessage', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comProprietaryMessage', False, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 197, 4), )

    
    ProprietaryMessage = property(__ProprietaryMessage.value, __ProprietaryMessage.set, None, None)

    
    # Element {http://www.w3schools.com}SEQUENCE uses Python identifier SEQUENCE
    __SEQUENCE = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SEQUENCE'), 'SEQUENCE', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comSEQUENCE', True, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 198, 4), )

    
    SEQUENCE = property(__SEQUENCE.value, __SEQUENCE.set, None, None)

    
    # Element {http://www.w3schools.com}NumberOfRepetitiveParts uses Python identifier NumberOfRepetitiveParts
    __NumberOfRepetitiveParts = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'NumberOfRepetitiveParts'), 'NumberOfRepetitiveParts', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comNumberOfRepetitiveParts', False, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 199, 4), )

    
    NumberOfRepetitiveParts = property(__NumberOfRepetitiveParts.value, __NumberOfRepetitiveParts.set, None, None)

    _ElementMap.update({
        __TransactionReference.name() : __TransactionReference,
        __SubMessageType.name() : __SubMessageType,
        __ProprietaryMessage.name() : __ProprietaryMessage,
        __SEQUENCE.name() : __SEQUENCE,
        __NumberOfRepetitiveParts.name() : __NumberOfRepetitiveParts
    })
    _AttributeMap.update({
        
    })



# Complex type {http://www.w3schools.com}MT598_131_SEQUENCE_30P_Type with content type SIMPLE
class MT598_131_SEQUENCE_30P_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_131_SEQUENCE_30P_Type with content type SIMPLE"""
    _TypeDefinition = MT598_131_SEQUENCE_30P_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_131_SEQUENCE_30P_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 8, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_131_SEQUENCE_30P_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_131_SEQUENCE_30P_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='30P')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 11, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 11, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT598_131_SEQUENCE_30P_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 12, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 12, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
Namespace.addCategoryObject('typeBinding', 'MT598_131_SEQUENCE_30P_Type', MT598_131_SEQUENCE_30P_Type)


# Complex type {http://www.w3schools.com}MT598_131_18A_Type with content type SIMPLE
class MT598_131_18A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_131_18A_Type with content type SIMPLE"""
    _TypeDefinition = MT598_131_18A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_131_18A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 29, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_131_18A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_131_18A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='18A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 32, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 32, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT598_131_18A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 33, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 33, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
Namespace.addCategoryObject('typeBinding', 'MT598_131_18A_Type', MT598_131_18A_Type)


# Complex type {http://www.w3schools.com}MT598_131_SEQUENCE_82B_Type with content type SIMPLE
class MT598_131_SEQUENCE_82B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_131_SEQUENCE_82B_Type with content type SIMPLE"""
    _TypeDefinition = MT598_131_SEQUENCE_82B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_131_SEQUENCE_82B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 42, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_131_SEQUENCE_82B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_131_SEQUENCE_82B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='82B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 45, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 45, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT598_131_SEQUENCE_82B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 46, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 46, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
Namespace.addCategoryObject('typeBinding', 'MT598_131_SEQUENCE_82B_Type', MT598_131_SEQUENCE_82B_Type)


# Complex type {http://www.w3schools.com}MT598_131_20_Type with content type SIMPLE
class MT598_131_20_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_131_20_Type with content type SIMPLE"""
    _TypeDefinition = MT598_131_20_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_131_20_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 55, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_131_20_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_131_20_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='20')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 58, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 58, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT598_131_20_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 59, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 59, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
Namespace.addCategoryObject('typeBinding', 'MT598_131_20_Type', MT598_131_20_Type)


# Complex type {http://www.w3schools.com}MT598_131_SEQUENCE_35A_Type with content type SIMPLE
class MT598_131_SEQUENCE_35A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_131_SEQUENCE_35A_Type with content type SIMPLE"""
    _TypeDefinition = MT598_131_SEQUENCE_35A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_131_SEQUENCE_35A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 68, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_131_SEQUENCE_35A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_131_SEQUENCE_35A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='35A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 71, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 71, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT598_131_SEQUENCE_35A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 72, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 72, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
Namespace.addCategoryObject('typeBinding', 'MT598_131_SEQUENCE_35A_Type', MT598_131_SEQUENCE_35A_Type)


# Complex type {http://www.w3schools.com}MT598_131_SEQUENCE_26H_Type with content type SIMPLE
class MT598_131_SEQUENCE_26H_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_131_SEQUENCE_26H_Type with content type SIMPLE"""
    _TypeDefinition = MT598_131_SEQUENCE_26H_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_131_SEQUENCE_26H_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 81, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_131_SEQUENCE_26H_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_131_SEQUENCE_26H_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='26H')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 84, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 84, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT598_131_SEQUENCE_26H_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 85, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 85, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
Namespace.addCategoryObject('typeBinding', 'MT598_131_SEQUENCE_26H_Type', MT598_131_SEQUENCE_26H_Type)


# Complex type {http://www.w3schools.com}MT598_131_SEQUENCE_87C_Type with content type SIMPLE
class MT598_131_SEQUENCE_87C_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_131_SEQUENCE_87C_Type with content type SIMPLE"""
    _TypeDefinition = MT598_131_SEQUENCE_87C_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_131_SEQUENCE_87C_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 94, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_131_SEQUENCE_87C_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_131_SEQUENCE_87C_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='87C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 97, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 97, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT598_131_SEQUENCE_87C_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 98, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 98, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
Namespace.addCategoryObject('typeBinding', 'MT598_131_SEQUENCE_87C_Type', MT598_131_SEQUENCE_87C_Type)


# Complex type {http://www.w3schools.com}MT598_131_SEQUENCE_35B_Type with content type SIMPLE
class MT598_131_SEQUENCE_35B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_131_SEQUENCE_35B_Type with content type SIMPLE"""
    _TypeDefinition = MT598_131_SEQUENCE_35B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_131_SEQUENCE_35B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 107, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_131_SEQUENCE_35B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_131_SEQUENCE_35B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='35B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 110, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 110, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT598_131_SEQUENCE_35B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 111, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 111, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
Namespace.addCategoryObject('typeBinding', 'MT598_131_SEQUENCE_35B_Type', MT598_131_SEQUENCE_35B_Type)


# Complex type {http://www.w3schools.com}MT598_131_SEQUENCE_30F_Type with content type SIMPLE
class MT598_131_SEQUENCE_30F_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_131_SEQUENCE_30F_Type with content type SIMPLE"""
    _TypeDefinition = MT598_131_SEQUENCE_30F_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_131_SEQUENCE_30F_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 120, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_131_SEQUENCE_30F_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_131_SEQUENCE_30F_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='30F')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 123, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 123, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT598_131_SEQUENCE_30F_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 124, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 124, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
Namespace.addCategoryObject('typeBinding', 'MT598_131_SEQUENCE_30F_Type', MT598_131_SEQUENCE_30F_Type)


# Complex type {http://www.w3schools.com}MT598_131_SEQUENCE_23_Type with content type SIMPLE
class MT598_131_SEQUENCE_23_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_131_SEQUENCE_23_Type with content type SIMPLE"""
    _TypeDefinition = MT598_131_SEQUENCE_23_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_131_SEQUENCE_23_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 133, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_131_SEQUENCE_23_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_131_SEQUENCE_23_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='23')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 136, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 136, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT598_131_SEQUENCE_23_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 137, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 137, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
Namespace.addCategoryObject('typeBinding', 'MT598_131_SEQUENCE_23_Type', MT598_131_SEQUENCE_23_Type)


# Complex type {http://www.w3schools.com}MT598_131_SEQUENCE_32B_Type with content type SIMPLE
class MT598_131_SEQUENCE_32B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_131_SEQUENCE_32B_Type with content type SIMPLE"""
    _TypeDefinition = MT598_131_SEQUENCE_32B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_131_SEQUENCE_32B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 146, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_131_SEQUENCE_32B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_131_SEQUENCE_32B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='32B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 149, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 149, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT598_131_SEQUENCE_32B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 150, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 150, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
Namespace.addCategoryObject('typeBinding', 'MT598_131_SEQUENCE_32B_Type', MT598_131_SEQUENCE_32B_Type)


# Complex type {http://www.w3schools.com}MT598_131_SEQUENCE_79_Type with content type SIMPLE
class MT598_131_SEQUENCE_79_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_131_SEQUENCE_79_Type with content type SIMPLE"""
    _TypeDefinition = MT598_131_SEQUENCE_79_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_131_SEQUENCE_79_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 167, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_131_SEQUENCE_79_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_131_SEQUENCE_79_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='79')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 170, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 170, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT598_131_SEQUENCE_79_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 171, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 171, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
Namespace.addCategoryObject('typeBinding', 'MT598_131_SEQUENCE_79_Type', MT598_131_SEQUENCE_79_Type)


MT598_131 = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'MT598_131'), CTD_ANON, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 192, 1))
Namespace.addCategoryObject('elementBinding', MT598_131.name().localName(), MT598_131)



MT598_131_SEQUENCE._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'FurtherIdentification'), MT598_131_SEQUENCE_23_Type, scope=MT598_131_SEQUENCE, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 180, 3)))

MT598_131_SEQUENCE._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SettlementDate'), MT598_131_SEQUENCE_30F_Type, scope=MT598_131_SEQUENCE, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 181, 3)))

MT598_131_SEQUENCE._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TradeDate'), MT598_131_SEQUENCE_30P_Type, scope=MT598_131_SEQUENCE, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 182, 3)))

MT598_131_SEQUENCE._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'QuantityOfSecurities'), MT598_131_SEQUENCE_35A_Type, scope=MT598_131_SEQUENCE, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 183, 3)))

MT598_131_SEQUENCE._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'IdentificationOfSecurities'), MT598_131_SEQUENCE_35B_Type, scope=MT598_131_SEQUENCE, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 184, 3)))

MT598_131_SEQUENCE._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SettlementAmount'), MT598_131_SEQUENCE_32B_Type, scope=MT598_131_SEQUENCE, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 185, 3)))

MT598_131_SEQUENCE._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Narrative'), MT598_131_SEQUENCE_79_Type, scope=MT598_131_SEQUENCE, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 186, 3)))

MT598_131_SEQUENCE._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SAFIRESLoanReference'), MT598_131_SEQUENCE_26H_Type, scope=MT598_131_SEQUENCE, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 187, 3)))

MT598_131_SEQUENCE._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TradingParty'), MT598_131_SEQUENCE_82B_Type, scope=MT598_131_SEQUENCE, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 188, 3)))

MT598_131_SEQUENCE._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CounterParty'), MT598_131_SEQUENCE_87C_Type, scope=MT598_131_SEQUENCE, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 189, 3)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 185, 3))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT598_131_SEQUENCE._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'FurtherIdentification')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 180, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT598_131_SEQUENCE._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SettlementDate')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 181, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT598_131_SEQUENCE._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'TradeDate')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 182, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT598_131_SEQUENCE._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'QuantityOfSecurities')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 183, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT598_131_SEQUENCE._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'IdentificationOfSecurities')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 184, 3))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT598_131_SEQUENCE._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SettlementAmount')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 185, 3))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT598_131_SEQUENCE._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Narrative')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 186, 3))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT598_131_SEQUENCE._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SAFIRESLoanReference')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 187, 3))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT598_131_SEQUENCE._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'TradingParty')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 188, 3))
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT598_131_SEQUENCE._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CounterParty')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 189, 3))
    st_9 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
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
    transitions.append(fac.Transition(st_6, [
         ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
         ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
         ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_9, [
         ]))
    st_8._set_transitionSet(transitions)
    transitions = []
    st_9._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
MT598_131_SEQUENCE._Automaton = _BuildAutomaton()




CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TransactionReference'), MT598_131_20_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 195, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SubMessageType'), MT598_131_12_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 196, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ProprietaryMessage'), MT598_131_77E_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 197, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SEQUENCE'), MT598_131_SEQUENCE, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 198, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'NumberOfRepetitiveParts'), MT598_131_18A_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 199, 4)))

def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'TransactionReference')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 195, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SubMessageType')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 196, 4))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ProprietaryMessage')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 197, 4))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SEQUENCE')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 198, 4))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'NumberOfRepetitiveParts')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_131.xsd', 199, 4))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
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
    transitions.append(fac.Transition(st_4, [
         ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    st_4._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON._Automaton = _BuildAutomaton_()


