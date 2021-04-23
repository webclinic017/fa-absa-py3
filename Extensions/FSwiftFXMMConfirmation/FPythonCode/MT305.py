# C:\Projects\Code\SwiftMessagingSolution_Python3\base\extensions\SwiftIntegration\Utilities\TemplateFiles\MT305.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:96afad3d20bbfe8d040a1a097fa388d9fecd10e3
# Generated 2019-11-07 12:24:15.371033 by PyXB version 1.2.6 using Python 3.7.4.final.0
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
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:696e450c-012b-11ea-b5a5-509a4c321f2f')

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


# Atomic simple type: {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_20_Type_Pattern
class MT305_SequenceA_GeneralInformation_20_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceA_GeneralInformation_20_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 3, 1)
    _Documentation = None
MT305_SequenceA_GeneralInformation_20_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT305_SequenceA_GeneralInformation_20_Type_Pattern._CF_pattern.addPattern(pattern="([^/]([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,16}[^/])")
MT305_SequenceA_GeneralInformation_20_Type_Pattern._InitializeFacetMap(MT305_SequenceA_GeneralInformation_20_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceA_GeneralInformation_20_Type_Pattern', MT305_SequenceA_GeneralInformation_20_Type_Pattern)
_module_typeBindings.MT305_SequenceA_GeneralInformation_20_Type_Pattern = MT305_SequenceA_GeneralInformation_20_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_21_Type_Pattern
class MT305_SequenceA_GeneralInformation_21_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceA_GeneralInformation_21_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 16, 1)
    _Documentation = None
MT305_SequenceA_GeneralInformation_21_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT305_SequenceA_GeneralInformation_21_Type_Pattern._CF_pattern.addPattern(pattern="([^/]([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,16}[^/])")
MT305_SequenceA_GeneralInformation_21_Type_Pattern._InitializeFacetMap(MT305_SequenceA_GeneralInformation_21_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceA_GeneralInformation_21_Type_Pattern', MT305_SequenceA_GeneralInformation_21_Type_Pattern)
_module_typeBindings.MT305_SequenceA_GeneralInformation_21_Type_Pattern = MT305_SequenceA_GeneralInformation_21_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_22_Type_Pattern
class MT305_SequenceA_GeneralInformation_22_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceA_GeneralInformation_22_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 29, 1)
    _Documentation = None
MT305_SequenceA_GeneralInformation_22_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT305_SequenceA_GeneralInformation_22_Type_Pattern._CF_pattern.addPattern(pattern='((AMEND|CANCEL|CLOSEOUT|NEW)/[A-Z]{4}[A-Z0-9]{2}[0-9]{4}[A-Z]{4}[A-Z0-9]{2})')
MT305_SequenceA_GeneralInformation_22_Type_Pattern._InitializeFacetMap(MT305_SequenceA_GeneralInformation_22_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceA_GeneralInformation_22_Type_Pattern', MT305_SequenceA_GeneralInformation_22_Type_Pattern)
_module_typeBindings.MT305_SequenceA_GeneralInformation_22_Type_Pattern = MT305_SequenceA_GeneralInformation_22_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_23_Type_Pattern
class MT305_SequenceA_GeneralInformation_23_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceA_GeneralInformation_23_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 42, 1)
    _Documentation = None
MT305_SequenceA_GeneralInformation_23_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT305_SequenceA_GeneralInformation_23_Type_Pattern._CF_pattern.addPattern(pattern='((BUY|SELL)/(CALL|PUT)/(A|E)/(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD))')
MT305_SequenceA_GeneralInformation_23_Type_Pattern._InitializeFacetMap(MT305_SequenceA_GeneralInformation_23_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceA_GeneralInformation_23_Type_Pattern', MT305_SequenceA_GeneralInformation_23_Type_Pattern)
_module_typeBindings.MT305_SequenceA_GeneralInformation_23_Type_Pattern = MT305_SequenceA_GeneralInformation_23_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_94A_Type_Pattern
class MT305_SequenceA_GeneralInformation_94A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceA_GeneralInformation_94A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 55, 1)
    _Documentation = None
MT305_SequenceA_GeneralInformation_94A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT305_SequenceA_GeneralInformation_94A_Type_Pattern._CF_pattern.addPattern(pattern='(AGN([0-5][0-9])|BILA|BROK)')
MT305_SequenceA_GeneralInformation_94A_Type_Pattern._InitializeFacetMap(MT305_SequenceA_GeneralInformation_94A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceA_GeneralInformation_94A_Type_Pattern', MT305_SequenceA_GeneralInformation_94A_Type_Pattern)
_module_typeBindings.MT305_SequenceA_GeneralInformation_94A_Type_Pattern = MT305_SequenceA_GeneralInformation_94A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_82A_Type_Pattern
class MT305_SequenceA_GeneralInformation_82A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceA_GeneralInformation_82A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 68, 1)
    _Documentation = None
MT305_SequenceA_GeneralInformation_82A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT305_SequenceA_GeneralInformation_82A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT305_SequenceA_GeneralInformation_82A_Type_Pattern._InitializeFacetMap(MT305_SequenceA_GeneralInformation_82A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceA_GeneralInformation_82A_Type_Pattern', MT305_SequenceA_GeneralInformation_82A_Type_Pattern)
_module_typeBindings.MT305_SequenceA_GeneralInformation_82A_Type_Pattern = MT305_SequenceA_GeneralInformation_82A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_82D_Type_Pattern
class MT305_SequenceA_GeneralInformation_82D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceA_GeneralInformation_82D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 81, 1)
    _Documentation = None
MT305_SequenceA_GeneralInformation_82D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT305_SequenceA_GeneralInformation_82D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT305_SequenceA_GeneralInformation_82D_Type_Pattern._InitializeFacetMap(MT305_SequenceA_GeneralInformation_82D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceA_GeneralInformation_82D_Type_Pattern', MT305_SequenceA_GeneralInformation_82D_Type_Pattern)
_module_typeBindings.MT305_SequenceA_GeneralInformation_82D_Type_Pattern = MT305_SequenceA_GeneralInformation_82D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_82J_Type_Pattern
class MT305_SequenceA_GeneralInformation_82J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceA_GeneralInformation_82J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 94, 1)
    _Documentation = None
MT305_SequenceA_GeneralInformation_82J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT305_SequenceA_GeneralInformation_82J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT305_SequenceA_GeneralInformation_82J_Type_Pattern._InitializeFacetMap(MT305_SequenceA_GeneralInformation_82J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceA_GeneralInformation_82J_Type_Pattern', MT305_SequenceA_GeneralInformation_82J_Type_Pattern)
_module_typeBindings.MT305_SequenceA_GeneralInformation_82J_Type_Pattern = MT305_SequenceA_GeneralInformation_82J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_87A_Type_Pattern
class MT305_SequenceA_GeneralInformation_87A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceA_GeneralInformation_87A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 107, 1)
    _Documentation = None
MT305_SequenceA_GeneralInformation_87A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT305_SequenceA_GeneralInformation_87A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT305_SequenceA_GeneralInformation_87A_Type_Pattern._InitializeFacetMap(MT305_SequenceA_GeneralInformation_87A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceA_GeneralInformation_87A_Type_Pattern', MT305_SequenceA_GeneralInformation_87A_Type_Pattern)
_module_typeBindings.MT305_SequenceA_GeneralInformation_87A_Type_Pattern = MT305_SequenceA_GeneralInformation_87A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_87D_Type_Pattern
class MT305_SequenceA_GeneralInformation_87D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceA_GeneralInformation_87D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 120, 1)
    _Documentation = None
MT305_SequenceA_GeneralInformation_87D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT305_SequenceA_GeneralInformation_87D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT305_SequenceA_GeneralInformation_87D_Type_Pattern._InitializeFacetMap(MT305_SequenceA_GeneralInformation_87D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceA_GeneralInformation_87D_Type_Pattern', MT305_SequenceA_GeneralInformation_87D_Type_Pattern)
_module_typeBindings.MT305_SequenceA_GeneralInformation_87D_Type_Pattern = MT305_SequenceA_GeneralInformation_87D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_87J_Type_Pattern
class MT305_SequenceA_GeneralInformation_87J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceA_GeneralInformation_87J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 133, 1)
    _Documentation = None
MT305_SequenceA_GeneralInformation_87J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT305_SequenceA_GeneralInformation_87J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT305_SequenceA_GeneralInformation_87J_Type_Pattern._InitializeFacetMap(MT305_SequenceA_GeneralInformation_87J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceA_GeneralInformation_87J_Type_Pattern', MT305_SequenceA_GeneralInformation_87J_Type_Pattern)
_module_typeBindings.MT305_SequenceA_GeneralInformation_87J_Type_Pattern = MT305_SequenceA_GeneralInformation_87J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_83A_Type_Pattern
class MT305_SequenceA_GeneralInformation_83A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceA_GeneralInformation_83A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 146, 1)
    _Documentation = None
MT305_SequenceA_GeneralInformation_83A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT305_SequenceA_GeneralInformation_83A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT305_SequenceA_GeneralInformation_83A_Type_Pattern._InitializeFacetMap(MT305_SequenceA_GeneralInformation_83A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceA_GeneralInformation_83A_Type_Pattern', MT305_SequenceA_GeneralInformation_83A_Type_Pattern)
_module_typeBindings.MT305_SequenceA_GeneralInformation_83A_Type_Pattern = MT305_SequenceA_GeneralInformation_83A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_83D_Type_Pattern
class MT305_SequenceA_GeneralInformation_83D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceA_GeneralInformation_83D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 159, 1)
    _Documentation = None
MT305_SequenceA_GeneralInformation_83D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT305_SequenceA_GeneralInformation_83D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT305_SequenceA_GeneralInformation_83D_Type_Pattern._InitializeFacetMap(MT305_SequenceA_GeneralInformation_83D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceA_GeneralInformation_83D_Type_Pattern', MT305_SequenceA_GeneralInformation_83D_Type_Pattern)
_module_typeBindings.MT305_SequenceA_GeneralInformation_83D_Type_Pattern = MT305_SequenceA_GeneralInformation_83D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_83J_Type_Pattern
class MT305_SequenceA_GeneralInformation_83J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceA_GeneralInformation_83J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 172, 1)
    _Documentation = None
MT305_SequenceA_GeneralInformation_83J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT305_SequenceA_GeneralInformation_83J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT305_SequenceA_GeneralInformation_83J_Type_Pattern._InitializeFacetMap(MT305_SequenceA_GeneralInformation_83J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceA_GeneralInformation_83J_Type_Pattern', MT305_SequenceA_GeneralInformation_83J_Type_Pattern)
_module_typeBindings.MT305_SequenceA_GeneralInformation_83J_Type_Pattern = MT305_SequenceA_GeneralInformation_83J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_30_Type_Pattern
class MT305_SequenceA_GeneralInformation_30_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceA_GeneralInformation_30_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 185, 1)
    _Documentation = None
MT305_SequenceA_GeneralInformation_30_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT305_SequenceA_GeneralInformation_30_Type_Pattern._CF_pattern.addPattern(pattern='([0-9]{2}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))')
MT305_SequenceA_GeneralInformation_30_Type_Pattern._InitializeFacetMap(MT305_SequenceA_GeneralInformation_30_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceA_GeneralInformation_30_Type_Pattern', MT305_SequenceA_GeneralInformation_30_Type_Pattern)
_module_typeBindings.MT305_SequenceA_GeneralInformation_30_Type_Pattern = MT305_SequenceA_GeneralInformation_30_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_31C_Type_Pattern
class MT305_SequenceA_GeneralInformation_31C_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceA_GeneralInformation_31C_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 198, 1)
    _Documentation = None
MT305_SequenceA_GeneralInformation_31C_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT305_SequenceA_GeneralInformation_31C_Type_Pattern._CF_pattern.addPattern(pattern='([0-9]{2}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))')
MT305_SequenceA_GeneralInformation_31C_Type_Pattern._InitializeFacetMap(MT305_SequenceA_GeneralInformation_31C_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceA_GeneralInformation_31C_Type_Pattern', MT305_SequenceA_GeneralInformation_31C_Type_Pattern)
_module_typeBindings.MT305_SequenceA_GeneralInformation_31C_Type_Pattern = MT305_SequenceA_GeneralInformation_31C_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_31G_Type_Pattern
class MT305_SequenceA_GeneralInformation_31G_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceA_GeneralInformation_31G_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 211, 1)
    _Documentation = None
MT305_SequenceA_GeneralInformation_31G_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT305_SequenceA_GeneralInformation_31G_Type_Pattern._CF_pattern.addPattern(pattern='([0-9]{2}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])/(0[0-9]|[1][0-9]|2[1-3])([0-5][0-9])/[A-Z]{1,12})')
MT305_SequenceA_GeneralInformation_31G_Type_Pattern._InitializeFacetMap(MT305_SequenceA_GeneralInformation_31G_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceA_GeneralInformation_31G_Type_Pattern', MT305_SequenceA_GeneralInformation_31G_Type_Pattern)
_module_typeBindings.MT305_SequenceA_GeneralInformation_31G_Type_Pattern = MT305_SequenceA_GeneralInformation_31G_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_31E_Type_Pattern
class MT305_SequenceA_GeneralInformation_31E_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceA_GeneralInformation_31E_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 224, 1)
    _Documentation = None
MT305_SequenceA_GeneralInformation_31E_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT305_SequenceA_GeneralInformation_31E_Type_Pattern._CF_pattern.addPattern(pattern='([0-9]{2}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))')
MT305_SequenceA_GeneralInformation_31E_Type_Pattern._InitializeFacetMap(MT305_SequenceA_GeneralInformation_31E_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceA_GeneralInformation_31E_Type_Pattern', MT305_SequenceA_GeneralInformation_31E_Type_Pattern)
_module_typeBindings.MT305_SequenceA_GeneralInformation_31E_Type_Pattern = MT305_SequenceA_GeneralInformation_31E_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_26F_Type_Pattern
class MT305_SequenceA_GeneralInformation_26F_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceA_GeneralInformation_26F_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 237, 1)
    _Documentation = None
MT305_SequenceA_GeneralInformation_26F_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT305_SequenceA_GeneralInformation_26F_Type_Pattern._CF_pattern.addPattern(pattern='(NE([0-5][0-9])CAS(0[0-9]|[1][0-9]|2[1-3])|PRINCIPAL)')
MT305_SequenceA_GeneralInformation_26F_Type_Pattern._InitializeFacetMap(MT305_SequenceA_GeneralInformation_26F_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceA_GeneralInformation_26F_Type_Pattern', MT305_SequenceA_GeneralInformation_26F_Type_Pattern)
_module_typeBindings.MT305_SequenceA_GeneralInformation_26F_Type_Pattern = MT305_SequenceA_GeneralInformation_26F_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_39M_Type_Pattern
class MT305_SequenceA_GeneralInformation_39M_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceA_GeneralInformation_39M_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 250, 1)
    _Documentation = None
MT305_SequenceA_GeneralInformation_39M_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT305_SequenceA_GeneralInformation_39M_Type_Pattern._CF_pattern.addPattern(pattern='([A-Z]{2})')
MT305_SequenceA_GeneralInformation_39M_Type_Pattern._InitializeFacetMap(MT305_SequenceA_GeneralInformation_39M_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceA_GeneralInformation_39M_Type_Pattern', MT305_SequenceA_GeneralInformation_39M_Type_Pattern)
_module_typeBindings.MT305_SequenceA_GeneralInformation_39M_Type_Pattern = MT305_SequenceA_GeneralInformation_39M_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_17F_Type_Pattern
class MT305_SequenceA_GeneralInformation_17F_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceA_GeneralInformation_17F_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 263, 1)
    _Documentation = None
MT305_SequenceA_GeneralInformation_17F_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT305_SequenceA_GeneralInformation_17F_Type_Pattern._CF_pattern.addPattern(pattern='((Y|N))')
MT305_SequenceA_GeneralInformation_17F_Type_Pattern._InitializeFacetMap(MT305_SequenceA_GeneralInformation_17F_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceA_GeneralInformation_17F_Type_Pattern', MT305_SequenceA_GeneralInformation_17F_Type_Pattern)
_module_typeBindings.MT305_SequenceA_GeneralInformation_17F_Type_Pattern = MT305_SequenceA_GeneralInformation_17F_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_14S_Type_Pattern
class MT305_SequenceA_GeneralInformation_14S_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceA_GeneralInformation_14S_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 276, 1)
    _Documentation = None
MT305_SequenceA_GeneralInformation_14S_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT305_SequenceA_GeneralInformation_14S_Type_Pattern._CF_pattern.addPattern(pattern='([A-Z]{3}[0-9]{1,2}(/(0[0-9]|[1][0-9]|2[1-3])([0-5][0-9])/[A-Z0-9]{4})?)')
MT305_SequenceA_GeneralInformation_14S_Type_Pattern._InitializeFacetMap(MT305_SequenceA_GeneralInformation_14S_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceA_GeneralInformation_14S_Type_Pattern', MT305_SequenceA_GeneralInformation_14S_Type_Pattern)
_module_typeBindings.MT305_SequenceA_GeneralInformation_14S_Type_Pattern = MT305_SequenceA_GeneralInformation_14S_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_32E_Type_Pattern
class MT305_SequenceA_GeneralInformation_32E_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceA_GeneralInformation_32E_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 289, 1)
    _Documentation = None
MT305_SequenceA_GeneralInformation_32E_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT305_SequenceA_GeneralInformation_32E_Type_Pattern._CF_pattern.addPattern(pattern='([A-Z]{3})')
MT305_SequenceA_GeneralInformation_32E_Type_Pattern._InitializeFacetMap(MT305_SequenceA_GeneralInformation_32E_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceA_GeneralInformation_32E_Type_Pattern', MT305_SequenceA_GeneralInformation_32E_Type_Pattern)
_module_typeBindings.MT305_SequenceA_GeneralInformation_32E_Type_Pattern = MT305_SequenceA_GeneralInformation_32E_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_32B_Type_Pattern
class MT305_SequenceA_GeneralInformation_32B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceA_GeneralInformation_32B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 302, 1)
    _Documentation = None
MT305_SequenceA_GeneralInformation_32B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT305_SequenceA_GeneralInformation_32B_Type_Pattern._CF_pattern.addPattern(pattern='((AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})')
MT305_SequenceA_GeneralInformation_32B_Type_Pattern._InitializeFacetMap(MT305_SequenceA_GeneralInformation_32B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceA_GeneralInformation_32B_Type_Pattern', MT305_SequenceA_GeneralInformation_32B_Type_Pattern)
_module_typeBindings.MT305_SequenceA_GeneralInformation_32B_Type_Pattern = MT305_SequenceA_GeneralInformation_32B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_36_Type_Pattern
class MT305_SequenceA_GeneralInformation_36_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceA_GeneralInformation_36_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 315, 1)
    _Documentation = None
MT305_SequenceA_GeneralInformation_36_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT305_SequenceA_GeneralInformation_36_Type_Pattern._CF_pattern.addPattern(pattern='([0-9,(?0-9)]{1,12})')
MT305_SequenceA_GeneralInformation_36_Type_Pattern._InitializeFacetMap(MT305_SequenceA_GeneralInformation_36_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceA_GeneralInformation_36_Type_Pattern', MT305_SequenceA_GeneralInformation_36_Type_Pattern)
_module_typeBindings.MT305_SequenceA_GeneralInformation_36_Type_Pattern = MT305_SequenceA_GeneralInformation_36_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_33B_Type_Pattern
class MT305_SequenceA_GeneralInformation_33B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceA_GeneralInformation_33B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 328, 1)
    _Documentation = None
MT305_SequenceA_GeneralInformation_33B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT305_SequenceA_GeneralInformation_33B_Type_Pattern._CF_pattern.addPattern(pattern='((AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})')
MT305_SequenceA_GeneralInformation_33B_Type_Pattern._InitializeFacetMap(MT305_SequenceA_GeneralInformation_33B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceA_GeneralInformation_33B_Type_Pattern', MT305_SequenceA_GeneralInformation_33B_Type_Pattern)
_module_typeBindings.MT305_SequenceA_GeneralInformation_33B_Type_Pattern = MT305_SequenceA_GeneralInformation_33B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_37K_Type_Pattern
class MT305_SequenceA_GeneralInformation_37K_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceA_GeneralInformation_37K_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 341, 1)
    _Documentation = None
MT305_SequenceA_GeneralInformation_37K_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT305_SequenceA_GeneralInformation_37K_Type_Pattern._CF_pattern.addPattern(pattern='((AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD|PCT)[0-9,(?0-9)]{1,12})')
MT305_SequenceA_GeneralInformation_37K_Type_Pattern._InitializeFacetMap(MT305_SequenceA_GeneralInformation_37K_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceA_GeneralInformation_37K_Type_Pattern', MT305_SequenceA_GeneralInformation_37K_Type_Pattern)
_module_typeBindings.MT305_SequenceA_GeneralInformation_37K_Type_Pattern = MT305_SequenceA_GeneralInformation_37K_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_34P_Type_Pattern
class MT305_SequenceA_GeneralInformation_34P_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceA_GeneralInformation_34P_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 354, 1)
    _Documentation = None
MT305_SequenceA_GeneralInformation_34P_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT305_SequenceA_GeneralInformation_34P_Type_Pattern._CF_pattern.addPattern(pattern='([0-9]{2}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})')
MT305_SequenceA_GeneralInformation_34P_Type_Pattern._InitializeFacetMap(MT305_SequenceA_GeneralInformation_34P_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceA_GeneralInformation_34P_Type_Pattern', MT305_SequenceA_GeneralInformation_34P_Type_Pattern)
_module_typeBindings.MT305_SequenceA_GeneralInformation_34P_Type_Pattern = MT305_SequenceA_GeneralInformation_34P_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_34R_Type_Pattern
class MT305_SequenceA_GeneralInformation_34R_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceA_GeneralInformation_34R_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 367, 1)
    _Documentation = None
MT305_SequenceA_GeneralInformation_34R_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT305_SequenceA_GeneralInformation_34R_Type_Pattern._CF_pattern.addPattern(pattern='([0-9]{2}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})')
MT305_SequenceA_GeneralInformation_34R_Type_Pattern._InitializeFacetMap(MT305_SequenceA_GeneralInformation_34R_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceA_GeneralInformation_34R_Type_Pattern', MT305_SequenceA_GeneralInformation_34R_Type_Pattern)
_module_typeBindings.MT305_SequenceA_GeneralInformation_34R_Type_Pattern = MT305_SequenceA_GeneralInformation_34R_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_53A_Type_Pattern
class MT305_SequenceA_GeneralInformation_53A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceA_GeneralInformation_53A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 380, 1)
    _Documentation = None
MT305_SequenceA_GeneralInformation_53A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT305_SequenceA_GeneralInformation_53A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT305_SequenceA_GeneralInformation_53A_Type_Pattern._InitializeFacetMap(MT305_SequenceA_GeneralInformation_53A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceA_GeneralInformation_53A_Type_Pattern', MT305_SequenceA_GeneralInformation_53A_Type_Pattern)
_module_typeBindings.MT305_SequenceA_GeneralInformation_53A_Type_Pattern = MT305_SequenceA_GeneralInformation_53A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_53D_Type_Pattern
class MT305_SequenceA_GeneralInformation_53D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceA_GeneralInformation_53D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 393, 1)
    _Documentation = None
