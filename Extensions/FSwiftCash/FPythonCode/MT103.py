# C:\Projects\Code\SwiftMessagingSolution_Python3\base\extensions\SwiftIntegration\Utilities\TemplateFiles\MT103\csv.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:96afad3d20bbfe8d040a1a097fa388d9fecd10e3
# Generated 2019-11-06 12:03:05.126682 by PyXB version 1.2.6 using Python 3.7.4.final.0
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
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:49e2872e-005f-11ea-a5ba-509a4c321f2f')

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


# Atomic simple type: {http://www.w3schools.com}MT103_20_Type_Pattern
class MT103_20_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT103_20_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 3, 1)
    _Documentation = None
MT103_20_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT103_20_Type_Pattern._CF_pattern.addPattern(pattern="([^/]([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,16}[^/])")
MT103_20_Type_Pattern._InitializeFacetMap(MT103_20_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT103_20_Type_Pattern', MT103_20_Type_Pattern)
_module_typeBindings.MT103_20_Type_Pattern = MT103_20_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT103_13C_Type_Pattern
class MT103_13C_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT103_13C_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 16, 1)
    _Documentation = None
MT103_13C_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT103_13C_Type_Pattern._CF_pattern.addPattern(pattern='(/[A-Z0-9]{1,8}/(0[0-9]|[1][0-9]|2[1-3])([0-5][0-9])([+]|[-])(0[0-9]|[1][0-9]|2[1-3])([0-5][0-9]))')
MT103_13C_Type_Pattern._InitializeFacetMap(MT103_13C_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT103_13C_Type_Pattern', MT103_13C_Type_Pattern)
_module_typeBindings.MT103_13C_Type_Pattern = MT103_13C_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT103_23B_Type_Pattern
class MT103_23B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT103_23B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 29, 1)
    _Documentation = None
MT103_23B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT103_23B_Type_Pattern._CF_pattern.addPattern(pattern='((CRED|CRTS|SPAY|SPRI|SSTD))')
MT103_23B_Type_Pattern._InitializeFacetMap(MT103_23B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT103_23B_Type_Pattern', MT103_23B_Type_Pattern)
_module_typeBindings.MT103_23B_Type_Pattern = MT103_23B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT103_23E_Type_Pattern
class MT103_23E_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT103_23E_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 42, 1)
    _Documentation = None
MT103_23E_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT103_23E_Type_Pattern._CF_pattern.addPattern(pattern="((CHQB|CORT|HOLD|INTC|PHOB|PHOI|PHON|REPA|SDVA|TELB|TELE|TELI)(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,30})?)")
MT103_23E_Type_Pattern._InitializeFacetMap(MT103_23E_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT103_23E_Type_Pattern', MT103_23E_Type_Pattern)
_module_typeBindings.MT103_23E_Type_Pattern = MT103_23E_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT103_26T_Type_Pattern
class MT103_26T_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT103_26T_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 55, 1)
    _Documentation = None
MT103_26T_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT103_26T_Type_Pattern._CF_pattern.addPattern(pattern='([A-Z0-9]{3})')
MT103_26T_Type_Pattern._InitializeFacetMap(MT103_26T_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT103_26T_Type_Pattern', MT103_26T_Type_Pattern)
_module_typeBindings.MT103_26T_Type_Pattern = MT103_26T_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT103_32A_Type_Pattern
class MT103_32A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT103_32A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 68, 1)
    _Documentation = None
MT103_32A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT103_32A_Type_Pattern._CF_pattern.addPattern(pattern='([0-9]{2}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})')
MT103_32A_Type_Pattern._InitializeFacetMap(MT103_32A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT103_32A_Type_Pattern', MT103_32A_Type_Pattern)
_module_typeBindings.MT103_32A_Type_Pattern = MT103_32A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT103_33B_Type_Pattern
class MT103_33B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT103_33B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 81, 1)
    _Documentation = None
MT103_33B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT103_33B_Type_Pattern._CF_pattern.addPattern(pattern='((AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})')
MT103_33B_Type_Pattern._InitializeFacetMap(MT103_33B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT103_33B_Type_Pattern', MT103_33B_Type_Pattern)
_module_typeBindings.MT103_33B_Type_Pattern = MT103_33B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT103_36_Type_Pattern
class MT103_36_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT103_36_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 94, 1)
    _Documentation = None
MT103_36_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT103_36_Type_Pattern._CF_pattern.addPattern(pattern='([0-9,(?0-9)]{1,12})')
MT103_36_Type_Pattern._InitializeFacetMap(MT103_36_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT103_36_Type_Pattern', MT103_36_Type_Pattern)
_module_typeBindings.MT103_36_Type_Pattern = MT103_36_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT103_50A_Type_Pattern
class MT103_50A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT103_50A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 107, 1)
    _Documentation = None
MT103_50A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT103_50A_Type_Pattern._CF_pattern.addPattern(pattern="((/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT103_50A_Type_Pattern._InitializeFacetMap(MT103_50A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT103_50A_Type_Pattern', MT103_50A_Type_Pattern)
_module_typeBindings.MT103_50A_Type_Pattern = MT103_50A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT103_50F_Type_Pattern
class MT103_50F_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT103_50F_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 120, 1)
    _Documentation = None
MT103_50F_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT103_50F_Type_Pattern._CF_pattern.addPattern(pattern="(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT103_50F_Type_Pattern._InitializeFacetMap(MT103_50F_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT103_50F_Type_Pattern', MT103_50F_Type_Pattern)
_module_typeBindings.MT103_50F_Type_Pattern = MT103_50F_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT103_50K_Type_Pattern
class MT103_50K_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT103_50K_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 133, 1)
    _Documentation = None
MT103_50K_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT103_50K_Type_Pattern._CF_pattern.addPattern(pattern="((/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT103_50K_Type_Pattern._InitializeFacetMap(MT103_50K_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT103_50K_Type_Pattern', MT103_50K_Type_Pattern)
_module_typeBindings.MT103_50K_Type_Pattern = MT103_50K_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT103_51A_Type_Pattern
class MT103_51A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT103_51A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 146, 1)
    _Documentation = None
MT103_51A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT103_51A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT103_51A_Type_Pattern._InitializeFacetMap(MT103_51A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT103_51A_Type_Pattern', MT103_51A_Type_Pattern)
_module_typeBindings.MT103_51A_Type_Pattern = MT103_51A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT103_52A_Type_Pattern
class MT103_52A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT103_52A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 159, 1)
    _Documentation = None
MT103_52A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT103_52A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT103_52A_Type_Pattern._InitializeFacetMap(MT103_52A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT103_52A_Type_Pattern', MT103_52A_Type_Pattern)
_module_typeBindings.MT103_52A_Type_Pattern = MT103_52A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT103_52D_Type_Pattern
class MT103_52D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT103_52D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 172, 1)
    _Documentation = None
MT103_52D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT103_52D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT103_52D_Type_Pattern._InitializeFacetMap(MT103_52D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT103_52D_Type_Pattern', MT103_52D_Type_Pattern)
_module_typeBindings.MT103_52D_Type_Pattern = MT103_52D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT103_53A_Type_Pattern
class MT103_53A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT103_53A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 185, 1)
    _Documentation = None
MT103_53A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT103_53A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT103_53A_Type_Pattern._InitializeFacetMap(MT103_53A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT103_53A_Type_Pattern', MT103_53A_Type_Pattern)
_module_typeBindings.MT103_53A_Type_Pattern = MT103_53A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT103_53B_Type_Pattern
class MT103_53B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT103_53B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 198, 1)
    _Documentation = None
MT103_53B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT103_53B_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35})?)")
MT103_53B_Type_Pattern._InitializeFacetMap(MT103_53B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT103_53B_Type_Pattern', MT103_53B_Type_Pattern)
_module_typeBindings.MT103_53B_Type_Pattern = MT103_53B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT103_53D_Type_Pattern
class MT103_53D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT103_53D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 211, 1)
    _Documentation = None
MT103_53D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT103_53D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT103_53D_Type_Pattern._InitializeFacetMap(MT103_53D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT103_53D_Type_Pattern', MT103_53D_Type_Pattern)
_module_typeBindings.MT103_53D_Type_Pattern = MT103_53D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT103_54A_Type_Pattern
class MT103_54A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT103_54A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 224, 1)
    _Documentation = None
MT103_54A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT103_54A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT103_54A_Type_Pattern._InitializeFacetMap(MT103_54A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT103_54A_Type_Pattern', MT103_54A_Type_Pattern)
_module_typeBindings.MT103_54A_Type_Pattern = MT103_54A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT103_54B_Type_Pattern
class MT103_54B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT103_54B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 237, 1)
    _Documentation = None
MT103_54B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT103_54B_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35})?)")
MT103_54B_Type_Pattern._InitializeFacetMap(MT103_54B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT103_54B_Type_Pattern', MT103_54B_Type_Pattern)
_module_typeBindings.MT103_54B_Type_Pattern = MT103_54B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT103_54D_Type_Pattern
class MT103_54D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT103_54D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 250, 1)
    _Documentation = None
MT103_54D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT103_54D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT103_54D_Type_Pattern._InitializeFacetMap(MT103_54D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT103_54D_Type_Pattern', MT103_54D_Type_Pattern)
_module_typeBindings.MT103_54D_Type_Pattern = MT103_54D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT103_55A_Type_Pattern
class MT103_55A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT103_55A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 263, 1)
    _Documentation = None
MT103_55A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT103_55A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT103_55A_Type_Pattern._InitializeFacetMap(MT103_55A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT103_55A_Type_Pattern', MT103_55A_Type_Pattern)
_module_typeBindings.MT103_55A_Type_Pattern = MT103_55A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT103_55B_Type_Pattern
class MT103_55B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT103_55B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 276, 1)
    _Documentation = None
MT103_55B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT103_55B_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35})?)")
MT103_55B_Type_Pattern._InitializeFacetMap(MT103_55B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT103_55B_Type_Pattern', MT103_55B_Type_Pattern)
_module_typeBindings.MT103_55B_Type_Pattern = MT103_55B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT103_55D_Type_Pattern
class MT103_55D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT103_55D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 289, 1)
    _Documentation = None
MT103_55D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT103_55D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT103_55D_Type_Pattern._InitializeFacetMap(MT103_55D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT103_55D_Type_Pattern', MT103_55D_Type_Pattern)
_module_typeBindings.MT103_55D_Type_Pattern = MT103_55D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT103_56A_Type_Pattern
class MT103_56A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT103_56A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 302, 1)
    _Documentation = None
MT103_56A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT103_56A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT103_56A_Type_Pattern._InitializeFacetMap(MT103_56A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT103_56A_Type_Pattern', MT103_56A_Type_Pattern)
_module_typeBindings.MT103_56A_Type_Pattern = MT103_56A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT103_56C_Type_Pattern
class MT103_56C_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT103_56C_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 315, 1)
    _Documentation = None
