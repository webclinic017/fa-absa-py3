# C:\SWIFT\SwiftReader\XSD\MT598_902.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:96afad3d20bbfe8d040a1a097fa388d9fecd10e3
# Generated 2017-02-16 17:37:53.404000 by PyXB version 1.2.2
# Namespace http://www.w3schools.com

import pyxb
import pyxb.binding
import pyxb.binding.saxer
import StringIO
import pyxb.utils.utility
import pyxb.utils.domutils
import sys

# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:8b4380c0-f440-11e6-a659-180373dbbcdf')

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


# Atomic simple type: {http://www.w3schools.com}MT598_902_GENL_35B_Type_Pattern
class MT598_902_GENL_35B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_902_GENL_35B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_902.xsd', 3, 1)
    _Documentation = None
MT598_902_GENL_35B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_902_GENL_35B_Type_Pattern._CF_pattern.addPattern(pattern='(ISIN {1}[A-Z0-9]{12})')
MT598_902_GENL_35B_Type_Pattern._InitializeFacetMap(MT598_902_GENL_35B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_902_GENL_35B_Type_Pattern', MT598_902_GENL_35B_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_902_GENL_70D_Type_Pattern
class MT598_902_GENL_70D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_902_GENL_70D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_902.xsd', 15, 1)
    _Documentation = None
MT598_902_GENL_70D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_902_GENL_70D_Type_Pattern._CF_pattern.addPattern(pattern='(:(EROR)//.{4}/.{4}/.{4}/.{4}/.{4})')
MT598_902_GENL_70D_Type_Pattern._InitializeFacetMap(MT598_902_GENL_70D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_902_GENL_70D_Type_Pattern', MT598_902_GENL_70D_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_902_20_Type_Pattern
class MT598_902_20_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_902_20_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_902.xsd', 41, 1)
    _Documentation = None
MT598_902_20_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_902_20_Type_Pattern._CF_pattern.addPattern(pattern='(.{1,16})')
MT598_902_20_Type_Pattern._InitializeFacetMap(MT598_902_20_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_902_20_Type_Pattern', MT598_902_20_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_902_GENL_20C_Type_Pattern
class MT598_902_GENL_20C_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_902_GENL_20C_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_902.xsd', 53, 1)
    _Documentation = None
MT598_902_GENL_20C_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_902_GENL_20C_Type_Pattern._CF_pattern.addPattern(pattern='(:(RELA)//.{1,16})')
MT598_902_GENL_20C_Type_Pattern._InitializeFacetMap(MT598_902_GENL_20C_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_902_GENL_20C_Type_Pattern', MT598_902_GENL_20C_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_902_GENL_98C_Type_Pattern
class MT598_902_GENL_98C_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_902_GENL_98C_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_902.xsd', 65, 1)
    _Documentation = None
MT598_902_GENL_98C_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_902_GENL_98C_Type_Pattern._CF_pattern.addPattern(pattern='(:(PREP)//[0-9]{8}[0-9]{6})')
MT598_902_GENL_98C_Type_Pattern._InitializeFacetMap(MT598_902_GENL_98C_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_902_GENL_98C_Type_Pattern', MT598_902_GENL_98C_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_902_16R_Type
class MT598_902_16R_Type (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_902_16R_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_902.xsd', 77, 1)
    _Documentation = None
MT598_902_16R_Type._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'MT598_902_16R_Type', MT598_902_16R_Type)

# Complex type {http://www.w3schools.com}MT598_902_77E_Type with content type SIMPLE
class MT598_902_77E_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_902_77E_Type with content type SIMPLE"""
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_902_77E_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_902.xsd', 27, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.string
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_902_77E_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='77E')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_902.xsd', 30, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_902.xsd', 30, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_902_77E_Type', MT598_902_77E_Type)


# Complex type {http://www.w3schools.com}MT598_902_12_Type with content type SIMPLE
class MT598_902_12_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_902_12_Type with content type SIMPLE"""
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_902_12_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_902.xsd', 34, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.string
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_902_12_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='12')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_902.xsd', 37, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_902.xsd', 37, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_902_12_Type', MT598_902_12_Type)


# Complex type {http://www.w3schools.com}MT598_902_GENL with content type ELEMENT_ONLY
class MT598_902_GENL (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_902_GENL with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_902_GENL')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_902.xsd', 80, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}RelatedReference uses Python identifier RelatedReference
    __RelatedReference = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'RelatedReference'), 'RelatedReference', '__httpwww_w3schools_com_MT598_902_GENL_httpwww_w3schools_comRelatedReference', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_902.xsd', 82, 3), )

    
    RelatedReference = property(__RelatedReference.value, __RelatedReference.set, None, None)

    
    # Element {http://www.w3schools.com}PreparationDateAndTime uses Python identifier PreparationDateAndTime
    __PreparationDateAndTime = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PreparationDateAndTime'), 'PreparationDateAndTime', '__httpwww_w3schools_com_MT598_902_GENL_httpwww_w3schools_comPreparationDateAndTime', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_902.xsd', 83, 3), )

    
    PreparationDateAndTime = property(__PreparationDateAndTime.value, __PreparationDateAndTime.set, None, None)

    
    # Element {http://www.w3schools.com}IdentificationOfSecurity uses Python identifier IdentificationOfSecurity
    __IdentificationOfSecurity = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'IdentificationOfSecurity'), 'IdentificationOfSecurity', '__httpwww_w3schools_com_MT598_902_GENL_httpwww_w3schools_comIdentificationOfSecurity', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_902.xsd', 84, 3), )

    
    IdentificationOfSecurity = property(__IdentificationOfSecurity.value, __IdentificationOfSecurity.set, None, None)

    
    # Element {http://www.w3schools.com}ErrorDetails uses Python identifier ErrorDetails
    __ErrorDetails = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ErrorDetails'), 'ErrorDetails', '__httpwww_w3schools_com_MT598_902_GENL_httpwww_w3schools_comErrorDetails', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_902.xsd', 85, 3), )

    
    ErrorDetails = property(__ErrorDetails.value, __ErrorDetails.set, None, None)

    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_902_GENL_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='16R')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_902.xsd', 87, 2)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_902.xsd', 87, 2)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        __RelatedReference.name() : __RelatedReference,
        __PreparationDateAndTime.name() : __PreparationDateAndTime,
        __IdentificationOfSecurity.name() : __IdentificationOfSecurity,
        __ErrorDetails.name() : __ErrorDetails
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_902_GENL', MT598_902_GENL)


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_902.xsd', 90, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}TransactionReference uses Python identifier TransactionReference
    __TransactionReference = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'TransactionReference'), 'TransactionReference', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comTransactionReference', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_902.xsd', 92, 4), )

    
    TransactionReference = property(__TransactionReference.value, __TransactionReference.set, None, None)

    
    # Element {http://www.w3schools.com}SubMessageType uses Python identifier SubMessageType
    __SubMessageType = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SubMessageType'), 'SubMessageType', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comSubMessageType', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_902.xsd', 93, 4), )

    
    SubMessageType = property(__SubMessageType.value, __SubMessageType.set, None, None)

    
    # Element {http://www.w3schools.com}ProprietaryMessage uses Python identifier ProprietaryMessage
    __ProprietaryMessage = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ProprietaryMessage'), 'ProprietaryMessage', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comProprietaryMessage', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_902.xsd', 94, 4), )

    
    ProprietaryMessage = property(__ProprietaryMessage.value, __ProprietaryMessage.set, None, None)

    
    # Element {http://www.w3schools.com}GENL uses Python identifier GENL
    __GENL = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'GENL'), 'GENL', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comGENL', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_902.xsd', 95, 4), )

    
    GENL = property(__GENL.value, __GENL.set, None, None)

    _ElementMap.update({
        __TransactionReference.name() : __TransactionReference,
        __SubMessageType.name() : __SubMessageType,
        __ProprietaryMessage.name() : __ProprietaryMessage,
        __GENL.name() : __GENL
    })
    _AttributeMap.update({
        
    })