MT305_SequenceA_GeneralInformation_53D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT305_SequenceA_GeneralInformation_53D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35})?)")
MT305_SequenceA_GeneralInformation_53D_Type_Pattern._InitializeFacetMap(MT305_SequenceA_GeneralInformation_53D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceA_GeneralInformation_53D_Type_Pattern', MT305_SequenceA_GeneralInformation_53D_Type_Pattern)
_module_typeBindings.MT305_SequenceA_GeneralInformation_53D_Type_Pattern = MT305_SequenceA_GeneralInformation_53D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_53J_Type_Pattern
class MT305_SequenceA_GeneralInformation_53J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceA_GeneralInformation_53J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 406, 1)
    _Documentation = None
MT305_SequenceA_GeneralInformation_53J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT305_SequenceA_GeneralInformation_53J_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT305_SequenceA_GeneralInformation_53J_Type_Pattern._InitializeFacetMap(MT305_SequenceA_GeneralInformation_53J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceA_GeneralInformation_53J_Type_Pattern', MT305_SequenceA_GeneralInformation_53J_Type_Pattern)
_module_typeBindings.MT305_SequenceA_GeneralInformation_53J_Type_Pattern = MT305_SequenceA_GeneralInformation_53J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_56A_Type_Pattern
class MT305_SequenceA_GeneralInformation_56A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceA_GeneralInformation_56A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 419, 1)
    _Documentation = None
MT305_SequenceA_GeneralInformation_56A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT305_SequenceA_GeneralInformation_56A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT305_SequenceA_GeneralInformation_56A_Type_Pattern._InitializeFacetMap(MT305_SequenceA_GeneralInformation_56A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceA_GeneralInformation_56A_Type_Pattern', MT305_SequenceA_GeneralInformation_56A_Type_Pattern)
_module_typeBindings.MT305_SequenceA_GeneralInformation_56A_Type_Pattern = MT305_SequenceA_GeneralInformation_56A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_56D_Type_Pattern
class MT305_SequenceA_GeneralInformation_56D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceA_GeneralInformation_56D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 432, 1)
    _Documentation = None
MT305_SequenceA_GeneralInformation_56D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT305_SequenceA_GeneralInformation_56D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT305_SequenceA_GeneralInformation_56D_Type_Pattern._InitializeFacetMap(MT305_SequenceA_GeneralInformation_56D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceA_GeneralInformation_56D_Type_Pattern', MT305_SequenceA_GeneralInformation_56D_Type_Pattern)
_module_typeBindings.MT305_SequenceA_GeneralInformation_56D_Type_Pattern = MT305_SequenceA_GeneralInformation_56D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_57A_Type_Pattern
class MT305_SequenceA_GeneralInformation_57A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceA_GeneralInformation_57A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 445, 1)
    _Documentation = None
MT305_SequenceA_GeneralInformation_57A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT305_SequenceA_GeneralInformation_57A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT305_SequenceA_GeneralInformation_57A_Type_Pattern._InitializeFacetMap(MT305_SequenceA_GeneralInformation_57A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceA_GeneralInformation_57A_Type_Pattern', MT305_SequenceA_GeneralInformation_57A_Type_Pattern)
_module_typeBindings.MT305_SequenceA_GeneralInformation_57A_Type_Pattern = MT305_SequenceA_GeneralInformation_57A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_57D_Type_Pattern
class MT305_SequenceA_GeneralInformation_57D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceA_GeneralInformation_57D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 458, 1)
    _Documentation = None
MT305_SequenceA_GeneralInformation_57D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT305_SequenceA_GeneralInformation_57D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT305_SequenceA_GeneralInformation_57D_Type_Pattern._InitializeFacetMap(MT305_SequenceA_GeneralInformation_57D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceA_GeneralInformation_57D_Type_Pattern', MT305_SequenceA_GeneralInformation_57D_Type_Pattern)
_module_typeBindings.MT305_SequenceA_GeneralInformation_57D_Type_Pattern = MT305_SequenceA_GeneralInformation_57D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_77H_Type_Pattern
class MT305_SequenceA_GeneralInformation_77H_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceA_GeneralInformation_77H_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 471, 1)
    _Documentation = None
MT305_SequenceA_GeneralInformation_77H_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT305_SequenceA_GeneralInformation_77H_Type_Pattern._CF_pattern.addPattern(pattern='((AFB|DERV|FBF|FEOMA|ICOM|IFEMA|ISDA|ISDACN|OTHER)(/[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))?(//[0-9]{4})?)')
MT305_SequenceA_GeneralInformation_77H_Type_Pattern._InitializeFacetMap(MT305_SequenceA_GeneralInformation_77H_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceA_GeneralInformation_77H_Type_Pattern', MT305_SequenceA_GeneralInformation_77H_Type_Pattern)
_module_typeBindings.MT305_SequenceA_GeneralInformation_77H_Type_Pattern = MT305_SequenceA_GeneralInformation_77H_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_14C_Type_Pattern
class MT305_SequenceA_GeneralInformation_14C_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceA_GeneralInformation_14C_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 484, 1)
    _Documentation = None
MT305_SequenceA_GeneralInformation_14C_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT305_SequenceA_GeneralInformation_14C_Type_Pattern._CF_pattern.addPattern(pattern='([0-9]{4})')
MT305_SequenceA_GeneralInformation_14C_Type_Pattern._InitializeFacetMap(MT305_SequenceA_GeneralInformation_14C_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceA_GeneralInformation_14C_Type_Pattern', MT305_SequenceA_GeneralInformation_14C_Type_Pattern)
_module_typeBindings.MT305_SequenceA_GeneralInformation_14C_Type_Pattern = MT305_SequenceA_GeneralInformation_14C_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_72_Type_Pattern
class MT305_SequenceA_GeneralInformation_72_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceA_GeneralInformation_72_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 497, 1)
    _Documentation = None
MT305_SequenceA_GeneralInformation_72_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT305_SequenceA_GeneralInformation_72_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,6})")
MT305_SequenceA_GeneralInformation_72_Type_Pattern._InitializeFacetMap(MT305_SequenceA_GeneralInformation_72_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceA_GeneralInformation_72_Type_Pattern', MT305_SequenceA_GeneralInformation_72_Type_Pattern)
_module_typeBindings.MT305_SequenceA_GeneralInformation_72_Type_Pattern = MT305_SequenceA_GeneralInformation_72_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_22L_Type_Pattern
class MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_22L_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_22L_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 510, 1)
    _Documentation = None
MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_22L_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_22L_Type_Pattern._CF_pattern.addPattern(pattern="(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35})")
MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_22L_Type_Pattern._InitializeFacetMap(MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_22L_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_22L_Type_Pattern', MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_22L_Type_Pattern)
_module_typeBindings.MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_22L_Type_Pattern = MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_22L_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_91A_Type_Pattern
class MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_91A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_91A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 523, 1)
    _Documentation = None
MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_91A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_91A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_91A_Type_Pattern._InitializeFacetMap(MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_91A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_91A_Type_Pattern', MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_91A_Type_Pattern)
_module_typeBindings.MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_91A_Type_Pattern = MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_91A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_91D_Type_Pattern
class MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_91D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_91D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 536, 1)
    _Documentation = None
MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_91D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_91D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_91D_Type_Pattern._InitializeFacetMap(MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_91D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_91D_Type_Pattern', MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_91D_Type_Pattern)
_module_typeBindings.MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_91D_Type_Pattern = MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_91D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_91J_Type_Pattern
class MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_91J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_91J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 549, 1)
    _Documentation = None
MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_91J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_91J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_91J_Type_Pattern._InitializeFacetMap(MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_91J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_91J_Type_Pattern', MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_91J_Type_Pattern)
_module_typeBindings.MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_91J_Type_Pattern = MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_91J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_22M_Type_Pattern
class MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_22M_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_22M_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 562, 1)
    _Documentation = None
MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_22M_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_22M_Type_Pattern._CF_pattern.addPattern(pattern="(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,30})")
MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_22M_Type_Pattern._InitializeFacetMap(MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_22M_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_22M_Type_Pattern', MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_22M_Type_Pattern)
_module_typeBindings.MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_22M_Type_Pattern = MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_22M_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_22N_Type_Pattern
class MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_22N_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_22N_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 575, 1)
    _Documentation = None
MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_22N_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_22N_Type_Pattern._CF_pattern.addPattern(pattern="(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,32})")
MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_22N_Type_Pattern._InitializeFacetMap(MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_22N_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_22N_Type_Pattern', MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_22N_Type_Pattern)
_module_typeBindings.MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_22N_Type_Pattern = MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_22N_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_SubsequenceB1a1_PriorUniqueTransactionIdentifier_22P_Type_Pattern
class MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_SubsequenceB1a1_PriorUniqueTransactionIdentifier_22P_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_SubsequenceB1a1_PriorUniqueTransactionIdentifier_22P_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 588, 1)
    _Documentation = None
MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_SubsequenceB1a1_PriorUniqueTransactionIdentifier_22P_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_SubsequenceB1a1_PriorUniqueTransactionIdentifier_22P_Type_Pattern._CF_pattern.addPattern(pattern="(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,30})")
MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_SubsequenceB1a1_PriorUniqueTransactionIdentifier_22P_Type_Pattern._InitializeFacetMap(MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_SubsequenceB1a1_PriorUniqueTransactionIdentifier_22P_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_SubsequenceB1a1_PriorUniqueTransactionIdentifier_22P_Type_Pattern', MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_SubsequenceB1a1_PriorUniqueTransactionIdentifier_22P_Type_Pattern)
_module_typeBindings.MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_SubsequenceB1a1_PriorUniqueTransactionIdentifier_22P_Type_Pattern = MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_SubsequenceB1a1_PriorUniqueTransactionIdentifier_22P_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_SubsequenceB1a1_PriorUniqueTransactionIdentifier_22R_Type_Pattern
class MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_SubsequenceB1a1_PriorUniqueTransactionIdentifier_22R_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_SubsequenceB1a1_PriorUniqueTransactionIdentifier_22R_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 601, 1)
    _Documentation = None
MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_SubsequenceB1a1_PriorUniqueTransactionIdentifier_22R_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_SubsequenceB1a1_PriorUniqueTransactionIdentifier_22R_Type_Pattern._CF_pattern.addPattern(pattern="(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,32})")
MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_SubsequenceB1a1_PriorUniqueTransactionIdentifier_22R_Type_Pattern._InitializeFacetMap(MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_SubsequenceB1a1_PriorUniqueTransactionIdentifier_22R_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_SubsequenceB1a1_PriorUniqueTransactionIdentifier_22R_Type_Pattern', MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_SubsequenceB1a1_PriorUniqueTransactionIdentifier_22R_Type_Pattern)
_module_typeBindings.MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_SubsequenceB1a1_PriorUniqueTransactionIdentifier_22R_Type_Pattern = MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_SubsequenceB1a1_PriorUniqueTransactionIdentifier_22R_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_81A_Type_Pattern
class MT305_SequenceB_ReportingInformation_81A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceB_ReportingInformation_81A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 614, 1)
    _Documentation = None
MT305_SequenceB_ReportingInformation_81A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT305_SequenceB_ReportingInformation_81A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT305_SequenceB_ReportingInformation_81A_Type_Pattern._InitializeFacetMap(MT305_SequenceB_ReportingInformation_81A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceB_ReportingInformation_81A_Type_Pattern', MT305_SequenceB_ReportingInformation_81A_Type_Pattern)
_module_typeBindings.MT305_SequenceB_ReportingInformation_81A_Type_Pattern = MT305_SequenceB_ReportingInformation_81A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_81D_Type_Pattern
class MT305_SequenceB_ReportingInformation_81D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceB_ReportingInformation_81D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 627, 1)
    _Documentation = None
MT305_SequenceB_ReportingInformation_81D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT305_SequenceB_ReportingInformation_81D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT305_SequenceB_ReportingInformation_81D_Type_Pattern._InitializeFacetMap(MT305_SequenceB_ReportingInformation_81D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceB_ReportingInformation_81D_Type_Pattern', MT305_SequenceB_ReportingInformation_81D_Type_Pattern)
_module_typeBindings.MT305_SequenceB_ReportingInformation_81D_Type_Pattern = MT305_SequenceB_ReportingInformation_81D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_81J_Type_Pattern
class MT305_SequenceB_ReportingInformation_81J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceB_ReportingInformation_81J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 640, 1)
    _Documentation = None
MT305_SequenceB_ReportingInformation_81J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT305_SequenceB_ReportingInformation_81J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT305_SequenceB_ReportingInformation_81J_Type_Pattern._InitializeFacetMap(MT305_SequenceB_ReportingInformation_81J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceB_ReportingInformation_81J_Type_Pattern', MT305_SequenceB_ReportingInformation_81J_Type_Pattern)
_module_typeBindings.MT305_SequenceB_ReportingInformation_81J_Type_Pattern = MT305_SequenceB_ReportingInformation_81J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_89A_Type_Pattern
class MT305_SequenceB_ReportingInformation_89A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceB_ReportingInformation_89A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 653, 1)
    _Documentation = None
MT305_SequenceB_ReportingInformation_89A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT305_SequenceB_ReportingInformation_89A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT305_SequenceB_ReportingInformation_89A_Type_Pattern._InitializeFacetMap(MT305_SequenceB_ReportingInformation_89A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceB_ReportingInformation_89A_Type_Pattern', MT305_SequenceB_ReportingInformation_89A_Type_Pattern)
_module_typeBindings.MT305_SequenceB_ReportingInformation_89A_Type_Pattern = MT305_SequenceB_ReportingInformation_89A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_89D_Type_Pattern
class MT305_SequenceB_ReportingInformation_89D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceB_ReportingInformation_89D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 666, 1)
    _Documentation = None
MT305_SequenceB_ReportingInformation_89D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT305_SequenceB_ReportingInformation_89D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT305_SequenceB_ReportingInformation_89D_Type_Pattern._InitializeFacetMap(MT305_SequenceB_ReportingInformation_89D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceB_ReportingInformation_89D_Type_Pattern', MT305_SequenceB_ReportingInformation_89D_Type_Pattern)
_module_typeBindings.MT305_SequenceB_ReportingInformation_89D_Type_Pattern = MT305_SequenceB_ReportingInformation_89D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_89J_Type_Pattern
class MT305_SequenceB_ReportingInformation_89J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceB_ReportingInformation_89J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 679, 1)
    _Documentation = None
MT305_SequenceB_ReportingInformation_89J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT305_SequenceB_ReportingInformation_89J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT305_SequenceB_ReportingInformation_89J_Type_Pattern._InitializeFacetMap(MT305_SequenceB_ReportingInformation_89J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceB_ReportingInformation_89J_Type_Pattern', MT305_SequenceB_ReportingInformation_89J_Type_Pattern)
_module_typeBindings.MT305_SequenceB_ReportingInformation_89J_Type_Pattern = MT305_SequenceB_ReportingInformation_89J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_96A_Type_Pattern
class MT305_SequenceB_ReportingInformation_96A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceB_ReportingInformation_96A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 692, 1)
    _Documentation = None
MT305_SequenceB_ReportingInformation_96A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT305_SequenceB_ReportingInformation_96A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT305_SequenceB_ReportingInformation_96A_Type_Pattern._InitializeFacetMap(MT305_SequenceB_ReportingInformation_96A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceB_ReportingInformation_96A_Type_Pattern', MT305_SequenceB_ReportingInformation_96A_Type_Pattern)
_module_typeBindings.MT305_SequenceB_ReportingInformation_96A_Type_Pattern = MT305_SequenceB_ReportingInformation_96A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_96D_Type_Pattern
class MT305_SequenceB_ReportingInformation_96D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceB_ReportingInformation_96D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 705, 1)
    _Documentation = None
MT305_SequenceB_ReportingInformation_96D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT305_SequenceB_ReportingInformation_96D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT305_SequenceB_ReportingInformation_96D_Type_Pattern._InitializeFacetMap(MT305_SequenceB_ReportingInformation_96D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceB_ReportingInformation_96D_Type_Pattern', MT305_SequenceB_ReportingInformation_96D_Type_Pattern)
_module_typeBindings.MT305_SequenceB_ReportingInformation_96D_Type_Pattern = MT305_SequenceB_ReportingInformation_96D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_96J_Type_Pattern
class MT305_SequenceB_ReportingInformation_96J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceB_ReportingInformation_96J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 718, 1)
    _Documentation = None
MT305_SequenceB_ReportingInformation_96J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT305_SequenceB_ReportingInformation_96J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT305_SequenceB_ReportingInformation_96J_Type_Pattern._InitializeFacetMap(MT305_SequenceB_ReportingInformation_96J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceB_ReportingInformation_96J_Type_Pattern', MT305_SequenceB_ReportingInformation_96J_Type_Pattern)
_module_typeBindings.MT305_SequenceB_ReportingInformation_96J_Type_Pattern = MT305_SequenceB_ReportingInformation_96J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_22S_Type_Pattern
class MT305_SequenceB_ReportingInformation_22S_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceB_ReportingInformation_22S_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 731, 1)
    _Documentation = None
MT305_SequenceB_ReportingInformation_22S_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT305_SequenceB_ReportingInformation_22S_Type_Pattern._CF_pattern.addPattern(pattern="((C|P)/(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35})?)")
MT305_SequenceB_ReportingInformation_22S_Type_Pattern._InitializeFacetMap(MT305_SequenceB_ReportingInformation_22S_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceB_ReportingInformation_22S_Type_Pattern', MT305_SequenceB_ReportingInformation_22S_Type_Pattern)
_module_typeBindings.MT305_SequenceB_ReportingInformation_22S_Type_Pattern = MT305_SequenceB_ReportingInformation_22S_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_22T_Type_Pattern
class MT305_SequenceB_ReportingInformation_22T_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceB_ReportingInformation_22T_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 744, 1)
    _Documentation = None
MT305_SequenceB_ReportingInformation_22T_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT305_SequenceB_ReportingInformation_22T_Type_Pattern._CF_pattern.addPattern(pattern="(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35})")
MT305_SequenceB_ReportingInformation_22T_Type_Pattern._InitializeFacetMap(MT305_SequenceB_ReportingInformation_22T_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceB_ReportingInformation_22T_Type_Pattern', MT305_SequenceB_ReportingInformation_22T_Type_Pattern)
_module_typeBindings.MT305_SequenceB_ReportingInformation_22T_Type_Pattern = MT305_SequenceB_ReportingInformation_22T_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_17E_Type_Pattern
class MT305_SequenceB_ReportingInformation_17E_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceB_ReportingInformation_17E_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 757, 1)
    _Documentation = None
MT305_SequenceB_ReportingInformation_17E_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT305_SequenceB_ReportingInformation_17E_Type_Pattern._CF_pattern.addPattern(pattern='((N|Y))')
MT305_SequenceB_ReportingInformation_17E_Type_Pattern._InitializeFacetMap(MT305_SequenceB_ReportingInformation_17E_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceB_ReportingInformation_17E_Type_Pattern', MT305_SequenceB_ReportingInformation_17E_Type_Pattern)
_module_typeBindings.MT305_SequenceB_ReportingInformation_17E_Type_Pattern = MT305_SequenceB_ReportingInformation_17E_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_22U_Type_Pattern
class MT305_SequenceB_ReportingInformation_22U_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceB_ReportingInformation_22U_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 770, 1)
    _Documentation = None
MT305_SequenceB_ReportingInformation_22U_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT305_SequenceB_ReportingInformation_22U_Type_Pattern._CF_pattern.addPattern(pattern='((FXNDOP|FXVAOP))')
MT305_SequenceB_ReportingInformation_22U_Type_Pattern._InitializeFacetMap(MT305_SequenceB_ReportingInformation_22U_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceB_ReportingInformation_22U_Type_Pattern', MT305_SequenceB_ReportingInformation_22U_Type_Pattern)
_module_typeBindings.MT305_SequenceB_ReportingInformation_22U_Type_Pattern = MT305_SequenceB_ReportingInformation_22U_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_35B_Type_Pattern
class MT305_SequenceB_ReportingInformation_35B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceB_ReportingInformation_35B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 783, 1)
    _Documentation = None
MT305_SequenceB_ReportingInformation_35B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT305_SequenceB_ReportingInformation_35B_Type_Pattern._CF_pattern.addPattern(pattern="((ISIN {1}[A-Z0-9]{12})?(\\n(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})?)")
MT305_SequenceB_ReportingInformation_35B_Type_Pattern._InitializeFacetMap(MT305_SequenceB_ReportingInformation_35B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceB_ReportingInformation_35B_Type_Pattern', MT305_SequenceB_ReportingInformation_35B_Type_Pattern)
_module_typeBindings.MT305_SequenceB_ReportingInformation_35B_Type_Pattern = MT305_SequenceB_ReportingInformation_35B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_17H_Type_Pattern
class MT305_SequenceB_ReportingInformation_17H_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceB_ReportingInformation_17H_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 796, 1)
    _Documentation = None
MT305_SequenceB_ReportingInformation_17H_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT305_SequenceB_ReportingInformation_17H_Type_Pattern._CF_pattern.addPattern(pattern='((A|P|U))')
MT305_SequenceB_ReportingInformation_17H_Type_Pattern._InitializeFacetMap(MT305_SequenceB_ReportingInformation_17H_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceB_ReportingInformation_17H_Type_Pattern', MT305_SequenceB_ReportingInformation_17H_Type_Pattern)
_module_typeBindings.MT305_SequenceB_ReportingInformation_17H_Type_Pattern = MT305_SequenceB_ReportingInformation_17H_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_17P_Type_Pattern
class MT305_SequenceB_ReportingInformation_17P_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceB_ReportingInformation_17P_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 809, 1)
    _Documentation = None
MT305_SequenceB_ReportingInformation_17P_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT305_SequenceB_ReportingInformation_17P_Type_Pattern._CF_pattern.addPattern(pattern='((F|O|P|U))')
MT305_SequenceB_ReportingInformation_17P_Type_Pattern._InitializeFacetMap(MT305_SequenceB_ReportingInformation_17P_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceB_ReportingInformation_17P_Type_Pattern', MT305_SequenceB_ReportingInformation_17P_Type_Pattern)
_module_typeBindings.MT305_SequenceB_ReportingInformation_17P_Type_Pattern = MT305_SequenceB_ReportingInformation_17P_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_22V_Type_Pattern
class MT305_SequenceB_ReportingInformation_22V_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceB_ReportingInformation_22V_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 822, 1)
    _Documentation = None
MT305_SequenceB_ReportingInformation_22V_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT305_SequenceB_ReportingInformation_22V_Type_Pattern._CF_pattern.addPattern(pattern="(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35})")
MT305_SequenceB_ReportingInformation_22V_Type_Pattern._InitializeFacetMap(MT305_SequenceB_ReportingInformation_22V_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceB_ReportingInformation_22V_Type_Pattern', MT305_SequenceB_ReportingInformation_22V_Type_Pattern)
_module_typeBindings.MT305_SequenceB_ReportingInformation_22V_Type_Pattern = MT305_SequenceB_ReportingInformation_22V_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_98D_Type_Pattern
class MT305_SequenceB_ReportingInformation_98D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceB_ReportingInformation_98D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 835, 1)
    _Documentation = None
MT305_SequenceB_ReportingInformation_98D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT305_SequenceB_ReportingInformation_98D_Type_Pattern._CF_pattern.addPattern(pattern='([0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])(0[0-9]|[1][0-9]|2[1-3])([0-5][0-9])([0-5][0-9])(,[0-9]{1,3})?(/(N)?(0[0-9]|[1][0-9]|2[1-3])(([0-5][0-9]))?)?)')
MT305_SequenceB_ReportingInformation_98D_Type_Pattern._InitializeFacetMap(MT305_SequenceB_ReportingInformation_98D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceB_ReportingInformation_98D_Type_Pattern', MT305_SequenceB_ReportingInformation_98D_Type_Pattern)
_module_typeBindings.MT305_SequenceB_ReportingInformation_98D_Type_Pattern = MT305_SequenceB_ReportingInformation_98D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_17W_Type_Pattern
class MT305_SequenceB_ReportingInformation_17W_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceB_ReportingInformation_17W_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 848, 1)
    _Documentation = None
