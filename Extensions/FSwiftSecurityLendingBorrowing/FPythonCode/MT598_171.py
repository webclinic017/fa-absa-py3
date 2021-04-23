# C:\SWIFT\SwiftReader\XSD\MT598_171.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:96afad3d20bbfe8d040a1a097fa388d9fecd10e3
# Generated 2017-02-16 17:34:45.821000 by PyXB version 1.2.2
# Namespace http://www.w3schools.com

import pyxb
import pyxb.binding
import pyxb.binding.saxer
import StringIO
import pyxb.utils.utility
import pyxb.utils.domutils
import sys

# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:1b6de50f-f440-11e6-8701-180373dbbcdf')

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


# Atomic simple type: {http://www.w3schools.com}MT598_171_BANDET_36B_Type_Pattern
class MT598_171_BANDET_36B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_171_BANDET_36B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 3, 1)
    _Documentation = None
MT598_171_BANDET_36B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_171_BANDET_36B_Type_Pattern._CF_pattern.addPattern(pattern='(:(SETT)//FAMT/[0-9]{1,12},([0-9]{1,2})*)')
MT598_171_BANDET_36B_Type_Pattern._InitializeFacetMap(MT598_171_BANDET_36B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_171_BANDET_36B_Type_Pattern', MT598_171_BANDET_36B_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_171_GENL_LINK_20C_Type_Pattern
class MT598_171_GENL_LINK_20C_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_171_GENL_LINK_20C_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 15, 1)
    _Documentation = None
MT598_171_GENL_LINK_20C_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_171_GENL_LINK_20C_Type_Pattern._CF_pattern.addPattern(pattern='(:(RELA)//[A-Z]{2}[0-9]{6}/[0-9]{1,7}|:(UTRN)//.{6})')
MT598_171_GENL_LINK_20C_Type_Pattern._InitializeFacetMap(MT598_171_GENL_LINK_20C_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_171_GENL_LINK_20C_Type_Pattern', MT598_171_GENL_LINK_20C_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_171_BANDET_97B_Type_Pattern
class MT598_171_BANDET_97B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_171_BANDET_97B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 27, 1)
    _Documentation = None
MT598_171_BANDET_97B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_171_BANDET_97B_Type_Pattern._CF_pattern.addPattern(pattern='(:(SAFE)/STRA/IORT/[0-9]{8})')
MT598_171_BANDET_97B_Type_Pattern._InitializeFacetMap(MT598_171_BANDET_97B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_171_BANDET_97B_Type_Pattern', MT598_171_BANDET_97B_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_171_BANDET_19A_Type_Pattern
class MT598_171_BANDET_19A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_171_BANDET_19A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 39, 1)
    _Documentation = None
MT598_171_BANDET_19A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_171_BANDET_19A_Type_Pattern._CF_pattern.addPattern(pattern='(:(SETT)//(N)?[A-Z]{3}[0-9]{1,12},([0-9]{1,2})*)')
MT598_171_BANDET_19A_Type_Pattern._InitializeFacetMap(MT598_171_BANDET_19A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_171_BANDET_19A_Type_Pattern', MT598_171_BANDET_19A_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_171_20_Type_Pattern
class MT598_171_20_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_171_20_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 51, 1)
    _Documentation = None
MT598_171_20_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_171_20_Type_Pattern._CF_pattern.addPattern(pattern='(.{1,16})')
MT598_171_20_Type_Pattern._InitializeFacetMap(MT598_171_20_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_171_20_Type_Pattern', MT598_171_20_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_171_BANDET_20C_Type_Pattern
class MT598_171_BANDET_20C_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_171_BANDET_20C_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 63, 1)
    _Documentation = None
MT598_171_BANDET_20C_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_171_BANDET_20C_Type_Pattern._CF_pattern.addPattern(pattern='(:(BANN)//.{9})')
MT598_171_BANDET_20C_Type_Pattern._InitializeFacetMap(MT598_171_BANDET_20C_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_171_BANDET_20C_Type_Pattern', MT598_171_BANDET_20C_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_171_GENL_98C_Type_Pattern
class MT598_171_GENL_98C_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_171_GENL_98C_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 82, 1)
    _Documentation = None
MT598_171_GENL_98C_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_171_GENL_98C_Type_Pattern._CF_pattern.addPattern(pattern='(:(PREP)//[0-9]{8}[0-9]{6})')
MT598_171_GENL_98C_Type_Pattern._InitializeFacetMap(MT598_171_GENL_98C_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_171_GENL_98C_Type_Pattern', MT598_171_GENL_98C_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_171_GENL_23G_Type_Pattern
class MT598_171_GENL_23G_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_171_GENL_23G_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 101, 1)
    _Documentation = None
