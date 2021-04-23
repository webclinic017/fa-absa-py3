# C:\Projects\Code\SwiftMessagingSolution_Python3\base\extensions\SwiftIntegration\Utilities\XSD\MT210.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:96afad3d20bbfe8d040a1a097fa388d9fecd10e3
# Generated 2019-11-06 16:25:01.144994 by PyXB version 1.2.6 using Python 3.7.4.final.0
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
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:e165725e-0083-11ea-ab7d-509a4c321f2f')

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

def CreateFromDocument (xml_text, default_namespace=None, location_base=None):
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

def CreateFromDOM (node, default_namespace=None):
    """Create a Python instance from the given DOM node.
    The node tag must correspond to an element declaration in this module.

    @deprecated: Forcing use of DOM interface is unnecessary; use L{CreateFromDocument}."""
    if default_namespace is None:
        default_namespace = Namespace.fallbackNamespace()
    return pyxb.binding.basis.element.AnyCreateFromDOM(node, default_namespace)


# Atomic simple type: {http://www.w3schools.com}MT210_SEQUENCE1_20_Type_Pattern
class MT210_SEQUENCE1_20_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT210_SEQUENCE1_20_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 3, 1)
    _Documentation = None
MT210_SEQUENCE1_20_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT210_SEQUENCE1_20_Type_Pattern._CF_pattern.addPattern(pattern="([^/]([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,16}[^/])")
MT210_SEQUENCE1_20_Type_Pattern._InitializeFacetMap(MT210_SEQUENCE1_20_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT210_SEQUENCE1_20_Type_Pattern', MT210_SEQUENCE1_20_Type_Pattern)
_module_typeBindings.MT210_SEQUENCE1_20_Type_Pattern = MT210_SEQUENCE1_20_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT210_SEQUENCE1_25_Type_Pattern
class MT210_SEQUENCE1_25_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT210_SEQUENCE1_25_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 16, 1)
    _Documentation = None
MT210_SEQUENCE1_25_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT210_SEQUENCE1_25_Type_Pattern._CF_pattern.addPattern(pattern="(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35})")
MT210_SEQUENCE1_25_Type_Pattern._InitializeFacetMap(MT210_SEQUENCE1_25_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT210_SEQUENCE1_25_Type_Pattern', MT210_SEQUENCE1_25_Type_Pattern)
_module_typeBindings.MT210_SEQUENCE1_25_Type_Pattern = MT210_SEQUENCE1_25_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT210_SEQUENCE1_30_Type_Pattern
class MT210_SEQUENCE1_30_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT210_SEQUENCE1_30_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 29, 1)
    _Documentation = None
MT210_SEQUENCE1_30_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT210_SEQUENCE1_30_Type_Pattern._CF_pattern.addPattern(pattern='([0-9]{2}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))')
MT210_SEQUENCE1_30_Type_Pattern._InitializeFacetMap(MT210_SEQUENCE1_30_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT210_SEQUENCE1_30_Type_Pattern', MT210_SEQUENCE1_30_Type_Pattern)
_module_typeBindings.MT210_SEQUENCE1_30_Type_Pattern = MT210_SEQUENCE1_30_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT210_SEQUENCE2_21_Type_Pattern
class MT210_SEQUENCE2_21_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT210_SEQUENCE2_21_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 42, 1)
    _Documentation = None
MT210_SEQUENCE2_21_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT210_SEQUENCE2_21_Type_Pattern._CF_pattern.addPattern(pattern="([^/]([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,16}[^/])")
MT210_SEQUENCE2_21_Type_Pattern._InitializeFacetMap(MT210_SEQUENCE2_21_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT210_SEQUENCE2_21_Type_Pattern', MT210_SEQUENCE2_21_Type_Pattern)
_module_typeBindings.MT210_SEQUENCE2_21_Type_Pattern = MT210_SEQUENCE2_21_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT210_SEQUENCE2_32B_Type_Pattern
class MT210_SEQUENCE2_32B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT210_SEQUENCE2_32B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 55, 1)
    _Documentation = None