MT305_SequenceB_ReportingInformation_17W_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT305_SequenceB_ReportingInformation_17W_Type_Pattern._CF_pattern.addPattern(pattern='([0-9])')
MT305_SequenceB_ReportingInformation_17W_Type_Pattern._InitializeFacetMap(MT305_SequenceB_ReportingInformation_17W_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceB_ReportingInformation_17W_Type_Pattern', MT305_SequenceB_ReportingInformation_17W_Type_Pattern)
_module_typeBindings.MT305_SequenceB_ReportingInformation_17W_Type_Pattern = MT305_SequenceB_ReportingInformation_17W_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_17Y_Type_Pattern
class MT305_SequenceB_ReportingInformation_17Y_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceB_ReportingInformation_17Y_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 861, 1)
    _Documentation = None
MT305_SequenceB_ReportingInformation_17Y_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT305_SequenceB_ReportingInformation_17Y_Type_Pattern._CF_pattern.addPattern(pattern='((F|N))')
MT305_SequenceB_ReportingInformation_17Y_Type_Pattern._InitializeFacetMap(MT305_SequenceB_ReportingInformation_17Y_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceB_ReportingInformation_17Y_Type_Pattern', MT305_SequenceB_ReportingInformation_17Y_Type_Pattern)
_module_typeBindings.MT305_SequenceB_ReportingInformation_17Y_Type_Pattern = MT305_SequenceB_ReportingInformation_17Y_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_17Z_Type_Pattern
class MT305_SequenceB_ReportingInformation_17Z_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceB_ReportingInformation_17Z_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 874, 1)
    _Documentation = None
MT305_SequenceB_ReportingInformation_17Z_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT305_SequenceB_ReportingInformation_17Z_Type_Pattern._CF_pattern.addPattern(pattern='((N|Y))')
MT305_SequenceB_ReportingInformation_17Z_Type_Pattern._InitializeFacetMap(MT305_SequenceB_ReportingInformation_17Z_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceB_ReportingInformation_17Z_Type_Pattern', MT305_SequenceB_ReportingInformation_17Z_Type_Pattern)
_module_typeBindings.MT305_SequenceB_ReportingInformation_17Z_Type_Pattern = MT305_SequenceB_ReportingInformation_17Z_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_22Q_Type_Pattern
class MT305_SequenceB_ReportingInformation_22Q_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceB_ReportingInformation_22Q_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 887, 1)
    _Documentation = None
MT305_SequenceB_ReportingInformation_22Q_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT305_SequenceB_ReportingInformation_22Q_Type_Pattern._CF_pattern.addPattern(pattern="(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,10})")
MT305_SequenceB_ReportingInformation_22Q_Type_Pattern._InitializeFacetMap(MT305_SequenceB_ReportingInformation_22Q_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceB_ReportingInformation_22Q_Type_Pattern', MT305_SequenceB_ReportingInformation_22Q_Type_Pattern)
_module_typeBindings.MT305_SequenceB_ReportingInformation_22Q_Type_Pattern = MT305_SequenceB_ReportingInformation_22Q_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_17L_Type_Pattern
class MT305_SequenceB_ReportingInformation_17L_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceB_ReportingInformation_17L_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 900, 1)
    _Documentation = None
MT305_SequenceB_ReportingInformation_17L_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT305_SequenceB_ReportingInformation_17L_Type_Pattern._CF_pattern.addPattern(pattern='((N|Y))')
MT305_SequenceB_ReportingInformation_17L_Type_Pattern._InitializeFacetMap(MT305_SequenceB_ReportingInformation_17L_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceB_ReportingInformation_17L_Type_Pattern', MT305_SequenceB_ReportingInformation_17L_Type_Pattern)
_module_typeBindings.MT305_SequenceB_ReportingInformation_17L_Type_Pattern = MT305_SequenceB_ReportingInformation_17L_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_17M_Type_Pattern
class MT305_SequenceB_ReportingInformation_17M_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceB_ReportingInformation_17M_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 913, 1)
    _Documentation = None
MT305_SequenceB_ReportingInformation_17M_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT305_SequenceB_ReportingInformation_17M_Type_Pattern._CF_pattern.addPattern(pattern='((A|C|F|I|L|O|R|U))')
MT305_SequenceB_ReportingInformation_17M_Type_Pattern._InitializeFacetMap(MT305_SequenceB_ReportingInformation_17M_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceB_ReportingInformation_17M_Type_Pattern', MT305_SequenceB_ReportingInformation_17M_Type_Pattern)
_module_typeBindings.MT305_SequenceB_ReportingInformation_17M_Type_Pattern = MT305_SequenceB_ReportingInformation_17M_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_17Q_Type_Pattern
class MT305_SequenceB_ReportingInformation_17Q_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceB_ReportingInformation_17Q_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 926, 1)
    _Documentation = None
MT305_SequenceB_ReportingInformation_17Q_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT305_SequenceB_ReportingInformation_17Q_Type_Pattern._CF_pattern.addPattern(pattern='(N|[0-9])')
MT305_SequenceB_ReportingInformation_17Q_Type_Pattern._InitializeFacetMap(MT305_SequenceB_ReportingInformation_17Q_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceB_ReportingInformation_17Q_Type_Pattern', MT305_SequenceB_ReportingInformation_17Q_Type_Pattern)
_module_typeBindings.MT305_SequenceB_ReportingInformation_17Q_Type_Pattern = MT305_SequenceB_ReportingInformation_17Q_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_17S_Type_Pattern
class MT305_SequenceB_ReportingInformation_17S_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceB_ReportingInformation_17S_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 939, 1)
    _Documentation = None
MT305_SequenceB_ReportingInformation_17S_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT305_SequenceB_ReportingInformation_17S_Type_Pattern._CF_pattern.addPattern(pattern='(N|[0-9])')
MT305_SequenceB_ReportingInformation_17S_Type_Pattern._InitializeFacetMap(MT305_SequenceB_ReportingInformation_17S_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceB_ReportingInformation_17S_Type_Pattern', MT305_SequenceB_ReportingInformation_17S_Type_Pattern)
_module_typeBindings.MT305_SequenceB_ReportingInformation_17S_Type_Pattern = MT305_SequenceB_ReportingInformation_17S_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_17X_Type_Pattern
class MT305_SequenceB_ReportingInformation_17X_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceB_ReportingInformation_17X_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 952, 1)
    _Documentation = None
MT305_SequenceB_ReportingInformation_17X_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT305_SequenceB_ReportingInformation_17X_Type_Pattern._CF_pattern.addPattern(pattern='(N|[0-9])')
MT305_SequenceB_ReportingInformation_17X_Type_Pattern._InitializeFacetMap(MT305_SequenceB_ReportingInformation_17X_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceB_ReportingInformation_17X_Type_Pattern', MT305_SequenceB_ReportingInformation_17X_Type_Pattern)
_module_typeBindings.MT305_SequenceB_ReportingInformation_17X_Type_Pattern = MT305_SequenceB_ReportingInformation_17X_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_34C_Type_Pattern
class MT305_SequenceB_ReportingInformation_34C_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceB_ReportingInformation_34C_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 965, 1)
    _Documentation = None
MT305_SequenceB_ReportingInformation_34C_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT305_SequenceB_ReportingInformation_34C_Type_Pattern._CF_pattern.addPattern(pattern='([A-Z0-9]{4}/(N)?(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})')
MT305_SequenceB_ReportingInformation_34C_Type_Pattern._InitializeFacetMap(MT305_SequenceB_ReportingInformation_34C_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceB_ReportingInformation_34C_Type_Pattern', MT305_SequenceB_ReportingInformation_34C_Type_Pattern)
_module_typeBindings.MT305_SequenceB_ReportingInformation_34C_Type_Pattern = MT305_SequenceB_ReportingInformation_34C_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_77A_Type_Pattern
class MT305_SequenceB_ReportingInformation_77A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceB_ReportingInformation_77A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 978, 1)
    _Documentation = None
MT305_SequenceB_ReportingInformation_77A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT305_SequenceB_ReportingInformation_77A_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,20})")
MT305_SequenceB_ReportingInformation_77A_Type_Pattern._InitializeFacetMap(MT305_SequenceB_ReportingInformation_77A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceB_ReportingInformation_77A_Type_Pattern', MT305_SequenceB_ReportingInformation_77A_Type_Pattern)
_module_typeBindings.MT305_SequenceB_ReportingInformation_77A_Type_Pattern = MT305_SequenceB_ReportingInformation_77A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT305_15A_Type
class MT305_15A_Type (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_15A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 991, 1)
    _Documentation = None
MT305_15A_Type._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'MT305_15A_Type', MT305_15A_Type)
_module_typeBindings.MT305_15A_Type = MT305_15A_Type

# Atomic simple type: {http://www.w3schools.com}MT305_15B_Type
class MT305_15B_Type (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_15B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 994, 1)
    _Documentation = None
MT305_15B_Type._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'MT305_15B_Type', MT305_15B_Type)
_module_typeBindings.MT305_15B_Type = MT305_15B_Type

# Complex type {http://www.w3schools.com}MT305_SequenceA_GeneralInformation with content type ELEMENT_ONLY
class MT305_SequenceA_GeneralInformation (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT305_SequenceA_GeneralInformation with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceA_GeneralInformation')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 997, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}TransactionReferenceNumber uses Python identifier TransactionReferenceNumber
    __TransactionReferenceNumber = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'TransactionReferenceNumber'), 'TransactionReferenceNumber', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_httpwww_w3schools_comTransactionReferenceNumber', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 999, 3), )

    
    TransactionReferenceNumber = property(__TransactionReferenceNumber.value, __TransactionReferenceNumber.set, None, None)

    
    # Element {http://www.w3schools.com}RelatedReference uses Python identifier RelatedReference
    __RelatedReference = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'RelatedReference'), 'RelatedReference', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_httpwww_w3schools_comRelatedReference', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1000, 3), )

    
    RelatedReference = property(__RelatedReference.value, __RelatedReference.set, None, None)

    
    # Element {http://www.w3schools.com}CodeCommonReference uses Python identifier CodeCommonReference
    __CodeCommonReference = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CodeCommonReference'), 'CodeCommonReference', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_httpwww_w3schools_comCodeCommonReference', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1001, 3), )

    
    CodeCommonReference = property(__CodeCommonReference.value, __CodeCommonReference.set, None, None)

    
    # Element {http://www.w3schools.com}FurtherIdentification uses Python identifier FurtherIdentification
    __FurtherIdentification = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'FurtherIdentification'), 'FurtherIdentification', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_httpwww_w3schools_comFurtherIdentification', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1002, 3), )

    
    FurtherIdentification = property(__FurtherIdentification.value, __FurtherIdentification.set, None, None)

    
    # Element {http://www.w3schools.com}ScopeOfOperation uses Python identifier ScopeOfOperation
    __ScopeOfOperation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ScopeOfOperation'), 'ScopeOfOperation', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_httpwww_w3schools_comScopeOfOperation', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1003, 3), )

    
    ScopeOfOperation = property(__ScopeOfOperation.value, __ScopeOfOperation.set, None, None)

    
    # Element {http://www.w3schools.com}PartyA_A uses Python identifier PartyA_A
    __PartyA_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PartyA_A'), 'PartyA_A', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_httpwww_w3schools_comPartyA_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1005, 4), )

    
    PartyA_A = property(__PartyA_A.value, __PartyA_A.set, None, None)

    
    # Element {http://www.w3schools.com}PartyA_D uses Python identifier PartyA_D
    __PartyA_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PartyA_D'), 'PartyA_D', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_httpwww_w3schools_comPartyA_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1006, 4), )

    
    PartyA_D = property(__PartyA_D.value, __PartyA_D.set, None, None)

    
    # Element {http://www.w3schools.com}PartyA_J uses Python identifier PartyA_J
    __PartyA_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PartyA_J'), 'PartyA_J', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_httpwww_w3schools_comPartyA_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1007, 4), )

    
    PartyA_J = property(__PartyA_J.value, __PartyA_J.set, None, None)

    
    # Element {http://www.w3schools.com}PartyB_A uses Python identifier PartyB_A
    __PartyB_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PartyB_A'), 'PartyB_A', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_httpwww_w3schools_comPartyB_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1010, 4), )

    
    PartyB_A = property(__PartyB_A.value, __PartyB_A.set, None, None)

    
    # Element {http://www.w3schools.com}PartyB_D uses Python identifier PartyB_D
    __PartyB_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PartyB_D'), 'PartyB_D', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_httpwww_w3schools_comPartyB_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1011, 4), )

    
    PartyB_D = property(__PartyB_D.value, __PartyB_D.set, None, None)

    
    # Element {http://www.w3schools.com}PartyB_J uses Python identifier PartyB_J
    __PartyB_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PartyB_J'), 'PartyB_J', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_httpwww_w3schools_comPartyB_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1012, 4), )

    
    PartyB_J = property(__PartyB_J.value, __PartyB_J.set, None, None)

    
    # Element {http://www.w3schools.com}FundOrBeneficiaryCustomer_A uses Python identifier FundOrBeneficiaryCustomer_A
    __FundOrBeneficiaryCustomer_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'FundOrBeneficiaryCustomer_A'), 'FundOrBeneficiaryCustomer_A', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_httpwww_w3schools_comFundOrBeneficiaryCustomer_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1015, 4), )

    
    FundOrBeneficiaryCustomer_A = property(__FundOrBeneficiaryCustomer_A.value, __FundOrBeneficiaryCustomer_A.set, None, None)

    
    # Element {http://www.w3schools.com}FundOrBeneficiaryCustomer_D uses Python identifier FundOrBeneficiaryCustomer_D
    __FundOrBeneficiaryCustomer_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'FundOrBeneficiaryCustomer_D'), 'FundOrBeneficiaryCustomer_D', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_httpwww_w3schools_comFundOrBeneficiaryCustomer_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1016, 4), )

    
    FundOrBeneficiaryCustomer_D = property(__FundOrBeneficiaryCustomer_D.value, __FundOrBeneficiaryCustomer_D.set, None, None)

    
    # Element {http://www.w3schools.com}FundOrBeneficiaryCustomer_J uses Python identifier FundOrBeneficiaryCustomer_J
    __FundOrBeneficiaryCustomer_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'FundOrBeneficiaryCustomer_J'), 'FundOrBeneficiaryCustomer_J', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_httpwww_w3schools_comFundOrBeneficiaryCustomer_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1017, 4), )

    
    FundOrBeneficiaryCustomer_J = property(__FundOrBeneficiaryCustomer_J.value, __FundOrBeneficiaryCustomer_J.set, None, None)

    
    # Element {http://www.w3schools.com}DateContractAgreedAmended uses Python identifier DateContractAgreedAmended
    __DateContractAgreedAmended = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DateContractAgreedAmended'), 'DateContractAgreedAmended', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_httpwww_w3schools_comDateContractAgreedAmended', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1019, 3), )

    
    DateContractAgreedAmended = property(__DateContractAgreedAmended.value, __DateContractAgreedAmended.set, None, None)

    
    # Element {http://www.w3schools.com}EarliestExerciseDate uses Python identifier EarliestExerciseDate
    __EarliestExerciseDate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'EarliestExerciseDate'), 'EarliestExerciseDate', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_httpwww_w3schools_comEarliestExerciseDate', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1020, 3), )

    
    EarliestExerciseDate = property(__EarliestExerciseDate.value, __EarliestExerciseDate.set, None, None)

    
    # Element {http://www.w3schools.com}ExpiryDetails uses Python identifier ExpiryDetails
    __ExpiryDetails = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ExpiryDetails'), 'ExpiryDetails', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_httpwww_w3schools_comExpiryDetails', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1021, 3), )

    
    ExpiryDetails = property(__ExpiryDetails.value, __ExpiryDetails.set, None, None)

    
    # Element {http://www.w3schools.com}FinalSettlementDate uses Python identifier FinalSettlementDate
    __FinalSettlementDate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'FinalSettlementDate'), 'FinalSettlementDate', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_httpwww_w3schools_comFinalSettlementDate', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1022, 3), )

    
    FinalSettlementDate = property(__FinalSettlementDate.value, __FinalSettlementDate.set, None, None)

    
    # Element {http://www.w3schools.com}SettlementType uses Python identifier SettlementType
    __SettlementType = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SettlementType'), 'SettlementType', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_httpwww_w3schools_comSettlementType', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1023, 3), )

    
    SettlementType = property(__SettlementType.value, __SettlementType.set, None, None)

    
    # Element {http://www.w3schools.com}PaymentClearingCentre uses Python identifier PaymentClearingCentre
    __PaymentClearingCentre = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PaymentClearingCentre'), 'PaymentClearingCentre', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_httpwww_w3schools_comPaymentClearingCentre', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1024, 3), )

    
    PaymentClearingCentre = property(__PaymentClearingCentre.value, __PaymentClearingCentre.set, None, None)

    
    # Element {http://www.w3schools.com}NonDeliverableIndicator uses Python identifier NonDeliverableIndicator
    __NonDeliverableIndicator = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'NonDeliverableIndicator'), 'NonDeliverableIndicator', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_httpwww_w3schools_comNonDeliverableIndicator', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1025, 3), )

    
    NonDeliverableIndicator = property(__NonDeliverableIndicator.value, __NonDeliverableIndicator.set, None, None)

    
    # Element {http://www.w3schools.com}SettlementRateSource uses Python identifier SettlementRateSource
    __SettlementRateSource = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SettlementRateSource'), 'SettlementRateSource', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_httpwww_w3schools_comSettlementRateSource', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1026, 3), )

    
    SettlementRateSource = property(__SettlementRateSource.value, __SettlementRateSource.set, None, None)

    
    # Element {http://www.w3schools.com}SettlementCurrency uses Python identifier SettlementCurrency
    __SettlementCurrency = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SettlementCurrency'), 'SettlementCurrency', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_httpwww_w3schools_comSettlementCurrency', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1027, 3), )

    
    SettlementCurrency = property(__SettlementCurrency.value, __SettlementCurrency.set, None, None)

    
    # Element {http://www.w3schools.com}UnderlyingCurrencyNAmount uses Python identifier UnderlyingCurrencyNAmount
    __UnderlyingCurrencyNAmount = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'UnderlyingCurrencyNAmount'), 'UnderlyingCurrencyNAmount', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_httpwww_w3schools_comUnderlyingCurrencyNAmount', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1028, 3), )

    
    UnderlyingCurrencyNAmount = property(__UnderlyingCurrencyNAmount.value, __UnderlyingCurrencyNAmount.set, None, None)

    
    # Element {http://www.w3schools.com}StrikePrice uses Python identifier StrikePrice
    __StrikePrice = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'StrikePrice'), 'StrikePrice', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_httpwww_w3schools_comStrikePrice', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1029, 3), )

    
    StrikePrice = property(__StrikePrice.value, __StrikePrice.set, None, None)

    
    # Element {http://www.w3schools.com}CounterCurrencyNAmount uses Python identifier CounterCurrencyNAmount
    __CounterCurrencyNAmount = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CounterCurrencyNAmount'), 'CounterCurrencyNAmount', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_httpwww_w3schools_comCounterCurrencyNAmount', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1030, 3), )

    
    CounterCurrencyNAmount = property(__CounterCurrencyNAmount.value, __CounterCurrencyNAmount.set, None, None)

    
    # Element {http://www.w3schools.com}PremiumPrice uses Python identifier PremiumPrice
    __PremiumPrice = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PremiumPrice'), 'PremiumPrice', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_httpwww_w3schools_comPremiumPrice', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1031, 3), )

    
    PremiumPrice = property(__PremiumPrice.value, __PremiumPrice.set, None, None)

    
    # Element {http://www.w3schools.com}PremiumPayment_P uses Python identifier PremiumPayment_P
    __PremiumPayment_P = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PremiumPayment_P'), 'PremiumPayment_P', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_httpwww_w3schools_comPremiumPayment_P', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1033, 4), )

    
    PremiumPayment_P = property(__PremiumPayment_P.value, __PremiumPayment_P.set, None, None)

    
    # Element {http://www.w3schools.com}PremiumPayment_R uses Python identifier PremiumPayment_R
    __PremiumPayment_R = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PremiumPayment_R'), 'PremiumPayment_R', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_httpwww_w3schools_comPremiumPayment_R', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1034, 4), )

    
    PremiumPayment_R = property(__PremiumPayment_R.value, __PremiumPayment_R.set, None, None)

    
    # Element {http://www.w3schools.com}SendersCorrespondent_A uses Python identifier SendersCorrespondent_A
    __SendersCorrespondent_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SendersCorrespondent_A'), 'SendersCorrespondent_A', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_httpwww_w3schools_comSendersCorrespondent_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1037, 4), )

    
    SendersCorrespondent_A = property(__SendersCorrespondent_A.value, __SendersCorrespondent_A.set, None, None)

    
    # Element {http://www.w3schools.com}SendersCorrespondent_B uses Python identifier SendersCorrespondent_B
    __SendersCorrespondent_B = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SendersCorrespondent_B'), 'SendersCorrespondent_B', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_httpwww_w3schools_comSendersCorrespondent_B', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1038, 4), )

    
    SendersCorrespondent_B = property(__SendersCorrespondent_B.value, __SendersCorrespondent_B.set, None, None)

    
    # Element {http://www.w3schools.com}SendersCorrespondent_D uses Python identifier SendersCorrespondent_D
    __SendersCorrespondent_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SendersCorrespondent_D'), 'SendersCorrespondent_D', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_httpwww_w3schools_comSendersCorrespondent_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1039, 4), )

    
    SendersCorrespondent_D = property(__SendersCorrespondent_D.value, __SendersCorrespondent_D.set, None, None)

    
    # Element {http://www.w3schools.com}Intermediary_A uses Python identifier Intermediary_A
    __Intermediary_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_A'), 'Intermediary_A', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_httpwww_w3schools_comIntermediary_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1042, 4), )

    
    Intermediary_A = property(__Intermediary_A.value, __Intermediary_A.set, None, None)

    
    # Element {http://www.w3schools.com}Intermediary_D uses Python identifier Intermediary_D
    __Intermediary_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_D'), 'Intermediary_D', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_httpwww_w3schools_comIntermediary_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1043, 4), )

    
    Intermediary_D = property(__Intermediary_D.value, __Intermediary_D.set, None, None)

    
    # Element {http://www.w3schools.com}AccountWithInstitution_A uses Python identifier AccountWithInstitution_A
    __AccountWithInstitution_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'AccountWithInstitution_A'), 'AccountWithInstitution_A', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_httpwww_w3schools_comAccountWithInstitution_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1046, 4), )

    
    AccountWithInstitution_A = property(__AccountWithInstitution_A.value, __AccountWithInstitution_A.set, None, None)

    
    # Element {http://www.w3schools.com}AccountWithInstitution_D uses Python identifier AccountWithInstitution_D
    __AccountWithInstitution_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'AccountWithInstitution_D'), 'AccountWithInstitution_D', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_httpwww_w3schools_comAccountWithInstitution_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1047, 4), )

    
    AccountWithInstitution_D = property(__AccountWithInstitution_D.value, __AccountWithInstitution_D.set, None, None)

    
    # Element {http://www.w3schools.com}TypeDateVersionOfAgreement uses Python identifier TypeDateVersionOfAgreement
    __TypeDateVersionOfAgreement = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'TypeDateVersionOfAgreement'), 'TypeDateVersionOfAgreement', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_httpwww_w3schools_comTypeDateVersionOfAgreement', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1049, 3), )

    
    TypeDateVersionOfAgreement = property(__TypeDateVersionOfAgreement.value, __TypeDateVersionOfAgreement.set, None, None)

    
    # Element {http://www.w3schools.com}YearOfDefinitions uses Python identifier YearOfDefinitions
    __YearOfDefinitions = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'YearOfDefinitions'), 'YearOfDefinitions', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_httpwww_w3schools_comYearOfDefinitions', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1050, 3), )

    
    YearOfDefinitions = property(__YearOfDefinitions.value, __YearOfDefinitions.set, None, None)

    
    # Element {http://www.w3schools.com}SenderToReceiverInformation uses Python identifier SenderToReceiverInformation
    __SenderToReceiverInformation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SenderToReceiverInformation'), 'SenderToReceiverInformation', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_httpwww_w3schools_comSenderToReceiverInformation', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1051, 3), )

    
    SenderToReceiverInformation = property(__SenderToReceiverInformation.value, __SenderToReceiverInformation.set, None, None)

    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='15A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1053, 2)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1053, 2)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1054, 2)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1054, 2)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    
    # Attribute formatTag uses Python identifier formatTag
    __formatTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'formatTag'), 'formatTag', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_formatTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='False')
    __formatTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1055, 2)
    __formatTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1055, 2)
    
    formatTag = property(__formatTag.value, __formatTag.set, None, None)

    _ElementMap.update({
        __TransactionReferenceNumber.name() : __TransactionReferenceNumber,
        __RelatedReference.name() : __RelatedReference,
        __CodeCommonReference.name() : __CodeCommonReference,
        __FurtherIdentification.name() : __FurtherIdentification,
        __ScopeOfOperation.name() : __ScopeOfOperation,
        __PartyA_A.name() : __PartyA_A,
        __PartyA_D.name() : __PartyA_D,
        __PartyA_J.name() : __PartyA_J,
        __PartyB_A.name() : __PartyB_A,
        __PartyB_D.name() : __PartyB_D,
        __PartyB_J.name() : __PartyB_J,
        __FundOrBeneficiaryCustomer_A.name() : __FundOrBeneficiaryCustomer_A,
        __FundOrBeneficiaryCustomer_D.name() : __FundOrBeneficiaryCustomer_D,
        __FundOrBeneficiaryCustomer_J.name() : __FundOrBeneficiaryCustomer_J,
        __DateContractAgreedAmended.name() : __DateContractAgreedAmended,
        __EarliestExerciseDate.name() : __EarliestExerciseDate,
        __ExpiryDetails.name() : __ExpiryDetails,
        __FinalSettlementDate.name() : __FinalSettlementDate,
        __SettlementType.name() : __SettlementType,
        __PaymentClearingCentre.name() : __PaymentClearingCentre,
        __NonDeliverableIndicator.name() : __NonDeliverableIndicator,
        __SettlementRateSource.name() : __SettlementRateSource,
        __SettlementCurrency.name() : __SettlementCurrency,
        __UnderlyingCurrencyNAmount.name() : __UnderlyingCurrencyNAmount,
        __StrikePrice.name() : __StrikePrice,
        __CounterCurrencyNAmount.name() : __CounterCurrencyNAmount,
        __PremiumPrice.name() : __PremiumPrice,
        __PremiumPayment_P.name() : __PremiumPayment_P,
        __PremiumPayment_R.name() : __PremiumPayment_R,
        __SendersCorrespondent_A.name() : __SendersCorrespondent_A,
        __SendersCorrespondent_B.name() : __SendersCorrespondent_B,
        __SendersCorrespondent_D.name() : __SendersCorrespondent_D,
        __Intermediary_A.name() : __Intermediary_A,
        __Intermediary_D.name() : __Intermediary_D,
        __AccountWithInstitution_A.name() : __AccountWithInstitution_A,
        __AccountWithInstitution_D.name() : __AccountWithInstitution_D,
        __TypeDateVersionOfAgreement.name() : __TypeDateVersionOfAgreement,
        __YearOfDefinitions.name() : __YearOfDefinitions,
        __SenderToReceiverInformation.name() : __SenderToReceiverInformation
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory,
        __formatTag.name() : __formatTag
    })
