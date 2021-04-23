# C:\Projects\Code\SwiftMessagingSolution_Python3\base\extensions\SwiftIntegration\Utilities\XSD\MT202COV.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:96afad3d20bbfe8d040a1a097fa388d9fecd10e3
# Generated 2019-11-06 16:22:28.977127 by PyXB version 1.2.6 using Python 3.7.4.final.0
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
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:86abda4c-0083-11ea-8ace-509a4c321f2f')

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


# Atomic simple type: {http://www.w3schools.com}MT202COV_SequenceA_GeneralInformation_20_Type_Pattern
class MT202COV_SequenceA_GeneralInformation_20_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202COV_SequenceA_GeneralInformation_20_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 3, 1)
    _Documentation = None
MT202COV_SequenceA_GeneralInformation_20_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT202COV_SequenceA_GeneralInformation_20_Type_Pattern._CF_pattern.addPattern(pattern="([^/]([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,16}[^/])")
MT202COV_SequenceA_GeneralInformation_20_Type_Pattern._InitializeFacetMap(MT202COV_SequenceA_GeneralInformation_20_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT202COV_SequenceA_GeneralInformation_20_Type_Pattern', MT202COV_SequenceA_GeneralInformation_20_Type_Pattern)
_module_typeBindings.MT202COV_SequenceA_GeneralInformation_20_Type_Pattern = MT202COV_SequenceA_GeneralInformation_20_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT202COV_SequenceA_GeneralInformation_21_Type_Pattern
class MT202COV_SequenceA_GeneralInformation_21_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202COV_SequenceA_GeneralInformation_21_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 16, 1)
    _Documentation = None
MT202COV_SequenceA_GeneralInformation_21_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT202COV_SequenceA_GeneralInformation_21_Type_Pattern._CF_pattern.addPattern(pattern="([^/]([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,16}[^/])")
MT202COV_SequenceA_GeneralInformation_21_Type_Pattern._InitializeFacetMap(MT202COV_SequenceA_GeneralInformation_21_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT202COV_SequenceA_GeneralInformation_21_Type_Pattern', MT202COV_SequenceA_GeneralInformation_21_Type_Pattern)
_module_typeBindings.MT202COV_SequenceA_GeneralInformation_21_Type_Pattern = MT202COV_SequenceA_GeneralInformation_21_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT202COV_SequenceA_GeneralInformation_13C_Type_Pattern
class MT202COV_SequenceA_GeneralInformation_13C_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202COV_SequenceA_GeneralInformation_13C_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 29, 1)
    _Documentation = None
MT202COV_SequenceA_GeneralInformation_13C_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT202COV_SequenceA_GeneralInformation_13C_Type_Pattern._CF_pattern.addPattern(pattern='(/(CLSTIME|RNCTIME|SNDTIME)/(0[0-9]|[1][0-9]|2[1-3])([0-5][0-9])([+]|[-])(0[0-9]|[1][0-9]|2[1-3])([0-5][0-9]))')
MT202COV_SequenceA_GeneralInformation_13C_Type_Pattern._InitializeFacetMap(MT202COV_SequenceA_GeneralInformation_13C_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT202COV_SequenceA_GeneralInformation_13C_Type_Pattern', MT202COV_SequenceA_GeneralInformation_13C_Type_Pattern)
_module_typeBindings.MT202COV_SequenceA_GeneralInformation_13C_Type_Pattern = MT202COV_SequenceA_GeneralInformation_13C_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT202COV_SequenceA_GeneralInformation_32A_Type_Pattern
class MT202COV_SequenceA_GeneralInformation_32A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202COV_SequenceA_GeneralInformation_32A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 42, 1)
    _Documentation = None
MT202COV_SequenceA_GeneralInformation_32A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT202COV_SequenceA_GeneralInformation_32A_Type_Pattern._CF_pattern.addPattern(pattern='([0-9]{2}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})')
MT202COV_SequenceA_GeneralInformation_32A_Type_Pattern._InitializeFacetMap(MT202COV_SequenceA_GeneralInformation_32A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT202COV_SequenceA_GeneralInformation_32A_Type_Pattern', MT202COV_SequenceA_GeneralInformation_32A_Type_Pattern)
_module_typeBindings.MT202COV_SequenceA_GeneralInformation_32A_Type_Pattern = MT202COV_SequenceA_GeneralInformation_32A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT202COV_SequenceA_GeneralInformation_52A_Type_Pattern
class MT202COV_SequenceA_GeneralInformation_52A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202COV_SequenceA_GeneralInformation_52A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 55, 1)
    _Documentation = None
MT202COV_SequenceA_GeneralInformation_52A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT202COV_SequenceA_GeneralInformation_52A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT202COV_SequenceA_GeneralInformation_52A_Type_Pattern._InitializeFacetMap(MT202COV_SequenceA_GeneralInformation_52A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT202COV_SequenceA_GeneralInformation_52A_Type_Pattern', MT202COV_SequenceA_GeneralInformation_52A_Type_Pattern)
_module_typeBindings.MT202COV_SequenceA_GeneralInformation_52A_Type_Pattern = MT202COV_SequenceA_GeneralInformation_52A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT202COV_SequenceA_GeneralInformation_52D_Type_Pattern
class MT202COV_SequenceA_GeneralInformation_52D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202COV_SequenceA_GeneralInformation_52D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 68, 1)
    _Documentation = None
MT202COV_SequenceA_GeneralInformation_52D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT202COV_SequenceA_GeneralInformation_52D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT202COV_SequenceA_GeneralInformation_52D_Type_Pattern._InitializeFacetMap(MT202COV_SequenceA_GeneralInformation_52D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT202COV_SequenceA_GeneralInformation_52D_Type_Pattern', MT202COV_SequenceA_GeneralInformation_52D_Type_Pattern)
_module_typeBindings.MT202COV_SequenceA_GeneralInformation_52D_Type_Pattern = MT202COV_SequenceA_GeneralInformation_52D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT202COV_SequenceA_GeneralInformation_53A_Type_Pattern
class MT202COV_SequenceA_GeneralInformation_53A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202COV_SequenceA_GeneralInformation_53A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 81, 1)
    _Documentation = None
MT202COV_SequenceA_GeneralInformation_53A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT202COV_SequenceA_GeneralInformation_53A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT202COV_SequenceA_GeneralInformation_53A_Type_Pattern._InitializeFacetMap(MT202COV_SequenceA_GeneralInformation_53A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT202COV_SequenceA_GeneralInformation_53A_Type_Pattern', MT202COV_SequenceA_GeneralInformation_53A_Type_Pattern)
_module_typeBindings.MT202COV_SequenceA_GeneralInformation_53A_Type_Pattern = MT202COV_SequenceA_GeneralInformation_53A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT202COV_SequenceA_GeneralInformation_53B_Type_Pattern
class MT202COV_SequenceA_GeneralInformation_53B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202COV_SequenceA_GeneralInformation_53B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 94, 1)
    _Documentation = None
MT202COV_SequenceA_GeneralInformation_53B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT202COV_SequenceA_GeneralInformation_53B_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35})?)")
MT202COV_SequenceA_GeneralInformation_53B_Type_Pattern._InitializeFacetMap(MT202COV_SequenceA_GeneralInformation_53B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT202COV_SequenceA_GeneralInformation_53B_Type_Pattern', MT202COV_SequenceA_GeneralInformation_53B_Type_Pattern)
_module_typeBindings.MT202COV_SequenceA_GeneralInformation_53B_Type_Pattern = MT202COV_SequenceA_GeneralInformation_53B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT202COV_SequenceA_GeneralInformation_53D_Type_Pattern
class MT202COV_SequenceA_GeneralInformation_53D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202COV_SequenceA_GeneralInformation_53D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 107, 1)
    _Documentation = None
MT202COV_SequenceA_GeneralInformation_53D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT202COV_SequenceA_GeneralInformation_53D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT202COV_SequenceA_GeneralInformation_53D_Type_Pattern._InitializeFacetMap(MT202COV_SequenceA_GeneralInformation_53D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT202COV_SequenceA_GeneralInformation_53D_Type_Pattern', MT202COV_SequenceA_GeneralInformation_53D_Type_Pattern)
_module_typeBindings.MT202COV_SequenceA_GeneralInformation_53D_Type_Pattern = MT202COV_SequenceA_GeneralInformation_53D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT202COV_SequenceA_GeneralInformation_54A_Type_Pattern
class MT202COV_SequenceA_GeneralInformation_54A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202COV_SequenceA_GeneralInformation_54A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 120, 1)
    _Documentation = None
MT202COV_SequenceA_GeneralInformation_54A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT202COV_SequenceA_GeneralInformation_54A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT202COV_SequenceA_GeneralInformation_54A_Type_Pattern._InitializeFacetMap(MT202COV_SequenceA_GeneralInformation_54A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT202COV_SequenceA_GeneralInformation_54A_Type_Pattern', MT202COV_SequenceA_GeneralInformation_54A_Type_Pattern)
_module_typeBindings.MT202COV_SequenceA_GeneralInformation_54A_Type_Pattern = MT202COV_SequenceA_GeneralInformation_54A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT202COV_SequenceA_GeneralInformation_54B_Type_Pattern
class MT202COV_SequenceA_GeneralInformation_54B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202COV_SequenceA_GeneralInformation_54B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 133, 1)
    _Documentation = None
MT202COV_SequenceA_GeneralInformation_54B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT202COV_SequenceA_GeneralInformation_54B_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35})?)")
MT202COV_SequenceA_GeneralInformation_54B_Type_Pattern._InitializeFacetMap(MT202COV_SequenceA_GeneralInformation_54B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT202COV_SequenceA_GeneralInformation_54B_Type_Pattern', MT202COV_SequenceA_GeneralInformation_54B_Type_Pattern)
_module_typeBindings.MT202COV_SequenceA_GeneralInformation_54B_Type_Pattern = MT202COV_SequenceA_GeneralInformation_54B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT202COV_SequenceA_GeneralInformation_54D_Type_Pattern
class MT202COV_SequenceA_GeneralInformation_54D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202COV_SequenceA_GeneralInformation_54D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 146, 1)
    _Documentation = None