MT210_SEQUENCE2_32B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT210_SEQUENCE2_32B_Type_Pattern._CF_pattern.addPattern(pattern='((AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})')
MT210_SEQUENCE2_32B_Type_Pattern._InitializeFacetMap(MT210_SEQUENCE2_32B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT210_SEQUENCE2_32B_Type_Pattern', MT210_SEQUENCE2_32B_Type_Pattern)
_module_typeBindings.MT210_SEQUENCE2_32B_Type_Pattern = MT210_SEQUENCE2_32B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT210_SEQUENCE2_50_Type_Pattern
class MT210_SEQUENCE2_50_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT210_SEQUENCE2_50_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 68, 1)
    _Documentation = None
MT210_SEQUENCE2_50_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT210_SEQUENCE2_50_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT210_SEQUENCE2_50_Type_Pattern._InitializeFacetMap(MT210_SEQUENCE2_50_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT210_SEQUENCE2_50_Type_Pattern', MT210_SEQUENCE2_50_Type_Pattern)
_module_typeBindings.MT210_SEQUENCE2_50_Type_Pattern = MT210_SEQUENCE2_50_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT210_SEQUENCE2_50C_Type_Pattern
class MT210_SEQUENCE2_50C_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT210_SEQUENCE2_50C_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 81, 1)
    _Documentation = None
MT210_SEQUENCE2_50C_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT210_SEQUENCE2_50C_Type_Pattern._CF_pattern.addPattern(pattern='([A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)')
MT210_SEQUENCE2_50C_Type_Pattern._InitializeFacetMap(MT210_SEQUENCE2_50C_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT210_SEQUENCE2_50C_Type_Pattern', MT210_SEQUENCE2_50C_Type_Pattern)
_module_typeBindings.MT210_SEQUENCE2_50C_Type_Pattern = MT210_SEQUENCE2_50C_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT210_SEQUENCE2_50F_Type_Pattern
class MT210_SEQUENCE2_50F_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT210_SEQUENCE2_50F_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 94, 1)
    _Documentation = None
MT210_SEQUENCE2_50F_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT210_SEQUENCE2_50F_Type_Pattern._CF_pattern.addPattern(pattern="(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT210_SEQUENCE2_50F_Type_Pattern._InitializeFacetMap(MT210_SEQUENCE2_50F_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT210_SEQUENCE2_50F_Type_Pattern', MT210_SEQUENCE2_50F_Type_Pattern)
_module_typeBindings.MT210_SEQUENCE2_50F_Type_Pattern = MT210_SEQUENCE2_50F_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT210_SEQUENCE2_52A_Type_Pattern
class MT210_SEQUENCE2_52A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT210_SEQUENCE2_52A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 107, 1)
    _Documentation = None
MT210_SEQUENCE2_52A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT210_SEQUENCE2_52A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT210_SEQUENCE2_52A_Type_Pattern._InitializeFacetMap(MT210_SEQUENCE2_52A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT210_SEQUENCE2_52A_Type_Pattern', MT210_SEQUENCE2_52A_Type_Pattern)
_module_typeBindings.MT210_SEQUENCE2_52A_Type_Pattern = MT210_SEQUENCE2_52A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT210_SEQUENCE2_52D_Type_Pattern
class MT210_SEQUENCE2_52D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT210_SEQUENCE2_52D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 120, 1)
    _Documentation = None
MT210_SEQUENCE2_52D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT210_SEQUENCE2_52D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT210_SEQUENCE2_52D_Type_Pattern._InitializeFacetMap(MT210_SEQUENCE2_52D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT210_SEQUENCE2_52D_Type_Pattern', MT210_SEQUENCE2_52D_Type_Pattern)
_module_typeBindings.MT210_SEQUENCE2_52D_Type_Pattern = MT210_SEQUENCE2_52D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT210_SEQUENCE2_56A_Type_Pattern
class MT210_SEQUENCE2_56A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT210_SEQUENCE2_56A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 133, 1)
    _Documentation = None