_module_typeBindings.MT305_SequenceA_GeneralInformation = MT305_SequenceA_GeneralInformation
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceA_GeneralInformation', MT305_SequenceA_GeneralInformation)


# Complex type {http://www.w3schools.com}MT305_SequenceB_ReportingInformation with content type ELEMENT_ONLY
class MT305_SequenceB_ReportingInformation (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT305_SequenceB_ReportingInformation with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceB_ReportingInformation')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1057, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}SubsequenceB1_ReportingParties uses Python identifier SubsequenceB1_ReportingParties
    __SubsequenceB1_ReportingParties = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SubsequenceB1_ReportingParties'), 'SubsequenceB1_ReportingParties', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_httpwww_w3schools_comSubsequenceB1_ReportingParties', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1059, 3), )

    
    SubsequenceB1_ReportingParties = property(__SubsequenceB1_ReportingParties.value, __SubsequenceB1_ReportingParties.set, None, None)

    
    # Element {http://www.w3schools.com}CentralCounterpartyClearingHouse_A uses Python identifier CentralCounterpartyClearingHouse_A
    __CentralCounterpartyClearingHouse_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CentralCounterpartyClearingHouse_A'), 'CentralCounterpartyClearingHouse_A', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_httpwww_w3schools_comCentralCounterpartyClearingHouse_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1061, 4), )

    
    CentralCounterpartyClearingHouse_A = property(__CentralCounterpartyClearingHouse_A.value, __CentralCounterpartyClearingHouse_A.set, None, None)

    
    # Element {http://www.w3schools.com}CentralCounterpartyClearingHouse_D uses Python identifier CentralCounterpartyClearingHouse_D
    __CentralCounterpartyClearingHouse_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CentralCounterpartyClearingHouse_D'), 'CentralCounterpartyClearingHouse_D', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_httpwww_w3schools_comCentralCounterpartyClearingHouse_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1062, 4), )

    
    CentralCounterpartyClearingHouse_D = property(__CentralCounterpartyClearingHouse_D.value, __CentralCounterpartyClearingHouse_D.set, None, None)

    
    # Element {http://www.w3schools.com}CentralCounterpartyClearingHouse_J uses Python identifier CentralCounterpartyClearingHouse_J
    __CentralCounterpartyClearingHouse_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CentralCounterpartyClearingHouse_J'), 'CentralCounterpartyClearingHouse_J', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_httpwww_w3schools_comCentralCounterpartyClearingHouse_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1063, 4), )

    
    CentralCounterpartyClearingHouse_J = property(__CentralCounterpartyClearingHouse_J.value, __CentralCounterpartyClearingHouse_J.set, None, None)

    
    # Element {http://www.w3schools.com}ClearingBroker_A uses Python identifier ClearingBroker_A
    __ClearingBroker_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ClearingBroker_A'), 'ClearingBroker_A', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_httpwww_w3schools_comClearingBroker_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1066, 4), )

    
    ClearingBroker_A = property(__ClearingBroker_A.value, __ClearingBroker_A.set, None, None)

    
    # Element {http://www.w3schools.com}ClearingBroker_D uses Python identifier ClearingBroker_D
    __ClearingBroker_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ClearingBroker_D'), 'ClearingBroker_D', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_httpwww_w3schools_comClearingBroker_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1067, 4), )

    
    ClearingBroker_D = property(__ClearingBroker_D.value, __ClearingBroker_D.set, None, None)

    
    # Element {http://www.w3schools.com}ClearingBroker_J uses Python identifier ClearingBroker_J
    __ClearingBroker_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ClearingBroker_J'), 'ClearingBroker_J', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_httpwww_w3schools_comClearingBroker_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1068, 4), )

    
    ClearingBroker_J = property(__ClearingBroker_J.value, __ClearingBroker_J.set, None, None)

    
    # Element {http://www.w3schools.com}ClearingExceptionParty_A uses Python identifier ClearingExceptionParty_A
    __ClearingExceptionParty_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ClearingExceptionParty_A'), 'ClearingExceptionParty_A', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_httpwww_w3schools_comClearingExceptionParty_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1071, 4), )

    
    ClearingExceptionParty_A = property(__ClearingExceptionParty_A.value, __ClearingExceptionParty_A.set, None, None)

    
    # Element {http://www.w3schools.com}ClearingExceptionParty_D uses Python identifier ClearingExceptionParty_D
    __ClearingExceptionParty_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ClearingExceptionParty_D'), 'ClearingExceptionParty_D', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_httpwww_w3schools_comClearingExceptionParty_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1072, 4), )

    
    ClearingExceptionParty_D = property(__ClearingExceptionParty_D.value, __ClearingExceptionParty_D.set, None, None)

    
    # Element {http://www.w3schools.com}ClearingExceptionParty_J uses Python identifier ClearingExceptionParty_J
    __ClearingExceptionParty_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ClearingExceptionParty_J'), 'ClearingExceptionParty_J', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_httpwww_w3schools_comClearingExceptionParty_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1073, 4), )

    
    ClearingExceptionParty_J = property(__ClearingExceptionParty_J.value, __ClearingExceptionParty_J.set, None, None)

    
    # Element {http://www.w3schools.com}ClearingBrokerIdentification uses Python identifier ClearingBrokerIdentification
    __ClearingBrokerIdentification = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ClearingBrokerIdentification'), 'ClearingBrokerIdentification', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_httpwww_w3schools_comClearingBrokerIdentification', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1075, 3), )

    
    ClearingBrokerIdentification = property(__ClearingBrokerIdentification.value, __ClearingBrokerIdentification.set, None, None)

    
    # Element {http://www.w3schools.com}ClearedProductIdentification uses Python identifier ClearedProductIdentification
    __ClearedProductIdentification = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ClearedProductIdentification'), 'ClearedProductIdentification', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_httpwww_w3schools_comClearedProductIdentification', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1076, 3), )

    
    ClearedProductIdentification = property(__ClearedProductIdentification.value, __ClearedProductIdentification.set, None, None)

    
    # Element {http://www.w3schools.com}ClearingThresholdIndicator uses Python identifier ClearingThresholdIndicator
    __ClearingThresholdIndicator = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ClearingThresholdIndicator'), 'ClearingThresholdIndicator', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_httpwww_w3schools_comClearingThresholdIndicator', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1077, 3), )

    
    ClearingThresholdIndicator = property(__ClearingThresholdIndicator.value, __ClearingThresholdIndicator.set, None, None)

    
    # Element {http://www.w3schools.com}UnderlyingProductIdentifier uses Python identifier UnderlyingProductIdentifier
    __UnderlyingProductIdentifier = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'UnderlyingProductIdentifier'), 'UnderlyingProductIdentifier', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_httpwww_w3schools_comUnderlyingProductIdentifier', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1078, 3), )

    
    UnderlyingProductIdentifier = property(__UnderlyingProductIdentifier.value, __UnderlyingProductIdentifier.set, None, None)

    
    # Element {http://www.w3schools.com}IdentificationOfFinancialInstrument uses Python identifier IdentificationOfFinancialInstrument
    __IdentificationOfFinancialInstrument = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'IdentificationOfFinancialInstrument'), 'IdentificationOfFinancialInstrument', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_httpwww_w3schools_comIdentificationOfFinancialInstrument', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1079, 3), )

    
    IdentificationOfFinancialInstrument = property(__IdentificationOfFinancialInstrument.value, __IdentificationOfFinancialInstrument.set, None, None)

    
    # Element {http://www.w3schools.com}AllocationIndicator uses Python identifier AllocationIndicator
    __AllocationIndicator = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'AllocationIndicator'), 'AllocationIndicator', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_httpwww_w3schools_comAllocationIndicator', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1080, 3), )

    
    AllocationIndicator = property(__AllocationIndicator.value, __AllocationIndicator.set, None, None)

    
    # Element {http://www.w3schools.com}CollateralisationIndicator uses Python identifier CollateralisationIndicator
    __CollateralisationIndicator = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CollateralisationIndicator'), 'CollateralisationIndicator', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_httpwww_w3schools_comCollateralisationIndicator', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1081, 3), )

    
    CollateralisationIndicator = property(__CollateralisationIndicator.value, __CollateralisationIndicator.set, None, None)

    
    # Element {http://www.w3schools.com}ExecutionVenue uses Python identifier ExecutionVenue
    __ExecutionVenue = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ExecutionVenue'), 'ExecutionVenue', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_httpwww_w3schools_comExecutionVenue', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1082, 3), )

    
    ExecutionVenue = property(__ExecutionVenue.value, __ExecutionVenue.set, None, None)

    
    # Element {http://www.w3schools.com}ExecutionTimestamp uses Python identifier ExecutionTimestamp
    __ExecutionTimestamp = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ExecutionTimestamp'), 'ExecutionTimestamp', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_httpwww_w3schools_comExecutionTimestamp', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1083, 3), )

    
    ExecutionTimestamp = property(__ExecutionTimestamp.value, __ExecutionTimestamp.set, None, None)

    
    # Element {http://www.w3schools.com}NonStandardFlag uses Python identifier NonStandardFlag
    __NonStandardFlag = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'NonStandardFlag'), 'NonStandardFlag', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_httpwww_w3schools_comNonStandardFlag', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1084, 3), )

    
    NonStandardFlag = property(__NonStandardFlag.value, __NonStandardFlag.set, None, None)

    
    # Element {http://www.w3schools.com}FinancialNatureOfCounterpartyIndicator uses Python identifier FinancialNatureOfCounterpartyIndicator
    __FinancialNatureOfCounterpartyIndicator = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'FinancialNatureOfCounterpartyIndicator'), 'FinancialNatureOfCounterpartyIndicator', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_httpwww_w3schools_comFinancialNatureOfCounterpartyIndicator', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1085, 3), )

    
    FinancialNatureOfCounterpartyIndicator = property(__FinancialNatureOfCounterpartyIndicator.value, __FinancialNatureOfCounterpartyIndicator.set, None, None)

    
    # Element {http://www.w3schools.com}CollateralPortfolioIndicator uses Python identifier CollateralPortfolioIndicator
    __CollateralPortfolioIndicator = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CollateralPortfolioIndicator'), 'CollateralPortfolioIndicator', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_httpwww_w3schools_comCollateralPortfolioIndicator', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1086, 3), )

    
    CollateralPortfolioIndicator = property(__CollateralPortfolioIndicator.value, __CollateralPortfolioIndicator.set, None, None)

    
    # Element {http://www.w3schools.com}CollateralPortfolioCode uses Python identifier CollateralPortfolioCode
    __CollateralPortfolioCode = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CollateralPortfolioCode'), 'CollateralPortfolioCode', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_httpwww_w3schools_comCollateralPortfolioCode', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1087, 3), )

    
    CollateralPortfolioCode = property(__CollateralPortfolioCode.value, __CollateralPortfolioCode.set, None, None)

    
    # Element {http://www.w3schools.com}PortfolioCompressionIndicator uses Python identifier PortfolioCompressionIndicator
    __PortfolioCompressionIndicator = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PortfolioCompressionIndicator'), 'PortfolioCompressionIndicator', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_httpwww_w3schools_comPortfolioCompressionIndicator', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1088, 3), )

    
    PortfolioCompressionIndicator = property(__PortfolioCompressionIndicator.value, __PortfolioCompressionIndicator.set, None, None)

    
    # Element {http://www.w3schools.com}CorporateSectorIndicator uses Python identifier CorporateSectorIndicator
    __CorporateSectorIndicator = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CorporateSectorIndicator'), 'CorporateSectorIndicator', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_httpwww_w3schools_comCorporateSectorIndicator', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1089, 3), )

    
    CorporateSectorIndicator = property(__CorporateSectorIndicator.value, __CorporateSectorIndicator.set, None, None)

    
    # Element {http://www.w3schools.com}TradeWithNonEEACounterpartyIndicator uses Python identifier TradeWithNonEEACounterpartyIndicator
    __TradeWithNonEEACounterpartyIndicator = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'TradeWithNonEEACounterpartyIndicator'), 'TradeWithNonEEACounterpartyIndicator', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_httpwww_w3schools_comTradeWithNonEEACounterpartyIndicator', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1090, 3), )

    
    TradeWithNonEEACounterpartyIndicator = property(__TradeWithNonEEACounterpartyIndicator.value, __TradeWithNonEEACounterpartyIndicator.set, None, None)

    
    # Element {http://www.w3schools.com}IntragroupTradeIndicator uses Python identifier IntragroupTradeIndicator
    __IntragroupTradeIndicator = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'IntragroupTradeIndicator'), 'IntragroupTradeIndicator', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_httpwww_w3schools_comIntragroupTradeIndicator', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1091, 3), )

    
    IntragroupTradeIndicator = property(__IntragroupTradeIndicator.value, __IntragroupTradeIndicator.set, None, None)

    
    # Element {http://www.w3schools.com}CommercialOrTreasuryFinancingIndicator uses Python identifier CommercialOrTreasuryFinancingIndicator
    __CommercialOrTreasuryFinancingIndicator = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CommercialOrTreasuryFinancingIndicator'), 'CommercialOrTreasuryFinancingIndicator', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_httpwww_w3schools_comCommercialOrTreasuryFinancingIndicator', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1092, 3), )

    
    CommercialOrTreasuryFinancingIndicator = property(__CommercialOrTreasuryFinancingIndicator.value, __CommercialOrTreasuryFinancingIndicator.set, None, None)

    
    # Element {http://www.w3schools.com}CommissionAndFees uses Python identifier CommissionAndFees
    __CommissionAndFees = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CommissionAndFees'), 'CommissionAndFees', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_httpwww_w3schools_comCommissionAndFees', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1093, 3), )

    
    CommissionAndFees = property(__CommissionAndFees.value, __CommissionAndFees.set, None, None)

    
    # Element {http://www.w3schools.com}AdditionalReportingInformation uses Python identifier AdditionalReportingInformation
    __AdditionalReportingInformation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'AdditionalReportingInformation'), 'AdditionalReportingInformation', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_httpwww_w3schools_comAdditionalReportingInformation', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1094, 3), )

    
    AdditionalReportingInformation = property(__AdditionalReportingInformation.value, __AdditionalReportingInformation.set, None, None)

    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='15B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1096, 2)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1096, 2)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1097, 2)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1097, 2)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    
    # Attribute formatTag uses Python identifier formatTag
    __formatTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'formatTag'), 'formatTag', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_formatTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='False')
    __formatTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1098, 2)
    __formatTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1098, 2)
    
    formatTag = property(__formatTag.value, __formatTag.set, None, None)

    _ElementMap.update({
        __SubsequenceB1_ReportingParties.name() : __SubsequenceB1_ReportingParties,
        __CentralCounterpartyClearingHouse_A.name() : __CentralCounterpartyClearingHouse_A,
        __CentralCounterpartyClearingHouse_D.name() : __CentralCounterpartyClearingHouse_D,
        __CentralCounterpartyClearingHouse_J.name() : __CentralCounterpartyClearingHouse_J,
        __ClearingBroker_A.name() : __ClearingBroker_A,
        __ClearingBroker_D.name() : __ClearingBroker_D,
        __ClearingBroker_J.name() : __ClearingBroker_J,
        __ClearingExceptionParty_A.name() : __ClearingExceptionParty_A,
        __ClearingExceptionParty_D.name() : __ClearingExceptionParty_D,
        __ClearingExceptionParty_J.name() : __ClearingExceptionParty_J,
        __ClearingBrokerIdentification.name() : __ClearingBrokerIdentification,
        __ClearedProductIdentification.name() : __ClearedProductIdentification,
        __ClearingThresholdIndicator.name() : __ClearingThresholdIndicator,
        __UnderlyingProductIdentifier.name() : __UnderlyingProductIdentifier,
        __IdentificationOfFinancialInstrument.name() : __IdentificationOfFinancialInstrument,
        __AllocationIndicator.name() : __AllocationIndicator,
        __CollateralisationIndicator.name() : __CollateralisationIndicator,
        __ExecutionVenue.name() : __ExecutionVenue,
        __ExecutionTimestamp.name() : __ExecutionTimestamp,
        __NonStandardFlag.name() : __NonStandardFlag,
        __FinancialNatureOfCounterpartyIndicator.name() : __FinancialNatureOfCounterpartyIndicator,
        __CollateralPortfolioIndicator.name() : __CollateralPortfolioIndicator,
        __CollateralPortfolioCode.name() : __CollateralPortfolioCode,
        __PortfolioCompressionIndicator.name() : __PortfolioCompressionIndicator,
        __CorporateSectorIndicator.name() : __CorporateSectorIndicator,
        __TradeWithNonEEACounterpartyIndicator.name() : __TradeWithNonEEACounterpartyIndicator,
        __IntragroupTradeIndicator.name() : __IntragroupTradeIndicator,
        __CommercialOrTreasuryFinancingIndicator.name() : __CommercialOrTreasuryFinancingIndicator,
        __CommissionAndFees.name() : __CommissionAndFees,
        __AdditionalReportingInformation.name() : __AdditionalReportingInformation
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory,
        __formatTag.name() : __formatTag
    })
_module_typeBindings.MT305_SequenceB_ReportingInformation = MT305_SequenceB_ReportingInformation
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceB_ReportingInformation', MT305_SequenceB_ReportingInformation)


