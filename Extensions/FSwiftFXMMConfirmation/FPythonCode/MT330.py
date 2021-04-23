# C:\Projects\Code\SwiftMessagingSolution_Python3\base\extensions\SwiftIntegration\Utilities\TemplateFiles\MT330.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:96afad3d20bbfe8d040a1a097fa388d9fecd10e3
# Generated 2019-11-07 12:38:31.688431 by PyXB version 1.2.6 using Python 3.7.4.final.0
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
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:67c4b012-012d-11ea-8958-509a4c321f2f')

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


# Atomic simple type: {http://www.w3schools.com}MT330_SequenceA_GeneralInformation_20_Type_Pattern
class MT330_SequenceA_GeneralInformation_20_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceA_GeneralInformation_20_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 3, 1)
    _Documentation = None
MT330_SequenceA_GeneralInformation_20_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceA_GeneralInformation_20_Type_Pattern._CF_pattern.addPattern(pattern="([^/]([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,16}[^/])")
MT330_SequenceA_GeneralInformation_20_Type_Pattern._InitializeFacetMap(MT330_SequenceA_GeneralInformation_20_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceA_GeneralInformation_20_Type_Pattern', MT330_SequenceA_GeneralInformation_20_Type_Pattern)
_module_typeBindings.MT330_SequenceA_GeneralInformation_20_Type_Pattern = MT330_SequenceA_GeneralInformation_20_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceA_GeneralInformation_21_Type_Pattern
class MT330_SequenceA_GeneralInformation_21_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceA_GeneralInformation_21_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 16, 1)
    _Documentation = None
MT330_SequenceA_GeneralInformation_21_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceA_GeneralInformation_21_Type_Pattern._CF_pattern.addPattern(pattern="([^/]([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,16}[^/])")
MT330_SequenceA_GeneralInformation_21_Type_Pattern._InitializeFacetMap(MT330_SequenceA_GeneralInformation_21_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceA_GeneralInformation_21_Type_Pattern', MT330_SequenceA_GeneralInformation_21_Type_Pattern)
_module_typeBindings.MT330_SequenceA_GeneralInformation_21_Type_Pattern = MT330_SequenceA_GeneralInformation_21_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceA_GeneralInformation_22A_Type_Pattern
class MT330_SequenceA_GeneralInformation_22A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceA_GeneralInformation_22A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 29, 1)
    _Documentation = None
MT330_SequenceA_GeneralInformation_22A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceA_GeneralInformation_22A_Type_Pattern._CF_pattern.addPattern(pattern='((AMND|CANC|DUPL|NEWT))')
MT330_SequenceA_GeneralInformation_22A_Type_Pattern._InitializeFacetMap(MT330_SequenceA_GeneralInformation_22A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceA_GeneralInformation_22A_Type_Pattern', MT330_SequenceA_GeneralInformation_22A_Type_Pattern)
_module_typeBindings.MT330_SequenceA_GeneralInformation_22A_Type_Pattern = MT330_SequenceA_GeneralInformation_22A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceA_GeneralInformation_94A_Type_Pattern
class MT330_SequenceA_GeneralInformation_94A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceA_GeneralInformation_94A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 42, 1)
    _Documentation = None
MT330_SequenceA_GeneralInformation_94A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceA_GeneralInformation_94A_Type_Pattern._CF_pattern.addPattern(pattern='((AGNT|BILA))')
MT330_SequenceA_GeneralInformation_94A_Type_Pattern._InitializeFacetMap(MT330_SequenceA_GeneralInformation_94A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceA_GeneralInformation_94A_Type_Pattern', MT330_SequenceA_GeneralInformation_94A_Type_Pattern)
_module_typeBindings.MT330_SequenceA_GeneralInformation_94A_Type_Pattern = MT330_SequenceA_GeneralInformation_94A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceA_GeneralInformation_22B_Type_Pattern
class MT330_SequenceA_GeneralInformation_22B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceA_GeneralInformation_22B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 55, 1)
    _Documentation = None
MT330_SequenceA_GeneralInformation_22B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceA_GeneralInformation_22B_Type_Pattern._CF_pattern.addPattern(pattern='((CHNG|CINT|CONF|SETT))')
MT330_SequenceA_GeneralInformation_22B_Type_Pattern._InitializeFacetMap(MT330_SequenceA_GeneralInformation_22B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceA_GeneralInformation_22B_Type_Pattern', MT330_SequenceA_GeneralInformation_22B_Type_Pattern)
_module_typeBindings.MT330_SequenceA_GeneralInformation_22B_Type_Pattern = MT330_SequenceA_GeneralInformation_22B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceA_GeneralInformation_22C_Type_Pattern
class MT330_SequenceA_GeneralInformation_22C_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceA_GeneralInformation_22C_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 68, 1)
    _Documentation = None
MT330_SequenceA_GeneralInformation_22C_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceA_GeneralInformation_22C_Type_Pattern._CF_pattern.addPattern(pattern='([A-Z]{4}[A-Z0-9]{2}[0-9]{4}[A-Z]{4}[A-Z0-9]{2})')
MT330_SequenceA_GeneralInformation_22C_Type_Pattern._InitializeFacetMap(MT330_SequenceA_GeneralInformation_22C_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceA_GeneralInformation_22C_Type_Pattern', MT330_SequenceA_GeneralInformation_22C_Type_Pattern)
_module_typeBindings.MT330_SequenceA_GeneralInformation_22C_Type_Pattern = MT330_SequenceA_GeneralInformation_22C_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceA_GeneralInformation_21N_Type_Pattern
class MT330_SequenceA_GeneralInformation_21N_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceA_GeneralInformation_21N_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 81, 1)
    _Documentation = None
MT330_SequenceA_GeneralInformation_21N_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceA_GeneralInformation_21N_Type_Pattern._CF_pattern.addPattern(pattern="(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,16})")
MT330_SequenceA_GeneralInformation_21N_Type_Pattern._InitializeFacetMap(MT330_SequenceA_GeneralInformation_21N_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceA_GeneralInformation_21N_Type_Pattern', MT330_SequenceA_GeneralInformation_21N_Type_Pattern)
_module_typeBindings.MT330_SequenceA_GeneralInformation_21N_Type_Pattern = MT330_SequenceA_GeneralInformation_21N_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceA_GeneralInformation_82A_Type_Pattern
class MT330_SequenceA_GeneralInformation_82A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceA_GeneralInformation_82A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 94, 1)
    _Documentation = None
MT330_SequenceA_GeneralInformation_82A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceA_GeneralInformation_82A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT330_SequenceA_GeneralInformation_82A_Type_Pattern._InitializeFacetMap(MT330_SequenceA_GeneralInformation_82A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceA_GeneralInformation_82A_Type_Pattern', MT330_SequenceA_GeneralInformation_82A_Type_Pattern)
_module_typeBindings.MT330_SequenceA_GeneralInformation_82A_Type_Pattern = MT330_SequenceA_GeneralInformation_82A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceA_GeneralInformation_82D_Type_Pattern
class MT330_SequenceA_GeneralInformation_82D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceA_GeneralInformation_82D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 107, 1)
    _Documentation = None
MT330_SequenceA_GeneralInformation_82D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceA_GeneralInformation_82D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT330_SequenceA_GeneralInformation_82D_Type_Pattern._InitializeFacetMap(MT330_SequenceA_GeneralInformation_82D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceA_GeneralInformation_82D_Type_Pattern', MT330_SequenceA_GeneralInformation_82D_Type_Pattern)
_module_typeBindings.MT330_SequenceA_GeneralInformation_82D_Type_Pattern = MT330_SequenceA_GeneralInformation_82D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceA_GeneralInformation_82J_Type_Pattern
class MT330_SequenceA_GeneralInformation_82J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceA_GeneralInformation_82J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 120, 1)
    _Documentation = None
MT330_SequenceA_GeneralInformation_82J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceA_GeneralInformation_82J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT330_SequenceA_GeneralInformation_82J_Type_Pattern._InitializeFacetMap(MT330_SequenceA_GeneralInformation_82J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceA_GeneralInformation_82J_Type_Pattern', MT330_SequenceA_GeneralInformation_82J_Type_Pattern)
_module_typeBindings.MT330_SequenceA_GeneralInformation_82J_Type_Pattern = MT330_SequenceA_GeneralInformation_82J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceA_GeneralInformation_87A_Type_Pattern
class MT330_SequenceA_GeneralInformation_87A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceA_GeneralInformation_87A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 133, 1)
    _Documentation = None
MT330_SequenceA_GeneralInformation_87A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceA_GeneralInformation_87A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT330_SequenceA_GeneralInformation_87A_Type_Pattern._InitializeFacetMap(MT330_SequenceA_GeneralInformation_87A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceA_GeneralInformation_87A_Type_Pattern', MT330_SequenceA_GeneralInformation_87A_Type_Pattern)
_module_typeBindings.MT330_SequenceA_GeneralInformation_87A_Type_Pattern = MT330_SequenceA_GeneralInformation_87A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceA_GeneralInformation_87D_Type_Pattern
class MT330_SequenceA_GeneralInformation_87D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceA_GeneralInformation_87D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 146, 1)
    _Documentation = None
MT330_SequenceA_GeneralInformation_87D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceA_GeneralInformation_87D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT330_SequenceA_GeneralInformation_87D_Type_Pattern._InitializeFacetMap(MT330_SequenceA_GeneralInformation_87D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceA_GeneralInformation_87D_Type_Pattern', MT330_SequenceA_GeneralInformation_87D_Type_Pattern)
_module_typeBindings.MT330_SequenceA_GeneralInformation_87D_Type_Pattern = MT330_SequenceA_GeneralInformation_87D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceA_GeneralInformation_87J_Type_Pattern
class MT330_SequenceA_GeneralInformation_87J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceA_GeneralInformation_87J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 159, 1)
    _Documentation = None
MT330_SequenceA_GeneralInformation_87J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceA_GeneralInformation_87J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT330_SequenceA_GeneralInformation_87J_Type_Pattern._InitializeFacetMap(MT330_SequenceA_GeneralInformation_87J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceA_GeneralInformation_87J_Type_Pattern', MT330_SequenceA_GeneralInformation_87J_Type_Pattern)
_module_typeBindings.MT330_SequenceA_GeneralInformation_87J_Type_Pattern = MT330_SequenceA_GeneralInformation_87J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceA_GeneralInformation_83A_Type_Pattern
class MT330_SequenceA_GeneralInformation_83A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceA_GeneralInformation_83A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 172, 1)
    _Documentation = None
MT330_SequenceA_GeneralInformation_83A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceA_GeneralInformation_83A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT330_SequenceA_GeneralInformation_83A_Type_Pattern._InitializeFacetMap(MT330_SequenceA_GeneralInformation_83A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceA_GeneralInformation_83A_Type_Pattern', MT330_SequenceA_GeneralInformation_83A_Type_Pattern)
_module_typeBindings.MT330_SequenceA_GeneralInformation_83A_Type_Pattern = MT330_SequenceA_GeneralInformation_83A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceA_GeneralInformation_83D_Type_Pattern
class MT330_SequenceA_GeneralInformation_83D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceA_GeneralInformation_83D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 185, 1)
    _Documentation = None
MT330_SequenceA_GeneralInformation_83D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceA_GeneralInformation_83D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT330_SequenceA_GeneralInformation_83D_Type_Pattern._InitializeFacetMap(MT330_SequenceA_GeneralInformation_83D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceA_GeneralInformation_83D_Type_Pattern', MT330_SequenceA_GeneralInformation_83D_Type_Pattern)
_module_typeBindings.MT330_SequenceA_GeneralInformation_83D_Type_Pattern = MT330_SequenceA_GeneralInformation_83D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceA_GeneralInformation_83J_Type_Pattern
class MT330_SequenceA_GeneralInformation_83J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceA_GeneralInformation_83J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 198, 1)
    _Documentation = None
MT330_SequenceA_GeneralInformation_83J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceA_GeneralInformation_83J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT330_SequenceA_GeneralInformation_83J_Type_Pattern._InitializeFacetMap(MT330_SequenceA_GeneralInformation_83J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceA_GeneralInformation_83J_Type_Pattern', MT330_SequenceA_GeneralInformation_83J_Type_Pattern)
_module_typeBindings.MT330_SequenceA_GeneralInformation_83J_Type_Pattern = MT330_SequenceA_GeneralInformation_83J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceA_GeneralInformation_77D_Type_Pattern
class MT330_SequenceA_GeneralInformation_77D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceA_GeneralInformation_77D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 211, 1)
    _Documentation = None
MT330_SequenceA_GeneralInformation_77D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceA_GeneralInformation_77D_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,6})")
MT330_SequenceA_GeneralInformation_77D_Type_Pattern._InitializeFacetMap(MT330_SequenceA_GeneralInformation_77D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceA_GeneralInformation_77D_Type_Pattern', MT330_SequenceA_GeneralInformation_77D_Type_Pattern)
_module_typeBindings.MT330_SequenceA_GeneralInformation_77D_Type_Pattern = MT330_SequenceA_GeneralInformation_77D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceB_TransactionDetails_17R_Type_Pattern
class MT330_SequenceB_TransactionDetails_17R_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceB_TransactionDetails_17R_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 224, 1)
    _Documentation = None
MT330_SequenceB_TransactionDetails_17R_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceB_TransactionDetails_17R_Type_Pattern._CF_pattern.addPattern(pattern='((B|L))')
MT330_SequenceB_TransactionDetails_17R_Type_Pattern._InitializeFacetMap(MT330_SequenceB_TransactionDetails_17R_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceB_TransactionDetails_17R_Type_Pattern', MT330_SequenceB_TransactionDetails_17R_Type_Pattern)
_module_typeBindings.MT330_SequenceB_TransactionDetails_17R_Type_Pattern = MT330_SequenceB_TransactionDetails_17R_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceB_TransactionDetails_30T_Type_Pattern
class MT330_SequenceB_TransactionDetails_30T_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceB_TransactionDetails_30T_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 237, 1)
    _Documentation = None
MT330_SequenceB_TransactionDetails_30T_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceB_TransactionDetails_30T_Type_Pattern._CF_pattern.addPattern(pattern='([0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))')
MT330_SequenceB_TransactionDetails_30T_Type_Pattern._InitializeFacetMap(MT330_SequenceB_TransactionDetails_30T_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceB_TransactionDetails_30T_Type_Pattern', MT330_SequenceB_TransactionDetails_30T_Type_Pattern)
_module_typeBindings.MT330_SequenceB_TransactionDetails_30T_Type_Pattern = MT330_SequenceB_TransactionDetails_30T_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceB_TransactionDetails_30V_Type_Pattern
class MT330_SequenceB_TransactionDetails_30V_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceB_TransactionDetails_30V_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 250, 1)
    _Documentation = None
MT330_SequenceB_TransactionDetails_30V_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceB_TransactionDetails_30V_Type_Pattern._CF_pattern.addPattern(pattern='([0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))')
MT330_SequenceB_TransactionDetails_30V_Type_Pattern._InitializeFacetMap(MT330_SequenceB_TransactionDetails_30V_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceB_TransactionDetails_30V_Type_Pattern', MT330_SequenceB_TransactionDetails_30V_Type_Pattern)
_module_typeBindings.MT330_SequenceB_TransactionDetails_30V_Type_Pattern = MT330_SequenceB_TransactionDetails_30V_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceB_TransactionDetails_38A_Type_Pattern
class MT330_SequenceB_TransactionDetails_38A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceB_TransactionDetails_38A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 263, 1)
    _Documentation = None
MT330_SequenceB_TransactionDetails_38A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceB_TransactionDetails_38A_Type_Pattern._CF_pattern.addPattern(pattern='([0-9]{1,3})')
MT330_SequenceB_TransactionDetails_38A_Type_Pattern._InitializeFacetMap(MT330_SequenceB_TransactionDetails_38A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceB_TransactionDetails_38A_Type_Pattern', MT330_SequenceB_TransactionDetails_38A_Type_Pattern)
_module_typeBindings.MT330_SequenceB_TransactionDetails_38A_Type_Pattern = MT330_SequenceB_TransactionDetails_38A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceB_TransactionDetails_32B_Type_Pattern
class MT330_SequenceB_TransactionDetails_32B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceB_TransactionDetails_32B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 276, 1)
    _Documentation = None
MT330_SequenceB_TransactionDetails_32B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceB_TransactionDetails_32B_Type_Pattern._CF_pattern.addPattern(pattern='((AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})')
MT330_SequenceB_TransactionDetails_32B_Type_Pattern._InitializeFacetMap(MT330_SequenceB_TransactionDetails_32B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceB_TransactionDetails_32B_Type_Pattern', MT330_SequenceB_TransactionDetails_32B_Type_Pattern)
_module_typeBindings.MT330_SequenceB_TransactionDetails_32B_Type_Pattern = MT330_SequenceB_TransactionDetails_32B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceB_TransactionDetails_32H_Type_Pattern
class MT330_SequenceB_TransactionDetails_32H_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceB_TransactionDetails_32H_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 289, 1)
    _Documentation = None
MT330_SequenceB_TransactionDetails_32H_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceB_TransactionDetails_32H_Type_Pattern._CF_pattern.addPattern(pattern='((N)?(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})')
MT330_SequenceB_TransactionDetails_32H_Type_Pattern._InitializeFacetMap(MT330_SequenceB_TransactionDetails_32H_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceB_TransactionDetails_32H_Type_Pattern', MT330_SequenceB_TransactionDetails_32H_Type_Pattern)
_module_typeBindings.MT330_SequenceB_TransactionDetails_32H_Type_Pattern = MT330_SequenceB_TransactionDetails_32H_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceB_TransactionDetails_30X_Type_Pattern
class MT330_SequenceB_TransactionDetails_30X_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceB_TransactionDetails_30X_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 302, 1)
    _Documentation = None
MT330_SequenceB_TransactionDetails_30X_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceB_TransactionDetails_30X_Type_Pattern._CF_pattern.addPattern(pattern='([0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))')
MT330_SequenceB_TransactionDetails_30X_Type_Pattern._InitializeFacetMap(MT330_SequenceB_TransactionDetails_30X_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceB_TransactionDetails_30X_Type_Pattern', MT330_SequenceB_TransactionDetails_30X_Type_Pattern)
_module_typeBindings.MT330_SequenceB_TransactionDetails_30X_Type_Pattern = MT330_SequenceB_TransactionDetails_30X_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceB_TransactionDetails_34E_Type_Pattern
class MT330_SequenceB_TransactionDetails_34E_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceB_TransactionDetails_34E_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 315, 1)
    _Documentation = None
MT330_SequenceB_TransactionDetails_34E_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceB_TransactionDetails_34E_Type_Pattern._CF_pattern.addPattern(pattern='((N)?(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})')
MT330_SequenceB_TransactionDetails_34E_Type_Pattern._InitializeFacetMap(MT330_SequenceB_TransactionDetails_34E_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceB_TransactionDetails_34E_Type_Pattern', MT330_SequenceB_TransactionDetails_34E_Type_Pattern)
_module_typeBindings.MT330_SequenceB_TransactionDetails_34E_Type_Pattern = MT330_SequenceB_TransactionDetails_34E_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceB_TransactionDetails_37G_Type_Pattern
class MT330_SequenceB_TransactionDetails_37G_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceB_TransactionDetails_37G_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 328, 1)
    _Documentation = None
MT330_SequenceB_TransactionDetails_37G_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceB_TransactionDetails_37G_Type_Pattern._CF_pattern.addPattern(pattern='((N)?[0-9,(?0-9)]{1,12})')
MT330_SequenceB_TransactionDetails_37G_Type_Pattern._InitializeFacetMap(MT330_SequenceB_TransactionDetails_37G_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceB_TransactionDetails_37G_Type_Pattern', MT330_SequenceB_TransactionDetails_37G_Type_Pattern)
_module_typeBindings.MT330_SequenceB_TransactionDetails_37G_Type_Pattern = MT330_SequenceB_TransactionDetails_37G_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceB_TransactionDetails_14D_Type_Pattern
class MT330_SequenceB_TransactionDetails_14D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceB_TransactionDetails_14D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 341, 1)
    _Documentation = None
MT330_SequenceB_TransactionDetails_14D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceB_TransactionDetails_14D_Type_Pattern._CF_pattern.addPattern(pattern='((30E/360|360/360|ACT/360|ACT/365|AFI/365))')
MT330_SequenceB_TransactionDetails_14D_Type_Pattern._InitializeFacetMap(MT330_SequenceB_TransactionDetails_14D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceB_TransactionDetails_14D_Type_Pattern', MT330_SequenceB_TransactionDetails_14D_Type_Pattern)
_module_typeBindings.MT330_SequenceB_TransactionDetails_14D_Type_Pattern = MT330_SequenceB_TransactionDetails_14D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceB_TransactionDetails_30F_Type_Pattern
class MT330_SequenceB_TransactionDetails_30F_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceB_TransactionDetails_30F_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 354, 1)
    _Documentation = None
MT330_SequenceB_TransactionDetails_30F_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceB_TransactionDetails_30F_Type_Pattern._CF_pattern.addPattern(pattern='([0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))')
MT330_SequenceB_TransactionDetails_30F_Type_Pattern._InitializeFacetMap(MT330_SequenceB_TransactionDetails_30F_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceB_TransactionDetails_30F_Type_Pattern', MT330_SequenceB_TransactionDetails_30F_Type_Pattern)
_module_typeBindings.MT330_SequenceB_TransactionDetails_30F_Type_Pattern = MT330_SequenceB_TransactionDetails_30F_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceB_TransactionDetails_38J_Type_Pattern
class MT330_SequenceB_TransactionDetails_38J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceB_TransactionDetails_38J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 367, 1)
    _Documentation = None
MT330_SequenceB_TransactionDetails_38J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceB_TransactionDetails_38J_Type_Pattern._CF_pattern.addPattern(pattern='([A-Z]{1}[0-9]{3})')
MT330_SequenceB_TransactionDetails_38J_Type_Pattern._InitializeFacetMap(MT330_SequenceB_TransactionDetails_38J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceB_TransactionDetails_38J_Type_Pattern', MT330_SequenceB_TransactionDetails_38J_Type_Pattern)
_module_typeBindings.MT330_SequenceB_TransactionDetails_38J_Type_Pattern = MT330_SequenceB_TransactionDetails_38J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceB_TransactionDetails_39M_Type_Pattern
class MT330_SequenceB_TransactionDetails_39M_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceB_TransactionDetails_39M_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 380, 1)
    _Documentation = None
MT330_SequenceB_TransactionDetails_39M_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceB_TransactionDetails_39M_Type_Pattern._CF_pattern.addPattern(pattern='([A-Z]{2})')
MT330_SequenceB_TransactionDetails_39M_Type_Pattern._InitializeFacetMap(MT330_SequenceB_TransactionDetails_39M_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceB_TransactionDetails_39M_Type_Pattern', MT330_SequenceB_TransactionDetails_39M_Type_Pattern)
_module_typeBindings.MT330_SequenceB_TransactionDetails_39M_Type_Pattern = MT330_SequenceB_TransactionDetails_39M_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53A_Type_Pattern
class MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 393, 1)
    _Documentation = None
MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53A_Type_Pattern._InitializeFacetMap(MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53A_Type_Pattern', MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53A_Type_Pattern)
_module_typeBindings.MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53A_Type_Pattern = MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53D_Type_Pattern
class MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 406, 1)
    _Documentation = None
MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53D_Type_Pattern._InitializeFacetMap(MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53D_Type_Pattern', MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53D_Type_Pattern)
_module_typeBindings.MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53D_Type_Pattern = MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53J_Type_Pattern
class MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 419, 1)
    _Documentation = None
MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53J_Type_Pattern._InitializeFacetMap(MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53J_Type_Pattern', MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53J_Type_Pattern)
_module_typeBindings.MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53J_Type_Pattern = MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86A_Type_Pattern
class MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 432, 1)
    _Documentation = None
MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86A_Type_Pattern._InitializeFacetMap(MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86A_Type_Pattern', MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86A_Type_Pattern)
_module_typeBindings.MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86A_Type_Pattern = MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86D_Type_Pattern
class MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 445, 1)
    _Documentation = None
MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86D_Type_Pattern._InitializeFacetMap(MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86D_Type_Pattern', MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86D_Type_Pattern)
_module_typeBindings.MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86D_Type_Pattern = MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86J_Type_Pattern
class MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 458, 1)
    _Documentation = None
MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86J_Type_Pattern._InitializeFacetMap(MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86J_Type_Pattern', MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86J_Type_Pattern)
_module_typeBindings.MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86J_Type_Pattern = MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56A_Type_Pattern
class MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 471, 1)
    _Documentation = None
MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56A_Type_Pattern._InitializeFacetMap(MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56A_Type_Pattern', MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56A_Type_Pattern)
_module_typeBindings.MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56A_Type_Pattern = MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56D_Type_Pattern
class MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 484, 1)
    _Documentation = None
MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56D_Type_Pattern._InitializeFacetMap(MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56D_Type_Pattern', MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56D_Type_Pattern)
_module_typeBindings.MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56D_Type_Pattern = MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56J_Type_Pattern
class MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 497, 1)
    _Documentation = None
MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56J_Type_Pattern._InitializeFacetMap(MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56J_Type_Pattern', MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56J_Type_Pattern)
_module_typeBindings.MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56J_Type_Pattern = MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57A_Type_Pattern
class MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 510, 1)
    _Documentation = None
MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57A_Type_Pattern._InitializeFacetMap(MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57A_Type_Pattern', MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57A_Type_Pattern)
_module_typeBindings.MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57A_Type_Pattern = MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57D_Type_Pattern
class MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 523, 1)
    _Documentation = None
MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57D_Type_Pattern._InitializeFacetMap(MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57D_Type_Pattern', MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57D_Type_Pattern)
_module_typeBindings.MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57D_Type_Pattern = MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57J_Type_Pattern
class MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 536, 1)
    _Documentation = None
MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57J_Type_Pattern._InitializeFacetMap(MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57J_Type_Pattern', MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57J_Type_Pattern)
_module_typeBindings.MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57J_Type_Pattern = MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58A_Type_Pattern
class MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 549, 1)
    _Documentation = None
MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58A_Type_Pattern._InitializeFacetMap(MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58A_Type_Pattern', MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58A_Type_Pattern)
_module_typeBindings.MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58A_Type_Pattern = MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58D_Type_Pattern
class MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 562, 1)
    _Documentation = None
MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58D_Type_Pattern._InitializeFacetMap(MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58D_Type_Pattern', MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58D_Type_Pattern)
_module_typeBindings.MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58D_Type_Pattern = MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58J_Type_Pattern
class MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 575, 1)
    _Documentation = None
MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58J_Type_Pattern._InitializeFacetMap(MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58J_Type_Pattern', MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58J_Type_Pattern)
_module_typeBindings.MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58J_Type_Pattern = MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53A_Type_Pattern
class MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 588, 1)
    _Documentation = None
MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53A_Type_Pattern._InitializeFacetMap(MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53A_Type_Pattern', MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53A_Type_Pattern)
_module_typeBindings.MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53A_Type_Pattern = MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53D_Type_Pattern
class MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 601, 1)
    _Documentation = None
MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53D_Type_Pattern._InitializeFacetMap(MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53D_Type_Pattern', MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53D_Type_Pattern)
_module_typeBindings.MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53D_Type_Pattern = MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53J_Type_Pattern
class MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 614, 1)
    _Documentation = None
MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53J_Type_Pattern._InitializeFacetMap(MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53J_Type_Pattern', MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53J_Type_Pattern)
_module_typeBindings.MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53J_Type_Pattern = MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86A_Type_Pattern
class MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 627, 1)
    _Documentation = None
MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86A_Type_Pattern._InitializeFacetMap(MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86A_Type_Pattern', MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86A_Type_Pattern)
_module_typeBindings.MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86A_Type_Pattern = MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86D_Type_Pattern
class MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 640, 1)
    _Documentation = None
MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86D_Type_Pattern._InitializeFacetMap(MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86D_Type_Pattern', MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86D_Type_Pattern)
_module_typeBindings.MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86D_Type_Pattern = MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86J_Type_Pattern
class MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 653, 1)
    _Documentation = None
MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86J_Type_Pattern._InitializeFacetMap(MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86J_Type_Pattern', MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86J_Type_Pattern)
_module_typeBindings.MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86J_Type_Pattern = MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56A_Type_Pattern
class MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 666, 1)
    _Documentation = None
MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56A_Type_Pattern._InitializeFacetMap(MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56A_Type_Pattern', MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56A_Type_Pattern)
_module_typeBindings.MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56A_Type_Pattern = MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56D_Type_Pattern
class MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 679, 1)
    _Documentation = None
MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56D_Type_Pattern._InitializeFacetMap(MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56D_Type_Pattern', MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56D_Type_Pattern)
_module_typeBindings.MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56D_Type_Pattern = MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56J_Type_Pattern
class MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 692, 1)
    _Documentation = None
MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56J_Type_Pattern._InitializeFacetMap(MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56J_Type_Pattern', MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56J_Type_Pattern)
_module_typeBindings.MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56J_Type_Pattern = MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57A_Type_Pattern
class MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 705, 1)
    _Documentation = None
MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57A_Type_Pattern._InitializeFacetMap(MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57A_Type_Pattern', MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57A_Type_Pattern)
_module_typeBindings.MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57A_Type_Pattern = MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57D_Type_Pattern
class MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 718, 1)
    _Documentation = None
MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57D_Type_Pattern._InitializeFacetMap(MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57D_Type_Pattern', MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57D_Type_Pattern)
_module_typeBindings.MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57D_Type_Pattern = MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57J_Type_Pattern
class MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 731, 1)
    _Documentation = None
MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57J_Type_Pattern._InitializeFacetMap(MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57J_Type_Pattern', MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57J_Type_Pattern)
_module_typeBindings.MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57J_Type_Pattern = MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58A_Type_Pattern
class MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 744, 1)
    _Documentation = None
MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58A_Type_Pattern._InitializeFacetMap(MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58A_Type_Pattern', MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58A_Type_Pattern)
_module_typeBindings.MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58A_Type_Pattern = MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58D_Type_Pattern
class MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 757, 1)
    _Documentation = None
MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58D_Type_Pattern._InitializeFacetMap(MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58D_Type_Pattern', MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58D_Type_Pattern)
_module_typeBindings.MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58D_Type_Pattern = MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58J_Type_Pattern
class MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 770, 1)
    _Documentation = None
MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58J_Type_Pattern._InitializeFacetMap(MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58J_Type_Pattern', MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58J_Type_Pattern)
_module_typeBindings.MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58J_Type_Pattern = MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53A_Type_Pattern
class MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 783, 1)
    _Documentation = None
MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53A_Type_Pattern._InitializeFacetMap(MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53A_Type_Pattern', MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53A_Type_Pattern)
_module_typeBindings.MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53A_Type_Pattern = MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53D_Type_Pattern
class MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 796, 1)
    _Documentation = None
MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53D_Type_Pattern._InitializeFacetMap(MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53D_Type_Pattern', MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53D_Type_Pattern)
_module_typeBindings.MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53D_Type_Pattern = MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53J_Type_Pattern
class MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 809, 1)
    _Documentation = None
MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53J_Type_Pattern._InitializeFacetMap(MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53J_Type_Pattern', MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53J_Type_Pattern)
_module_typeBindings.MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53J_Type_Pattern = MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86A_Type_Pattern
class MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 822, 1)
    _Documentation = None
MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86A_Type_Pattern._InitializeFacetMap(MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86A_Type_Pattern', MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86A_Type_Pattern)
_module_typeBindings.MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86A_Type_Pattern = MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86D_Type_Pattern
class MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 835, 1)
    _Documentation = None
MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86D_Type_Pattern._InitializeFacetMap(MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86D_Type_Pattern', MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86D_Type_Pattern)
_module_typeBindings.MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86D_Type_Pattern = MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86J_Type_Pattern
class MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 848, 1)
    _Documentation = None
MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86J_Type_Pattern._InitializeFacetMap(MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86J_Type_Pattern', MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86J_Type_Pattern)
_module_typeBindings.MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86J_Type_Pattern = MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56A_Type_Pattern
class MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 861, 1)
    _Documentation = None
MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56A_Type_Pattern._InitializeFacetMap(MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56A_Type_Pattern', MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56A_Type_Pattern)
_module_typeBindings.MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56A_Type_Pattern = MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56D_Type_Pattern
class MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 874, 1)
    _Documentation = None
MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56D_Type_Pattern._InitializeFacetMap(MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56D_Type_Pattern', MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56D_Type_Pattern)
_module_typeBindings.MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56D_Type_Pattern = MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56J_Type_Pattern
class MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 887, 1)
    _Documentation = None
MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56J_Type_Pattern._InitializeFacetMap(MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56J_Type_Pattern', MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56J_Type_Pattern)
_module_typeBindings.MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56J_Type_Pattern = MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57A_Type_Pattern
class MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 900, 1)
    _Documentation = None
MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57A_Type_Pattern._InitializeFacetMap(MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57A_Type_Pattern', MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57A_Type_Pattern)
_module_typeBindings.MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57A_Type_Pattern = MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57D_Type_Pattern
class MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 913, 1)
    _Documentation = None
MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57D_Type_Pattern._InitializeFacetMap(MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57D_Type_Pattern', MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57D_Type_Pattern)
_module_typeBindings.MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57D_Type_Pattern = MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57J_Type_Pattern
class MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 926, 1)
    _Documentation = None
MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57J_Type_Pattern._InitializeFacetMap(MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57J_Type_Pattern', MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57J_Type_Pattern)
_module_typeBindings.MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57J_Type_Pattern = MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58A_Type_Pattern
class MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 939, 1)
    _Documentation = None
MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58A_Type_Pattern._InitializeFacetMap(MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58A_Type_Pattern', MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58A_Type_Pattern)
_module_typeBindings.MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58A_Type_Pattern = MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58D_Type_Pattern
class MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 952, 1)
    _Documentation = None
MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58D_Type_Pattern._InitializeFacetMap(MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58D_Type_Pattern', MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58D_Type_Pattern)
_module_typeBindings.MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58D_Type_Pattern = MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58J_Type_Pattern
class MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 965, 1)
    _Documentation = None
MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58J_Type_Pattern._InitializeFacetMap(MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58J_Type_Pattern', MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58J_Type_Pattern)
_module_typeBindings.MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58J_Type_Pattern = MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53A_Type_Pattern
class MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 978, 1)
    _Documentation = None
MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53A_Type_Pattern._InitializeFacetMap(MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53A_Type_Pattern', MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53A_Type_Pattern)
_module_typeBindings.MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53A_Type_Pattern = MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53D_Type_Pattern
class MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 991, 1)
    _Documentation = None
MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53D_Type_Pattern._InitializeFacetMap(MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53D_Type_Pattern', MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53D_Type_Pattern)
_module_typeBindings.MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53D_Type_Pattern = MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53J_Type_Pattern
class MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1004, 1)
    _Documentation = None
MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53J_Type_Pattern._InitializeFacetMap(MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53J_Type_Pattern', MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53J_Type_Pattern)
_module_typeBindings.MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53J_Type_Pattern = MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86A_Type_Pattern
class MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1017, 1)
    _Documentation = None
MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86A_Type_Pattern._InitializeFacetMap(MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86A_Type_Pattern', MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86A_Type_Pattern)
_module_typeBindings.MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86A_Type_Pattern = MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86D_Type_Pattern
class MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1030, 1)
    _Documentation = None
MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86D_Type_Pattern._InitializeFacetMap(MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86D_Type_Pattern', MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86D_Type_Pattern)
_module_typeBindings.MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86D_Type_Pattern = MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86J_Type_Pattern
class MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1043, 1)
    _Documentation = None
MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86J_Type_Pattern._InitializeFacetMap(MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86J_Type_Pattern', MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86J_Type_Pattern)
_module_typeBindings.MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86J_Type_Pattern = MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56A_Type_Pattern
class MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1056, 1)
    _Documentation = None
MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56A_Type_Pattern._InitializeFacetMap(MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56A_Type_Pattern', MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56A_Type_Pattern)
_module_typeBindings.MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56A_Type_Pattern = MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56D_Type_Pattern
class MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1069, 1)
    _Documentation = None
MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56D_Type_Pattern._InitializeFacetMap(MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56D_Type_Pattern', MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56D_Type_Pattern)
_module_typeBindings.MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56D_Type_Pattern = MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56J_Type_Pattern
class MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1082, 1)
    _Documentation = None
MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56J_Type_Pattern._InitializeFacetMap(MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56J_Type_Pattern', MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56J_Type_Pattern)
_module_typeBindings.MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56J_Type_Pattern = MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57A_Type_Pattern
class MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1095, 1)
    _Documentation = None
MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57A_Type_Pattern._InitializeFacetMap(MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57A_Type_Pattern', MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57A_Type_Pattern)
_module_typeBindings.MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57A_Type_Pattern = MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57D_Type_Pattern
class MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1108, 1)
    _Documentation = None
MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57D_Type_Pattern._InitializeFacetMap(MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57D_Type_Pattern', MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57D_Type_Pattern)
_module_typeBindings.MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57D_Type_Pattern = MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57J_Type_Pattern
class MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1121, 1)
    _Documentation = None
MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57J_Type_Pattern._InitializeFacetMap(MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57J_Type_Pattern', MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57J_Type_Pattern)
_module_typeBindings.MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57J_Type_Pattern = MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58A_Type_Pattern
class MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1134, 1)
    _Documentation = None
MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58A_Type_Pattern._InitializeFacetMap(MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58A_Type_Pattern', MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58A_Type_Pattern)
_module_typeBindings.MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58A_Type_Pattern = MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58D_Type_Pattern
class MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1147, 1)
    _Documentation = None
MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58D_Type_Pattern._InitializeFacetMap(MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58D_Type_Pattern', MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58D_Type_Pattern)
_module_typeBindings.MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58D_Type_Pattern = MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58J_Type_Pattern
class MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1160, 1)
    _Documentation = None
MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58J_Type_Pattern._InitializeFacetMap(MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58J_Type_Pattern', MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58J_Type_Pattern)
_module_typeBindings.MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58J_Type_Pattern = MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceG_TaxInformation_37L_Type_Pattern
class MT330_SequenceG_TaxInformation_37L_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceG_TaxInformation_37L_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1173, 1)
    _Documentation = None
MT330_SequenceG_TaxInformation_37L_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceG_TaxInformation_37L_Type_Pattern._CF_pattern.addPattern(pattern='([0-9,(?0-9)]{1,12})')
MT330_SequenceG_TaxInformation_37L_Type_Pattern._InitializeFacetMap(MT330_SequenceG_TaxInformation_37L_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceG_TaxInformation_37L_Type_Pattern', MT330_SequenceG_TaxInformation_37L_Type_Pattern)
_module_typeBindings.MT330_SequenceG_TaxInformation_37L_Type_Pattern = MT330_SequenceG_TaxInformation_37L_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceG_TaxInformation_33B_Type_Pattern
class MT330_SequenceG_TaxInformation_33B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceG_TaxInformation_33B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1186, 1)
    _Documentation = None
MT330_SequenceG_TaxInformation_33B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceG_TaxInformation_33B_Type_Pattern._CF_pattern.addPattern(pattern='((AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})')
MT330_SequenceG_TaxInformation_33B_Type_Pattern._InitializeFacetMap(MT330_SequenceG_TaxInformation_33B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceG_TaxInformation_33B_Type_Pattern', MT330_SequenceG_TaxInformation_33B_Type_Pattern)
_module_typeBindings.MT330_SequenceG_TaxInformation_33B_Type_Pattern = MT330_SequenceG_TaxInformation_33B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceG_TaxInformation_36_Type_Pattern
class MT330_SequenceG_TaxInformation_36_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceG_TaxInformation_36_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1199, 1)
    _Documentation = None
MT330_SequenceG_TaxInformation_36_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceG_TaxInformation_36_Type_Pattern._CF_pattern.addPattern(pattern='([0-9,(?0-9)]{1,12})')
MT330_SequenceG_TaxInformation_36_Type_Pattern._InitializeFacetMap(MT330_SequenceG_TaxInformation_36_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceG_TaxInformation_36_Type_Pattern', MT330_SequenceG_TaxInformation_36_Type_Pattern)
_module_typeBindings.MT330_SequenceG_TaxInformation_36_Type_Pattern = MT330_SequenceG_TaxInformation_36_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceG_TaxInformation_33E_Type_Pattern
class MT330_SequenceG_TaxInformation_33E_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceG_TaxInformation_33E_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1212, 1)
    _Documentation = None
MT330_SequenceG_TaxInformation_33E_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceG_TaxInformation_33E_Type_Pattern._CF_pattern.addPattern(pattern='((AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})')
MT330_SequenceG_TaxInformation_33E_Type_Pattern._InitializeFacetMap(MT330_SequenceG_TaxInformation_33E_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceG_TaxInformation_33E_Type_Pattern', MT330_SequenceG_TaxInformation_33E_Type_Pattern)
_module_typeBindings.MT330_SequenceG_TaxInformation_33E_Type_Pattern = MT330_SequenceG_TaxInformation_33E_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceH_AdditionalInformation_29A_Type_Pattern
class MT330_SequenceH_AdditionalInformation_29A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceH_AdditionalInformation_29A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1225, 1)
    _Documentation = None
MT330_SequenceH_AdditionalInformation_29A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceH_AdditionalInformation_29A_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT330_SequenceH_AdditionalInformation_29A_Type_Pattern._InitializeFacetMap(MT330_SequenceH_AdditionalInformation_29A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceH_AdditionalInformation_29A_Type_Pattern', MT330_SequenceH_AdditionalInformation_29A_Type_Pattern)
_module_typeBindings.MT330_SequenceH_AdditionalInformation_29A_Type_Pattern = MT330_SequenceH_AdditionalInformation_29A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceH_AdditionalInformation_24D_Type_Pattern
class MT330_SequenceH_AdditionalInformation_24D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceH_AdditionalInformation_24D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1238, 1)
    _Documentation = None
MT330_SequenceH_AdditionalInformation_24D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceH_AdditionalInformation_24D_Type_Pattern._CF_pattern.addPattern(pattern="((ELEC|PHON)(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35})?)")
MT330_SequenceH_AdditionalInformation_24D_Type_Pattern._InitializeFacetMap(MT330_SequenceH_AdditionalInformation_24D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceH_AdditionalInformation_24D_Type_Pattern', MT330_SequenceH_AdditionalInformation_24D_Type_Pattern)
_module_typeBindings.MT330_SequenceH_AdditionalInformation_24D_Type_Pattern = MT330_SequenceH_AdditionalInformation_24D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceH_AdditionalInformation_84A_Type_Pattern
class MT330_SequenceH_AdditionalInformation_84A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceH_AdditionalInformation_84A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1251, 1)
    _Documentation = None
MT330_SequenceH_AdditionalInformation_84A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceH_AdditionalInformation_84A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT330_SequenceH_AdditionalInformation_84A_Type_Pattern._InitializeFacetMap(MT330_SequenceH_AdditionalInformation_84A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceH_AdditionalInformation_84A_Type_Pattern', MT330_SequenceH_AdditionalInformation_84A_Type_Pattern)
_module_typeBindings.MT330_SequenceH_AdditionalInformation_84A_Type_Pattern = MT330_SequenceH_AdditionalInformation_84A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceH_AdditionalInformation_84B_Type_Pattern
class MT330_SequenceH_AdditionalInformation_84B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceH_AdditionalInformation_84B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1264, 1)
    _Documentation = None
MT330_SequenceH_AdditionalInformation_84B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceH_AdditionalInformation_84B_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35})?)")
MT330_SequenceH_AdditionalInformation_84B_Type_Pattern._InitializeFacetMap(MT330_SequenceH_AdditionalInformation_84B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceH_AdditionalInformation_84B_Type_Pattern', MT330_SequenceH_AdditionalInformation_84B_Type_Pattern)
_module_typeBindings.MT330_SequenceH_AdditionalInformation_84B_Type_Pattern = MT330_SequenceH_AdditionalInformation_84B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceH_AdditionalInformation_84D_Type_Pattern
class MT330_SequenceH_AdditionalInformation_84D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceH_AdditionalInformation_84D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1277, 1)
    _Documentation = None
MT330_SequenceH_AdditionalInformation_84D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceH_AdditionalInformation_84D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT330_SequenceH_AdditionalInformation_84D_Type_Pattern._InitializeFacetMap(MT330_SequenceH_AdditionalInformation_84D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceH_AdditionalInformation_84D_Type_Pattern', MT330_SequenceH_AdditionalInformation_84D_Type_Pattern)
_module_typeBindings.MT330_SequenceH_AdditionalInformation_84D_Type_Pattern = MT330_SequenceH_AdditionalInformation_84D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceH_AdditionalInformation_84J_Type_Pattern
class MT330_SequenceH_AdditionalInformation_84J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceH_AdditionalInformation_84J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1290, 1)
    _Documentation = None
MT330_SequenceH_AdditionalInformation_84J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceH_AdditionalInformation_84J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT330_SequenceH_AdditionalInformation_84J_Type_Pattern._InitializeFacetMap(MT330_SequenceH_AdditionalInformation_84J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceH_AdditionalInformation_84J_Type_Pattern', MT330_SequenceH_AdditionalInformation_84J_Type_Pattern)
_module_typeBindings.MT330_SequenceH_AdditionalInformation_84J_Type_Pattern = MT330_SequenceH_AdditionalInformation_84J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceH_AdditionalInformation_85A_Type_Pattern
class MT330_SequenceH_AdditionalInformation_85A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceH_AdditionalInformation_85A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1303, 1)
    _Documentation = None
MT330_SequenceH_AdditionalInformation_85A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceH_AdditionalInformation_85A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT330_SequenceH_AdditionalInformation_85A_Type_Pattern._InitializeFacetMap(MT330_SequenceH_AdditionalInformation_85A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceH_AdditionalInformation_85A_Type_Pattern', MT330_SequenceH_AdditionalInformation_85A_Type_Pattern)
_module_typeBindings.MT330_SequenceH_AdditionalInformation_85A_Type_Pattern = MT330_SequenceH_AdditionalInformation_85A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceH_AdditionalInformation_85B_Type_Pattern
class MT330_SequenceH_AdditionalInformation_85B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceH_AdditionalInformation_85B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1316, 1)
    _Documentation = None
MT330_SequenceH_AdditionalInformation_85B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceH_AdditionalInformation_85B_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35})?)")
MT330_SequenceH_AdditionalInformation_85B_Type_Pattern._InitializeFacetMap(MT330_SequenceH_AdditionalInformation_85B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceH_AdditionalInformation_85B_Type_Pattern', MT330_SequenceH_AdditionalInformation_85B_Type_Pattern)
_module_typeBindings.MT330_SequenceH_AdditionalInformation_85B_Type_Pattern = MT330_SequenceH_AdditionalInformation_85B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceH_AdditionalInformation_85D_Type_Pattern
class MT330_SequenceH_AdditionalInformation_85D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceH_AdditionalInformation_85D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1329, 1)
    _Documentation = None
