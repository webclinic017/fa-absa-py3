# C:\Projects\Code\SwiftMessagingSolution_Python3\base\extensions\SwiftIntegration\Utilities\TemplateFiles\MT202\csv.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:96afad3d20bbfe8d040a1a097fa388d9fecd10e3
# Generated 2019-11-06 15:04:07.546863 by PyXB version 1.2.6 using Python 3.7.4.final.0
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
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:947389de-0078-11ea-8dc7-509a4c321f2f')

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


# Atomic simple type: {http://www.w3schools.com}MT202_20_Type_Pattern
class MT202_20_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202_20_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 3, 1)
    _Documentation = None
MT202_20_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT202_20_Type_Pattern._CF_pattern.addPattern(pattern="([^/]([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,16}[^/])")
MT202_20_Type_Pattern._InitializeFacetMap(MT202_20_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT202_20_Type_Pattern', MT202_20_Type_Pattern)
_module_typeBindings.MT202_20_Type_Pattern = MT202_20_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT202_21_Type_Pattern
class MT202_21_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202_21_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 16, 1)
    _Documentation = None
MT202_21_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT202_21_Type_Pattern._CF_pattern.addPattern(pattern="([^/]([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,16}[^/])")
MT202_21_Type_Pattern._InitializeFacetMap(MT202_21_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT202_21_Type_Pattern', MT202_21_Type_Pattern)
_module_typeBindings.MT202_21_Type_Pattern = MT202_21_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT202_13C_Type_Pattern
class MT202_13C_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202_13C_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 29, 1)
    _Documentation = None
MT202_13C_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT202_13C_Type_Pattern._CF_pattern.addPattern(pattern='(/(CLSTIME|RNCTIME|SNDTIME)/(0[0-9]|[1][0-9]|2[1-3])([0-5][0-9])([+]|[-])(0[0-9]|[1][0-9]|2[1-3])([0-5][0-9]))')
MT202_13C_Type_Pattern._InitializeFacetMap(MT202_13C_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT202_13C_Type_Pattern', MT202_13C_Type_Pattern)
_module_typeBindings.MT202_13C_Type_Pattern = MT202_13C_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT202_32A_Type_Pattern
class MT202_32A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202_32A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 42, 1)
    _Documentation = None
MT202_32A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT202_32A_Type_Pattern._CF_pattern.addPattern(pattern='([0-9]{2}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})')
MT202_32A_Type_Pattern._InitializeFacetMap(MT202_32A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT202_32A_Type_Pattern', MT202_32A_Type_Pattern)
_module_typeBindings.MT202_32A_Type_Pattern = MT202_32A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT202_52A_Type_Pattern
class MT202_52A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202_52A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 55, 1)
    _Documentation = None
MT202_52A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT202_52A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT202_52A_Type_Pattern._InitializeFacetMap(MT202_52A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT202_52A_Type_Pattern', MT202_52A_Type_Pattern)
_module_typeBindings.MT202_52A_Type_Pattern = MT202_52A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT202_52D_Type_Pattern
class MT202_52D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202_52D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 68, 1)
    _Documentation = None
MT202_52D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT202_52D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT202_52D_Type_Pattern._InitializeFacetMap(MT202_52D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT202_52D_Type_Pattern', MT202_52D_Type_Pattern)
_module_typeBindings.MT202_52D_Type_Pattern = MT202_52D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT202_53A_Type_Pattern
class MT202_53A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202_53A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 81, 1)
    _Documentation = None
MT202_53A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT202_53A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT202_53A_Type_Pattern._InitializeFacetMap(MT202_53A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT202_53A_Type_Pattern', MT202_53A_Type_Pattern)
_module_typeBindings.MT202_53A_Type_Pattern = MT202_53A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT202_53B_Type_Pattern
class MT202_53B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202_53B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 94, 1)
    _Documentation = None
MT202_53B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT202_53B_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35})?)")
MT202_53B_Type_Pattern._InitializeFacetMap(MT202_53B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT202_53B_Type_Pattern', MT202_53B_Type_Pattern)
_module_typeBindings.MT202_53B_Type_Pattern = MT202_53B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT202_53D_Type_Pattern
class MT202_53D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202_53D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 107, 1)
    _Documentation = None
