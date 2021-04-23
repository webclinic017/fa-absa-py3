
# C:\Swift\Templates\MT598_132.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:96afad3d20bbfe8d040a1a097fa388d9fecd10e3
# Generated 2019-06-19 11:04:52.282000 by PyXB version 1.2.2
# Namespace http://www.w3schools.com

import pyxb
import pyxb.binding
import pyxb.binding.saxer
import StringIO
import pyxb.utils.utility
import pyxb.utils.domutils
import sys

# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:f6380c80-9253-11e9-8892-8851fb4dff7a')

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


# Atomic simple type: {http://www.w3schools.com}MT598_132_20_Type_Pattern
class MT598_132_20_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_132_20_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_132.xsd', 3, 1)
    _Documentation = None
MT598_132_20_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_132_20_Type_Pattern._CF_pattern.addPattern(pattern="(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,16})")
MT598_132_20_Type_Pattern._InitializeFacetMap(MT598_132_20_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_132_20_Type_Pattern', MT598_132_20_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_132_26H_Type_Pattern
class MT598_132_26H_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_132_26H_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_132.xsd', 24, 1)
    _Documentation = None
MT598_132_26H_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_132_26H_Type_Pattern._CF_pattern.addPattern(pattern='(([A-Z]{1,2}[0-9]{1,6})?/[0-9]{1,10})')
MT598_132_26H_Type_Pattern._InitializeFacetMap(MT598_132_26H_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_132_26H_Type_Pattern', MT598_132_26H_Type_Pattern)

# Complex type {http://www.w3schools.com}MT598_132_12_Type with content type SIMPLE
class MT598_132_12_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_132_12_Type with content type SIMPLE"""
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_132_12_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_132.xsd', 16, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.string
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_132_12_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='12')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_132.xsd', 19, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_132.xsd', 19, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT598_132_12_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_132.xsd', 20, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_132.xsd', 20, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
Namespace.addCategoryObject('typeBinding', 'MT598_132_12_Type', MT598_132_12_Type)


# Complex type {http://www.w3schools.com}MT598_132_77E_Type with content type SIMPLE
class MT598_132_77E_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_132_77E_Type with content type SIMPLE"""
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_132_77E_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_132.xsd', 37, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.string
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_132_77E_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='77E')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_132.xsd', 40, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_132.xsd', 40, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT598_132_77E_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_132.xsd', 41, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_132.xsd', 41, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
Namespace.addCategoryObject('typeBinding', 'MT598_132_77E_Type', MT598_132_77E_Type)


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_132.xsd', 46, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}TransactionReference uses Python identifier TransactionReference
    __TransactionReference = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'TransactionReference'), 'TransactionReference', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comTransactionReference', False, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_132.xsd', 48, 4), )

    
    TransactionReference = property(__TransactionReference.value, __TransactionReference.set, None, None)

    
    # Element {http://www.w3schools.com}SubMessageType uses Python identifier SubMessageType
    __SubMessageType = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SubMessageType'), 'SubMessageType', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comSubMessageType', False, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_132.xsd', 49, 4), )

    
    SubMessageType = property(__SubMessageType.value, __SubMessageType.set, None, None)

    
    # Element {http://www.w3schools.com}ProprietaryMessage uses Python identifier ProprietaryMessage
    __ProprietaryMessage = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ProprietaryMessage'), 'ProprietaryMessage', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comProprietaryMessage', False, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_132.xsd', 50, 4), )

    
    ProprietaryMessage = property(__ProprietaryMessage.value, __ProprietaryMessage.set, None, None)

    
    # Element {http://www.w3schools.com}SAFIRESLoanReference uses Python identifier SAFIRESLoanReference
    __SAFIRESLoanReference = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SAFIRESLoanReference'), 'SAFIRESLoanReference', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comSAFIRESLoanReference', False, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_132.xsd', 51, 4), )

    
    SAFIRESLoanReference = property(__SAFIRESLoanReference.value, __SAFIRESLoanReference.set, None, None)

    _ElementMap.update({
        __TransactionReference.name() : __TransactionReference,
        __SubMessageType.name() : __SubMessageType,
        __ProprietaryMessage.name() : __ProprietaryMessage,
        __SAFIRESLoanReference.name() : __SAFIRESLoanReference
    })
    _AttributeMap.update({
        
    })



# Complex type {http://www.w3schools.com}MT598_132_20_Type with content type SIMPLE
class MT598_132_20_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_132_20_Type with content type SIMPLE"""
    _TypeDefinition = MT598_132_20_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_132_20_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_132.xsd', 8, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_132_20_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_132_20_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='20')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_132.xsd', 11, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_132.xsd', 11, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT598_132_20_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_132.xsd', 12, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_132.xsd', 12, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
Namespace.addCategoryObject('typeBinding', 'MT598_132_20_Type', MT598_132_20_Type)


# Complex type {http://www.w3schools.com}MT598_132_26H_Type with content type SIMPLE
class MT598_132_26H_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_132_26H_Type with content type SIMPLE"""
    _TypeDefinition = MT598_132_26H_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_132_26H_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_132.xsd', 29, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_132_26H_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_132_26H_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='26H')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_132.xsd', 32, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_132.xsd', 32, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT598_132_26H_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_132.xsd', 33, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_132.xsd', 33, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
Namespace.addCategoryObject('typeBinding', 'MT598_132_26H_Type', MT598_132_26H_Type)


MT598_132 = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'MT598_132'), CTD_ANON, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_132.xsd', 45, 1))
Namespace.addCategoryObject('elementBinding', MT598_132.name().localName(), MT598_132)



CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TransactionReference'), MT598_132_20_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_132.xsd', 48, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SubMessageType'), MT598_132_12_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_132.xsd', 49, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ProprietaryMessage'), MT598_132_77E_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_132.xsd', 50, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SAFIRESLoanReference'), MT598_132_26H_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_132.xsd', 51, 4)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'TransactionReference')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_132.xsd', 48, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SubMessageType')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_132.xsd', 49, 4))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ProprietaryMessage')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_132.xsd', 50, 4))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SAFIRESLoanReference')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT598_132.xsd', 51, 4))
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
CTD_ANON._Automaton = _BuildAutomaton()