MT210_SEQUENCE2_56A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT210_SEQUENCE2_56A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT210_SEQUENCE2_56A_Type_Pattern._InitializeFacetMap(MT210_SEQUENCE2_56A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT210_SEQUENCE2_56A_Type_Pattern', MT210_SEQUENCE2_56A_Type_Pattern)
_module_typeBindings.MT210_SEQUENCE2_56A_Type_Pattern = MT210_SEQUENCE2_56A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT210_SEQUENCE2_56D_Type_Pattern
class MT210_SEQUENCE2_56D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT210_SEQUENCE2_56D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 146, 1)
    _Documentation = None
MT210_SEQUENCE2_56D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT210_SEQUENCE2_56D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT210_SEQUENCE2_56D_Type_Pattern._InitializeFacetMap(MT210_SEQUENCE2_56D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT210_SEQUENCE2_56D_Type_Pattern', MT210_SEQUENCE2_56D_Type_Pattern)
_module_typeBindings.MT210_SEQUENCE2_56D_Type_Pattern = MT210_SEQUENCE2_56D_Type_Pattern

# Complex type {http://www.w3schools.com}MT210_SEQUENCE1 with content type ELEMENT_ONLY
class MT210_SEQUENCE1 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT210_SEQUENCE1 with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT210_SEQUENCE1')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 159, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}TransactionReferenceNumber uses Python identifier TransactionReferenceNumber
    __TransactionReferenceNumber = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'TransactionReferenceNumber'), 'TransactionReferenceNumber', '__httpwww_w3schools_com_MT210_SEQUENCE1_httpwww_w3schools_comTransactionReferenceNumber', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 161, 3), )

    
    TransactionReferenceNumber = property(__TransactionReferenceNumber.value, __TransactionReferenceNumber.set, None, None)

    
    # Element {http://www.w3schools.com}AccountIdentification uses Python identifier AccountIdentification
    __AccountIdentification = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'AccountIdentification'), 'AccountIdentification', '__httpwww_w3schools_com_MT210_SEQUENCE1_httpwww_w3schools_comAccountIdentification', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 162, 3), )

    
    AccountIdentification = property(__AccountIdentification.value, __AccountIdentification.set, None, None)

    
    # Element {http://www.w3schools.com}ValueDate uses Python identifier ValueDate
    __ValueDate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ValueDate'), 'ValueDate', '__httpwww_w3schools_com_MT210_SEQUENCE1_httpwww_w3schools_comValueDate', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 163, 3), )

    
    ValueDate = property(__ValueDate.value, __ValueDate.set, None, None)

    _ElementMap.update({
        __TransactionReferenceNumber.name() : __TransactionReferenceNumber,
        __AccountIdentification.name() : __AccountIdentification,
        __ValueDate.name() : __ValueDate
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.MT210_SEQUENCE1 = MT210_SEQUENCE1
Namespace.addCategoryObject('typeBinding', 'MT210_SEQUENCE1', MT210_SEQUENCE1)


# Complex type {http://www.w3schools.com}MT210_SEQUENCE2 with content type ELEMENT_ONLY
class MT210_SEQUENCE2 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT210_SEQUENCE2 with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT210_SEQUENCE2')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 166, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}RelatedReference uses Python identifier RelatedReference
    __RelatedReference = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'RelatedReference'), 'RelatedReference', '__httpwww_w3schools_com_MT210_SEQUENCE2_httpwww_w3schools_comRelatedReference', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 168, 3), )

    
    RelatedReference = property(__RelatedReference.value, __RelatedReference.set, None, None)

    
    # Element {http://www.w3schools.com}CurrencyCodeAmount uses Python identifier CurrencyCodeAmount
    __CurrencyCodeAmount = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CurrencyCodeAmount'), 'CurrencyCodeAmount', '__httpwww_w3schools_com_MT210_SEQUENCE2_httpwww_w3schools_comCurrencyCodeAmount', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 169, 3), )

    
    CurrencyCodeAmount = property(__CurrencyCodeAmount.value, __CurrencyCodeAmount.set, None, None)

    
    # Element {http://www.w3schools.com}OrderingCustomer uses Python identifier OrderingCustomer
    __OrderingCustomer = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'OrderingCustomer'), 'OrderingCustomer', '__httpwww_w3schools_com_MT210_SEQUENCE2_httpwww_w3schools_comOrderingCustomer', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 171, 4), )

    
    OrderingCustomer = property(__OrderingCustomer.value, __OrderingCustomer.set, None, None)

    
    # Element {http://www.w3schools.com}OrderingCustomer_C uses Python identifier OrderingCustomer_C
    __OrderingCustomer_C = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'OrderingCustomer_C'), 'OrderingCustomer_C', '__httpwww_w3schools_com_MT210_SEQUENCE2_httpwww_w3schools_comOrderingCustomer_C', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 172, 4), )

    
    OrderingCustomer_C = property(__OrderingCustomer_C.value, __OrderingCustomer_C.set, None, None)

    
    # Element {http://www.w3schools.com}OrderingCustomer_F uses Python identifier OrderingCustomer_F
    __OrderingCustomer_F = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'OrderingCustomer_F'), 'OrderingCustomer_F', '__httpwww_w3schools_com_MT210_SEQUENCE2_httpwww_w3schools_comOrderingCustomer_F', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 173, 4), )

    
    OrderingCustomer_F = property(__OrderingCustomer_F.value, __OrderingCustomer_F.set, None, None)

    
    # Element {http://www.w3schools.com}OrderingInstitution_A uses Python identifier OrderingInstitution_A
    __OrderingInstitution_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'OrderingInstitution_A'), 'OrderingInstitution_A', '__httpwww_w3schools_com_MT210_SEQUENCE2_httpwww_w3schools_comOrderingInstitution_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 176, 4), )

    
    OrderingInstitution_A = property(__OrderingInstitution_A.value, __OrderingInstitution_A.set, None, None)

    
    # Element {http://www.w3schools.com}OrderingInstitution_D uses Python identifier OrderingInstitution_D
    __OrderingInstitution_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'OrderingInstitution_D'), 'OrderingInstitution_D', '__httpwww_w3schools_com_MT210_SEQUENCE2_httpwww_w3schools_comOrderingInstitution_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 177, 4), )

    
    OrderingInstitution_D = property(__OrderingInstitution_D.value, __OrderingInstitution_D.set, None, None)

    
    # Element {http://www.w3schools.com}Intermedairy_A uses Python identifier Intermedairy_A
    __Intermedairy_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Intermedairy_A'), 'Intermedairy_A', '__httpwww_w3schools_com_MT210_SEQUENCE2_httpwww_w3schools_comIntermedairy_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 180, 4), )

    
    Intermedairy_A = property(__Intermedairy_A.value, __Intermedairy_A.set, None, None)

    
    # Element {http://www.w3schools.com}Intermedairy_D uses Python identifier Intermedairy_D
    __Intermedairy_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Intermedairy_D'), 'Intermedairy_D', '__httpwww_w3schools_com_MT210_SEQUENCE2_httpwww_w3schools_comIntermedairy_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 181, 4), )

    
    Intermedairy_D = property(__Intermedairy_D.value, __Intermedairy_D.set, None, None)

    _ElementMap.update({
        __RelatedReference.name() : __RelatedReference,
        __CurrencyCodeAmount.name() : __CurrencyCodeAmount,
        __OrderingCustomer.name() : __OrderingCustomer,
        __OrderingCustomer_C.name() : __OrderingCustomer_C,
        __OrderingCustomer_F.name() : __OrderingCustomer_F,
        __OrderingInstitution_A.name() : __OrderingInstitution_A,
        __OrderingInstitution_D.name() : __OrderingInstitution_D,
        __Intermedairy_A.name() : __Intermedairy_A,
        __Intermedairy_D.name() : __Intermedairy_D
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.MT210_SEQUENCE2 = MT210_SEQUENCE2
Namespace.addCategoryObject('typeBinding', 'MT210_SEQUENCE2', MT210_SEQUENCE2)


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 186, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}SEQUENCE1 uses Python identifier SEQUENCE1
    __SEQUENCE1 = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SEQUENCE1'), 'SEQUENCE1', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comSEQUENCE1', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 188, 4), )

    
    SEQUENCE1 = property(__SEQUENCE1.value, __SEQUENCE1.set, None, None)

    
    # Element {http://www.w3schools.com}SEQUENCE2 uses Python identifier SEQUENCE2
    __SEQUENCE2 = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SEQUENCE2'), 'SEQUENCE2', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comSEQUENCE2', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 189, 4), )

    
    SEQUENCE2 = property(__SEQUENCE2.value, __SEQUENCE2.set, None, None)

    _ElementMap.update({
        __SEQUENCE1.name() : __SEQUENCE1,
        __SEQUENCE2.name() : __SEQUENCE2
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON = CTD_ANON


# Complex type {http://www.w3schools.com}MT210_SEQUENCE1_20_Type with content type SIMPLE
class MT210_SEQUENCE1_20_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT210_SEQUENCE1_20_Type with content type SIMPLE"""
    _TypeDefinition = MT210_SEQUENCE1_20_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT210_SEQUENCE1_20_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 8, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT210_SEQUENCE1_20_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT210_SEQUENCE1_20_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='20')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 11, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 11, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT210_SEQUENCE1_20_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 12, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 12, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT210_SEQUENCE1_20_Type = MT210_SEQUENCE1_20_Type
Namespace.addCategoryObject('typeBinding', 'MT210_SEQUENCE1_20_Type', MT210_SEQUENCE1_20_Type)


# Complex type {http://www.w3schools.com}MT210_SEQUENCE1_25_Type with content type SIMPLE
class MT210_SEQUENCE1_25_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT210_SEQUENCE1_25_Type with content type SIMPLE"""
    _TypeDefinition = MT210_SEQUENCE1_25_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT210_SEQUENCE1_25_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 21, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT210_SEQUENCE1_25_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT210_SEQUENCE1_25_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='25')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 24, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 24, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT210_SEQUENCE1_25_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 25, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 25, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT210_SEQUENCE1_25_Type = MT210_SEQUENCE1_25_Type
Namespace.addCategoryObject('typeBinding', 'MT210_SEQUENCE1_25_Type', MT210_SEQUENCE1_25_Type)


# Complex type {http://www.w3schools.com}MT210_SEQUENCE1_30_Type with content type SIMPLE
class MT210_SEQUENCE1_30_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT210_SEQUENCE1_30_Type with content type SIMPLE"""
    _TypeDefinition = MT210_SEQUENCE1_30_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT210_SEQUENCE1_30_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 34, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT210_SEQUENCE1_30_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT210_SEQUENCE1_30_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='30')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 37, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 37, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT210_SEQUENCE1_30_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 38, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 38, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT210_SEQUENCE1_30_Type = MT210_SEQUENCE1_30_Type
Namespace.addCategoryObject('typeBinding', 'MT210_SEQUENCE1_30_Type', MT210_SEQUENCE1_30_Type)


# Complex type {http://www.w3schools.com}MT210_SEQUENCE2_21_Type with content type SIMPLE
class MT210_SEQUENCE2_21_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT210_SEQUENCE2_21_Type with content type SIMPLE"""
    _TypeDefinition = MT210_SEQUENCE2_21_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT210_SEQUENCE2_21_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 47, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT210_SEQUENCE2_21_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT210_SEQUENCE2_21_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='21')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 50, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 50, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT210_SEQUENCE2_21_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 51, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 51, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT210_SEQUENCE2_21_Type = MT210_SEQUENCE2_21_Type