MT598_171_GENL_23G_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_171_GENL_23G_Type_Pattern._CF_pattern.addPattern(pattern='((NEWM))')
MT598_171_GENL_23G_Type_Pattern._InitializeFacetMap(MT598_171_GENL_23G_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_171_GENL_23G_Type_Pattern', MT598_171_GENL_23G_Type_Pattern)

# Complex type {http://www.w3schools.com}MT598_171_12_Type with content type SIMPLE
class MT598_171_12_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_171_12_Type with content type SIMPLE"""
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_171_12_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 75, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.string
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_171_12_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='12')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 78, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 78, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_171_12_Type', MT598_171_12_Type)


# Complex type {http://www.w3schools.com}MT598_171_77E_Type with content type SIMPLE
class MT598_171_77E_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_171_77E_Type with content type SIMPLE"""
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_171_77E_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 94, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.string
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_171_77E_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='77E')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 97, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 97, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_171_77E_Type', MT598_171_77E_Type)


# Complex type {http://www.w3schools.com}MT598_171_GENL_LINK with content type ELEMENT_ONLY
class MT598_171_GENL_LINK (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_171_GENL_LINK with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_171_GENL_LINK')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 113, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}InternalTrdRef_UTI uses Python identifier InternalTrdRef_UTI
    __InternalTrdRef_UTI = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'InternalTrdRef_UTI'), 'InternalTrdRef_UTI', '__httpwww_w3schools_com_MT598_171_GENL_LINK_httpwww_w3schools_comInternalTrdRef_UTI', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 115, 3), )

    
    InternalTrdRef_UTI = property(__InternalTrdRef_UTI.value, __InternalTrdRef_UTI.set, None, None)

    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_171_GENL_LINK_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='16R')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 117, 2)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 117, 2)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        __InternalTrdRef_UTI.name() : __InternalTrdRef_UTI
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_171_GENL_LINK', MT598_171_GENL_LINK)


# Complex type {http://www.w3schools.com}MT598_171_GENL with content type ELEMENT_ONLY
class MT598_171_GENL (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_171_GENL with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_171_GENL')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 119, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}FunctionOfMessage uses Python identifier FunctionOfMessage
    __FunctionOfMessage = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'FunctionOfMessage'), 'FunctionOfMessage', '__httpwww_w3schools_com_MT598_171_GENL_httpwww_w3schools_comFunctionOfMessage', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 121, 3), )

    
    FunctionOfMessage = property(__FunctionOfMessage.value, __FunctionOfMessage.set, None, None)

    
    # Element {http://www.w3schools.com}PreparationDateAndTime uses Python identifier PreparationDateAndTime
    __PreparationDateAndTime = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PreparationDateAndTime'), 'PreparationDateAndTime', '__httpwww_w3schools_com_MT598_171_GENL_httpwww_w3schools_comPreparationDateAndTime', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 122, 3), )

    
    PreparationDateAndTime = property(__PreparationDateAndTime.value, __PreparationDateAndTime.set, None, None)

    
    # Element {http://www.w3schools.com}LINK uses Python identifier LINK
    __LINK = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'LINK'), 'LINK', '__httpwww_w3schools_com_MT598_171_GENL_httpwww_w3schools_comLINK', True, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 123, 3), )

    
    LINK = property(__LINK.value, __LINK.set, None, None)

    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_171_GENL_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='16R')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 125, 2)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 125, 2)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        __FunctionOfMessage.name() : __FunctionOfMessage,
        __PreparationDateAndTime.name() : __PreparationDateAndTime,
        __LINK.name() : __LINK
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_171_GENL', MT598_171_GENL)