MT103_56C_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT103_56C_Type_Pattern._CF_pattern.addPattern(pattern="(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})")
MT103_56C_Type_Pattern._InitializeFacetMap(MT103_56C_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT103_56C_Type_Pattern', MT103_56C_Type_Pattern)
_module_typeBindings.MT103_56C_Type_Pattern = MT103_56C_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT103_56D_Type_Pattern
class MT103_56D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT103_56D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 328, 1)
    _Documentation = None
MT103_56D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT103_56D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT103_56D_Type_Pattern._InitializeFacetMap(MT103_56D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT103_56D_Type_Pattern', MT103_56D_Type_Pattern)
_module_typeBindings.MT103_56D_Type_Pattern = MT103_56D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT103_57A_Type_Pattern
class MT103_57A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT103_57A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 341, 1)
    _Documentation = None
MT103_57A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT103_57A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT103_57A_Type_Pattern._InitializeFacetMap(MT103_57A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT103_57A_Type_Pattern', MT103_57A_Type_Pattern)
_module_typeBindings.MT103_57A_Type_Pattern = MT103_57A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT103_57B_Type_Pattern
class MT103_57B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT103_57B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 354, 1)
    _Documentation = None
MT103_57B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT103_57B_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35})?)")
MT103_57B_Type_Pattern._InitializeFacetMap(MT103_57B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT103_57B_Type_Pattern', MT103_57B_Type_Pattern)
_module_typeBindings.MT103_57B_Type_Pattern = MT103_57B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT103_57C_Type_Pattern
class MT103_57C_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT103_57C_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 367, 1)
    _Documentation = None
MT103_57C_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT103_57C_Type_Pattern._CF_pattern.addPattern(pattern="(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})")
MT103_57C_Type_Pattern._InitializeFacetMap(MT103_57C_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT103_57C_Type_Pattern', MT103_57C_Type_Pattern)
_module_typeBindings.MT103_57C_Type_Pattern = MT103_57C_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT103_57D_Type_Pattern
class MT103_57D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT103_57D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 380, 1)
    _Documentation = None
MT103_57D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT103_57D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT103_57D_Type_Pattern._InitializeFacetMap(MT103_57D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT103_57D_Type_Pattern', MT103_57D_Type_Pattern)
_module_typeBindings.MT103_57D_Type_Pattern = MT103_57D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT103_59_Type_Pattern
class MT103_59_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT103_59_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 393, 1)
    _Documentation = None
MT103_59_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT103_59_Type_Pattern._CF_pattern.addPattern(pattern="((/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT103_59_Type_Pattern._InitializeFacetMap(MT103_59_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT103_59_Type_Pattern', MT103_59_Type_Pattern)
_module_typeBindings.MT103_59_Type_Pattern = MT103_59_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT103_59A_Type_Pattern
class MT103_59A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT103_59A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 406, 1)
    _Documentation = None
MT103_59A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT103_59A_Type_Pattern._CF_pattern.addPattern(pattern="((/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT103_59A_Type_Pattern._InitializeFacetMap(MT103_59A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT103_59A_Type_Pattern', MT103_59A_Type_Pattern)
_module_typeBindings.MT103_59A_Type_Pattern = MT103_59A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT103_59F_Type_Pattern
class MT103_59F_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT103_59F_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 419, 1)
    _Documentation = None
MT103_59F_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT103_59F_Type_Pattern._CF_pattern.addPattern(pattern="((/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34}\\n)?((1|2|3)/(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,33}\\n?){1,4}))")
MT103_59F_Type_Pattern._InitializeFacetMap(MT103_59F_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT103_59F_Type_Pattern', MT103_59F_Type_Pattern)
_module_typeBindings.MT103_59F_Type_Pattern = MT103_59F_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT103_70_Type_Pattern
class MT103_70_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT103_70_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 432, 1)
    _Documentation = None
MT103_70_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT103_70_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT103_70_Type_Pattern._InitializeFacetMap(MT103_70_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT103_70_Type_Pattern', MT103_70_Type_Pattern)
_module_typeBindings.MT103_70_Type_Pattern = MT103_70_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT103_71A_Type_Pattern
class MT103_71A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT103_71A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 445, 1)
    _Documentation = None
MT103_71A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT103_71A_Type_Pattern._CF_pattern.addPattern(pattern='((BEN|OUR|SHA))')
MT103_71A_Type_Pattern._InitializeFacetMap(MT103_71A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT103_71A_Type_Pattern', MT103_71A_Type_Pattern)
_module_typeBindings.MT103_71A_Type_Pattern = MT103_71A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT103_71F_Type_Pattern
class MT103_71F_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT103_71F_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 458, 1)
    _Documentation = None
MT103_71F_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT103_71F_Type_Pattern._CF_pattern.addPattern(pattern='((AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})')
MT103_71F_Type_Pattern._InitializeFacetMap(MT103_71F_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT103_71F_Type_Pattern', MT103_71F_Type_Pattern)
_module_typeBindings.MT103_71F_Type_Pattern = MT103_71F_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT103_71G_Type_Pattern
class MT103_71G_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT103_71G_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 471, 1)
    _Documentation = None
MT103_71G_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT103_71G_Type_Pattern._CF_pattern.addPattern(pattern='((AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})')
MT103_71G_Type_Pattern._InitializeFacetMap(MT103_71G_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT103_71G_Type_Pattern', MT103_71G_Type_Pattern)
_module_typeBindings.MT103_71G_Type_Pattern = MT103_71G_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT103_72_Type_Pattern
class MT103_72_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT103_72_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 484, 1)
    _Documentation = None
MT103_72_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT103_72_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,6})")
MT103_72_Type_Pattern._InitializeFacetMap(MT103_72_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT103_72_Type_Pattern', MT103_72_Type_Pattern)
_module_typeBindings.MT103_72_Type_Pattern = MT103_72_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT103_77B_Type_Pattern
class MT103_77B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT103_77B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 497, 1)
    _Documentation = None