# Complex type {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties with content type ELEMENT_ONLY
class MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1100, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}ReportingJurisdiction uses Python identifier ReportingJurisdiction
    __ReportingJurisdiction = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ReportingJurisdiction'), 'ReportingJurisdiction', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_httpwww_w3schools_comReportingJurisdiction', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1102, 3), )

    
    ReportingJurisdiction = property(__ReportingJurisdiction.value, __ReportingJurisdiction.set, None, None)

    
    # Element {http://www.w3schools.com}ReportingParty_A uses Python identifier ReportingParty_A
    __ReportingParty_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ReportingParty_A'), 'ReportingParty_A', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_httpwww_w3schools_comReportingParty_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1104, 4), )

    
    ReportingParty_A = property(__ReportingParty_A.value, __ReportingParty_A.set, None, None)

    
    # Element {http://www.w3schools.com}ReportingParty_D uses Python identifier ReportingParty_D
    __ReportingParty_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ReportingParty_D'), 'ReportingParty_D', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_httpwww_w3schools_comReportingParty_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1105, 4), )

    
    ReportingParty_D = property(__ReportingParty_D.value, __ReportingParty_D.set, None, None)

    
    # Element {http://www.w3schools.com}ReportingParty_J uses Python identifier ReportingParty_J
    __ReportingParty_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ReportingParty_J'), 'ReportingParty_J', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_httpwww_w3schools_comReportingParty_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1106, 4), )

    
    ReportingParty_J = property(__ReportingParty_J.value, __ReportingParty_J.set, None, None)

    
    # Element {http://www.w3schools.com}SubsequenceB1a_UniqueTransactionIdentifier uses Python identifier SubsequenceB1a_UniqueTransactionIdentifier
    __SubsequenceB1a_UniqueTransactionIdentifier = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SubsequenceB1a_UniqueTransactionIdentifier'), 'SubsequenceB1a_UniqueTransactionIdentifier', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_httpwww_w3schools_comSubsequenceB1a_UniqueTransactionIdentifier', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1108, 3), )

    
    SubsequenceB1a_UniqueTransactionIdentifier = property(__SubsequenceB1a_UniqueTransactionIdentifier.value, __SubsequenceB1a_UniqueTransactionIdentifier.set, None, None)

    _ElementMap.update({
        __ReportingJurisdiction.name() : __ReportingJurisdiction,
        __ReportingParty_A.name() : __ReportingParty_A,
        __ReportingParty_D.name() : __ReportingParty_D,
        __ReportingParty_J.name() : __ReportingParty_J,
        __SubsequenceB1a_UniqueTransactionIdentifier.name() : __SubsequenceB1a_UniqueTransactionIdentifier
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties = MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties', MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties)


# Complex type {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier with content type ELEMENT_ONLY
class MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1111, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}UTINamespaceIssuerCode uses Python identifier UTINamespaceIssuerCode
    __UTINamespaceIssuerCode = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'UTINamespaceIssuerCode'), 'UTINamespaceIssuerCode', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_httpwww_w3schools_comUTINamespaceIssuerCode', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1113, 3), )

    
    UTINamespaceIssuerCode = property(__UTINamespaceIssuerCode.value, __UTINamespaceIssuerCode.set, None, None)

    
    # Element {http://www.w3schools.com}TransactionIdentifier uses Python identifier TransactionIdentifier
    __TransactionIdentifier = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'TransactionIdentifier'), 'TransactionIdentifier', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_httpwww_w3schools_comTransactionIdentifier', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1114, 3), )

    
    TransactionIdentifier = property(__TransactionIdentifier.value, __TransactionIdentifier.set, None, None)

    
    # Element {http://www.w3schools.com}SubsequenceB1a1_PriorUniqueTransactionIdentifier uses Python identifier SubsequenceB1a1_PriorUniqueTransactionIdentifier
    __SubsequenceB1a1_PriorUniqueTransactionIdentifier = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SubsequenceB1a1_PriorUniqueTransactionIdentifier'), 'SubsequenceB1a1_PriorUniqueTransactionIdentifier', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_httpwww_w3schools_comSubsequenceB1a1_PriorUniqueTransactionIdentifier', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1115, 3), )

    
    SubsequenceB1a1_PriorUniqueTransactionIdentifier = property(__SubsequenceB1a1_PriorUniqueTransactionIdentifier.value, __SubsequenceB1a1_PriorUniqueTransactionIdentifier.set, None, None)

    _ElementMap.update({
        __UTINamespaceIssuerCode.name() : __UTINamespaceIssuerCode,
        __TransactionIdentifier.name() : __TransactionIdentifier,
        __SubsequenceB1a1_PriorUniqueTransactionIdentifier.name() : __SubsequenceB1a1_PriorUniqueTransactionIdentifier
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier = MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier', MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier)


# Complex type {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_SubsequenceB1a1_PriorUniqueTransactionIdentifier with content type ELEMENT_ONLY
class MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_SubsequenceB1a1_PriorUniqueTransactionIdentifier (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_SubsequenceB1a1_PriorUniqueTransactionIdentifier with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_SubsequenceB1a1_PriorUniqueTransactionIdentifier')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1118, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}PUTINamespaceIssuerCode uses Python identifier PUTINamespaceIssuerCode
    __PUTINamespaceIssuerCode = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PUTINamespaceIssuerCode'), 'PUTINamespaceIssuerCode', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_SubsequenceB1a1_PriorUniqueTransactionIdentifier_httpwww_w3schools_comPUTINamespaceIssuerCode', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1120, 3), )

    
    PUTINamespaceIssuerCode = property(__PUTINamespaceIssuerCode.value, __PUTINamespaceIssuerCode.set, None, None)

    
    # Element {http://www.w3schools.com}PriorTransactionIdentifier uses Python identifier PriorTransactionIdentifier
    __PriorTransactionIdentifier = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PriorTransactionIdentifier'), 'PriorTransactionIdentifier', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_SubsequenceB1a1_PriorUniqueTransactionIdentifier_httpwww_w3schools_comPriorTransactionIdentifier', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1121, 3), )

    
    PriorTransactionIdentifier = property(__PriorTransactionIdentifier.value, __PriorTransactionIdentifier.set, None, None)

    _ElementMap.update({
        __PUTINamespaceIssuerCode.name() : __PUTINamespaceIssuerCode,
        __PriorTransactionIdentifier.name() : __PriorTransactionIdentifier
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_SubsequenceB1a1_PriorUniqueTransactionIdentifier = MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_SubsequenceB1a1_PriorUniqueTransactionIdentifier
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_SubsequenceB1a1_PriorUniqueTransactionIdentifier', MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_SubsequenceB1a1_PriorUniqueTransactionIdentifier)


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1125, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}SequenceA_GeneralInformation uses Python identifier SequenceA_GeneralInformation
    __SequenceA_GeneralInformation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SequenceA_GeneralInformation'), 'SequenceA_GeneralInformation', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comSequenceA_GeneralInformation', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1127, 4), )

    
    SequenceA_GeneralInformation = property(__SequenceA_GeneralInformation.value, __SequenceA_GeneralInformation.set, None, None)

    
    # Element {http://www.w3schools.com}SequenceB_ReportingInformation uses Python identifier SequenceB_ReportingInformation
    __SequenceB_ReportingInformation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SequenceB_ReportingInformation'), 'SequenceB_ReportingInformation', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comSequenceB_ReportingInformation', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1128, 4), )

    
    SequenceB_ReportingInformation = property(__SequenceB_ReportingInformation.value, __SequenceB_ReportingInformation.set, None, None)

    _ElementMap.update({
        __SequenceA_GeneralInformation.name() : __SequenceA_GeneralInformation,
        __SequenceB_ReportingInformation.name() : __SequenceB_ReportingInformation
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON = CTD_ANON


# Complex type {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_20_Type with content type SIMPLE
class MT305_SequenceA_GeneralInformation_20_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_20_Type with content type SIMPLE"""
    _TypeDefinition = MT305_SequenceA_GeneralInformation_20_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceA_GeneralInformation_20_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 8, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT305_SequenceA_GeneralInformation_20_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_20_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='20')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 11, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 11, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_20_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 12, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 12, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT305_SequenceA_GeneralInformation_20_Type = MT305_SequenceA_GeneralInformation_20_Type
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceA_GeneralInformation_20_Type', MT305_SequenceA_GeneralInformation_20_Type)


# Complex type {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_21_Type with content type SIMPLE
class MT305_SequenceA_GeneralInformation_21_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_21_Type with content type SIMPLE"""
    _TypeDefinition = MT305_SequenceA_GeneralInformation_21_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceA_GeneralInformation_21_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 21, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT305_SequenceA_GeneralInformation_21_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_21_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='21')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 24, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 24, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_21_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 25, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 25, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT305_SequenceA_GeneralInformation_21_Type = MT305_SequenceA_GeneralInformation_21_Type
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceA_GeneralInformation_21_Type', MT305_SequenceA_GeneralInformation_21_Type)


# Complex type {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_22_Type with content type SIMPLE
class MT305_SequenceA_GeneralInformation_22_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_22_Type with content type SIMPLE"""
    _TypeDefinition = MT305_SequenceA_GeneralInformation_22_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceA_GeneralInformation_22_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 34, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT305_SequenceA_GeneralInformation_22_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_22_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='22')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 37, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 37, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_22_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 38, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 38, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT305_SequenceA_GeneralInformation_22_Type = MT305_SequenceA_GeneralInformation_22_Type
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceA_GeneralInformation_22_Type', MT305_SequenceA_GeneralInformation_22_Type)


# Complex type {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_23_Type with content type SIMPLE
class MT305_SequenceA_GeneralInformation_23_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_23_Type with content type SIMPLE"""
    _TypeDefinition = MT305_SequenceA_GeneralInformation_23_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceA_GeneralInformation_23_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 47, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT305_SequenceA_GeneralInformation_23_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_23_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='23')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 50, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 50, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_23_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 51, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 51, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT305_SequenceA_GeneralInformation_23_Type = MT305_SequenceA_GeneralInformation_23_Type
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceA_GeneralInformation_23_Type', MT305_SequenceA_GeneralInformation_23_Type)


# Complex type {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_94A_Type with content type SIMPLE
class MT305_SequenceA_GeneralInformation_94A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_94A_Type with content type SIMPLE"""
    _TypeDefinition = MT305_SequenceA_GeneralInformation_94A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceA_GeneralInformation_94A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 60, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT305_SequenceA_GeneralInformation_94A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_94A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='94A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 63, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 63, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_94A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 64, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 64, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT305_SequenceA_GeneralInformation_94A_Type = MT305_SequenceA_GeneralInformation_94A_Type
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceA_GeneralInformation_94A_Type', MT305_SequenceA_GeneralInformation_94A_Type)


# Complex type {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_82A_Type with content type SIMPLE
class MT305_SequenceA_GeneralInformation_82A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_82A_Type with content type SIMPLE"""
    _TypeDefinition = MT305_SequenceA_GeneralInformation_82A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceA_GeneralInformation_82A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 73, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT305_SequenceA_GeneralInformation_82A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_82A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='82A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 76, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 76, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_82A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 77, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 77, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT305_SequenceA_GeneralInformation_82A_Type = MT305_SequenceA_GeneralInformation_82A_Type
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceA_GeneralInformation_82A_Type', MT305_SequenceA_GeneralInformation_82A_Type)


# Complex type {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_82D_Type with content type SIMPLE
class MT305_SequenceA_GeneralInformation_82D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_82D_Type with content type SIMPLE"""
    _TypeDefinition = MT305_SequenceA_GeneralInformation_82D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceA_GeneralInformation_82D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 86, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT305_SequenceA_GeneralInformation_82D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_82D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='82D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 89, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 89, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_82D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 90, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 90, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT305_SequenceA_GeneralInformation_82D_Type = MT305_SequenceA_GeneralInformation_82D_Type
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceA_GeneralInformation_82D_Type', MT305_SequenceA_GeneralInformation_82D_Type)


# Complex type {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_82J_Type with content type SIMPLE
class MT305_SequenceA_GeneralInformation_82J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_82J_Type with content type SIMPLE"""
    _TypeDefinition = MT305_SequenceA_GeneralInformation_82J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceA_GeneralInformation_82J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 99, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT305_SequenceA_GeneralInformation_82J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_82J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='82J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 102, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 102, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_82J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 103, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 103, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT305_SequenceA_GeneralInformation_82J_Type = MT305_SequenceA_GeneralInformation_82J_Type
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceA_GeneralInformation_82J_Type', MT305_SequenceA_GeneralInformation_82J_Type)


# Complex type {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_87A_Type with content type SIMPLE
class MT305_SequenceA_GeneralInformation_87A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_87A_Type with content type SIMPLE"""
    _TypeDefinition = MT305_SequenceA_GeneralInformation_87A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceA_GeneralInformation_87A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 112, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT305_SequenceA_GeneralInformation_87A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_87A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='87A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 115, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 115, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_87A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 116, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 116, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT305_SequenceA_GeneralInformation_87A_Type = MT305_SequenceA_GeneralInformation_87A_Type
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceA_GeneralInformation_87A_Type', MT305_SequenceA_GeneralInformation_87A_Type)


# Complex type {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_87D_Type with content type SIMPLE
class MT305_SequenceA_GeneralInformation_87D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_87D_Type with content type SIMPLE"""
    _TypeDefinition = MT305_SequenceA_GeneralInformation_87D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceA_GeneralInformation_87D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 125, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT305_SequenceA_GeneralInformation_87D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_87D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='87D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 128, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 128, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_87D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 129, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 129, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT305_SequenceA_GeneralInformation_87D_Type = MT305_SequenceA_GeneralInformation_87D_Type
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceA_GeneralInformation_87D_Type', MT305_SequenceA_GeneralInformation_87D_Type)


# Complex type {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_87J_Type with content type SIMPLE
class MT305_SequenceA_GeneralInformation_87J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_87J_Type with content type SIMPLE"""
    _TypeDefinition = MT305_SequenceA_GeneralInformation_87J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceA_GeneralInformation_87J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 138, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT305_SequenceA_GeneralInformation_87J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_87J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='87J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 141, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 141, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_87J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 142, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 142, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT305_SequenceA_GeneralInformation_87J_Type = MT305_SequenceA_GeneralInformation_87J_Type
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceA_GeneralInformation_87J_Type', MT305_SequenceA_GeneralInformation_87J_Type)


# Complex type {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_83A_Type with content type SIMPLE
class MT305_SequenceA_GeneralInformation_83A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_83A_Type with content type SIMPLE"""
    _TypeDefinition = MT305_SequenceA_GeneralInformation_83A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceA_GeneralInformation_83A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 151, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT305_SequenceA_GeneralInformation_83A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_83A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='83A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 154, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 154, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_83A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 155, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 155, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT305_SequenceA_GeneralInformation_83A_Type = MT305_SequenceA_GeneralInformation_83A_Type
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceA_GeneralInformation_83A_Type', MT305_SequenceA_GeneralInformation_83A_Type)


# Complex type {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_83D_Type with content type SIMPLE
class MT305_SequenceA_GeneralInformation_83D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_83D_Type with content type SIMPLE"""
    _TypeDefinition = MT305_SequenceA_GeneralInformation_83D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceA_GeneralInformation_83D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 164, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT305_SequenceA_GeneralInformation_83D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_83D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='83D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 167, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 167, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_83D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 168, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 168, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT305_SequenceA_GeneralInformation_83D_Type = MT305_SequenceA_GeneralInformation_83D_Type
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceA_GeneralInformation_83D_Type', MT305_SequenceA_GeneralInformation_83D_Type)


# Complex type {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_83J_Type with content type SIMPLE
class MT305_SequenceA_GeneralInformation_83J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_83J_Type with content type SIMPLE"""
    _TypeDefinition = MT305_SequenceA_GeneralInformation_83J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceA_GeneralInformation_83J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 177, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT305_SequenceA_GeneralInformation_83J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_83J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='83J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 180, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 180, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_83J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 181, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 181, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT305_SequenceA_GeneralInformation_83J_Type = MT305_SequenceA_GeneralInformation_83J_Type
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceA_GeneralInformation_83J_Type', MT305_SequenceA_GeneralInformation_83J_Type)


# Complex type {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_30_Type with content type SIMPLE
class MT305_SequenceA_GeneralInformation_30_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_30_Type with content type SIMPLE"""
    _TypeDefinition = MT305_SequenceA_GeneralInformation_30_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceA_GeneralInformation_30_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 190, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT305_SequenceA_GeneralInformation_30_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_30_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='30')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 193, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 193, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_30_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 194, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 194, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT305_SequenceA_GeneralInformation_30_Type = MT305_SequenceA_GeneralInformation_30_Type
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceA_GeneralInformation_30_Type', MT305_SequenceA_GeneralInformation_30_Type)


# Complex type {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_31C_Type with content type SIMPLE
class MT305_SequenceA_GeneralInformation_31C_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_31C_Type with content type SIMPLE"""
    _TypeDefinition = MT305_SequenceA_GeneralInformation_31C_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceA_GeneralInformation_31C_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 203, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT305_SequenceA_GeneralInformation_31C_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_31C_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='31C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 206, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 206, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_31C_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 207, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 207, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT305_SequenceA_GeneralInformation_31C_Type = MT305_SequenceA_GeneralInformation_31C_Type
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceA_GeneralInformation_31C_Type', MT305_SequenceA_GeneralInformation_31C_Type)


# Complex type {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_31G_Type with content type SIMPLE
class MT305_SequenceA_GeneralInformation_31G_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_31G_Type with content type SIMPLE"""
    _TypeDefinition = MT305_SequenceA_GeneralInformation_31G_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceA_GeneralInformation_31G_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 216, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT305_SequenceA_GeneralInformation_31G_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_31G_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='31G')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 219, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 219, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_31G_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 220, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 220, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT305_SequenceA_GeneralInformation_31G_Type = MT305_SequenceA_GeneralInformation_31G_Type
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceA_GeneralInformation_31G_Type', MT305_SequenceA_GeneralInformation_31G_Type)


# Complex type {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_31E_Type with content type SIMPLE
class MT305_SequenceA_GeneralInformation_31E_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_31E_Type with content type SIMPLE"""
    _TypeDefinition = MT305_SequenceA_GeneralInformation_31E_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceA_GeneralInformation_31E_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 229, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT305_SequenceA_GeneralInformation_31E_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_31E_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='31E')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 232, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 232, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_31E_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 233, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 233, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT305_SequenceA_GeneralInformation_31E_Type = MT305_SequenceA_GeneralInformation_31E_Type
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceA_GeneralInformation_31E_Type', MT305_SequenceA_GeneralInformation_31E_Type)


# Complex type {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_26F_Type with content type SIMPLE
class MT305_SequenceA_GeneralInformation_26F_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_26F_Type with content type SIMPLE"""
    _TypeDefinition = MT305_SequenceA_GeneralInformation_26F_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceA_GeneralInformation_26F_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 242, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT305_SequenceA_GeneralInformation_26F_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_26F_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='26F')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 245, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 245, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_26F_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 246, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 246, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT305_SequenceA_GeneralInformation_26F_Type = MT305_SequenceA_GeneralInformation_26F_Type
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceA_GeneralInformation_26F_Type', MT305_SequenceA_GeneralInformation_26F_Type)


# Complex type {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_39M_Type with content type SIMPLE
class MT305_SequenceA_GeneralInformation_39M_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_39M_Type with content type SIMPLE"""
    _TypeDefinition = MT305_SequenceA_GeneralInformation_39M_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceA_GeneralInformation_39M_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 255, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT305_SequenceA_GeneralInformation_39M_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_39M_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='39M')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 258, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 258, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_39M_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 259, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 259, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT305_SequenceA_GeneralInformation_39M_Type = MT305_SequenceA_GeneralInformation_39M_Type
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceA_GeneralInformation_39M_Type', MT305_SequenceA_GeneralInformation_39M_Type)


# Complex type {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_17F_Type with content type SIMPLE
class MT305_SequenceA_GeneralInformation_17F_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_17F_Type with content type SIMPLE"""
    _TypeDefinition = MT305_SequenceA_GeneralInformation_17F_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceA_GeneralInformation_17F_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 268, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT305_SequenceA_GeneralInformation_17F_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_17F_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='17F')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 271, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 271, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_17F_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 272, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 272, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT305_SequenceA_GeneralInformation_17F_Type = MT305_SequenceA_GeneralInformation_17F_Type
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceA_GeneralInformation_17F_Type', MT305_SequenceA_GeneralInformation_17F_Type)


# Complex type {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_14S_Type with content type SIMPLE
class MT305_SequenceA_GeneralInformation_14S_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_14S_Type with content type SIMPLE"""
    _TypeDefinition = MT305_SequenceA_GeneralInformation_14S_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceA_GeneralInformation_14S_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 281, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT305_SequenceA_GeneralInformation_14S_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_14S_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='14S')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 284, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 284, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_14S_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 285, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 285, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT305_SequenceA_GeneralInformation_14S_Type = MT305_SequenceA_GeneralInformation_14S_Type
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceA_GeneralInformation_14S_Type', MT305_SequenceA_GeneralInformation_14S_Type)


# Complex type {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_32E_Type with content type SIMPLE
class MT305_SequenceA_GeneralInformation_32E_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_32E_Type with content type SIMPLE"""
    _TypeDefinition = MT305_SequenceA_GeneralInformation_32E_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceA_GeneralInformation_32E_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 294, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT305_SequenceA_GeneralInformation_32E_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_32E_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='32E')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 297, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 297, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_32E_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 298, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 298, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT305_SequenceA_GeneralInformation_32E_Type = MT305_SequenceA_GeneralInformation_32E_Type
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceA_GeneralInformation_32E_Type', MT305_SequenceA_GeneralInformation_32E_Type)


# Complex type {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_32B_Type with content type SIMPLE
class MT305_SequenceA_GeneralInformation_32B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_32B_Type with content type SIMPLE"""
    _TypeDefinition = MT305_SequenceA_GeneralInformation_32B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceA_GeneralInformation_32B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 307, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT305_SequenceA_GeneralInformation_32B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_32B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='32B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 310, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 310, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_32B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 311, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 311, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT305_SequenceA_GeneralInformation_32B_Type = MT305_SequenceA_GeneralInformation_32B_Type
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceA_GeneralInformation_32B_Type', MT305_SequenceA_GeneralInformation_32B_Type)


# Complex type {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_36_Type with content type SIMPLE
class MT305_SequenceA_GeneralInformation_36_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_36_Type with content type SIMPLE"""
    _TypeDefinition = MT305_SequenceA_GeneralInformation_36_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceA_GeneralInformation_36_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 320, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT305_SequenceA_GeneralInformation_36_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_36_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='36')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 323, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 323, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_36_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 324, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 324, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT305_SequenceA_GeneralInformation_36_Type = MT305_SequenceA_GeneralInformation_36_Type
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceA_GeneralInformation_36_Type', MT305_SequenceA_GeneralInformation_36_Type)


# Complex type {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_33B_Type with content type SIMPLE
class MT305_SequenceA_GeneralInformation_33B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_33B_Type with content type SIMPLE"""
    _TypeDefinition = MT305_SequenceA_GeneralInformation_33B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceA_GeneralInformation_33B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 333, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT305_SequenceA_GeneralInformation_33B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_33B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='33B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 336, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 336, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_33B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 337, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 337, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT305_SequenceA_GeneralInformation_33B_Type = MT305_SequenceA_GeneralInformation_33B_Type
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceA_GeneralInformation_33B_Type', MT305_SequenceA_GeneralInformation_33B_Type)


# Complex type {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_37K_Type with content type SIMPLE
class MT305_SequenceA_GeneralInformation_37K_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_37K_Type with content type SIMPLE"""
    _TypeDefinition = MT305_SequenceA_GeneralInformation_37K_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceA_GeneralInformation_37K_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 346, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT305_SequenceA_GeneralInformation_37K_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_37K_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='37K')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 349, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 349, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_37K_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 350, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 350, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT305_SequenceA_GeneralInformation_37K_Type = MT305_SequenceA_GeneralInformation_37K_Type
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceA_GeneralInformation_37K_Type', MT305_SequenceA_GeneralInformation_37K_Type)


# Complex type {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_34P_Type with content type SIMPLE
class MT305_SequenceA_GeneralInformation_34P_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_34P_Type with content type SIMPLE"""
    _TypeDefinition = MT305_SequenceA_GeneralInformation_34P_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceA_GeneralInformation_34P_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 359, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT305_SequenceA_GeneralInformation_34P_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_34P_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='34P')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 362, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 362, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_34P_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 363, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 363, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT305_SequenceA_GeneralInformation_34P_Type = MT305_SequenceA_GeneralInformation_34P_Type
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceA_GeneralInformation_34P_Type', MT305_SequenceA_GeneralInformation_34P_Type)


# Complex type {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_34R_Type with content type SIMPLE
class MT305_SequenceA_GeneralInformation_34R_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_34R_Type with content type SIMPLE"""
    _TypeDefinition = MT305_SequenceA_GeneralInformation_34R_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceA_GeneralInformation_34R_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 372, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT305_SequenceA_GeneralInformation_34R_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_34R_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='34R')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 375, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 375, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_34R_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 376, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 376, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT305_SequenceA_GeneralInformation_34R_Type = MT305_SequenceA_GeneralInformation_34R_Type
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceA_GeneralInformation_34R_Type', MT305_SequenceA_GeneralInformation_34R_Type)


# Complex type {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_53A_Type with content type SIMPLE
class MT305_SequenceA_GeneralInformation_53A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_53A_Type with content type SIMPLE"""
    _TypeDefinition = MT305_SequenceA_GeneralInformation_53A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceA_GeneralInformation_53A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 385, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT305_SequenceA_GeneralInformation_53A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_53A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='53A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 388, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 388, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_53A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 389, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 389, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT305_SequenceA_GeneralInformation_53A_Type = MT305_SequenceA_GeneralInformation_53A_Type
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceA_GeneralInformation_53A_Type', MT305_SequenceA_GeneralInformation_53A_Type)