Namespace.addCategoryObject('typeBinding', 'MT210_SEQUENCE2_21_Type', MT210_SEQUENCE2_21_Type)


# Complex type {http://www.w3schools.com}MT210_SEQUENCE2_32B_Type with content type SIMPLE
class MT210_SEQUENCE2_32B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT210_SEQUENCE2_32B_Type with content type SIMPLE"""
    _TypeDefinition = MT210_SEQUENCE2_32B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT210_SEQUENCE2_32B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 60, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT210_SEQUENCE2_32B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT210_SEQUENCE2_32B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='32B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 63, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 63, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT210_SEQUENCE2_32B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 64, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 64, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT210_SEQUENCE2_32B_Type = MT210_SEQUENCE2_32B_Type
Namespace.addCategoryObject('typeBinding', 'MT210_SEQUENCE2_32B_Type', MT210_SEQUENCE2_32B_Type)


# Complex type {http://www.w3schools.com}MT210_SEQUENCE2_50_Type with content type SIMPLE
class MT210_SEQUENCE2_50_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT210_SEQUENCE2_50_Type with content type SIMPLE"""
    _TypeDefinition = MT210_SEQUENCE2_50_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT210_SEQUENCE2_50_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 73, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT210_SEQUENCE2_50_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT210_SEQUENCE2_50_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='50')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 76, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 76, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT210_SEQUENCE2_50_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 77, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 77, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT210_SEQUENCE2_50_Type = MT210_SEQUENCE2_50_Type