MT103_77B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT103_77B_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,3})")
MT103_77B_Type_Pattern._InitializeFacetMap(MT103_77B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT103_77B_Type_Pattern', MT103_77B_Type_Pattern)
_module_typeBindings.MT103_77B_Type_Pattern = MT103_77B_Type_Pattern

# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 511, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}SendersReference uses Python identifier SendersReference
    __SendersReference = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SendersReference'), 'SendersReference', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comSendersReference', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 513, 4), )

    
    SendersReference = property(__SendersReference.value, __SendersReference.set, None, None)

    
    # Element {http://www.w3schools.com}TimeIndication uses Python identifier TimeIndication
    __TimeIndication = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'TimeIndication'), 'TimeIndication', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comTimeIndication', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 514, 4), )

    
    TimeIndication = property(__TimeIndication.value, __TimeIndication.set, None, None)

    
    # Element {http://www.w3schools.com}BankOperationCode uses Python identifier BankOperationCode
    __BankOperationCode = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'BankOperationCode'), 'BankOperationCode', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comBankOperationCode', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 515, 4), )

    
    BankOperationCode = property(__BankOperationCode.value, __BankOperationCode.set, None, None)

    
    # Element {http://www.w3schools.com}InstructionCode uses Python identifier InstructionCode
    __InstructionCode = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'InstructionCode'), 'InstructionCode', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comInstructionCode', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 516, 4), )

    
    InstructionCode = property(__InstructionCode.value, __InstructionCode.set, None, None)

    
    # Element {http://www.w3schools.com}TransactionTypeCode uses Python identifier TransactionTypeCode
    __TransactionTypeCode = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'TransactionTypeCode'), 'TransactionTypeCode', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comTransactionTypeCode', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 517, 4), )

    
    TransactionTypeCode = property(__TransactionTypeCode.value, __TransactionTypeCode.set, None, None)

    
    # Element {http://www.w3schools.com}ValueDateCurrencyInterbankSettledAmount uses Python identifier ValueDateCurrencyInterbankSettledAmount
    __ValueDateCurrencyInterbankSettledAmount = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ValueDateCurrencyInterbankSettledAmount'), 'ValueDateCurrencyInterbankSettledAmount', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comValueDateCurrencyInterbankSettledAmount', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 518, 4), )

    
    ValueDateCurrencyInterbankSettledAmount = property(__ValueDateCurrencyInterbankSettledAmount.value, __ValueDateCurrencyInterbankSettledAmount.set, None, None)

    
    # Element {http://www.w3schools.com}CurrencyInstructedAmount uses Python identifier CurrencyInstructedAmount
    __CurrencyInstructedAmount = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CurrencyInstructedAmount'), 'CurrencyInstructedAmount', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comCurrencyInstructedAmount', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 519, 4), )

    
    CurrencyInstructedAmount = property(__CurrencyInstructedAmount.value, __CurrencyInstructedAmount.set, None, None)

    
    # Element {http://www.w3schools.com}ExchangeRate uses Python identifier ExchangeRate
    __ExchangeRate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ExchangeRate'), 'ExchangeRate', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comExchangeRate', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 520, 4), )

    
    ExchangeRate = property(__ExchangeRate.value, __ExchangeRate.set, None, None)

    
    # Element {http://www.w3schools.com}OrderingCustomer_A uses Python identifier OrderingCustomer_A
    __OrderingCustomer_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'OrderingCustomer_A'), 'OrderingCustomer_A', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comOrderingCustomer_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 522, 5), )

    
    OrderingCustomer_A = property(__OrderingCustomer_A.value, __OrderingCustomer_A.set, None, None)

    
    # Element {http://www.w3schools.com}OrderingCustomer_F uses Python identifier OrderingCustomer_F
    __OrderingCustomer_F = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'OrderingCustomer_F'), 'OrderingCustomer_F', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comOrderingCustomer_F', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 523, 5), )

    
    OrderingCustomer_F = property(__OrderingCustomer_F.value, __OrderingCustomer_F.set, None, None)

    
    # Element {http://www.w3schools.com}OrderingCustomer_K uses Python identifier OrderingCustomer_K
    __OrderingCustomer_K = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'OrderingCustomer_K'), 'OrderingCustomer_K', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comOrderingCustomer_K', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 524, 5), )

    
    OrderingCustomer_K = property(__OrderingCustomer_K.value, __OrderingCustomer_K.set, None, None)

    
    # Element {http://www.w3schools.com}SendingInstitution uses Python identifier SendingInstitution
    __SendingInstitution = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SendingInstitution'), 'SendingInstitution', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comSendingInstitution', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 526, 4), )

    
    SendingInstitution = property(__SendingInstitution.value, __SendingInstitution.set, None, None)

    
    # Element {http://www.w3schools.com}OrderingInstitution_A uses Python identifier OrderingInstitution_A
    __OrderingInstitution_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'OrderingInstitution_A'), 'OrderingInstitution_A', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comOrderingInstitution_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 528, 5), )

    
    OrderingInstitution_A = property(__OrderingInstitution_A.value, __OrderingInstitution_A.set, None, None)

    
    # Element {http://www.w3schools.com}OrderingInstitution_D uses Python identifier OrderingInstitution_D
    __OrderingInstitution_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'OrderingInstitution_D'), 'OrderingInstitution_D', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comOrderingInstitution_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 529, 5), )

    
    OrderingInstitution_D = property(__OrderingInstitution_D.value, __OrderingInstitution_D.set, None, None)

    
    # Element {http://www.w3schools.com}SendersCorrespondent_A uses Python identifier SendersCorrespondent_A
    __SendersCorrespondent_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SendersCorrespondent_A'), 'SendersCorrespondent_A', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comSendersCorrespondent_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 532, 5), )

    
    SendersCorrespondent_A = property(__SendersCorrespondent_A.value, __SendersCorrespondent_A.set, None, None)

    
    # Element {http://www.w3schools.com}SendersCorrespondent_B uses Python identifier SendersCorrespondent_B
    __SendersCorrespondent_B = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SendersCorrespondent_B'), 'SendersCorrespondent_B', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comSendersCorrespondent_B', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 533, 5), )

    
    SendersCorrespondent_B = property(__SendersCorrespondent_B.value, __SendersCorrespondent_B.set, None, None)

    
    # Element {http://www.w3schools.com}SendersCorrespondent_D uses Python identifier SendersCorrespondent_D
    __SendersCorrespondent_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SendersCorrespondent_D'), 'SendersCorrespondent_D', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comSendersCorrespondent_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 534, 5), )

    
    SendersCorrespondent_D = property(__SendersCorrespondent_D.value, __SendersCorrespondent_D.set, None, None)

    
    # Element {http://www.w3schools.com}ReceiversCorrespondent_A uses Python identifier ReceiversCorrespondent_A
    __ReceiversCorrespondent_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ReceiversCorrespondent_A'), 'ReceiversCorrespondent_A', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comReceiversCorrespondent_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 537, 5), )

    
    ReceiversCorrespondent_A = property(__ReceiversCorrespondent_A.value, __ReceiversCorrespondent_A.set, None, None)

    
    # Element {http://www.w3schools.com}ReceiversCorrespondent_B uses Python identifier ReceiversCorrespondent_B
    __ReceiversCorrespondent_B = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ReceiversCorrespondent_B'), 'ReceiversCorrespondent_B', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comReceiversCorrespondent_B', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 538, 5), )

    
    ReceiversCorrespondent_B = property(__ReceiversCorrespondent_B.value, __ReceiversCorrespondent_B.set, None, None)

    
    # Element {http://www.w3schools.com}ReceiversCorrespondent_D uses Python identifier ReceiversCorrespondent_D
    __ReceiversCorrespondent_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ReceiversCorrespondent_D'), 'ReceiversCorrespondent_D', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comReceiversCorrespondent_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 539, 5), )

    
    ReceiversCorrespondent_D = property(__ReceiversCorrespondent_D.value, __ReceiversCorrespondent_D.set, None, None)

    
    # Element {http://www.w3schools.com}ThirdReimbursementInstitution_A uses Python identifier ThirdReimbursementInstitution_A
    __ThirdReimbursementInstitution_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ThirdReimbursementInstitution_A'), 'ThirdReimbursementInstitution_A', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comThirdReimbursementInstitution_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 542, 5), )

    
    ThirdReimbursementInstitution_A = property(__ThirdReimbursementInstitution_A.value, __ThirdReimbursementInstitution_A.set, None, None)

    
    # Element {http://www.w3schools.com}ThirdReimbursementInstitution_B uses Python identifier ThirdReimbursementInstitution_B
    __ThirdReimbursementInstitution_B = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ThirdReimbursementInstitution_B'), 'ThirdReimbursementInstitution_B', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comThirdReimbursementInstitution_B', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 543, 5), )

    
    ThirdReimbursementInstitution_B = property(__ThirdReimbursementInstitution_B.value, __ThirdReimbursementInstitution_B.set, None, None)

    
    # Element {http://www.w3schools.com}ThirdReimbursementInstitution_D uses Python identifier ThirdReimbursementInstitution_D
    __ThirdReimbursementInstitution_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ThirdReimbursementInstitution_D'), 'ThirdReimbursementInstitution_D', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comThirdReimbursementInstitution_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 544, 5), )

    
    ThirdReimbursementInstitution_D = property(__ThirdReimbursementInstitution_D.value, __ThirdReimbursementInstitution_D.set, None, None)

    
    # Element {http://www.w3schools.com}IntermediaryInstitution_A uses Python identifier IntermediaryInstitution_A
    __IntermediaryInstitution_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'IntermediaryInstitution_A'), 'IntermediaryInstitution_A', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comIntermediaryInstitution_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 547, 5), )

    
    IntermediaryInstitution_A = property(__IntermediaryInstitution_A.value, __IntermediaryInstitution_A.set, None, None)

    
    # Element {http://www.w3schools.com}IntermediaryInstitution_C uses Python identifier IntermediaryInstitution_C
    __IntermediaryInstitution_C = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'IntermediaryInstitution_C'), 'IntermediaryInstitution_C', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comIntermediaryInstitution_C', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 548, 5), )

    
    IntermediaryInstitution_C = property(__IntermediaryInstitution_C.value, __IntermediaryInstitution_C.set, None, None)

    
    # Element {http://www.w3schools.com}IntermediaryInstitution_D uses Python identifier IntermediaryInstitution_D
    __IntermediaryInstitution_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'IntermediaryInstitution_D'), 'IntermediaryInstitution_D', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comIntermediaryInstitution_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 549, 5), )

    
    IntermediaryInstitution_D = property(__IntermediaryInstitution_D.value, __IntermediaryInstitution_D.set, None, None)

    
    # Element {http://www.w3schools.com}AccountWithInstitution_A uses Python identifier AccountWithInstitution_A
    __AccountWithInstitution_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'AccountWithInstitution_A'), 'AccountWithInstitution_A', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comAccountWithInstitution_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 552, 5), )

    
    AccountWithInstitution_A = property(__AccountWithInstitution_A.value, __AccountWithInstitution_A.set, None, None)

    
    # Element {http://www.w3schools.com}AccountWithInstitution_B uses Python identifier AccountWithInstitution_B
    __AccountWithInstitution_B = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'AccountWithInstitution_B'), 'AccountWithInstitution_B', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comAccountWithInstitution_B', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 553, 5), )

    
    AccountWithInstitution_B = property(__AccountWithInstitution_B.value, __AccountWithInstitution_B.set, None, None)

    
    # Element {http://www.w3schools.com}AccountWithInstitution_C uses Python identifier AccountWithInstitution_C
    __AccountWithInstitution_C = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'AccountWithInstitution_C'), 'AccountWithInstitution_C', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comAccountWithInstitution_C', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 554, 5), )

    
    AccountWithInstitution_C = property(__AccountWithInstitution_C.value, __AccountWithInstitution_C.set, None, None)

    
    # Element {http://www.w3schools.com}AccountWithInstitution_D uses Python identifier AccountWithInstitution_D
    __AccountWithInstitution_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'AccountWithInstitution_D'), 'AccountWithInstitution_D', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comAccountWithInstitution_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 555, 5), )

    
    AccountWithInstitution_D = property(__AccountWithInstitution_D.value, __AccountWithInstitution_D.set, None, None)

    
    # Element {http://www.w3schools.com}BeneficiaryCustomer uses Python identifier BeneficiaryCustomer
    __BeneficiaryCustomer = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryCustomer'), 'BeneficiaryCustomer', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comBeneficiaryCustomer', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 558, 5), )

    
    BeneficiaryCustomer = property(__BeneficiaryCustomer.value, __BeneficiaryCustomer.set, None, None)

    
    # Element {http://www.w3schools.com}BeneficiaryCustomer_A uses Python identifier BeneficiaryCustomer_A
    __BeneficiaryCustomer_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryCustomer_A'), 'BeneficiaryCustomer_A', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comBeneficiaryCustomer_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 559, 5), )

    
    BeneficiaryCustomer_A = property(__BeneficiaryCustomer_A.value, __BeneficiaryCustomer_A.set, None, None)

    
    # Element {http://www.w3schools.com}BeneficiaryCustomer_F uses Python identifier BeneficiaryCustomer_F
    __BeneficiaryCustomer_F = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryCustomer_F'), 'BeneficiaryCustomer_F', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comBeneficiaryCustomer_F', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 560, 5), )

    
    BeneficiaryCustomer_F = property(__BeneficiaryCustomer_F.value, __BeneficiaryCustomer_F.set, None, None)

    
    # Element {http://www.w3schools.com}RemittanceInformation uses Python identifier RemittanceInformation
    __RemittanceInformation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'RemittanceInformation'), 'RemittanceInformation', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comRemittanceInformation', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 562, 4), )

    
    RemittanceInformation = property(__RemittanceInformation.value, __RemittanceInformation.set, None, None)

    
    # Element {http://www.w3schools.com}DetailsOfCharges uses Python identifier DetailsOfCharges
    __DetailsOfCharges = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DetailsOfCharges'), 'DetailsOfCharges', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comDetailsOfCharges', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 563, 4), )

    
    DetailsOfCharges = property(__DetailsOfCharges.value, __DetailsOfCharges.set, None, None)

    
    # Element {http://www.w3schools.com}SendersCharges uses Python identifier SendersCharges
    __SendersCharges = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SendersCharges'), 'SendersCharges', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comSendersCharges', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 564, 4), )

    
    SendersCharges = property(__SendersCharges.value, __SendersCharges.set, None, None)

    
    # Element {http://www.w3schools.com}ReceiversCharges uses Python identifier ReceiversCharges
    __ReceiversCharges = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ReceiversCharges'), 'ReceiversCharges', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comReceiversCharges', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 565, 4), )

    
    ReceiversCharges = property(__ReceiversCharges.value, __ReceiversCharges.set, None, None)

    
    # Element {http://www.w3schools.com}SenderToReceiverInformation uses Python identifier SenderToReceiverInformation
    __SenderToReceiverInformation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SenderToReceiverInformation'), 'SenderToReceiverInformation', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comSenderToReceiverInformation', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 566, 4), )

    
    SenderToReceiverInformation = property(__SenderToReceiverInformation.value, __SenderToReceiverInformation.set, None, None)

    
    # Element {http://www.w3schools.com}RegulatoryReporting uses Python identifier RegulatoryReporting
    __RegulatoryReporting = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'RegulatoryReporting'), 'RegulatoryReporting', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comRegulatoryReporting', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 567, 4), )

    
    RegulatoryReporting = property(__RegulatoryReporting.value, __RegulatoryReporting.set, None, None)

    _ElementMap.update({
        __SendersReference.name() : __SendersReference,
        __TimeIndication.name() : __TimeIndication,
        __BankOperationCode.name() : __BankOperationCode,
        __InstructionCode.name() : __InstructionCode,
        __TransactionTypeCode.name() : __TransactionTypeCode,
        __ValueDateCurrencyInterbankSettledAmount.name() : __ValueDateCurrencyInterbankSettledAmount,
        __CurrencyInstructedAmount.name() : __CurrencyInstructedAmount,
        __ExchangeRate.name() : __ExchangeRate,
        __OrderingCustomer_A.name() : __OrderingCustomer_A,
        __OrderingCustomer_F.name() : __OrderingCustomer_F,
        __OrderingCustomer_K.name() : __OrderingCustomer_K,
        __SendingInstitution.name() : __SendingInstitution,
        __OrderingInstitution_A.name() : __OrderingInstitution_A,
        __OrderingInstitution_D.name() : __OrderingInstitution_D,
        __SendersCorrespondent_A.name() : __SendersCorrespondent_A,
        __SendersCorrespondent_B.name() : __SendersCorrespondent_B,
        __SendersCorrespondent_D.name() : __SendersCorrespondent_D,
        __ReceiversCorrespondent_A.name() : __ReceiversCorrespondent_A,
        __ReceiversCorrespondent_B.name() : __ReceiversCorrespondent_B,
        __ReceiversCorrespondent_D.name() : __ReceiversCorrespondent_D,
        __ThirdReimbursementInstitution_A.name() : __ThirdReimbursementInstitution_A,
        __ThirdReimbursementInstitution_B.name() : __ThirdReimbursementInstitution_B,
        __ThirdReimbursementInstitution_D.name() : __ThirdReimbursementInstitution_D,
        __IntermediaryInstitution_A.name() : __IntermediaryInstitution_A,
        __IntermediaryInstitution_C.name() : __IntermediaryInstitution_C,
        __IntermediaryInstitution_D.name() : __IntermediaryInstitution_D,
        __AccountWithInstitution_A.name() : __AccountWithInstitution_A,
        __AccountWithInstitution_B.name() : __AccountWithInstitution_B,
        __AccountWithInstitution_C.name() : __AccountWithInstitution_C,
        __AccountWithInstitution_D.name() : __AccountWithInstitution_D,
        __BeneficiaryCustomer.name() : __BeneficiaryCustomer,
        __BeneficiaryCustomer_A.name() : __BeneficiaryCustomer_A,
        __BeneficiaryCustomer_F.name() : __BeneficiaryCustomer_F,
        __RemittanceInformation.name() : __RemittanceInformation,
        __DetailsOfCharges.name() : __DetailsOfCharges,
        __SendersCharges.name() : __SendersCharges,
        __ReceiversCharges.name() : __ReceiversCharges,
        __SenderToReceiverInformation.name() : __SenderToReceiverInformation,
        __RegulatoryReporting.name() : __RegulatoryReporting
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON = CTD_ANON


# Complex type {http://www.w3schools.com}MT103_20_Type with content type SIMPLE
class MT103_20_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT103_20_Type with content type SIMPLE"""
    _TypeDefinition = MT103_20_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT103_20_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 8, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT103_20_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT103_20_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='20')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 11, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 11, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT103_20_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 12, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 12, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT103_20_Type = MT103_20_Type
Namespace.addCategoryObject('typeBinding', 'MT103_20_Type', MT103_20_Type)


# Complex type {http://www.w3schools.com}MT103_13C_Type with content type SIMPLE
class MT103_13C_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT103_13C_Type with content type SIMPLE"""
    _TypeDefinition = MT103_13C_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT103_13C_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 21, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT103_13C_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT103_13C_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='13C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 24, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 24, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT103_13C_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 25, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 25, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT103_13C_Type = MT103_13C_Type
Namespace.addCategoryObject('typeBinding', 'MT103_13C_Type', MT103_13C_Type)


# Complex type {http://www.w3schools.com}MT103_23B_Type with content type SIMPLE
class MT103_23B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT103_23B_Type with content type SIMPLE"""
    _TypeDefinition = MT103_23B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT103_23B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 34, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT103_23B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT103_23B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='23B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 37, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 37, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT103_23B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 38, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 38, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT103_23B_Type = MT103_23B_Type
Namespace.addCategoryObject('typeBinding', 'MT103_23B_Type', MT103_23B_Type)


# Complex type {http://www.w3schools.com}MT103_23E_Type with content type SIMPLE
class MT103_23E_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT103_23E_Type with content type SIMPLE"""
    _TypeDefinition = MT103_23E_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT103_23E_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 47, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT103_23E_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT103_23E_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='23E')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 50, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 50, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT103_23E_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 51, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 51, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT103_23E_Type = MT103_23E_Type
Namespace.addCategoryObject('typeBinding', 'MT103_23E_Type', MT103_23E_Type)


# Complex type {http://www.w3schools.com}MT103_26T_Type with content type SIMPLE
class MT103_26T_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT103_26T_Type with content type SIMPLE"""
    _TypeDefinition = MT103_26T_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT103_26T_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 60, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT103_26T_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT103_26T_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='26T')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 63, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 63, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT103_26T_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 64, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 64, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT103_26T_Type = MT103_26T_Type
Namespace.addCategoryObject('typeBinding', 'MT103_26T_Type', MT103_26T_Type)


# Complex type {http://www.w3schools.com}MT103_32A_Type with content type SIMPLE
class MT103_32A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT103_32A_Type with content type SIMPLE"""
    _TypeDefinition = MT103_32A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT103_32A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 73, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT103_32A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT103_32A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='32A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 76, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 76, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT103_32A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 77, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 77, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT103_32A_Type = MT103_32A_Type
Namespace.addCategoryObject('typeBinding', 'MT103_32A_Type', MT103_32A_Type)


# Complex type {http://www.w3schools.com}MT103_33B_Type with content type SIMPLE
class MT103_33B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT103_33B_Type with content type SIMPLE"""
    _TypeDefinition = MT103_33B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT103_33B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 86, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT103_33B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT103_33B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='33B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 89, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 89, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT103_33B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 90, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 90, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT103_33B_Type = MT103_33B_Type
Namespace.addCategoryObject('typeBinding', 'MT103_33B_Type', MT103_33B_Type)


# Complex type {http://www.w3schools.com}MT103_36_Type with content type SIMPLE
class MT103_36_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT103_36_Type with content type SIMPLE"""
    _TypeDefinition = MT103_36_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT103_36_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 99, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT103_36_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT103_36_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='36')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 102, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 102, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT103_36_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 103, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 103, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT103_36_Type = MT103_36_Type