# Complex type {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_53D_Type with content type SIMPLE
class MT305_SequenceA_GeneralInformation_53D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_53D_Type with content type SIMPLE"""
    _TypeDefinition = MT305_SequenceA_GeneralInformation_53D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceA_GeneralInformation_53D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 398, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT305_SequenceA_GeneralInformation_53D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_53D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='53D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 401, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 401, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_53D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 402, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 402, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT305_SequenceA_GeneralInformation_53D_Type = MT305_SequenceA_GeneralInformation_53D_Type
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceA_GeneralInformation_53D_Type', MT305_SequenceA_GeneralInformation_53D_Type)


# Complex type {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_53J_Type with content type SIMPLE
class MT305_SequenceA_GeneralInformation_53J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_53J_Type with content type SIMPLE"""
    _TypeDefinition = MT305_SequenceA_GeneralInformation_53J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceA_GeneralInformation_53J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 411, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT305_SequenceA_GeneralInformation_53J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_53J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='53J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 414, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 414, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_53J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 415, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 415, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT305_SequenceA_GeneralInformation_53J_Type = MT305_SequenceA_GeneralInformation_53J_Type
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceA_GeneralInformation_53J_Type', MT305_SequenceA_GeneralInformation_53J_Type)


# Complex type {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_56A_Type with content type SIMPLE
class MT305_SequenceA_GeneralInformation_56A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_56A_Type with content type SIMPLE"""
    _TypeDefinition = MT305_SequenceA_GeneralInformation_56A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceA_GeneralInformation_56A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 424, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT305_SequenceA_GeneralInformation_56A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_56A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='56A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 427, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 427, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_56A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 428, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 428, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT305_SequenceA_GeneralInformation_56A_Type = MT305_SequenceA_GeneralInformation_56A_Type
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceA_GeneralInformation_56A_Type', MT305_SequenceA_GeneralInformation_56A_Type)


# Complex type {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_56D_Type with content type SIMPLE
class MT305_SequenceA_GeneralInformation_56D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_56D_Type with content type SIMPLE"""
    _TypeDefinition = MT305_SequenceA_GeneralInformation_56D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceA_GeneralInformation_56D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 437, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT305_SequenceA_GeneralInformation_56D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_56D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='56D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 440, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 440, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_56D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 441, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 441, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT305_SequenceA_GeneralInformation_56D_Type = MT305_SequenceA_GeneralInformation_56D_Type
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceA_GeneralInformation_56D_Type', MT305_SequenceA_GeneralInformation_56D_Type)


# Complex type {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_57A_Type with content type SIMPLE
class MT305_SequenceA_GeneralInformation_57A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_57A_Type with content type SIMPLE"""
    _TypeDefinition = MT305_SequenceA_GeneralInformation_57A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceA_GeneralInformation_57A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 450, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT305_SequenceA_GeneralInformation_57A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_57A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='57A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 453, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 453, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_57A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 454, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 454, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT305_SequenceA_GeneralInformation_57A_Type = MT305_SequenceA_GeneralInformation_57A_Type
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceA_GeneralInformation_57A_Type', MT305_SequenceA_GeneralInformation_57A_Type)


# Complex type {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_57D_Type with content type SIMPLE
class MT305_SequenceA_GeneralInformation_57D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_57D_Type with content type SIMPLE"""
    _TypeDefinition = MT305_SequenceA_GeneralInformation_57D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceA_GeneralInformation_57D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 463, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT305_SequenceA_GeneralInformation_57D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_57D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='57D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 466, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 466, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_57D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 467, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 467, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT305_SequenceA_GeneralInformation_57D_Type = MT305_SequenceA_GeneralInformation_57D_Type
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceA_GeneralInformation_57D_Type', MT305_SequenceA_GeneralInformation_57D_Type)


# Complex type {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_77H_Type with content type SIMPLE
class MT305_SequenceA_GeneralInformation_77H_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_77H_Type with content type SIMPLE"""
    _TypeDefinition = MT305_SequenceA_GeneralInformation_77H_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceA_GeneralInformation_77H_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 476, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT305_SequenceA_GeneralInformation_77H_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_77H_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='77H')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 479, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 479, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_77H_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 480, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 480, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT305_SequenceA_GeneralInformation_77H_Type = MT305_SequenceA_GeneralInformation_77H_Type
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceA_GeneralInformation_77H_Type', MT305_SequenceA_GeneralInformation_77H_Type)


# Complex type {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_14C_Type with content type SIMPLE
class MT305_SequenceA_GeneralInformation_14C_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_14C_Type with content type SIMPLE"""
    _TypeDefinition = MT305_SequenceA_GeneralInformation_14C_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceA_GeneralInformation_14C_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 489, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT305_SequenceA_GeneralInformation_14C_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_14C_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='14C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 492, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 492, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_14C_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 493, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 493, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT305_SequenceA_GeneralInformation_14C_Type = MT305_SequenceA_GeneralInformation_14C_Type
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceA_GeneralInformation_14C_Type', MT305_SequenceA_GeneralInformation_14C_Type)


# Complex type {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_72_Type with content type SIMPLE
class MT305_SequenceA_GeneralInformation_72_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT305_SequenceA_GeneralInformation_72_Type with content type SIMPLE"""
    _TypeDefinition = MT305_SequenceA_GeneralInformation_72_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceA_GeneralInformation_72_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 502, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT305_SequenceA_GeneralInformation_72_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_72_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='72')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 505, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 505, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT305_SequenceA_GeneralInformation_72_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 506, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 506, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT305_SequenceA_GeneralInformation_72_Type = MT305_SequenceA_GeneralInformation_72_Type
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceA_GeneralInformation_72_Type', MT305_SequenceA_GeneralInformation_72_Type)


# Complex type {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_22L_Type with content type SIMPLE
class MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_22L_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_22L_Type with content type SIMPLE"""
    _TypeDefinition = MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_22L_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_22L_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 515, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_22L_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_22L_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='22L')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 518, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 518, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_22L_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 519, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 519, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_22L_Type = MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_22L_Type
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_22L_Type', MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_22L_Type)


# Complex type {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_91A_Type with content type SIMPLE
class MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_91A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_91A_Type with content type SIMPLE"""
    _TypeDefinition = MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_91A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_91A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 528, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_91A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_91A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='91A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 531, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 531, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_91A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 532, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 532, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_91A_Type = MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_91A_Type
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_91A_Type', MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_91A_Type)


# Complex type {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_91D_Type with content type SIMPLE
class MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_91D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_91D_Type with content type SIMPLE"""
    _TypeDefinition = MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_91D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_91D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 541, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_91D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_91D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='91D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 544, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 544, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_91D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 545, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 545, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_91D_Type = MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_91D_Type
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_91D_Type', MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_91D_Type)


# Complex type {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_91J_Type with content type SIMPLE
class MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_91J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_91J_Type with content type SIMPLE"""
    _TypeDefinition = MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_91J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_91J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 554, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_91J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_91J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='91J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 557, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 557, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_91J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 558, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 558, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_91J_Type = MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_91J_Type
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_91J_Type', MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_91J_Type)


# Complex type {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_22M_Type with content type SIMPLE
class MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_22M_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_22M_Type with content type SIMPLE"""
    _TypeDefinition = MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_22M_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_22M_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 567, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_22M_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_22M_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='22M')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 570, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 570, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_22M_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 571, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 571, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_22M_Type = MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_22M_Type
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_22M_Type', MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_22M_Type)


# Complex type {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_22N_Type with content type SIMPLE
class MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_22N_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_22N_Type with content type SIMPLE"""
    _TypeDefinition = MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_22N_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_22N_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 580, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_22N_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_22N_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='22N')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 583, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 583, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_22N_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 584, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 584, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_22N_Type = MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_22N_Type
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_22N_Type', MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_22N_Type)


# Complex type {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_SubsequenceB1a1_PriorUniqueTransactionIdentifier_22P_Type with content type SIMPLE
class MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_SubsequenceB1a1_PriorUniqueTransactionIdentifier_22P_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_SubsequenceB1a1_PriorUniqueTransactionIdentifier_22P_Type with content type SIMPLE"""
    _TypeDefinition = MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_SubsequenceB1a1_PriorUniqueTransactionIdentifier_22P_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_SubsequenceB1a1_PriorUniqueTransactionIdentifier_22P_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 593, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_SubsequenceB1a1_PriorUniqueTransactionIdentifier_22P_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_SubsequenceB1a1_PriorUniqueTransactionIdentifier_22P_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='22P')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 596, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 596, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_SubsequenceB1a1_PriorUniqueTransactionIdentifier_22P_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 597, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 597, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_SubsequenceB1a1_PriorUniqueTransactionIdentifier_22P_Type = MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_SubsequenceB1a1_PriorUniqueTransactionIdentifier_22P_Type
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_SubsequenceB1a1_PriorUniqueTransactionIdentifier_22P_Type', MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_SubsequenceB1a1_PriorUniqueTransactionIdentifier_22P_Type)


# Complex type {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_SubsequenceB1a1_PriorUniqueTransactionIdentifier_22R_Type with content type SIMPLE
class MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_SubsequenceB1a1_PriorUniqueTransactionIdentifier_22R_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_SubsequenceB1a1_PriorUniqueTransactionIdentifier_22R_Type with content type SIMPLE"""
    _TypeDefinition = MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_SubsequenceB1a1_PriorUniqueTransactionIdentifier_22R_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_SubsequenceB1a1_PriorUniqueTransactionIdentifier_22R_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 606, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_SubsequenceB1a1_PriorUniqueTransactionIdentifier_22R_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_SubsequenceB1a1_PriorUniqueTransactionIdentifier_22R_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='22R')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 609, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 609, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_SubsequenceB1a1_PriorUniqueTransactionIdentifier_22R_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 610, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 610, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_SubsequenceB1a1_PriorUniqueTransactionIdentifier_22R_Type = MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_SubsequenceB1a1_PriorUniqueTransactionIdentifier_22R_Type
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_SubsequenceB1a1_PriorUniqueTransactionIdentifier_22R_Type', MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_SubsequenceB1a1_PriorUniqueTransactionIdentifier_22R_Type)


# Complex type {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_81A_Type with content type SIMPLE
class MT305_SequenceB_ReportingInformation_81A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_81A_Type with content type SIMPLE"""
    _TypeDefinition = MT305_SequenceB_ReportingInformation_81A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceB_ReportingInformation_81A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 619, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT305_SequenceB_ReportingInformation_81A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_81A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='81A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 622, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 622, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_81A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 623, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 623, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT305_SequenceB_ReportingInformation_81A_Type = MT305_SequenceB_ReportingInformation_81A_Type
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceB_ReportingInformation_81A_Type', MT305_SequenceB_ReportingInformation_81A_Type)


# Complex type {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_81D_Type with content type SIMPLE
class MT305_SequenceB_ReportingInformation_81D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_81D_Type with content type SIMPLE"""
    _TypeDefinition = MT305_SequenceB_ReportingInformation_81D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceB_ReportingInformation_81D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 632, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT305_SequenceB_ReportingInformation_81D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_81D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='81D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 635, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 635, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_81D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 636, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 636, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT305_SequenceB_ReportingInformation_81D_Type = MT305_SequenceB_ReportingInformation_81D_Type
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceB_ReportingInformation_81D_Type', MT305_SequenceB_ReportingInformation_81D_Type)


# Complex type {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_81J_Type with content type SIMPLE
class MT305_SequenceB_ReportingInformation_81J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_81J_Type with content type SIMPLE"""
    _TypeDefinition = MT305_SequenceB_ReportingInformation_81J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceB_ReportingInformation_81J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 645, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT305_SequenceB_ReportingInformation_81J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_81J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='81J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 648, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 648, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_81J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 649, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 649, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT305_SequenceB_ReportingInformation_81J_Type = MT305_SequenceB_ReportingInformation_81J_Type
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceB_ReportingInformation_81J_Type', MT305_SequenceB_ReportingInformation_81J_Type)


# Complex type {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_89A_Type with content type SIMPLE
class MT305_SequenceB_ReportingInformation_89A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_89A_Type with content type SIMPLE"""
    _TypeDefinition = MT305_SequenceB_ReportingInformation_89A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceB_ReportingInformation_89A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 658, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT305_SequenceB_ReportingInformation_89A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_89A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='89A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 661, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 661, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_89A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 662, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 662, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT305_SequenceB_ReportingInformation_89A_Type = MT305_SequenceB_ReportingInformation_89A_Type
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceB_ReportingInformation_89A_Type', MT305_SequenceB_ReportingInformation_89A_Type)


# Complex type {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_89D_Type with content type SIMPLE
class MT305_SequenceB_ReportingInformation_89D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_89D_Type with content type SIMPLE"""
    _TypeDefinition = MT305_SequenceB_ReportingInformation_89D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceB_ReportingInformation_89D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 671, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT305_SequenceB_ReportingInformation_89D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_89D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='89D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 674, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 674, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_89D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 675, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 675, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT305_SequenceB_ReportingInformation_89D_Type = MT305_SequenceB_ReportingInformation_89D_Type
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceB_ReportingInformation_89D_Type', MT305_SequenceB_ReportingInformation_89D_Type)


# Complex type {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_89J_Type with content type SIMPLE
class MT305_SequenceB_ReportingInformation_89J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_89J_Type with content type SIMPLE"""
    _TypeDefinition = MT305_SequenceB_ReportingInformation_89J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceB_ReportingInformation_89J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 684, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT305_SequenceB_ReportingInformation_89J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_89J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='89J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 687, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 687, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_89J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 688, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 688, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT305_SequenceB_ReportingInformation_89J_Type = MT305_SequenceB_ReportingInformation_89J_Type
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceB_ReportingInformation_89J_Type', MT305_SequenceB_ReportingInformation_89J_Type)


# Complex type {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_96A_Type with content type SIMPLE
class MT305_SequenceB_ReportingInformation_96A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_96A_Type with content type SIMPLE"""
    _TypeDefinition = MT305_SequenceB_ReportingInformation_96A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceB_ReportingInformation_96A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 697, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT305_SequenceB_ReportingInformation_96A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_96A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='96A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 700, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 700, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_96A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 701, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 701, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT305_SequenceB_ReportingInformation_96A_Type = MT305_SequenceB_ReportingInformation_96A_Type
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceB_ReportingInformation_96A_Type', MT305_SequenceB_ReportingInformation_96A_Type)


# Complex type {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_96D_Type with content type SIMPLE
class MT305_SequenceB_ReportingInformation_96D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_96D_Type with content type SIMPLE"""
    _TypeDefinition = MT305_SequenceB_ReportingInformation_96D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceB_ReportingInformation_96D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 710, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT305_SequenceB_ReportingInformation_96D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_96D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='96D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 713, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 713, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_96D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 714, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 714, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT305_SequenceB_ReportingInformation_96D_Type = MT305_SequenceB_ReportingInformation_96D_Type
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceB_ReportingInformation_96D_Type', MT305_SequenceB_ReportingInformation_96D_Type)


# Complex type {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_96J_Type with content type SIMPLE
class MT305_SequenceB_ReportingInformation_96J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_96J_Type with content type SIMPLE"""
    _TypeDefinition = MT305_SequenceB_ReportingInformation_96J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceB_ReportingInformation_96J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 723, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT305_SequenceB_ReportingInformation_96J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_96J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='96J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 726, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 726, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_96J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 727, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 727, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT305_SequenceB_ReportingInformation_96J_Type = MT305_SequenceB_ReportingInformation_96J_Type
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceB_ReportingInformation_96J_Type', MT305_SequenceB_ReportingInformation_96J_Type)


# Complex type {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_22S_Type with content type SIMPLE
class MT305_SequenceB_ReportingInformation_22S_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_22S_Type with content type SIMPLE"""
    _TypeDefinition = MT305_SequenceB_ReportingInformation_22S_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceB_ReportingInformation_22S_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 736, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT305_SequenceB_ReportingInformation_22S_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_22S_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='22S')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 739, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 739, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_22S_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 740, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 740, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT305_SequenceB_ReportingInformation_22S_Type = MT305_SequenceB_ReportingInformation_22S_Type
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceB_ReportingInformation_22S_Type', MT305_SequenceB_ReportingInformation_22S_Type)


# Complex type {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_22T_Type with content type SIMPLE
class MT305_SequenceB_ReportingInformation_22T_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_22T_Type with content type SIMPLE"""
    _TypeDefinition = MT305_SequenceB_ReportingInformation_22T_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceB_ReportingInformation_22T_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 749, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT305_SequenceB_ReportingInformation_22T_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_22T_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='22T')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 752, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 752, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_22T_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 753, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 753, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT305_SequenceB_ReportingInformation_22T_Type = MT305_SequenceB_ReportingInformation_22T_Type
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceB_ReportingInformation_22T_Type', MT305_SequenceB_ReportingInformation_22T_Type)


# Complex type {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_17E_Type with content type SIMPLE
class MT305_SequenceB_ReportingInformation_17E_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_17E_Type with content type SIMPLE"""
    _TypeDefinition = MT305_SequenceB_ReportingInformation_17E_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceB_ReportingInformation_17E_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 762, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT305_SequenceB_ReportingInformation_17E_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_17E_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='17E')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 765, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 765, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_17E_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 766, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 766, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT305_SequenceB_ReportingInformation_17E_Type = MT305_SequenceB_ReportingInformation_17E_Type
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceB_ReportingInformation_17E_Type', MT305_SequenceB_ReportingInformation_17E_Type)


# Complex type {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_22U_Type with content type SIMPLE
class MT305_SequenceB_ReportingInformation_22U_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_22U_Type with content type SIMPLE"""
    _TypeDefinition = MT305_SequenceB_ReportingInformation_22U_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceB_ReportingInformation_22U_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 775, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT305_SequenceB_ReportingInformation_22U_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_22U_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='22U')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 778, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 778, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_22U_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 779, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 779, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT305_SequenceB_ReportingInformation_22U_Type = MT305_SequenceB_ReportingInformation_22U_Type
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceB_ReportingInformation_22U_Type', MT305_SequenceB_ReportingInformation_22U_Type)


# Complex type {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_35B_Type with content type SIMPLE
class MT305_SequenceB_ReportingInformation_35B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_35B_Type with content type SIMPLE"""
    _TypeDefinition = MT305_SequenceB_ReportingInformation_35B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceB_ReportingInformation_35B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 788, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT305_SequenceB_ReportingInformation_35B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_35B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='35B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 791, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 791, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_35B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 792, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 792, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT305_SequenceB_ReportingInformation_35B_Type = MT305_SequenceB_ReportingInformation_35B_Type
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceB_ReportingInformation_35B_Type', MT305_SequenceB_ReportingInformation_35B_Type)


# Complex type {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_17H_Type with content type SIMPLE
class MT305_SequenceB_ReportingInformation_17H_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_17H_Type with content type SIMPLE"""
    _TypeDefinition = MT305_SequenceB_ReportingInformation_17H_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceB_ReportingInformation_17H_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 801, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT305_SequenceB_ReportingInformation_17H_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_17H_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='17H')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 804, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 804, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_17H_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 805, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 805, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT305_SequenceB_ReportingInformation_17H_Type = MT305_SequenceB_ReportingInformation_17H_Type
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceB_ReportingInformation_17H_Type', MT305_SequenceB_ReportingInformation_17H_Type)


# Complex type {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_17P_Type with content type SIMPLE
class MT305_SequenceB_ReportingInformation_17P_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_17P_Type with content type SIMPLE"""
    _TypeDefinition = MT305_SequenceB_ReportingInformation_17P_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceB_ReportingInformation_17P_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 814, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT305_SequenceB_ReportingInformation_17P_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_17P_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='17P')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 817, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 817, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_17P_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 818, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 818, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT305_SequenceB_ReportingInformation_17P_Type = MT305_SequenceB_ReportingInformation_17P_Type
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceB_ReportingInformation_17P_Type', MT305_SequenceB_ReportingInformation_17P_Type)


# Complex type {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_22V_Type with content type SIMPLE
class MT305_SequenceB_ReportingInformation_22V_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_22V_Type with content type SIMPLE"""
    _TypeDefinition = MT305_SequenceB_ReportingInformation_22V_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceB_ReportingInformation_22V_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 827, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT305_SequenceB_ReportingInformation_22V_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_22V_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='22V')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 830, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 830, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_22V_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 831, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 831, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT305_SequenceB_ReportingInformation_22V_Type = MT305_SequenceB_ReportingInformation_22V_Type
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceB_ReportingInformation_22V_Type', MT305_SequenceB_ReportingInformation_22V_Type)


# Complex type {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_98D_Type with content type SIMPLE
class MT305_SequenceB_ReportingInformation_98D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_98D_Type with content type SIMPLE"""
    _TypeDefinition = MT305_SequenceB_ReportingInformation_98D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceB_ReportingInformation_98D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 840, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT305_SequenceB_ReportingInformation_98D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_98D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='98D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 843, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 843, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_98D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 844, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 844, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT305_SequenceB_ReportingInformation_98D_Type = MT305_SequenceB_ReportingInformation_98D_Type
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceB_ReportingInformation_98D_Type', MT305_SequenceB_ReportingInformation_98D_Type)


# Complex type {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_17W_Type with content type SIMPLE
class MT305_SequenceB_ReportingInformation_17W_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_17W_Type with content type SIMPLE"""
    _TypeDefinition = MT305_SequenceB_ReportingInformation_17W_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceB_ReportingInformation_17W_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 853, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT305_SequenceB_ReportingInformation_17W_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_17W_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='17W')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 856, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 856, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_17W_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 857, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 857, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT305_SequenceB_ReportingInformation_17W_Type = MT305_SequenceB_ReportingInformation_17W_Type
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceB_ReportingInformation_17W_Type', MT305_SequenceB_ReportingInformation_17W_Type)


# Complex type {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_17Y_Type with content type SIMPLE
class MT305_SequenceB_ReportingInformation_17Y_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_17Y_Type with content type SIMPLE"""
    _TypeDefinition = MT305_SequenceB_ReportingInformation_17Y_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceB_ReportingInformation_17Y_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 866, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT305_SequenceB_ReportingInformation_17Y_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_17Y_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='17Y')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 869, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 869, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_17Y_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 870, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 870, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT305_SequenceB_ReportingInformation_17Y_Type = MT305_SequenceB_ReportingInformation_17Y_Type
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceB_ReportingInformation_17Y_Type', MT305_SequenceB_ReportingInformation_17Y_Type)


# Complex type {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_17Z_Type with content type SIMPLE
class MT305_SequenceB_ReportingInformation_17Z_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_17Z_Type with content type SIMPLE"""
    _TypeDefinition = MT305_SequenceB_ReportingInformation_17Z_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceB_ReportingInformation_17Z_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 879, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT305_SequenceB_ReportingInformation_17Z_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_17Z_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='17Z')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 882, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 882, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_17Z_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 883, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 883, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT305_SequenceB_ReportingInformation_17Z_Type = MT305_SequenceB_ReportingInformation_17Z_Type
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceB_ReportingInformation_17Z_Type', MT305_SequenceB_ReportingInformation_17Z_Type)