MT202_53D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT202_53D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT202_53D_Type_Pattern._InitializeFacetMap(MT202_53D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT202_53D_Type_Pattern', MT202_53D_Type_Pattern)
_module_typeBindings.MT202_53D_Type_Pattern = MT202_53D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT202_54A_Type_Pattern
class MT202_54A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202_54A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 120, 1)
    _Documentation = None
MT202_54A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT202_54A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT202_54A_Type_Pattern._InitializeFacetMap(MT202_54A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT202_54A_Type_Pattern', MT202_54A_Type_Pattern)
_module_typeBindings.MT202_54A_Type_Pattern = MT202_54A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT202_54B_Type_Pattern
class MT202_54B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202_54B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 133, 1)
    _Documentation = None
MT202_54B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT202_54B_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35})?)")
MT202_54B_Type_Pattern._InitializeFacetMap(MT202_54B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT202_54B_Type_Pattern', MT202_54B_Type_Pattern)
_module_typeBindings.MT202_54B_Type_Pattern = MT202_54B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT202_54D_Type_Pattern
class MT202_54D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202_54D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 146, 1)
    _Documentation = None
MT202_54D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT202_54D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT202_54D_Type_Pattern._InitializeFacetMap(MT202_54D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT202_54D_Type_Pattern', MT202_54D_Type_Pattern)
_module_typeBindings.MT202_54D_Type_Pattern = MT202_54D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT202_56A_Type_Pattern
class MT202_56A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202_56A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 159, 1)
    _Documentation = None
MT202_56A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT202_56A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT202_56A_Type_Pattern._InitializeFacetMap(MT202_56A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT202_56A_Type_Pattern', MT202_56A_Type_Pattern)
_module_typeBindings.MT202_56A_Type_Pattern = MT202_56A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT202_56D_Type_Pattern
class MT202_56D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202_56D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 172, 1)
    _Documentation = None
MT202_56D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT202_56D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT202_56D_Type_Pattern._InitializeFacetMap(MT202_56D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT202_56D_Type_Pattern', MT202_56D_Type_Pattern)
_module_typeBindings.MT202_56D_Type_Pattern = MT202_56D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT202_57A_Type_Pattern
class MT202_57A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202_57A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 185, 1)
    _Documentation = None
MT202_57A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT202_57A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT202_57A_Type_Pattern._InitializeFacetMap(MT202_57A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT202_57A_Type_Pattern', MT202_57A_Type_Pattern)
_module_typeBindings.MT202_57A_Type_Pattern = MT202_57A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT202_57B_Type_Pattern
class MT202_57B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202_57B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 198, 1)
    _Documentation = None
MT202_57B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT202_57B_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35})?)")
MT202_57B_Type_Pattern._InitializeFacetMap(MT202_57B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT202_57B_Type_Pattern', MT202_57B_Type_Pattern)
_module_typeBindings.MT202_57B_Type_Pattern = MT202_57B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT202_57D_Type_Pattern
class MT202_57D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202_57D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 211, 1)
    _Documentation = None
MT202_57D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT202_57D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT202_57D_Type_Pattern._InitializeFacetMap(MT202_57D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT202_57D_Type_Pattern', MT202_57D_Type_Pattern)
_module_typeBindings.MT202_57D_Type_Pattern = MT202_57D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT202_58A_Type_Pattern
class MT202_58A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202_58A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 224, 1)
    _Documentation = None
MT202_58A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT202_58A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT202_58A_Type_Pattern._InitializeFacetMap(MT202_58A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT202_58A_Type_Pattern', MT202_58A_Type_Pattern)
_module_typeBindings.MT202_58A_Type_Pattern = MT202_58A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT202_58D_Type_Pattern
class MT202_58D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202_58D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 237, 1)
    _Documentation = None
MT202_58D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT202_58D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT202_58D_Type_Pattern._InitializeFacetMap(MT202_58D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT202_58D_Type_Pattern', MT202_58D_Type_Pattern)
_module_typeBindings.MT202_58D_Type_Pattern = MT202_58D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT202_72_Type_Pattern
class MT202_72_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202_72_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 250, 1)
    _Documentation = None
