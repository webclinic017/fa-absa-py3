# C:\Projects\Swift_Integration_ap\base\extensions\SwiftIntegration\Utilities\XSD\MTx99.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:96afad3d20bbfe8d040a1a097fa388d9fecd10e3
# Generated 2019-10-22 17:01:40.499222 by PyXB version 1.2.6 using Python 3.7.4.final.0
# Namespace http://www.w3schools.com


import pyxb
import pyxb.binding
import pyxb.binding.saxer
import io
import pyxb.utils.utility
import pyxb.utils.domutils
import sys
import pyxb.utils.six as _six

# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:83ff3db6-f4bf-11e9-81f6-484d7e9b1690')

# Version of PyXB used to generate the bindings
_PyXBVersion = '1.2.6'
# Generated bindings are not compatible across PyXB versions
if pyxb.__version__ != _PyXBVersion:
    raise pyxb.PyXBVersionError(_PyXBVersion)

# A holder for module-level binding classes so we can access them from
# inside class definitions where property names may conflict.
_module_typeBindings = pyxb.utils.utility.Object()

# Import bindings for namespaces imported into schema
import pyxb.binding.datatypes

# NOTE: All namespace declarations are reserved within the binding
Namespace = pyxb.namespace.NamespaceForURI('http://www.w3schools.com', create_if_missing=True)
Namespace.configureCategories(['typeBinding', 'elementBinding'])