MT202COV_SequenceA_GeneralInformation_54D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT202COV_SequenceA_GeneralInformation_54D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT202COV_SequenceA_GeneralInformation_54D_Type_Pattern._InitializeFacetMap(MT202COV_SequenceA_GeneralInformation_54D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT202COV_SequenceA_GeneralInformation_54D_Type_Pattern', MT202COV_SequenceA_GeneralInformation_54D_Type_Pattern)
_module_typeBindings.MT202COV_SequenceA_GeneralInformation_54D_Type_Pattern = MT202COV_SequenceA_GeneralInformation_54D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT202COV_SequenceA_GeneralInformation_56A_Type_Pattern
class MT202COV_SequenceA_GeneralInformation_56A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202COV_SequenceA_GeneralInformation_56A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 159, 1)
    _Documentation = None
MT202COV_SequenceA_GeneralInformation_56A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT202COV_SequenceA_GeneralInformation_56A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT202COV_SequenceA_GeneralInformation_56A_Type_Pattern._InitializeFacetMap(MT202COV_SequenceA_GeneralInformation_56A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT202COV_SequenceA_GeneralInformation_56A_Type_Pattern', MT202COV_SequenceA_GeneralInformation_56A_Type_Pattern)
_module_typeBindings.MT202COV_SequenceA_GeneralInformation_56A_Type_Pattern = MT202COV_SequenceA_GeneralInformation_56A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT202COV_SequenceA_GeneralInformation_56D_Type_Pattern
class MT202COV_SequenceA_GeneralInformation_56D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202COV_SequenceA_GeneralInformation_56D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 172, 1)
    _Documentation = None
MT202COV_SequenceA_GeneralInformation_56D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT202COV_SequenceA_GeneralInformation_56D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT202COV_SequenceA_GeneralInformation_56D_Type_Pattern._InitializeFacetMap(MT202COV_SequenceA_GeneralInformation_56D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT202COV_SequenceA_GeneralInformation_56D_Type_Pattern', MT202COV_SequenceA_GeneralInformation_56D_Type_Pattern)
_module_typeBindings.MT202COV_SequenceA_GeneralInformation_56D_Type_Pattern = MT202COV_SequenceA_GeneralInformation_56D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT202COV_SequenceA_GeneralInformation_57A_Type_Pattern
class MT202COV_SequenceA_GeneralInformation_57A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202COV_SequenceA_GeneralInformation_57A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 185, 1)
    _Documentation = None
MT202COV_SequenceA_GeneralInformation_57A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT202COV_SequenceA_GeneralInformation_57A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT202COV_SequenceA_GeneralInformation_57A_Type_Pattern._InitializeFacetMap(MT202COV_SequenceA_GeneralInformation_57A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT202COV_SequenceA_GeneralInformation_57A_Type_Pattern', MT202COV_SequenceA_GeneralInformation_57A_Type_Pattern)
_module_typeBindings.MT202COV_SequenceA_GeneralInformation_57A_Type_Pattern = MT202COV_SequenceA_GeneralInformation_57A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT202COV_SequenceA_GeneralInformation_57B_Type_Pattern
class MT202COV_SequenceA_GeneralInformation_57B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202COV_SequenceA_GeneralInformation_57B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 198, 1)
    _Documentation = None
MT202COV_SequenceA_GeneralInformation_57B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT202COV_SequenceA_GeneralInformation_57B_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35})?)")
MT202COV_SequenceA_GeneralInformation_57B_Type_Pattern._InitializeFacetMap(MT202COV_SequenceA_GeneralInformation_57B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT202COV_SequenceA_GeneralInformation_57B_Type_Pattern', MT202COV_SequenceA_GeneralInformation_57B_Type_Pattern)
_module_typeBindings.MT202COV_SequenceA_GeneralInformation_57B_Type_Pattern = MT202COV_SequenceA_GeneralInformation_57B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT202COV_SequenceA_GeneralInformation_57D_Type_Pattern
class MT202COV_SequenceA_GeneralInformation_57D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202COV_SequenceA_GeneralInformation_57D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 211, 1)
    _Documentation = None
MT202COV_SequenceA_GeneralInformation_57D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT202COV_SequenceA_GeneralInformation_57D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT202COV_SequenceA_GeneralInformation_57D_Type_Pattern._InitializeFacetMap(MT202COV_SequenceA_GeneralInformation_57D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT202COV_SequenceA_GeneralInformation_57D_Type_Pattern', MT202COV_SequenceA_GeneralInformation_57D_Type_Pattern)
_module_typeBindings.MT202COV_SequenceA_GeneralInformation_57D_Type_Pattern = MT202COV_SequenceA_GeneralInformation_57D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT202COV_SequenceA_GeneralInformation_58A_Type_Pattern
class MT202COV_SequenceA_GeneralInformation_58A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202COV_SequenceA_GeneralInformation_58A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 224, 1)
    _Documentation = None
MT202COV_SequenceA_GeneralInformation_58A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT202COV_SequenceA_GeneralInformation_58A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT202COV_SequenceA_GeneralInformation_58A_Type_Pattern._InitializeFacetMap(MT202COV_SequenceA_GeneralInformation_58A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT202COV_SequenceA_GeneralInformation_58A_Type_Pattern', MT202COV_SequenceA_GeneralInformation_58A_Type_Pattern)
_module_typeBindings.MT202COV_SequenceA_GeneralInformation_58A_Type_Pattern = MT202COV_SequenceA_GeneralInformation_58A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT202COV_SequenceA_GeneralInformation_58D_Type_Pattern
class MT202COV_SequenceA_GeneralInformation_58D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202COV_SequenceA_GeneralInformation_58D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 237, 1)
    _Documentation = None
MT202COV_SequenceA_GeneralInformation_58D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT202COV_SequenceA_GeneralInformation_58D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT202COV_SequenceA_GeneralInformation_58D_Type_Pattern._InitializeFacetMap(MT202COV_SequenceA_GeneralInformation_58D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT202COV_SequenceA_GeneralInformation_58D_Type_Pattern', MT202COV_SequenceA_GeneralInformation_58D_Type_Pattern)
_module_typeBindings.MT202COV_SequenceA_GeneralInformation_58D_Type_Pattern = MT202COV_SequenceA_GeneralInformation_58D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT202COV_SequenceA_GeneralInformation_72_Type_Pattern
class MT202COV_SequenceA_GeneralInformation_72_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202COV_SequenceA_GeneralInformation_72_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 250, 1)
    _Documentation = None
MT202COV_SequenceA_GeneralInformation_72_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT202COV_SequenceA_GeneralInformation_72_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,6})")
MT202COV_SequenceA_GeneralInformation_72_Type_Pattern._InitializeFacetMap(MT202COV_SequenceA_GeneralInformation_72_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT202COV_SequenceA_GeneralInformation_72_Type_Pattern', MT202COV_SequenceA_GeneralInformation_72_Type_Pattern)
_module_typeBindings.MT202COV_SequenceA_GeneralInformation_72_Type_Pattern = MT202COV_SequenceA_GeneralInformation_72_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50A_Type_Pattern
class MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 263, 1)
    _Documentation = None
MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50A_Type_Pattern._CF_pattern.addPattern(pattern="((/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50A_Type_Pattern._InitializeFacetMap(MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50A_Type_Pattern', MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50A_Type_Pattern)
_module_typeBindings.MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50A_Type_Pattern = MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50F_Type_Pattern
class MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50F_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50F_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 276, 1)
    _Documentation = None
MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50F_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50F_Type_Pattern._CF_pattern.addPattern(pattern="(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50F_Type_Pattern._InitializeFacetMap(MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50F_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50F_Type_Pattern', MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50F_Type_Pattern)
_module_typeBindings.MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50F_Type_Pattern = MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50F_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50K_Type_Pattern
class MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50K_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50K_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 289, 1)
    _Documentation = None
MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50K_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50K_Type_Pattern._CF_pattern.addPattern(pattern="((/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50K_Type_Pattern._InitializeFacetMap(MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50K_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50K_Type_Pattern', MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50K_Type_Pattern)
_module_typeBindings.MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50K_Type_Pattern = MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50K_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_52A_Type_Pattern
class MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_52A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_52A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 302, 1)
    _Documentation = None
MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_52A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_52A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_52A_Type_Pattern._InitializeFacetMap(MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_52A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_52A_Type_Pattern', MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_52A_Type_Pattern)
_module_typeBindings.MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_52A_Type_Pattern = MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_52A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_52D_Type_Pattern
class MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_52D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_52D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 315, 1)
    _Documentation = None
MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_52D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_52D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_52D_Type_Pattern._InitializeFacetMap(MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_52D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_52D_Type_Pattern', MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_52D_Type_Pattern)
_module_typeBindings.MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_52D_Type_Pattern = MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_52D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_56A_Type_Pattern
class MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_56A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_56A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 328, 1)
    _Documentation = None
MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_56A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_56A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_56A_Type_Pattern._InitializeFacetMap(MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_56A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_56A_Type_Pattern', MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_56A_Type_Pattern)
_module_typeBindings.MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_56A_Type_Pattern = MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_56A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_56C_Type_Pattern
class MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_56C_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_56C_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 341, 1)
    _Documentation = None
MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_56C_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_56C_Type_Pattern._CF_pattern.addPattern(pattern="(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})")
MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_56C_Type_Pattern._InitializeFacetMap(MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_56C_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_56C_Type_Pattern', MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_56C_Type_Pattern)
_module_typeBindings.MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_56C_Type_Pattern = MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_56C_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_56D_Type_Pattern
class MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_56D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_56D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 354, 1)
    _Documentation = None
MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_56D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_56D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_56D_Type_Pattern._InitializeFacetMap(MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_56D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_56D_Type_Pattern', MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_56D_Type_Pattern)
_module_typeBindings.MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_56D_Type_Pattern = MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_56D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57A_Type_Pattern
class MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 367, 1)
    _Documentation = None
MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57A_Type_Pattern._InitializeFacetMap(MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57A_Type_Pattern', MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57A_Type_Pattern)
_module_typeBindings.MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57A_Type_Pattern = MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57B_Type_Pattern
class MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 380, 1)
    _Documentation = None
MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57B_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35})?)")
MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57B_Type_Pattern._InitializeFacetMap(MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57B_Type_Pattern', MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57B_Type_Pattern)
_module_typeBindings.MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57B_Type_Pattern = MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57C_Type_Pattern
class MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57C_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57C_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 393, 1)
    _Documentation = None
MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57C_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57C_Type_Pattern._CF_pattern.addPattern(pattern="(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})")
MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57C_Type_Pattern._InitializeFacetMap(MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57C_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57C_Type_Pattern', MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57C_Type_Pattern)
_module_typeBindings.MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57C_Type_Pattern = MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57C_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57D_Type_Pattern
class MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 406, 1)
    _Documentation = None
MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57D_Type_Pattern._InitializeFacetMap(MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57D_Type_Pattern', MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57D_Type_Pattern)
_module_typeBindings.MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57D_Type_Pattern = MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59_Type_Pattern
class MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 419, 1)
    _Documentation = None
MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59_Type_Pattern._CF_pattern.addPattern(pattern="((/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59_Type_Pattern._InitializeFacetMap(MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59_Type_Pattern', MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59_Type_Pattern)
_module_typeBindings.MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59_Type_Pattern = MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59A_Type_Pattern
class MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 432, 1)
    _Documentation = None
MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59A_Type_Pattern._CF_pattern.addPattern(pattern="((/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59A_Type_Pattern._InitializeFacetMap(MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59A_Type_Pattern', MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59A_Type_Pattern)
_module_typeBindings.MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59A_Type_Pattern = MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59F_Type_Pattern
class MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59F_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59F_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 445, 1)
    _Documentation = None
MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59F_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59F_Type_Pattern._CF_pattern.addPattern(pattern="((/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?((1|2|3)/(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,33}\\n?){1,4}))")
MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59F_Type_Pattern._InitializeFacetMap(MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59F_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59F_Type_Pattern', MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59F_Type_Pattern)
_module_typeBindings.MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59F_Type_Pattern = MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59F_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_70_Type_Pattern
class MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_70_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_70_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 458, 1)
    _Documentation = None
MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_70_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_70_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_70_Type_Pattern._InitializeFacetMap(MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_70_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_70_Type_Pattern', MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_70_Type_Pattern)
_module_typeBindings.MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_70_Type_Pattern = MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_70_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_72_Type_Pattern
class MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_72_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_72_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 471, 1)
    _Documentation = None
MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_72_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_72_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,6})")
MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_72_Type_Pattern._InitializeFacetMap(MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_72_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_72_Type_Pattern', MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_72_Type_Pattern)
_module_typeBindings.MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_72_Type_Pattern = MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_72_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_33B_Type_Pattern
class MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_33B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_33B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 484, 1)
    _Documentation = None
MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_33B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_33B_Type_Pattern._CF_pattern.addPattern(pattern='((AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})')
MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_33B_Type_Pattern._InitializeFacetMap(MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_33B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_33B_Type_Pattern', MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_33B_Type_Pattern)
_module_typeBindings.MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_33B_Type_Pattern = MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_33B_Type_Pattern

# Complex type {http://www.w3schools.com}MT202COV_SequenceA_GeneralInformation with content type ELEMENT_ONLY
class MT202COV_SequenceA_GeneralInformation (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT202COV_SequenceA_GeneralInformation with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202COV_SequenceA_GeneralInformation')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 497, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}TransactionReferenceNumber uses Python identifier TransactionReferenceNumber
    __TransactionReferenceNumber = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'TransactionReferenceNumber'), 'TransactionReferenceNumber', '__httpwww_w3schools_com_MT202COV_SequenceA_GeneralInformation_httpwww_w3schools_comTransactionReferenceNumber', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 499, 3), )

    
    TransactionReferenceNumber = property(__TransactionReferenceNumber.value, __TransactionReferenceNumber.set, None, None)

    
    # Element {http://www.w3schools.com}RelatedReference uses Python identifier RelatedReference
    __RelatedReference = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'RelatedReference'), 'RelatedReference', '__httpwww_w3schools_com_MT202COV_SequenceA_GeneralInformation_httpwww_w3schools_comRelatedReference', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 500, 3), )

    
    RelatedReference = property(__RelatedReference.value, __RelatedReference.set, None, None)

    
    # Element {http://www.w3schools.com}TimeIndication uses Python identifier TimeIndication
    __TimeIndication = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'TimeIndication'), 'TimeIndication', '__httpwww_w3schools_com_MT202COV_SequenceA_GeneralInformation_httpwww_w3schools_comTimeIndication', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 501, 3), )

    
    TimeIndication = property(__TimeIndication.value, __TimeIndication.set, None, None)

    
    # Element {http://www.w3schools.com}DateCurrencyAmount uses Python identifier DateCurrencyAmount
    __DateCurrencyAmount = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DateCurrencyAmount'), 'DateCurrencyAmount', '__httpwww_w3schools_com_MT202COV_SequenceA_GeneralInformation_httpwww_w3schools_comDateCurrencyAmount', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 502, 3), )

    
    DateCurrencyAmount = property(__DateCurrencyAmount.value, __DateCurrencyAmount.set, None, None)

    
    # Element {http://www.w3schools.com}OrderingInstitution_A uses Python identifier OrderingInstitution_A
    __OrderingInstitution_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'OrderingInstitution_A'), 'OrderingInstitution_A', '__httpwww_w3schools_com_MT202COV_SequenceA_GeneralInformation_httpwww_w3schools_comOrderingInstitution_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 504, 4), )

    
    OrderingInstitution_A = property(__OrderingInstitution_A.value, __OrderingInstitution_A.set, None, None)

    
    # Element {http://www.w3schools.com}OrderingInstitution_D uses Python identifier OrderingInstitution_D
    __OrderingInstitution_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'OrderingInstitution_D'), 'OrderingInstitution_D', '__httpwww_w3schools_com_MT202COV_SequenceA_GeneralInformation_httpwww_w3schools_comOrderingInstitution_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 505, 4), )

    
    OrderingInstitution_D = property(__OrderingInstitution_D.value, __OrderingInstitution_D.set, None, None)

    
    # Element {http://www.w3schools.com}SendersCorrespondent_A uses Python identifier SendersCorrespondent_A
    __SendersCorrespondent_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SendersCorrespondent_A'), 'SendersCorrespondent_A', '__httpwww_w3schools_com_MT202COV_SequenceA_GeneralInformation_httpwww_w3schools_comSendersCorrespondent_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 508, 4), )

    
    SendersCorrespondent_A = property(__SendersCorrespondent_A.value, __SendersCorrespondent_A.set, None, None)

    
    # Element {http://www.w3schools.com}SendersCorrespondent_B uses Python identifier SendersCorrespondent_B
    __SendersCorrespondent_B = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SendersCorrespondent_B'), 'SendersCorrespondent_B', '__httpwww_w3schools_com_MT202COV_SequenceA_GeneralInformation_httpwww_w3schools_comSendersCorrespondent_B', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 509, 4), )

    
    SendersCorrespondent_B = property(__SendersCorrespondent_B.value, __SendersCorrespondent_B.set, None, None)

    
    # Element {http://www.w3schools.com}SendersCorrespondent_D uses Python identifier SendersCorrespondent_D
    __SendersCorrespondent_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SendersCorrespondent_D'), 'SendersCorrespondent_D', '__httpwww_w3schools_com_MT202COV_SequenceA_GeneralInformation_httpwww_w3schools_comSendersCorrespondent_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 510, 4), )

    
    SendersCorrespondent_D = property(__SendersCorrespondent_D.value, __SendersCorrespondent_D.set, None, None)

    
    # Element {http://www.w3schools.com}ReceiversCorrespondent_A uses Python identifier ReceiversCorrespondent_A
    __ReceiversCorrespondent_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ReceiversCorrespondent_A'), 'ReceiversCorrespondent_A', '__httpwww_w3schools_com_MT202COV_SequenceA_GeneralInformation_httpwww_w3schools_comReceiversCorrespondent_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 513, 4), )

    
    ReceiversCorrespondent_A = property(__ReceiversCorrespondent_A.value, __ReceiversCorrespondent_A.set, None, None)

    
    # Element {http://www.w3schools.com}ReceiversCorrespondent_B uses Python identifier ReceiversCorrespondent_B
    __ReceiversCorrespondent_B = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ReceiversCorrespondent_B'), 'ReceiversCorrespondent_B', '__httpwww_w3schools_com_MT202COV_SequenceA_GeneralInformation_httpwww_w3schools_comReceiversCorrespondent_B', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 514, 4), )

    
    ReceiversCorrespondent_B = property(__ReceiversCorrespondent_B.value, __ReceiversCorrespondent_B.set, None, None)

    
    # Element {http://www.w3schools.com}ReceiversCorrespondent_D uses Python identifier ReceiversCorrespondent_D
    __ReceiversCorrespondent_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ReceiversCorrespondent_D'), 'ReceiversCorrespondent_D', '__httpwww_w3schools_com_MT202COV_SequenceA_GeneralInformation_httpwww_w3schools_comReceiversCorrespondent_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 515, 4), )

    
    ReceiversCorrespondent_D = property(__ReceiversCorrespondent_D.value, __ReceiversCorrespondent_D.set, None, None)

    
    # Element {http://www.w3schools.com}Intermedairy_A uses Python identifier Intermedairy_A
    __Intermedairy_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Intermedairy_A'), 'Intermedairy_A', '__httpwww_w3schools_com_MT202COV_SequenceA_GeneralInformation_httpwww_w3schools_comIntermedairy_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 518, 4), )

    
    Intermedairy_A = property(__Intermedairy_A.value, __Intermedairy_A.set, None, None)

    
    # Element {http://www.w3schools.com}Intermedairy_D uses Python identifier Intermedairy_D
    __Intermedairy_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Intermedairy_D'), 'Intermedairy_D', '__httpwww_w3schools_com_MT202COV_SequenceA_GeneralInformation_httpwww_w3schools_comIntermedairy_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 519, 4), )

    
    Intermedairy_D = property(__Intermedairy_D.value, __Intermedairy_D.set, None, None)

    
    # Element {http://www.w3schools.com}AccountWithInstitution_A uses Python identifier AccountWithInstitution_A
    __AccountWithInstitution_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'AccountWithInstitution_A'), 'AccountWithInstitution_A', '__httpwww_w3schools_com_MT202COV_SequenceA_GeneralInformation_httpwww_w3schools_comAccountWithInstitution_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 522, 4), )

    
    AccountWithInstitution_A = property(__AccountWithInstitution_A.value, __AccountWithInstitution_A.set, None, None)

    
    # Element {http://www.w3schools.com}AccountWithInstitution_B uses Python identifier AccountWithInstitution_B
    __AccountWithInstitution_B = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'AccountWithInstitution_B'), 'AccountWithInstitution_B', '__httpwww_w3schools_com_MT202COV_SequenceA_GeneralInformation_httpwww_w3schools_comAccountWithInstitution_B', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 523, 4), )

    
    AccountWithInstitution_B = property(__AccountWithInstitution_B.value, __AccountWithInstitution_B.set, None, None)

    
    # Element {http://www.w3schools.com}AccountWithInstitution_D uses Python identifier AccountWithInstitution_D
    __AccountWithInstitution_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'AccountWithInstitution_D'), 'AccountWithInstitution_D', '__httpwww_w3schools_com_MT202COV_SequenceA_GeneralInformation_httpwww_w3schools_comAccountWithInstitution_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 524, 4), )

    
    AccountWithInstitution_D = property(__AccountWithInstitution_D.value, __AccountWithInstitution_D.set, None, None)

    
    # Element {http://www.w3schools.com}BeneficiaryInstitution_A uses Python identifier BeneficiaryInstitution_A
    __BeneficiaryInstitution_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_A'), 'BeneficiaryInstitution_A', '__httpwww_w3schools_com_MT202COV_SequenceA_GeneralInformation_httpwww_w3schools_comBeneficiaryInstitution_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 527, 4), )

    
    BeneficiaryInstitution_A = property(__BeneficiaryInstitution_A.value, __BeneficiaryInstitution_A.set, None, None)

    
    # Element {http://www.w3schools.com}BeneficiaryInstitution_D uses Python identifier BeneficiaryInstitution_D
    __BeneficiaryInstitution_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_D'), 'BeneficiaryInstitution_D', '__httpwww_w3schools_com_MT202COV_SequenceA_GeneralInformation_httpwww_w3schools_comBeneficiaryInstitution_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 528, 4), )

    
    BeneficiaryInstitution_D = property(__BeneficiaryInstitution_D.value, __BeneficiaryInstitution_D.set, None, None)

    
    # Element {http://www.w3schools.com}SenderToReceiverInformation uses Python identifier SenderToReceiverInformation
    __SenderToReceiverInformation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SenderToReceiverInformation'), 'SenderToReceiverInformation', '__httpwww_w3schools_com_MT202COV_SequenceA_GeneralInformation_httpwww_w3schools_comSenderToReceiverInformation', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 530, 3), )

    
    SenderToReceiverInformation = property(__SenderToReceiverInformation.value, __SenderToReceiverInformation.set, None, None)

    _ElementMap.update({
        __TransactionReferenceNumber.name() : __TransactionReferenceNumber,
        __RelatedReference.name() : __RelatedReference,
        __TimeIndication.name() : __TimeIndication,
        __DateCurrencyAmount.name() : __DateCurrencyAmount,
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
_module_typeBindings.MT202COV_SequenceA_GeneralInformation = MT202COV_SequenceA_GeneralInformation
Namespace.addCategoryObject('typeBinding', 'MT202COV_SequenceA_GeneralInformation', MT202COV_SequenceA_GeneralInformation)


# Complex type {http://www.w3schools.com}MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails with content type ELEMENT_ONLY
class MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 533, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}OrderingCustomer_A uses Python identifier OrderingCustomer_A
    __OrderingCustomer_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'OrderingCustomer_A'), 'OrderingCustomer_A', '__httpwww_w3schools_com_MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_httpwww_w3schools_comOrderingCustomer_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 536, 4), )

    
    OrderingCustomer_A = property(__OrderingCustomer_A.value, __OrderingCustomer_A.set, None, None)

    
    # Element {http://www.w3schools.com}OrderingCustomer_F uses Python identifier OrderingCustomer_F
    __OrderingCustomer_F = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'OrderingCustomer_F'), 'OrderingCustomer_F', '__httpwww_w3schools_com_MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_httpwww_w3schools_comOrderingCustomer_F', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 537, 4), )

    
    OrderingCustomer_F = property(__OrderingCustomer_F.value, __OrderingCustomer_F.set, None, None)

    
    # Element {http://www.w3schools.com}OrderingCustomer_K uses Python identifier OrderingCustomer_K
    __OrderingCustomer_K = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'OrderingCustomer_K'), 'OrderingCustomer_K', '__httpwww_w3schools_com_MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_httpwww_w3schools_comOrderingCustomer_K', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 538, 4), )

    
    OrderingCustomer_K = property(__OrderingCustomer_K.value, __OrderingCustomer_K.set, None, None)

    
    # Element {http://www.w3schools.com}OrderingInstitution_A uses Python identifier OrderingInstitution_A
    __OrderingInstitution_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'OrderingInstitution_A'), 'OrderingInstitution_A', '__httpwww_w3schools_com_MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_httpwww_w3schools_comOrderingInstitution_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 541, 4), )

    
    OrderingInstitution_A = property(__OrderingInstitution_A.value, __OrderingInstitution_A.set, None, None)

    
    # Element {http://www.w3schools.com}OrderingInstitution_D uses Python identifier OrderingInstitution_D
    __OrderingInstitution_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'OrderingInstitution_D'), 'OrderingInstitution_D', '__httpwww_w3schools_com_MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_httpwww_w3schools_comOrderingInstitution_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 542, 4), )

    
    OrderingInstitution_D = property(__OrderingInstitution_D.value, __OrderingInstitution_D.set, None, None)

    
    # Element {http://www.w3schools.com}IntermediaryInstitution_A uses Python identifier IntermediaryInstitution_A
    __IntermediaryInstitution_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'IntermediaryInstitution_A'), 'IntermediaryInstitution_A', '__httpwww_w3schools_com_MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_httpwww_w3schools_comIntermediaryInstitution_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 545, 4), )

    
    IntermediaryInstitution_A = property(__IntermediaryInstitution_A.value, __IntermediaryInstitution_A.set, None, None)

    
    # Element {http://www.w3schools.com}IntermediaryInstitution_C uses Python identifier IntermediaryInstitution_C
    __IntermediaryInstitution_C = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'IntermediaryInstitution_C'), 'IntermediaryInstitution_C', '__httpwww_w3schools_com_MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_httpwww_w3schools_comIntermediaryInstitution_C', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 546, 4), )

    
    IntermediaryInstitution_C = property(__IntermediaryInstitution_C.value, __IntermediaryInstitution_C.set, None, None)

    
    # Element {http://www.w3schools.com}IntermediaryInstitution_D uses Python identifier IntermediaryInstitution_D
    __IntermediaryInstitution_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'IntermediaryInstitution_D'), 'IntermediaryInstitution_D', '__httpwww_w3schools_com_MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_httpwww_w3schools_comIntermediaryInstitution_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 547, 4), )

    
    IntermediaryInstitution_D = property(__IntermediaryInstitution_D.value, __IntermediaryInstitution_D.set, None, None)

    
    # Element {http://www.w3schools.com}AccountWithInstitution_A uses Python identifier AccountWithInstitution_A
    __AccountWithInstitution_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'AccountWithInstitution_A'), 'AccountWithInstitution_A', '__httpwww_w3schools_com_MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_httpwww_w3schools_comAccountWithInstitution_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 550, 4), )

    
    AccountWithInstitution_A = property(__AccountWithInstitution_A.value, __AccountWithInstitution_A.set, None, None)

    
    # Element {http://www.w3schools.com}AccountWithInstitution_B uses Python identifier AccountWithInstitution_B
    __AccountWithInstitution_B = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'AccountWithInstitution_B'), 'AccountWithInstitution_B', '__httpwww_w3schools_com_MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_httpwww_w3schools_comAccountWithInstitution_B', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 551, 4), )

    
    AccountWithInstitution_B = property(__AccountWithInstitution_B.value, __AccountWithInstitution_B.set, None, None)

    
    # Element {http://www.w3schools.com}AccountWithInstitution_C uses Python identifier AccountWithInstitution_C
    __AccountWithInstitution_C = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'AccountWithInstitution_C'), 'AccountWithInstitution_C', '__httpwww_w3schools_com_MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_httpwww_w3schools_comAccountWithInstitution_C', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 552, 4), )

    
    AccountWithInstitution_C = property(__AccountWithInstitution_C.value, __AccountWithInstitution_C.set, None, None)

    
    # Element {http://www.w3schools.com}AccountWithInstitution_D uses Python identifier AccountWithInstitution_D
    __AccountWithInstitution_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'AccountWithInstitution_D'), 'AccountWithInstitution_D', '__httpwww_w3schools_com_MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_httpwww_w3schools_comAccountWithInstitution_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 553, 4), )

    
    AccountWithInstitution_D = property(__AccountWithInstitution_D.value, __AccountWithInstitution_D.set, None, None)

    
    # Element {http://www.w3schools.com}BeneficiaryCustomer uses Python identifier BeneficiaryCustomer
    __BeneficiaryCustomer = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryCustomer'), 'BeneficiaryCustomer', '__httpwww_w3schools_com_MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_httpwww_w3schools_comBeneficiaryCustomer', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 556, 4), )

    
    BeneficiaryCustomer = property(__BeneficiaryCustomer.value, __BeneficiaryCustomer.set, None, None)

    
    # Element {http://www.w3schools.com}BeneficiaryCustomer_A uses Python identifier BeneficiaryCustomer_A
    __BeneficiaryCustomer_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryCustomer_A'), 'BeneficiaryCustomer_A', '__httpwww_w3schools_com_MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_httpwww_w3schools_comBeneficiaryCustomer_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 557, 4), )

    
    BeneficiaryCustomer_A = property(__BeneficiaryCustomer_A.value, __BeneficiaryCustomer_A.set, None, None)

    
    # Element {http://www.w3schools.com}BeneficiaryCustomer_F uses Python identifier BeneficiaryCustomer_F
    __BeneficiaryCustomer_F = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryCustomer_F'), 'BeneficiaryCustomer_F', '__httpwww_w3schools_com_MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_httpwww_w3schools_comBeneficiaryCustomer_F', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 558, 4), )

    
    BeneficiaryCustomer_F = property(__BeneficiaryCustomer_F.value, __BeneficiaryCustomer_F.set, None, None)

    
    # Element {http://www.w3schools.com}RemittanceInformation uses Python identifier RemittanceInformation
    __RemittanceInformation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'RemittanceInformation'), 'RemittanceInformation', '__httpwww_w3schools_com_MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_httpwww_w3schools_comRemittanceInformation', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 560, 3), )

    
    RemittanceInformation = property(__RemittanceInformation.value, __RemittanceInformation.set, None, None)

    
    # Element {http://www.w3schools.com}SenderToReceiverInformation uses Python identifier SenderToReceiverInformation
    __SenderToReceiverInformation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SenderToReceiverInformation'), 'SenderToReceiverInformation', '__httpwww_w3schools_com_MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_httpwww_w3schools_comSenderToReceiverInformation', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 561, 3), )

    
    SenderToReceiverInformation = property(__SenderToReceiverInformation.value, __SenderToReceiverInformation.set, None, None)

    
    # Element {http://www.w3schools.com}CurrencyInstructedAmount uses Python identifier CurrencyInstructedAmount
    __CurrencyInstructedAmount = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CurrencyInstructedAmount'), 'CurrencyInstructedAmount', '__httpwww_w3schools_com_MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_httpwww_w3schools_comCurrencyInstructedAmount', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 562, 3), )

    
    CurrencyInstructedAmount = property(__CurrencyInstructedAmount.value, __CurrencyInstructedAmount.set, None, None)

    _ElementMap.update({
        __OrderingCustomer_A.name() : __OrderingCustomer_A,
        __OrderingCustomer_F.name() : __OrderingCustomer_F,
        __OrderingCustomer_K.name() : __OrderingCustomer_K,
        __OrderingInstitution_A.name() : __OrderingInstitution_A,
        __OrderingInstitution_D.name() : __OrderingInstitution_D,
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
        __SenderToReceiverInformation.name() : __SenderToReceiverInformation,
        __CurrencyInstructedAmount.name() : __CurrencyInstructedAmount
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails = MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails
Namespace.addCategoryObject('typeBinding', 'MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails', MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails)


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 566, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}SequenceA_GeneralInformation uses Python identifier SequenceA_GeneralInformation
    __SequenceA_GeneralInformation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SequenceA_GeneralInformation'), 'SequenceA_GeneralInformation', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comSequenceA_GeneralInformation', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 568, 4), )

    
    SequenceA_GeneralInformation = property(__SequenceA_GeneralInformation.value, __SequenceA_GeneralInformation.set, None, None)

    
    # Element {http://www.w3schools.com}SequenceB_UnderlyingCustomerCreditTransferDetails uses Python identifier SequenceB_UnderlyingCustomerCreditTransferDetails
    __SequenceB_UnderlyingCustomerCreditTransferDetails = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SequenceB_UnderlyingCustomerCreditTransferDetails'), 'SequenceB_UnderlyingCustomerCreditTransferDetails', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comSequenceB_UnderlyingCustomerCreditTransferDetails', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 569, 4), )

    
    SequenceB_UnderlyingCustomerCreditTransferDetails = property(__SequenceB_UnderlyingCustomerCreditTransferDetails.value, __SequenceB_UnderlyingCustomerCreditTransferDetails.set, None, None)

    _ElementMap.update({
        __SequenceA_GeneralInformation.name() : __SequenceA_GeneralInformation,
        __SequenceB_UnderlyingCustomerCreditTransferDetails.name() : __SequenceB_UnderlyingCustomerCreditTransferDetails
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON = CTD_ANON


# Complex type {http://www.w3schools.com}MT202COV_SequenceA_GeneralInformation_20_Type with content type SIMPLE
class MT202COV_SequenceA_GeneralInformation_20_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT202COV_SequenceA_GeneralInformation_20_Type with content type SIMPLE"""
    _TypeDefinition = MT202COV_SequenceA_GeneralInformation_20_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202COV_SequenceA_GeneralInformation_20_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 8, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT202COV_SequenceA_GeneralInformation_20_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT202COV_SequenceA_GeneralInformation_20_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='20')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 11, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 11, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT202COV_SequenceA_GeneralInformation_20_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 12, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 12, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT202COV_SequenceA_GeneralInformation_20_Type = MT202COV_SequenceA_GeneralInformation_20_Type
Namespace.addCategoryObject('typeBinding', 'MT202COV_SequenceA_GeneralInformation_20_Type', MT202COV_SequenceA_GeneralInformation_20_Type)


# Complex type {http://www.w3schools.com}MT202COV_SequenceA_GeneralInformation_21_Type with content type SIMPLE
class MT202COV_SequenceA_GeneralInformation_21_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT202COV_SequenceA_GeneralInformation_21_Type with content type SIMPLE"""
    _TypeDefinition = MT202COV_SequenceA_GeneralInformation_21_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202COV_SequenceA_GeneralInformation_21_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 21, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT202COV_SequenceA_GeneralInformation_21_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT202COV_SequenceA_GeneralInformation_21_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='21')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 24, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 24, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT202COV_SequenceA_GeneralInformation_21_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 25, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 25, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT202COV_SequenceA_GeneralInformation_21_Type = MT202COV_SequenceA_GeneralInformation_21_Type
Namespace.addCategoryObject('typeBinding', 'MT202COV_SequenceA_GeneralInformation_21_Type', MT202COV_SequenceA_GeneralInformation_21_Type)


# Complex type {http://www.w3schools.com}MT202COV_SequenceA_GeneralInformation_13C_Type with content type SIMPLE
class MT202COV_SequenceA_GeneralInformation_13C_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT202COV_SequenceA_GeneralInformation_13C_Type with content type SIMPLE"""
    _TypeDefinition = MT202COV_SequenceA_GeneralInformation_13C_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202COV_SequenceA_GeneralInformation_13C_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 34, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT202COV_SequenceA_GeneralInformation_13C_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT202COV_SequenceA_GeneralInformation_13C_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='13C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 37, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 37, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT202COV_SequenceA_GeneralInformation_13C_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 38, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 38, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT202COV_SequenceA_GeneralInformation_13C_Type = MT202COV_SequenceA_GeneralInformation_13C_Type
Namespace.addCategoryObject('typeBinding', 'MT202COV_SequenceA_GeneralInformation_13C_Type', MT202COV_SequenceA_GeneralInformation_13C_Type)


# Complex type {http://www.w3schools.com}MT202COV_SequenceA_GeneralInformation_32A_Type with content type SIMPLE
class MT202COV_SequenceA_GeneralInformation_32A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT202COV_SequenceA_GeneralInformation_32A_Type with content type SIMPLE"""
    _TypeDefinition = MT202COV_SequenceA_GeneralInformation_32A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202COV_SequenceA_GeneralInformation_32A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 47, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT202COV_SequenceA_GeneralInformation_32A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT202COV_SequenceA_GeneralInformation_32A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='32A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 50, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 50, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT202COV_SequenceA_GeneralInformation_32A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 51, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 51, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT202COV_SequenceA_GeneralInformation_32A_Type = MT202COV_SequenceA_GeneralInformation_32A_Type
Namespace.addCategoryObject('typeBinding', 'MT202COV_SequenceA_GeneralInformation_32A_Type', MT202COV_SequenceA_GeneralInformation_32A_Type)


# Complex type {http://www.w3schools.com}MT202COV_SequenceA_GeneralInformation_52A_Type with content type SIMPLE
class MT202COV_SequenceA_GeneralInformation_52A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT202COV_SequenceA_GeneralInformation_52A_Type with content type SIMPLE"""
    _TypeDefinition = MT202COV_SequenceA_GeneralInformation_52A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202COV_SequenceA_GeneralInformation_52A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 60, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT202COV_SequenceA_GeneralInformation_52A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT202COV_SequenceA_GeneralInformation_52A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='52A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 63, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 63, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT202COV_SequenceA_GeneralInformation_52A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 64, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 64, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT202COV_SequenceA_GeneralInformation_52A_Type = MT202COV_SequenceA_GeneralInformation_52A_Type
Namespace.addCategoryObject('typeBinding', 'MT202COV_SequenceA_GeneralInformation_52A_Type', MT202COV_SequenceA_GeneralInformation_52A_Type)


# Complex type {http://www.w3schools.com}MT202COV_SequenceA_GeneralInformation_52D_Type with content type SIMPLE
class MT202COV_SequenceA_GeneralInformation_52D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT202COV_SequenceA_GeneralInformation_52D_Type with content type SIMPLE"""
    _TypeDefinition = MT202COV_SequenceA_GeneralInformation_52D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202COV_SequenceA_GeneralInformation_52D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 73, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT202COV_SequenceA_GeneralInformation_52D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT202COV_SequenceA_GeneralInformation_52D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='52D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 76, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 76, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT202COV_SequenceA_GeneralInformation_52D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 77, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 77, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT202COV_SequenceA_GeneralInformation_52D_Type = MT202COV_SequenceA_GeneralInformation_52D_Type
Namespace.addCategoryObject('typeBinding', 'MT202COV_SequenceA_GeneralInformation_52D_Type', MT202COV_SequenceA_GeneralInformation_52D_Type)


# Complex type {http://www.w3schools.com}MT202COV_SequenceA_GeneralInformation_53A_Type with content type SIMPLE
class MT202COV_SequenceA_GeneralInformation_53A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT202COV_SequenceA_GeneralInformation_53A_Type with content type SIMPLE"""
    _TypeDefinition = MT202COV_SequenceA_GeneralInformation_53A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202COV_SequenceA_GeneralInformation_53A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 86, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT202COV_SequenceA_GeneralInformation_53A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT202COV_SequenceA_GeneralInformation_53A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='53A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 89, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 89, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT202COV_SequenceA_GeneralInformation_53A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 90, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 90, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT202COV_SequenceA_GeneralInformation_53A_Type = MT202COV_SequenceA_GeneralInformation_53A_Type
Namespace.addCategoryObject('typeBinding', 'MT202COV_SequenceA_GeneralInformation_53A_Type', MT202COV_SequenceA_GeneralInformation_53A_Type)


# Complex type {http://www.w3schools.com}MT202COV_SequenceA_GeneralInformation_53B_Type with content type SIMPLE
class MT202COV_SequenceA_GeneralInformation_53B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT202COV_SequenceA_GeneralInformation_53B_Type with content type SIMPLE"""
    _TypeDefinition = MT202COV_SequenceA_GeneralInformation_53B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202COV_SequenceA_GeneralInformation_53B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 99, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT202COV_SequenceA_GeneralInformation_53B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT202COV_SequenceA_GeneralInformation_53B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='53B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 102, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 102, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT202COV_SequenceA_GeneralInformation_53B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 103, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 103, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT202COV_SequenceA_GeneralInformation_53B_Type = MT202COV_SequenceA_GeneralInformation_53B_Type
Namespace.addCategoryObject('typeBinding', 'MT202COV_SequenceA_GeneralInformation_53B_Type', MT202COV_SequenceA_GeneralInformation_53B_Type)


# Complex type {http://www.w3schools.com}MT202COV_SequenceA_GeneralInformation_53D_Type with content type SIMPLE
class MT202COV_SequenceA_GeneralInformation_53D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT202COV_SequenceA_GeneralInformation_53D_Type with content type SIMPLE"""
    _TypeDefinition = MT202COV_SequenceA_GeneralInformation_53D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202COV_SequenceA_GeneralInformation_53D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 112, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT202COV_SequenceA_GeneralInformation_53D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT202COV_SequenceA_GeneralInformation_53D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='53D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 115, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 115, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT202COV_SequenceA_GeneralInformation_53D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 116, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 116, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT202COV_SequenceA_GeneralInformation_53D_Type = MT202COV_SequenceA_GeneralInformation_53D_Type
Namespace.addCategoryObject('typeBinding', 'MT202COV_SequenceA_GeneralInformation_53D_Type', MT202COV_SequenceA_GeneralInformation_53D_Type)


# Complex type {http://www.w3schools.com}MT202COV_SequenceA_GeneralInformation_54A_Type with content type SIMPLE
class MT202COV_SequenceA_GeneralInformation_54A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT202COV_SequenceA_GeneralInformation_54A_Type with content type SIMPLE"""
    _TypeDefinition = MT202COV_SequenceA_GeneralInformation_54A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202COV_SequenceA_GeneralInformation_54A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 125, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT202COV_SequenceA_GeneralInformation_54A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT202COV_SequenceA_GeneralInformation_54A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='54A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 128, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 128, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT202COV_SequenceA_GeneralInformation_54A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 129, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 129, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT202COV_SequenceA_GeneralInformation_54A_Type = MT202COV_SequenceA_GeneralInformation_54A_Type
Namespace.addCategoryObject('typeBinding', 'MT202COV_SequenceA_GeneralInformation_54A_Type', MT202COV_SequenceA_GeneralInformation_54A_Type)


# Complex type {http://www.w3schools.com}MT202COV_SequenceA_GeneralInformation_54B_Type with content type SIMPLE
class MT202COV_SequenceA_GeneralInformation_54B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT202COV_SequenceA_GeneralInformation_54B_Type with content type SIMPLE"""
    _TypeDefinition = MT202COV_SequenceA_GeneralInformation_54B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202COV_SequenceA_GeneralInformation_54B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 138, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT202COV_SequenceA_GeneralInformation_54B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT202COV_SequenceA_GeneralInformation_54B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='54B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 141, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 141, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT202COV_SequenceA_GeneralInformation_54B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 142, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 142, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT202COV_SequenceA_GeneralInformation_54B_Type = MT202COV_SequenceA_GeneralInformation_54B_Type
Namespace.addCategoryObject('typeBinding', 'MT202COV_SequenceA_GeneralInformation_54B_Type', MT202COV_SequenceA_GeneralInformation_54B_Type)


# Complex type {http://www.w3schools.com}MT202COV_SequenceA_GeneralInformation_54D_Type with content type SIMPLE
class MT202COV_SequenceA_GeneralInformation_54D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT202COV_SequenceA_GeneralInformation_54D_Type with content type SIMPLE"""
    _TypeDefinition = MT202COV_SequenceA_GeneralInformation_54D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202COV_SequenceA_GeneralInformation_54D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 151, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT202COV_SequenceA_GeneralInformation_54D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT202COV_SequenceA_GeneralInformation_54D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='54D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 154, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 154, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT202COV_SequenceA_GeneralInformation_54D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 155, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 155, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT202COV_SequenceA_GeneralInformation_54D_Type = MT202COV_SequenceA_GeneralInformation_54D_Type
Namespace.addCategoryObject('typeBinding', 'MT202COV_SequenceA_GeneralInformation_54D_Type', MT202COV_SequenceA_GeneralInformation_54D_Type)


# Complex type {http://www.w3schools.com}MT202COV_SequenceA_GeneralInformation_56A_Type with content type SIMPLE
class MT202COV_SequenceA_GeneralInformation_56A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT202COV_SequenceA_GeneralInformation_56A_Type with content type SIMPLE"""
    _TypeDefinition = MT202COV_SequenceA_GeneralInformation_56A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202COV_SequenceA_GeneralInformation_56A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 164, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT202COV_SequenceA_GeneralInformation_56A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT202COV_SequenceA_GeneralInformation_56A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='56A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 167, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 167, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT202COV_SequenceA_GeneralInformation_56A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 168, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 168, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT202COV_SequenceA_GeneralInformation_56A_Type = MT202COV_SequenceA_GeneralInformation_56A_Type
Namespace.addCategoryObject('typeBinding', 'MT202COV_SequenceA_GeneralInformation_56A_Type', MT202COV_SequenceA_GeneralInformation_56A_Type)


# Complex type {http://www.w3schools.com}MT202COV_SequenceA_GeneralInformation_56D_Type with content type SIMPLE
class MT202COV_SequenceA_GeneralInformation_56D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT202COV_SequenceA_GeneralInformation_56D_Type with content type SIMPLE"""
    _TypeDefinition = MT202COV_SequenceA_GeneralInformation_56D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202COV_SequenceA_GeneralInformation_56D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 177, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT202COV_SequenceA_GeneralInformation_56D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT202COV_SequenceA_GeneralInformation_56D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='56D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 180, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 180, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT202COV_SequenceA_GeneralInformation_56D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 181, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 181, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT202COV_SequenceA_GeneralInformation_56D_Type = MT202COV_SequenceA_GeneralInformation_56D_Type
Namespace.addCategoryObject('typeBinding', 'MT202COV_SequenceA_GeneralInformation_56D_Type', MT202COV_SequenceA_GeneralInformation_56D_Type)


# Complex type {http://www.w3schools.com}MT202COV_SequenceA_GeneralInformation_57A_Type with content type SIMPLE
class MT202COV_SequenceA_GeneralInformation_57A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT202COV_SequenceA_GeneralInformation_57A_Type with content type SIMPLE"""
    _TypeDefinition = MT202COV_SequenceA_GeneralInformation_57A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202COV_SequenceA_GeneralInformation_57A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 190, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT202COV_SequenceA_GeneralInformation_57A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT202COV_SequenceA_GeneralInformation_57A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='57A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 193, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 193, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT202COV_SequenceA_GeneralInformation_57A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 194, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 194, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT202COV_SequenceA_GeneralInformation_57A_Type = MT202COV_SequenceA_GeneralInformation_57A_Type
Namespace.addCategoryObject('typeBinding', 'MT202COV_SequenceA_GeneralInformation_57A_Type', MT202COV_SequenceA_GeneralInformation_57A_Type)


# Complex type {http://www.w3schools.com}MT202COV_SequenceA_GeneralInformation_57B_Type with content type SIMPLE
class MT202COV_SequenceA_GeneralInformation_57B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT202COV_SequenceA_GeneralInformation_57B_Type with content type SIMPLE"""
    _TypeDefinition = MT202COV_SequenceA_GeneralInformation_57B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202COV_SequenceA_GeneralInformation_57B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 203, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT202COV_SequenceA_GeneralInformation_57B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT202COV_SequenceA_GeneralInformation_57B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='57B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 206, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 206, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT202COV_SequenceA_GeneralInformation_57B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 207, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 207, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT202COV_SequenceA_GeneralInformation_57B_Type = MT202COV_SequenceA_GeneralInformation_57B_Type
Namespace.addCategoryObject('typeBinding', 'MT202COV_SequenceA_GeneralInformation_57B_Type', MT202COV_SequenceA_GeneralInformation_57B_Type)


# Complex type {http://www.w3schools.com}MT202COV_SequenceA_GeneralInformation_57D_Type with content type SIMPLE
class MT202COV_SequenceA_GeneralInformation_57D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT202COV_SequenceA_GeneralInformation_57D_Type with content type SIMPLE"""
    _TypeDefinition = MT202COV_SequenceA_GeneralInformation_57D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202COV_SequenceA_GeneralInformation_57D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 216, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT202COV_SequenceA_GeneralInformation_57D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT202COV_SequenceA_GeneralInformation_57D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='57D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 219, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 219, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT202COV_SequenceA_GeneralInformation_57D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 220, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 220, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT202COV_SequenceA_GeneralInformation_57D_Type = MT202COV_SequenceA_GeneralInformation_57D_Type
Namespace.addCategoryObject('typeBinding', 'MT202COV_SequenceA_GeneralInformation_57D_Type', MT202COV_SequenceA_GeneralInformation_57D_Type)


# Complex type {http://www.w3schools.com}MT202COV_SequenceA_GeneralInformation_58A_Type with content type SIMPLE
class MT202COV_SequenceA_GeneralInformation_58A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT202COV_SequenceA_GeneralInformation_58A_Type with content type SIMPLE"""
    _TypeDefinition = MT202COV_SequenceA_GeneralInformation_58A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202COV_SequenceA_GeneralInformation_58A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 229, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT202COV_SequenceA_GeneralInformation_58A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT202COV_SequenceA_GeneralInformation_58A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='58A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 232, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 232, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT202COV_SequenceA_GeneralInformation_58A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 233, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 233, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT202COV_SequenceA_GeneralInformation_58A_Type = MT202COV_SequenceA_GeneralInformation_58A_Type
Namespace.addCategoryObject('typeBinding', 'MT202COV_SequenceA_GeneralInformation_58A_Type', MT202COV_SequenceA_GeneralInformation_58A_Type)


# Complex type {http://www.w3schools.com}MT202COV_SequenceA_GeneralInformation_58D_Type with content type SIMPLE
class MT202COV_SequenceA_GeneralInformation_58D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT202COV_SequenceA_GeneralInformation_58D_Type with content type SIMPLE"""
    _TypeDefinition = MT202COV_SequenceA_GeneralInformation_58D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202COV_SequenceA_GeneralInformation_58D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 242, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT202COV_SequenceA_GeneralInformation_58D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT202COV_SequenceA_GeneralInformation_58D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='58D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 245, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 245, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT202COV_SequenceA_GeneralInformation_58D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 246, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 246, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT202COV_SequenceA_GeneralInformation_58D_Type = MT202COV_SequenceA_GeneralInformation_58D_Type
Namespace.addCategoryObject('typeBinding', 'MT202COV_SequenceA_GeneralInformation_58D_Type', MT202COV_SequenceA_GeneralInformation_58D_Type)


# Complex type {http://www.w3schools.com}MT202COV_SequenceA_GeneralInformation_72_Type with content type SIMPLE
class MT202COV_SequenceA_GeneralInformation_72_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT202COV_SequenceA_GeneralInformation_72_Type with content type SIMPLE"""
    _TypeDefinition = MT202COV_SequenceA_GeneralInformation_72_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202COV_SequenceA_GeneralInformation_72_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 255, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT202COV_SequenceA_GeneralInformation_72_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT202COV_SequenceA_GeneralInformation_72_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='72')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 258, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 258, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT202COV_SequenceA_GeneralInformation_72_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 259, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 259, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT202COV_SequenceA_GeneralInformation_72_Type = MT202COV_SequenceA_GeneralInformation_72_Type
