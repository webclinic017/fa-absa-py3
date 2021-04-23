# C:\Projects\Swift_Integration_ap\base\extensions\SwiftIntegration\FFXMMConfirmation\Outgoing\XSD\MT395.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:96afad3d20bbfe8d040a1a097fa388d9fecd10e3
# Generated 2019-10-25 10:44:44.342859 by PyXB version 1.2.6 using Python 3.7.4.final.0
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
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:5aca4578-f6e6-11e9-88dc-484d7e9b1690')

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


# Atomic simple type: {http://www.w3schools.com}MT395_79_Type_Pattern
class MT395_79_Type_Pattern(pyxb.binding.datatypes.string):
    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT395_79_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location(
        'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\FFXMMConfirmation\\Outgoing\\XSD\\MT395.xsd',
        3, 1)
    _Documentation = None


MT395_79_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT395_79_Type_Pattern._CF_pattern.addPattern(
    pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,50}\\n?){1,35})")
MT395_79_Type_Pattern._InitializeFacetMap(MT395_79_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT395_79_Type_Pattern', MT395_79_Type_Pattern)
_module_typeBindings.MT395_79_Type_Pattern = MT395_79_Type_Pattern


# Atomic simple type: {http://www.w3schools.com}MT395_11R_Type_Pattern
class MT395_11R_Type_Pattern(pyxb.binding.datatypes.string):
    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT395_11R_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location(
        'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\FFXMMConfirmation\\Outgoing\\XSD\\MT395.xsd',
        16, 1)
    _Documentation = None


MT395_11R_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT395_11R_Type_Pattern._CF_pattern.addPattern(
    pattern='([0-9]{3}(\\n)?[0-9]{2}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])(\\n)?([0-9]{4}[0-9]{6})?)')
MT395_11R_Type_Pattern._InitializeFacetMap(MT395_11R_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT395_11R_Type_Pattern', MT395_11R_Type_Pattern)
_module_typeBindings.MT395_11R_Type_Pattern = MT395_11R_Type_Pattern


# Atomic simple type: {http://www.w3schools.com}MT395_20_Type_Pattern
class MT395_20_Type_Pattern(pyxb.binding.datatypes.string):
    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT395_20_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location(
        'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\FFXMMConfirmation\\Outgoing\\XSD\\MT395.xsd',
        29, 1)
    _Documentation = None


MT395_20_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT395_20_Type_Pattern._CF_pattern.addPattern(
    pattern="([^/]([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,16}[^/])")
MT395_20_Type_Pattern._InitializeFacetMap(MT395_20_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT395_20_Type_Pattern', MT395_20_Type_Pattern)
_module_typeBindings.MT395_20_Type_Pattern = MT395_20_Type_Pattern


# Atomic simple type: {http://www.w3schools.com}MT395_75_Type_Pattern
class MT395_75_Type_Pattern(pyxb.binding.datatypes.string):
    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT395_75_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location(
        'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\FFXMMConfirmation\\Outgoing\\XSD\\MT395.xsd',
        42, 1)
    _Documentation = None


MT395_75_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT395_75_Type_Pattern._CF_pattern.addPattern(
    pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,6})")
MT395_75_Type_Pattern._InitializeFacetMap(MT395_75_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT395_75_Type_Pattern', MT395_75_Type_Pattern)
_module_typeBindings.MT395_75_Type_Pattern = MT395_75_Type_Pattern


# Atomic simple type: {http://www.w3schools.com}MT395_21_Type_Pattern
class MT395_21_Type_Pattern(pyxb.binding.datatypes.string):
    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT395_21_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location(
        'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\FFXMMConfirmation\\Outgoing\\XSD\\MT395.xsd',
        55, 1)
    _Documentation = None


MT395_21_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT395_21_Type_Pattern._CF_pattern.addPattern(
    pattern="([^/]([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,16}[^/])")
MT395_21_Type_Pattern._InitializeFacetMap(MT395_21_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT395_21_Type_Pattern', MT395_21_Type_Pattern)
_module_typeBindings.MT395_21_Type_Pattern = MT395_21_Type_Pattern


# Atomic simple type: {http://www.w3schools.com}MT395_77A_Type_Pattern
class MT395_77A_Type_Pattern(pyxb.binding.datatypes.string):
    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT395_77A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location(
        'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\FFXMMConfirmation\\Outgoing\\XSD\\MT395.xsd',
        68, 1)
    _Documentation = None


MT395_77A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT395_77A_Type_Pattern._CF_pattern.addPattern(
    pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,20})")
MT395_77A_Type_Pattern._InitializeFacetMap(MT395_77A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT395_77A_Type_Pattern', MT395_77A_Type_Pattern)
_module_typeBindings.MT395_77A_Type_Pattern = MT395_77A_Type_Pattern


# Atomic simple type: {http://www.w3schools.com}MT395_11S_Type_Pattern
class MT395_11S_Type_Pattern(pyxb.binding.datatypes.string):
    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT395_11S_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location(
        'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\FFXMMConfirmation\\Outgoing\\XSD\\MT395.xsd',
        81, 1)
    _Documentation = None


MT395_11S_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT395_11S_Type_Pattern._CF_pattern.addPattern(
    pattern='([0-9]{3}(\\n)?[0-9]{2}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])(\\n)?([0-9]{4}[0-9]{6})?)')
MT395_11S_Type_Pattern._InitializeFacetMap(MT395_11S_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT395_11S_Type_Pattern', MT395_11S_Type_Pattern)
_module_typeBindings.MT395_11S_Type_Pattern = MT395_11S_Type_Pattern


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON(pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location(
        'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\FFXMMConfirmation\\Outgoing\\XSD\\MT395.xsd',
        95, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    # Element {http://www.w3schools.com}TransactionReferenceNumber uses Python identifier TransactionReferenceNumber
    __TransactionReferenceNumber = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(Namespace, 'TransactionReferenceNumber'), 'TransactionReferenceNumber',
        '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comTransactionReferenceNumber', False,
        pyxb.utils.utility.Location(
            'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\FFXMMConfirmation\\Outgoing\\XSD\\MT395.xsd',
            97, 4), )

    TransactionReferenceNumber = property(__TransactionReferenceNumber.value, __TransactionReferenceNumber.set, None,
        None)

    # Element {http://www.w3schools.com}RelatedReference uses Python identifier RelatedReference
    __RelatedReference = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(Namespace, 'RelatedReference'), 'RelatedReference',
        '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comRelatedReference', False, pyxb.utils.utility.Location(
            'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\FFXMMConfirmation\\Outgoing\\XSD\\MT395.xsd',
            98, 4), )

    RelatedReference = property(__RelatedReference.value, __RelatedReference.set, None, None)

    # Element {http://www.w3schools.com}Queries uses Python identifier Queries
    __Queries = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Queries'), 'Queries',
        '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comQueries', False, pyxb.utils.utility.Location(
            'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\FFXMMConfirmation\\Outgoing\\XSD\\MT395.xsd',
            99, 4), )

    Queries = property(__Queries.value, __Queries.set, None, None)

    # Element {http://www.w3schools.com}Narrative uses Python identifier Narrative
    __Narrative = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Narrative'),
        'Narrative', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comNarrative', False,
        pyxb.utils.utility.Location(
            'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\FFXMMConfirmation\\Outgoing\\XSD\\MT395.xsd',
            100, 4), )

    Narrative = property(__Narrative.value, __Narrative.set, None, None)

    # Element {http://www.w3schools.com}MTAndDateOfTheOriginalMessage_R uses Python identifier MTAndDateOfTheOriginalMessage_R
    __MTAndDateOfTheOriginalMessage_R = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(Namespace, 'MTAndDateOfTheOriginalMessage_R'), 'MTAndDateOfTheOriginalMessage_R',
        '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comMTAndDateOfTheOriginalMessage_R', False,
        pyxb.utils.utility.Location(
            'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\FFXMMConfirmation\\Outgoing\\XSD\\MT395.xsd',
            102, 5), )

    MTAndDateOfTheOriginalMessage_R = property(__MTAndDateOfTheOriginalMessage_R.value,
        __MTAndDateOfTheOriginalMessage_R.set, None, None)

    # Element {http://www.w3schools.com}MTAndDateOfTheOriginalMessage_S uses Python identifier MTAndDateOfTheOriginalMessage_S
    __MTAndDateOfTheOriginalMessage_S = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(Namespace, 'MTAndDateOfTheOriginalMessage_S'), 'MTAndDateOfTheOriginalMessage_S',
        '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comMTAndDateOfTheOriginalMessage_S', False,
        pyxb.utils.utility.Location(
            'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\FFXMMConfirmation\\Outgoing\\XSD\\MT395.xsd',
            103, 5), )

    MTAndDateOfTheOriginalMessage_S = property(__MTAndDateOfTheOriginalMessage_S.value,
        __MTAndDateOfTheOriginalMessage_S.set, None, None)

    # Element {http://www.w3schools.com}NarrativeDescriptionOfTheOriginalMessage uses Python identifier NarrativeDescriptionOfTheOriginalMessage
    __NarrativeDescriptionOfTheOriginalMessage = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(Namespace, 'NarrativeDescriptionOfTheOriginalMessage'),
        'NarrativeDescriptionOfTheOriginalMessage',
        '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comNarrativeDescriptionOfTheOriginalMessage', False,
        pyxb.utils.utility.Location(
            'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\FFXMMConfirmation\\Outgoing\\XSD\\MT395.xsd',
            105, 4), )

    NarrativeDescriptionOfTheOriginalMessage = property(__NarrativeDescriptionOfTheOriginalMessage.value,
        __NarrativeDescriptionOfTheOriginalMessage.set, None, None)

    _ElementMap.update({
        __TransactionReferenceNumber.name(): __TransactionReferenceNumber,
        __RelatedReference.name(): __RelatedReference,
        __Queries.name(): __Queries,
        __Narrative.name(): __Narrative,
        __MTAndDateOfTheOriginalMessage_R.name(): __MTAndDateOfTheOriginalMessage_R,
        __MTAndDateOfTheOriginalMessage_S.name(): __MTAndDateOfTheOriginalMessage_S,
        __NarrativeDescriptionOfTheOriginalMessage.name(): __NarrativeDescriptionOfTheOriginalMessage
    })
    _AttributeMap.update({
    })