MT330_SequenceH_AdditionalInformation_85D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceH_AdditionalInformation_85D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT330_SequenceH_AdditionalInformation_85D_Type_Pattern._InitializeFacetMap(MT330_SequenceH_AdditionalInformation_85D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceH_AdditionalInformation_85D_Type_Pattern', MT330_SequenceH_AdditionalInformation_85D_Type_Pattern)
_module_typeBindings.MT330_SequenceH_AdditionalInformation_85D_Type_Pattern = MT330_SequenceH_AdditionalInformation_85D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceH_AdditionalInformation_85J_Type_Pattern
class MT330_SequenceH_AdditionalInformation_85J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceH_AdditionalInformation_85J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1342, 1)
    _Documentation = None
MT330_SequenceH_AdditionalInformation_85J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceH_AdditionalInformation_85J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT330_SequenceH_AdditionalInformation_85J_Type_Pattern._InitializeFacetMap(MT330_SequenceH_AdditionalInformation_85J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceH_AdditionalInformation_85J_Type_Pattern', MT330_SequenceH_AdditionalInformation_85J_Type_Pattern)
_module_typeBindings.MT330_SequenceH_AdditionalInformation_85J_Type_Pattern = MT330_SequenceH_AdditionalInformation_85J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceH_AdditionalInformation_26H_Type_Pattern
class MT330_SequenceH_AdditionalInformation_26H_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceH_AdditionalInformation_26H_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1355, 1)
    _Documentation = None
MT330_SequenceH_AdditionalInformation_26H_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceH_AdditionalInformation_26H_Type_Pattern._CF_pattern.addPattern(pattern="(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,16})")
MT330_SequenceH_AdditionalInformation_26H_Type_Pattern._InitializeFacetMap(MT330_SequenceH_AdditionalInformation_26H_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceH_AdditionalInformation_26H_Type_Pattern', MT330_SequenceH_AdditionalInformation_26H_Type_Pattern)
_module_typeBindings.MT330_SequenceH_AdditionalInformation_26H_Type_Pattern = MT330_SequenceH_AdditionalInformation_26H_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceH_AdditionalInformation_34C_Type_Pattern
class MT330_SequenceH_AdditionalInformation_34C_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceH_AdditionalInformation_34C_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1368, 1)
    _Documentation = None
MT330_SequenceH_AdditionalInformation_34C_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceH_AdditionalInformation_34C_Type_Pattern._CF_pattern.addPattern(pattern='([A-Z0-9]{4}/(N)?(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})')
MT330_SequenceH_AdditionalInformation_34C_Type_Pattern._InitializeFacetMap(MT330_SequenceH_AdditionalInformation_34C_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceH_AdditionalInformation_34C_Type_Pattern', MT330_SequenceH_AdditionalInformation_34C_Type_Pattern)
_module_typeBindings.MT330_SequenceH_AdditionalInformation_34C_Type_Pattern = MT330_SequenceH_AdditionalInformation_34C_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT330_SequenceH_AdditionalInformation_72_Type_Pattern
class MT330_SequenceH_AdditionalInformation_72_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceH_AdditionalInformation_72_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1381, 1)
    _Documentation = None
MT330_SequenceH_AdditionalInformation_72_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT330_SequenceH_AdditionalInformation_72_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,6})")
MT330_SequenceH_AdditionalInformation_72_Type_Pattern._InitializeFacetMap(MT330_SequenceH_AdditionalInformation_72_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceH_AdditionalInformation_72_Type_Pattern', MT330_SequenceH_AdditionalInformation_72_Type_Pattern)
_module_typeBindings.MT330_SequenceH_AdditionalInformation_72_Type_Pattern = MT330_SequenceH_AdditionalInformation_72_Type_Pattern

# Complex type {http://www.w3schools.com}MT330_SequenceA_GeneralInformation with content type ELEMENT_ONLY
class MT330_SequenceA_GeneralInformation (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceA_GeneralInformation with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceA_GeneralInformation')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1394, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}SendersReference uses Python identifier SendersReference
    __SendersReference = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SendersReference'), 'SendersReference', '__httpwww_w3schools_com_MT330_SequenceA_GeneralInformation_httpwww_w3schools_comSendersReference', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1396, 3), )

    
    SendersReference = property(__SendersReference.value, __SendersReference.set, None, None)

    
    # Element {http://www.w3schools.com}RelatedReference uses Python identifier RelatedReference
    __RelatedReference = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'RelatedReference'), 'RelatedReference', '__httpwww_w3schools_com_MT330_SequenceA_GeneralInformation_httpwww_w3schools_comRelatedReference', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1397, 3), )

    
    RelatedReference = property(__RelatedReference.value, __RelatedReference.set, None, None)

    
    # Element {http://www.w3schools.com}TypeOfOperation uses Python identifier TypeOfOperation
    __TypeOfOperation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'TypeOfOperation'), 'TypeOfOperation', '__httpwww_w3schools_com_MT330_SequenceA_GeneralInformation_httpwww_w3schools_comTypeOfOperation', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1398, 3), )

    
    TypeOfOperation = property(__TypeOfOperation.value, __TypeOfOperation.set, None, None)

    
    # Element {http://www.w3schools.com}ScopeOfOperation uses Python identifier ScopeOfOperation
    __ScopeOfOperation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ScopeOfOperation'), 'ScopeOfOperation', '__httpwww_w3schools_com_MT330_SequenceA_GeneralInformation_httpwww_w3schools_comScopeOfOperation', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1399, 3), )

    
    ScopeOfOperation = property(__ScopeOfOperation.value, __ScopeOfOperation.set, None, None)

    
    # Element {http://www.w3schools.com}TypeOfEvent uses Python identifier TypeOfEvent
    __TypeOfEvent = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'TypeOfEvent'), 'TypeOfEvent', '__httpwww_w3schools_com_MT330_SequenceA_GeneralInformation_httpwww_w3schools_comTypeOfEvent', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1400, 3), )

    
    TypeOfEvent = property(__TypeOfEvent.value, __TypeOfEvent.set, None, None)

    
    # Element {http://www.w3schools.com}CommonReference uses Python identifier CommonReference
    __CommonReference = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CommonReference'), 'CommonReference', '__httpwww_w3schools_com_MT330_SequenceA_GeneralInformation_httpwww_w3schools_comCommonReference', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1401, 3), )

    
    CommonReference = property(__CommonReference.value, __CommonReference.set, None, None)

    
    # Element {http://www.w3schools.com}ContractNumberPartyA uses Python identifier ContractNumberPartyA
    __ContractNumberPartyA = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ContractNumberPartyA'), 'ContractNumberPartyA', '__httpwww_w3schools_com_MT330_SequenceA_GeneralInformation_httpwww_w3schools_comContractNumberPartyA', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1402, 3), )

    
    ContractNumberPartyA = property(__ContractNumberPartyA.value, __ContractNumberPartyA.set, None, None)

    
    # Element {http://www.w3schools.com}PartyA_A uses Python identifier PartyA_A
    __PartyA_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PartyA_A'), 'PartyA_A', '__httpwww_w3schools_com_MT330_SequenceA_GeneralInformation_httpwww_w3schools_comPartyA_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1404, 4), )

    
    PartyA_A = property(__PartyA_A.value, __PartyA_A.set, None, None)

    
    # Element {http://www.w3schools.com}PartyA_D uses Python identifier PartyA_D
    __PartyA_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PartyA_D'), 'PartyA_D', '__httpwww_w3schools_com_MT330_SequenceA_GeneralInformation_httpwww_w3schools_comPartyA_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1405, 4), )

    
    PartyA_D = property(__PartyA_D.value, __PartyA_D.set, None, None)

    
    # Element {http://www.w3schools.com}PartyA_J uses Python identifier PartyA_J
    __PartyA_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PartyA_J'), 'PartyA_J', '__httpwww_w3schools_com_MT330_SequenceA_GeneralInformation_httpwww_w3schools_comPartyA_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1406, 4), )

    
    PartyA_J = property(__PartyA_J.value, __PartyA_J.set, None, None)

    
    # Element {http://www.w3schools.com}PartyB_A uses Python identifier PartyB_A
    __PartyB_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PartyB_A'), 'PartyB_A', '__httpwww_w3schools_com_MT330_SequenceA_GeneralInformation_httpwww_w3schools_comPartyB_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1409, 4), )

    
    PartyB_A = property(__PartyB_A.value, __PartyB_A.set, None, None)

    
    # Element {http://www.w3schools.com}PartyB_D uses Python identifier PartyB_D
    __PartyB_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PartyB_D'), 'PartyB_D', '__httpwww_w3schools_com_MT330_SequenceA_GeneralInformation_httpwww_w3schools_comPartyB_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1410, 4), )

    
    PartyB_D = property(__PartyB_D.value, __PartyB_D.set, None, None)

    
    # Element {http://www.w3schools.com}PartyB_J uses Python identifier PartyB_J
    __PartyB_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PartyB_J'), 'PartyB_J', '__httpwww_w3schools_com_MT330_SequenceA_GeneralInformation_httpwww_w3schools_comPartyB_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1411, 4), )

    
    PartyB_J = property(__PartyB_J.value, __PartyB_J.set, None, None)

    
    # Element {http://www.w3schools.com}FundOrInstructingParty_A uses Python identifier FundOrInstructingParty_A
    __FundOrInstructingParty_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'FundOrInstructingParty_A'), 'FundOrInstructingParty_A', '__httpwww_w3schools_com_MT330_SequenceA_GeneralInformation_httpwww_w3schools_comFundOrInstructingParty_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1414, 4), )

    
    FundOrInstructingParty_A = property(__FundOrInstructingParty_A.value, __FundOrInstructingParty_A.set, None, None)

    
    # Element {http://www.w3schools.com}FundOrInstructingParty_D uses Python identifier FundOrInstructingParty_D
    __FundOrInstructingParty_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'FundOrInstructingParty_D'), 'FundOrInstructingParty_D', '__httpwww_w3schools_com_MT330_SequenceA_GeneralInformation_httpwww_w3schools_comFundOrInstructingParty_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1415, 4), )

    
    FundOrInstructingParty_D = property(__FundOrInstructingParty_D.value, __FundOrInstructingParty_D.set, None, None)

    
    # Element {http://www.w3schools.com}FundOrInstructingParty_J uses Python identifier FundOrInstructingParty_J
    __FundOrInstructingParty_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'FundOrInstructingParty_J'), 'FundOrInstructingParty_J', '__httpwww_w3schools_com_MT330_SequenceA_GeneralInformation_httpwww_w3schools_comFundOrInstructingParty_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1416, 4), )

    
    FundOrInstructingParty_J = property(__FundOrInstructingParty_J.value, __FundOrInstructingParty_J.set, None, None)

    
    # Element {http://www.w3schools.com}TermsAndConditions uses Python identifier TermsAndConditions
    __TermsAndConditions = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'TermsAndConditions'), 'TermsAndConditions', '__httpwww_w3schools_com_MT330_SequenceA_GeneralInformation_httpwww_w3schools_comTermsAndConditions', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1418, 3), )

    
    TermsAndConditions = property(__TermsAndConditions.value, __TermsAndConditions.set, None, None)

    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceA_GeneralInformation_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='15A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1420, 2)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1420, 2)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceA_GeneralInformation_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1421, 2)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1421, 2)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    
    # Attribute formatTag uses Python identifier formatTag
    __formatTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'formatTag'), 'formatTag', '__httpwww_w3schools_com_MT330_SequenceA_GeneralInformation_formatTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='False')
    __formatTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1422, 2)
    __formatTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1422, 2)
    
    formatTag = property(__formatTag.value, __formatTag.set, None, None)

    _ElementMap.update({
        __SendersReference.name() : __SendersReference,
        __RelatedReference.name() : __RelatedReference,
        __TypeOfOperation.name() : __TypeOfOperation,
        __ScopeOfOperation.name() : __ScopeOfOperation,
        __TypeOfEvent.name() : __TypeOfEvent,
        __CommonReference.name() : __CommonReference,
        __ContractNumberPartyA.name() : __ContractNumberPartyA,
        __PartyA_A.name() : __PartyA_A,
        __PartyA_D.name() : __PartyA_D,
        __PartyA_J.name() : __PartyA_J,
        __PartyB_A.name() : __PartyB_A,
        __PartyB_D.name() : __PartyB_D,
        __PartyB_J.name() : __PartyB_J,
        __FundOrInstructingParty_A.name() : __FundOrInstructingParty_A,
        __FundOrInstructingParty_D.name() : __FundOrInstructingParty_D,
        __FundOrInstructingParty_J.name() : __FundOrInstructingParty_J,
        __TermsAndConditions.name() : __TermsAndConditions
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory,
        __formatTag.name() : __formatTag
    })
_module_typeBindings.MT330_SequenceA_GeneralInformation = MT330_SequenceA_GeneralInformation
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceA_GeneralInformation', MT330_SequenceA_GeneralInformation)


# Complex type {http://www.w3schools.com}MT330_SequenceB_TransactionDetails with content type ELEMENT_ONLY
class MT330_SequenceB_TransactionDetails (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceB_TransactionDetails with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceB_TransactionDetails')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1424, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}PartyAsRole uses Python identifier PartyAsRole
    __PartyAsRole = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PartyAsRole'), 'PartyAsRole', '__httpwww_w3schools_com_MT330_SequenceB_TransactionDetails_httpwww_w3schools_comPartyAsRole', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1426, 3), )

    
    PartyAsRole = property(__PartyAsRole.value, __PartyAsRole.set, None, None)

    
    # Element {http://www.w3schools.com}TradeDate uses Python identifier TradeDate
    __TradeDate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'TradeDate'), 'TradeDate', '__httpwww_w3schools_com_MT330_SequenceB_TransactionDetails_httpwww_w3schools_comTradeDate', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1427, 3), )

    
    TradeDate = property(__TradeDate.value, __TradeDate.set, None, None)

    
    # Element {http://www.w3schools.com}ValueDate uses Python identifier ValueDate
    __ValueDate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ValueDate'), 'ValueDate', '__httpwww_w3schools_com_MT330_SequenceB_TransactionDetails_httpwww_w3schools_comValueDate', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1428, 3), )

    
    ValueDate = property(__ValueDate.value, __ValueDate.set, None, None)

    
    # Element {http://www.w3schools.com}PeriodOfNotice uses Python identifier PeriodOfNotice
    __PeriodOfNotice = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PeriodOfNotice'), 'PeriodOfNotice', '__httpwww_w3schools_com_MT330_SequenceB_TransactionDetails_httpwww_w3schools_comPeriodOfNotice', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1429, 3), )

    
    PeriodOfNotice = property(__PeriodOfNotice.value, __PeriodOfNotice.set, None, None)

    
    # Element {http://www.w3schools.com}CurrencyAndBalance uses Python identifier CurrencyAndBalance
    __CurrencyAndBalance = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CurrencyAndBalance'), 'CurrencyAndBalance', '__httpwww_w3schools_com_MT330_SequenceB_TransactionDetails_httpwww_w3schools_comCurrencyAndBalance', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1430, 3), )

    
    CurrencyAndBalance = property(__CurrencyAndBalance.value, __CurrencyAndBalance.set, None, None)

    
    # Element {http://www.w3schools.com}PrincipalAmountToBeSettled uses Python identifier PrincipalAmountToBeSettled
    __PrincipalAmountToBeSettled = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PrincipalAmountToBeSettled'), 'PrincipalAmountToBeSettled', '__httpwww_w3schools_com_MT330_SequenceB_TransactionDetails_httpwww_w3schools_comPrincipalAmountToBeSettled', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1431, 3), )

    
    PrincipalAmountToBeSettled = property(__PrincipalAmountToBeSettled.value, __PrincipalAmountToBeSettled.set, None, None)

    
    # Element {http://www.w3schools.com}InterestDueDate uses Python identifier InterestDueDate
    __InterestDueDate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'InterestDueDate'), 'InterestDueDate', '__httpwww_w3schools_com_MT330_SequenceB_TransactionDetails_httpwww_w3schools_comInterestDueDate', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1432, 3), )

    
    InterestDueDate = property(__InterestDueDate.value, __InterestDueDate.set, None, None)

    
    # Element {http://www.w3schools.com}CurrencyAndInterestAmount uses Python identifier CurrencyAndInterestAmount
    __CurrencyAndInterestAmount = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CurrencyAndInterestAmount'), 'CurrencyAndInterestAmount', '__httpwww_w3schools_com_MT330_SequenceB_TransactionDetails_httpwww_w3schools_comCurrencyAndInterestAmount', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1433, 3), )

    
    CurrencyAndInterestAmount = property(__CurrencyAndInterestAmount.value, __CurrencyAndInterestAmount.set, None, None)

    
    # Element {http://www.w3schools.com}InterestRate uses Python identifier InterestRate
    __InterestRate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'InterestRate'), 'InterestRate', '__httpwww_w3schools_com_MT330_SequenceB_TransactionDetails_httpwww_w3schools_comInterestRate', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1434, 3), )

    
    InterestRate = property(__InterestRate.value, __InterestRate.set, None, None)

    
    # Element {http://www.w3schools.com}DayCountFraction uses Python identifier DayCountFraction
    __DayCountFraction = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DayCountFraction'), 'DayCountFraction', '__httpwww_w3schools_com_MT330_SequenceB_TransactionDetails_httpwww_w3schools_comDayCountFraction', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1435, 3), )

    
    DayCountFraction = property(__DayCountFraction.value, __DayCountFraction.set, None, None)

    
    # Element {http://www.w3schools.com}LastDayOfTheNextInterestPeriod uses Python identifier LastDayOfTheNextInterestPeriod
    __LastDayOfTheNextInterestPeriod = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'LastDayOfTheNextInterestPeriod'), 'LastDayOfTheNextInterestPeriod', '__httpwww_w3schools_com_MT330_SequenceB_TransactionDetails_httpwww_w3schools_comLastDayOfTheNextInterestPeriod', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1436, 3), )

    
    LastDayOfTheNextInterestPeriod = property(__LastDayOfTheNextInterestPeriod.value, __LastDayOfTheNextInterestPeriod.set, None, None)

    
    # Element {http://www.w3schools.com}NumberOfDays uses Python identifier NumberOfDays
    __NumberOfDays = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'NumberOfDays'), 'NumberOfDays', '__httpwww_w3schools_com_MT330_SequenceB_TransactionDetails_httpwww_w3schools_comNumberOfDays', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1437, 3), )

    
    NumberOfDays = property(__NumberOfDays.value, __NumberOfDays.set, None, None)

    
    # Element {http://www.w3schools.com}PaymentClearingCentre uses Python identifier PaymentClearingCentre
    __PaymentClearingCentre = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PaymentClearingCentre'), 'PaymentClearingCentre', '__httpwww_w3schools_com_MT330_SequenceB_TransactionDetails_httpwww_w3schools_comPaymentClearingCentre', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1438, 3), )

    
    PaymentClearingCentre = property(__PaymentClearingCentre.value, __PaymentClearingCentre.set, None, None)

    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceB_TransactionDetails_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='15B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1440, 2)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1440, 2)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceB_TransactionDetails_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1441, 2)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1441, 2)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    
    # Attribute formatTag uses Python identifier formatTag
    __formatTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'formatTag'), 'formatTag', '__httpwww_w3schools_com_MT330_SequenceB_TransactionDetails_formatTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='False')
    __formatTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1442, 2)
    __formatTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1442, 2)
    
    formatTag = property(__formatTag.value, __formatTag.set, None, None)

    _ElementMap.update({
        __PartyAsRole.name() : __PartyAsRole,
        __TradeDate.name() : __TradeDate,
        __ValueDate.name() : __ValueDate,
        __PeriodOfNotice.name() : __PeriodOfNotice,
        __CurrencyAndBalance.name() : __CurrencyAndBalance,
        __PrincipalAmountToBeSettled.name() : __PrincipalAmountToBeSettled,
        __InterestDueDate.name() : __InterestDueDate,
        __CurrencyAndInterestAmount.name() : __CurrencyAndInterestAmount,
        __InterestRate.name() : __InterestRate,
        __DayCountFraction.name() : __DayCountFraction,
        __LastDayOfTheNextInterestPeriod.name() : __LastDayOfTheNextInterestPeriod,
        __NumberOfDays.name() : __NumberOfDays,
        __PaymentClearingCentre.name() : __PaymentClearingCentre
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory,
        __formatTag.name() : __formatTag
    })
_module_typeBindings.MT330_SequenceB_TransactionDetails = MT330_SequenceB_TransactionDetails
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceB_TransactionDetails', MT330_SequenceB_TransactionDetails)