Namespace.addCategoryObject('typeBinding', 'MT210_SEQUENCE2_50_Type', MT210_SEQUENCE2_50_Type)


# Complex type {http://www.w3schools.com}MT210_SEQUENCE2_50C_Type with content type SIMPLE
class MT210_SEQUENCE2_50C_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT210_SEQUENCE2_50C_Type with content type SIMPLE"""
    _TypeDefinition = MT210_SEQUENCE2_50C_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT210_SEQUENCE2_50C_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 86, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT210_SEQUENCE2_50C_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT210_SEQUENCE2_50C_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='50C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 89, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 89, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT210_SEQUENCE2_50C_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 90, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 90, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT210_SEQUENCE2_50C_Type = MT210_SEQUENCE2_50C_Type
Namespace.addCategoryObject('typeBinding', 'MT210_SEQUENCE2_50C_Type', MT210_SEQUENCE2_50C_Type)


# Complex type {http://www.w3schools.com}MT210_SEQUENCE2_50F_Type with content type SIMPLE
class MT210_SEQUENCE2_50F_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT210_SEQUENCE2_50F_Type with content type SIMPLE"""
    _TypeDefinition = MT210_SEQUENCE2_50F_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT210_SEQUENCE2_50F_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 99, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT210_SEQUENCE2_50F_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT210_SEQUENCE2_50F_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='50F')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 102, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 102, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT210_SEQUENCE2_50F_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 103, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 103, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT210_SEQUENCE2_50F_Type = MT210_SEQUENCE2_50F_Type