def CreateFromDocument(xml_text, default_namespace=None, location_base=None):
    """Parse the given XML and use the document element to create a
    Python instance.

    @param xml_text An XML document.  This should be data (Python 2
    str or Python 3 bytes), or a text (Python 2 unicode or Python 3
    str) in the L{pyxb._InputEncoding} encoding.

    @keyword default_namespace The L{pyxb.Namespace} instance to use as the
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
        return CreateFromDOM(dom.documentElement, default_namespace=default_namespace)
    if default_namespace is None:
        default_namespace = Namespace.fallbackNamespace()
    saxer = pyxb.binding.saxer.make_parser(fallback_namespace=default_namespace, location_base=location_base)
    handler = saxer.getContentHandler()
    xmld = xml_text
    if isinstance(xmld, _six.text_type):
        xmld = xmld.encode(pyxb._InputEncoding)
    saxer.parse(io.BytesIO(xmld))
    instance = handler.rootObject()
    return instance


def CreateFromDOM(node, default_namespace=None):
    """Create a Python instance from the given DOM node.
    The node tag must correspond to an element declaration in this module.

    @deprecated: Forcing use of DOM interface is unnecessary; use L{CreateFromDocument}."""
    if default_namespace is None:
        default_namespace = Namespace.fallbackNamespace()
    return pyxb.binding.basis.element.AnyCreateFromDOM(node, default_namespace)


# Atomic simple type: {http://www.w3schools.com}MTx99_20_Type_Pattern
class MTx99_20_Type_Pattern(pyxb.binding.datatypes.string):
    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MTx99_20_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location(
        'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MTx99.xsd', 3, 1)
    _Documentation = None


MTx99_20_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MTx99_20_Type_Pattern._CF_pattern.addPattern(
    pattern="([^/]([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,16}[^/])")
MTx99_20_Type_Pattern._InitializeFacetMap(MTx99_20_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MTx99_20_Type_Pattern', MTx99_20_Type_Pattern)
_module_typeBindings.MTx99_20_Type_Pattern = MTx99_20_Type_Pattern


# Atomic simple type: {http://www.w3schools.com}MTx99_21_Type_Pattern
class MTx99_21_Type_Pattern(pyxb.binding.datatypes.string):
    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MTx99_21_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location(
        'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MTx99.xsd', 16, 1)
    _Documentation = None


MTx99_21_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MTx99_21_Type_Pattern._CF_pattern.addPattern(
    pattern="([^/]([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,16}[^/])")
MTx99_21_Type_Pattern._InitializeFacetMap(MTx99_21_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MTx99_21_Type_Pattern', MTx99_21_Type_Pattern)
_module_typeBindings.MTx99_21_Type_Pattern = MTx99_21_Type_Pattern


# Atomic simple type: {http://www.w3schools.com}MTx99_79_Type_Pattern
class MTx99_79_Type_Pattern(pyxb.binding.datatypes.string):
    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MTx99_79_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location(
        'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MTx99.xsd', 29, 1)
    _Documentation = None


MTx99_79_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MTx99_79_Type_Pattern._CF_pattern.addPattern(
    pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,50}\\n?){1,35})")
MTx99_79_Type_Pattern._InitializeFacetMap(MTx99_79_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MTx99_79_Type_Pattern', MTx99_79_Type_Pattern)
_module_typeBindings.MTx99_79_Type_Pattern = MTx99_79_Type_Pattern


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON(pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location(
        'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MTx99.xsd', 43, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element {http://www.w3schools.com}TransactionReferenceNumber uses Python identifier TransactionReferenceNumber
    __TransactionReferenceNumber = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(Namespace, 'TransactionReferenceNumber'), 'TransactionReferenceNumber',
        '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comTransactionReferenceNumber', False,
        pyxb.utils.utility.Location(
            'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MTx99.xsd', 45,
            4), )

    TransactionReferenceNumber = property(__TransactionReferenceNumber.value, __TransactionReferenceNumber.set, None,
                                          None)

    # Element {http://www.w3schools.com}RelatedReference uses Python identifier RelatedReference
    __RelatedReference = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(Namespace, 'RelatedReference'), 'RelatedReference',
        '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comRelatedReference', False, pyxb.utils.utility.Location(
            'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MTx99.xsd', 46,
            4), )

    RelatedReference = property(__RelatedReference.value, __RelatedReference.set, None, None)

    # Element {http://www.w3schools.com}Narrative uses Python identifier Narrative
    __Narrative = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Narrative'),
                                                          'Narrative',
                                                          '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comNarrative',
                                                          False, pyxb.utils.utility.Location(
            'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MTx99.xsd', 47,
            4), )

    Narrative = property(__Narrative.value, __Narrative.set, None, None)

    _ElementMap.update({
        __TransactionReferenceNumber.name(): __TransactionReferenceNumber,
        __RelatedReference.name(): __RelatedReference,
        __Narrative.name(): __Narrative
    })
    _AttributeMap.update({

    })


_module_typeBindings.CTD_ANON = CTD_ANON


# Complex type {http://www.w3schools.com}MTx99_20_Type with content type SIMPLE
class MTx99_20_Type(pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MTx99_20_Type with content type SIMPLE"""
    _TypeDefinition = MTx99_20_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MTx99_20_Type')
    _XSDLocation = pyxb.utils.utility.Location(
        'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MTx99.xsd', 8, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MTx99_20_Type_Pattern

    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag',
                                                   '__httpwww_w3schools_com_MTx99_20_Type_swiftTag',
                                                   pyxb.binding.datatypes.anySimpleType, fixed=True,
                                                   unicode_default='20')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location(
        'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MTx99.xsd', 11, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location(
        'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MTx99.xsd', 11, 4)

    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory',
                                                      '__httpwww_w3schools_com_MTx99_20_Type_isMandatory',
                                                      pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location(
        'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MTx99.xsd', 12, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location(
        'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MTx99.xsd', 12, 4)

    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({

    })
    _AttributeMap.update({
        __swiftTag.name(): __swiftTag,
        __isMandatory.name(): __isMandatory
    })


_module_typeBindings.MTx99_20_Type = MTx99_20_Type
Namespace.addCategoryObject('typeBinding', 'MTx99_20_Type', MTx99_20_Type)


# Complex type {http://www.w3schools.com}MTx99_21_Type with content type SIMPLE
class MTx99_21_Type(pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MTx99_21_Type with content type SIMPLE"""
    _TypeDefinition = MTx99_21_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MTx99_21_Type')
    _XSDLocation = pyxb.utils.utility.Location(
        'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MTx99.xsd', 21, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MTx99_21_Type_Pattern

    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag',
                                                   '__httpwww_w3schools_com_MTx99_21_Type_swiftTag',
                                                   pyxb.binding.datatypes.anySimpleType, fixed=True,
                                                   unicode_default='21')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location(
        'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MTx99.xsd', 24, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location(
        'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MTx99.xsd', 24, 4)

    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory',
                                                      '__httpwww_w3schools_com_MTx99_21_Type_isMandatory',
                                                      pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location(
        'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MTx99.xsd', 25, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location(
        'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MTx99.xsd', 25, 4)

    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({

    })
    _AttributeMap.update({
        __swiftTag.name(): __swiftTag,
        __isMandatory.name(): __isMandatory
    })


_module_typeBindings.MTx99_21_Type = MTx99_21_Type
Namespace.addCategoryObject('typeBinding', 'MTx99_21_Type', MTx99_21_Type)


# Complex type {http://www.w3schools.com}MTx99_79_Type with content type SIMPLE
class MTx99_79_Type(pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MTx99_79_Type with content type SIMPLE"""
    _TypeDefinition = MTx99_79_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MTx99_79_Type')
    _XSDLocation = pyxb.utils.utility.Location(
        'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MTx99.xsd', 34, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MTx99_79_Type_Pattern

    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag',
                                                   '__httpwww_w3schools_com_MTx99_79_Type_swiftTag',
                                                   pyxb.binding.datatypes.anySimpleType, fixed=True,
                                                   unicode_default='79')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location(
        'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MTx99.xsd', 37, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location(
        'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MTx99.xsd', 37, 4)

    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory',
                                                      '__httpwww_w3schools_com_MTx99_79_Type_isMandatory',
                                                      pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location(
        'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MTx99.xsd', 38, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location(
        'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MTx99.xsd', 38, 4)

    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({

    })
    _AttributeMap.update({
        __swiftTag.name(): __swiftTag,
        __isMandatory.name(): __isMandatory
    })


_module_typeBindings.MTx99_79_Type = MTx99_79_Type
Namespace.addCategoryObject('typeBinding', 'MTx99_79_Type', MTx99_79_Type)

MTx99 = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'MTx99'), CTD_ANON,
                                   location=pyxb.utils.utility.Location(
                                       'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MTx99.xsd',
                                       42, 1))
Namespace.addCategoryObject('elementBinding', MTx99.name().localName(), MTx99)

CTD_ANON._AddElement(
    pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TransactionReferenceNumber'), MTx99_20_Type,
                               scope=CTD_ANON, location=pyxb.utils.utility.Location(
            'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MTx99.xsd', 45,
            4)))

CTD_ANON._AddElement(
    pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'RelatedReference'), MTx99_21_Type,
                               scope=CTD_ANON, location=pyxb.utils.utility.Location(
            'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MTx99.xsd', 46,
            4)))

CTD_ANON._AddElement(
    pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Narrative'), MTx99_79_Type, scope=CTD_ANON,
                               location=pyxb.utils.utility.Location(
                                   'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MTx99.xsd',
                                   47, 4)))


def _BuildAutomaton():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location(
        'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MTx99.xsd', 46, 4))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'TransactionReferenceNumber')),
        pyxb.utils.utility.Location(
            'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MTx99.xsd', 45, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'RelatedReference')), pyxb.utils.utility.Location(
            'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MTx99.xsd', 46, 4))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Narrative')),
                                             pyxb.utils.utility.Location(
                                                 'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MTx99.xsd',
                                                 47, 4))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_1, [
    ]))
    transitions.append(fac.Transition(st_2, [
    ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True)]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False)]))
    st_1._set_transitionSet(transitions)
    transitions = []
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)


CTD_ANON._Automaton = _BuildAutomaton()