# Complex type {http://www.w3schools.com}MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA with content type ELEMENT_ONLY
class MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1444, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}DeliveryAgent_A uses Python identifier DeliveryAgent_A
    __DeliveryAgent_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_A'), 'DeliveryAgent_A', '__httpwww_w3schools_com_MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_httpwww_w3schools_comDeliveryAgent_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1447, 4), )

    
    DeliveryAgent_A = property(__DeliveryAgent_A.value, __DeliveryAgent_A.set, None, None)

    
    # Element {http://www.w3schools.com}DeliveryAgent_D uses Python identifier DeliveryAgent_D
    __DeliveryAgent_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_D'), 'DeliveryAgent_D', '__httpwww_w3schools_com_MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_httpwww_w3schools_comDeliveryAgent_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1448, 4), )

    
    DeliveryAgent_D = property(__DeliveryAgent_D.value, __DeliveryAgent_D.set, None, None)

    
    # Element {http://www.w3schools.com}DeliveryAgent_J uses Python identifier DeliveryAgent_J
    __DeliveryAgent_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_J'), 'DeliveryAgent_J', '__httpwww_w3schools_com_MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_httpwww_w3schools_comDeliveryAgent_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1449, 4), )

    
    DeliveryAgent_J = property(__DeliveryAgent_J.value, __DeliveryAgent_J.set, None, None)

    
    # Element {http://www.w3schools.com}Intermediary2_A uses Python identifier Intermediary2_A
    __Intermediary2_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Intermediary2_A'), 'Intermediary2_A', '__httpwww_w3schools_com_MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_httpwww_w3schools_comIntermediary2_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1452, 4), )

    
    Intermediary2_A = property(__Intermediary2_A.value, __Intermediary2_A.set, None, None)

    
    # Element {http://www.w3schools.com}Intermediary2_D uses Python identifier Intermediary2_D
    __Intermediary2_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Intermediary2_D'), 'Intermediary2_D', '__httpwww_w3schools_com_MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_httpwww_w3schools_comIntermediary2_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1453, 4), )

    
    Intermediary2_D = property(__Intermediary2_D.value, __Intermediary2_D.set, None, None)

    
    # Element {http://www.w3schools.com}Intermediary2_J uses Python identifier Intermediary2_J
    __Intermediary2_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Intermediary2_J'), 'Intermediary2_J', '__httpwww_w3schools_com_MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_httpwww_w3schools_comIntermediary2_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1454, 4), )

    
    Intermediary2_J = property(__Intermediary2_J.value, __Intermediary2_J.set, None, None)

    
    # Element {http://www.w3schools.com}Intermediary_A uses Python identifier Intermediary_A
    __Intermediary_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_A'), 'Intermediary_A', '__httpwww_w3schools_com_MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_httpwww_w3schools_comIntermediary_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1457, 4), )

    
    Intermediary_A = property(__Intermediary_A.value, __Intermediary_A.set, None, None)

    
    # Element {http://www.w3schools.com}Intermediary_D uses Python identifier Intermediary_D
    __Intermediary_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_D'), 'Intermediary_D', '__httpwww_w3schools_com_MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_httpwww_w3schools_comIntermediary_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1458, 4), )

    
    Intermediary_D = property(__Intermediary_D.value, __Intermediary_D.set, None, None)

    
    # Element {http://www.w3schools.com}Intermediary_J uses Python identifier Intermediary_J
    __Intermediary_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_J'), 'Intermediary_J', '__httpwww_w3schools_com_MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_httpwww_w3schools_comIntermediary_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1459, 4), )

    
    Intermediary_J = property(__Intermediary_J.value, __Intermediary_J.set, None, None)

    
    # Element {http://www.w3schools.com}ReceivingAgent_A uses Python identifier ReceivingAgent_A
    __ReceivingAgent_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_A'), 'ReceivingAgent_A', '__httpwww_w3schools_com_MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_httpwww_w3schools_comReceivingAgent_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1462, 4), )

    
    ReceivingAgent_A = property(__ReceivingAgent_A.value, __ReceivingAgent_A.set, None, None)

    
    # Element {http://www.w3schools.com}ReceivingAgent_D uses Python identifier ReceivingAgent_D
    __ReceivingAgent_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_D'), 'ReceivingAgent_D', '__httpwww_w3schools_com_MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_httpwww_w3schools_comReceivingAgent_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1463, 4), )

    
    ReceivingAgent_D = property(__ReceivingAgent_D.value, __ReceivingAgent_D.set, None, None)

    
    # Element {http://www.w3schools.com}ReceivingAgent_J uses Python identifier ReceivingAgent_J
    __ReceivingAgent_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_J'), 'ReceivingAgent_J', '__httpwww_w3schools_com_MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_httpwww_w3schools_comReceivingAgent_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1464, 4), )

    
    ReceivingAgent_J = property(__ReceivingAgent_J.value, __ReceivingAgent_J.set, None, None)

    
    # Element {http://www.w3schools.com}BeneficiaryInstitution_A uses Python identifier BeneficiaryInstitution_A
    __BeneficiaryInstitution_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_A'), 'BeneficiaryInstitution_A', '__httpwww_w3schools_com_MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_httpwww_w3schools_comBeneficiaryInstitution_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1467, 4), )

    
    BeneficiaryInstitution_A = property(__BeneficiaryInstitution_A.value, __BeneficiaryInstitution_A.set, None, None)

    
    # Element {http://www.w3schools.com}BeneficiaryInstitution_D uses Python identifier BeneficiaryInstitution_D
    __BeneficiaryInstitution_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_D'), 'BeneficiaryInstitution_D', '__httpwww_w3schools_com_MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_httpwww_w3schools_comBeneficiaryInstitution_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1468, 4), )

    
    BeneficiaryInstitution_D = property(__BeneficiaryInstitution_D.value, __BeneficiaryInstitution_D.set, None, None)

    
    # Element {http://www.w3schools.com}BeneficiaryInstitution_J uses Python identifier BeneficiaryInstitution_J
    __BeneficiaryInstitution_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_J'), 'BeneficiaryInstitution_J', '__httpwww_w3schools_com_MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_httpwww_w3schools_comBeneficiaryInstitution_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1469, 4), )

    
    BeneficiaryInstitution_J = property(__BeneficiaryInstitution_J.value, __BeneficiaryInstitution_J.set, None, None)

    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='15C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1472, 2)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1472, 2)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1473, 2)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1473, 2)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    
    # Attribute formatTag uses Python identifier formatTag
    __formatTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'formatTag'), 'formatTag', '__httpwww_w3schools_com_MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_formatTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='False')
    __formatTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1474, 2)
    __formatTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1474, 2)
    
    formatTag = property(__formatTag.value, __formatTag.set, None, None)

    _ElementMap.update({
        __DeliveryAgent_A.name() : __DeliveryAgent_A,
        __DeliveryAgent_D.name() : __DeliveryAgent_D,
        __DeliveryAgent_J.name() : __DeliveryAgent_J,
        __Intermediary2_A.name() : __Intermediary2_A,
        __Intermediary2_D.name() : __Intermediary2_D,
        __Intermediary2_J.name() : __Intermediary2_J,
        __Intermediary_A.name() : __Intermediary_A,
        __Intermediary_D.name() : __Intermediary_D,
        __Intermediary_J.name() : __Intermediary_J,
        __ReceivingAgent_A.name() : __ReceivingAgent_A,
        __ReceivingAgent_D.name() : __ReceivingAgent_D,
        __ReceivingAgent_J.name() : __ReceivingAgent_J,
        __BeneficiaryInstitution_A.name() : __BeneficiaryInstitution_A,
        __BeneficiaryInstitution_D.name() : __BeneficiaryInstitution_D,
        __BeneficiaryInstitution_J.name() : __BeneficiaryInstitution_J
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory,
        __formatTag.name() : __formatTag
    })
_module_typeBindings.MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA = MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA', MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA)


# Complex type {http://www.w3schools.com}MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB with content type ELEMENT_ONLY
class MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1476, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}DeliveryAgent_A uses Python identifier DeliveryAgent_A
    __DeliveryAgent_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_A'), 'DeliveryAgent_A', '__httpwww_w3schools_com_MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_httpwww_w3schools_comDeliveryAgent_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1479, 4), )

    
    DeliveryAgent_A = property(__DeliveryAgent_A.value, __DeliveryAgent_A.set, None, None)

    
    # Element {http://www.w3schools.com}DeliveryAgent_D uses Python identifier DeliveryAgent_D
    __DeliveryAgent_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_D'), 'DeliveryAgent_D', '__httpwww_w3schools_com_MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_httpwww_w3schools_comDeliveryAgent_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1480, 4), )

    
    DeliveryAgent_D = property(__DeliveryAgent_D.value, __DeliveryAgent_D.set, None, None)

    
    # Element {http://www.w3schools.com}DeliveryAgent_J uses Python identifier DeliveryAgent_J
    __DeliveryAgent_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_J'), 'DeliveryAgent_J', '__httpwww_w3schools_com_MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_httpwww_w3schools_comDeliveryAgent_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1481, 4), )

    
    DeliveryAgent_J = property(__DeliveryAgent_J.value, __DeliveryAgent_J.set, None, None)

    
    # Element {http://www.w3schools.com}Intermediary2_A uses Python identifier Intermediary2_A
    __Intermediary2_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Intermediary2_A'), 'Intermediary2_A', '__httpwww_w3schools_com_MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_httpwww_w3schools_comIntermediary2_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1484, 4), )

    
    Intermediary2_A = property(__Intermediary2_A.value, __Intermediary2_A.set, None, None)

    
    # Element {http://www.w3schools.com}Intermediary2_D uses Python identifier Intermediary2_D
    __Intermediary2_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Intermediary2_D'), 'Intermediary2_D', '__httpwww_w3schools_com_MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_httpwww_w3schools_comIntermediary2_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1485, 4), )

    
    Intermediary2_D = property(__Intermediary2_D.value, __Intermediary2_D.set, None, None)

    
    # Element {http://www.w3schools.com}Intermediary2_J uses Python identifier Intermediary2_J
    __Intermediary2_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Intermediary2_J'), 'Intermediary2_J', '__httpwww_w3schools_com_MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_httpwww_w3schools_comIntermediary2_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1486, 4), )

    
    Intermediary2_J = property(__Intermediary2_J.value, __Intermediary2_J.set, None, None)

    
    # Element {http://www.w3schools.com}Intermediary_A uses Python identifier Intermediary_A
    __Intermediary_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_A'), 'Intermediary_A', '__httpwww_w3schools_com_MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_httpwww_w3schools_comIntermediary_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1489, 4), )

    
    Intermediary_A = property(__Intermediary_A.value, __Intermediary_A.set, None, None)

    
    # Element {http://www.w3schools.com}Intermediary_D uses Python identifier Intermediary_D
    __Intermediary_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_D'), 'Intermediary_D', '__httpwww_w3schools_com_MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_httpwww_w3schools_comIntermediary_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1490, 4), )

    
    Intermediary_D = property(__Intermediary_D.value, __Intermediary_D.set, None, None)

    
    # Element {http://www.w3schools.com}Intermediary_J uses Python identifier Intermediary_J
    __Intermediary_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_J'), 'Intermediary_J', '__httpwww_w3schools_com_MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_httpwww_w3schools_comIntermediary_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1491, 4), )

    
    Intermediary_J = property(__Intermediary_J.value, __Intermediary_J.set, None, None)

    
    # Element {http://www.w3schools.com}ReceivingAgent_A uses Python identifier ReceivingAgent_A
    __ReceivingAgent_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_A'), 'ReceivingAgent_A', '__httpwww_w3schools_com_MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_httpwww_w3schools_comReceivingAgent_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1494, 4), )

    
    ReceivingAgent_A = property(__ReceivingAgent_A.value, __ReceivingAgent_A.set, None, None)

    
    # Element {http://www.w3schools.com}ReceivingAgent_D uses Python identifier ReceivingAgent_D
    __ReceivingAgent_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_D'), 'ReceivingAgent_D', '__httpwww_w3schools_com_MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_httpwww_w3schools_comReceivingAgent_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1495, 4), )

    
    ReceivingAgent_D = property(__ReceivingAgent_D.value, __ReceivingAgent_D.set, None, None)

    
    # Element {http://www.w3schools.com}ReceivingAgent_J uses Python identifier ReceivingAgent_J
    __ReceivingAgent_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_J'), 'ReceivingAgent_J', '__httpwww_w3schools_com_MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_httpwww_w3schools_comReceivingAgent_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1496, 4), )

    
    ReceivingAgent_J = property(__ReceivingAgent_J.value, __ReceivingAgent_J.set, None, None)

    
    # Element {http://www.w3schools.com}BeneficiaryInstitution_A uses Python identifier BeneficiaryInstitution_A
    __BeneficiaryInstitution_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_A'), 'BeneficiaryInstitution_A', '__httpwww_w3schools_com_MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_httpwww_w3schools_comBeneficiaryInstitution_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1499, 4), )

    
    BeneficiaryInstitution_A = property(__BeneficiaryInstitution_A.value, __BeneficiaryInstitution_A.set, None, None)

    
    # Element {http://www.w3schools.com}BeneficiaryInstitution_D uses Python identifier BeneficiaryInstitution_D
    __BeneficiaryInstitution_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_D'), 'BeneficiaryInstitution_D', '__httpwww_w3schools_com_MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_httpwww_w3schools_comBeneficiaryInstitution_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1500, 4), )

    
    BeneficiaryInstitution_D = property(__BeneficiaryInstitution_D.value, __BeneficiaryInstitution_D.set, None, None)

    
    # Element {http://www.w3schools.com}BeneficiaryInstitution_J uses Python identifier BeneficiaryInstitution_J
    __BeneficiaryInstitution_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_J'), 'BeneficiaryInstitution_J', '__httpwww_w3schools_com_MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_httpwww_w3schools_comBeneficiaryInstitution_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1501, 4), )

    
    BeneficiaryInstitution_J = property(__BeneficiaryInstitution_J.value, __BeneficiaryInstitution_J.set, None, None)

    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='15D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1504, 2)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1504, 2)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1505, 2)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1505, 2)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    
    # Attribute formatTag uses Python identifier formatTag
    __formatTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'formatTag'), 'formatTag', '__httpwww_w3schools_com_MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_formatTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='False')
    __formatTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1506, 2)
    __formatTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1506, 2)
    
    formatTag = property(__formatTag.value, __formatTag.set, None, None)

    _ElementMap.update({
        __DeliveryAgent_A.name() : __DeliveryAgent_A,
        __DeliveryAgent_D.name() : __DeliveryAgent_D,
        __DeliveryAgent_J.name() : __DeliveryAgent_J,
        __Intermediary2_A.name() : __Intermediary2_A,
        __Intermediary2_D.name() : __Intermediary2_D,
        __Intermediary2_J.name() : __Intermediary2_J,
        __Intermediary_A.name() : __Intermediary_A,
        __Intermediary_D.name() : __Intermediary_D,
        __Intermediary_J.name() : __Intermediary_J,
        __ReceivingAgent_A.name() : __ReceivingAgent_A,
        __ReceivingAgent_D.name() : __ReceivingAgent_D,
        __ReceivingAgent_J.name() : __ReceivingAgent_J,
        __BeneficiaryInstitution_A.name() : __BeneficiaryInstitution_A,
        __BeneficiaryInstitution_D.name() : __BeneficiaryInstitution_D,
        __BeneficiaryInstitution_J.name() : __BeneficiaryInstitution_J
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory,
        __formatTag.name() : __formatTag
    })
_module_typeBindings.MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB = MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB', MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB)


# Complex type {http://www.w3schools.com}MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA with content type ELEMENT_ONLY
class MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1508, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}DeliveryAgent_A uses Python identifier DeliveryAgent_A
    __DeliveryAgent_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_A'), 'DeliveryAgent_A', '__httpwww_w3schools_com_MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_httpwww_w3schools_comDeliveryAgent_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1511, 4), )

    
    DeliveryAgent_A = property(__DeliveryAgent_A.value, __DeliveryAgent_A.set, None, None)

    
    # Element {http://www.w3schools.com}DeliveryAgent_D uses Python identifier DeliveryAgent_D
    __DeliveryAgent_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_D'), 'DeliveryAgent_D', '__httpwww_w3schools_com_MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_httpwww_w3schools_comDeliveryAgent_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1512, 4), )

    
    DeliveryAgent_D = property(__DeliveryAgent_D.value, __DeliveryAgent_D.set, None, None)

    
    # Element {http://www.w3schools.com}DeliveryAgent_J uses Python identifier DeliveryAgent_J
    __DeliveryAgent_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_J'), 'DeliveryAgent_J', '__httpwww_w3schools_com_MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_httpwww_w3schools_comDeliveryAgent_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1513, 4), )

    
    DeliveryAgent_J = property(__DeliveryAgent_J.value, __DeliveryAgent_J.set, None, None)

    
    # Element {http://www.w3schools.com}Intermediary2_A uses Python identifier Intermediary2_A
    __Intermediary2_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Intermediary2_A'), 'Intermediary2_A', '__httpwww_w3schools_com_MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_httpwww_w3schools_comIntermediary2_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1516, 4), )

    
    Intermediary2_A = property(__Intermediary2_A.value, __Intermediary2_A.set, None, None)

    
    # Element {http://www.w3schools.com}Intermediary2_D uses Python identifier Intermediary2_D
    __Intermediary2_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Intermediary2_D'), 'Intermediary2_D', '__httpwww_w3schools_com_MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_httpwww_w3schools_comIntermediary2_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1517, 4), )

    
    Intermediary2_D = property(__Intermediary2_D.value, __Intermediary2_D.set, None, None)

    
    # Element {http://www.w3schools.com}Intermediary2_J uses Python identifier Intermediary2_J
    __Intermediary2_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Intermediary2_J'), 'Intermediary2_J', '__httpwww_w3schools_com_MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_httpwww_w3schools_comIntermediary2_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1518, 4), )

    
    Intermediary2_J = property(__Intermediary2_J.value, __Intermediary2_J.set, None, None)

    
    # Element {http://www.w3schools.com}Intermediary_A uses Python identifier Intermediary_A
    __Intermediary_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_A'), 'Intermediary_A', '__httpwww_w3schools_com_MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_httpwww_w3schools_comIntermediary_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1521, 4), )

    
    Intermediary_A = property(__Intermediary_A.value, __Intermediary_A.set, None, None)

    
    # Element {http://www.w3schools.com}Intermediary_D uses Python identifier Intermediary_D
    __Intermediary_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_D'), 'Intermediary_D', '__httpwww_w3schools_com_MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_httpwww_w3schools_comIntermediary_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1522, 4), )

    
    Intermediary_D = property(__Intermediary_D.value, __Intermediary_D.set, None, None)

    
    # Element {http://www.w3schools.com}Intermediary_J uses Python identifier Intermediary_J
    __Intermediary_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_J'), 'Intermediary_J', '__httpwww_w3schools_com_MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_httpwww_w3schools_comIntermediary_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1523, 4), )

    
    Intermediary_J = property(__Intermediary_J.value, __Intermediary_J.set, None, None)

    
    # Element {http://www.w3schools.com}ReceivingAgent_A uses Python identifier ReceivingAgent_A
    __ReceivingAgent_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_A'), 'ReceivingAgent_A', '__httpwww_w3schools_com_MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_httpwww_w3schools_comReceivingAgent_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1526, 4), )

    
    ReceivingAgent_A = property(__ReceivingAgent_A.value, __ReceivingAgent_A.set, None, None)

    
    # Element {http://www.w3schools.com}ReceivingAgent_D uses Python identifier ReceivingAgent_D
    __ReceivingAgent_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_D'), 'ReceivingAgent_D', '__httpwww_w3schools_com_MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_httpwww_w3schools_comReceivingAgent_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1527, 4), )

    
    ReceivingAgent_D = property(__ReceivingAgent_D.value, __ReceivingAgent_D.set, None, None)

    
    # Element {http://www.w3schools.com}ReceivingAgent_J uses Python identifier ReceivingAgent_J
    __ReceivingAgent_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_J'), 'ReceivingAgent_J', '__httpwww_w3schools_com_MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_httpwww_w3schools_comReceivingAgent_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1528, 4), )

    
    ReceivingAgent_J = property(__ReceivingAgent_J.value, __ReceivingAgent_J.set, None, None)

    
    # Element {http://www.w3schools.com}BeneficiaryInstitution_A uses Python identifier BeneficiaryInstitution_A
    __BeneficiaryInstitution_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_A'), 'BeneficiaryInstitution_A', '__httpwww_w3schools_com_MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_httpwww_w3schools_comBeneficiaryInstitution_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1531, 4), )

    
    BeneficiaryInstitution_A = property(__BeneficiaryInstitution_A.value, __BeneficiaryInstitution_A.set, None, None)

    
    # Element {http://www.w3schools.com}BeneficiaryInstitution_D uses Python identifier BeneficiaryInstitution_D
    __BeneficiaryInstitution_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_D'), 'BeneficiaryInstitution_D', '__httpwww_w3schools_com_MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_httpwww_w3schools_comBeneficiaryInstitution_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1532, 4), )

    
    BeneficiaryInstitution_D = property(__BeneficiaryInstitution_D.value, __BeneficiaryInstitution_D.set, None, None)

    
    # Element {http://www.w3schools.com}BeneficiaryInstitution_J uses Python identifier BeneficiaryInstitution_J
    __BeneficiaryInstitution_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_J'), 'BeneficiaryInstitution_J', '__httpwww_w3schools_com_MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_httpwww_w3schools_comBeneficiaryInstitution_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1533, 4), )

    
    BeneficiaryInstitution_J = property(__BeneficiaryInstitution_J.value, __BeneficiaryInstitution_J.set, None, None)

    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='15E')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1536, 2)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1536, 2)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1537, 2)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1537, 2)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    
    # Attribute formatTag uses Python identifier formatTag
    __formatTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'formatTag'), 'formatTag', '__httpwww_w3schools_com_MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_formatTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='False')
    __formatTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1538, 2)
    __formatTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1538, 2)
    
    formatTag = property(__formatTag.value, __formatTag.set, None, None)

    _ElementMap.update({
        __DeliveryAgent_A.name() : __DeliveryAgent_A,
        __DeliveryAgent_D.name() : __DeliveryAgent_D,
        __DeliveryAgent_J.name() : __DeliveryAgent_J,
        __Intermediary2_A.name() : __Intermediary2_A,
        __Intermediary2_D.name() : __Intermediary2_D,
        __Intermediary2_J.name() : __Intermediary2_J,
        __Intermediary_A.name() : __Intermediary_A,
        __Intermediary_D.name() : __Intermediary_D,
        __Intermediary_J.name() : __Intermediary_J,
        __ReceivingAgent_A.name() : __ReceivingAgent_A,
        __ReceivingAgent_D.name() : __ReceivingAgent_D,
        __ReceivingAgent_J.name() : __ReceivingAgent_J,
        __BeneficiaryInstitution_A.name() : __BeneficiaryInstitution_A,
        __BeneficiaryInstitution_D.name() : __BeneficiaryInstitution_D,
        __BeneficiaryInstitution_J.name() : __BeneficiaryInstitution_J
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory,
        __formatTag.name() : __formatTag
    })
_module_typeBindings.MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA = MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA', MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA)