# Complex type {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_22Q_Type with content type SIMPLE
class MT305_SequenceB_ReportingInformation_22Q_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_22Q_Type with content type SIMPLE"""
    _TypeDefinition = MT305_SequenceB_ReportingInformation_22Q_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceB_ReportingInformation_22Q_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 892, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT305_SequenceB_ReportingInformation_22Q_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_22Q_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='22Q')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 895, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 895, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_22Q_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 896, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 896, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT305_SequenceB_ReportingInformation_22Q_Type = MT305_SequenceB_ReportingInformation_22Q_Type
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceB_ReportingInformation_22Q_Type', MT305_SequenceB_ReportingInformation_22Q_Type)


# Complex type {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_17L_Type with content type SIMPLE
class MT305_SequenceB_ReportingInformation_17L_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_17L_Type with content type SIMPLE"""
    _TypeDefinition = MT305_SequenceB_ReportingInformation_17L_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceB_ReportingInformation_17L_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 905, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT305_SequenceB_ReportingInformation_17L_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_17L_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='17L')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 908, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 908, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_17L_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 909, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 909, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT305_SequenceB_ReportingInformation_17L_Type = MT305_SequenceB_ReportingInformation_17L_Type
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceB_ReportingInformation_17L_Type', MT305_SequenceB_ReportingInformation_17L_Type)


# Complex type {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_17M_Type with content type SIMPLE
class MT305_SequenceB_ReportingInformation_17M_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_17M_Type with content type SIMPLE"""
    _TypeDefinition = MT305_SequenceB_ReportingInformation_17M_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceB_ReportingInformation_17M_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 918, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT305_SequenceB_ReportingInformation_17M_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_17M_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='17M')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 921, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 921, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_17M_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 922, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 922, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT305_SequenceB_ReportingInformation_17M_Type = MT305_SequenceB_ReportingInformation_17M_Type
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceB_ReportingInformation_17M_Type', MT305_SequenceB_ReportingInformation_17M_Type)


# Complex type {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_17Q_Type with content type SIMPLE
class MT305_SequenceB_ReportingInformation_17Q_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_17Q_Type with content type SIMPLE"""
    _TypeDefinition = MT305_SequenceB_ReportingInformation_17Q_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceB_ReportingInformation_17Q_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 931, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT305_SequenceB_ReportingInformation_17Q_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_17Q_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='17Q')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 934, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 934, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_17Q_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 935, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 935, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT305_SequenceB_ReportingInformation_17Q_Type = MT305_SequenceB_ReportingInformation_17Q_Type
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceB_ReportingInformation_17Q_Type', MT305_SequenceB_ReportingInformation_17Q_Type)


# Complex type {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_17S_Type with content type SIMPLE
class MT305_SequenceB_ReportingInformation_17S_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_17S_Type with content type SIMPLE"""
    _TypeDefinition = MT305_SequenceB_ReportingInformation_17S_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceB_ReportingInformation_17S_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 944, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT305_SequenceB_ReportingInformation_17S_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_17S_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='17S')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 947, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 947, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_17S_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 948, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 948, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT305_SequenceB_ReportingInformation_17S_Type = MT305_SequenceB_ReportingInformation_17S_Type
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceB_ReportingInformation_17S_Type', MT305_SequenceB_ReportingInformation_17S_Type)


# Complex type {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_17X_Type with content type SIMPLE
class MT305_SequenceB_ReportingInformation_17X_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_17X_Type with content type SIMPLE"""
    _TypeDefinition = MT305_SequenceB_ReportingInformation_17X_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceB_ReportingInformation_17X_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 957, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT305_SequenceB_ReportingInformation_17X_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_17X_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='17X')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 960, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 960, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_17X_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 961, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 961, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT305_SequenceB_ReportingInformation_17X_Type = MT305_SequenceB_ReportingInformation_17X_Type
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceB_ReportingInformation_17X_Type', MT305_SequenceB_ReportingInformation_17X_Type)


# Complex type {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_34C_Type with content type SIMPLE
class MT305_SequenceB_ReportingInformation_34C_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_34C_Type with content type SIMPLE"""
    _TypeDefinition = MT305_SequenceB_ReportingInformation_34C_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceB_ReportingInformation_34C_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 970, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT305_SequenceB_ReportingInformation_34C_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_34C_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='34C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 973, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 973, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_34C_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 974, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 974, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT305_SequenceB_ReportingInformation_34C_Type = MT305_SequenceB_ReportingInformation_34C_Type
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceB_ReportingInformation_34C_Type', MT305_SequenceB_ReportingInformation_34C_Type)


# Complex type {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_77A_Type with content type SIMPLE
class MT305_SequenceB_ReportingInformation_77A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT305_SequenceB_ReportingInformation_77A_Type with content type SIMPLE"""
    _TypeDefinition = MT305_SequenceB_ReportingInformation_77A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT305_SequenceB_ReportingInformation_77A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 983, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT305_SequenceB_ReportingInformation_77A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_77A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='77A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 986, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 986, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT305_SequenceB_ReportingInformation_77A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 987, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 987, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT305_SequenceB_ReportingInformation_77A_Type = MT305_SequenceB_ReportingInformation_77A_Type
Namespace.addCategoryObject('typeBinding', 'MT305_SequenceB_ReportingInformation_77A_Type', MT305_SequenceB_ReportingInformation_77A_Type)


MT305 = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'MT305'), CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1124, 1))
Namespace.addCategoryObject('elementBinding', MT305.name().localName(), MT305)



MT305_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TransactionReferenceNumber'), MT305_SequenceA_GeneralInformation_20_Type, scope=MT305_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 999, 3)))

MT305_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'RelatedReference'), MT305_SequenceA_GeneralInformation_21_Type, scope=MT305_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1000, 3)))

MT305_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CodeCommonReference'), MT305_SequenceA_GeneralInformation_22_Type, scope=MT305_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1001, 3)))

MT305_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'FurtherIdentification'), MT305_SequenceA_GeneralInformation_23_Type, scope=MT305_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1002, 3)))

MT305_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ScopeOfOperation'), MT305_SequenceA_GeneralInformation_94A_Type, scope=MT305_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1003, 3)))

MT305_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PartyA_A'), MT305_SequenceA_GeneralInformation_82A_Type, scope=MT305_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1005, 4)))

MT305_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PartyA_D'), MT305_SequenceA_GeneralInformation_82D_Type, scope=MT305_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1006, 4)))

MT305_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PartyA_J'), MT305_SequenceA_GeneralInformation_82J_Type, scope=MT305_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1007, 4)))

MT305_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PartyB_A'), MT305_SequenceA_GeneralInformation_87A_Type, scope=MT305_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1010, 4)))

MT305_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PartyB_D'), MT305_SequenceA_GeneralInformation_87D_Type, scope=MT305_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1011, 4)))

MT305_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PartyB_J'), MT305_SequenceA_GeneralInformation_87J_Type, scope=MT305_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1012, 4)))

MT305_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'FundOrBeneficiaryCustomer_A'), MT305_SequenceA_GeneralInformation_83A_Type, scope=MT305_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1015, 4)))

MT305_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'FundOrBeneficiaryCustomer_D'), MT305_SequenceA_GeneralInformation_83D_Type, scope=MT305_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1016, 4)))

MT305_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'FundOrBeneficiaryCustomer_J'), MT305_SequenceA_GeneralInformation_83J_Type, scope=MT305_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1017, 4)))

MT305_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DateContractAgreedAmended'), MT305_SequenceA_GeneralInformation_30_Type, scope=MT305_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1019, 3)))

MT305_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'EarliestExerciseDate'), MT305_SequenceA_GeneralInformation_31C_Type, scope=MT305_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1020, 3)))

MT305_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ExpiryDetails'), MT305_SequenceA_GeneralInformation_31G_Type, scope=MT305_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1021, 3)))

MT305_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'FinalSettlementDate'), MT305_SequenceA_GeneralInformation_31E_Type, scope=MT305_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1022, 3)))

MT305_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SettlementType'), MT305_SequenceA_GeneralInformation_26F_Type, scope=MT305_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1023, 3)))

MT305_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PaymentClearingCentre'), MT305_SequenceA_GeneralInformation_39M_Type, scope=MT305_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1024, 3)))

MT305_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'NonDeliverableIndicator'), MT305_SequenceA_GeneralInformation_17F_Type, scope=MT305_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1025, 3)))

MT305_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SettlementRateSource'), MT305_SequenceA_GeneralInformation_14S_Type, scope=MT305_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1026, 3)))

MT305_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SettlementCurrency'), MT305_SequenceA_GeneralInformation_32E_Type, scope=MT305_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1027, 3)))

MT305_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'UnderlyingCurrencyNAmount'), MT305_SequenceA_GeneralInformation_32B_Type, scope=MT305_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1028, 3)))

MT305_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'StrikePrice'), MT305_SequenceA_GeneralInformation_36_Type, scope=MT305_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1029, 3)))

MT305_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CounterCurrencyNAmount'), MT305_SequenceA_GeneralInformation_33B_Type, scope=MT305_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1030, 3)))

MT305_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PremiumPrice'), MT305_SequenceA_GeneralInformation_37K_Type, scope=MT305_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1031, 3)))

MT305_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PremiumPayment_P'), MT305_SequenceA_GeneralInformation_34P_Type, scope=MT305_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1033, 4)))

MT305_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PremiumPayment_R'), MT305_SequenceA_GeneralInformation_34R_Type, scope=MT305_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1034, 4)))

MT305_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SendersCorrespondent_A'), MT305_SequenceA_GeneralInformation_53A_Type, scope=MT305_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1037, 4)))

MT305_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SendersCorrespondent_B'), MT305_SequenceA_GeneralInformation_53D_Type, scope=MT305_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1038, 4)))

MT305_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SendersCorrespondent_D'), MT305_SequenceA_GeneralInformation_53J_Type, scope=MT305_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1039, 4)))

MT305_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_A'), MT305_SequenceA_GeneralInformation_56A_Type, scope=MT305_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1042, 4)))

MT305_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_D'), MT305_SequenceA_GeneralInformation_56D_Type, scope=MT305_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1043, 4)))

MT305_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'AccountWithInstitution_A'), MT305_SequenceA_GeneralInformation_57A_Type, scope=MT305_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1046, 4)))

MT305_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'AccountWithInstitution_D'), MT305_SequenceA_GeneralInformation_57D_Type, scope=MT305_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1047, 4)))

MT305_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TypeDateVersionOfAgreement'), MT305_SequenceA_GeneralInformation_77H_Type, scope=MT305_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1049, 3)))

MT305_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'YearOfDefinitions'), MT305_SequenceA_GeneralInformation_14C_Type, scope=MT305_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1050, 3)))

MT305_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SenderToReceiverInformation'), MT305_SequenceA_GeneralInformation_72_Type, scope=MT305_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1051, 3)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1003, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1014, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1015, 4))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1016, 4))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1017, 4))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1020, 3))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1024, 3))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1025, 3))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1026, 3))
    counters.add(cc_8)
    cc_9 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1027, 3))
    counters.add(cc_9)
    cc_10 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1036, 3))
    counters.add(cc_10)
    cc_11 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1037, 4))
    counters.add(cc_11)
    cc_12 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1038, 4))
    counters.add(cc_12)
    cc_13 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1039, 4))
    counters.add(cc_13)
    cc_14 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1041, 3))
    counters.add(cc_14)
    cc_15 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1042, 4))
    counters.add(cc_15)
    cc_16 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1043, 4))
    counters.add(cc_16)
    cc_17 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1049, 3))
    counters.add(cc_17)
    cc_18 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1050, 3))
    counters.add(cc_18)
    cc_19 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1051, 3))
    counters.add(cc_19)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT305_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'TransactionReferenceNumber')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 999, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT305_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'RelatedReference')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1000, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT305_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CodeCommonReference')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1001, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT305_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'FurtherIdentification')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1002, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT305_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ScopeOfOperation')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1003, 3))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT305_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PartyA_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1005, 4))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT305_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PartyA_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1006, 4))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT305_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PartyA_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1007, 4))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT305_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PartyB_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1010, 4))
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT305_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PartyB_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1011, 4))
    st_9 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT305_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PartyB_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1012, 4))
    st_10 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT305_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'FundOrBeneficiaryCustomer_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1015, 4))
    st_11 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT305_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'FundOrBeneficiaryCustomer_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1016, 4))
    st_12 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_12)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT305_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'FundOrBeneficiaryCustomer_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1017, 4))
    st_13 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_13)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT305_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DateContractAgreedAmended')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1019, 3))
    st_14 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_14)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT305_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'EarliestExerciseDate')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1020, 3))
    st_15 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_15)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT305_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ExpiryDetails')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1021, 3))
    st_16 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_16)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT305_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'FinalSettlementDate')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1022, 3))
    st_17 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_17)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT305_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SettlementType')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1023, 3))
    st_18 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_18)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT305_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PaymentClearingCentre')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1024, 3))
    st_19 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_19)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT305_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'NonDeliverableIndicator')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1025, 3))
    st_20 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_20)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT305_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SettlementRateSource')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1026, 3))
    st_21 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_21)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT305_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SettlementCurrency')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1027, 3))
    st_22 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_22)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT305_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'UnderlyingCurrencyNAmount')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1028, 3))
    st_23 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_23)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT305_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'StrikePrice')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1029, 3))
    st_24 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_24)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT305_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CounterCurrencyNAmount')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1030, 3))
    st_25 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_25)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT305_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PremiumPrice')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1031, 3))
    st_26 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_26)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT305_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PremiumPayment_P')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1033, 4))
    st_27 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_27)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT305_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PremiumPayment_R')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1034, 4))
    st_28 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_28)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT305_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SendersCorrespondent_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1037, 4))
    st_29 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_29)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT305_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SendersCorrespondent_B')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1038, 4))
    st_30 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_30)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT305_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SendersCorrespondent_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1039, 4))
    st_31 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_31)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT305_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1042, 4))
    st_32 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_32)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT305_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1043, 4))
    st_33 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_33)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT305_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'AccountWithInstitution_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1046, 4))
    st_34 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_34)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT305_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'AccountWithInstitution_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1047, 4))
    st_35 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_35)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_17, False))
    symbol = pyxb.binding.content.ElementUse(MT305_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'TypeDateVersionOfAgreement')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1049, 3))
    st_36 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_36)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_18, False))
    symbol = pyxb.binding.content.ElementUse(MT305_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'YearOfDefinitions')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1050, 3))
    st_37 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_37)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_19, False))
    symbol = pyxb.binding.content.ElementUse(MT305_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SenderToReceiverInformation')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1051, 3))
    st_38 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_38)
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
    transitions.append(fac.Transition(st_5, [
         ]))
    transitions.append(fac.Transition(st_6, [
         ]))
    transitions.append(fac.Transition(st_7, [
         ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
         ]))
    transitions.append(fac.Transition(st_9, [
         ]))
    transitions.append(fac.Transition(st_10, [
         ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
         ]))
    transitions.append(fac.Transition(st_9, [
         ]))
    transitions.append(fac.Transition(st_10, [
         ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
         ]))
    transitions.append(fac.Transition(st_9, [
         ]))
    transitions.append(fac.Transition(st_10, [
         ]))
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
    st_10._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_1, True),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_1, True),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_1, True),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_2, False) ]))
    st_11._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_1, True),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_1, True),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_1, True),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_3, False) ]))
    st_12._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_1, True),
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_1, True),
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_1, True),
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_4, False) ]))
    st_13._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_15, [
         ]))
    transitions.append(fac.Transition(st_16, [
         ]))
    st_14._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_5, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_5, False) ]))
    st_15._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_17, [
         ]))
    st_16._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_18, [
         ]))
    st_17._set_transitionSet(transitions)
    transitions = []
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
    st_18._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_6, True) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_6, False) ]))
    st_19._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_7, True) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_7, False) ]))
    st_20._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_8, True) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_8, False) ]))
    st_21._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_9, True) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_9, False) ]))
    st_22._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_24, [
         ]))
    st_23._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_25, [
         ]))
    st_24._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_26, [
         ]))
    st_25._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_27, [
         ]))
    transitions.append(fac.Transition(st_28, [
         ]))
    st_26._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_29, [
         ]))
    transitions.append(fac.Transition(st_30, [
         ]))
    transitions.append(fac.Transition(st_31, [
         ]))
    transitions.append(fac.Transition(st_32, [
         ]))
    transitions.append(fac.Transition(st_33, [
         ]))
    transitions.append(fac.Transition(st_34, [
         ]))
    transitions.append(fac.Transition(st_35, [
         ]))
    st_27._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_29, [
         ]))
    transitions.append(fac.Transition(st_30, [
         ]))
    transitions.append(fac.Transition(st_31, [
         ]))
    transitions.append(fac.Transition(st_32, [
         ]))
    transitions.append(fac.Transition(st_33, [
         ]))
    transitions.append(fac.Transition(st_34, [
         ]))
    transitions.append(fac.Transition(st_35, [
         ]))
    st_28._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_29, [
        fac.UpdateInstruction(cc_10, True),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_29, [
        fac.UpdateInstruction(cc_11, True) ]))
    transitions.append(fac.Transition(st_30, [
        fac.UpdateInstruction(cc_10, True),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_31, [
        fac.UpdateInstruction(cc_10, True),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_32, [
        fac.UpdateInstruction(cc_10, False),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_33, [
        fac.UpdateInstruction(cc_10, False),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_34, [
        fac.UpdateInstruction(cc_10, False),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_35, [
        fac.UpdateInstruction(cc_10, False),
        fac.UpdateInstruction(cc_11, False) ]))
    st_29._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_29, [
        fac.UpdateInstruction(cc_10, True),
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_30, [
        fac.UpdateInstruction(cc_10, True),
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_30, [
        fac.UpdateInstruction(cc_12, True) ]))
    transitions.append(fac.Transition(st_31, [
        fac.UpdateInstruction(cc_10, True),
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_32, [
        fac.UpdateInstruction(cc_10, False),
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_33, [
        fac.UpdateInstruction(cc_10, False),
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_34, [
        fac.UpdateInstruction(cc_10, False),
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_35, [
        fac.UpdateInstruction(cc_10, False),
        fac.UpdateInstruction(cc_12, False) ]))
    st_30._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_29, [
        fac.UpdateInstruction(cc_10, True),
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_30, [
        fac.UpdateInstruction(cc_10, True),
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_31, [
        fac.UpdateInstruction(cc_10, True),
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_31, [
        fac.UpdateInstruction(cc_13, True) ]))
    transitions.append(fac.Transition(st_32, [
        fac.UpdateInstruction(cc_10, False),
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_33, [
        fac.UpdateInstruction(cc_10, False),
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_34, [
        fac.UpdateInstruction(cc_10, False),
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_35, [
        fac.UpdateInstruction(cc_10, False),
        fac.UpdateInstruction(cc_13, False) ]))
    st_31._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_32, [
        fac.UpdateInstruction(cc_14, True),
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_32, [
        fac.UpdateInstruction(cc_15, True) ]))
    transitions.append(fac.Transition(st_33, [
        fac.UpdateInstruction(cc_14, True),
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_34, [
        fac.UpdateInstruction(cc_14, False),
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_35, [
        fac.UpdateInstruction(cc_14, False),
        fac.UpdateInstruction(cc_15, False) ]))
    st_32._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_32, [
        fac.UpdateInstruction(cc_14, True),
        fac.UpdateInstruction(cc_16, False) ]))
    transitions.append(fac.Transition(st_33, [
        fac.UpdateInstruction(cc_14, True),
        fac.UpdateInstruction(cc_16, False) ]))
    transitions.append(fac.Transition(st_33, [
        fac.UpdateInstruction(cc_16, True) ]))
    transitions.append(fac.Transition(st_34, [
        fac.UpdateInstruction(cc_14, False),
        fac.UpdateInstruction(cc_16, False) ]))
    transitions.append(fac.Transition(st_35, [
        fac.UpdateInstruction(cc_14, False),
        fac.UpdateInstruction(cc_16, False) ]))
    st_33._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_36, [
         ]))
    transitions.append(fac.Transition(st_37, [
         ]))
    transitions.append(fac.Transition(st_38, [
         ]))
    st_34._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_36, [
         ]))
    transitions.append(fac.Transition(st_37, [
         ]))
    transitions.append(fac.Transition(st_38, [
         ]))
    st_35._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_36, [
        fac.UpdateInstruction(cc_17, True) ]))
    transitions.append(fac.Transition(st_37, [
        fac.UpdateInstruction(cc_17, False) ]))
    transitions.append(fac.Transition(st_38, [
        fac.UpdateInstruction(cc_17, False) ]))
    st_36._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_37, [
        fac.UpdateInstruction(cc_18, True) ]))
    transitions.append(fac.Transition(st_38, [
        fac.UpdateInstruction(cc_18, False) ]))
    st_37._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_38, [
        fac.UpdateInstruction(cc_19, True) ]))
    st_38._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
MT305_SequenceA_GeneralInformation._Automaton = _BuildAutomaton()




MT305_SequenceB_ReportingInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SubsequenceB1_ReportingParties'), MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties, scope=MT305_SequenceB_ReportingInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1059, 3)))

MT305_SequenceB_ReportingInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CentralCounterpartyClearingHouse_A'), MT305_SequenceB_ReportingInformation_81A_Type, scope=MT305_SequenceB_ReportingInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1061, 4)))

MT305_SequenceB_ReportingInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CentralCounterpartyClearingHouse_D'), MT305_SequenceB_ReportingInformation_81D_Type, scope=MT305_SequenceB_ReportingInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1062, 4)))

MT305_SequenceB_ReportingInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CentralCounterpartyClearingHouse_J'), MT305_SequenceB_ReportingInformation_81J_Type, scope=MT305_SequenceB_ReportingInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1063, 4)))

MT305_SequenceB_ReportingInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ClearingBroker_A'), MT305_SequenceB_ReportingInformation_89A_Type, scope=MT305_SequenceB_ReportingInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1066, 4)))

MT305_SequenceB_ReportingInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ClearingBroker_D'), MT305_SequenceB_ReportingInformation_89D_Type, scope=MT305_SequenceB_ReportingInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1067, 4)))

MT305_SequenceB_ReportingInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ClearingBroker_J'), MT305_SequenceB_ReportingInformation_89J_Type, scope=MT305_SequenceB_ReportingInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1068, 4)))

MT305_SequenceB_ReportingInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ClearingExceptionParty_A'), MT305_SequenceB_ReportingInformation_96A_Type, scope=MT305_SequenceB_ReportingInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1071, 4)))

MT305_SequenceB_ReportingInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ClearingExceptionParty_D'), MT305_SequenceB_ReportingInformation_96D_Type, scope=MT305_SequenceB_ReportingInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1072, 4)))

MT305_SequenceB_ReportingInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ClearingExceptionParty_J'), MT305_SequenceB_ReportingInformation_96J_Type, scope=MT305_SequenceB_ReportingInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1073, 4)))

MT305_SequenceB_ReportingInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ClearingBrokerIdentification'), MT305_SequenceB_ReportingInformation_22S_Type, scope=MT305_SequenceB_ReportingInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1075, 3)))

MT305_SequenceB_ReportingInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ClearedProductIdentification'), MT305_SequenceB_ReportingInformation_22T_Type, scope=MT305_SequenceB_ReportingInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1076, 3)))

MT305_SequenceB_ReportingInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ClearingThresholdIndicator'), MT305_SequenceB_ReportingInformation_17E_Type, scope=MT305_SequenceB_ReportingInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1077, 3)))

MT305_SequenceB_ReportingInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'UnderlyingProductIdentifier'), MT305_SequenceB_ReportingInformation_22U_Type, scope=MT305_SequenceB_ReportingInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1078, 3)))