_module_typeBindings.CTD_ANON = CTD_ANON


# Complex type {http://www.w3schools.com}MT395_79_Type with content type SIMPLE
class MT395_79_Type(pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT395_79_Type with content type SIMPLE"""
    _TypeDefinition = MT395_79_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT395_79_Type')
    _XSDLocation = pyxb.utils.utility.Location(
        'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\FFXMMConfirmation\\Outgoing\\XSD\\MT395.xsd',
        8, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT395_79_Type_Pattern
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag',
        '__httpwww_w3schools_com_MT395_79_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True,
        unicode_default='79')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location(
        'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\FFXMMConfirmation\\Outgoing\\XSD\\MT395.xsd',
        11, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location(
        'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\FFXMMConfirmation\\Outgoing\\XSD\\MT395.xsd',
        11, 4)

    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory',
        '__httpwww_w3schools_com_MT395_79_Type_isMandatory', pyxb.binding.datatypes.anySimpleType,
        unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location(
        'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\FFXMMConfirmation\\Outgoing\\XSD\\MT395.xsd',
        12, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location(
        'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\FFXMMConfirmation\\Outgoing\\XSD\\MT395.xsd',
        12, 4)

    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
    })
    _AttributeMap.update({
        __swiftTag.name(): __swiftTag,
        __isMandatory.name(): __isMandatory
    })


_module_typeBindings.MT395_79_Type = MT395_79_Type
Namespace.addCategoryObject('typeBinding', 'MT395_79_Type', MT395_79_Type)


# Complex type {http://www.w3schools.com}MT395_11R_Type with content type SIMPLE
class MT395_11R_Type(pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT395_11R_Type with content type SIMPLE"""
    _TypeDefinition = MT395_11R_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT395_11R_Type')
    _XSDLocation = pyxb.utils.utility.Location(
        'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\FFXMMConfirmation\\Outgoing\\XSD\\MT395.xsd',
        21, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT395_11R_Type_Pattern
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag',
        '__httpwww_w3schools_com_MT395_11R_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True,
        unicode_default='11R')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location(
        'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\FFXMMConfirmation\\Outgoing\\XSD\\MT395.xsd',
        24, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location(
        'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\FFXMMConfirmation\\Outgoing\\XSD\\MT395.xsd',
        24, 4)

    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory',
        '__httpwww_w3schools_com_MT395_11R_Type_isMandatory', pyxb.binding.datatypes.anySimpleType,
        unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location(
        'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\FFXMMConfirmation\\Outgoing\\XSD\\MT395.xsd',
        25, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location(
        'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\FFXMMConfirmation\\Outgoing\\XSD\\MT395.xsd',
        25, 4)

    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
    })
    _AttributeMap.update({
        __swiftTag.name(): __swiftTag,
        __isMandatory.name(): __isMandatory
    })


_module_typeBindings.MT395_11R_Type = MT395_11R_Type
Namespace.addCategoryObject('typeBinding', 'MT395_11R_Type', MT395_11R_Type)


# Complex type {http://www.w3schools.com}MT395_20_Type with content type SIMPLE
class MT395_20_Type(pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT395_20_Type with content type SIMPLE"""
    _TypeDefinition = MT395_20_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT395_20_Type')
    _XSDLocation = pyxb.utils.utility.Location(
        'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\FFXMMConfirmation\\Outgoing\\XSD\\MT395.xsd',
        34, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT395_20_Type_Pattern
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag',
        '__httpwww_w3schools_com_MT395_20_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True,
        unicode_default='20')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location(
        'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\FFXMMConfirmation\\Outgoing\\XSD\\MT395.xsd',
        37, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location(
        'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\FFXMMConfirmation\\Outgoing\\XSD\\MT395.xsd',
        37, 4)

    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory',
        '__httpwww_w3schools_com_MT395_20_Type_isMandatory', pyxb.binding.datatypes.anySimpleType,
        unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location(
        'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\FFXMMConfirmation\\Outgoing\\XSD\\MT395.xsd',
        38, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location(
        'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\FFXMMConfirmation\\Outgoing\\XSD\\MT395.xsd',
        38, 4)

    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
    })
    _AttributeMap.update({
        __swiftTag.name(): __swiftTag,
        __isMandatory.name(): __isMandatory
    })


_module_typeBindings.MT395_20_Type = MT395_20_Type
Namespace.addCategoryObject('typeBinding', 'MT395_20_Type', MT395_20_Type)


# Complex type {http://www.w3schools.com}MT395_75_Type with content type SIMPLE
class MT395_75_Type(pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT395_75_Type with content type SIMPLE"""
    _TypeDefinition = MT395_75_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT395_75_Type')
    _XSDLocation = pyxb.utils.utility.Location(
        'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\FFXMMConfirmation\\Outgoing\\XSD\\MT395.xsd',
        47, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT395_75_Type_Pattern
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag',
        '__httpwww_w3schools_com_MT395_75_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True,
        unicode_default='75')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location(
        'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\FFXMMConfirmation\\Outgoing\\XSD\\MT395.xsd',
        50, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location(
        'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\FFXMMConfirmation\\Outgoing\\XSD\\MT395.xsd',
        50, 4)

    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory',
        '__httpwww_w3schools_com_MT395_75_Type_isMandatory', pyxb.binding.datatypes.anySimpleType,
        unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location(
        'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\FFXMMConfirmation\\Outgoing\\XSD\\MT395.xsd',
        51, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location(
        'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\FFXMMConfirmation\\Outgoing\\XSD\\MT395.xsd',
        51, 4)

    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
    })
    _AttributeMap.update({
        __swiftTag.name(): __swiftTag,
        __isMandatory.name(): __isMandatory
    })


_module_typeBindings.MT395_75_Type = MT395_75_Type
Namespace.addCategoryObject('typeBinding', 'MT395_75_Type', MT395_75_Type)


# Complex type {http://www.w3schools.com}MT395_21_Type with content type SIMPLE
class MT395_21_Type(pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT395_21_Type with content type SIMPLE"""
    _TypeDefinition = MT395_21_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT395_21_Type')
    _XSDLocation = pyxb.utils.utility.Location(
        'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\FFXMMConfirmation\\Outgoing\\XSD\\MT395.xsd',
        60, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT395_21_Type_Pattern
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag',
        '__httpwww_w3schools_com_MT395_21_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True,
        unicode_default='21')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location(
        'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\FFXMMConfirmation\\Outgoing\\XSD\\MT395.xsd',
        63, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location(
        'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\FFXMMConfirmation\\Outgoing\\XSD\\MT395.xsd',
        63, 4)

    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory',
        '__httpwww_w3schools_com_MT395_21_Type_isMandatory', pyxb.binding.datatypes.anySimpleType,
        unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location(
        'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\FFXMMConfirmation\\Outgoing\\XSD\\MT395.xsd',
        64, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location(
        'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\FFXMMConfirmation\\Outgoing\\XSD\\MT395.xsd',
        64, 4)

    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
    })
    _AttributeMap.update({
        __swiftTag.name(): __swiftTag,
        __isMandatory.name(): __isMandatory
    })


_module_typeBindings.MT395_21_Type = MT395_21_Type
Namespace.addCategoryObject('typeBinding', 'MT395_21_Type', MT395_21_Type)


# Complex type {http://www.w3schools.com}MT395_77A_Type with content type SIMPLE
class MT395_77A_Type(pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT395_77A_Type with content type SIMPLE"""
    _TypeDefinition = MT395_77A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT395_77A_Type')
    _XSDLocation = pyxb.utils.utility.Location(
        'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\FFXMMConfirmation\\Outgoing\\XSD\\MT395.xsd',
        73, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT395_77A_Type_Pattern
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag',
        '__httpwww_w3schools_com_MT395_77A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True,
        unicode_default='77A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location(
        'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\FFXMMConfirmation\\Outgoing\\XSD\\MT395.xsd',
        76, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location(
        'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\FFXMMConfirmation\\Outgoing\\XSD\\MT395.xsd',
        76, 4)

    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory',
        '__httpwww_w3schools_com_MT395_77A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType,
        unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location(
        'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\FFXMMConfirmation\\Outgoing\\XSD\\MT395.xsd',
        77, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location(
        'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\FFXMMConfirmation\\Outgoing\\XSD\\MT395.xsd',
        77, 4)

    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
    })
    _AttributeMap.update({
        __swiftTag.name(): __swiftTag,
        __isMandatory.name(): __isMandatory
    })


_module_typeBindings.MT395_77A_Type = MT395_77A_Type
Namespace.addCategoryObject('typeBinding', 'MT395_77A_Type', MT395_77A_Type)


# Complex type {http://www.w3schools.com}MT395_11S_Type with content type SIMPLE
class MT395_11S_Type(pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT395_11S_Type with content type SIMPLE"""
    _TypeDefinition = MT395_11S_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT395_11S_Type')
    _XSDLocation = pyxb.utils.utility.Location(
        'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\FFXMMConfirmation\\Outgoing\\XSD\\MT395.xsd',
        86, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT395_11S_Type_Pattern
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag',
        '__httpwww_w3schools_com_MT395_11S_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True,
        unicode_default='11S')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location(
        'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\FFXMMConfirmation\\Outgoing\\XSD\\MT395.xsd',
        89, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location(
        'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\FFXMMConfirmation\\Outgoing\\XSD\\MT395.xsd',
        89, 4)

    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory',
        '__httpwww_w3schools_com_MT395_11S_Type_isMandatory', pyxb.binding.datatypes.anySimpleType,
        unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location(
        'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\FFXMMConfirmation\\Outgoing\\XSD\\MT395.xsd',
        90, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location(
        'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\FFXMMConfirmation\\Outgoing\\XSD\\MT395.xsd',
        90, 4)

    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
    })
    _AttributeMap.update({
        __swiftTag.name(): __swiftTag,
        __isMandatory.name(): __isMandatory
    })


_module_typeBindings.MT395_11S_Type = MT395_11S_Type
Namespace.addCategoryObject('typeBinding', 'MT395_11S_Type', MT395_11S_Type)

MT395 = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'MT395'), CTD_ANON,
    location=pyxb.utils.utility.Location(
        'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\FFXMMConfirmation\\Outgoing\\XSD\\MT395.xsd',
        94, 1))
Namespace.addCategoryObject('elementBinding', MT395.name().localName(), MT395)

CTD_ANON._AddElement(
    pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TransactionReferenceNumber'), MT395_20_Type,
        scope=CTD_ANON, location=pyxb.utils.utility.Location(
            'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\FFXMMConfirmation\\Outgoing\\XSD\\MT395.xsd',
            97, 4)))

CTD_ANON._AddElement(
    pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'RelatedReference'), MT395_21_Type,
        scope=CTD_ANON, location=pyxb.utils.utility.Location(
            'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\FFXMMConfirmation\\Outgoing\\XSD\\MT395.xsd',
            98, 4)))

CTD_ANON._AddElement(
    pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Queries'), MT395_75_Type, scope=CTD_ANON,
        location=pyxb.utils.utility.Location(
            'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\FFXMMConfirmation\\Outgoing\\XSD\\MT395.xsd',
            99, 4)))

CTD_ANON._AddElement(
    pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Narrative'), MT395_77A_Type, scope=CTD_ANON,
        location=pyxb.utils.utility.Location(
            'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\FFXMMConfirmation\\Outgoing\\XSD\\MT395.xsd',
            100, 4)))

CTD_ANON._AddElement(
    pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'MTAndDateOfTheOriginalMessage_R'),
        MT395_11R_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location(
            'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\FFXMMConfirmation\\Outgoing\\XSD\\MT395.xsd',
            102, 5)))

CTD_ANON._AddElement(
    pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'MTAndDateOfTheOriginalMessage_S'),
        MT395_11S_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location(
            'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\FFXMMConfirmation\\Outgoing\\XSD\\MT395.xsd',
            103, 5)))

CTD_ANON._AddElement(
    pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'NarrativeDescriptionOfTheOriginalMessage'),
        MT395_79_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location(
            'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\FFXMMConfirmation\\Outgoing\\XSD\\MT395.xsd',
            105, 4)))


def _BuildAutomaton():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location(
        'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\FFXMMConfirmation\\Outgoing\\XSD\\MT395.xsd',
        100, 4))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location(
        'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\FFXMMConfirmation\\Outgoing\\XSD\\MT395.xsd',
        101, 4))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location(
        'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\FFXMMConfirmation\\Outgoing\\XSD\\MT395.xsd',
        102, 5))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location(
        'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\FFXMMConfirmation\\Outgoing\\XSD\\MT395.xsd',
        103, 5))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location(
        'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\FFXMMConfirmation\\Outgoing\\XSD\\MT395.xsd',
        105, 4))
    counters.add(cc_4)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'TransactionReferenceNumber')),
        pyxb.utils.utility.Location(
            'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\FFXMMConfirmation\\Outgoing\\XSD\\MT395.xsd',
            97, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'RelatedReference')), pyxb.utils.utility.Location(
            'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\FFXMMConfirmation\\Outgoing\\XSD\\MT395.xsd',
            98, 4))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Queries')),
        pyxb.utils.utility.Location(
            'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\FFXMMConfirmation\\Outgoing\\XSD\\MT395.xsd',
            99, 4))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Narrative')),
        pyxb.utils.utility.Location(
            'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\FFXMMConfirmation\\Outgoing\\XSD\\MT395.xsd',
            100, 4))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(
        CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'MTAndDateOfTheOriginalMessage_R')),
        pyxb.utils.utility.Location(
            'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\FFXMMConfirmation\\Outgoing\\XSD\\MT395.xsd',
            102, 5))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(
        CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'MTAndDateOfTheOriginalMessage_S')),
        pyxb.utils.utility.Location(
            'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\FFXMMConfirmation\\Outgoing\\XSD\\MT395.xsd',
            103, 5))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(
        CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'NarrativeDescriptionOfTheOriginalMessage')),
        pyxb.utils.utility.Location(
            'C:\\Projects\\Swift-Integration_ap\\base\\extensions\\SwiftIntegration\\FFXMMConfirmation\\Outgoing\\XSD\\MT395.xsd',
            105, 4))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
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
    transitions.append(fac.Transition(st_4, [
    ]))
    transitions.append(fac.Transition(st_5, [
    ]))
    transitions.append(fac.Transition(st_6, [
    ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True)]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False)]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, False)]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, False)]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, True),
        fac.UpdateInstruction(cc_2, False)]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, True)]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, True),
        fac.UpdateInstruction(cc_2, False)]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_2, False)]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, True),
        fac.UpdateInstruction(cc_3, False)]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, True),
        fac.UpdateInstruction(cc_3, False)]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_3, True)]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_3, False)]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_4, True)]))
    st_6._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)


CTD_ANON._Automaton = _BuildAutomaton()