# Complex type {http://www.w3schools.com}MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB with content type ELEMENT_ONLY
class MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1540, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}DeliveryAgent_A uses Python identifier DeliveryAgent_A
    __DeliveryAgent_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_A'), 'DeliveryAgent_A', '__httpwww_w3schools_com_MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_httpwww_w3schools_comDeliveryAgent_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1543, 4), )

    
    DeliveryAgent_A = property(__DeliveryAgent_A.value, __DeliveryAgent_A.set, None, None)

    
    # Element {http://www.w3schools.com}DeliveryAgent_D uses Python identifier DeliveryAgent_D
    __DeliveryAgent_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_D'), 'DeliveryAgent_D', '__httpwww_w3schools_com_MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_httpwww_w3schools_comDeliveryAgent_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1544, 4), )

    
    DeliveryAgent_D = property(__DeliveryAgent_D.value, __DeliveryAgent_D.set, None, None)

    
    # Element {http://www.w3schools.com}DeliveryAgent_J uses Python identifier DeliveryAgent_J
    __DeliveryAgent_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_J'), 'DeliveryAgent_J', '__httpwww_w3schools_com_MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_httpwww_w3schools_comDeliveryAgent_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1545, 4), )

    
    DeliveryAgent_J = property(__DeliveryAgent_J.value, __DeliveryAgent_J.set, None, None)

    
    # Element {http://www.w3schools.com}Intermediary2_A uses Python identifier Intermediary2_A
    __Intermediary2_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Intermediary2_A'), 'Intermediary2_A', '__httpwww_w3schools_com_MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_httpwww_w3schools_comIntermediary2_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1548, 4), )

    
    Intermediary2_A = property(__Intermediary2_A.value, __Intermediary2_A.set, None, None)

    
    # Element {http://www.w3schools.com}Intermediary2_D uses Python identifier Intermediary2_D
    __Intermediary2_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Intermediary2_D'), 'Intermediary2_D', '__httpwww_w3schools_com_MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_httpwww_w3schools_comIntermediary2_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1549, 4), )

    
    Intermediary2_D = property(__Intermediary2_D.value, __Intermediary2_D.set, None, None)

    
    # Element {http://www.w3schools.com}Intermediary2_J uses Python identifier Intermediary2_J
    __Intermediary2_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Intermediary2_J'), 'Intermediary2_J', '__httpwww_w3schools_com_MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_httpwww_w3schools_comIntermediary2_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1550, 4), )

    
    Intermediary2_J = property(__Intermediary2_J.value, __Intermediary2_J.set, None, None)

    
    # Element {http://www.w3schools.com}Intermediary_A uses Python identifier Intermediary_A
    __Intermediary_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_A'), 'Intermediary_A', '__httpwww_w3schools_com_MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_httpwww_w3schools_comIntermediary_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1553, 4), )

    
    Intermediary_A = property(__Intermediary_A.value, __Intermediary_A.set, None, None)

    
    # Element {http://www.w3schools.com}Intermediary_D uses Python identifier Intermediary_D
    __Intermediary_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_D'), 'Intermediary_D', '__httpwww_w3schools_com_MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_httpwww_w3schools_comIntermediary_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1554, 4), )

    
    Intermediary_D = property(__Intermediary_D.value, __Intermediary_D.set, None, None)

    
    # Element {http://www.w3schools.com}Intermediary_J uses Python identifier Intermediary_J
    __Intermediary_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_J'), 'Intermediary_J', '__httpwww_w3schools_com_MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_httpwww_w3schools_comIntermediary_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1555, 4), )

    
    Intermediary_J = property(__Intermediary_J.value, __Intermediary_J.set, None, None)

    
    # Element {http://www.w3schools.com}ReceivingAgent_A uses Python identifier ReceivingAgent_A
    __ReceivingAgent_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_A'), 'ReceivingAgent_A', '__httpwww_w3schools_com_MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_httpwww_w3schools_comReceivingAgent_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1558, 4), )

    
    ReceivingAgent_A = property(__ReceivingAgent_A.value, __ReceivingAgent_A.set, None, None)

    
    # Element {http://www.w3schools.com}ReceivingAgent_D uses Python identifier ReceivingAgent_D
    __ReceivingAgent_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_D'), 'ReceivingAgent_D', '__httpwww_w3schools_com_MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_httpwww_w3schools_comReceivingAgent_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1559, 4), )

    
    ReceivingAgent_D = property(__ReceivingAgent_D.value, __ReceivingAgent_D.set, None, None)

    
    # Element {http://www.w3schools.com}ReceivingAgent_J uses Python identifier ReceivingAgent_J
    __ReceivingAgent_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_J'), 'ReceivingAgent_J', '__httpwww_w3schools_com_MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_httpwww_w3schools_comReceivingAgent_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1560, 4), )

    
    ReceivingAgent_J = property(__ReceivingAgent_J.value, __ReceivingAgent_J.set, None, None)

    
    # Element {http://www.w3schools.com}BeneficiaryInstitution_A uses Python identifier BeneficiaryInstitution_A
    __BeneficiaryInstitution_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_A'), 'BeneficiaryInstitution_A', '__httpwww_w3schools_com_MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_httpwww_w3schools_comBeneficiaryInstitution_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1563, 4), )

    
    BeneficiaryInstitution_A = property(__BeneficiaryInstitution_A.value, __BeneficiaryInstitution_A.set, None, None)

    
    # Element {http://www.w3schools.com}BeneficiaryInstitution_D uses Python identifier BeneficiaryInstitution_D
    __BeneficiaryInstitution_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_D'), 'BeneficiaryInstitution_D', '__httpwww_w3schools_com_MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_httpwww_w3schools_comBeneficiaryInstitution_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1564, 4), )

    
    BeneficiaryInstitution_D = property(__BeneficiaryInstitution_D.value, __BeneficiaryInstitution_D.set, None, None)

    
    # Element {http://www.w3schools.com}BeneficiaryInstitution_J uses Python identifier BeneficiaryInstitution_J
    __BeneficiaryInstitution_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_J'), 'BeneficiaryInstitution_J', '__httpwww_w3schools_com_MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_httpwww_w3schools_comBeneficiaryInstitution_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1565, 4), )

    
    BeneficiaryInstitution_J = property(__BeneficiaryInstitution_J.value, __BeneficiaryInstitution_J.set, None, None)

    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='15F')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1568, 2)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1568, 2)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1569, 2)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1569, 2)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    
    # Attribute formatTag uses Python identifier formatTag
    __formatTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'formatTag'), 'formatTag', '__httpwww_w3schools_com_MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_formatTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='False')
    __formatTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1570, 2)
    __formatTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1570, 2)
    
    formatTag = property(__formatTag.value, __formatTag.set, None, None)

    _ElementMap.update({
        __DeliveryAgent_A.name() : __DeliveryAgent_A,
        __DeliveryAgent_D.name() : __DeliveryAgent_D,
        __DeliveryAgent_J.name() : __DeliveryAgent_J,
        __Intermediary2_A.name() : __Intermediary2_A,
        __Intermediary2_D.name() : __Intermediary2_D,
        __Intermediary2_J.name() : __Intermediary2_J,
        __Intermediary_A.name() : __Intermediary_A,
        __Intermediary_D.name() : __Intermediary_D,
        __Intermediary_J.name() : __Intermediary_J,
        __ReceivingAgent_A.name() : __ReceivingAgent_A,
        __ReceivingAgent_D.name() : __ReceivingAgent_D,
        __ReceivingAgent_J.name() : __ReceivingAgent_J,
        __BeneficiaryInstitution_A.name() : __BeneficiaryInstitution_A,
        __BeneficiaryInstitution_D.name() : __BeneficiaryInstitution_D,
        __BeneficiaryInstitution_J.name() : __BeneficiaryInstitution_J
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory,
        __formatTag.name() : __formatTag
    })
_module_typeBindings.MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB = MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB', MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB)


# Complex type {http://www.w3schools.com}MT330_SequenceG_TaxInformation with content type ELEMENT_ONLY
class MT330_SequenceG_TaxInformation (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceG_TaxInformation with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceG_TaxInformation')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1572, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}TaxRate uses Python identifier TaxRate
    __TaxRate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'TaxRate'), 'TaxRate', '__httpwww_w3schools_com_MT330_SequenceG_TaxInformation_httpwww_w3schools_comTaxRate', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1574, 3), )

    
    TaxRate = property(__TaxRate.value, __TaxRate.set, None, None)

    
    # Element {http://www.w3schools.com}TransactionCurrencyAndNetInterestAmount uses Python identifier TransactionCurrencyAndNetInterestAmount
    __TransactionCurrencyAndNetInterestAmount = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'TransactionCurrencyAndNetInterestAmount'), 'TransactionCurrencyAndNetInterestAmount', '__httpwww_w3schools_com_MT330_SequenceG_TaxInformation_httpwww_w3schools_comTransactionCurrencyAndNetInterestAmount', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1575, 3), )

    
    TransactionCurrencyAndNetInterestAmount = property(__TransactionCurrencyAndNetInterestAmount.value, __TransactionCurrencyAndNetInterestAmount.set, None, None)

    
    # Element {http://www.w3schools.com}ExchangeRate uses Python identifier ExchangeRate
    __ExchangeRate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ExchangeRate'), 'ExchangeRate', '__httpwww_w3schools_com_MT330_SequenceG_TaxInformation_httpwww_w3schools_comExchangeRate', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1576, 3), )

    
    ExchangeRate = property(__ExchangeRate.value, __ExchangeRate.set, None, None)

    
    # Element {http://www.w3schools.com}ReportingCurrencyAndTaxAmount uses Python identifier ReportingCurrencyAndTaxAmount
    __ReportingCurrencyAndTaxAmount = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ReportingCurrencyAndTaxAmount'), 'ReportingCurrencyAndTaxAmount', '__httpwww_w3schools_com_MT330_SequenceG_TaxInformation_httpwww_w3schools_comReportingCurrencyAndTaxAmount', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1577, 3), )

    
    ReportingCurrencyAndTaxAmount = property(__ReportingCurrencyAndTaxAmount.value, __ReportingCurrencyAndTaxAmount.set, None, None)

    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceG_TaxInformation_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='15G')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1579, 2)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1579, 2)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceG_TaxInformation_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1580, 2)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1580, 2)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    
    # Attribute formatTag uses Python identifier formatTag
    __formatTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'formatTag'), 'formatTag', '__httpwww_w3schools_com_MT330_SequenceG_TaxInformation_formatTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='False')
    __formatTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1581, 2)
    __formatTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1581, 2)
    
    formatTag = property(__formatTag.value, __formatTag.set, None, None)

    _ElementMap.update({
        __TaxRate.name() : __TaxRate,
        __TransactionCurrencyAndNetInterestAmount.name() : __TransactionCurrencyAndNetInterestAmount,
        __ExchangeRate.name() : __ExchangeRate,
        __ReportingCurrencyAndTaxAmount.name() : __ReportingCurrencyAndTaxAmount
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory,
        __formatTag.name() : __formatTag
    })
_module_typeBindings.MT330_SequenceG_TaxInformation = MT330_SequenceG_TaxInformation
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceG_TaxInformation', MT330_SequenceG_TaxInformation)


# Complex type {http://www.w3schools.com}MT330_SequenceH_AdditionalInformation with content type ELEMENT_ONLY
class MT330_SequenceH_AdditionalInformation (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceH_AdditionalInformation with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceH_AdditionalInformation')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1583, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}ContactInformation uses Python identifier ContactInformation
    __ContactInformation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ContactInformation'), 'ContactInformation', '__httpwww_w3schools_com_MT330_SequenceH_AdditionalInformation_httpwww_w3schools_comContactInformation', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1585, 3), )

    
    ContactInformation = property(__ContactInformation.value, __ContactInformation.set, None, None)

    
    # Element {http://www.w3schools.com}DealingMethod uses Python identifier DealingMethod
    __DealingMethod = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DealingMethod'), 'DealingMethod', '__httpwww_w3schools_com_MT330_SequenceH_AdditionalInformation_httpwww_w3schools_comDealingMethod', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1586, 3), )

    
    DealingMethod = property(__DealingMethod.value, __DealingMethod.set, None, None)

    
    # Element {http://www.w3schools.com}DealingBranchPartyA_A uses Python identifier DealingBranchPartyA_A
    __DealingBranchPartyA_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DealingBranchPartyA_A'), 'DealingBranchPartyA_A', '__httpwww_w3schools_com_MT330_SequenceH_AdditionalInformation_httpwww_w3schools_comDealingBranchPartyA_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1588, 4), )

    
    DealingBranchPartyA_A = property(__DealingBranchPartyA_A.value, __DealingBranchPartyA_A.set, None, None)

    
    # Element {http://www.w3schools.com}DealingBranchPartyA_B uses Python identifier DealingBranchPartyA_B
    __DealingBranchPartyA_B = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DealingBranchPartyA_B'), 'DealingBranchPartyA_B', '__httpwww_w3schools_com_MT330_SequenceH_AdditionalInformation_httpwww_w3schools_comDealingBranchPartyA_B', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1589, 4), )

    
    DealingBranchPartyA_B = property(__DealingBranchPartyA_B.value, __DealingBranchPartyA_B.set, None, None)

    
    # Element {http://www.w3schools.com}DealingBranchPartyA_D uses Python identifier DealingBranchPartyA_D
    __DealingBranchPartyA_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DealingBranchPartyA_D'), 'DealingBranchPartyA_D', '__httpwww_w3schools_com_MT330_SequenceH_AdditionalInformation_httpwww_w3schools_comDealingBranchPartyA_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1590, 4), )

    
    DealingBranchPartyA_D = property(__DealingBranchPartyA_D.value, __DealingBranchPartyA_D.set, None, None)

    
    # Element {http://www.w3schools.com}DealingBranchPartyA_J uses Python identifier DealingBranchPartyA_J
    __DealingBranchPartyA_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DealingBranchPartyA_J'), 'DealingBranchPartyA_J', '__httpwww_w3schools_com_MT330_SequenceH_AdditionalInformation_httpwww_w3schools_comDealingBranchPartyA_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1591, 4), )

    
    DealingBranchPartyA_J = property(__DealingBranchPartyA_J.value, __DealingBranchPartyA_J.set, None, None)

    
    # Element {http://www.w3schools.com}DealingBranchPartyB_A uses Python identifier DealingBranchPartyB_A
    __DealingBranchPartyB_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DealingBranchPartyB_A'), 'DealingBranchPartyB_A', '__httpwww_w3schools_com_MT330_SequenceH_AdditionalInformation_httpwww_w3schools_comDealingBranchPartyB_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1594, 4), )

    
    DealingBranchPartyB_A = property(__DealingBranchPartyB_A.value, __DealingBranchPartyB_A.set, None, None)

    
    # Element {http://www.w3schools.com}DealingBranchPartyB_B uses Python identifier DealingBranchPartyB_B
    __DealingBranchPartyB_B = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DealingBranchPartyB_B'), 'DealingBranchPartyB_B', '__httpwww_w3schools_com_MT330_SequenceH_AdditionalInformation_httpwww_w3schools_comDealingBranchPartyB_B', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1595, 4), )

    
    DealingBranchPartyB_B = property(__DealingBranchPartyB_B.value, __DealingBranchPartyB_B.set, None, None)

    
    # Element {http://www.w3schools.com}DealingBranchPartyB_D uses Python identifier DealingBranchPartyB_D
    __DealingBranchPartyB_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DealingBranchPartyB_D'), 'DealingBranchPartyB_D', '__httpwww_w3schools_com_MT330_SequenceH_AdditionalInformation_httpwww_w3schools_comDealingBranchPartyB_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1596, 4), )

    
    DealingBranchPartyB_D = property(__DealingBranchPartyB_D.value, __DealingBranchPartyB_D.set, None, None)

    
    # Element {http://www.w3schools.com}DealingBranchPartyB_J uses Python identifier DealingBranchPartyB_J
    __DealingBranchPartyB_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DealingBranchPartyB_J'), 'DealingBranchPartyB_J', '__httpwww_w3schools_com_MT330_SequenceH_AdditionalInformation_httpwww_w3schools_comDealingBranchPartyB_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1597, 4), )

    
    DealingBranchPartyB_J = property(__DealingBranchPartyB_J.value, __DealingBranchPartyB_J.set, None, None)

    
    # Element {http://www.w3schools.com}CounterpartysReference uses Python identifier CounterpartysReference
    __CounterpartysReference = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CounterpartysReference'), 'CounterpartysReference', '__httpwww_w3schools_com_MT330_SequenceH_AdditionalInformation_httpwww_w3schools_comCounterpartysReference', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1599, 3), )

    
    CounterpartysReference = property(__CounterpartysReference.value, __CounterpartysReference.set, None, None)

    
    # Element {http://www.w3schools.com}CommissionAndFees uses Python identifier CommissionAndFees
    __CommissionAndFees = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CommissionAndFees'), 'CommissionAndFees', '__httpwww_w3schools_com_MT330_SequenceH_AdditionalInformation_httpwww_w3schools_comCommissionAndFees', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1600, 3), )

    
    CommissionAndFees = property(__CommissionAndFees.value, __CommissionAndFees.set, None, None)

    
    # Element {http://www.w3schools.com}SenderToReceiverInformation uses Python identifier SenderToReceiverInformation
    __SenderToReceiverInformation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SenderToReceiverInformation'), 'SenderToReceiverInformation', '__httpwww_w3schools_com_MT330_SequenceH_AdditionalInformation_httpwww_w3schools_comSenderToReceiverInformation', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1601, 3), )

    
    SenderToReceiverInformation = property(__SenderToReceiverInformation.value, __SenderToReceiverInformation.set, None, None)

    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceH_AdditionalInformation_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='15H')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1603, 2)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1603, 2)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceH_AdditionalInformation_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1604, 2)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1604, 2)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    
    # Attribute formatTag uses Python identifier formatTag
    __formatTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'formatTag'), 'formatTag', '__httpwww_w3schools_com_MT330_SequenceH_AdditionalInformation_formatTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='False')
    __formatTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1605, 2)
    __formatTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1605, 2)
    
    formatTag = property(__formatTag.value, __formatTag.set, None, None)

    _ElementMap.update({
        __ContactInformation.name() : __ContactInformation,
        __DealingMethod.name() : __DealingMethod,
        __DealingBranchPartyA_A.name() : __DealingBranchPartyA_A,
        __DealingBranchPartyA_B.name() : __DealingBranchPartyA_B,
        __DealingBranchPartyA_D.name() : __DealingBranchPartyA_D,
        __DealingBranchPartyA_J.name() : __DealingBranchPartyA_J,
        __DealingBranchPartyB_A.name() : __DealingBranchPartyB_A,
        __DealingBranchPartyB_B.name() : __DealingBranchPartyB_B,
        __DealingBranchPartyB_D.name() : __DealingBranchPartyB_D,
        __DealingBranchPartyB_J.name() : __DealingBranchPartyB_J,
        __CounterpartysReference.name() : __CounterpartysReference,
        __CommissionAndFees.name() : __CommissionAndFees,
        __SenderToReceiverInformation.name() : __SenderToReceiverInformation
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory,
        __formatTag.name() : __formatTag
    })