MT202_72_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT202_72_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,6})")
MT202_72_Type_Pattern._InitializeFacetMap(MT202_72_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT202_72_Type_Pattern', MT202_72_Type_Pattern)
_module_typeBindings.MT202_72_Type_Pattern = MT202_72_Type_Pattern

# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 264, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}TransactionReferenceNumber uses Python identifier TransactionReferenceNumber
    __TransactionReferenceNumber = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'TransactionReferenceNumber'), 'TransactionReferenceNumber', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comTransactionReferenceNumber', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 266, 4), )

    
    TransactionReferenceNumber = property(__TransactionReferenceNumber.value, __TransactionReferenceNumber.set, None, None)

    
    # Element {http://www.w3schools.com}RelatedReference uses Python identifier RelatedReference
    __RelatedReference = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'RelatedReference'), 'RelatedReference', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comRelatedReference', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 267, 4), )

    
    RelatedReference = property(__RelatedReference.value, __RelatedReference.set, None, None)

    
    # Element {http://www.w3schools.com}TimeIndication uses Python identifier TimeIndication
    __TimeIndication = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'TimeIndication'), 'TimeIndication', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comTimeIndication', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 268, 4), )

    
    TimeIndication = property(__TimeIndication.value, __TimeIndication.set, None, None)

    
    # Element {http://www.w3schools.com}ValueDateCurrencyCodeAmount uses Python identifier ValueDateCurrencyCodeAmount
    __ValueDateCurrencyCodeAmount = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ValueDateCurrencyCodeAmount'), 'ValueDateCurrencyCodeAmount', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comValueDateCurrencyCodeAmount', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 269, 4), )

    
    ValueDateCurrencyCodeAmount = property(__ValueDateCurrencyCodeAmount.value, __ValueDateCurrencyCodeAmount.set, None, None)

    
    # Element {http://www.w3schools.com}OrderingInstitution_A uses Python identifier OrderingInstitution_A
    __OrderingInstitution_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'OrderingInstitution_A'), 'OrderingInstitution_A', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comOrderingInstitution_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 271, 5), )

    
    OrderingInstitution_A = property(__OrderingInstitution_A.value, __OrderingInstitution_A.set, None, None)

    
    # Element {http://www.w3schools.com}OrderingInstitution_D uses Python identifier OrderingInstitution_D
    __OrderingInstitution_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'OrderingInstitution_D'), 'OrderingInstitution_D', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comOrderingInstitution_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 272, 5), )

    
    OrderingInstitution_D = property(__OrderingInstitution_D.value, __OrderingInstitution_D.set, None, None)

    
    # Element {http://www.w3schools.com}SendersCorrespondent_A uses Python identifier SendersCorrespondent_A
    __SendersCorrespondent_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SendersCorrespondent_A'), 'SendersCorrespondent_A', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comSendersCorrespondent_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 275, 5), )

    
    SendersCorrespondent_A = property(__SendersCorrespondent_A.value, __SendersCorrespondent_A.set, None, None)

    
    # Element {http://www.w3schools.com}SendersCorrespondent_B uses Python identifier SendersCorrespondent_B
    __SendersCorrespondent_B = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SendersCorrespondent_B'), 'SendersCorrespondent_B', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comSendersCorrespondent_B', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 276, 5), )

    
    SendersCorrespondent_B = property(__SendersCorrespondent_B.value, __SendersCorrespondent_B.set, None, None)

    
    # Element {http://www.w3schools.com}SendersCorrespondent_D uses Python identifier SendersCorrespondent_D
    __SendersCorrespondent_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SendersCorrespondent_D'), 'SendersCorrespondent_D', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comSendersCorrespondent_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 277, 5), )

    
    SendersCorrespondent_D = property(__SendersCorrespondent_D.value, __SendersCorrespondent_D.set, None, None)

    
    # Element {http://www.w3schools.com}ReceiversCorrespondent_A uses Python identifier ReceiversCorrespondent_A
    __ReceiversCorrespondent_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ReceiversCorrespondent_A'), 'ReceiversCorrespondent_A', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comReceiversCorrespondent_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 280, 5), )

    
    ReceiversCorrespondent_A = property(__ReceiversCorrespondent_A.value, __ReceiversCorrespondent_A.set, None, None)

    
    # Element {http://www.w3schools.com}ReceiversCorrespondent_B uses Python identifier ReceiversCorrespondent_B
    __ReceiversCorrespondent_B = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ReceiversCorrespondent_B'), 'ReceiversCorrespondent_B', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comReceiversCorrespondent_B', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 281, 5), )

    
    ReceiversCorrespondent_B = property(__ReceiversCorrespondent_B.value, __ReceiversCorrespondent_B.set, None, None)

    
    # Element {http://www.w3schools.com}ReceiversCorrespondent_D uses Python identifier ReceiversCorrespondent_D
    __ReceiversCorrespondent_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ReceiversCorrespondent_D'), 'ReceiversCorrespondent_D', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comReceiversCorrespondent_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 282, 5), )

    
    ReceiversCorrespondent_D = property(__ReceiversCorrespondent_D.value, __ReceiversCorrespondent_D.set, None, None)

    
    # Element {http://www.w3schools.com}Intermedairy_A uses Python identifier Intermedairy_A
    __Intermedairy_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Intermedairy_A'), 'Intermedairy_A', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comIntermedairy_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 285, 5), )

    
    Intermedairy_A = property(__Intermedairy_A.value, __Intermedairy_A.set, None, None)

    
    # Element {http://www.w3schools.com}Intermedairy_D uses Python identifier Intermedairy_D
    __Intermedairy_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Intermedairy_D'), 'Intermedairy_D', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comIntermedairy_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 286, 5), )

    
    Intermedairy_D = property(__Intermedairy_D.value, __Intermedairy_D.set, None, None)

    
    # Element {http://www.w3schools.com}AccountWithInstitution_A uses Python identifier AccountWithInstitution_A
    __AccountWithInstitution_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'AccountWithInstitution_A'), 'AccountWithInstitution_A', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comAccountWithInstitution_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 289, 5), )

    
    AccountWithInstitution_A = property(__AccountWithInstitution_A.value, __AccountWithInstitution_A.set, None, None)

    
    # Element {http://www.w3schools.com}AccountWithInstitution_B uses Python identifier AccountWithInstitution_B
    __AccountWithInstitution_B = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'AccountWithInstitution_B'), 'AccountWithInstitution_B', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comAccountWithInstitution_B', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 290, 5), )

    
    AccountWithInstitution_B = property(__AccountWithInstitution_B.value, __AccountWithInstitution_B.set, None, None)

    
    # Element {http://www.w3schools.com}AccountWithInstitution_D uses Python identifier AccountWithInstitution_D
    __AccountWithInstitution_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'AccountWithInstitution_D'), 'AccountWithInstitution_D', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comAccountWithInstitution_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 291, 5), )

    
    AccountWithInstitution_D = property(__AccountWithInstitution_D.value, __AccountWithInstitution_D.set, None, None)

    
    # Element {http://www.w3schools.com}BeneficiaryInstitution_A uses Python identifier BeneficiaryInstitution_A
    __BeneficiaryInstitution_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_A'), 'BeneficiaryInstitution_A', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comBeneficiaryInstitution_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 294, 5), )

    
    BeneficiaryInstitution_A = property(__BeneficiaryInstitution_A.value, __BeneficiaryInstitution_A.set, None, None)

    
    # Element {http://www.w3schools.com}BeneficiaryInstitution_D uses Python identifier BeneficiaryInstitution_D
    __BeneficiaryInstitution_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_D'), 'BeneficiaryInstitution_D', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comBeneficiaryInstitution_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 295, 5), )

    
    BeneficiaryInstitution_D = property(__BeneficiaryInstitution_D.value, __BeneficiaryInstitution_D.set, None, None)

    
    # Element {http://www.w3schools.com}SenderToReceiverInformation uses Python identifier SenderToReceiverInformation
    __SenderToReceiverInformation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SenderToReceiverInformation'), 'SenderToReceiverInformation', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comSenderToReceiverInformation', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 297, 4), )

    
    SenderToReceiverInformation = property(__SenderToReceiverInformation.value, __SenderToReceiverInformation.set, None, None)

    _ElementMap.update({
        __TransactionReferenceNumber.name() : __TransactionReferenceNumber,
        __RelatedReference.name() : __RelatedReference,
        __TimeIndication.name() : __TimeIndication,
        __ValueDateCurrencyCodeAmount.name() : __ValueDateCurrencyCodeAmount,
        __OrderingInstitution_A.name() : __OrderingInstitution_A,
        __OrderingInstitution_D.name() : __OrderingInstitution_D,
        __SendersCorrespondent_A.name() : __SendersCorrespondent_A,
        __SendersCorrespondent_B.name() : __SendersCorrespondent_B,
        __SendersCorrespondent_D.name() : __SendersCorrespondent_D,
        __ReceiversCorrespondent_A.name() : __ReceiversCorrespondent_A,
        __ReceiversCorrespondent_B.name() : __ReceiversCorrespondent_B,
        __ReceiversCorrespondent_D.name() : __ReceiversCorrespondent_D,
        __Intermedairy_A.name() : __Intermedairy_A,
        __Intermedairy_D.name() : __Intermedairy_D,
        __AccountWithInstitution_A.name() : __AccountWithInstitution_A,
        __AccountWithInstitution_B.name() : __AccountWithInstitution_B,
        __AccountWithInstitution_D.name() : __AccountWithInstitution_D,
        __BeneficiaryInstitution_A.name() : __BeneficiaryInstitution_A,
        __BeneficiaryInstitution_D.name() : __BeneficiaryInstitution_D,
        __SenderToReceiverInformation.name() : __SenderToReceiverInformation
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON = CTD_ANON


# Complex type {http://www.w3schools.com}MT202_20_Type with content type SIMPLE
class MT202_20_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT202_20_Type with content type SIMPLE"""
    _TypeDefinition = MT202_20_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202_20_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 8, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT202_20_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT202_20_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='20')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 11, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 11, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT202_20_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 12, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 12, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT202_20_Type = MT202_20_Type
Namespace.addCategoryObject('typeBinding', 'MT202_20_Type', MT202_20_Type)


# Complex type {http://www.w3schools.com}MT202_21_Type with content type SIMPLE
class MT202_21_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT202_21_Type with content type SIMPLE"""
    _TypeDefinition = MT202_21_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202_21_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 21, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT202_21_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT202_21_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='21')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 24, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 24, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT202_21_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 25, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 25, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT202_21_Type = MT202_21_Type
Namespace.addCategoryObject('typeBinding', 'MT202_21_Type', MT202_21_Type)


# Complex type {http://www.w3schools.com}MT202_13C_Type with content type SIMPLE
class MT202_13C_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT202_13C_Type with content type SIMPLE"""
    _TypeDefinition = MT202_13C_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202_13C_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 34, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT202_13C_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT202_13C_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='13C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 37, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 37, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT202_13C_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 38, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 38, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT202_13C_Type = MT202_13C_Type
Namespace.addCategoryObject('typeBinding', 'MT202_13C_Type', MT202_13C_Type)


# Complex type {http://www.w3schools.com}MT202_32A_Type with content type SIMPLE
class MT202_32A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT202_32A_Type with content type SIMPLE"""
    _TypeDefinition = MT202_32A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202_32A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 47, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT202_32A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT202_32A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='32A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 50, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 50, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT202_32A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 51, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 51, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT202_32A_Type = MT202_32A_Type
Namespace.addCategoryObject('typeBinding', 'MT202_32A_Type', MT202_32A_Type)


# Complex type {http://www.w3schools.com}MT202_52A_Type with content type SIMPLE
class MT202_52A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT202_52A_Type with content type SIMPLE"""
    _TypeDefinition = MT202_52A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202_52A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 60, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT202_52A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT202_52A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='52A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 63, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 63, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT202_52A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 64, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 64, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT202_52A_Type = MT202_52A_Type
Namespace.addCategoryObject('typeBinding', 'MT202_52A_Type', MT202_52A_Type)


# Complex type {http://www.w3schools.com}MT202_52D_Type with content type SIMPLE
class MT202_52D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT202_52D_Type with content type SIMPLE"""
    _TypeDefinition = MT202_52D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202_52D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 73, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT202_52D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT202_52D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='52D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 76, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 76, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT202_52D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 77, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 77, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT202_52D_Type = MT202_52D_Type
Namespace.addCategoryObject('typeBinding', 'MT202_52D_Type', MT202_52D_Type)


# Complex type {http://www.w3schools.com}MT202_53A_Type with content type SIMPLE
class MT202_53A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT202_53A_Type with content type SIMPLE"""
    _TypeDefinition = MT202_53A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202_53A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 86, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT202_53A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT202_53A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='53A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 89, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 89, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT202_53A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 90, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 90, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT202_53A_Type = MT202_53A_Type
Namespace.addCategoryObject('typeBinding', 'MT202_53A_Type', MT202_53A_Type)


# Complex type {http://www.w3schools.com}MT202_53B_Type with content type SIMPLE
class MT202_53B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT202_53B_Type with content type SIMPLE"""
    _TypeDefinition = MT202_53B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202_53B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 99, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT202_53B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT202_53B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='53B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 102, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 102, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT202_53B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 103, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 103, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT202_53B_Type = MT202_53B_Type
Namespace.addCategoryObject('typeBinding', 'MT202_53B_Type', MT202_53B_Type)


# Complex type {http://www.w3schools.com}MT202_53D_Type with content type SIMPLE
class MT202_53D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT202_53D_Type with content type SIMPLE"""
    _TypeDefinition = MT202_53D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202_53D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 112, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT202_53D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT202_53D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='53D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 115, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 115, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT202_53D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 116, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 116, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT202_53D_Type = MT202_53D_Type
Namespace.addCategoryObject('typeBinding', 'MT202_53D_Type', MT202_53D_Type)


# Complex type {http://www.w3schools.com}MT202_54A_Type with content type SIMPLE
class MT202_54A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT202_54A_Type with content type SIMPLE"""
    _TypeDefinition = MT202_54A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202_54A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 125, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT202_54A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT202_54A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='54A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 128, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 128, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT202_54A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 129, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 129, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT202_54A_Type = MT202_54A_Type
Namespace.addCategoryObject('typeBinding', 'MT202_54A_Type', MT202_54A_Type)


# Complex type {http://www.w3schools.com}MT202_54B_Type with content type SIMPLE
class MT202_54B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT202_54B_Type with content type SIMPLE"""
    _TypeDefinition = MT202_54B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202_54B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 138, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT202_54B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT202_54B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='54B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 141, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 141, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT202_54B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 142, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 142, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT202_54B_Type = MT202_54B_Type
Namespace.addCategoryObject('typeBinding', 'MT202_54B_Type', MT202_54B_Type)


# Complex type {http://www.w3schools.com}MT202_54D_Type with content type SIMPLE
class MT202_54D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT202_54D_Type with content type SIMPLE"""
    _TypeDefinition = MT202_54D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202_54D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 151, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT202_54D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT202_54D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='54D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 154, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 154, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT202_54D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 155, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 155, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT202_54D_Type = MT202_54D_Type
Namespace.addCategoryObject('typeBinding', 'MT202_54D_Type', MT202_54D_Type)


# Complex type {http://www.w3schools.com}MT202_56A_Type with content type SIMPLE
class MT202_56A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT202_56A_Type with content type SIMPLE"""
    _TypeDefinition = MT202_56A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202_56A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 164, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT202_56A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT202_56A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='56A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 167, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 167, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT202_56A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 168, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 168, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT202_56A_Type = MT202_56A_Type
Namespace.addCategoryObject('typeBinding', 'MT202_56A_Type', MT202_56A_Type)


# Complex type {http://www.w3schools.com}MT202_56D_Type with content type SIMPLE
class MT202_56D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT202_56D_Type with content type SIMPLE"""
    _TypeDefinition = MT202_56D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202_56D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 177, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT202_56D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT202_56D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='56D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 180, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 180, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT202_56D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 181, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 181, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT202_56D_Type = MT202_56D_Type
Namespace.addCategoryObject('typeBinding', 'MT202_56D_Type', MT202_56D_Type)


# Complex type {http://www.w3schools.com}MT202_57A_Type with content type SIMPLE
class MT202_57A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT202_57A_Type with content type SIMPLE"""
    _TypeDefinition = MT202_57A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202_57A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 190, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT202_57A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT202_57A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='57A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 193, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 193, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT202_57A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 194, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 194, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT202_57A_Type = MT202_57A_Type
Namespace.addCategoryObject('typeBinding', 'MT202_57A_Type', MT202_57A_Type)


# Complex type {http://www.w3schools.com}MT202_57B_Type with content type SIMPLE
class MT202_57B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT202_57B_Type with content type SIMPLE"""
    _TypeDefinition = MT202_57B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202_57B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 203, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT202_57B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT202_57B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='57B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 206, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 206, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT202_57B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 207, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 207, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT202_57B_Type = MT202_57B_Type
Namespace.addCategoryObject('typeBinding', 'MT202_57B_Type', MT202_57B_Type)


# Complex type {http://www.w3schools.com}MT202_57D_Type with content type SIMPLE
class MT202_57D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT202_57D_Type with content type SIMPLE"""
    _TypeDefinition = MT202_57D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202_57D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 216, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT202_57D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT202_57D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='57D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 219, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 219, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT202_57D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 220, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 220, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT202_57D_Type = MT202_57D_Type
Namespace.addCategoryObject('typeBinding', 'MT202_57D_Type', MT202_57D_Type)


# Complex type {http://www.w3schools.com}MT202_58A_Type with content type SIMPLE
class MT202_58A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT202_58A_Type with content type SIMPLE"""
    _TypeDefinition = MT202_58A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202_58A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 229, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT202_58A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT202_58A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='58A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 232, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 232, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT202_58A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 233, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 233, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT202_58A_Type = MT202_58A_Type
Namespace.addCategoryObject('typeBinding', 'MT202_58A_Type', MT202_58A_Type)


# Complex type {http://www.w3schools.com}MT202_58D_Type with content type SIMPLE
class MT202_58D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT202_58D_Type with content type SIMPLE"""
    _TypeDefinition = MT202_58D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202_58D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 242, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT202_58D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT202_58D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='58D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 245, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 245, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT202_58D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 246, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 246, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT202_58D_Type = MT202_58D_Type
Namespace.addCategoryObject('typeBinding', 'MT202_58D_Type', MT202_58D_Type)


# Complex type {http://www.w3schools.com}MT202_72_Type with content type SIMPLE
class MT202_72_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT202_72_Type with content type SIMPLE"""
    _TypeDefinition = MT202_72_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202_72_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 255, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT202_72_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT202_72_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='72')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 258, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 258, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT202_72_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 259, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 259, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT202_72_Type = MT202_72_Type