Namespace.addCategoryObject('typeBinding', 'MT210_SEQUENCE2_50F_Type', MT210_SEQUENCE2_50F_Type)


# Complex type {http://www.w3schools.com}MT210_SEQUENCE2_52A_Type with content type SIMPLE
class MT210_SEQUENCE2_52A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT210_SEQUENCE2_52A_Type with content type SIMPLE"""
    _TypeDefinition = MT210_SEQUENCE2_52A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT210_SEQUENCE2_52A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 112, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT210_SEQUENCE2_52A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT210_SEQUENCE2_52A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='52A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 115, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 115, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT210_SEQUENCE2_52A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 116, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 116, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT210_SEQUENCE2_52A_Type = MT210_SEQUENCE2_52A_Type
Namespace.addCategoryObject('typeBinding', 'MT210_SEQUENCE2_52A_Type', MT210_SEQUENCE2_52A_Type)


# Complex type {http://www.w3schools.com}MT210_SEQUENCE2_52D_Type with content type SIMPLE
class MT210_SEQUENCE2_52D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT210_SEQUENCE2_52D_Type with content type SIMPLE"""
    _TypeDefinition = MT210_SEQUENCE2_52D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT210_SEQUENCE2_52D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 125, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT210_SEQUENCE2_52D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT210_SEQUENCE2_52D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='52D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 128, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 128, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT210_SEQUENCE2_52D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 129, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 129, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT210_SEQUENCE2_52D_Type = MT210_SEQUENCE2_52D_Type