Namespace.addCategoryObject('typeBinding', 'MT103_36_Type', MT103_36_Type)


# Complex type {http://www.w3schools.com}MT103_50A_Type with content type SIMPLE
class MT103_50A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT103_50A_Type with content type SIMPLE"""
    _TypeDefinition = MT103_50A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT103_50A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 112, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT103_50A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT103_50A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='50A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 115, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 115, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT103_50A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 116, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 116, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT103_50A_Type = MT103_50A_Type
Namespace.addCategoryObject('typeBinding', 'MT103_50A_Type', MT103_50A_Type)


# Complex type {http://www.w3schools.com}MT103_50F_Type with content type SIMPLE
class MT103_50F_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT103_50F_Type with content type SIMPLE"""
    _TypeDefinition = MT103_50F_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT103_50F_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 125, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT103_50F_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT103_50F_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='50F')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 128, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 128, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT103_50F_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 129, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 129, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT103_50F_Type = MT103_50F_Type
Namespace.addCategoryObject('typeBinding', 'MT103_50F_Type', MT103_50F_Type)


# Complex type {http://www.w3schools.com}MT103_50K_Type with content type SIMPLE
class MT103_50K_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT103_50K_Type with content type SIMPLE"""
    _TypeDefinition = MT103_50K_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT103_50K_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 138, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT103_50K_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT103_50K_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='50K')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 141, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 141, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT103_50K_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 142, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 142, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT103_50K_Type = MT103_50K_Type
Namespace.addCategoryObject('typeBinding', 'MT103_50K_Type', MT103_50K_Type)


# Complex type {http://www.w3schools.com}MT103_51A_Type with content type SIMPLE
class MT103_51A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT103_51A_Type with content type SIMPLE"""
    _TypeDefinition = MT103_51A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT103_51A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 151, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT103_51A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT103_51A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='51A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 154, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 154, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT103_51A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 155, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 155, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT103_51A_Type = MT103_51A_Type
Namespace.addCategoryObject('typeBinding', 'MT103_51A_Type', MT103_51A_Type)


# Complex type {http://www.w3schools.com}MT103_52A_Type with content type SIMPLE
class MT103_52A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT103_52A_Type with content type SIMPLE"""
    _TypeDefinition = MT103_52A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT103_52A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 164, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT103_52A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT103_52A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='52A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 167, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 167, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT103_52A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 168, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 168, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT103_52A_Type = MT103_52A_Type
Namespace.addCategoryObject('typeBinding', 'MT103_52A_Type', MT103_52A_Type)


# Complex type {http://www.w3schools.com}MT103_52D_Type with content type SIMPLE
class MT103_52D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT103_52D_Type with content type SIMPLE"""
    _TypeDefinition = MT103_52D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT103_52D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 177, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT103_52D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT103_52D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='52D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 180, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 180, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT103_52D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 181, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 181, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT103_52D_Type = MT103_52D_Type
Namespace.addCategoryObject('typeBinding', 'MT103_52D_Type', MT103_52D_Type)


# Complex type {http://www.w3schools.com}MT103_53A_Type with content type SIMPLE
class MT103_53A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT103_53A_Type with content type SIMPLE"""
    _TypeDefinition = MT103_53A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT103_53A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 190, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT103_53A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT103_53A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='53A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 193, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 193, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT103_53A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 194, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 194, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT103_53A_Type = MT103_53A_Type
Namespace.addCategoryObject('typeBinding', 'MT103_53A_Type', MT103_53A_Type)


# Complex type {http://www.w3schools.com}MT103_53B_Type with content type SIMPLE
class MT103_53B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT103_53B_Type with content type SIMPLE"""
    _TypeDefinition = MT103_53B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT103_53B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 203, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT103_53B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT103_53B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='53B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 206, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 206, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT103_53B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 207, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 207, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT103_53B_Type = MT103_53B_Type
Namespace.addCategoryObject('typeBinding', 'MT103_53B_Type', MT103_53B_Type)