# Complex type {http://www.w3schools.com}MT598_902_GENL_35B_Type with content type SIMPLE
class MT598_902_GENL_35B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_902_GENL_35B_Type with content type SIMPLE"""
    _TypeDefinition = MT598_902_GENL_35B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_902_GENL_35B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_902.xsd', 8, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_902_GENL_35B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_902_GENL_35B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='35B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_902.xsd', 11, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_902.xsd', 11, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_902_GENL_35B_Type', MT598_902_GENL_35B_Type)


# Complex type {http://www.w3schools.com}MT598_902_GENL_70D_Type with content type SIMPLE
class MT598_902_GENL_70D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_902_GENL_70D_Type with content type SIMPLE"""
    _TypeDefinition = MT598_902_GENL_70D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_902_GENL_70D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_902.xsd', 20, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_902_GENL_70D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_902_GENL_70D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='70D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_902.xsd', 23, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_902.xsd', 23, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_902_GENL_70D_Type', MT598_902_GENL_70D_Type)


# Complex type {http://www.w3schools.com}MT598_902_20_Type with content type SIMPLE
class MT598_902_20_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_902_20_Type with content type SIMPLE"""
    _TypeDefinition = MT598_902_20_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_902_20_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_902.xsd', 46, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_902_20_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_902_20_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='20')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_902.xsd', 49, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_902.xsd', 49, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_902_20_Type', MT598_902_20_Type)


# Complex type {http://www.w3schools.com}MT598_902_GENL_20C_Type with content type SIMPLE
class MT598_902_GENL_20C_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_902_GENL_20C_Type with content type SIMPLE"""
    _TypeDefinition = MT598_902_GENL_20C_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_902_GENL_20C_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_902.xsd', 58, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_902_GENL_20C_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_902_GENL_20C_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='20C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_902.xsd', 61, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_902.xsd', 61, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_902_GENL_20C_Type', MT598_902_GENL_20C_Type)