Namespace.addCategoryObject('typeBinding', 'MT210_SEQUENCE2_52D_Type', MT210_SEQUENCE2_52D_Type)


# Complex type {http://www.w3schools.com}MT210_SEQUENCE2_56A_Type with content type SIMPLE
class MT210_SEQUENCE2_56A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT210_SEQUENCE2_56A_Type with content type SIMPLE"""
    _TypeDefinition = MT210_SEQUENCE2_56A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT210_SEQUENCE2_56A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 138, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT210_SEQUENCE2_56A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT210_SEQUENCE2_56A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='56A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 141, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 141, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT210_SEQUENCE2_56A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 142, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 142, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT210_SEQUENCE2_56A_Type = MT210_SEQUENCE2_56A_Type
Namespace.addCategoryObject('typeBinding', 'MT210_SEQUENCE2_56A_Type', MT210_SEQUENCE2_56A_Type)


# Complex type {http://www.w3schools.com}MT210_SEQUENCE2_56D_Type with content type SIMPLE
class MT210_SEQUENCE2_56D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT210_SEQUENCE2_56D_Type with content type SIMPLE"""
    _TypeDefinition = MT210_SEQUENCE2_56D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT210_SEQUENCE2_56D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 151, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT210_SEQUENCE2_56D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT210_SEQUENCE2_56D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='56D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 154, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 154, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT210_SEQUENCE2_56D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 155, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 155, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT210_SEQUENCE2_56D_Type = MT210_SEQUENCE2_56D_Type
Namespace.addCategoryObject('typeBinding', 'MT210_SEQUENCE2_56D_Type', MT210_SEQUENCE2_56D_Type)


MT210 = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'MT210'), CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 185, 1))
Namespace.addCategoryObject('elementBinding', MT210.name().localName(), MT210)



MT210_SEQUENCE1._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TransactionReferenceNumber'), MT210_SEQUENCE1_20_Type, scope=MT210_SEQUENCE1, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 161, 3)))

MT210_SEQUENCE1._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'AccountIdentification'), MT210_SEQUENCE1_25_Type, scope=MT210_SEQUENCE1, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 162, 3)))

MT210_SEQUENCE1._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ValueDate'), MT210_SEQUENCE1_30_Type, scope=MT210_SEQUENCE1, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 163, 3)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 162, 3))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT210_SEQUENCE1._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'TransactionReferenceNumber')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 161, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT210_SEQUENCE1._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'AccountIdentification')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 162, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT210_SEQUENCE1._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ValueDate')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 163, 3))
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
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
MT210_SEQUENCE1._Automaton = _BuildAutomaton()




MT210_SEQUENCE2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'RelatedReference'), MT210_SEQUENCE2_21_Type, scope=MT210_SEQUENCE2, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 168, 3)))