Namespace.addCategoryObject('typeBinding', 'MT202_72_Type', MT202_72_Type)


MT202 = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'MT202'), CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 263, 1))
Namespace.addCategoryObject('elementBinding', MT202.name().localName(), MT202)



CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TransactionReferenceNumber'), MT202_20_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 266, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'RelatedReference'), MT202_21_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 267, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TimeIndication'), MT202_13C_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 268, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ValueDateCurrencyCodeAmount'), MT202_32A_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 269, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'OrderingInstitution_A'), MT202_52A_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 271, 5)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'OrderingInstitution_D'), MT202_52D_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 272, 5)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SendersCorrespondent_A'), MT202_53A_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 275, 5)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SendersCorrespondent_B'), MT202_53B_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 276, 5)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SendersCorrespondent_D'), MT202_53D_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 277, 5)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ReceiversCorrespondent_A'), MT202_54A_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 280, 5)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ReceiversCorrespondent_B'), MT202_54B_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 281, 5)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ReceiversCorrespondent_D'), MT202_54D_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 282, 5)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Intermedairy_A'), MT202_56A_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 285, 5)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Intermedairy_D'), MT202_56D_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 286, 5)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'AccountWithInstitution_A'), MT202_57A_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 289, 5)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'AccountWithInstitution_B'), MT202_57B_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 290, 5)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'AccountWithInstitution_D'), MT202_57D_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 291, 5)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_A'), MT202_58A_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 294, 5)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_D'), MT202_58D_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 295, 5)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SenderToReceiverInformation'), MT202_72_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 297, 4)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 268, 4))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 270, 4))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 271, 5))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 272, 5))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 274, 4))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 275, 5))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 276, 5))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 277, 5))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 279, 4))
    counters.add(cc_8)
    cc_9 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 280, 5))
    counters.add(cc_9)
    cc_10 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 281, 5))
    counters.add(cc_10)
    cc_11 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 282, 5))
    counters.add(cc_11)
    cc_12 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 284, 4))
    counters.add(cc_12)
    cc_13 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 285, 5))
    counters.add(cc_13)
    cc_14 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 286, 5))
    counters.add(cc_14)
    cc_15 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 288, 4))
    counters.add(cc_15)
    cc_16 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 289, 5))
    counters.add(cc_16)
    cc_17 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 290, 5))
    counters.add(cc_17)
    cc_18 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 291, 5))
    counters.add(cc_18)
    cc_19 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 297, 4))
    counters.add(cc_19)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'TransactionReferenceNumber')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 266, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'RelatedReference')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 267, 4))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'TimeIndication')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 268, 4))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ValueDateCurrencyCodeAmount')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 269, 4))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'OrderingInstitution_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 271, 5))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'OrderingInstitution_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 272, 5))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SendersCorrespondent_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 275, 5))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SendersCorrespondent_B')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 276, 5))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SendersCorrespondent_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 277, 5))
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ReceiversCorrespondent_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 280, 5))
    st_9 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ReceiversCorrespondent_B')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 281, 5))
    st_10 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ReceiversCorrespondent_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 282, 5))
    st_11 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Intermedairy_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 285, 5))
    st_12 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_12)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Intermedairy_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 286, 5))
    st_13 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_13)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'AccountWithInstitution_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 289, 5))
    st_14 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_14)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'AccountWithInstitution_B')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 290, 5))
    st_15 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_15)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'AccountWithInstitution_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 291, 5))
    st_16 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_16)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 294, 5))
    st_17 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_17)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 295, 5))
    st_18 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_18)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_19, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SenderToReceiverInformation')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT202.csv.xsd', 297, 4))
    st_19 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_19)
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
    transitions.append(fac.Transition(st_9, [
         ]))
    transitions.append(fac.Transition(st_10, [
         ]))
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
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, True),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, True),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_2, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, True),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, True),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_3, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_4, True),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_5, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_4, True),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_4, True),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_5, False) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_4, True),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_4, True),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_6, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_4, True),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_6, False) ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_4, True),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_4, True),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_4, True),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_7, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_7, False) ]))
    st_8._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_8, True),
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_9, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_8, True),
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_8, True),
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_9, False) ]))
    st_9._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_8, True),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_8, True),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_10, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_8, True),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_10, False) ]))
    st_10._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_8, True),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_8, True),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_8, True),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_11, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_11, False) ]))
    st_11._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_12, True),
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_13, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_12, True),
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_12, False),
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_12, False),
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_12, False),
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_12, False),
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_12, False),
        fac.UpdateInstruction(cc_13, False) ]))
    st_12._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_12, True),
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_12, True),
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_14, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_12, False),
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_12, False),
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_12, False),
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_12, False),
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_12, False),
        fac.UpdateInstruction(cc_14, False) ]))
    st_13._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_15, True),
        fac.UpdateInstruction(cc_16, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_16, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_15, True),
        fac.UpdateInstruction(cc_16, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_15, True),
        fac.UpdateInstruction(cc_16, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_15, False),
        fac.UpdateInstruction(cc_16, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_15, False),
        fac.UpdateInstruction(cc_16, False) ]))
    st_14._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_15, True),
        fac.UpdateInstruction(cc_17, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_15, True),
        fac.UpdateInstruction(cc_17, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_17, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_15, True),
        fac.UpdateInstruction(cc_17, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_15, False),
        fac.UpdateInstruction(cc_17, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_15, False),
        fac.UpdateInstruction(cc_17, False) ]))
    st_15._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_15, True),
        fac.UpdateInstruction(cc_18, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_15, True),
        fac.UpdateInstruction(cc_18, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_15, True),
        fac.UpdateInstruction(cc_18, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_18, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_15, False),
        fac.UpdateInstruction(cc_18, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_15, False),
        fac.UpdateInstruction(cc_18, False) ]))
    st_16._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_19, [
         ]))
    st_17._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_19, [
         ]))
    st_18._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_19, True) ]))
    st_19._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON._Automaton = _BuildAutomaton()