Namespace.addCategoryObject('typeBinding', 'MT202COV_SequenceA_GeneralInformation_72_Type', MT202COV_SequenceA_GeneralInformation_72_Type)


# Complex type {http://www.w3schools.com}MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50A_Type with content type SIMPLE
class MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50A_Type with content type SIMPLE"""
    _TypeDefinition = MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 268, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='50A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 271, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 271, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 272, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 272, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50A_Type = MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50A_Type
Namespace.addCategoryObject('typeBinding', 'MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50A_Type', MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50A_Type)


# Complex type {http://www.w3schools.com}MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50F_Type with content type SIMPLE
class MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50F_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50F_Type with content type SIMPLE"""
    _TypeDefinition = MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50F_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50F_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 281, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50F_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50F_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='50F')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 284, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 284, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50F_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 285, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 285, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50F_Type = MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50F_Type
Namespace.addCategoryObject('typeBinding', 'MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50F_Type', MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50F_Type)


# Complex type {http://www.w3schools.com}MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50K_Type with content type SIMPLE
class MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50K_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50K_Type with content type SIMPLE"""
    _TypeDefinition = MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50K_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50K_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 294, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50K_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50K_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='50K')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 297, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 297, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50K_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 298, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 298, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50K_Type = MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50K_Type
Namespace.addCategoryObject('typeBinding', 'MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50K_Type', MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50K_Type)


# Complex type {http://www.w3schools.com}MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_52A_Type with content type SIMPLE
class MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_52A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_52A_Type with content type SIMPLE"""
    _TypeDefinition = MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_52A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_52A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 307, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_52A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_52A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='52A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 310, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 310, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_52A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 311, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 311, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_52A_Type = MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_52A_Type