# Complex type {http://www.w3schools.com}MT598_171_BANDET with content type ELEMENT_ONLY
class MT598_171_BANDET (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_171_BANDET with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_171_BANDET')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 127, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}BANReference uses Python identifier BANReference
    __BANReference = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'BANReference'), 'BANReference', '__httpwww_w3schools_com_MT598_171_BANDET_httpwww_w3schools_comBANReference', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 129, 3), )

    
    BANReference = property(__BANReference.value, __BANReference.set, None, None)

    
    # Element {http://www.w3schools.com}SORAccount uses Python identifier SORAccount
    __SORAccount = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SORAccount'), 'SORAccount', '__httpwww_w3schools_com_MT598_171_BANDET_httpwww_w3schools_comSORAccount', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 130, 3), )

    
    SORAccount = property(__SORAccount.value, __SORAccount.set, None, None)

    
    # Element {http://www.w3schools.com}NominalValue uses Python identifier NominalValue
    __NominalValue = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'NominalValue'), 'NominalValue', '__httpwww_w3schools_com_MT598_171_BANDET_httpwww_w3schools_comNominalValue', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 131, 3), )

    
    NominalValue = property(__NominalValue.value, __NominalValue.set, None, None)

    
    # Element {http://www.w3schools.com}SettlementAmount uses Python identifier SettlementAmount
    __SettlementAmount = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SettlementAmount'), 'SettlementAmount', '__httpwww_w3schools_com_MT598_171_BANDET_httpwww_w3schools_comSettlementAmount', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 132, 3), )

    
    SettlementAmount = property(__SettlementAmount.value, __SettlementAmount.set, None, None)

    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_171_BANDET_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='16R')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 134, 2)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 134, 2)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        __BANReference.name() : __BANReference,
        __SORAccount.name() : __SORAccount,
        __NominalValue.name() : __NominalValue,
        __SettlementAmount.name() : __SettlementAmount
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_171_BANDET', MT598_171_BANDET)


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 137, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}TransactionReference uses Python identifier TransactionReference
    __TransactionReference = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'TransactionReference'), 'TransactionReference', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comTransactionReference', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 139, 4), )

    
    TransactionReference = property(__TransactionReference.value, __TransactionReference.set, None, None)

    
    # Element {http://www.w3schools.com}SubMessageType uses Python identifier SubMessageType
    __SubMessageType = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SubMessageType'), 'SubMessageType', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comSubMessageType', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 140, 4), )

    
    SubMessageType = property(__SubMessageType.value, __SubMessageType.set, None, None)

    
    # Element {http://www.w3schools.com}ProprietaryMessage uses Python identifier ProprietaryMessage
    __ProprietaryMessage = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ProprietaryMessage'), 'ProprietaryMessage', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comProprietaryMessage', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 141, 4), )

    
    ProprietaryMessage = property(__ProprietaryMessage.value, __ProprietaryMessage.set, None, None)

    
    # Element {http://www.w3schools.com}GENL uses Python identifier GENL
    __GENL = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'GENL'), 'GENL', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comGENL', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 142, 4), )

    
    GENL = property(__GENL.value, __GENL.set, None, None)

    
    # Element {http://www.w3schools.com}BANDET uses Python identifier BANDET
    __BANDET = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'BANDET'), 'BANDET', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comBANDET', True, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 143, 4), )

    
    BANDET = property(__BANDET.value, __BANDET.set, None, None)

    _ElementMap.update({
        __TransactionReference.name() : __TransactionReference,
        __SubMessageType.name() : __SubMessageType,
        __ProprietaryMessage.name() : __ProprietaryMessage,
        __GENL.name() : __GENL,
        __BANDET.name() : __BANDET
    })
    _AttributeMap.update({
        
    })



# Complex type {http://www.w3schools.com}MT598_171_BANDET_36B_Type with content type SIMPLE
class MT598_171_BANDET_36B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_171_BANDET_36B_Type with content type SIMPLE"""
    _TypeDefinition = MT598_171_BANDET_36B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_171_BANDET_36B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 8, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_171_BANDET_36B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_171_BANDET_36B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='36B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 11, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 11, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_171_BANDET_36B_Type', MT598_171_BANDET_36B_Type)


# Complex type {http://www.w3schools.com}MT598_171_GENL_LINK_20C_Type with content type SIMPLE
class MT598_171_GENL_LINK_20C_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_171_GENL_LINK_20C_Type with content type SIMPLE"""
    _TypeDefinition = MT598_171_GENL_LINK_20C_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_171_GENL_LINK_20C_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 20, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_171_GENL_LINK_20C_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_171_GENL_LINK_20C_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='20C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 23, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 23, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_171_GENL_LINK_20C_Type', MT598_171_GENL_LINK_20C_Type)


# Complex type {http://www.w3schools.com}MT598_171_BANDET_97B_Type with content type SIMPLE
class MT598_171_BANDET_97B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_171_BANDET_97B_Type with content type SIMPLE"""
    _TypeDefinition = MT598_171_BANDET_97B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_171_BANDET_97B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 32, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_171_BANDET_97B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_171_BANDET_97B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='97B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 35, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 35, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_171_BANDET_97B_Type', MT598_171_BANDET_97B_Type)


# Complex type {http://www.w3schools.com}MT598_171_BANDET_19A_Type with content type SIMPLE
class MT598_171_BANDET_19A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_171_BANDET_19A_Type with content type SIMPLE"""
    _TypeDefinition = MT598_171_BANDET_19A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_171_BANDET_19A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 44, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_171_BANDET_19A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_171_BANDET_19A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='19A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 47, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 47, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_171_BANDET_19A_Type', MT598_171_BANDET_19A_Type)