MT210_SEQUENCE2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CurrencyCodeAmount'), MT210_SEQUENCE2_32B_Type, scope=MT210_SEQUENCE2, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 169, 3)))

MT210_SEQUENCE2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'OrderingCustomer'), MT210_SEQUENCE2_50_Type, scope=MT210_SEQUENCE2, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 171, 4)))

MT210_SEQUENCE2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'OrderingCustomer_C'), MT210_SEQUENCE2_50C_Type, scope=MT210_SEQUENCE2, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 172, 4)))

MT210_SEQUENCE2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'OrderingCustomer_F'), MT210_SEQUENCE2_50F_Type, scope=MT210_SEQUENCE2, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 173, 4)))

MT210_SEQUENCE2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'OrderingInstitution_A'), MT210_SEQUENCE2_52A_Type, scope=MT210_SEQUENCE2, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 176, 4)))

MT210_SEQUENCE2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'OrderingInstitution_D'), MT210_SEQUENCE2_52D_Type, scope=MT210_SEQUENCE2, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 177, 4)))

MT210_SEQUENCE2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Intermedairy_A'), MT210_SEQUENCE2_56A_Type, scope=MT210_SEQUENCE2, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 180, 4)))

MT210_SEQUENCE2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Intermedairy_D'), MT210_SEQUENCE2_56D_Type, scope=MT210_SEQUENCE2, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 181, 4)))

def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 170, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 171, 4))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 172, 4))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 173, 4))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 175, 3))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 176, 4))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 177, 4))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 179, 3))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 180, 4))
    counters.add(cc_8)
    cc_9 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 181, 4))
    counters.add(cc_9)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT210_SEQUENCE2._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'RelatedReference')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 168, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT210_SEQUENCE2._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CurrencyCodeAmount')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 169, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(MT210_SEQUENCE2._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'OrderingCustomer')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 171, 4))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(MT210_SEQUENCE2._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'OrderingCustomer_C')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 172, 4))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(MT210_SEQUENCE2._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'OrderingCustomer_F')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 173, 4))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(MT210_SEQUENCE2._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'OrderingInstitution_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 176, 4))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    final_update.add(fac.UpdateInstruction(cc_6, False))
    symbol = pyxb.binding.content.ElementUse(MT210_SEQUENCE2._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'OrderingInstitution_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 177, 4))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_7, False))
    final_update.add(fac.UpdateInstruction(cc_8, False))
    symbol = pyxb.binding.content.ElementUse(MT210_SEQUENCE2._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Intermedairy_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 180, 4))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_7, False))
    final_update.add(fac.UpdateInstruction(cc_9, False))
    symbol = pyxb.binding.content.ElementUse(MT210_SEQUENCE2._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Intermedairy_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 181, 4))
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    transitions.append(fac.Transition(st_3, [
         ]))
    transitions.append(fac.Transition(st_4, [
         ]))
    transitions.append(fac.Transition(st_5, [
         ]))
    transitions.append(fac.Transition(st_6, [
         ]))
    transitions.append(fac.Transition(st_7, [
         ]))
    transitions.append(fac.Transition(st_8, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True),
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True),
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True),
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_1, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_2, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_3, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_4, True),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_5, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_4, True),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_5, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_4, True),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_4, True),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_6, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_6, False) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_7, True),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_8, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_7, True),
        fac.UpdateInstruction(cc_8, False) ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_7, True),
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_7, True),
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_9, True) ]))
    st_8._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
MT210_SEQUENCE2._Automaton = _BuildAutomaton_()




CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SEQUENCE1'), MT210_SEQUENCE1, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 188, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SEQUENCE2'), MT210_SEQUENCE2, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 189, 4)))

def _BuildAutomaton_2 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_2
    del _BuildAutomaton_2
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SEQUENCE1')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 188, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SEQUENCE2')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT210.xsd', 189, 4))
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
CTD_ANON._Automaton = _BuildAutomaton_2()