_module_typeBindings.MT330_SequenceH_AdditionalInformation = MT330_SequenceH_AdditionalInformation
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceH_AdditionalInformation', MT330_SequenceH_AdditionalInformation)


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1608, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}SequenceA_GeneralInformation uses Python identifier SequenceA_GeneralInformation
    __SequenceA_GeneralInformation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SequenceA_GeneralInformation'), 'SequenceA_GeneralInformation', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comSequenceA_GeneralInformation', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1610, 4), )

    
    SequenceA_GeneralInformation = property(__SequenceA_GeneralInformation.value, __SequenceA_GeneralInformation.set, None, None)

    
    # Element {http://www.w3schools.com}SequenceB_TransactionDetails uses Python identifier SequenceB_TransactionDetails
    __SequenceB_TransactionDetails = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SequenceB_TransactionDetails'), 'SequenceB_TransactionDetails', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comSequenceB_TransactionDetails', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1611, 4), )

    
    SequenceB_TransactionDetails = property(__SequenceB_TransactionDetails.value, __SequenceB_TransactionDetails.set, None, None)

    
    # Element {http://www.w3schools.com}SequenceC_SettlementInstructionsforAmountsPayablebyPartyA uses Python identifier SequenceC_SettlementInstructionsforAmountsPayablebyPartyA
    __SequenceC_SettlementInstructionsforAmountsPayablebyPartyA = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SequenceC_SettlementInstructionsforAmountsPayablebyPartyA'), 'SequenceC_SettlementInstructionsforAmountsPayablebyPartyA', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comSequenceC_SettlementInstructionsforAmountsPayablebyPartyA', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1612, 4), )

    
    SequenceC_SettlementInstructionsforAmountsPayablebyPartyA = property(__SequenceC_SettlementInstructionsforAmountsPayablebyPartyA.value, __SequenceC_SettlementInstructionsforAmountsPayablebyPartyA.set, None, None)

    
    # Element {http://www.w3schools.com}SequenceD_SettlementInstructionsforAmountsPayablebyPartyB uses Python identifier SequenceD_SettlementInstructionsforAmountsPayablebyPartyB
    __SequenceD_SettlementInstructionsforAmountsPayablebyPartyB = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SequenceD_SettlementInstructionsforAmountsPayablebyPartyB'), 'SequenceD_SettlementInstructionsforAmountsPayablebyPartyB', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comSequenceD_SettlementInstructionsforAmountsPayablebyPartyB', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1613, 4), )

    
    SequenceD_SettlementInstructionsforAmountsPayablebyPartyB = property(__SequenceD_SettlementInstructionsforAmountsPayablebyPartyB.value, __SequenceD_SettlementInstructionsforAmountsPayablebyPartyB.set, None, None)

    
    # Element {http://www.w3schools.com}SequenceE_SettlementInstructionsforInterestsPayablebyPartyA uses Python identifier SequenceE_SettlementInstructionsforInterestsPayablebyPartyA
    __SequenceE_SettlementInstructionsforInterestsPayablebyPartyA = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SequenceE_SettlementInstructionsforInterestsPayablebyPartyA'), 'SequenceE_SettlementInstructionsforInterestsPayablebyPartyA', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comSequenceE_SettlementInstructionsforInterestsPayablebyPartyA', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1614, 4), )

    
    SequenceE_SettlementInstructionsforInterestsPayablebyPartyA = property(__SequenceE_SettlementInstructionsforInterestsPayablebyPartyA.value, __SequenceE_SettlementInstructionsforInterestsPayablebyPartyA.set, None, None)

    
    # Element {http://www.w3schools.com}SequenceF_SettlementInstructionsforInterestsPayablebyPartyB uses Python identifier SequenceF_SettlementInstructionsforInterestsPayablebyPartyB
    __SequenceF_SettlementInstructionsforInterestsPayablebyPartyB = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SequenceF_SettlementInstructionsforInterestsPayablebyPartyB'), 'SequenceF_SettlementInstructionsforInterestsPayablebyPartyB', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comSequenceF_SettlementInstructionsforInterestsPayablebyPartyB', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1615, 4), )

    
    SequenceF_SettlementInstructionsforInterestsPayablebyPartyB = property(__SequenceF_SettlementInstructionsforInterestsPayablebyPartyB.value, __SequenceF_SettlementInstructionsforInterestsPayablebyPartyB.set, None, None)

    
    # Element {http://www.w3schools.com}SequenceG_TaxInformation uses Python identifier SequenceG_TaxInformation
    __SequenceG_TaxInformation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SequenceG_TaxInformation'), 'SequenceG_TaxInformation', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comSequenceG_TaxInformation', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1616, 4), )

    
    SequenceG_TaxInformation = property(__SequenceG_TaxInformation.value, __SequenceG_TaxInformation.set, None, None)

    
    # Element {http://www.w3schools.com}SequenceH_AdditionalInformation uses Python identifier SequenceH_AdditionalInformation
    __SequenceH_AdditionalInformation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SequenceH_AdditionalInformation'), 'SequenceH_AdditionalInformation', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comSequenceH_AdditionalInformation', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1617, 4), )

    
    SequenceH_AdditionalInformation = property(__SequenceH_AdditionalInformation.value, __SequenceH_AdditionalInformation.set, None, None)

    _ElementMap.update({
        __SequenceA_GeneralInformation.name() : __SequenceA_GeneralInformation,
        __SequenceB_TransactionDetails.name() : __SequenceB_TransactionDetails,
        __SequenceC_SettlementInstructionsforAmountsPayablebyPartyA.name() : __SequenceC_SettlementInstructionsforAmountsPayablebyPartyA,
        __SequenceD_SettlementInstructionsforAmountsPayablebyPartyB.name() : __SequenceD_SettlementInstructionsforAmountsPayablebyPartyB,
        __SequenceE_SettlementInstructionsforInterestsPayablebyPartyA.name() : __SequenceE_SettlementInstructionsforInterestsPayablebyPartyA,
        __SequenceF_SettlementInstructionsforInterestsPayablebyPartyB.name() : __SequenceF_SettlementInstructionsforInterestsPayablebyPartyB,
        __SequenceG_TaxInformation.name() : __SequenceG_TaxInformation,
        __SequenceH_AdditionalInformation.name() : __SequenceH_AdditionalInformation
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON = CTD_ANON


# Complex type {http://www.w3schools.com}MT330_SequenceA_GeneralInformation_20_Type with content type SIMPLE
class MT330_SequenceA_GeneralInformation_20_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceA_GeneralInformation_20_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceA_GeneralInformation_20_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceA_GeneralInformation_20_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 8, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceA_GeneralInformation_20_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceA_GeneralInformation_20_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='20')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 11, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 11, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceA_GeneralInformation_20_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 12, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 12, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceA_GeneralInformation_20_Type = MT330_SequenceA_GeneralInformation_20_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceA_GeneralInformation_20_Type', MT330_SequenceA_GeneralInformation_20_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceA_GeneralInformation_21_Type with content type SIMPLE
class MT330_SequenceA_GeneralInformation_21_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceA_GeneralInformation_21_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceA_GeneralInformation_21_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceA_GeneralInformation_21_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 21, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceA_GeneralInformation_21_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceA_GeneralInformation_21_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='21')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 24, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 24, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceA_GeneralInformation_21_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 25, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 25, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceA_GeneralInformation_21_Type = MT330_SequenceA_GeneralInformation_21_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceA_GeneralInformation_21_Type', MT330_SequenceA_GeneralInformation_21_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceA_GeneralInformation_22A_Type with content type SIMPLE
class MT330_SequenceA_GeneralInformation_22A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceA_GeneralInformation_22A_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceA_GeneralInformation_22A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceA_GeneralInformation_22A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 34, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceA_GeneralInformation_22A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceA_GeneralInformation_22A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='22A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 37, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 37, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceA_GeneralInformation_22A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 38, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 38, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceA_GeneralInformation_22A_Type = MT330_SequenceA_GeneralInformation_22A_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceA_GeneralInformation_22A_Type', MT330_SequenceA_GeneralInformation_22A_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceA_GeneralInformation_94A_Type with content type SIMPLE
class MT330_SequenceA_GeneralInformation_94A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceA_GeneralInformation_94A_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceA_GeneralInformation_94A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceA_GeneralInformation_94A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 47, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceA_GeneralInformation_94A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceA_GeneralInformation_94A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='94A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 50, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 50, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceA_GeneralInformation_94A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 51, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 51, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceA_GeneralInformation_94A_Type = MT330_SequenceA_GeneralInformation_94A_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceA_GeneralInformation_94A_Type', MT330_SequenceA_GeneralInformation_94A_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceA_GeneralInformation_22B_Type with content type SIMPLE
class MT330_SequenceA_GeneralInformation_22B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceA_GeneralInformation_22B_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceA_GeneralInformation_22B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceA_GeneralInformation_22B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 60, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceA_GeneralInformation_22B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceA_GeneralInformation_22B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='22B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 63, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 63, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceA_GeneralInformation_22B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 64, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 64, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceA_GeneralInformation_22B_Type = MT330_SequenceA_GeneralInformation_22B_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceA_GeneralInformation_22B_Type', MT330_SequenceA_GeneralInformation_22B_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceA_GeneralInformation_22C_Type with content type SIMPLE
class MT330_SequenceA_GeneralInformation_22C_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceA_GeneralInformation_22C_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceA_GeneralInformation_22C_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceA_GeneralInformation_22C_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 73, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceA_GeneralInformation_22C_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceA_GeneralInformation_22C_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='22C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 76, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 76, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceA_GeneralInformation_22C_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 77, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 77, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceA_GeneralInformation_22C_Type = MT330_SequenceA_GeneralInformation_22C_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceA_GeneralInformation_22C_Type', MT330_SequenceA_GeneralInformation_22C_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceA_GeneralInformation_21N_Type with content type SIMPLE
class MT330_SequenceA_GeneralInformation_21N_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceA_GeneralInformation_21N_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceA_GeneralInformation_21N_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceA_GeneralInformation_21N_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 86, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceA_GeneralInformation_21N_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceA_GeneralInformation_21N_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='21N')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 89, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 89, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceA_GeneralInformation_21N_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 90, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 90, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceA_GeneralInformation_21N_Type = MT330_SequenceA_GeneralInformation_21N_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceA_GeneralInformation_21N_Type', MT330_SequenceA_GeneralInformation_21N_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceA_GeneralInformation_82A_Type with content type SIMPLE
class MT330_SequenceA_GeneralInformation_82A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceA_GeneralInformation_82A_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceA_GeneralInformation_82A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceA_GeneralInformation_82A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 99, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceA_GeneralInformation_82A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceA_GeneralInformation_82A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='82A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 102, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 102, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceA_GeneralInformation_82A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 103, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 103, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceA_GeneralInformation_82A_Type = MT330_SequenceA_GeneralInformation_82A_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceA_GeneralInformation_82A_Type', MT330_SequenceA_GeneralInformation_82A_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceA_GeneralInformation_82D_Type with content type SIMPLE
class MT330_SequenceA_GeneralInformation_82D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceA_GeneralInformation_82D_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceA_GeneralInformation_82D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceA_GeneralInformation_82D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 112, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceA_GeneralInformation_82D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceA_GeneralInformation_82D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='82D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 115, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 115, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceA_GeneralInformation_82D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 116, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 116, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceA_GeneralInformation_82D_Type = MT330_SequenceA_GeneralInformation_82D_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceA_GeneralInformation_82D_Type', MT330_SequenceA_GeneralInformation_82D_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceA_GeneralInformation_82J_Type with content type SIMPLE
class MT330_SequenceA_GeneralInformation_82J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceA_GeneralInformation_82J_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceA_GeneralInformation_82J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceA_GeneralInformation_82J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 125, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceA_GeneralInformation_82J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceA_GeneralInformation_82J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='82J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 128, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 128, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceA_GeneralInformation_82J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 129, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 129, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceA_GeneralInformation_82J_Type = MT330_SequenceA_GeneralInformation_82J_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceA_GeneralInformation_82J_Type', MT330_SequenceA_GeneralInformation_82J_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceA_GeneralInformation_87A_Type with content type SIMPLE
class MT330_SequenceA_GeneralInformation_87A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceA_GeneralInformation_87A_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceA_GeneralInformation_87A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceA_GeneralInformation_87A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 138, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceA_GeneralInformation_87A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceA_GeneralInformation_87A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='87A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 141, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 141, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceA_GeneralInformation_87A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 142, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 142, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceA_GeneralInformation_87A_Type = MT330_SequenceA_GeneralInformation_87A_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceA_GeneralInformation_87A_Type', MT330_SequenceA_GeneralInformation_87A_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceA_GeneralInformation_87D_Type with content type SIMPLE
class MT330_SequenceA_GeneralInformation_87D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceA_GeneralInformation_87D_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceA_GeneralInformation_87D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceA_GeneralInformation_87D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 151, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceA_GeneralInformation_87D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceA_GeneralInformation_87D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='87D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 154, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 154, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceA_GeneralInformation_87D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 155, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 155, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceA_GeneralInformation_87D_Type = MT330_SequenceA_GeneralInformation_87D_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceA_GeneralInformation_87D_Type', MT330_SequenceA_GeneralInformation_87D_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceA_GeneralInformation_87J_Type with content type SIMPLE
class MT330_SequenceA_GeneralInformation_87J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceA_GeneralInformation_87J_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceA_GeneralInformation_87J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceA_GeneralInformation_87J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 164, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceA_GeneralInformation_87J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceA_GeneralInformation_87J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='87J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 167, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 167, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceA_GeneralInformation_87J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 168, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 168, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceA_GeneralInformation_87J_Type = MT330_SequenceA_GeneralInformation_87J_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceA_GeneralInformation_87J_Type', MT330_SequenceA_GeneralInformation_87J_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceA_GeneralInformation_83A_Type with content type SIMPLE
class MT330_SequenceA_GeneralInformation_83A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceA_GeneralInformation_83A_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceA_GeneralInformation_83A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceA_GeneralInformation_83A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 177, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceA_GeneralInformation_83A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceA_GeneralInformation_83A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='83A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 180, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 180, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceA_GeneralInformation_83A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 181, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 181, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceA_GeneralInformation_83A_Type = MT330_SequenceA_GeneralInformation_83A_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceA_GeneralInformation_83A_Type', MT330_SequenceA_GeneralInformation_83A_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceA_GeneralInformation_83D_Type with content type SIMPLE
class MT330_SequenceA_GeneralInformation_83D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceA_GeneralInformation_83D_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceA_GeneralInformation_83D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceA_GeneralInformation_83D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 190, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceA_GeneralInformation_83D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceA_GeneralInformation_83D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='83D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 193, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 193, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceA_GeneralInformation_83D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 194, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 194, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceA_GeneralInformation_83D_Type = MT330_SequenceA_GeneralInformation_83D_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceA_GeneralInformation_83D_Type', MT330_SequenceA_GeneralInformation_83D_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceA_GeneralInformation_83J_Type with content type SIMPLE
class MT330_SequenceA_GeneralInformation_83J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceA_GeneralInformation_83J_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceA_GeneralInformation_83J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceA_GeneralInformation_83J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 203, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceA_GeneralInformation_83J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceA_GeneralInformation_83J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='83J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 206, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 206, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceA_GeneralInformation_83J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 207, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 207, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceA_GeneralInformation_83J_Type = MT330_SequenceA_GeneralInformation_83J_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceA_GeneralInformation_83J_Type', MT330_SequenceA_GeneralInformation_83J_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceA_GeneralInformation_77D_Type with content type SIMPLE
class MT330_SequenceA_GeneralInformation_77D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceA_GeneralInformation_77D_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceA_GeneralInformation_77D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceA_GeneralInformation_77D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 216, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceA_GeneralInformation_77D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceA_GeneralInformation_77D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='77D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 219, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 219, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceA_GeneralInformation_77D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 220, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 220, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceA_GeneralInformation_77D_Type = MT330_SequenceA_GeneralInformation_77D_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceA_GeneralInformation_77D_Type', MT330_SequenceA_GeneralInformation_77D_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceB_TransactionDetails_17R_Type with content type SIMPLE
class MT330_SequenceB_TransactionDetails_17R_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceB_TransactionDetails_17R_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceB_TransactionDetails_17R_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceB_TransactionDetails_17R_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 229, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceB_TransactionDetails_17R_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceB_TransactionDetails_17R_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='17R')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 232, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 232, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceB_TransactionDetails_17R_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 233, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 233, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceB_TransactionDetails_17R_Type = MT330_SequenceB_TransactionDetails_17R_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceB_TransactionDetails_17R_Type', MT330_SequenceB_TransactionDetails_17R_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceB_TransactionDetails_30T_Type with content type SIMPLE
class MT330_SequenceB_TransactionDetails_30T_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceB_TransactionDetails_30T_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceB_TransactionDetails_30T_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceB_TransactionDetails_30T_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 242, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceB_TransactionDetails_30T_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceB_TransactionDetails_30T_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='30T')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 245, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 245, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceB_TransactionDetails_30T_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 246, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 246, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceB_TransactionDetails_30T_Type = MT330_SequenceB_TransactionDetails_30T_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceB_TransactionDetails_30T_Type', MT330_SequenceB_TransactionDetails_30T_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceB_TransactionDetails_30V_Type with content type SIMPLE
class MT330_SequenceB_TransactionDetails_30V_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceB_TransactionDetails_30V_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceB_TransactionDetails_30V_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceB_TransactionDetails_30V_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 255, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceB_TransactionDetails_30V_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceB_TransactionDetails_30V_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='30V')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 258, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 258, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceB_TransactionDetails_30V_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 259, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 259, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceB_TransactionDetails_30V_Type = MT330_SequenceB_TransactionDetails_30V_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceB_TransactionDetails_30V_Type', MT330_SequenceB_TransactionDetails_30V_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceB_TransactionDetails_38A_Type with content type SIMPLE
class MT330_SequenceB_TransactionDetails_38A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceB_TransactionDetails_38A_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceB_TransactionDetails_38A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceB_TransactionDetails_38A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 268, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceB_TransactionDetails_38A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceB_TransactionDetails_38A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='38A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 271, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 271, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceB_TransactionDetails_38A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 272, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 272, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceB_TransactionDetails_38A_Type = MT330_SequenceB_TransactionDetails_38A_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceB_TransactionDetails_38A_Type', MT330_SequenceB_TransactionDetails_38A_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceB_TransactionDetails_32B_Type with content type SIMPLE
class MT330_SequenceB_TransactionDetails_32B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceB_TransactionDetails_32B_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceB_TransactionDetails_32B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceB_TransactionDetails_32B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 281, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceB_TransactionDetails_32B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceB_TransactionDetails_32B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='32B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 284, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 284, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceB_TransactionDetails_32B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 285, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 285, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceB_TransactionDetails_32B_Type = MT330_SequenceB_TransactionDetails_32B_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceB_TransactionDetails_32B_Type', MT330_SequenceB_TransactionDetails_32B_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceB_TransactionDetails_32H_Type with content type SIMPLE
class MT330_SequenceB_TransactionDetails_32H_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceB_TransactionDetails_32H_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceB_TransactionDetails_32H_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceB_TransactionDetails_32H_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 294, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceB_TransactionDetails_32H_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceB_TransactionDetails_32H_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='32H')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 297, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 297, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceB_TransactionDetails_32H_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 298, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 298, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceB_TransactionDetails_32H_Type = MT330_SequenceB_TransactionDetails_32H_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceB_TransactionDetails_32H_Type', MT330_SequenceB_TransactionDetails_32H_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceB_TransactionDetails_30X_Type with content type SIMPLE
class MT330_SequenceB_TransactionDetails_30X_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceB_TransactionDetails_30X_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceB_TransactionDetails_30X_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceB_TransactionDetails_30X_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 307, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceB_TransactionDetails_30X_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceB_TransactionDetails_30X_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='30X')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 310, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 310, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceB_TransactionDetails_30X_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 311, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 311, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceB_TransactionDetails_30X_Type = MT330_SequenceB_TransactionDetails_30X_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceB_TransactionDetails_30X_Type', MT330_SequenceB_TransactionDetails_30X_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceB_TransactionDetails_34E_Type with content type SIMPLE
class MT330_SequenceB_TransactionDetails_34E_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceB_TransactionDetails_34E_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceB_TransactionDetails_34E_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceB_TransactionDetails_34E_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 320, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceB_TransactionDetails_34E_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceB_TransactionDetails_34E_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='34E')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 323, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 323, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceB_TransactionDetails_34E_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 324, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 324, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceB_TransactionDetails_34E_Type = MT330_SequenceB_TransactionDetails_34E_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceB_TransactionDetails_34E_Type', MT330_SequenceB_TransactionDetails_34E_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceB_TransactionDetails_37G_Type with content type SIMPLE
class MT330_SequenceB_TransactionDetails_37G_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceB_TransactionDetails_37G_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceB_TransactionDetails_37G_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceB_TransactionDetails_37G_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 333, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceB_TransactionDetails_37G_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceB_TransactionDetails_37G_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='37G')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 336, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 336, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceB_TransactionDetails_37G_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 337, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 337, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceB_TransactionDetails_37G_Type = MT330_SequenceB_TransactionDetails_37G_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceB_TransactionDetails_37G_Type', MT330_SequenceB_TransactionDetails_37G_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceB_TransactionDetails_14D_Type with content type SIMPLE
class MT330_SequenceB_TransactionDetails_14D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceB_TransactionDetails_14D_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceB_TransactionDetails_14D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceB_TransactionDetails_14D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 346, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceB_TransactionDetails_14D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceB_TransactionDetails_14D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='14D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 349, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 349, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceB_TransactionDetails_14D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 350, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 350, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceB_TransactionDetails_14D_Type = MT330_SequenceB_TransactionDetails_14D_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceB_TransactionDetails_14D_Type', MT330_SequenceB_TransactionDetails_14D_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceB_TransactionDetails_30F_Type with content type SIMPLE
class MT330_SequenceB_TransactionDetails_30F_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceB_TransactionDetails_30F_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceB_TransactionDetails_30F_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceB_TransactionDetails_30F_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 359, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceB_TransactionDetails_30F_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceB_TransactionDetails_30F_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='30F')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 362, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 362, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceB_TransactionDetails_30F_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 363, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 363, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceB_TransactionDetails_30F_Type = MT330_SequenceB_TransactionDetails_30F_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceB_TransactionDetails_30F_Type', MT330_SequenceB_TransactionDetails_30F_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceB_TransactionDetails_38J_Type with content type SIMPLE
class MT330_SequenceB_TransactionDetails_38J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceB_TransactionDetails_38J_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceB_TransactionDetails_38J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceB_TransactionDetails_38J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 372, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceB_TransactionDetails_38J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceB_TransactionDetails_38J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='38J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 375, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 375, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceB_TransactionDetails_38J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 376, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 376, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceB_TransactionDetails_38J_Type = MT330_SequenceB_TransactionDetails_38J_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceB_TransactionDetails_38J_Type', MT330_SequenceB_TransactionDetails_38J_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceB_TransactionDetails_39M_Type with content type SIMPLE
class MT330_SequenceB_TransactionDetails_39M_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceB_TransactionDetails_39M_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceB_TransactionDetails_39M_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceB_TransactionDetails_39M_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 385, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceB_TransactionDetails_39M_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceB_TransactionDetails_39M_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='39M')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 388, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 388, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceB_TransactionDetails_39M_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 389, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 389, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceB_TransactionDetails_39M_Type = MT330_SequenceB_TransactionDetails_39M_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceB_TransactionDetails_39M_Type', MT330_SequenceB_TransactionDetails_39M_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53A_Type with content type SIMPLE
class MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53A_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 398, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='53A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 401, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 401, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 402, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 402, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53A_Type = MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53A_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53A_Type', MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53A_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53D_Type with content type SIMPLE
class MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53D_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 411, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='53D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 414, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 414, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 415, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 415, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53D_Type = MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53D_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53D_Type', MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53D_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53J_Type with content type SIMPLE
class MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53J_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 424, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='53J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 427, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 427, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 428, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 428, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53J_Type = MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53J_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53J_Type', MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53J_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86A_Type with content type SIMPLE
class MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86A_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 437, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='86A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 440, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 440, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 441, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 441, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86A_Type = MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86A_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86A_Type', MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86A_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86D_Type with content type SIMPLE
class MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86D_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 450, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='86D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 453, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 453, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 454, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 454, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86D_Type = MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86D_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86D_Type', MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86D_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86J_Type with content type SIMPLE
class MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86J_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 463, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='86J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 466, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 466, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 467, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 467, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86J_Type = MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86J_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86J_Type', MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86J_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56A_Type with content type SIMPLE
class MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56A_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 476, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='56A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 479, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 479, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 480, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 480, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56A_Type = MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56A_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56A_Type', MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56A_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56D_Type with content type SIMPLE
class MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56D_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 489, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='56D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 492, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 492, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 493, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 493, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56D_Type = MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56D_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56D_Type', MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56D_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56J_Type with content type SIMPLE
class MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56J_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 502, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='56J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 505, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 505, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 506, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 506, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56J_Type = MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56J_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56J_Type', MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56J_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57A_Type with content type SIMPLE
class MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57A_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 515, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='57A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 518, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 518, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 519, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 519, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57A_Type = MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57A_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57A_Type', MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57A_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57D_Type with content type SIMPLE
class MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57D_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 528, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='57D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 531, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 531, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 532, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 532, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57D_Type = MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57D_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57D_Type', MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57D_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57J_Type with content type SIMPLE
class MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57J_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 541, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='57J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 544, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 544, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 545, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 545, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57J_Type = MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57J_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57J_Type', MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57J_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58A_Type with content type SIMPLE
class MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58A_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 554, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='58A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 557, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 557, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 558, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 558, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58A_Type = MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58A_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58A_Type', MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58A_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58D_Type with content type SIMPLE
class MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58D_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 567, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='58D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 570, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 570, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 571, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 571, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58D_Type = MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58D_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58D_Type', MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58D_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58J_Type with content type SIMPLE
class MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58J_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 580, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='58J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 583, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 583, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 584, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 584, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58J_Type = MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58J_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58J_Type', MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58J_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53A_Type with content type SIMPLE
class MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53A_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 593, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='53A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 596, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 596, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 597, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 597, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53A_Type = MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53A_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53A_Type', MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53A_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53D_Type with content type SIMPLE
class MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53D_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 606, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='53D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 609, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 609, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 610, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 610, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53D_Type = MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53D_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53D_Type', MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53D_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53J_Type with content type SIMPLE
class MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53J_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 619, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='53J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 622, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 622, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 623, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 623, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53J_Type = MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53J_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53J_Type', MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53J_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86A_Type with content type SIMPLE
class MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86A_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 632, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='86A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 635, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 635, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 636, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 636, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86A_Type = MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86A_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86A_Type', MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86A_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86D_Type with content type SIMPLE
class MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86D_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 645, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='86D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 648, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 648, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 649, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 649, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86D_Type = MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86D_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86D_Type', MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86D_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86J_Type with content type SIMPLE
class MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86J_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 658, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='86J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 661, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 661, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 662, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 662, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86J_Type = MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86J_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86J_Type', MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86J_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56A_Type with content type SIMPLE
class MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56A_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 671, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='56A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 674, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 674, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 675, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 675, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56A_Type = MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56A_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56A_Type', MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56A_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56D_Type with content type SIMPLE
class MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56D_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 684, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='56D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 687, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 687, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 688, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 688, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56D_Type = MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56D_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56D_Type', MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56D_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56J_Type with content type SIMPLE
class MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56J_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 697, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='56J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 700, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 700, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 701, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 701, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56J_Type = MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56J_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56J_Type', MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56J_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57A_Type with content type SIMPLE
class MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57A_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 710, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='57A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 713, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 713, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 714, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 714, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57A_Type = MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57A_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57A_Type', MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57A_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57D_Type with content type SIMPLE
class MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57D_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 723, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='57D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 726, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 726, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 727, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 727, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57D_Type = MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57D_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57D_Type', MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57D_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57J_Type with content type SIMPLE
class MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57J_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 736, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='57J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 739, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 739, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 740, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 740, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57J_Type = MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57J_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57J_Type', MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57J_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58A_Type with content type SIMPLE
class MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58A_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 749, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='58A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 752, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 752, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 753, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 753, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58A_Type = MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58A_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58A_Type', MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58A_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58D_Type with content type SIMPLE
class MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58D_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 762, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='58D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 765, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 765, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 766, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 766, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58D_Type = MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58D_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58D_Type', MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58D_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58J_Type with content type SIMPLE
class MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58J_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 775, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='58J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 778, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 778, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 779, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 779, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58J_Type = MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58J_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58J_Type', MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58J_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53A_Type with content type SIMPLE
class MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53A_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 788, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='53A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 791, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 791, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 792, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 792, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53A_Type = MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53A_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53A_Type', MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53A_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53D_Type with content type SIMPLE
class MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53D_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 801, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='53D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 804, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 804, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 805, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 805, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53D_Type = MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53D_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53D_Type', MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53D_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53J_Type with content type SIMPLE
class MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53J_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 814, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='53J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 817, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 817, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 818, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 818, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53J_Type = MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53J_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53J_Type', MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53J_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86A_Type with content type SIMPLE
class MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86A_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 827, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='86A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 830, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 830, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 831, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 831, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86A_Type = MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86A_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86A_Type', MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86A_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86D_Type with content type SIMPLE
class MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86D_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 840, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='86D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 843, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 843, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 844, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 844, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86D_Type = MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86D_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86D_Type', MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86D_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86J_Type with content type SIMPLE
class MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86J_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 853, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='86J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 856, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 856, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 857, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 857, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86J_Type = MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86J_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86J_Type', MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86J_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56A_Type with content type SIMPLE
class MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56A_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 866, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='56A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 869, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 869, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 870, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 870, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56A_Type = MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56A_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56A_Type', MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56A_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56D_Type with content type SIMPLE
class MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56D_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 879, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='56D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 882, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 882, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 883, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 883, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56D_Type = MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56D_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56D_Type', MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56D_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56J_Type with content type SIMPLE
class MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56J_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 892, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='56J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 895, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 895, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 896, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 896, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56J_Type = MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56J_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56J_Type', MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56J_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57A_Type with content type SIMPLE
class MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57A_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 905, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='57A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 908, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 908, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 909, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 909, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57A_Type = MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57A_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57A_Type', MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57A_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57D_Type with content type SIMPLE
class MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57D_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 918, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='57D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 921, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 921, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 922, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 922, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57D_Type = MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57D_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57D_Type', MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57D_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57J_Type with content type SIMPLE
class MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57J_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 931, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='57J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 934, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 934, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 935, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 935, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57J_Type = MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57J_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57J_Type', MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57J_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58A_Type with content type SIMPLE
class MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58A_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 944, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='58A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 947, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 947, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 948, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 948, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58A_Type = MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58A_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58A_Type', MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58A_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58D_Type with content type SIMPLE
class MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58D_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 957, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='58D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 960, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 960, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 961, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 961, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58D_Type = MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58D_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58D_Type', MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58D_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58J_Type with content type SIMPLE
class MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58J_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 970, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='58J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 973, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 973, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 974, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 974, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58J_Type = MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58J_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58J_Type', MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58J_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53A_Type with content type SIMPLE
class MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53A_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 983, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='53A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 986, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 986, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 987, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 987, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53A_Type = MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53A_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53A_Type', MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53A_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53D_Type with content type SIMPLE
class MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53D_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 996, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='53D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 999, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 999, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1000, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1000, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53D_Type = MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53D_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53D_Type', MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53D_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53J_Type with content type SIMPLE
class MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53J_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1009, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='53J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1012, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1012, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1013, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1013, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53J_Type = MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53J_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53J_Type', MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53J_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86A_Type with content type SIMPLE
class MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86A_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1022, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='86A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1025, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1025, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1026, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1026, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86A_Type = MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86A_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86A_Type', MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86A_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86D_Type with content type SIMPLE
class MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86D_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1035, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='86D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1038, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1038, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1039, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1039, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86D_Type = MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86D_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86D_Type', MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86D_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86J_Type with content type SIMPLE
class MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86J_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1048, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='86J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1051, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1051, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1052, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1052, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86J_Type = MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86J_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86J_Type', MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86J_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56A_Type with content type SIMPLE
class MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56A_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1061, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='56A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1064, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1064, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1065, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1065, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56A_Type = MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56A_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56A_Type', MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56A_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56D_Type with content type SIMPLE
class MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56D_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1074, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='56D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1077, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1077, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1078, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1078, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56D_Type = MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56D_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56D_Type', MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56D_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56J_Type with content type SIMPLE
class MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56J_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1087, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='56J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1090, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1090, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1091, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1091, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56J_Type = MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56J_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56J_Type', MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56J_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57A_Type with content type SIMPLE
class MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57A_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1100, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='57A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1103, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1103, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1104, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1104, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57A_Type = MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57A_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57A_Type', MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57A_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57D_Type with content type SIMPLE
class MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57D_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1113, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='57D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1116, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1116, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1117, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1117, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57D_Type = MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57D_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57D_Type', MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57D_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57J_Type with content type SIMPLE
class MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57J_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1126, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='57J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1129, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1129, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1130, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1130, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57J_Type = MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57J_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57J_Type', MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57J_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58A_Type with content type SIMPLE
class MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58A_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1139, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='58A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1142, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1142, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1143, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1143, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58A_Type = MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58A_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58A_Type', MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58A_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58D_Type with content type SIMPLE
class MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58D_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1152, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='58D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1155, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1155, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1156, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1156, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58D_Type = MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58D_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58D_Type', MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58D_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58J_Type with content type SIMPLE
class MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58J_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1165, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='58J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1168, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1168, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1169, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1169, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58J_Type = MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58J_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58J_Type', MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58J_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceG_TaxInformation_37L_Type with content type SIMPLE
class MT330_SequenceG_TaxInformation_37L_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceG_TaxInformation_37L_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceG_TaxInformation_37L_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceG_TaxInformation_37L_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1178, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceG_TaxInformation_37L_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceG_TaxInformation_37L_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='37L')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1181, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1181, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceG_TaxInformation_37L_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1182, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1182, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceG_TaxInformation_37L_Type = MT330_SequenceG_TaxInformation_37L_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceG_TaxInformation_37L_Type', MT330_SequenceG_TaxInformation_37L_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceG_TaxInformation_33B_Type with content type SIMPLE
class MT330_SequenceG_TaxInformation_33B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceG_TaxInformation_33B_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceG_TaxInformation_33B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceG_TaxInformation_33B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1191, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceG_TaxInformation_33B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceG_TaxInformation_33B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='33B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1194, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1194, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceG_TaxInformation_33B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1195, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1195, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceG_TaxInformation_33B_Type = MT330_SequenceG_TaxInformation_33B_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceG_TaxInformation_33B_Type', MT330_SequenceG_TaxInformation_33B_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceG_TaxInformation_36_Type with content type SIMPLE
class MT330_SequenceG_TaxInformation_36_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceG_TaxInformation_36_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceG_TaxInformation_36_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceG_TaxInformation_36_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1204, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceG_TaxInformation_36_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceG_TaxInformation_36_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='36')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1207, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1207, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceG_TaxInformation_36_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1208, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1208, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceG_TaxInformation_36_Type = MT330_SequenceG_TaxInformation_36_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceG_TaxInformation_36_Type', MT330_SequenceG_TaxInformation_36_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceG_TaxInformation_33E_Type with content type SIMPLE
class MT330_SequenceG_TaxInformation_33E_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceG_TaxInformation_33E_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceG_TaxInformation_33E_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceG_TaxInformation_33E_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1217, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceG_TaxInformation_33E_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceG_TaxInformation_33E_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='33E')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1220, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1220, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceG_TaxInformation_33E_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1221, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1221, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceG_TaxInformation_33E_Type = MT330_SequenceG_TaxInformation_33E_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceG_TaxInformation_33E_Type', MT330_SequenceG_TaxInformation_33E_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceH_AdditionalInformation_29A_Type with content type SIMPLE
class MT330_SequenceH_AdditionalInformation_29A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceH_AdditionalInformation_29A_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceH_AdditionalInformation_29A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceH_AdditionalInformation_29A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1230, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceH_AdditionalInformation_29A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceH_AdditionalInformation_29A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='29A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1233, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1233, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceH_AdditionalInformation_29A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1234, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1234, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceH_AdditionalInformation_29A_Type = MT330_SequenceH_AdditionalInformation_29A_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceH_AdditionalInformation_29A_Type', MT330_SequenceH_AdditionalInformation_29A_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceH_AdditionalInformation_24D_Type with content type SIMPLE
class MT330_SequenceH_AdditionalInformation_24D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceH_AdditionalInformation_24D_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceH_AdditionalInformation_24D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceH_AdditionalInformation_24D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1243, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceH_AdditionalInformation_24D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceH_AdditionalInformation_24D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='24D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1246, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1246, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceH_AdditionalInformation_24D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1247, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1247, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceH_AdditionalInformation_24D_Type = MT330_SequenceH_AdditionalInformation_24D_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceH_AdditionalInformation_24D_Type', MT330_SequenceH_AdditionalInformation_24D_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceH_AdditionalInformation_84A_Type with content type SIMPLE
class MT330_SequenceH_AdditionalInformation_84A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceH_AdditionalInformation_84A_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceH_AdditionalInformation_84A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceH_AdditionalInformation_84A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1256, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceH_AdditionalInformation_84A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceH_AdditionalInformation_84A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='84A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1259, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1259, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceH_AdditionalInformation_84A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1260, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1260, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceH_AdditionalInformation_84A_Type = MT330_SequenceH_AdditionalInformation_84A_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceH_AdditionalInformation_84A_Type', MT330_SequenceH_AdditionalInformation_84A_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceH_AdditionalInformation_84B_Type with content type SIMPLE
class MT330_SequenceH_AdditionalInformation_84B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceH_AdditionalInformation_84B_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceH_AdditionalInformation_84B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceH_AdditionalInformation_84B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1269, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceH_AdditionalInformation_84B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceH_AdditionalInformation_84B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='84B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1272, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1272, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceH_AdditionalInformation_84B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1273, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1273, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceH_AdditionalInformation_84B_Type = MT330_SequenceH_AdditionalInformation_84B_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceH_AdditionalInformation_84B_Type', MT330_SequenceH_AdditionalInformation_84B_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceH_AdditionalInformation_84D_Type with content type SIMPLE
class MT330_SequenceH_AdditionalInformation_84D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceH_AdditionalInformation_84D_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceH_AdditionalInformation_84D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceH_AdditionalInformation_84D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1282, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceH_AdditionalInformation_84D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceH_AdditionalInformation_84D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='84D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1285, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1285, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceH_AdditionalInformation_84D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1286, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1286, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceH_AdditionalInformation_84D_Type = MT330_SequenceH_AdditionalInformation_84D_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceH_AdditionalInformation_84D_Type', MT330_SequenceH_AdditionalInformation_84D_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceH_AdditionalInformation_84J_Type with content type SIMPLE
class MT330_SequenceH_AdditionalInformation_84J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceH_AdditionalInformation_84J_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceH_AdditionalInformation_84J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceH_AdditionalInformation_84J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1295, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceH_AdditionalInformation_84J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceH_AdditionalInformation_84J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='84J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1298, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1298, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceH_AdditionalInformation_84J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1299, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1299, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceH_AdditionalInformation_84J_Type = MT330_SequenceH_AdditionalInformation_84J_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceH_AdditionalInformation_84J_Type', MT330_SequenceH_AdditionalInformation_84J_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceH_AdditionalInformation_85A_Type with content type SIMPLE
class MT330_SequenceH_AdditionalInformation_85A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceH_AdditionalInformation_85A_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceH_AdditionalInformation_85A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceH_AdditionalInformation_85A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1308, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceH_AdditionalInformation_85A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceH_AdditionalInformation_85A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='85A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1311, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1311, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceH_AdditionalInformation_85A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1312, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1312, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceH_AdditionalInformation_85A_Type = MT330_SequenceH_AdditionalInformation_85A_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceH_AdditionalInformation_85A_Type', MT330_SequenceH_AdditionalInformation_85A_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceH_AdditionalInformation_85B_Type with content type SIMPLE
class MT330_SequenceH_AdditionalInformation_85B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceH_AdditionalInformation_85B_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceH_AdditionalInformation_85B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceH_AdditionalInformation_85B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1321, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceH_AdditionalInformation_85B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceH_AdditionalInformation_85B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='85B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1324, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1324, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceH_AdditionalInformation_85B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1325, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1325, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceH_AdditionalInformation_85B_Type = MT330_SequenceH_AdditionalInformation_85B_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceH_AdditionalInformation_85B_Type', MT330_SequenceH_AdditionalInformation_85B_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceH_AdditionalInformation_85D_Type with content type SIMPLE
class MT330_SequenceH_AdditionalInformation_85D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceH_AdditionalInformation_85D_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceH_AdditionalInformation_85D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceH_AdditionalInformation_85D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1334, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceH_AdditionalInformation_85D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceH_AdditionalInformation_85D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='85D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1337, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1337, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceH_AdditionalInformation_85D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1338, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1338, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceH_AdditionalInformation_85D_Type = MT330_SequenceH_AdditionalInformation_85D_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceH_AdditionalInformation_85D_Type', MT330_SequenceH_AdditionalInformation_85D_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceH_AdditionalInformation_85J_Type with content type SIMPLE
class MT330_SequenceH_AdditionalInformation_85J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceH_AdditionalInformation_85J_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceH_AdditionalInformation_85J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceH_AdditionalInformation_85J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1347, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceH_AdditionalInformation_85J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceH_AdditionalInformation_85J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='85J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1350, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1350, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceH_AdditionalInformation_85J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1351, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1351, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceH_AdditionalInformation_85J_Type = MT330_SequenceH_AdditionalInformation_85J_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceH_AdditionalInformation_85J_Type', MT330_SequenceH_AdditionalInformation_85J_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceH_AdditionalInformation_26H_Type with content type SIMPLE
class MT330_SequenceH_AdditionalInformation_26H_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceH_AdditionalInformation_26H_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceH_AdditionalInformation_26H_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceH_AdditionalInformation_26H_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1360, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceH_AdditionalInformation_26H_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceH_AdditionalInformation_26H_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='26H')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1363, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1363, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceH_AdditionalInformation_26H_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1364, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1364, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceH_AdditionalInformation_26H_Type = MT330_SequenceH_AdditionalInformation_26H_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceH_AdditionalInformation_26H_Type', MT330_SequenceH_AdditionalInformation_26H_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceH_AdditionalInformation_34C_Type with content type SIMPLE
class MT330_SequenceH_AdditionalInformation_34C_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceH_AdditionalInformation_34C_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceH_AdditionalInformation_34C_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceH_AdditionalInformation_34C_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1373, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceH_AdditionalInformation_34C_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceH_AdditionalInformation_34C_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='34C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1376, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1376, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceH_AdditionalInformation_34C_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1377, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1377, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceH_AdditionalInformation_34C_Type = MT330_SequenceH_AdditionalInformation_34C_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceH_AdditionalInformation_34C_Type', MT330_SequenceH_AdditionalInformation_34C_Type)