Namespace.addCategoryObject('typeBinding', 'MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_52A_Type', MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_52A_Type)


# Complex type {http://www.w3schools.com}MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_52D_Type with content type SIMPLE
class MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_52D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_52D_Type with content type SIMPLE"""
    _TypeDefinition = MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_52D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_52D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 320, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_52D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_52D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='52D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 323, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 323, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_52D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 324, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 324, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_52D_Type = MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_52D_Type
Namespace.addCategoryObject('typeBinding', 'MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_52D_Type', MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_52D_Type)


# Complex type {http://www.w3schools.com}MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_56A_Type with content type SIMPLE
class MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_56A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_56A_Type with content type SIMPLE"""
    _TypeDefinition = MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_56A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_56A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 333, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_56A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_56A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='56A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 336, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 336, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_56A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 337, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 337, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_56A_Type = MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_56A_Type
Namespace.addCategoryObject('typeBinding', 'MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_56A_Type', MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_56A_Type)


# Complex type {http://www.w3schools.com}MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_56C_Type with content type SIMPLE
class MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_56C_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_56C_Type with content type SIMPLE"""
    _TypeDefinition = MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_56C_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_56C_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 346, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_56C_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_56C_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='56C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 349, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 349, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_56C_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 350, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 350, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_56C_Type = MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_56C_Type
Namespace.addCategoryObject('typeBinding', 'MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_56C_Type', MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_56C_Type)


# Complex type {http://www.w3schools.com}MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_56D_Type with content type SIMPLE
class MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_56D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_56D_Type with content type SIMPLE"""
    _TypeDefinition = MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_56D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_56D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 359, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_56D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_56D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='56D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 362, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 362, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_56D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 363, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 363, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_56D_Type = MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_56D_Type
