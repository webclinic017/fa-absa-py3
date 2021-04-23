
# C:\SWIFT\SwiftReader\XSD\MT598_901.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:96afad3d20bbfe8d040a1a097fa388d9fecd10e3
# Generated 2017-02-16 17:37:20.684000 by PyXB version 1.2.2
# Namespace http://www.w3schools.com

import pyxb
import pyxb.binding
import pyxb.binding.saxer
import StringIO
import pyxb.utils.utility
import pyxb.utils.domutils
import sys

# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:77c43351-f440-11e6-aaa5-180373dbbcdf')

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


# Atomic simple type: {http://www.w3schools.com}MT598_901_20_Type_Pattern
class MT598_901_20_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_901_20_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_901.xsd', 17, 1)
    _Documentation = None
MT598_901_20_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_901_20_Type_Pattern._CF_pattern.addPattern(pattern='(.{1,16})')
MT598_901_20_Type_Pattern._InitializeFacetMap(MT598_901_20_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_901_20_Type_Pattern', MT598_901_20_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_901_13E_Type_Pattern
class MT598_901_13E_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_901_13E_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_901.xsd', 29, 1)
    _Documentation = None
MT598_901_13E_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_901_13E_Type_Pattern._CF_pattern.addPattern(pattern='([0-9]{8}[0-9]{4})')
MT598_901_13E_Type_Pattern._InitializeFacetMap(MT598_901_13E_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_901_13E_Type_Pattern', MT598_901_13E_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_901_21_Type_Pattern
class MT598_901_21_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_901_21_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_901.xsd', 41, 1)
    _Documentation = None
MT598_901_21_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_901_21_Type_Pattern._CF_pattern.addPattern(pattern='(.{1,16})')
MT598_901_21_Type_Pattern._InitializeFacetMap(MT598_901_21_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_901_21_Type_Pattern', MT598_901_21_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_901_79_Type_Pattern
class MT598_901_79_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_901_79_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_901.xsd', 53, 1)
    _Documentation = None
MT598_901_79_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_901_79_Type_Pattern._CF_pattern.addPattern(pattern='(.{4}/[A-Z0-9]{1,3})')
MT598_901_79_Type_Pattern._InitializeFacetMap(MT598_901_79_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_901_79_Type_Pattern', MT598_901_79_Type_Pattern)

# Complex type {http://www.w3schools.com}MT598_901_77E_Type with content type SIMPLE
class MT598_901_77E_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_901_77E_Type with content type SIMPLE"""
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_901_77E_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_901.xsd', 3, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.string
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_901_77E_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='77E')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_901.xsd', 6, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_901.xsd', 6, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_901_77E_Type', MT598_901_77E_Type)


# Complex type {http://www.w3schools.com}MT598_901_12_Type with content type SIMPLE
class MT598_901_12_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_901_12_Type with content type SIMPLE"""
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_901_12_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_901.xsd', 10, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.string
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_901_12_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='12')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_901.xsd', 13, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_901.xsd', 13, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_901_12_Type', MT598_901_12_Type)


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_901.xsd', 66, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}TransactionReference uses Python identifier TransactionReference
    __TransactionReference = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'TransactionReference'), 'TransactionReference', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comTransactionReference', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_901.xsd', 68, 4), )

    
    TransactionReference = property(__TransactionReference.value, __TransactionReference.set, None, None)

    
    # Element {http://www.w3schools.com}SubMessageType uses Python identifier SubMessageType
    __SubMessageType = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SubMessageType'), 'SubMessageType', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comSubMessageType', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_901.xsd', 69, 4), )

    
    SubMessageType = property(__SubMessageType.value, __SubMessageType.set, None, None)

    
    # Element {http://www.w3schools.com}ProprietaryMessage uses Python identifier ProprietaryMessage
    __ProprietaryMessage = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ProprietaryMessage'), 'ProprietaryMessage', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comProprietaryMessage', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_901.xsd', 70, 4), )

    
    ProprietaryMessage = property(__ProprietaryMessage.value, __ProprietaryMessage.set, None, None)

    
    # Element {http://www.w3schools.com}Narrative uses Python identifier Narrative
    __Narrative = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Narrative'), 'Narrative', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comNarrative', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_901.xsd', 71, 4), )

    
    Narrative = property(__Narrative.value, __Narrative.set, None, None)

    
    # Element {http://www.w3schools.com}DateTimeIndicator uses Python identifier DateTimeIndicator
    __DateTimeIndicator = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DateTimeIndicator'), 'DateTimeIndicator', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comDateTimeIndicator', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_901.xsd', 72, 4), )

    
    DateTimeIndicator = property(__DateTimeIndicator.value, __DateTimeIndicator.set, None, None)

    
    # Element {http://www.w3schools.com}RelatedReference uses Python identifier RelatedReference
    __RelatedReference = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'RelatedReference'), 'RelatedReference', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comRelatedReference', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_901.xsd', 73, 4), )

    
    RelatedReference = property(__RelatedReference.value, __RelatedReference.set, None, None)

    _ElementMap.update({
        __TransactionReference.name() : __TransactionReference,
        __SubMessageType.name() : __SubMessageType,
        __ProprietaryMessage.name() : __ProprietaryMessage,
        __Narrative.name() : __Narrative,
        __DateTimeIndicator.name() : __DateTimeIndicator,
        __RelatedReference.name() : __RelatedReference
    })
    _AttributeMap.update({
        
    })