# Complex type {http://www.w3schools.com}MT103_53D_Type with content type SIMPLE
class MT103_53D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT103_53D_Type with content type SIMPLE"""
    _TypeDefinition = MT103_53D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT103_53D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 216, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT103_53D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT103_53D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='53D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 219, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 219, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT103_53D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 220, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 220, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT103_53D_Type = MT103_53D_Type
Namespace.addCategoryObject('typeBinding', 'MT103_53D_Type', MT103_53D_Type)


# Complex type {http://www.w3schools.com}MT103_54A_Type with content type SIMPLE
class MT103_54A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT103_54A_Type with content type SIMPLE"""
    _TypeDefinition = MT103_54A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT103_54A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 229, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT103_54A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT103_54A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='54A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 232, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 232, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT103_54A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 233, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 233, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT103_54A_Type = MT103_54A_Type
Namespace.addCategoryObject('typeBinding', 'MT103_54A_Type', MT103_54A_Type)


# Complex type {http://www.w3schools.com}MT103_54B_Type with content type SIMPLE
class MT103_54B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT103_54B_Type with content type SIMPLE"""
    _TypeDefinition = MT103_54B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT103_54B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 242, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT103_54B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT103_54B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='54B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 245, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 245, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT103_54B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 246, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 246, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT103_54B_Type = MT103_54B_Type
Namespace.addCategoryObject('typeBinding', 'MT103_54B_Type', MT103_54B_Type)


# Complex type {http://www.w3schools.com}MT103_54D_Type with content type SIMPLE
class MT103_54D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT103_54D_Type with content type SIMPLE"""
    _TypeDefinition = MT103_54D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT103_54D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 255, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT103_54D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT103_54D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='54D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 258, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 258, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT103_54D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 259, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 259, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT103_54D_Type = MT103_54D_Type
Namespace.addCategoryObject('typeBinding', 'MT103_54D_Type', MT103_54D_Type)


# Complex type {http://www.w3schools.com}MT103_55A_Type with content type SIMPLE
class MT103_55A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT103_55A_Type with content type SIMPLE"""
    _TypeDefinition = MT103_55A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT103_55A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 268, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT103_55A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT103_55A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='55A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 271, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 271, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT103_55A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 272, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 272, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT103_55A_Type = MT103_55A_Type
Namespace.addCategoryObject('typeBinding', 'MT103_55A_Type', MT103_55A_Type)


# Complex type {http://www.w3schools.com}MT103_55B_Type with content type SIMPLE
class MT103_55B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT103_55B_Type with content type SIMPLE"""
    _TypeDefinition = MT103_55B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT103_55B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 281, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT103_55B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT103_55B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='55B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 284, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 284, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT103_55B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 285, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 285, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT103_55B_Type = MT103_55B_Type
Namespace.addCategoryObject('typeBinding', 'MT103_55B_Type', MT103_55B_Type)


# Complex type {http://www.w3schools.com}MT103_55D_Type with content type SIMPLE
class MT103_55D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT103_55D_Type with content type SIMPLE"""
    _TypeDefinition = MT103_55D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT103_55D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 294, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT103_55D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT103_55D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='55D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 297, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 297, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT103_55D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 298, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 298, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT103_55D_Type = MT103_55D_Type
Namespace.addCategoryObject('typeBinding', 'MT103_55D_Type', MT103_55D_Type)


# Complex type {http://www.w3schools.com}MT103_56A_Type with content type SIMPLE
class MT103_56A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT103_56A_Type with content type SIMPLE"""
    _TypeDefinition = MT103_56A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT103_56A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 307, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT103_56A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT103_56A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='56A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 310, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 310, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT103_56A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 311, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 311, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT103_56A_Type = MT103_56A_Type
Namespace.addCategoryObject('typeBinding', 'MT103_56A_Type', MT103_56A_Type)


# Complex type {http://www.w3schools.com}MT103_56C_Type with content type SIMPLE
class MT103_56C_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT103_56C_Type with content type SIMPLE"""
    _TypeDefinition = MT103_56C_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT103_56C_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 320, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT103_56C_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT103_56C_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='56C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 323, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 323, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT103_56C_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 324, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 324, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT103_56C_Type = MT103_56C_Type
Namespace.addCategoryObject('typeBinding', 'MT103_56C_Type', MT103_56C_Type)


# Complex type {http://www.w3schools.com}MT103_56D_Type with content type SIMPLE
class MT103_56D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT103_56D_Type with content type SIMPLE"""
    _TypeDefinition = MT103_56D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT103_56D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 333, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT103_56D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT103_56D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='56D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 336, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 336, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT103_56D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 337, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 337, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT103_56D_Type = MT103_56D_Type
Namespace.addCategoryObject('typeBinding', 'MT103_56D_Type', MT103_56D_Type)


# Complex type {http://www.w3schools.com}MT103_57A_Type with content type SIMPLE
class MT103_57A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT103_57A_Type with content type SIMPLE"""
    _TypeDefinition = MT103_57A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT103_57A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 346, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT103_57A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT103_57A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='57A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 349, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 349, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT103_57A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 350, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 350, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT103_57A_Type = MT103_57A_Type
Namespace.addCategoryObject('typeBinding', 'MT103_57A_Type', MT103_57A_Type)


# Complex type {http://www.w3schools.com}MT103_57B_Type with content type SIMPLE
class MT103_57B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT103_57B_Type with content type SIMPLE"""
    _TypeDefinition = MT103_57B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT103_57B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 359, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT103_57B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT103_57B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='57B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 362, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 362, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT103_57B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 363, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 363, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT103_57B_Type = MT103_57B_Type
Namespace.addCategoryObject('typeBinding', 'MT103_57B_Type', MT103_57B_Type)


# Complex type {http://www.w3schools.com}MT103_57C_Type with content type SIMPLE
class MT103_57C_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT103_57C_Type with content type SIMPLE"""
    _TypeDefinition = MT103_57C_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT103_57C_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 372, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT103_57C_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT103_57C_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='57C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 375, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 375, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT103_57C_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 376, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 376, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT103_57C_Type = MT103_57C_Type
Namespace.addCategoryObject('typeBinding', 'MT103_57C_Type', MT103_57C_Type)


# Complex type {http://www.w3schools.com}MT103_57D_Type with content type SIMPLE
class MT103_57D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT103_57D_Type with content type SIMPLE"""
    _TypeDefinition = MT103_57D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT103_57D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 385, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT103_57D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT103_57D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='57D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 388, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 388, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT103_57D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 389, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 389, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT103_57D_Type = MT103_57D_Type
Namespace.addCategoryObject('typeBinding', 'MT103_57D_Type', MT103_57D_Type)


# Complex type {http://www.w3schools.com}MT103_59_Type with content type SIMPLE
class MT103_59_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT103_59_Type with content type SIMPLE"""
    _TypeDefinition = MT103_59_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT103_59_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 398, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT103_59_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT103_59_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='59')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 401, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 401, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT103_59_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 402, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 402, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT103_59_Type = MT103_59_Type
Namespace.addCategoryObject('typeBinding', 'MT103_59_Type', MT103_59_Type)


# Complex type {http://www.w3schools.com}MT103_59A_Type with content type SIMPLE
class MT103_59A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT103_59A_Type with content type SIMPLE"""
    _TypeDefinition = MT103_59A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT103_59A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 411, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT103_59A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT103_59A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='59A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 414, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 414, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT103_59A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 415, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 415, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT103_59A_Type = MT103_59A_Type
Namespace.addCategoryObject('typeBinding', 'MT103_59A_Type', MT103_59A_Type)


# Complex type {http://www.w3schools.com}MT103_59F_Type with content type SIMPLE
class MT103_59F_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT103_59F_Type with content type SIMPLE"""
    _TypeDefinition = MT103_59F_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT103_59F_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 424, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT103_59F_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT103_59F_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='59F')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 427, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 427, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT103_59F_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 428, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 428, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT103_59F_Type = MT103_59F_Type
Namespace.addCategoryObject('typeBinding', 'MT103_59F_Type', MT103_59F_Type)


# Complex type {http://www.w3schools.com}MT103_70_Type with content type SIMPLE
class MT103_70_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT103_70_Type with content type SIMPLE"""
    _TypeDefinition = MT103_70_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT103_70_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 437, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT103_70_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT103_70_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='70')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 440, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 440, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT103_70_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 441, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 441, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT103_70_Type = MT103_70_Type
Namespace.addCategoryObject('typeBinding', 'MT103_70_Type', MT103_70_Type)


# Complex type {http://www.w3schools.com}MT103_71A_Type with content type SIMPLE
class MT103_71A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT103_71A_Type with content type SIMPLE"""
    _TypeDefinition = MT103_71A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT103_71A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 450, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT103_71A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT103_71A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='71A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 453, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 453, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT103_71A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 454, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 454, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT103_71A_Type = MT103_71A_Type
Namespace.addCategoryObject('typeBinding', 'MT103_71A_Type', MT103_71A_Type)


# Complex type {http://www.w3schools.com}MT103_71F_Type with content type SIMPLE
class MT103_71F_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT103_71F_Type with content type SIMPLE"""
    _TypeDefinition = MT103_71F_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT103_71F_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 463, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT103_71F_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT103_71F_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='71F')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 466, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 466, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT103_71F_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 467, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 467, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT103_71F_Type = MT103_71F_Type
Namespace.addCategoryObject('typeBinding', 'MT103_71F_Type', MT103_71F_Type)


# Complex type {http://www.w3schools.com}MT103_71G_Type with content type SIMPLE
class MT103_71G_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT103_71G_Type with content type SIMPLE"""
    _TypeDefinition = MT103_71G_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT103_71G_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 476, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT103_71G_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT103_71G_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='71G')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 479, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 479, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT103_71G_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 480, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 480, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT103_71G_Type = MT103_71G_Type
Namespace.addCategoryObject('typeBinding', 'MT103_71G_Type', MT103_71G_Type)


# Complex type {http://www.w3schools.com}MT103_72_Type with content type SIMPLE
class MT103_72_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT103_72_Type with content type SIMPLE"""
    _TypeDefinition = MT103_72_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT103_72_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 489, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT103_72_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT103_72_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='72')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 492, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 492, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT103_72_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 493, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 493, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT103_72_Type = MT103_72_Type
Namespace.addCategoryObject('typeBinding', 'MT103_72_Type', MT103_72_Type)