Namespace.addCategoryObject('typeBinding', 'MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_56D_Type', MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_56D_Type)


# Complex type {http://www.w3schools.com}MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57A_Type with content type SIMPLE
class MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57A_Type with content type SIMPLE"""
    _TypeDefinition = MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 372, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='57A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 375, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 375, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 376, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 376, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57A_Type = MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57A_Type
Namespace.addCategoryObject('typeBinding', 'MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57A_Type', MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57A_Type)


# Complex type {http://www.w3schools.com}MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57B_Type with content type SIMPLE
class MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57B_Type with content type SIMPLE"""
    _TypeDefinition = MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 385, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='57B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 388, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 388, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 389, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 389, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57B_Type = MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57B_Type
Namespace.addCategoryObject('typeBinding', 'MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57B_Type', MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57B_Type)


# Complex type {http://www.w3schools.com}MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57C_Type with content type SIMPLE
class MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57C_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57C_Type with content type SIMPLE"""
    _TypeDefinition = MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57C_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57C_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 398, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57C_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57C_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='57C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 401, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 401, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57C_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 402, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 402, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57C_Type = MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57C_Type
Namespace.addCategoryObject('typeBinding', 'MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57C_Type', MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57C_Type)


# Complex type {http://www.w3schools.com}MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57D_Type with content type SIMPLE
class MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57D_Type with content type SIMPLE"""
    _TypeDefinition = MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 411, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='57D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 414, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 414, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 415, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 415, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57D_Type = MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57D_Type
Namespace.addCategoryObject('typeBinding', 'MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57D_Type', MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57D_Type)


# Complex type {http://www.w3schools.com}MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59_Type with content type SIMPLE
class MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59_Type with content type SIMPLE"""
    _TypeDefinition = MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 424, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='59')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 427, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 427, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 428, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 428, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59_Type = MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59_Type
Namespace.addCategoryObject('typeBinding', 'MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59_Type', MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59_Type)


# Complex type {http://www.w3schools.com}MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59A_Type with content type SIMPLE
class MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59A_Type with content type SIMPLE"""
    _TypeDefinition = MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 437, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='59A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 440, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 440, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 441, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 441, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59A_Type = MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59A_Type
Namespace.addCategoryObject('typeBinding', 'MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59A_Type', MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59A_Type)


# Complex type {http://www.w3schools.com}MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59F_Type with content type SIMPLE
class MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59F_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59F_Type with content type SIMPLE"""
    _TypeDefinition = MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59F_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59F_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 450, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59F_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59F_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='59F')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 453, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 453, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59F_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 454, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 454, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59F_Type = MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59F_Type
Namespace.addCategoryObject('typeBinding', 'MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59F_Type', MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59F_Type)


# Complex type {http://www.w3schools.com}MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_70_Type with content type SIMPLE
class MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_70_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_70_Type with content type SIMPLE"""
    _TypeDefinition = MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_70_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_70_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 463, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_70_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_70_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='70')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 466, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 466, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_70_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 467, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 467, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_70_Type = MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_70_Type
Namespace.addCategoryObject('typeBinding', 'MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_70_Type', MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_70_Type)


# Complex type {http://www.w3schools.com}MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_72_Type with content type SIMPLE
class MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_72_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_72_Type with content type SIMPLE"""
    _TypeDefinition = MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_72_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_72_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 476, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_72_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_72_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='72')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 479, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 479, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_72_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 480, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 480, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_72_Type = MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_72_Type
Namespace.addCategoryObject('typeBinding', 'MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_72_Type', MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_72_Type)


# Complex type {http://www.w3schools.com}MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_33B_Type with content type SIMPLE
class MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_33B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_33B_Type with content type SIMPLE"""
    _TypeDefinition = MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_33B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_33B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 489, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_33B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_33B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='33B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 492, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 492, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_33B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 493, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 493, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_33B_Type = MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_33B_Type
Namespace.addCategoryObject('typeBinding', 'MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_33B_Type', MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_33B_Type)


MT202COV = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'MT202COV'), CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 565, 1))
Namespace.addCategoryObject('elementBinding', MT202COV.name().localName(), MT202COV)



MT202COV_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TransactionReferenceNumber'), MT202COV_SequenceA_GeneralInformation_20_Type, scope=MT202COV_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 499, 3)))

MT202COV_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'RelatedReference'), MT202COV_SequenceA_GeneralInformation_21_Type, scope=MT202COV_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 500, 3)))

MT202COV_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TimeIndication'), MT202COV_SequenceA_GeneralInformation_13C_Type, scope=MT202COV_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 501, 3)))

MT202COV_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DateCurrencyAmount'), MT202COV_SequenceA_GeneralInformation_32A_Type, scope=MT202COV_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 502, 3)))

MT202COV_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'OrderingInstitution_A'), MT202COV_SequenceA_GeneralInformation_52A_Type, scope=MT202COV_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 504, 4)))

MT202COV_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'OrderingInstitution_D'), MT202COV_SequenceA_GeneralInformation_52D_Type, scope=MT202COV_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 505, 4)))

MT202COV_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SendersCorrespondent_A'), MT202COV_SequenceA_GeneralInformation_53A_Type, scope=MT202COV_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 508, 4)))

MT202COV_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SendersCorrespondent_B'), MT202COV_SequenceA_GeneralInformation_53B_Type, scope=MT202COV_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 509, 4)))

MT202COV_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SendersCorrespondent_D'), MT202COV_SequenceA_GeneralInformation_53D_Type, scope=MT202COV_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 510, 4)))