# Complex type {http://www.w3schools.com}MT598_171_20_Type with content type SIMPLE
class MT598_171_20_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_171_20_Type with content type SIMPLE"""
    _TypeDefinition = MT598_171_20_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_171_20_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 56, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_171_20_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_171_20_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='20')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 59, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 59, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_171_20_Type', MT598_171_20_Type)


# Complex type {http://www.w3schools.com}MT598_171_BANDET_20C_Type with content type SIMPLE
class MT598_171_BANDET_20C_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_171_BANDET_20C_Type with content type SIMPLE"""
    _TypeDefinition = MT598_171_BANDET_20C_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_171_BANDET_20C_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 68, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_171_BANDET_20C_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_171_BANDET_20C_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='20C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 71, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 71, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_171_BANDET_20C_Type', MT598_171_BANDET_20C_Type)


# Complex type {http://www.w3schools.com}MT598_171_GENL_98C_Type with content type SIMPLE
class MT598_171_GENL_98C_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_171_GENL_98C_Type with content type SIMPLE"""
    _TypeDefinition = MT598_171_GENL_98C_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_171_GENL_98C_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 87, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_171_GENL_98C_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_171_GENL_98C_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='98C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 90, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 90, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_171_GENL_98C_Type', MT598_171_GENL_98C_Type)


# Complex type {http://www.w3schools.com}MT598_171_GENL_23G_Type with content type SIMPLE
class MT598_171_GENL_23G_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_171_GENL_23G_Type with content type SIMPLE"""
    _TypeDefinition = MT598_171_GENL_23G_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_171_GENL_23G_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 106, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_171_GENL_23G_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_171_GENL_23G_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='23G')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 109, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 109, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_171_GENL_23G_Type', MT598_171_GENL_23G_Type)


MT598_171 = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'MT598_171'), CTD_ANON, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 136, 1))
Namespace.addCategoryObject('elementBinding', MT598_171.name().localName(), MT598_171)



MT598_171_GENL_LINK._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'InternalTrdRef_UTI'), MT598_171_GENL_LINK_20C_Type, scope=MT598_171_GENL_LINK, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 115, 3)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT598_171_GENL_LINK._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'InternalTrdRef_UTI')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 115, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
MT598_171_GENL_LINK._Automaton = _BuildAutomaton()




MT598_171_GENL._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'FunctionOfMessage'), MT598_171_GENL_23G_Type, scope=MT598_171_GENL, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 121, 3)))

MT598_171_GENL._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PreparationDateAndTime'), MT598_171_GENL_98C_Type, scope=MT598_171_GENL, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 122, 3)))

MT598_171_GENL._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'LINK'), MT598_171_GENL_LINK, scope=MT598_171_GENL, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 123, 3)))

def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT598_171_GENL._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'FunctionOfMessage')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 121, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT598_171_GENL._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PreparationDateAndTime')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 122, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT598_171_GENL._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'LINK')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 123, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
MT598_171_GENL._Automaton = _BuildAutomaton_()




MT598_171_BANDET._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'BANReference'), MT598_171_BANDET_20C_Type, scope=MT598_171_BANDET, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 129, 3)))

MT598_171_BANDET._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SORAccount'), MT598_171_BANDET_97B_Type, scope=MT598_171_BANDET, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 130, 3)))

MT598_171_BANDET._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'NominalValue'), MT598_171_BANDET_36B_Type, scope=MT598_171_BANDET, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 131, 3)))

MT598_171_BANDET._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SettlementAmount'), MT598_171_BANDET_19A_Type, scope=MT598_171_BANDET, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 132, 3)))

def _BuildAutomaton_2 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_2
    del _BuildAutomaton_2
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 132, 3))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT598_171_BANDET._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'BANReference')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 129, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT598_171_BANDET._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SORAccount')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 130, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT598_171_BANDET._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'NominalValue')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 131, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(MT598_171_BANDET._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SettlementAmount')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 132, 3))
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
        fac.UpdateInstruction(cc_0, True) ]))
    st_3._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
MT598_171_BANDET._Automaton = _BuildAutomaton_2()




CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TransactionReference'), MT598_171_20_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 139, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SubMessageType'), MT598_171_12_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 140, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ProprietaryMessage'), MT598_171_77E_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 141, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'GENL'), MT598_171_GENL, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 142, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'BANDET'), MT598_171_BANDET, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 143, 4)))

def _BuildAutomaton_3 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_3
    del _BuildAutomaton_3
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'TransactionReference')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 139, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SubMessageType')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 140, 4))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ProprietaryMessage')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 141, 4))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'GENL')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 142, 4))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'BANDET')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_171.xsd', 143, 4))
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
    transitions.append(fac.Transition(st_4, [
         ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
         ]))
    st_4._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON._Automaton = _BuildAutomaton_3()