# Complex type {http://www.w3schools.com}MT598_902_GENL_98C_Type with content type SIMPLE
class MT598_902_GENL_98C_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_902_GENL_98C_Type with content type SIMPLE"""
    _TypeDefinition = MT598_902_GENL_98C_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_902_GENL_98C_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_902.xsd', 70, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_902_GENL_98C_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_902_GENL_98C_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='98C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_902.xsd', 73, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_902.xsd', 73, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_902_GENL_98C_Type', MT598_902_GENL_98C_Type)


MT598_902 = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'MT598_902'), CTD_ANON, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_902.xsd', 89, 1))
Namespace.addCategoryObject('elementBinding', MT598_902.name().localName(), MT598_902)



MT598_902_GENL._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'RelatedReference'), MT598_902_GENL_20C_Type, scope=MT598_902_GENL, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_902.xsd', 82, 3)))

MT598_902_GENL._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PreparationDateAndTime'), MT598_902_GENL_98C_Type, scope=MT598_902_GENL, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_902.xsd', 83, 3)))

MT598_902_GENL._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'IdentificationOfSecurity'), MT598_902_GENL_35B_Type, scope=MT598_902_GENL, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_902.xsd', 84, 3)))

MT598_902_GENL._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ErrorDetails'), MT598_902_GENL_70D_Type, scope=MT598_902_GENL, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_902.xsd', 85, 3)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_902.xsd', 84, 3))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT598_902_GENL._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'RelatedReference')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_902.xsd', 82, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT598_902_GENL._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PreparationDateAndTime')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_902.xsd', 83, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT598_902_GENL._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'IdentificationOfSecurity')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_902.xsd', 84, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT598_902_GENL._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ErrorDetails')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_902.xsd', 85, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    transitions.append(fac.Transition(st_3, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    st_3._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
MT598_902_GENL._Automaton = _BuildAutomaton()




CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TransactionReference'), MT598_902_20_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_902.xsd', 92, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SubMessageType'), MT598_902_12_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_902.xsd', 93, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ProprietaryMessage'), MT598_902_77E_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_902.xsd', 94, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'GENL'), MT598_902_GENL, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_902.xsd', 95, 4)))

def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'TransactionReference')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_902.xsd', 92, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SubMessageType')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_902.xsd', 93, 4))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ProprietaryMessage')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_902.xsd', 94, 4))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'GENL')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_902.xsd', 95, 4))
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
CTD_ANON._Automaton = _BuildAutomaton_()