# Complex type {http://www.w3schools.com}MT330_SequenceH_AdditionalInformation_72_Type with content type SIMPLE
class MT330_SequenceH_AdditionalInformation_72_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT330_SequenceH_AdditionalInformation_72_Type with content type SIMPLE"""
    _TypeDefinition = MT330_SequenceH_AdditionalInformation_72_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT330_SequenceH_AdditionalInformation_72_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1386, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT330_SequenceH_AdditionalInformation_72_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT330_SequenceH_AdditionalInformation_72_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='72')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1389, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1389, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT330_SequenceH_AdditionalInformation_72_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1390, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1390, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT330_SequenceH_AdditionalInformation_72_Type = MT330_SequenceH_AdditionalInformation_72_Type
Namespace.addCategoryObject('typeBinding', 'MT330_SequenceH_AdditionalInformation_72_Type', MT330_SequenceH_AdditionalInformation_72_Type)


MT330 = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'MT330'), CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1607, 1))
Namespace.addCategoryObject('elementBinding', MT330.name().localName(), MT330)



MT330_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SendersReference'), MT330_SequenceA_GeneralInformation_20_Type, scope=MT330_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1396, 3)))

MT330_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'RelatedReference'), MT330_SequenceA_GeneralInformation_21_Type, scope=MT330_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1397, 3)))

MT330_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TypeOfOperation'), MT330_SequenceA_GeneralInformation_22A_Type, scope=MT330_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1398, 3)))

MT330_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ScopeOfOperation'), MT330_SequenceA_GeneralInformation_94A_Type, scope=MT330_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1399, 3)))

MT330_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TypeOfEvent'), MT330_SequenceA_GeneralInformation_22B_Type, scope=MT330_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1400, 3)))

MT330_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CommonReference'), MT330_SequenceA_GeneralInformation_22C_Type, scope=MT330_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1401, 3)))

MT330_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ContractNumberPartyA'), MT330_SequenceA_GeneralInformation_21N_Type, scope=MT330_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1402, 3)))

MT330_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PartyA_A'), MT330_SequenceA_GeneralInformation_82A_Type, scope=MT330_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1404, 4)))

MT330_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PartyA_D'), MT330_SequenceA_GeneralInformation_82D_Type, scope=MT330_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1405, 4)))

MT330_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PartyA_J'), MT330_SequenceA_GeneralInformation_82J_Type, scope=MT330_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1406, 4)))

MT330_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PartyB_A'), MT330_SequenceA_GeneralInformation_87A_Type, scope=MT330_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1409, 4)))

MT330_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PartyB_D'), MT330_SequenceA_GeneralInformation_87D_Type, scope=MT330_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1410, 4)))

MT330_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PartyB_J'), MT330_SequenceA_GeneralInformation_87J_Type, scope=MT330_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1411, 4)))

MT330_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'FundOrInstructingParty_A'), MT330_SequenceA_GeneralInformation_83A_Type, scope=MT330_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1414, 4)))

MT330_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'FundOrInstructingParty_D'), MT330_SequenceA_GeneralInformation_83D_Type, scope=MT330_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1415, 4)))

MT330_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'FundOrInstructingParty_J'), MT330_SequenceA_GeneralInformation_83J_Type, scope=MT330_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1416, 4)))

MT330_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TermsAndConditions'), MT330_SequenceA_GeneralInformation_77D_Type, scope=MT330_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1418, 3)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1397, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1399, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1402, 3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1413, 3))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1414, 4))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1415, 4))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1416, 4))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1418, 3))
    counters.add(cc_7)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SendersReference')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1396, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'RelatedReference')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1397, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'TypeOfOperation')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1398, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ScopeOfOperation')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1399, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'TypeOfEvent')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1400, 3))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CommonReference')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1401, 3))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ContractNumberPartyA')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1402, 3))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PartyA_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1404, 4))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PartyA_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1405, 4))
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PartyA_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1406, 4))
    st_9 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PartyB_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1409, 4))
    st_10 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PartyB_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1410, 4))
    st_11 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PartyB_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1411, 4))
    st_12 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_12)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'FundOrInstructingParty_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1414, 4))
    st_13 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_13)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'FundOrInstructingParty_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1415, 4))
    st_14 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_14)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    final_update.add(fac.UpdateInstruction(cc_6, False))
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'FundOrInstructingParty_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1416, 4))
    st_15 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_15)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_7, False))
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'TermsAndConditions')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1418, 3))
    st_16 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_16)
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
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
         ]))
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
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_10, [
         ]))
    transitions.append(fac.Transition(st_11, [
         ]))
    transitions.append(fac.Transition(st_12, [
         ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_10, [
         ]))
    transitions.append(fac.Transition(st_11, [
         ]))
    transitions.append(fac.Transition(st_12, [
         ]))
    st_8._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_10, [
         ]))
    transitions.append(fac.Transition(st_11, [
         ]))
    transitions.append(fac.Transition(st_12, [
         ]))
    st_9._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_13, [
         ]))
    transitions.append(fac.Transition(st_14, [
         ]))
    transitions.append(fac.Transition(st_15, [
         ]))
    transitions.append(fac.Transition(st_16, [
         ]))
    st_10._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_13, [
         ]))
    transitions.append(fac.Transition(st_14, [
         ]))
    transitions.append(fac.Transition(st_15, [
         ]))
    transitions.append(fac.Transition(st_16, [
         ]))
    st_11._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_13, [
         ]))
    transitions.append(fac.Transition(st_14, [
         ]))
    transitions.append(fac.Transition(st_15, [
         ]))
    transitions.append(fac.Transition(st_16, [
         ]))
    st_12._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_3, True),
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_3, True),
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_3, True),
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_3, False),
        fac.UpdateInstruction(cc_4, False) ]))
    st_13._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_3, True),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_3, True),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_5, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_3, True),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_3, False),
        fac.UpdateInstruction(cc_5, False) ]))
    st_14._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_3, True),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_3, True),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_3, True),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_6, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_3, False),
        fac.UpdateInstruction(cc_6, False) ]))
    st_15._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_7, True) ]))
    st_16._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
MT330_SequenceA_GeneralInformation._Automaton = _BuildAutomaton()




MT330_SequenceB_TransactionDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PartyAsRole'), MT330_SequenceB_TransactionDetails_17R_Type, scope=MT330_SequenceB_TransactionDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1426, 3)))

MT330_SequenceB_TransactionDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TradeDate'), MT330_SequenceB_TransactionDetails_30T_Type, scope=MT330_SequenceB_TransactionDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1427, 3)))

MT330_SequenceB_TransactionDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ValueDate'), MT330_SequenceB_TransactionDetails_30V_Type, scope=MT330_SequenceB_TransactionDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1428, 3)))

MT330_SequenceB_TransactionDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PeriodOfNotice'), MT330_SequenceB_TransactionDetails_38A_Type, scope=MT330_SequenceB_TransactionDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1429, 3)))

MT330_SequenceB_TransactionDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CurrencyAndBalance'), MT330_SequenceB_TransactionDetails_32B_Type, scope=MT330_SequenceB_TransactionDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1430, 3)))

MT330_SequenceB_TransactionDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PrincipalAmountToBeSettled'), MT330_SequenceB_TransactionDetails_32H_Type, scope=MT330_SequenceB_TransactionDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1431, 3)))

MT330_SequenceB_TransactionDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'InterestDueDate'), MT330_SequenceB_TransactionDetails_30X_Type, scope=MT330_SequenceB_TransactionDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1432, 3)))

MT330_SequenceB_TransactionDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CurrencyAndInterestAmount'), MT330_SequenceB_TransactionDetails_34E_Type, scope=MT330_SequenceB_TransactionDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1433, 3)))

MT330_SequenceB_TransactionDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'InterestRate'), MT330_SequenceB_TransactionDetails_37G_Type, scope=MT330_SequenceB_TransactionDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1434, 3)))

MT330_SequenceB_TransactionDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DayCountFraction'), MT330_SequenceB_TransactionDetails_14D_Type, scope=MT330_SequenceB_TransactionDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1435, 3)))

MT330_SequenceB_TransactionDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'LastDayOfTheNextInterestPeriod'), MT330_SequenceB_TransactionDetails_30F_Type, scope=MT330_SequenceB_TransactionDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1436, 3)))

MT330_SequenceB_TransactionDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'NumberOfDays'), MT330_SequenceB_TransactionDetails_38J_Type, scope=MT330_SequenceB_TransactionDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1437, 3)))

MT330_SequenceB_TransactionDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PaymentClearingCentre'), MT330_SequenceB_TransactionDetails_39M_Type, scope=MT330_SequenceB_TransactionDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1438, 3)))

def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1430, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1431, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1432, 3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1433, 3))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1436, 3))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1437, 3))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1438, 3))
    counters.add(cc_6)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceB_TransactionDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PartyAsRole')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1426, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceB_TransactionDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'TradeDate')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1427, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceB_TransactionDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ValueDate')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1428, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceB_TransactionDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PeriodOfNotice')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1429, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceB_TransactionDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CurrencyAndBalance')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1430, 3))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceB_TransactionDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PrincipalAmountToBeSettled')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1431, 3))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceB_TransactionDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'InterestDueDate')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1432, 3))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceB_TransactionDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CurrencyAndInterestAmount')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1433, 3))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceB_TransactionDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'InterestRate')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1434, 3))
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceB_TransactionDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DayCountFraction')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1435, 3))
    st_9 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceB_TransactionDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'LastDayOfTheNextInterestPeriod')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1436, 3))
    st_10 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceB_TransactionDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'NumberOfDays')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1437, 3))
    st_11 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_6, False))
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceB_TransactionDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PaymentClearingCentre')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1438, 3))
    st_12 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_12)
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
    transitions.append(fac.Transition(st_8, [
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
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_9, [
         ]))
    st_8._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_10, [
         ]))
    transitions.append(fac.Transition(st_11, [
         ]))
    transitions.append(fac.Transition(st_12, [
         ]))
    st_9._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_4, False) ]))
    st_10._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_5, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_5, False) ]))
    st_11._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_6, True) ]))
    st_12._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
MT330_SequenceB_TransactionDetails._Automaton = _BuildAutomaton_()




MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_A'), MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53A_Type, scope=MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1447, 4)))

MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_D'), MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53D_Type, scope=MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1448, 4)))

MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_J'), MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53J_Type, scope=MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1449, 4)))

MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Intermediary2_A'), MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86A_Type, scope=MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1452, 4)))

MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Intermediary2_D'), MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86D_Type, scope=MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1453, 4)))

MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Intermediary2_J'), MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86J_Type, scope=MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1454, 4)))

MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_A'), MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56A_Type, scope=MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1457, 4)))

MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_D'), MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56D_Type, scope=MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1458, 4)))

MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_J'), MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56J_Type, scope=MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1459, 4)))

MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_A'), MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57A_Type, scope=MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1462, 4)))

MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_D'), MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57D_Type, scope=MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1463, 4)))

MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_J'), MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57J_Type, scope=MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1464, 4)))

MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_A'), MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58A_Type, scope=MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1467, 4)))

MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_D'), MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58D_Type, scope=MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1468, 4)))

MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_J'), MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58J_Type, scope=MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1469, 4)))

def _BuildAutomaton_2 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_2
    del _BuildAutomaton_2
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1446, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1447, 4))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1448, 4))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1449, 4))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1451, 3))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1452, 4))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1453, 4))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1454, 4))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1456, 3))
    counters.add(cc_8)
    cc_9 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1457, 4))
    counters.add(cc_9)
    cc_10 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1458, 4))
    counters.add(cc_10)
    cc_11 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1459, 4))
    counters.add(cc_11)
    cc_12 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1466, 3))
    counters.add(cc_12)
    cc_13 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1467, 4))
    counters.add(cc_13)
    cc_14 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1468, 4))
    counters.add(cc_14)
    cc_15 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1469, 4))
    counters.add(cc_15)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1447, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1448, 4))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1449, 4))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Intermediary2_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1452, 4))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Intermediary2_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1453, 4))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Intermediary2_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1454, 4))
    st_5 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1457, 4))
    st_6 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1458, 4))
    st_7 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1459, 4))
    st_8 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1462, 4))
    st_9 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1463, 4))
    st_10 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1464, 4))
    st_11 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_12, False))
    final_update.add(fac.UpdateInstruction(cc_13, False))
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1467, 4))
    st_12 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_12)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_12, False))
    final_update.add(fac.UpdateInstruction(cc_14, False))
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1468, 4))
    st_13 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_13)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_12, False))
    final_update.add(fac.UpdateInstruction(cc_15, False))
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1469, 4))
    st_14 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_14)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True),
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True),
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True),
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False),
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
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False),
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
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_2, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_3, False) ]))
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
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_3, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_4, True),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_5, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_4, True),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_4, True),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_4, False),
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
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_4, True),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_4, True),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_6, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_4, True),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_4, False),
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
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_4, True),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_4, True),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_4, True),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_7, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_7, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_8, True),
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_9, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_8, True),
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_8, True),
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_9, False) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_8, True),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_8, True),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_10, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_8, True),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_10, False) ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_8, True),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_8, True),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_8, True),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_11, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_11, False) ]))
    st_8._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_12, [
         ]))
    transitions.append(fac.Transition(st_13, [
         ]))
    transitions.append(fac.Transition(st_14, [
         ]))
    st_9._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_12, [
         ]))
    transitions.append(fac.Transition(st_13, [
         ]))
    transitions.append(fac.Transition(st_14, [
         ]))
    st_10._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_12, [
         ]))
    transitions.append(fac.Transition(st_13, [
         ]))
    transitions.append(fac.Transition(st_14, [
         ]))
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
        fac.UpdateInstruction(cc_12, True),
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
        fac.UpdateInstruction(cc_12, True),
        fac.UpdateInstruction(cc_14, False) ]))
    st_13._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_12, True),
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_12, True),
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_12, True),
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_15, True) ]))
    st_14._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA._Automaton = _BuildAutomaton_2()




MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_A'), MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53A_Type, scope=MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1479, 4)))

MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_D'), MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53D_Type, scope=MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1480, 4)))

MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_J'), MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53J_Type, scope=MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1481, 4)))

MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Intermediary2_A'), MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86A_Type, scope=MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1484, 4)))

MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Intermediary2_D'), MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86D_Type, scope=MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1485, 4)))

MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Intermediary2_J'), MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86J_Type, scope=MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1486, 4)))

MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_A'), MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56A_Type, scope=MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1489, 4)))

MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_D'), MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56D_Type, scope=MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1490, 4)))

MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_J'), MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56J_Type, scope=MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1491, 4)))

MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_A'), MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57A_Type, scope=MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1494, 4)))

MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_D'), MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57D_Type, scope=MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1495, 4)))

MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_J'), MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57J_Type, scope=MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1496, 4)))

MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_A'), MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58A_Type, scope=MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1499, 4)))

MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_D'), MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58D_Type, scope=MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1500, 4)))

MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_J'), MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58J_Type, scope=MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1501, 4)))

def _BuildAutomaton_3 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_3
    del _BuildAutomaton_3
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1478, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1479, 4))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1480, 4))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1481, 4))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1483, 3))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1484, 4))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1485, 4))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1486, 4))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1488, 3))
    counters.add(cc_8)
    cc_9 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1489, 4))
    counters.add(cc_9)
    cc_10 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1490, 4))
    counters.add(cc_10)
    cc_11 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1491, 4))
    counters.add(cc_11)
    cc_12 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1498, 3))
    counters.add(cc_12)
    cc_13 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1499, 4))
    counters.add(cc_13)
    cc_14 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1500, 4))
    counters.add(cc_14)
    cc_15 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1501, 4))
    counters.add(cc_15)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1479, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1480, 4))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1481, 4))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Intermediary2_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1484, 4))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Intermediary2_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1485, 4))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Intermediary2_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1486, 4))
    st_5 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1489, 4))
    st_6 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1490, 4))
    st_7 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1491, 4))
    st_8 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1494, 4))
    st_9 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1495, 4))
    st_10 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1496, 4))
    st_11 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_12, False))
    final_update.add(fac.UpdateInstruction(cc_13, False))
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1499, 4))
    st_12 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_12)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_12, False))
    final_update.add(fac.UpdateInstruction(cc_14, False))
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1500, 4))
    st_13 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_13)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_12, False))
    final_update.add(fac.UpdateInstruction(cc_15, False))
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1501, 4))
    st_14 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_14)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True),
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True),
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True),
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False),
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
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False),
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
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_2, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_3, False) ]))
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
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_3, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_4, True),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_5, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_4, True),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_4, True),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_4, False),
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
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_4, True),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_4, True),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_6, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_4, True),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_4, False),
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
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_4, True),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_4, True),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_4, True),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_7, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_7, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_8, True),
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_9, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_8, True),
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_8, True),
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_9, False) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_8, True),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_8, True),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_10, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_8, True),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_10, False) ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_8, True),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_8, True),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_8, True),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_11, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_11, False) ]))
    st_8._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_12, [
         ]))
    transitions.append(fac.Transition(st_13, [
         ]))
    transitions.append(fac.Transition(st_14, [
         ]))
    st_9._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_12, [
         ]))
    transitions.append(fac.Transition(st_13, [
         ]))
    transitions.append(fac.Transition(st_14, [
         ]))
    st_10._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_12, [
         ]))
    transitions.append(fac.Transition(st_13, [
         ]))
    transitions.append(fac.Transition(st_14, [
         ]))
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
        fac.UpdateInstruction(cc_12, True),
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
        fac.UpdateInstruction(cc_12, True),
        fac.UpdateInstruction(cc_14, False) ]))
    st_13._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_12, True),
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_12, True),
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_12, True),
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_15, True) ]))
    st_14._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB._Automaton = _BuildAutomaton_3()




MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_A'), MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53A_Type, scope=MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1511, 4)))

MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_D'), MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53D_Type, scope=MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1512, 4)))

MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_J'), MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53J_Type, scope=MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1513, 4)))

MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Intermediary2_A'), MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86A_Type, scope=MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1516, 4)))

MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Intermediary2_D'), MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86D_Type, scope=MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1517, 4)))

MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Intermediary2_J'), MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86J_Type, scope=MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1518, 4)))

MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_A'), MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56A_Type, scope=MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1521, 4)))

MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_D'), MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56D_Type, scope=MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1522, 4)))

MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_J'), MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56J_Type, scope=MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1523, 4)))

MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_A'), MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57A_Type, scope=MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1526, 4)))

MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_D'), MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57D_Type, scope=MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1527, 4)))

MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_J'), MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57J_Type, scope=MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1528, 4)))

MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_A'), MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58A_Type, scope=MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1531, 4)))

MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_D'), MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58D_Type, scope=MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1532, 4)))

MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_J'), MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58J_Type, scope=MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1533, 4)))

def _BuildAutomaton_4 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_4
    del _BuildAutomaton_4
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1510, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1511, 4))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1512, 4))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1513, 4))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1515, 3))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1516, 4))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1517, 4))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1518, 4))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1520, 3))
    counters.add(cc_8)
    cc_9 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1521, 4))
    counters.add(cc_9)
    cc_10 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1522, 4))
    counters.add(cc_10)
    cc_11 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1523, 4))
    counters.add(cc_11)
    cc_12 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1530, 3))
    counters.add(cc_12)
    cc_13 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1531, 4))
    counters.add(cc_13)
    cc_14 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1532, 4))
    counters.add(cc_14)
    cc_15 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1533, 4))
    counters.add(cc_15)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1511, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1512, 4))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1513, 4))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Intermediary2_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1516, 4))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Intermediary2_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1517, 4))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Intermediary2_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1518, 4))
    st_5 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1521, 4))
    st_6 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1522, 4))
    st_7 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1523, 4))
    st_8 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1526, 4))
    st_9 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1527, 4))
    st_10 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1528, 4))
    st_11 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_12, False))
    final_update.add(fac.UpdateInstruction(cc_13, False))
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1531, 4))
    st_12 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_12)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_12, False))
    final_update.add(fac.UpdateInstruction(cc_14, False))
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1532, 4))
    st_13 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_13)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_12, False))
    final_update.add(fac.UpdateInstruction(cc_15, False))
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1533, 4))
    st_14 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_14)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True),
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True),
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True),
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False),
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
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False),
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
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_2, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_3, False) ]))
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
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_3, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_4, True),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_5, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_4, True),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_4, True),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_4, False),
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
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_4, True),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_4, True),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_6, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_4, True),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_4, False),
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
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_4, True),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_4, True),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_4, True),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_7, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_7, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_8, True),
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_9, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_8, True),
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_8, True),
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_9, False) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_8, True),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_8, True),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_10, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_8, True),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_10, False) ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_8, True),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_8, True),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_8, True),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_11, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_11, False) ]))
    st_8._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_12, [
         ]))
    transitions.append(fac.Transition(st_13, [
         ]))
    transitions.append(fac.Transition(st_14, [
         ]))
    st_9._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_12, [
         ]))
    transitions.append(fac.Transition(st_13, [
         ]))
    transitions.append(fac.Transition(st_14, [
         ]))
    st_10._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_12, [
         ]))
    transitions.append(fac.Transition(st_13, [
         ]))
    transitions.append(fac.Transition(st_14, [
         ]))
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
        fac.UpdateInstruction(cc_12, True),
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
        fac.UpdateInstruction(cc_12, True),
        fac.UpdateInstruction(cc_14, False) ]))
    st_13._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_12, True),
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_12, True),
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_12, True),
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_15, True) ]))
    st_14._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA._Automaton = _BuildAutomaton_4()




MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_A'), MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53A_Type, scope=MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1543, 4)))

MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_D'), MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53D_Type, scope=MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1544, 4)))

MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_J'), MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53J_Type, scope=MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1545, 4)))

MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Intermediary2_A'), MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86A_Type, scope=MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1548, 4)))

MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Intermediary2_D'), MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86D_Type, scope=MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1549, 4)))

MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Intermediary2_J'), MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86J_Type, scope=MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1550, 4)))

MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_A'), MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56A_Type, scope=MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1553, 4)))

MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_D'), MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56D_Type, scope=MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1554, 4)))

MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_J'), MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56J_Type, scope=MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1555, 4)))

MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_A'), MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57A_Type, scope=MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1558, 4)))

MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_D'), MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57D_Type, scope=MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1559, 4)))

MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_J'), MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57J_Type, scope=MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1560, 4)))

MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_A'), MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58A_Type, scope=MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1563, 4)))

MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_D'), MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58D_Type, scope=MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1564, 4)))

MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_J'), MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58J_Type, scope=MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1565, 4)))

def _BuildAutomaton_5 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_5
    del _BuildAutomaton_5
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1542, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1543, 4))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1544, 4))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1545, 4))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1547, 3))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1548, 4))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1549, 4))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1550, 4))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1552, 3))
    counters.add(cc_8)
    cc_9 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1553, 4))
    counters.add(cc_9)
    cc_10 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1554, 4))
    counters.add(cc_10)
    cc_11 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1555, 4))
    counters.add(cc_11)
    cc_12 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1562, 3))
    counters.add(cc_12)
    cc_13 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1563, 4))
    counters.add(cc_13)
    cc_14 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1564, 4))
    counters.add(cc_14)
    cc_15 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1565, 4))
    counters.add(cc_15)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1543, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1544, 4))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1545, 4))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Intermediary2_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1548, 4))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Intermediary2_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1549, 4))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Intermediary2_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1550, 4))
    st_5 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1553, 4))
    st_6 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1554, 4))
    st_7 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1555, 4))
    st_8 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1558, 4))
    st_9 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1559, 4))
    st_10 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1560, 4))
    st_11 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_12, False))
    final_update.add(fac.UpdateInstruction(cc_13, False))
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1563, 4))
    st_12 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_12)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_12, False))
    final_update.add(fac.UpdateInstruction(cc_14, False))
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1564, 4))
    st_13 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_13)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_12, False))
    final_update.add(fac.UpdateInstruction(cc_15, False))
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1565, 4))
    st_14 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_14)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True),
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True),
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True),
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False),
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
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False),
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
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_2, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_3, False) ]))
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
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_3, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_4, True),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_5, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_4, True),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_4, True),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_4, False),
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
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_4, True),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_4, True),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_6, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_4, True),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_4, False),
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
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_4, True),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_4, True),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_4, True),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_7, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_7, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_8, True),
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_9, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_8, True),
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_8, True),
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_9, False) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_8, True),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_8, True),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_10, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_8, True),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_10, False) ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_8, True),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_8, True),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_8, True),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_11, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_11, False) ]))
    st_8._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_12, [
         ]))
    transitions.append(fac.Transition(st_13, [
         ]))
    transitions.append(fac.Transition(st_14, [
         ]))
    st_9._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_12, [
         ]))
    transitions.append(fac.Transition(st_13, [
         ]))
    transitions.append(fac.Transition(st_14, [
         ]))
    st_10._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_12, [
         ]))
    transitions.append(fac.Transition(st_13, [
         ]))
    transitions.append(fac.Transition(st_14, [
         ]))
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
        fac.UpdateInstruction(cc_12, True),
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
        fac.UpdateInstruction(cc_12, True),
        fac.UpdateInstruction(cc_14, False) ]))
    st_13._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_12, True),
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_12, True),
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_12, True),
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_15, True) ]))
    st_14._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB._Automaton = _BuildAutomaton_5()




MT330_SequenceG_TaxInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TaxRate'), MT330_SequenceG_TaxInformation_37L_Type, scope=MT330_SequenceG_TaxInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1574, 3)))

MT330_SequenceG_TaxInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TransactionCurrencyAndNetInterestAmount'), MT330_SequenceG_TaxInformation_33B_Type, scope=MT330_SequenceG_TaxInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1575, 3)))

MT330_SequenceG_TaxInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ExchangeRate'), MT330_SequenceG_TaxInformation_36_Type, scope=MT330_SequenceG_TaxInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1576, 3)))

MT330_SequenceG_TaxInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ReportingCurrencyAndTaxAmount'), MT330_SequenceG_TaxInformation_33E_Type, scope=MT330_SequenceG_TaxInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1577, 3)))

def _BuildAutomaton_6 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_6
    del _BuildAutomaton_6
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1576, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1577, 3))
    counters.add(cc_1)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceG_TaxInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'TaxRate')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1574, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceG_TaxInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'TransactionCurrencyAndNetInterestAmount')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1575, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceG_TaxInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ExchangeRate')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1576, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceG_TaxInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ReportingCurrencyAndTaxAmount')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1577, 3))
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
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_3._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
MT330_SequenceG_TaxInformation._Automaton = _BuildAutomaton_6()




MT330_SequenceH_AdditionalInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ContactInformation'), MT330_SequenceH_AdditionalInformation_29A_Type, scope=MT330_SequenceH_AdditionalInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1585, 3)))

MT330_SequenceH_AdditionalInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DealingMethod'), MT330_SequenceH_AdditionalInformation_24D_Type, scope=MT330_SequenceH_AdditionalInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1586, 3)))

MT330_SequenceH_AdditionalInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DealingBranchPartyA_A'), MT330_SequenceH_AdditionalInformation_84A_Type, scope=MT330_SequenceH_AdditionalInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1588, 4)))

MT330_SequenceH_AdditionalInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DealingBranchPartyA_B'), MT330_SequenceH_AdditionalInformation_84B_Type, scope=MT330_SequenceH_AdditionalInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1589, 4)))

MT330_SequenceH_AdditionalInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DealingBranchPartyA_D'), MT330_SequenceH_AdditionalInformation_84D_Type, scope=MT330_SequenceH_AdditionalInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1590, 4)))

MT330_SequenceH_AdditionalInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DealingBranchPartyA_J'), MT330_SequenceH_AdditionalInformation_84J_Type, scope=MT330_SequenceH_AdditionalInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1591, 4)))

MT330_SequenceH_AdditionalInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DealingBranchPartyB_A'), MT330_SequenceH_AdditionalInformation_85A_Type, scope=MT330_SequenceH_AdditionalInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1594, 4)))

MT330_SequenceH_AdditionalInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DealingBranchPartyB_B'), MT330_SequenceH_AdditionalInformation_85B_Type, scope=MT330_SequenceH_AdditionalInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1595, 4)))

MT330_SequenceH_AdditionalInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DealingBranchPartyB_D'), MT330_SequenceH_AdditionalInformation_85D_Type, scope=MT330_SequenceH_AdditionalInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1596, 4)))

MT330_SequenceH_AdditionalInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DealingBranchPartyB_J'), MT330_SequenceH_AdditionalInformation_85J_Type, scope=MT330_SequenceH_AdditionalInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1597, 4)))

MT330_SequenceH_AdditionalInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CounterpartysReference'), MT330_SequenceH_AdditionalInformation_26H_Type, scope=MT330_SequenceH_AdditionalInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1599, 3)))

MT330_SequenceH_AdditionalInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CommissionAndFees'), MT330_SequenceH_AdditionalInformation_34C_Type, scope=MT330_SequenceH_AdditionalInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1600, 3)))

MT330_SequenceH_AdditionalInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SenderToReceiverInformation'), MT330_SequenceH_AdditionalInformation_72_Type, scope=MT330_SequenceH_AdditionalInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1601, 3)))

def _BuildAutomaton_7 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_7
    del _BuildAutomaton_7
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1585, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1586, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1587, 3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1588, 4))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1589, 4))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1590, 4))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1591, 4))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1593, 3))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1594, 4))
    counters.add(cc_8)
    cc_9 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1595, 4))
    counters.add(cc_9)
    cc_10 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1596, 4))
    counters.add(cc_10)
    cc_11 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1597, 4))
    counters.add(cc_11)
    cc_12 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1599, 3))
    counters.add(cc_12)
    cc_13 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1600, 3))
    counters.add(cc_13)
    cc_14 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1601, 3))
    counters.add(cc_14)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceH_AdditionalInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ContactInformation')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1585, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceH_AdditionalInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DealingMethod')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1586, 3))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceH_AdditionalInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DealingBranchPartyA_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1588, 4))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceH_AdditionalInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DealingBranchPartyA_B')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1589, 4))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceH_AdditionalInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DealingBranchPartyA_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1590, 4))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    final_update.add(fac.UpdateInstruction(cc_6, False))
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceH_AdditionalInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DealingBranchPartyA_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1591, 4))
    st_5 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_7, False))
    final_update.add(fac.UpdateInstruction(cc_8, False))
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceH_AdditionalInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DealingBranchPartyB_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1594, 4))
    st_6 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_7, False))
    final_update.add(fac.UpdateInstruction(cc_9, False))
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceH_AdditionalInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DealingBranchPartyB_B')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1595, 4))
    st_7 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_7, False))
    final_update.add(fac.UpdateInstruction(cc_10, False))
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceH_AdditionalInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DealingBranchPartyB_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1596, 4))
    st_8 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_7, False))
    final_update.add(fac.UpdateInstruction(cc_11, False))
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceH_AdditionalInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DealingBranchPartyB_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1597, 4))
    st_9 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_12, False))
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceH_AdditionalInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CounterpartysReference')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1599, 3))
    st_10 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_13, False))
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceH_AdditionalInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CommissionAndFees')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1600, 3))
    st_11 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_14, False))
    symbol = pyxb.binding.content.ElementUse(MT330_SequenceH_AdditionalInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SenderToReceiverInformation')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1601, 3))
    st_12 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_12)
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
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_2, True),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, True),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, True),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, True),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_2, False),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_2, False),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_2, False),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_2, False),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_2, False),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_2, False),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_2, False),
        fac.UpdateInstruction(cc_3, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_2, True),
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, True),
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, True),
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, True),
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_2, False),
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_2, False),
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_2, False),
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_2, False),
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_2, False),
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_2, False),
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_2, False),
        fac.UpdateInstruction(cc_4, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_2, True),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, True),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, True),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_5, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, True),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_2, False),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_2, False),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_2, False),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_2, False),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_2, False),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_2, False),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_2, False),
        fac.UpdateInstruction(cc_5, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_2, True),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, True),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, True),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, True),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_6, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_2, False),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_2, False),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_2, False),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_2, False),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_2, False),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_2, False),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_2, False),
        fac.UpdateInstruction(cc_6, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_7, True),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_8, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_7, True),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_7, True),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_7, True),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_7, False),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_7, False),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_7, False),
        fac.UpdateInstruction(cc_8, False) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_7, True),
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_7, True),
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_9, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_7, True),
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_7, True),
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_7, False),
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_7, False),
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_7, False),
        fac.UpdateInstruction(cc_9, False) ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_7, True),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_7, True),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_7, True),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_10, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_7, True),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_7, False),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_7, False),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_7, False),
        fac.UpdateInstruction(cc_10, False) ]))
    st_8._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_7, True),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_7, True),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_7, True),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_7, True),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_11, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_7, False),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_7, False),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_7, False),
        fac.UpdateInstruction(cc_11, False) ]))
    st_9._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_12, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_12, False) ]))
    st_10._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_13, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_13, False) ]))
    st_11._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_14, True) ]))
    st_12._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
MT330_SequenceH_AdditionalInformation._Automaton = _BuildAutomaton_7()




CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SequenceA_GeneralInformation'), MT330_SequenceA_GeneralInformation, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1610, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SequenceB_TransactionDetails'), MT330_SequenceB_TransactionDetails, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1611, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SequenceC_SettlementInstructionsforAmountsPayablebyPartyA'), MT330_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1612, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SequenceD_SettlementInstructionsforAmountsPayablebyPartyB'), MT330_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1613, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SequenceE_SettlementInstructionsforInterestsPayablebyPartyA'), MT330_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1614, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SequenceF_SettlementInstructionsforInterestsPayablebyPartyB'), MT330_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1615, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SequenceG_TaxInformation'), MT330_SequenceG_TaxInformation, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1616, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SequenceH_AdditionalInformation'), MT330_SequenceH_AdditionalInformation, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1617, 4)))

def _BuildAutomaton_8 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_8
    del _BuildAutomaton_8
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1614, 4))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1615, 4))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1616, 4))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1617, 4))
    counters.add(cc_3)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SequenceA_GeneralInformation')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1610, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SequenceB_TransactionDetails')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1611, 4))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SequenceC_SettlementInstructionsforAmountsPayablebyPartyA')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1612, 4))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SequenceD_SettlementInstructionsforAmountsPayablebyPartyB')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1613, 4))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SequenceE_SettlementInstructionsforInterestsPayablebyPartyA')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1614, 4))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SequenceF_SettlementInstructionsforInterestsPayablebyPartyB')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1615, 4))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SequenceG_TaxInformation')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1616, 4))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SequenceH_AdditionalInformation')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT330.xsd', 1617, 4))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
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
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_3, True) ]))
    st_7._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON._Automaton = _BuildAutomaton_8()