# Complex type {http://www.w3schools.com}MT598_901_20_Type with content type SIMPLE
class MT598_901_20_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_901_20_Type with content type SIMPLE"""
    _TypeDefinition = MT598_901_20_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_901_20_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_901.xsd', 22, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_901_20_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_901_20_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='20')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_901.xsd', 25, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_901.xsd', 25, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_901_20_Type', MT598_901_20_Type)


# Complex type {http://www.w3schools.com}MT598_901_13E_Type with content type SIMPLE
class MT598_901_13E_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_901_13E_Type with content type SIMPLE"""
    _TypeDefinition = MT598_901_13E_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_901_13E_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_901.xsd', 34, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_901_13E_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_901_13E_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='13E')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_901.xsd', 37, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_901.xsd', 37, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_901_13E_Type', MT598_901_13E_Type)


# Complex type {http://www.w3schools.com}MT598_901_21_Type with content type SIMPLE
class MT598_901_21_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_901_21_Type with content type SIMPLE"""
    _TypeDefinition = MT598_901_21_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_901_21_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_901.xsd', 46, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_901_21_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_901_21_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='21')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_901.xsd', 49, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_901.xsd', 49, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_901_21_Type', MT598_901_21_Type)


# Complex type {http://www.w3schools.com}MT598_901_79_Type with content type SIMPLE
class MT598_901_79_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_901_79_Type with content type SIMPLE"""
    _TypeDefinition = MT598_901_79_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_901_79_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_901.xsd', 58, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_901_79_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_901_79_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='79')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_901.xsd', 61, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_901.xsd', 61, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_901_79_Type', MT598_901_79_Type)


MT598_901 = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'MT598_901'), CTD_ANON, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_901.xsd', 65, 1))
Namespace.addCategoryObject('elementBinding', MT598_901.name().localName(), MT598_901)



CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TransactionReference'), MT598_901_20_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_901.xsd', 68, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SubMessageType'), MT598_901_12_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_901.xsd', 69, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ProprietaryMessage'), MT598_901_77E_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_901.xsd', 70, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Narrative'), MT598_901_79_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_901.xsd', 71, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DateTimeIndicator'), MT598_901_13E_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_901.xsd', 72, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'RelatedReference'), MT598_901_21_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_901.xsd', 73, 4)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'TransactionReference')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_901.xsd', 68, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SubMessageType')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_901.xsd', 69, 4))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ProprietaryMessage')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_901.xsd', 70, 4))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Narrative')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_901.xsd', 71, 4))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DateTimeIndicator')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_901.xsd', 72, 4))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'RelatedReference')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_901.xsd', 73, 4))
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
    st_5._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON._Automaton = _BuildAutomaton()