# Complex type {http://www.w3schools.com}MT103_77B_Type with content type SIMPLE
class MT103_77B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT103_77B_Type with content type SIMPLE"""
    _TypeDefinition = MT103_77B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT103_77B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 502, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT103_77B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT103_77B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='77B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 505, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 505, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT103_77B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 506, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 506, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT103_77B_Type = MT103_77B_Type
Namespace.addCategoryObject('typeBinding', 'MT103_77B_Type', MT103_77B_Type)


MT103 = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'MT103'), CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 510, 1))
Namespace.addCategoryObject('elementBinding', MT103.name().localName(), MT103)



CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SendersReference'), MT103_20_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 513, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TimeIndication'), MT103_13C_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 514, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'BankOperationCode'), MT103_23B_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 515, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'InstructionCode'), MT103_23E_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 516, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TransactionTypeCode'), MT103_26T_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 517, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ValueDateCurrencyInterbankSettledAmount'), MT103_32A_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 518, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CurrencyInstructedAmount'), MT103_33B_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 519, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ExchangeRate'), MT103_36_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 520, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'OrderingCustomer_A'), MT103_50A_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 522, 5)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'OrderingCustomer_F'), MT103_50F_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 523, 5)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'OrderingCustomer_K'), MT103_50K_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 524, 5)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SendingInstitution'), MT103_51A_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 526, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'OrderingInstitution_A'), MT103_52A_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 528, 5)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'OrderingInstitution_D'), MT103_52D_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 529, 5)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SendersCorrespondent_A'), MT103_53A_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 532, 5)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SendersCorrespondent_B'), MT103_53B_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 533, 5)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SendersCorrespondent_D'), MT103_53D_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 534, 5)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ReceiversCorrespondent_A'), MT103_54A_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 537, 5)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ReceiversCorrespondent_B'), MT103_54B_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 538, 5)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ReceiversCorrespondent_D'), MT103_54D_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 539, 5)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ThirdReimbursementInstitution_A'), MT103_55A_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 542, 5)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ThirdReimbursementInstitution_B'), MT103_55B_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 543, 5)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ThirdReimbursementInstitution_D'), MT103_55D_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 544, 5)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'IntermediaryInstitution_A'), MT103_56A_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 547, 5)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'IntermediaryInstitution_C'), MT103_56C_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 548, 5)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'IntermediaryInstitution_D'), MT103_56D_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 549, 5)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'AccountWithInstitution_A'), MT103_57A_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 552, 5)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'AccountWithInstitution_B'), MT103_57B_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 553, 5)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'AccountWithInstitution_C'), MT103_57C_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 554, 5)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'AccountWithInstitution_D'), MT103_57D_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 555, 5)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryCustomer'), MT103_59_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 558, 5)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryCustomer_A'), MT103_59A_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 559, 5)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryCustomer_F'), MT103_59F_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 560, 5)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'RemittanceInformation'), MT103_70_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 562, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DetailsOfCharges'), MT103_71A_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 563, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SendersCharges'), MT103_71F_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 564, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ReceiversCharges'), MT103_71G_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 565, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SenderToReceiverInformation'), MT103_72_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 566, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'RegulatoryReporting'), MT103_77B_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 567, 4)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 514, 4))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 516, 4))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 517, 4))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 519, 4))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 520, 4))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 526, 4))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 527, 4))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 528, 5))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 529, 5))
    counters.add(cc_8)
    cc_9 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 531, 4))
    counters.add(cc_9)
    cc_10 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 532, 5))
    counters.add(cc_10)
    cc_11 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 533, 5))
    counters.add(cc_11)
    cc_12 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 534, 5))
    counters.add(cc_12)
    cc_13 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 536, 4))
    counters.add(cc_13)
    cc_14 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 537, 5))
    counters.add(cc_14)
    cc_15 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 538, 5))
    counters.add(cc_15)
    cc_16 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 539, 5))
    counters.add(cc_16)
    cc_17 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 541, 4))
    counters.add(cc_17)
    cc_18 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 542, 5))
    counters.add(cc_18)
    cc_19 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 543, 5))
    counters.add(cc_19)
    cc_20 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 544, 5))
    counters.add(cc_20)
    cc_21 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 546, 4))
    counters.add(cc_21)
    cc_22 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 547, 5))
    counters.add(cc_22)
    cc_23 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 548, 5))
    counters.add(cc_23)
    cc_24 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 549, 5))
    counters.add(cc_24)
    cc_25 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 551, 4))
    counters.add(cc_25)
    cc_26 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 552, 5))
    counters.add(cc_26)
    cc_27 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 553, 5))
    counters.add(cc_27)
    cc_28 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 554, 5))
    counters.add(cc_28)
    cc_29 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 555, 5))
    counters.add(cc_29)
    cc_30 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 562, 4))
    counters.add(cc_30)
    cc_31 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 564, 4))
    counters.add(cc_31)
    cc_32 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 565, 4))
    counters.add(cc_32)
    cc_33 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 566, 4))
    counters.add(cc_33)
    cc_34 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 567, 4))
    counters.add(cc_34)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SendersReference')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 513, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'TimeIndication')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 514, 4))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'BankOperationCode')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 515, 4))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'InstructionCode')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 516, 4))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'TransactionTypeCode')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 517, 4))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ValueDateCurrencyInterbankSettledAmount')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 518, 4))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CurrencyInstructedAmount')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 519, 4))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ExchangeRate')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 520, 4))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'OrderingCustomer_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 522, 5))
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'OrderingCustomer_F')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 523, 5))
    st_9 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'OrderingCustomer_K')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 524, 5))
    st_10 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SendingInstitution')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 526, 4))
    st_11 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'OrderingInstitution_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 528, 5))
    st_12 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_12)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'OrderingInstitution_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 529, 5))
    st_13 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_13)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SendersCorrespondent_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 532, 5))
    st_14 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_14)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SendersCorrespondent_B')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 533, 5))
    st_15 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_15)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SendersCorrespondent_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 534, 5))
    st_16 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_16)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ReceiversCorrespondent_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 537, 5))
    st_17 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_17)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ReceiversCorrespondent_B')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 538, 5))
    st_18 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_18)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ReceiversCorrespondent_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 539, 5))
    st_19 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_19)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ThirdReimbursementInstitution_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 542, 5))
    st_20 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_20)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ThirdReimbursementInstitution_B')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 543, 5))
    st_21 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_21)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ThirdReimbursementInstitution_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 544, 5))
    st_22 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_22)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'IntermediaryInstitution_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 547, 5))
    st_23 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_23)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'IntermediaryInstitution_C')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 548, 5))
    st_24 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_24)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'IntermediaryInstitution_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 549, 5))
    st_25 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_25)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'AccountWithInstitution_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 552, 5))
    st_26 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_26)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'AccountWithInstitution_B')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 553, 5))
    st_27 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_27)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'AccountWithInstitution_C')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 554, 5))
    st_28 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_28)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'AccountWithInstitution_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 555, 5))
    st_29 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_29)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryCustomer')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 558, 5))
    st_30 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_30)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryCustomer_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 559, 5))
    st_31 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_31)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryCustomer_F')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 560, 5))
    st_32 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_32)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'RemittanceInformation')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 562, 4))
    st_33 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_33)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DetailsOfCharges')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 563, 4))
    st_34 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_34)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_31, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SendersCharges')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 564, 4))
    st_35 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_35)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_32, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ReceiversCharges')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 565, 4))
    st_36 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_36)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_33, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SenderToReceiverInformation')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 566, 4))
    st_37 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_37)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_34, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'RegulatoryReporting')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT103.csv.xsd', 567, 4))
    st_38 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_38)
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
    transitions.append(fac.Transition(st_3, [
         ]))
    transitions.append(fac.Transition(st_4, [
         ]))
    transitions.append(fac.Transition(st_5, [
         ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
         ]))
    transitions.append(fac.Transition(st_7, [
         ]))
    transitions.append(fac.Transition(st_8, [
         ]))
    transitions.append(fac.Transition(st_9, [
         ]))
    transitions.append(fac.Transition(st_10, [
         ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_4, False) ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_11, [
         ]))
    transitions.append(fac.Transition(st_12, [
         ]))
    transitions.append(fac.Transition(st_13, [
         ]))
    transitions.append(fac.Transition(st_14, [
         ]))
    transitions.append(fac.Transition(st_15, [
         ]))
    transitions.append(fac.Transition(st_16, [
         ]))
    transitions.append(fac.Transition(st_17, [
         ]))
    transitions.append(fac.Transition(st_18, [
         ]))
    transitions.append(fac.Transition(st_19, [
         ]))
    transitions.append(fac.Transition(st_20, [
         ]))
    transitions.append(fac.Transition(st_21, [
         ]))
    transitions.append(fac.Transition(st_22, [
         ]))
    transitions.append(fac.Transition(st_23, [
         ]))
    transitions.append(fac.Transition(st_24, [
         ]))
    transitions.append(fac.Transition(st_25, [
         ]))
    transitions.append(fac.Transition(st_26, [
         ]))
    transitions.append(fac.Transition(st_27, [
         ]))
    transitions.append(fac.Transition(st_28, [
         ]))
    transitions.append(fac.Transition(st_29, [
         ]))
    transitions.append(fac.Transition(st_30, [
         ]))
    transitions.append(fac.Transition(st_31, [
         ]))
    transitions.append(fac.Transition(st_32, [
         ]))
    st_8._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_11, [
         ]))
    transitions.append(fac.Transition(st_12, [
         ]))
    transitions.append(fac.Transition(st_13, [
         ]))
    transitions.append(fac.Transition(st_14, [
         ]))
    transitions.append(fac.Transition(st_15, [
         ]))
    transitions.append(fac.Transition(st_16, [
         ]))
    transitions.append(fac.Transition(st_17, [
         ]))
    transitions.append(fac.Transition(st_18, [
         ]))
    transitions.append(fac.Transition(st_19, [
         ]))
    transitions.append(fac.Transition(st_20, [
         ]))
    transitions.append(fac.Transition(st_21, [
         ]))
    transitions.append(fac.Transition(st_22, [
         ]))
    transitions.append(fac.Transition(st_23, [
         ]))
    transitions.append(fac.Transition(st_24, [
         ]))
    transitions.append(fac.Transition(st_25, [
         ]))
    transitions.append(fac.Transition(st_26, [
         ]))
    transitions.append(fac.Transition(st_27, [
         ]))
    transitions.append(fac.Transition(st_28, [
         ]))
    transitions.append(fac.Transition(st_29, [
         ]))
    transitions.append(fac.Transition(st_30, [
         ]))
    transitions.append(fac.Transition(st_31, [
         ]))
    transitions.append(fac.Transition(st_32, [
         ]))
    st_9._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_11, [
         ]))
    transitions.append(fac.Transition(st_12, [
         ]))
    transitions.append(fac.Transition(st_13, [
         ]))
    transitions.append(fac.Transition(st_14, [
         ]))
    transitions.append(fac.Transition(st_15, [
         ]))
    transitions.append(fac.Transition(st_16, [
         ]))
    transitions.append(fac.Transition(st_17, [
         ]))
    transitions.append(fac.Transition(st_18, [
         ]))
    transitions.append(fac.Transition(st_19, [
         ]))
    transitions.append(fac.Transition(st_20, [
         ]))
    transitions.append(fac.Transition(st_21, [
         ]))
    transitions.append(fac.Transition(st_22, [
         ]))
    transitions.append(fac.Transition(st_23, [
         ]))
    transitions.append(fac.Transition(st_24, [
         ]))
    transitions.append(fac.Transition(st_25, [
         ]))
    transitions.append(fac.Transition(st_26, [
         ]))
    transitions.append(fac.Transition(st_27, [
         ]))
    transitions.append(fac.Transition(st_28, [
         ]))
    transitions.append(fac.Transition(st_29, [
         ]))
    transitions.append(fac.Transition(st_30, [
         ]))
    transitions.append(fac.Transition(st_31, [
         ]))
    transitions.append(fac.Transition(st_32, [
         ]))
    st_10._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_5, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_27, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_28, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_29, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_30, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_31, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_32, [
        fac.UpdateInstruction(cc_5, False) ]))
    st_11._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_6, True),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_7, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_6, True),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_6, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_6, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_6, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_6, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_6, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_6, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_6, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_6, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_6, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_6, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_6, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_6, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_6, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_27, [
        fac.UpdateInstruction(cc_6, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_28, [
        fac.UpdateInstruction(cc_6, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_29, [
        fac.UpdateInstruction(cc_6, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_30, [
        fac.UpdateInstruction(cc_6, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_31, [
        fac.UpdateInstruction(cc_6, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_32, [
        fac.UpdateInstruction(cc_6, False),
        fac.UpdateInstruction(cc_7, False) ]))
    st_12._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_6, True),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_6, True),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_8, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_6, False),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_6, False),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_6, False),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_6, False),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_6, False),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_6, False),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_6, False),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_6, False),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_6, False),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_6, False),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_6, False),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_6, False),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_6, False),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_27, [
        fac.UpdateInstruction(cc_6, False),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_28, [
        fac.UpdateInstruction(cc_6, False),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_29, [
        fac.UpdateInstruction(cc_6, False),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_30, [
        fac.UpdateInstruction(cc_6, False),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_31, [
        fac.UpdateInstruction(cc_6, False),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_32, [
        fac.UpdateInstruction(cc_6, False),
        fac.UpdateInstruction(cc_8, False) ]))
    st_13._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_9, True),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_10, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_9, True),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_9, True),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_9, False),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_9, False),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_9, False),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_9, False),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_9, False),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_9, False),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_9, False),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_9, False),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_9, False),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_9, False),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_27, [
        fac.UpdateInstruction(cc_9, False),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_28, [
        fac.UpdateInstruction(cc_9, False),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_29, [
        fac.UpdateInstruction(cc_9, False),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_30, [
        fac.UpdateInstruction(cc_9, False),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_31, [
        fac.UpdateInstruction(cc_9, False),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_32, [
        fac.UpdateInstruction(cc_9, False),
        fac.UpdateInstruction(cc_10, False) ]))
    st_14._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_9, True),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_9, True),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_11, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_9, True),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_9, False),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_9, False),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_9, False),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_9, False),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_9, False),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_9, False),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_9, False),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_9, False),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_9, False),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_9, False),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_27, [
        fac.UpdateInstruction(cc_9, False),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_28, [
        fac.UpdateInstruction(cc_9, False),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_29, [
        fac.UpdateInstruction(cc_9, False),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_30, [
        fac.UpdateInstruction(cc_9, False),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_31, [
        fac.UpdateInstruction(cc_9, False),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_32, [
        fac.UpdateInstruction(cc_9, False),
        fac.UpdateInstruction(cc_11, False) ]))
    st_15._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_9, True),
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_9, True),
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_9, True),
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_12, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_9, False),
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_9, False),
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_9, False),
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_9, False),
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_9, False),
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_9, False),
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_9, False),
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_9, False),
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_9, False),
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_9, False),
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_27, [
        fac.UpdateInstruction(cc_9, False),
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_28, [
        fac.UpdateInstruction(cc_9, False),
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_29, [
        fac.UpdateInstruction(cc_9, False),
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_30, [
        fac.UpdateInstruction(cc_9, False),
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_31, [
        fac.UpdateInstruction(cc_9, False),
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_32, [
        fac.UpdateInstruction(cc_9, False),
        fac.UpdateInstruction(cc_12, False) ]))
    st_16._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_13, True),
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_14, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_13, True),
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_13, True),
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_13, False),
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_13, False),
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_13, False),
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_13, False),
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_13, False),
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_13, False),
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_13, False),
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_27, [
        fac.UpdateInstruction(cc_13, False),
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_28, [
        fac.UpdateInstruction(cc_13, False),
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_29, [
        fac.UpdateInstruction(cc_13, False),
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_30, [
        fac.UpdateInstruction(cc_13, False),
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_31, [
        fac.UpdateInstruction(cc_13, False),
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_32, [
        fac.UpdateInstruction(cc_13, False),
        fac.UpdateInstruction(cc_14, False) ]))
    st_17._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_13, True),
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_13, True),
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_15, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_13, True),
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_13, False),
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_13, False),
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_13, False),
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_13, False),
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_13, False),
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_13, False),
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_13, False),
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_27, [
        fac.UpdateInstruction(cc_13, False),
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_28, [
        fac.UpdateInstruction(cc_13, False),
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_29, [
        fac.UpdateInstruction(cc_13, False),
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_30, [
        fac.UpdateInstruction(cc_13, False),
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_31, [
        fac.UpdateInstruction(cc_13, False),
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_32, [
        fac.UpdateInstruction(cc_13, False),
        fac.UpdateInstruction(cc_15, False) ]))
    st_18._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_13, True),
        fac.UpdateInstruction(cc_16, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_13, True),
        fac.UpdateInstruction(cc_16, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_13, True),
        fac.UpdateInstruction(cc_16, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_16, True) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_13, False),
        fac.UpdateInstruction(cc_16, False) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_13, False),
        fac.UpdateInstruction(cc_16, False) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_13, False),
        fac.UpdateInstruction(cc_16, False) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_13, False),
        fac.UpdateInstruction(cc_16, False) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_13, False),
        fac.UpdateInstruction(cc_16, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_13, False),
        fac.UpdateInstruction(cc_16, False) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_13, False),
        fac.UpdateInstruction(cc_16, False) ]))
    transitions.append(fac.Transition(st_27, [
        fac.UpdateInstruction(cc_13, False),
        fac.UpdateInstruction(cc_16, False) ]))
    transitions.append(fac.Transition(st_28, [
        fac.UpdateInstruction(cc_13, False),
        fac.UpdateInstruction(cc_16, False) ]))
    transitions.append(fac.Transition(st_29, [
        fac.UpdateInstruction(cc_13, False),
        fac.UpdateInstruction(cc_16, False) ]))
    transitions.append(fac.Transition(st_30, [
        fac.UpdateInstruction(cc_13, False),
        fac.UpdateInstruction(cc_16, False) ]))
    transitions.append(fac.Transition(st_31, [
        fac.UpdateInstruction(cc_13, False),
        fac.UpdateInstruction(cc_16, False) ]))
    transitions.append(fac.Transition(st_32, [
        fac.UpdateInstruction(cc_13, False),
        fac.UpdateInstruction(cc_16, False) ]))
    st_19._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_17, True),
        fac.UpdateInstruction(cc_18, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_18, True) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_17, True),
        fac.UpdateInstruction(cc_18, False) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_17, True),
        fac.UpdateInstruction(cc_18, False) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_17, False),
        fac.UpdateInstruction(cc_18, False) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_17, False),
        fac.UpdateInstruction(cc_18, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_17, False),
        fac.UpdateInstruction(cc_18, False) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_17, False),
        fac.UpdateInstruction(cc_18, False) ]))
    transitions.append(fac.Transition(st_27, [
        fac.UpdateInstruction(cc_17, False),
        fac.UpdateInstruction(cc_18, False) ]))
    transitions.append(fac.Transition(st_28, [
        fac.UpdateInstruction(cc_17, False),
        fac.UpdateInstruction(cc_18, False) ]))
    transitions.append(fac.Transition(st_29, [
        fac.UpdateInstruction(cc_17, False),
        fac.UpdateInstruction(cc_18, False) ]))
    transitions.append(fac.Transition(st_30, [
        fac.UpdateInstruction(cc_17, False),
        fac.UpdateInstruction(cc_18, False) ]))
    transitions.append(fac.Transition(st_31, [
        fac.UpdateInstruction(cc_17, False),
        fac.UpdateInstruction(cc_18, False) ]))
    transitions.append(fac.Transition(st_32, [
        fac.UpdateInstruction(cc_17, False),
        fac.UpdateInstruction(cc_18, False) ]))
    st_20._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_17, True),
        fac.UpdateInstruction(cc_19, False) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_17, True),
        fac.UpdateInstruction(cc_19, False) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_19, True) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_17, True),
        fac.UpdateInstruction(cc_19, False) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_17, False),
        fac.UpdateInstruction(cc_19, False) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_17, False),
        fac.UpdateInstruction(cc_19, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_17, False),
        fac.UpdateInstruction(cc_19, False) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_17, False),
        fac.UpdateInstruction(cc_19, False) ]))
    transitions.append(fac.Transition(st_27, [
        fac.UpdateInstruction(cc_17, False),
        fac.UpdateInstruction(cc_19, False) ]))
    transitions.append(fac.Transition(st_28, [
        fac.UpdateInstruction(cc_17, False),
        fac.UpdateInstruction(cc_19, False) ]))
    transitions.append(fac.Transition(st_29, [
        fac.UpdateInstruction(cc_17, False),
        fac.UpdateInstruction(cc_19, False) ]))
    transitions.append(fac.Transition(st_30, [
        fac.UpdateInstruction(cc_17, False),
        fac.UpdateInstruction(cc_19, False) ]))
    transitions.append(fac.Transition(st_31, [
        fac.UpdateInstruction(cc_17, False),
        fac.UpdateInstruction(cc_19, False) ]))
    transitions.append(fac.Transition(st_32, [
        fac.UpdateInstruction(cc_17, False),
        fac.UpdateInstruction(cc_19, False) ]))
    st_21._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_17, True),
        fac.UpdateInstruction(cc_20, False) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_17, True),
        fac.UpdateInstruction(cc_20, False) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_17, True),
        fac.UpdateInstruction(cc_20, False) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_20, True) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_17, False),
        fac.UpdateInstruction(cc_20, False) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_17, False),
        fac.UpdateInstruction(cc_20, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_17, False),
        fac.UpdateInstruction(cc_20, False) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_17, False),
        fac.UpdateInstruction(cc_20, False) ]))
    transitions.append(fac.Transition(st_27, [
        fac.UpdateInstruction(cc_17, False),
        fac.UpdateInstruction(cc_20, False) ]))
    transitions.append(fac.Transition(st_28, [
        fac.UpdateInstruction(cc_17, False),
        fac.UpdateInstruction(cc_20, False) ]))
    transitions.append(fac.Transition(st_29, [
        fac.UpdateInstruction(cc_17, False),
        fac.UpdateInstruction(cc_20, False) ]))
    transitions.append(fac.Transition(st_30, [
        fac.UpdateInstruction(cc_17, False),
        fac.UpdateInstruction(cc_20, False) ]))
    transitions.append(fac.Transition(st_31, [
        fac.UpdateInstruction(cc_17, False),
        fac.UpdateInstruction(cc_20, False) ]))
    transitions.append(fac.Transition(st_32, [
        fac.UpdateInstruction(cc_17, False),
        fac.UpdateInstruction(cc_20, False) ]))
    st_22._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_21, True),
        fac.UpdateInstruction(cc_22, False) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_22, True) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_21, True),
        fac.UpdateInstruction(cc_22, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_21, True),
        fac.UpdateInstruction(cc_22, False) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_21, False),
        fac.UpdateInstruction(cc_22, False) ]))
    transitions.append(fac.Transition(st_27, [
        fac.UpdateInstruction(cc_21, False),
        fac.UpdateInstruction(cc_22, False) ]))
    transitions.append(fac.Transition(st_28, [
        fac.UpdateInstruction(cc_21, False),
        fac.UpdateInstruction(cc_22, False) ]))
    transitions.append(fac.Transition(st_29, [
        fac.UpdateInstruction(cc_21, False),
        fac.UpdateInstruction(cc_22, False) ]))
    transitions.append(fac.Transition(st_30, [
        fac.UpdateInstruction(cc_21, False),
        fac.UpdateInstruction(cc_22, False) ]))
    transitions.append(fac.Transition(st_31, [
        fac.UpdateInstruction(cc_21, False),
        fac.UpdateInstruction(cc_22, False) ]))
    transitions.append(fac.Transition(st_32, [
        fac.UpdateInstruction(cc_21, False),
        fac.UpdateInstruction(cc_22, False) ]))
    st_23._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_21, True),
        fac.UpdateInstruction(cc_23, False) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_21, True),
        fac.UpdateInstruction(cc_23, False) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_23, True) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_21, True),
        fac.UpdateInstruction(cc_23, False) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_21, False),
        fac.UpdateInstruction(cc_23, False) ]))
    transitions.append(fac.Transition(st_27, [
        fac.UpdateInstruction(cc_21, False),
        fac.UpdateInstruction(cc_23, False) ]))
    transitions.append(fac.Transition(st_28, [
        fac.UpdateInstruction(cc_21, False),
        fac.UpdateInstruction(cc_23, False) ]))
    transitions.append(fac.Transition(st_29, [
        fac.UpdateInstruction(cc_21, False),
        fac.UpdateInstruction(cc_23, False) ]))
    transitions.append(fac.Transition(st_30, [
        fac.UpdateInstruction(cc_21, False),
        fac.UpdateInstruction(cc_23, False) ]))
    transitions.append(fac.Transition(st_31, [
        fac.UpdateInstruction(cc_21, False),
        fac.UpdateInstruction(cc_23, False) ]))
    transitions.append(fac.Transition(st_32, [
        fac.UpdateInstruction(cc_21, False),
        fac.UpdateInstruction(cc_23, False) ]))
    st_24._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_21, True),
        fac.UpdateInstruction(cc_24, False) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_21, True),
        fac.UpdateInstruction(cc_24, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_21, True),
        fac.UpdateInstruction(cc_24, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_24, True) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_21, False),
        fac.UpdateInstruction(cc_24, False) ]))
    transitions.append(fac.Transition(st_27, [
        fac.UpdateInstruction(cc_21, False),
        fac.UpdateInstruction(cc_24, False) ]))
    transitions.append(fac.Transition(st_28, [
        fac.UpdateInstruction(cc_21, False),
        fac.UpdateInstruction(cc_24, False) ]))
    transitions.append(fac.Transition(st_29, [
        fac.UpdateInstruction(cc_21, False),
        fac.UpdateInstruction(cc_24, False) ]))
    transitions.append(fac.Transition(st_30, [
        fac.UpdateInstruction(cc_21, False),
        fac.UpdateInstruction(cc_24, False) ]))
    transitions.append(fac.Transition(st_31, [
        fac.UpdateInstruction(cc_21, False),
        fac.UpdateInstruction(cc_24, False) ]))
    transitions.append(fac.Transition(st_32, [
        fac.UpdateInstruction(cc_21, False),
        fac.UpdateInstruction(cc_24, False) ]))
    st_25._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_25, True),
        fac.UpdateInstruction(cc_26, False) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_26, True) ]))
    transitions.append(fac.Transition(st_27, [
        fac.UpdateInstruction(cc_25, True),
        fac.UpdateInstruction(cc_26, False) ]))
    transitions.append(fac.Transition(st_28, [
        fac.UpdateInstruction(cc_25, True),
        fac.UpdateInstruction(cc_26, False) ]))
    transitions.append(fac.Transition(st_29, [
        fac.UpdateInstruction(cc_25, True),
        fac.UpdateInstruction(cc_26, False) ]))
    transitions.append(fac.Transition(st_30, [
        fac.UpdateInstruction(cc_25, False),
        fac.UpdateInstruction(cc_26, False) ]))
    transitions.append(fac.Transition(st_31, [
        fac.UpdateInstruction(cc_25, False),
        fac.UpdateInstruction(cc_26, False) ]))
    transitions.append(fac.Transition(st_32, [
        fac.UpdateInstruction(cc_25, False),
        fac.UpdateInstruction(cc_26, False) ]))
    st_26._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_25, True),
        fac.UpdateInstruction(cc_27, False) ]))
    transitions.append(fac.Transition(st_27, [
        fac.UpdateInstruction(cc_25, True),
        fac.UpdateInstruction(cc_27, False) ]))
    transitions.append(fac.Transition(st_27, [
        fac.UpdateInstruction(cc_27, True) ]))
    transitions.append(fac.Transition(st_28, [
        fac.UpdateInstruction(cc_25, True),
        fac.UpdateInstruction(cc_27, False) ]))
    transitions.append(fac.Transition(st_29, [
        fac.UpdateInstruction(cc_25, True),
        fac.UpdateInstruction(cc_27, False) ]))
    transitions.append(fac.Transition(st_30, [
        fac.UpdateInstruction(cc_25, False),
        fac.UpdateInstruction(cc_27, False) ]))
    transitions.append(fac.Transition(st_31, [
        fac.UpdateInstruction(cc_25, False),
        fac.UpdateInstruction(cc_27, False) ]))
    transitions.append(fac.Transition(st_32, [
        fac.UpdateInstruction(cc_25, False),
        fac.UpdateInstruction(cc_27, False) ]))
    st_27._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_25, True),
        fac.UpdateInstruction(cc_28, False) ]))
    transitions.append(fac.Transition(st_27, [
        fac.UpdateInstruction(cc_25, True),
        fac.UpdateInstruction(cc_28, False) ]))
    transitions.append(fac.Transition(st_28, [
        fac.UpdateInstruction(cc_25, True),
        fac.UpdateInstruction(cc_28, False) ]))
    transitions.append(fac.Transition(st_28, [
        fac.UpdateInstruction(cc_28, True) ]))
    transitions.append(fac.Transition(st_29, [
        fac.UpdateInstruction(cc_25, True),
        fac.UpdateInstruction(cc_28, False) ]))
    transitions.append(fac.Transition(st_30, [
        fac.UpdateInstruction(cc_25, False),
        fac.UpdateInstruction(cc_28, False) ]))
    transitions.append(fac.Transition(st_31, [
        fac.UpdateInstruction(cc_25, False),
        fac.UpdateInstruction(cc_28, False) ]))
    transitions.append(fac.Transition(st_32, [
        fac.UpdateInstruction(cc_25, False),
        fac.UpdateInstruction(cc_28, False) ]))
    st_28._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_25, True),
        fac.UpdateInstruction(cc_29, False) ]))
    transitions.append(fac.Transition(st_27, [
        fac.UpdateInstruction(cc_25, True),
        fac.UpdateInstruction(cc_29, False) ]))
    transitions.append(fac.Transition(st_28, [
        fac.UpdateInstruction(cc_25, True),
        fac.UpdateInstruction(cc_29, False) ]))
    transitions.append(fac.Transition(st_29, [
        fac.UpdateInstruction(cc_25, True),
        fac.UpdateInstruction(cc_29, False) ]))
    transitions.append(fac.Transition(st_29, [
        fac.UpdateInstruction(cc_29, True) ]))
    transitions.append(fac.Transition(st_30, [
        fac.UpdateInstruction(cc_25, False),
        fac.UpdateInstruction(cc_29, False) ]))
    transitions.append(fac.Transition(st_31, [
        fac.UpdateInstruction(cc_25, False),
        fac.UpdateInstruction(cc_29, False) ]))
    transitions.append(fac.Transition(st_32, [
        fac.UpdateInstruction(cc_25, False),
        fac.UpdateInstruction(cc_29, False) ]))
    st_29._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_33, [
         ]))
    transitions.append(fac.Transition(st_34, [
         ]))
    st_30._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_33, [
         ]))
    transitions.append(fac.Transition(st_34, [
         ]))
    st_31._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_33, [
         ]))
    transitions.append(fac.Transition(st_34, [
         ]))
    st_32._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_33, [
        fac.UpdateInstruction(cc_30, True) ]))
    transitions.append(fac.Transition(st_34, [
        fac.UpdateInstruction(cc_30, False) ]))
    st_33._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_35, [
         ]))
    transitions.append(fac.Transition(st_36, [
         ]))
    transitions.append(fac.Transition(st_37, [
         ]))
    transitions.append(fac.Transition(st_38, [
         ]))
    st_34._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_35, [
        fac.UpdateInstruction(cc_31, True) ]))
    transitions.append(fac.Transition(st_36, [
        fac.UpdateInstruction(cc_31, False) ]))
    transitions.append(fac.Transition(st_37, [
        fac.UpdateInstruction(cc_31, False) ]))
    transitions.append(fac.Transition(st_38, [
        fac.UpdateInstruction(cc_31, False) ]))
    st_35._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_36, [
        fac.UpdateInstruction(cc_32, True) ]))
    transitions.append(fac.Transition(st_37, [
        fac.UpdateInstruction(cc_32, False) ]))
    transitions.append(fac.Transition(st_38, [
        fac.UpdateInstruction(cc_32, False) ]))
    st_36._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_37, [
        fac.UpdateInstruction(cc_33, True) ]))
    transitions.append(fac.Transition(st_38, [
        fac.UpdateInstruction(cc_33, False) ]))
    st_37._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_38, [
        fac.UpdateInstruction(cc_34, True) ]))
    st_38._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON._Automaton = _BuildAutomaton()