MT305_SequenceB_ReportingInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'IdentificationOfFinancialInstrument'), MT305_SequenceB_ReportingInformation_35B_Type, scope=MT305_SequenceB_ReportingInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1079, 3)))

MT305_SequenceB_ReportingInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'AllocationIndicator'), MT305_SequenceB_ReportingInformation_17H_Type, scope=MT305_SequenceB_ReportingInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1080, 3)))

MT305_SequenceB_ReportingInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CollateralisationIndicator'), MT305_SequenceB_ReportingInformation_17P_Type, scope=MT305_SequenceB_ReportingInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1081, 3)))

MT305_SequenceB_ReportingInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ExecutionVenue'), MT305_SequenceB_ReportingInformation_22V_Type, scope=MT305_SequenceB_ReportingInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1082, 3)))

MT305_SequenceB_ReportingInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ExecutionTimestamp'), MT305_SequenceB_ReportingInformation_98D_Type, scope=MT305_SequenceB_ReportingInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1083, 3)))

MT305_SequenceB_ReportingInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'NonStandardFlag'), MT305_SequenceB_ReportingInformation_17W_Type, scope=MT305_SequenceB_ReportingInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1084, 3)))

MT305_SequenceB_ReportingInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'FinancialNatureOfCounterpartyIndicator'), MT305_SequenceB_ReportingInformation_17Y_Type, scope=MT305_SequenceB_ReportingInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1085, 3)))

MT305_SequenceB_ReportingInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CollateralPortfolioIndicator'), MT305_SequenceB_ReportingInformation_17Z_Type, scope=MT305_SequenceB_ReportingInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1086, 3)))

MT305_SequenceB_ReportingInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CollateralPortfolioCode'), MT305_SequenceB_ReportingInformation_22Q_Type, scope=MT305_SequenceB_ReportingInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1087, 3)))

MT305_SequenceB_ReportingInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PortfolioCompressionIndicator'), MT305_SequenceB_ReportingInformation_17L_Type, scope=MT305_SequenceB_ReportingInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1088, 3)))

MT305_SequenceB_ReportingInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CorporateSectorIndicator'), MT305_SequenceB_ReportingInformation_17M_Type, scope=MT305_SequenceB_ReportingInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1089, 3)))

MT305_SequenceB_ReportingInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TradeWithNonEEACounterpartyIndicator'), MT305_SequenceB_ReportingInformation_17Q_Type, scope=MT305_SequenceB_ReportingInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1090, 3)))

MT305_SequenceB_ReportingInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'IntragroupTradeIndicator'), MT305_SequenceB_ReportingInformation_17S_Type, scope=MT305_SequenceB_ReportingInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1091, 3)))

MT305_SequenceB_ReportingInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CommercialOrTreasuryFinancingIndicator'), MT305_SequenceB_ReportingInformation_17X_Type, scope=MT305_SequenceB_ReportingInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1092, 3)))

MT305_SequenceB_ReportingInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CommissionAndFees'), MT305_SequenceB_ReportingInformation_34C_Type, scope=MT305_SequenceB_ReportingInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1093, 3)))

MT305_SequenceB_ReportingInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'AdditionalReportingInformation'), MT305_SequenceB_ReportingInformation_77A_Type, scope=MT305_SequenceB_ReportingInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1094, 3)))

def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1059, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1060, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1061, 4))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1062, 4))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1063, 4))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1065, 3))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1066, 4))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1067, 4))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1068, 4))
    counters.add(cc_8)
    cc_9 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1070, 3))
    counters.add(cc_9)
    cc_10 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1071, 4))
    counters.add(cc_10)
    cc_11 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1072, 4))
    counters.add(cc_11)
    cc_12 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1073, 4))
    counters.add(cc_12)
    cc_13 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1075, 3))
    counters.add(cc_13)
    cc_14 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1076, 3))
    counters.add(cc_14)
    cc_15 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1077, 3))
    counters.add(cc_15)
    cc_16 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1078, 3))
    counters.add(cc_16)
    cc_17 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1079, 3))
    counters.add(cc_17)
    cc_18 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1080, 3))
    counters.add(cc_18)
    cc_19 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1081, 3))
    counters.add(cc_19)
    cc_20 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1082, 3))
    counters.add(cc_20)
    cc_21 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1083, 3))
    counters.add(cc_21)
    cc_22 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1084, 3))
    counters.add(cc_22)
    cc_23 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1085, 3))
    counters.add(cc_23)
    cc_24 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1086, 3))
    counters.add(cc_24)
    cc_25 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1087, 3))
    counters.add(cc_25)
    cc_26 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1088, 3))
    counters.add(cc_26)
    cc_27 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1089, 3))
    counters.add(cc_27)
    cc_28 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1090, 3))
    counters.add(cc_28)
    cc_29 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1091, 3))
    counters.add(cc_29)
    cc_30 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1092, 3))
    counters.add(cc_30)
    cc_31 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1093, 3))
    counters.add(cc_31)
    cc_32 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1094, 3))
    counters.add(cc_32)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(MT305_SequenceB_ReportingInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SubsequenceB1_ReportingParties')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1059, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(MT305_SequenceB_ReportingInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CentralCounterpartyClearingHouse_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1061, 4))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(MT305_SequenceB_ReportingInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CentralCounterpartyClearingHouse_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1062, 4))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(MT305_SequenceB_ReportingInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CentralCounterpartyClearingHouse_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1063, 4))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_5, False))
    final_update.add(fac.UpdateInstruction(cc_6, False))
    symbol = pyxb.binding.content.ElementUse(MT305_SequenceB_ReportingInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ClearingBroker_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1066, 4))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_5, False))
    final_update.add(fac.UpdateInstruction(cc_7, False))
    symbol = pyxb.binding.content.ElementUse(MT305_SequenceB_ReportingInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ClearingBroker_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1067, 4))
    st_5 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_5, False))
    final_update.add(fac.UpdateInstruction(cc_8, False))
    symbol = pyxb.binding.content.ElementUse(MT305_SequenceB_ReportingInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ClearingBroker_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1068, 4))
    st_6 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_9, False))
    final_update.add(fac.UpdateInstruction(cc_10, False))
    symbol = pyxb.binding.content.ElementUse(MT305_SequenceB_ReportingInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ClearingExceptionParty_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1071, 4))
    st_7 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_9, False))
    final_update.add(fac.UpdateInstruction(cc_11, False))
    symbol = pyxb.binding.content.ElementUse(MT305_SequenceB_ReportingInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ClearingExceptionParty_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1072, 4))
    st_8 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_9, False))
    final_update.add(fac.UpdateInstruction(cc_12, False))
    symbol = pyxb.binding.content.ElementUse(MT305_SequenceB_ReportingInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ClearingExceptionParty_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1073, 4))
    st_9 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_13, False))
    symbol = pyxb.binding.content.ElementUse(MT305_SequenceB_ReportingInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ClearingBrokerIdentification')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1075, 3))
    st_10 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_14, False))
    symbol = pyxb.binding.content.ElementUse(MT305_SequenceB_ReportingInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ClearedProductIdentification')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1076, 3))
    st_11 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_15, False))
    symbol = pyxb.binding.content.ElementUse(MT305_SequenceB_ReportingInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ClearingThresholdIndicator')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1077, 3))
    st_12 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_12)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_16, False))
    symbol = pyxb.binding.content.ElementUse(MT305_SequenceB_ReportingInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'UnderlyingProductIdentifier')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1078, 3))
    st_13 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_13)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_17, False))
    symbol = pyxb.binding.content.ElementUse(MT305_SequenceB_ReportingInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'IdentificationOfFinancialInstrument')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1079, 3))
    st_14 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_14)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_18, False))
    symbol = pyxb.binding.content.ElementUse(MT305_SequenceB_ReportingInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'AllocationIndicator')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1080, 3))
    st_15 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_15)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_19, False))
    symbol = pyxb.binding.content.ElementUse(MT305_SequenceB_ReportingInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CollateralisationIndicator')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1081, 3))
    st_16 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_16)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_20, False))
    symbol = pyxb.binding.content.ElementUse(MT305_SequenceB_ReportingInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ExecutionVenue')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1082, 3))
    st_17 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_17)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_21, False))
    symbol = pyxb.binding.content.ElementUse(MT305_SequenceB_ReportingInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ExecutionTimestamp')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1083, 3))
    st_18 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_18)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_22, False))
    symbol = pyxb.binding.content.ElementUse(MT305_SequenceB_ReportingInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'NonStandardFlag')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1084, 3))
    st_19 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_19)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_23, False))
    symbol = pyxb.binding.content.ElementUse(MT305_SequenceB_ReportingInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'FinancialNatureOfCounterpartyIndicator')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1085, 3))
    st_20 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_20)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_24, False))
    symbol = pyxb.binding.content.ElementUse(MT305_SequenceB_ReportingInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CollateralPortfolioIndicator')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1086, 3))
    st_21 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_21)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_25, False))
    symbol = pyxb.binding.content.ElementUse(MT305_SequenceB_ReportingInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CollateralPortfolioCode')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1087, 3))
    st_22 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_22)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_26, False))
    symbol = pyxb.binding.content.ElementUse(MT305_SequenceB_ReportingInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PortfolioCompressionIndicator')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1088, 3))
    st_23 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_23)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_27, False))
    symbol = pyxb.binding.content.ElementUse(MT305_SequenceB_ReportingInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CorporateSectorIndicator')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1089, 3))
    st_24 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_24)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_28, False))
    symbol = pyxb.binding.content.ElementUse(MT305_SequenceB_ReportingInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'TradeWithNonEEACounterpartyIndicator')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1090, 3))
    st_25 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_25)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_29, False))
    symbol = pyxb.binding.content.ElementUse(MT305_SequenceB_ReportingInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'IntragroupTradeIndicator')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1091, 3))
    st_26 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_26)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_30, False))
    symbol = pyxb.binding.content.ElementUse(MT305_SequenceB_ReportingInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CommercialOrTreasuryFinancingIndicator')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1092, 3))
    st_27 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_27)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_31, False))
    symbol = pyxb.binding.content.ElementUse(MT305_SequenceB_ReportingInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CommissionAndFees')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1093, 3))
    st_28 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_28)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_32, False))
    symbol = pyxb.binding.content.ElementUse(MT305_SequenceB_ReportingInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'AdditionalReportingInformation')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1094, 3))
    st_29 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_29)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_27, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_28, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_29, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, True),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, True),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, False),
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
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_27, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_28, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_29, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_2, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, True),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, True),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_3, False) ]))
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
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_27, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_28, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_29, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_3, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True),
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, True),
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, True),
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_27, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_28, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_29, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_4, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_5, True),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_6, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_5, True),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_5, True),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_5, False),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_5, False),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_5, False),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_5, False),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_5, False),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_5, False),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_5, False),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_5, False),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_5, False),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_5, False),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_5, False),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_5, False),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_5, False),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_5, False),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_5, False),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_5, False),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_5, False),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_5, False),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_5, False),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_5, False),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_27, [
        fac.UpdateInstruction(cc_5, False),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_28, [
        fac.UpdateInstruction(cc_5, False),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_29, [
        fac.UpdateInstruction(cc_5, False),
        fac.UpdateInstruction(cc_6, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_5, True),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_5, True),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_7, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_5, True),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_5, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_5, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_5, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_5, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_5, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_5, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_5, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_5, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_5, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_5, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_5, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_5, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_5, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_5, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_5, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_5, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_5, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_5, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_5, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_5, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_27, [
        fac.UpdateInstruction(cc_5, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_28, [
        fac.UpdateInstruction(cc_5, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_29, [
        fac.UpdateInstruction(cc_5, False),
        fac.UpdateInstruction(cc_7, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_5, True),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_5, True),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_5, True),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_8, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_5, False),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_5, False),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_5, False),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_5, False),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_5, False),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_5, False),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_5, False),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_5, False),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_5, False),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_5, False),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_5, False),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_5, False),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_5, False),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_5, False),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_5, False),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_5, False),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_5, False),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_5, False),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_5, False),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_5, False),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_27, [
        fac.UpdateInstruction(cc_5, False),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_28, [
        fac.UpdateInstruction(cc_5, False),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_29, [
        fac.UpdateInstruction(cc_5, False),
        fac.UpdateInstruction(cc_8, False) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_9, True),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_10, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_9, True),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_9, True),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_9, False),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_9, False),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_9, False),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_9, False),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_9, False),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_9, False),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_9, False),
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
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_9, True),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_9, True),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_11, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_9, True),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_9, False),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_9, False),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_9, False),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_9, False),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_9, False),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_9, False),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_9, False),
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
    st_8._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_9, True),
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_9, True),
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_9, True),
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_12, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_9, False),
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_9, False),
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_9, False),
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_9, False),
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_9, False),
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_9, False),
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_9, False),
        fac.UpdateInstruction(cc_12, False) ]))
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
    st_9._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_13, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_27, [
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_28, [
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_29, [
        fac.UpdateInstruction(cc_13, False) ]))
    st_10._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_14, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_27, [
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_28, [
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_29, [
        fac.UpdateInstruction(cc_14, False) ]))
    st_11._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_15, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_27, [
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_28, [
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_29, [
        fac.UpdateInstruction(cc_15, False) ]))
    st_12._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_16, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_16, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_16, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_16, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_16, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_16, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_16, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_16, False) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_16, False) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_16, False) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_16, False) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_16, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_16, False) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_16, False) ]))
    transitions.append(fac.Transition(st_27, [
        fac.UpdateInstruction(cc_16, False) ]))
    transitions.append(fac.Transition(st_28, [
        fac.UpdateInstruction(cc_16, False) ]))
    transitions.append(fac.Transition(st_29, [
        fac.UpdateInstruction(cc_16, False) ]))
    st_13._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_17, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_17, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_17, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_17, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_17, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_17, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_17, False) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_17, False) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_17, False) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_17, False) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_17, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_17, False) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_17, False) ]))
    transitions.append(fac.Transition(st_27, [
        fac.UpdateInstruction(cc_17, False) ]))
    transitions.append(fac.Transition(st_28, [
        fac.UpdateInstruction(cc_17, False) ]))
    transitions.append(fac.Transition(st_29, [
        fac.UpdateInstruction(cc_17, False) ]))
    st_14._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_18, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_18, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_18, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_18, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_18, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_18, False) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_18, False) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_18, False) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_18, False) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_18, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_18, False) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_18, False) ]))
    transitions.append(fac.Transition(st_27, [
        fac.UpdateInstruction(cc_18, False) ]))
    transitions.append(fac.Transition(st_28, [
        fac.UpdateInstruction(cc_18, False) ]))
    transitions.append(fac.Transition(st_29, [
        fac.UpdateInstruction(cc_18, False) ]))
    st_15._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_19, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_19, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_19, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_19, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_19, False) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_19, False) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_19, False) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_19, False) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_19, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_19, False) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_19, False) ]))
    transitions.append(fac.Transition(st_27, [
        fac.UpdateInstruction(cc_19, False) ]))
    transitions.append(fac.Transition(st_28, [
        fac.UpdateInstruction(cc_19, False) ]))
    transitions.append(fac.Transition(st_29, [
        fac.UpdateInstruction(cc_19, False) ]))
    st_16._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_20, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_20, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_20, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_20, False) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_20, False) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_20, False) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_20, False) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_20, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_20, False) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_20, False) ]))
    transitions.append(fac.Transition(st_27, [
        fac.UpdateInstruction(cc_20, False) ]))
    transitions.append(fac.Transition(st_28, [
        fac.UpdateInstruction(cc_20, False) ]))
    transitions.append(fac.Transition(st_29, [
        fac.UpdateInstruction(cc_20, False) ]))
    st_17._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_21, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_21, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_21, False) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_21, False) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_21, False) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_21, False) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_21, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_21, False) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_21, False) ]))
    transitions.append(fac.Transition(st_27, [
        fac.UpdateInstruction(cc_21, False) ]))
    transitions.append(fac.Transition(st_28, [
        fac.UpdateInstruction(cc_21, False) ]))
    transitions.append(fac.Transition(st_29, [
        fac.UpdateInstruction(cc_21, False) ]))
    st_18._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_22, True) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_22, False) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_22, False) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_22, False) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_22, False) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_22, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_22, False) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_22, False) ]))
    transitions.append(fac.Transition(st_27, [
        fac.UpdateInstruction(cc_22, False) ]))
    transitions.append(fac.Transition(st_28, [
        fac.UpdateInstruction(cc_22, False) ]))
    transitions.append(fac.Transition(st_29, [
        fac.UpdateInstruction(cc_22, False) ]))
    st_19._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_23, True) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_23, False) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_23, False) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_23, False) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_23, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_23, False) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_23, False) ]))
    transitions.append(fac.Transition(st_27, [
        fac.UpdateInstruction(cc_23, False) ]))
    transitions.append(fac.Transition(st_28, [
        fac.UpdateInstruction(cc_23, False) ]))
    transitions.append(fac.Transition(st_29, [
        fac.UpdateInstruction(cc_23, False) ]))
    st_20._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_24, True) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_24, False) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_24, False) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_24, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_24, False) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_24, False) ]))
    transitions.append(fac.Transition(st_27, [
        fac.UpdateInstruction(cc_24, False) ]))
    transitions.append(fac.Transition(st_28, [
        fac.UpdateInstruction(cc_24, False) ]))
    transitions.append(fac.Transition(st_29, [
        fac.UpdateInstruction(cc_24, False) ]))
    st_21._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_25, True) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_25, False) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_25, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_25, False) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_25, False) ]))
    transitions.append(fac.Transition(st_27, [
        fac.UpdateInstruction(cc_25, False) ]))
    transitions.append(fac.Transition(st_28, [
        fac.UpdateInstruction(cc_25, False) ]))
    transitions.append(fac.Transition(st_29, [
        fac.UpdateInstruction(cc_25, False) ]))
    st_22._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_26, True) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_26, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_26, False) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_26, False) ]))
    transitions.append(fac.Transition(st_27, [
        fac.UpdateInstruction(cc_26, False) ]))
    transitions.append(fac.Transition(st_28, [
        fac.UpdateInstruction(cc_26, False) ]))
    transitions.append(fac.Transition(st_29, [
        fac.UpdateInstruction(cc_26, False) ]))
    st_23._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_27, True) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_27, False) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_27, False) ]))
    transitions.append(fac.Transition(st_27, [
        fac.UpdateInstruction(cc_27, False) ]))
    transitions.append(fac.Transition(st_28, [
        fac.UpdateInstruction(cc_27, False) ]))
    transitions.append(fac.Transition(st_29, [
        fac.UpdateInstruction(cc_27, False) ]))
    st_24._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_28, True) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_28, False) ]))
    transitions.append(fac.Transition(st_27, [
        fac.UpdateInstruction(cc_28, False) ]))
    transitions.append(fac.Transition(st_28, [
        fac.UpdateInstruction(cc_28, False) ]))
    transitions.append(fac.Transition(st_29, [
        fac.UpdateInstruction(cc_28, False) ]))
    st_25._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_29, True) ]))
    transitions.append(fac.Transition(st_27, [
        fac.UpdateInstruction(cc_29, False) ]))
    transitions.append(fac.Transition(st_28, [
        fac.UpdateInstruction(cc_29, False) ]))
    transitions.append(fac.Transition(st_29, [
        fac.UpdateInstruction(cc_29, False) ]))
    st_26._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_27, [
        fac.UpdateInstruction(cc_30, True) ]))
    transitions.append(fac.Transition(st_28, [
        fac.UpdateInstruction(cc_30, False) ]))
    transitions.append(fac.Transition(st_29, [
        fac.UpdateInstruction(cc_30, False) ]))
    st_27._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_28, [
        fac.UpdateInstruction(cc_31, True) ]))
    transitions.append(fac.Transition(st_29, [
        fac.UpdateInstruction(cc_31, False) ]))
    st_28._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_29, [
        fac.UpdateInstruction(cc_32, True) ]))
    st_29._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
MT305_SequenceB_ReportingInformation._Automaton = _BuildAutomaton_()




MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ReportingJurisdiction'), MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_22L_Type, scope=MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1102, 3)))

MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ReportingParty_A'), MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_91A_Type, scope=MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1104, 4)))

MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ReportingParty_D'), MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_91D_Type, scope=MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1105, 4)))

MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ReportingParty_J'), MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_91J_Type, scope=MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1106, 4)))

MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SubsequenceB1a_UniqueTransactionIdentifier'), MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier, scope=MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1108, 3)))

def _BuildAutomaton_2 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_2
    del _BuildAutomaton_2
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1103, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1104, 4))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1105, 4))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1106, 4))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1108, 3))
    counters.add(cc_4)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ReportingJurisdiction')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1102, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ReportingParty_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1104, 4))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ReportingParty_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1105, 4))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ReportingParty_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1106, 4))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SubsequenceB1a_UniqueTransactionIdentifier')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1108, 3))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    transitions.append(fac.Transition(st_2, [
         ]))
    transitions.append(fac.Transition(st_3, [
         ]))
    transitions.append(fac.Transition(st_4, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True),
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True),
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True),
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_1, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_2, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_3, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_4, True) ]))
    st_4._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties._Automaton = _BuildAutomaton_2()




MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'UTINamespaceIssuerCode'), MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_22M_Type, scope=MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1113, 3)))

MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TransactionIdentifier'), MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_22N_Type, scope=MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1114, 3)))

MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SubsequenceB1a1_PriorUniqueTransactionIdentifier'), MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_SubsequenceB1a1_PriorUniqueTransactionIdentifier, scope=MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1115, 3)))

def _BuildAutomaton_3 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_3
    del _BuildAutomaton_3
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1115, 3))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'UTINamespaceIssuerCode')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1113, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'TransactionIdentifier')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1114, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SubsequenceB1a1_PriorUniqueTransactionIdentifier')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1115, 3))
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
        fac.UpdateInstruction(cc_0, True) ]))
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier._Automaton = _BuildAutomaton_3()




MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_SubsequenceB1a1_PriorUniqueTransactionIdentifier._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PUTINamespaceIssuerCode'), MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_SubsequenceB1a1_PriorUniqueTransactionIdentifier_22P_Type, scope=MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_SubsequenceB1a1_PriorUniqueTransactionIdentifier, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1120, 3)))

MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_SubsequenceB1a1_PriorUniqueTransactionIdentifier._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PriorTransactionIdentifier'), MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_SubsequenceB1a1_PriorUniqueTransactionIdentifier_22R_Type, scope=MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_SubsequenceB1a1_PriorUniqueTransactionIdentifier, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1121, 3)))

def _BuildAutomaton_4 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_4
    del _BuildAutomaton_4
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_SubsequenceB1a1_PriorUniqueTransactionIdentifier._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PUTINamespaceIssuerCode')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1120, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_SubsequenceB1a1_PriorUniqueTransactionIdentifier._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PriorTransactionIdentifier')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1121, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
MT305_SequenceB_ReportingInformation_SubsequenceB1_ReportingParties_SubsequenceB1a_UniqueTransactionIdentifier_SubsequenceB1a1_PriorUniqueTransactionIdentifier._Automaton = _BuildAutomaton_4()




CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SequenceA_GeneralInformation'), MT305_SequenceA_GeneralInformation, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1127, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SequenceB_ReportingInformation'), MT305_SequenceB_ReportingInformation, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1128, 4)))

def _BuildAutomaton_5 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_5
    del _BuildAutomaton_5
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1128, 4))
    counters.add(cc_0)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SequenceA_GeneralInformation')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1127, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SequenceB_ReportingInformation')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT305.xsd', 1128, 4))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON._Automaton = _BuildAutomaton_5()