MT202COV_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ReceiversCorrespondent_A'), MT202COV_SequenceA_GeneralInformation_54A_Type, scope=MT202COV_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 513, 4)))

MT202COV_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ReceiversCorrespondent_B'), MT202COV_SequenceA_GeneralInformation_54B_Type, scope=MT202COV_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 514, 4)))

MT202COV_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ReceiversCorrespondent_D'), MT202COV_SequenceA_GeneralInformation_54D_Type, scope=MT202COV_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 515, 4)))

MT202COV_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Intermedairy_A'), MT202COV_SequenceA_GeneralInformation_56A_Type, scope=MT202COV_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 518, 4)))

MT202COV_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Intermedairy_D'), MT202COV_SequenceA_GeneralInformation_56D_Type, scope=MT202COV_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 519, 4)))

MT202COV_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'AccountWithInstitution_A'), MT202COV_SequenceA_GeneralInformation_57A_Type, scope=MT202COV_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 522, 4)))

MT202COV_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'AccountWithInstitution_B'), MT202COV_SequenceA_GeneralInformation_57B_Type, scope=MT202COV_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 523, 4)))

MT202COV_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'AccountWithInstitution_D'), MT202COV_SequenceA_GeneralInformation_57D_Type, scope=MT202COV_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 524, 4)))

MT202COV_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_A'), MT202COV_SequenceA_GeneralInformation_58A_Type, scope=MT202COV_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 527, 4)))

MT202COV_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_D'), MT202COV_SequenceA_GeneralInformation_58D_Type, scope=MT202COV_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 528, 4)))

MT202COV_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SenderToReceiverInformation'), MT202COV_SequenceA_GeneralInformation_72_Type, scope=MT202COV_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 530, 3)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 501, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 503, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 504, 4))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 505, 4))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 507, 3))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 508, 4))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 509, 4))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 510, 4))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 512, 3))
    counters.add(cc_8)
    cc_9 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 513, 4))
    counters.add(cc_9)
    cc_10 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 514, 4))
    counters.add(cc_10)
    cc_11 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 515, 4))
    counters.add(cc_11)
    cc_12 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 517, 3))
    counters.add(cc_12)
    cc_13 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 518, 4))
    counters.add(cc_13)
    cc_14 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 519, 4))
    counters.add(cc_14)
    cc_15 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 521, 3))
    counters.add(cc_15)
    cc_16 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 522, 4))
    counters.add(cc_16)
    cc_17 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 523, 4))
    counters.add(cc_17)
    cc_18 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 524, 4))
    counters.add(cc_18)
    cc_19 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 530, 3))
    counters.add(cc_19)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT202COV_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'TransactionReferenceNumber')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 499, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT202COV_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'RelatedReference')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 500, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT202COV_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'TimeIndication')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 501, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT202COV_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DateCurrencyAmount')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 502, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT202COV_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'OrderingInstitution_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 504, 4))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT202COV_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'OrderingInstitution_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 505, 4))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT202COV_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SendersCorrespondent_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 508, 4))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT202COV_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SendersCorrespondent_B')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 509, 4))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT202COV_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SendersCorrespondent_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 510, 4))
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT202COV_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ReceiversCorrespondent_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 513, 4))
    st_9 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT202COV_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ReceiversCorrespondent_B')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 514, 4))
    st_10 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT202COV_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ReceiversCorrespondent_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 515, 4))
    st_11 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT202COV_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Intermedairy_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 518, 4))
    st_12 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_12)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT202COV_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Intermedairy_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 519, 4))
    st_13 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_13)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT202COV_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'AccountWithInstitution_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 522, 4))
    st_14 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_14)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT202COV_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'AccountWithInstitution_B')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 523, 4))
    st_15 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_15)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT202COV_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'AccountWithInstitution_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 524, 4))
    st_16 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_16)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT202COV_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 527, 4))
    st_17 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_17)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT202COV_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 528, 4))
    st_18 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_18)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_19, False))
    symbol = pyxb.binding.content.ElementUse(MT202COV_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SenderToReceiverInformation')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 530, 3))
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
MT202COV_SequenceA_GeneralInformation._Automaton = _BuildAutomaton()




MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'OrderingCustomer_A'), MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50A_Type, scope=MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 536, 4)))

MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'OrderingCustomer_F'), MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50F_Type, scope=MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 537, 4)))

MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'OrderingCustomer_K'), MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_50K_Type, scope=MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 538, 4)))

MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'OrderingInstitution_A'), MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_52A_Type, scope=MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 541, 4)))

MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'OrderingInstitution_D'), MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_52D_Type, scope=MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 542, 4)))

MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'IntermediaryInstitution_A'), MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_56A_Type, scope=MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 545, 4)))

MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'IntermediaryInstitution_C'), MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_56C_Type, scope=MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 546, 4)))

MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'IntermediaryInstitution_D'), MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_56D_Type, scope=MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 547, 4)))

MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'AccountWithInstitution_A'), MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57A_Type, scope=MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 550, 4)))

MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'AccountWithInstitution_B'), MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57B_Type, scope=MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 551, 4)))

MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'AccountWithInstitution_C'), MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57C_Type, scope=MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 552, 4)))

MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'AccountWithInstitution_D'), MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_57D_Type, scope=MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 553, 4)))

MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryCustomer'), MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59_Type, scope=MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 556, 4)))

MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryCustomer_A'), MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59A_Type, scope=MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 557, 4)))

MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryCustomer_F'), MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_59F_Type, scope=MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 558, 4)))

MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'RemittanceInformation'), MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_70_Type, scope=MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 560, 3)))

MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SenderToReceiverInformation'), MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_72_Type, scope=MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 561, 3)))

MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CurrencyInstructedAmount'), MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails_33B_Type, scope=MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 562, 3)))

def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 540, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 541, 4))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 542, 4))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 544, 3))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 545, 4))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 546, 4))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 547, 4))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 549, 3))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 550, 4))
    counters.add(cc_8)
    cc_9 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 551, 4))
    counters.add(cc_9)
    cc_10 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 552, 4))
    counters.add(cc_10)
    cc_11 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 553, 4))
    counters.add(cc_11)
    cc_12 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 560, 3))
    counters.add(cc_12)
    cc_13 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 561, 3))
    counters.add(cc_13)
    cc_14 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 562, 3))
    counters.add(cc_14)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'OrderingCustomer_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 536, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'OrderingCustomer_F')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 537, 4))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'OrderingCustomer_K')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 538, 4))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'OrderingInstitution_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 541, 4))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'OrderingInstitution_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 542, 4))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'IntermediaryInstitution_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 545, 4))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'IntermediaryInstitution_C')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 546, 4))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'IntermediaryInstitution_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 547, 4))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'AccountWithInstitution_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 550, 4))
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'AccountWithInstitution_B')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 551, 4))
    st_9 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'AccountWithInstitution_C')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 552, 4))
    st_10 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'AccountWithInstitution_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 553, 4))
    st_11 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryCustomer')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 556, 4))
    st_12 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_12)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryCustomer_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 557, 4))
    st_13 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_13)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryCustomer_F')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 558, 4))
    st_14 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_14)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_12, False))
    symbol = pyxb.binding.content.ElementUse(MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'RemittanceInformation')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 560, 3))
    st_15 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_15)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_13, False))
    symbol = pyxb.binding.content.ElementUse(MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SenderToReceiverInformation')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 561, 3))
    st_16 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_16)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_14, False))
    symbol = pyxb.binding.content.ElementUse(MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CurrencyInstructedAmount')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 562, 3))
    st_17 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_17)
    transitions = []
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
    st_0._set_transitionSet(transitions)
    transitions = []
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
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True),
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, True) ]))
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
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_1, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, True) ]))
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
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_2, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_3, True),
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_3, True),
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_3, True),
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_3, False),
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_3, False),
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_3, False),
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_3, False),
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_3, False),
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_3, False),
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_3, False),
        fac.UpdateInstruction(cc_4, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_3, True),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_3, True),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_5, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_3, True),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_3, False),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_3, False),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_3, False),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_3, False),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_3, False),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_3, False),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_3, False),
        fac.UpdateInstruction(cc_5, False) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_3, True),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_3, True),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_3, True),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_6, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_3, False),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_3, False),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_3, False),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_3, False),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_3, False),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_3, False),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_3, False),
        fac.UpdateInstruction(cc_6, False) ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_7, True),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_8, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_7, True),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_7, True),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_7, True),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_7, False),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_7, False),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_7, False),
        fac.UpdateInstruction(cc_8, False) ]))
    st_8._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_7, True),
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_7, True),
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_9, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_7, True),
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_7, True),
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_7, False),
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_7, False),
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_7, False),
        fac.UpdateInstruction(cc_9, False) ]))
    st_9._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_7, True),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_7, True),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_7, True),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_10, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_7, True),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_7, False),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_7, False),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_7, False),
        fac.UpdateInstruction(cc_10, False) ]))
    st_10._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_7, True),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_7, True),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_7, True),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_7, True),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_11, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_7, False),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_7, False),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_7, False),
        fac.UpdateInstruction(cc_11, False) ]))
    st_11._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_15, [
         ]))
    transitions.append(fac.Transition(st_16, [
         ]))
    transitions.append(fac.Transition(st_17, [
         ]))
    st_12._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_15, [
         ]))
    transitions.append(fac.Transition(st_16, [
         ]))
    transitions.append(fac.Transition(st_17, [
         ]))
    st_13._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_15, [
         ]))
    transitions.append(fac.Transition(st_16, [
         ]))
    transitions.append(fac.Transition(st_17, [
         ]))
    st_14._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_12, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_12, False) ]))
    st_15._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_13, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_13, False) ]))
    st_16._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_14, True) ]))
    st_17._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails._Automaton = _BuildAutomaton_()




CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SequenceA_GeneralInformation'), MT202COV_SequenceA_GeneralInformation, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 568, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SequenceB_UnderlyingCustomerCreditTransferDetails'), MT202COV_SequenceB_UnderlyingCustomerCreditTransferDetails, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 569, 4)))

def _BuildAutomaton_2 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_2
    del _BuildAutomaton_2
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SequenceA_GeneralInformation')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 568, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SequenceB_UnderlyingCustomerCreditTransferDetails')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT202COV.xsd', 569, 4))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON._Automaton = _BuildAutomaton_2()


