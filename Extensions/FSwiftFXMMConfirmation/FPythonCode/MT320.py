# C:\Projects\Code\SwiftMessagingSolution_Python3\base\extensions\SwiftIntegration\Utilities\TemplateFiles\MT320.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:96afad3d20bbfe8d040a1a097fa388d9fecd10e3
# Generated 2019-11-07 12:27:19.160791 by PyXB version 1.2.6 using Python 3.7.4.final.0
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
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:d6e2a0ec-012b-11ea-b6eb-509a4c321f2f')

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


# Atomic simple type: {http://www.w3schools.com}MT320_SequenceA_GeneralInformation_20_Type_Pattern
class MT320_SequenceA_GeneralInformation_20_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceA_GeneralInformation_20_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 3, 1)
    _Documentation = None
MT320_SequenceA_GeneralInformation_20_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceA_GeneralInformation_20_Type_Pattern._CF_pattern.addPattern(pattern="([^/]([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,16}[^/])")
MT320_SequenceA_GeneralInformation_20_Type_Pattern._InitializeFacetMap(MT320_SequenceA_GeneralInformation_20_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceA_GeneralInformation_20_Type_Pattern', MT320_SequenceA_GeneralInformation_20_Type_Pattern)
_module_typeBindings.MT320_SequenceA_GeneralInformation_20_Type_Pattern = MT320_SequenceA_GeneralInformation_20_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceA_GeneralInformation_21_Type_Pattern
class MT320_SequenceA_GeneralInformation_21_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceA_GeneralInformation_21_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 16, 1)
    _Documentation = None
MT320_SequenceA_GeneralInformation_21_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceA_GeneralInformation_21_Type_Pattern._CF_pattern.addPattern(pattern="([^/]([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,16}[^/])")
MT320_SequenceA_GeneralInformation_21_Type_Pattern._InitializeFacetMap(MT320_SequenceA_GeneralInformation_21_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceA_GeneralInformation_21_Type_Pattern', MT320_SequenceA_GeneralInformation_21_Type_Pattern)
_module_typeBindings.MT320_SequenceA_GeneralInformation_21_Type_Pattern = MT320_SequenceA_GeneralInformation_21_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceA_GeneralInformation_22A_Type_Pattern
class MT320_SequenceA_GeneralInformation_22A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceA_GeneralInformation_22A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 29, 1)
    _Documentation = None
MT320_SequenceA_GeneralInformation_22A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceA_GeneralInformation_22A_Type_Pattern._CF_pattern.addPattern(pattern='((AMND|CANC|DUPL|NEWT))')
MT320_SequenceA_GeneralInformation_22A_Type_Pattern._InitializeFacetMap(MT320_SequenceA_GeneralInformation_22A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceA_GeneralInformation_22A_Type_Pattern', MT320_SequenceA_GeneralInformation_22A_Type_Pattern)
_module_typeBindings.MT320_SequenceA_GeneralInformation_22A_Type_Pattern = MT320_SequenceA_GeneralInformation_22A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceA_GeneralInformation_94A_Type_Pattern
class MT320_SequenceA_GeneralInformation_94A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceA_GeneralInformation_94A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 42, 1)
    _Documentation = None
MT320_SequenceA_GeneralInformation_94A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceA_GeneralInformation_94A_Type_Pattern._CF_pattern.addPattern(pattern='((AGNT|BILA|BROK))')
MT320_SequenceA_GeneralInformation_94A_Type_Pattern._InitializeFacetMap(MT320_SequenceA_GeneralInformation_94A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceA_GeneralInformation_94A_Type_Pattern', MT320_SequenceA_GeneralInformation_94A_Type_Pattern)
_module_typeBindings.MT320_SequenceA_GeneralInformation_94A_Type_Pattern = MT320_SequenceA_GeneralInformation_94A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceA_GeneralInformation_22B_Type_Pattern
class MT320_SequenceA_GeneralInformation_22B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceA_GeneralInformation_22B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 55, 1)
    _Documentation = None
MT320_SequenceA_GeneralInformation_22B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceA_GeneralInformation_22B_Type_Pattern._CF_pattern.addPattern(pattern='((CONF|MATU|ROLL))')
MT320_SequenceA_GeneralInformation_22B_Type_Pattern._InitializeFacetMap(MT320_SequenceA_GeneralInformation_22B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceA_GeneralInformation_22B_Type_Pattern', MT320_SequenceA_GeneralInformation_22B_Type_Pattern)
_module_typeBindings.MT320_SequenceA_GeneralInformation_22B_Type_Pattern = MT320_SequenceA_GeneralInformation_22B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceA_GeneralInformation_22C_Type_Pattern
class MT320_SequenceA_GeneralInformation_22C_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceA_GeneralInformation_22C_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 68, 1)
    _Documentation = None
MT320_SequenceA_GeneralInformation_22C_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceA_GeneralInformation_22C_Type_Pattern._CF_pattern.addPattern(pattern='([A-Z]{4}[A-Z0-9]{2}[0-9]{4}[A-Z]{4}[A-Z0-9]{2})')
MT320_SequenceA_GeneralInformation_22C_Type_Pattern._InitializeFacetMap(MT320_SequenceA_GeneralInformation_22C_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceA_GeneralInformation_22C_Type_Pattern', MT320_SequenceA_GeneralInformation_22C_Type_Pattern)
_module_typeBindings.MT320_SequenceA_GeneralInformation_22C_Type_Pattern = MT320_SequenceA_GeneralInformation_22C_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceA_GeneralInformation_21N_Type_Pattern
class MT320_SequenceA_GeneralInformation_21N_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceA_GeneralInformation_21N_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 81, 1)
    _Documentation = None
MT320_SequenceA_GeneralInformation_21N_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceA_GeneralInformation_21N_Type_Pattern._CF_pattern.addPattern(pattern="(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,16})")
MT320_SequenceA_GeneralInformation_21N_Type_Pattern._InitializeFacetMap(MT320_SequenceA_GeneralInformation_21N_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceA_GeneralInformation_21N_Type_Pattern', MT320_SequenceA_GeneralInformation_21N_Type_Pattern)
_module_typeBindings.MT320_SequenceA_GeneralInformation_21N_Type_Pattern = MT320_SequenceA_GeneralInformation_21N_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceA_GeneralInformation_82A_Type_Pattern
class MT320_SequenceA_GeneralInformation_82A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceA_GeneralInformation_82A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 94, 1)
    _Documentation = None
MT320_SequenceA_GeneralInformation_82A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceA_GeneralInformation_82A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT320_SequenceA_GeneralInformation_82A_Type_Pattern._InitializeFacetMap(MT320_SequenceA_GeneralInformation_82A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceA_GeneralInformation_82A_Type_Pattern', MT320_SequenceA_GeneralInformation_82A_Type_Pattern)
_module_typeBindings.MT320_SequenceA_GeneralInformation_82A_Type_Pattern = MT320_SequenceA_GeneralInformation_82A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceA_GeneralInformation_82D_Type_Pattern
class MT320_SequenceA_GeneralInformation_82D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceA_GeneralInformation_82D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 107, 1)
    _Documentation = None
MT320_SequenceA_GeneralInformation_82D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceA_GeneralInformation_82D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT320_SequenceA_GeneralInformation_82D_Type_Pattern._InitializeFacetMap(MT320_SequenceA_GeneralInformation_82D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceA_GeneralInformation_82D_Type_Pattern', MT320_SequenceA_GeneralInformation_82D_Type_Pattern)
_module_typeBindings.MT320_SequenceA_GeneralInformation_82D_Type_Pattern = MT320_SequenceA_GeneralInformation_82D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceA_GeneralInformation_82J_Type_Pattern
class MT320_SequenceA_GeneralInformation_82J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceA_GeneralInformation_82J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 120, 1)
    _Documentation = None
MT320_SequenceA_GeneralInformation_82J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceA_GeneralInformation_82J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT320_SequenceA_GeneralInformation_82J_Type_Pattern._InitializeFacetMap(MT320_SequenceA_GeneralInformation_82J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceA_GeneralInformation_82J_Type_Pattern', MT320_SequenceA_GeneralInformation_82J_Type_Pattern)
_module_typeBindings.MT320_SequenceA_GeneralInformation_82J_Type_Pattern = MT320_SequenceA_GeneralInformation_82J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceA_GeneralInformation_87A_Type_Pattern
class MT320_SequenceA_GeneralInformation_87A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceA_GeneralInformation_87A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 133, 1)
    _Documentation = None
MT320_SequenceA_GeneralInformation_87A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceA_GeneralInformation_87A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT320_SequenceA_GeneralInformation_87A_Type_Pattern._InitializeFacetMap(MT320_SequenceA_GeneralInformation_87A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceA_GeneralInformation_87A_Type_Pattern', MT320_SequenceA_GeneralInformation_87A_Type_Pattern)
_module_typeBindings.MT320_SequenceA_GeneralInformation_87A_Type_Pattern = MT320_SequenceA_GeneralInformation_87A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceA_GeneralInformation_87D_Type_Pattern
class MT320_SequenceA_GeneralInformation_87D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceA_GeneralInformation_87D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 146, 1)
    _Documentation = None
MT320_SequenceA_GeneralInformation_87D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceA_GeneralInformation_87D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT320_SequenceA_GeneralInformation_87D_Type_Pattern._InitializeFacetMap(MT320_SequenceA_GeneralInformation_87D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceA_GeneralInformation_87D_Type_Pattern', MT320_SequenceA_GeneralInformation_87D_Type_Pattern)
_module_typeBindings.MT320_SequenceA_GeneralInformation_87D_Type_Pattern = MT320_SequenceA_GeneralInformation_87D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceA_GeneralInformation_87J_Type_Pattern
class MT320_SequenceA_GeneralInformation_87J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceA_GeneralInformation_87J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 159, 1)
    _Documentation = None
MT320_SequenceA_GeneralInformation_87J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceA_GeneralInformation_87J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT320_SequenceA_GeneralInformation_87J_Type_Pattern._InitializeFacetMap(MT320_SequenceA_GeneralInformation_87J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceA_GeneralInformation_87J_Type_Pattern', MT320_SequenceA_GeneralInformation_87J_Type_Pattern)
_module_typeBindings.MT320_SequenceA_GeneralInformation_87J_Type_Pattern = MT320_SequenceA_GeneralInformation_87J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceA_GeneralInformation_83A_Type_Pattern
class MT320_SequenceA_GeneralInformation_83A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceA_GeneralInformation_83A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 172, 1)
    _Documentation = None
MT320_SequenceA_GeneralInformation_83A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceA_GeneralInformation_83A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT320_SequenceA_GeneralInformation_83A_Type_Pattern._InitializeFacetMap(MT320_SequenceA_GeneralInformation_83A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceA_GeneralInformation_83A_Type_Pattern', MT320_SequenceA_GeneralInformation_83A_Type_Pattern)
_module_typeBindings.MT320_SequenceA_GeneralInformation_83A_Type_Pattern = MT320_SequenceA_GeneralInformation_83A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceA_GeneralInformation_83D_Type_Pattern
class MT320_SequenceA_GeneralInformation_83D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceA_GeneralInformation_83D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 185, 1)
    _Documentation = None
MT320_SequenceA_GeneralInformation_83D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceA_GeneralInformation_83D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT320_SequenceA_GeneralInformation_83D_Type_Pattern._InitializeFacetMap(MT320_SequenceA_GeneralInformation_83D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceA_GeneralInformation_83D_Type_Pattern', MT320_SequenceA_GeneralInformation_83D_Type_Pattern)
_module_typeBindings.MT320_SequenceA_GeneralInformation_83D_Type_Pattern = MT320_SequenceA_GeneralInformation_83D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceA_GeneralInformation_83J_Type_Pattern
class MT320_SequenceA_GeneralInformation_83J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceA_GeneralInformation_83J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 198, 1)
    _Documentation = None
MT320_SequenceA_GeneralInformation_83J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceA_GeneralInformation_83J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT320_SequenceA_GeneralInformation_83J_Type_Pattern._InitializeFacetMap(MT320_SequenceA_GeneralInformation_83J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceA_GeneralInformation_83J_Type_Pattern', MT320_SequenceA_GeneralInformation_83J_Type_Pattern)
_module_typeBindings.MT320_SequenceA_GeneralInformation_83J_Type_Pattern = MT320_SequenceA_GeneralInformation_83J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceA_GeneralInformation_77D_Type_Pattern
class MT320_SequenceA_GeneralInformation_77D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceA_GeneralInformation_77D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 211, 1)
    _Documentation = None
MT320_SequenceA_GeneralInformation_77D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceA_GeneralInformation_77D_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,6})")
MT320_SequenceA_GeneralInformation_77D_Type_Pattern._InitializeFacetMap(MT320_SequenceA_GeneralInformation_77D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceA_GeneralInformation_77D_Type_Pattern', MT320_SequenceA_GeneralInformation_77D_Type_Pattern)
_module_typeBindings.MT320_SequenceA_GeneralInformation_77D_Type_Pattern = MT320_SequenceA_GeneralInformation_77D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceB_TransactionDetails_17R_Type_Pattern
class MT320_SequenceB_TransactionDetails_17R_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceB_TransactionDetails_17R_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 224, 1)
    _Documentation = None
MT320_SequenceB_TransactionDetails_17R_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceB_TransactionDetails_17R_Type_Pattern._CF_pattern.addPattern(pattern='((B|L))')
MT320_SequenceB_TransactionDetails_17R_Type_Pattern._InitializeFacetMap(MT320_SequenceB_TransactionDetails_17R_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceB_TransactionDetails_17R_Type_Pattern', MT320_SequenceB_TransactionDetails_17R_Type_Pattern)
_module_typeBindings.MT320_SequenceB_TransactionDetails_17R_Type_Pattern = MT320_SequenceB_TransactionDetails_17R_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceB_TransactionDetails_30T_Type_Pattern
class MT320_SequenceB_TransactionDetails_30T_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceB_TransactionDetails_30T_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 237, 1)
    _Documentation = None
MT320_SequenceB_TransactionDetails_30T_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceB_TransactionDetails_30T_Type_Pattern._CF_pattern.addPattern(pattern='([0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))')
MT320_SequenceB_TransactionDetails_30T_Type_Pattern._InitializeFacetMap(MT320_SequenceB_TransactionDetails_30T_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceB_TransactionDetails_30T_Type_Pattern', MT320_SequenceB_TransactionDetails_30T_Type_Pattern)
_module_typeBindings.MT320_SequenceB_TransactionDetails_30T_Type_Pattern = MT320_SequenceB_TransactionDetails_30T_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceB_TransactionDetails_30V_Type_Pattern
class MT320_SequenceB_TransactionDetails_30V_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceB_TransactionDetails_30V_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 250, 1)
    _Documentation = None
MT320_SequenceB_TransactionDetails_30V_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceB_TransactionDetails_30V_Type_Pattern._CF_pattern.addPattern(pattern='([0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))')
MT320_SequenceB_TransactionDetails_30V_Type_Pattern._InitializeFacetMap(MT320_SequenceB_TransactionDetails_30V_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceB_TransactionDetails_30V_Type_Pattern', MT320_SequenceB_TransactionDetails_30V_Type_Pattern)
_module_typeBindings.MT320_SequenceB_TransactionDetails_30V_Type_Pattern = MT320_SequenceB_TransactionDetails_30V_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceB_TransactionDetails_30P_Type_Pattern
class MT320_SequenceB_TransactionDetails_30P_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceB_TransactionDetails_30P_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 263, 1)
    _Documentation = None
MT320_SequenceB_TransactionDetails_30P_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceB_TransactionDetails_30P_Type_Pattern._CF_pattern.addPattern(pattern='([0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))')
MT320_SequenceB_TransactionDetails_30P_Type_Pattern._InitializeFacetMap(MT320_SequenceB_TransactionDetails_30P_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceB_TransactionDetails_30P_Type_Pattern', MT320_SequenceB_TransactionDetails_30P_Type_Pattern)
_module_typeBindings.MT320_SequenceB_TransactionDetails_30P_Type_Pattern = MT320_SequenceB_TransactionDetails_30P_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceB_TransactionDetails_32B_Type_Pattern
class MT320_SequenceB_TransactionDetails_32B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceB_TransactionDetails_32B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 276, 1)
    _Documentation = None
MT320_SequenceB_TransactionDetails_32B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceB_TransactionDetails_32B_Type_Pattern._CF_pattern.addPattern(pattern='((AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})')
MT320_SequenceB_TransactionDetails_32B_Type_Pattern._InitializeFacetMap(MT320_SequenceB_TransactionDetails_32B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceB_TransactionDetails_32B_Type_Pattern', MT320_SequenceB_TransactionDetails_32B_Type_Pattern)
_module_typeBindings.MT320_SequenceB_TransactionDetails_32B_Type_Pattern = MT320_SequenceB_TransactionDetails_32B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceB_TransactionDetails_32H_Type_Pattern
class MT320_SequenceB_TransactionDetails_32H_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceB_TransactionDetails_32H_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 289, 1)
    _Documentation = None
MT320_SequenceB_TransactionDetails_32H_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceB_TransactionDetails_32H_Type_Pattern._CF_pattern.addPattern(pattern='((N)?(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})')
MT320_SequenceB_TransactionDetails_32H_Type_Pattern._InitializeFacetMap(MT320_SequenceB_TransactionDetails_32H_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceB_TransactionDetails_32H_Type_Pattern', MT320_SequenceB_TransactionDetails_32H_Type_Pattern)
_module_typeBindings.MT320_SequenceB_TransactionDetails_32H_Type_Pattern = MT320_SequenceB_TransactionDetails_32H_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceB_TransactionDetails_30X_Type_Pattern
class MT320_SequenceB_TransactionDetails_30X_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceB_TransactionDetails_30X_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 302, 1)
    _Documentation = None
MT320_SequenceB_TransactionDetails_30X_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceB_TransactionDetails_30X_Type_Pattern._CF_pattern.addPattern(pattern='([0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))')
MT320_SequenceB_TransactionDetails_30X_Type_Pattern._InitializeFacetMap(MT320_SequenceB_TransactionDetails_30X_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceB_TransactionDetails_30X_Type_Pattern', MT320_SequenceB_TransactionDetails_30X_Type_Pattern)
_module_typeBindings.MT320_SequenceB_TransactionDetails_30X_Type_Pattern = MT320_SequenceB_TransactionDetails_30X_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceB_TransactionDetails_34E_Type_Pattern
class MT320_SequenceB_TransactionDetails_34E_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceB_TransactionDetails_34E_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 315, 1)
    _Documentation = None
MT320_SequenceB_TransactionDetails_34E_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceB_TransactionDetails_34E_Type_Pattern._CF_pattern.addPattern(pattern='((N)?(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})')
MT320_SequenceB_TransactionDetails_34E_Type_Pattern._InitializeFacetMap(MT320_SequenceB_TransactionDetails_34E_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceB_TransactionDetails_34E_Type_Pattern', MT320_SequenceB_TransactionDetails_34E_Type_Pattern)
_module_typeBindings.MT320_SequenceB_TransactionDetails_34E_Type_Pattern = MT320_SequenceB_TransactionDetails_34E_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceB_TransactionDetails_37G_Type_Pattern
class MT320_SequenceB_TransactionDetails_37G_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceB_TransactionDetails_37G_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 328, 1)
    _Documentation = None
MT320_SequenceB_TransactionDetails_37G_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceB_TransactionDetails_37G_Type_Pattern._CF_pattern.addPattern(pattern='((N)?[0-9,(?0-9)]{1,12})')
MT320_SequenceB_TransactionDetails_37G_Type_Pattern._InitializeFacetMap(MT320_SequenceB_TransactionDetails_37G_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceB_TransactionDetails_37G_Type_Pattern', MT320_SequenceB_TransactionDetails_37G_Type_Pattern)
_module_typeBindings.MT320_SequenceB_TransactionDetails_37G_Type_Pattern = MT320_SequenceB_TransactionDetails_37G_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceB_TransactionDetails_14D_Type_Pattern
class MT320_SequenceB_TransactionDetails_14D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceB_TransactionDetails_14D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 341, 1)
    _Documentation = None
MT320_SequenceB_TransactionDetails_14D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceB_TransactionDetails_14D_Type_Pattern._CF_pattern.addPattern(pattern="(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,7})")
MT320_SequenceB_TransactionDetails_14D_Type_Pattern._InitializeFacetMap(MT320_SequenceB_TransactionDetails_14D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceB_TransactionDetails_14D_Type_Pattern', MT320_SequenceB_TransactionDetails_14D_Type_Pattern)
_module_typeBindings.MT320_SequenceB_TransactionDetails_14D_Type_Pattern = MT320_SequenceB_TransactionDetails_14D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceB_TransactionDetails_30F_Type_Pattern
class MT320_SequenceB_TransactionDetails_30F_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceB_TransactionDetails_30F_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 354, 1)
    _Documentation = None
MT320_SequenceB_TransactionDetails_30F_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceB_TransactionDetails_30F_Type_Pattern._CF_pattern.addPattern(pattern='([0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))')
MT320_SequenceB_TransactionDetails_30F_Type_Pattern._InitializeFacetMap(MT320_SequenceB_TransactionDetails_30F_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceB_TransactionDetails_30F_Type_Pattern', MT320_SequenceB_TransactionDetails_30F_Type_Pattern)
_module_typeBindings.MT320_SequenceB_TransactionDetails_30F_Type_Pattern = MT320_SequenceB_TransactionDetails_30F_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceB_TransactionDetails_38J_Type_Pattern
class MT320_SequenceB_TransactionDetails_38J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceB_TransactionDetails_38J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 367, 1)
    _Documentation = None
MT320_SequenceB_TransactionDetails_38J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceB_TransactionDetails_38J_Type_Pattern._CF_pattern.addPattern(pattern='([A-Z]{1}[0-9]{3})')
MT320_SequenceB_TransactionDetails_38J_Type_Pattern._InitializeFacetMap(MT320_SequenceB_TransactionDetails_38J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceB_TransactionDetails_38J_Type_Pattern', MT320_SequenceB_TransactionDetails_38J_Type_Pattern)
_module_typeBindings.MT320_SequenceB_TransactionDetails_38J_Type_Pattern = MT320_SequenceB_TransactionDetails_38J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceB_TransactionDetails_39M_Type_Pattern
class MT320_SequenceB_TransactionDetails_39M_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceB_TransactionDetails_39M_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 380, 1)
    _Documentation = None
MT320_SequenceB_TransactionDetails_39M_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceB_TransactionDetails_39M_Type_Pattern._CF_pattern.addPattern(pattern='([A-Z]{2})')
MT320_SequenceB_TransactionDetails_39M_Type_Pattern._InitializeFacetMap(MT320_SequenceB_TransactionDetails_39M_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceB_TransactionDetails_39M_Type_Pattern', MT320_SequenceB_TransactionDetails_39M_Type_Pattern)
_module_typeBindings.MT320_SequenceB_TransactionDetails_39M_Type_Pattern = MT320_SequenceB_TransactionDetails_39M_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53A_Type_Pattern
class MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 393, 1)
    _Documentation = None
MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53A_Type_Pattern._InitializeFacetMap(MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53A_Type_Pattern', MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53A_Type_Pattern)
_module_typeBindings.MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53A_Type_Pattern = MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53D_Type_Pattern
class MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 406, 1)
    _Documentation = None
MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53D_Type_Pattern._InitializeFacetMap(MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53D_Type_Pattern', MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53D_Type_Pattern)
_module_typeBindings.MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53D_Type_Pattern = MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53J_Type_Pattern
class MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 419, 1)
    _Documentation = None
MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53J_Type_Pattern._InitializeFacetMap(MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53J_Type_Pattern', MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53J_Type_Pattern)
_module_typeBindings.MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53J_Type_Pattern = MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86A_Type_Pattern
class MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 432, 1)
    _Documentation = None
MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86A_Type_Pattern._InitializeFacetMap(MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86A_Type_Pattern', MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86A_Type_Pattern)
_module_typeBindings.MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86A_Type_Pattern = MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86D_Type_Pattern
class MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 445, 1)
    _Documentation = None
MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86D_Type_Pattern._InitializeFacetMap(MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86D_Type_Pattern', MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86D_Type_Pattern)
_module_typeBindings.MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86D_Type_Pattern = MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86J_Type_Pattern
class MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 458, 1)
    _Documentation = None
MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86J_Type_Pattern._InitializeFacetMap(MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86J_Type_Pattern', MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86J_Type_Pattern)
_module_typeBindings.MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86J_Type_Pattern = MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56A_Type_Pattern
class MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 471, 1)
    _Documentation = None
MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56A_Type_Pattern._InitializeFacetMap(MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56A_Type_Pattern', MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56A_Type_Pattern)
_module_typeBindings.MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56A_Type_Pattern = MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56D_Type_Pattern
class MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 484, 1)
    _Documentation = None
MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56D_Type_Pattern._InitializeFacetMap(MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56D_Type_Pattern', MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56D_Type_Pattern)
_module_typeBindings.MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56D_Type_Pattern = MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56J_Type_Pattern
class MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 497, 1)
    _Documentation = None
MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56J_Type_Pattern._InitializeFacetMap(MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56J_Type_Pattern', MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56J_Type_Pattern)
_module_typeBindings.MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56J_Type_Pattern = MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57A_Type_Pattern
class MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 510, 1)
    _Documentation = None
MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57A_Type_Pattern._InitializeFacetMap(MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57A_Type_Pattern', MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57A_Type_Pattern)
_module_typeBindings.MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57A_Type_Pattern = MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57D_Type_Pattern
class MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 523, 1)
    _Documentation = None
MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57D_Type_Pattern._InitializeFacetMap(MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57D_Type_Pattern', MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57D_Type_Pattern)
_module_typeBindings.MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57D_Type_Pattern = MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57J_Type_Pattern
class MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 536, 1)
    _Documentation = None
MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57J_Type_Pattern._InitializeFacetMap(MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57J_Type_Pattern', MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57J_Type_Pattern)
_module_typeBindings.MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57J_Type_Pattern = MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58A_Type_Pattern
class MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 549, 1)
    _Documentation = None
MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58A_Type_Pattern._InitializeFacetMap(MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58A_Type_Pattern', MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58A_Type_Pattern)
_module_typeBindings.MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58A_Type_Pattern = MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58D_Type_Pattern
class MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 562, 1)
    _Documentation = None
MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58D_Type_Pattern._InitializeFacetMap(MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58D_Type_Pattern', MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58D_Type_Pattern)
_module_typeBindings.MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58D_Type_Pattern = MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58J_Type_Pattern
class MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 575, 1)
    _Documentation = None
MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58J_Type_Pattern._InitializeFacetMap(MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58J_Type_Pattern', MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58J_Type_Pattern)
_module_typeBindings.MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58J_Type_Pattern = MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53A_Type_Pattern
class MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 588, 1)
    _Documentation = None
MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53A_Type_Pattern._InitializeFacetMap(MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53A_Type_Pattern', MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53A_Type_Pattern)
_module_typeBindings.MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53A_Type_Pattern = MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53D_Type_Pattern
class MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 601, 1)
    _Documentation = None
MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53D_Type_Pattern._InitializeFacetMap(MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53D_Type_Pattern', MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53D_Type_Pattern)
_module_typeBindings.MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53D_Type_Pattern = MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53J_Type_Pattern
class MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 614, 1)
    _Documentation = None
MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53J_Type_Pattern._InitializeFacetMap(MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53J_Type_Pattern', MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53J_Type_Pattern)
_module_typeBindings.MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53J_Type_Pattern = MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86A_Type_Pattern
class MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 627, 1)
    _Documentation = None
MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86A_Type_Pattern._InitializeFacetMap(MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86A_Type_Pattern', MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86A_Type_Pattern)
_module_typeBindings.MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86A_Type_Pattern = MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86D_Type_Pattern
class MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 640, 1)
    _Documentation = None
MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86D_Type_Pattern._InitializeFacetMap(MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86D_Type_Pattern', MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86D_Type_Pattern)
_module_typeBindings.MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86D_Type_Pattern = MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86J_Type_Pattern
class MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 653, 1)
    _Documentation = None
MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86J_Type_Pattern._InitializeFacetMap(MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86J_Type_Pattern', MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86J_Type_Pattern)
_module_typeBindings.MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86J_Type_Pattern = MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56A_Type_Pattern
class MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 666, 1)
    _Documentation = None
MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56A_Type_Pattern._InitializeFacetMap(MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56A_Type_Pattern', MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56A_Type_Pattern)
_module_typeBindings.MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56A_Type_Pattern = MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56D_Type_Pattern
class MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 679, 1)
    _Documentation = None
MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56D_Type_Pattern._InitializeFacetMap(MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56D_Type_Pattern', MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56D_Type_Pattern)
_module_typeBindings.MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56D_Type_Pattern = MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56J_Type_Pattern
class MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 692, 1)
    _Documentation = None
MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56J_Type_Pattern._InitializeFacetMap(MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56J_Type_Pattern', MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56J_Type_Pattern)
_module_typeBindings.MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56J_Type_Pattern = MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57A_Type_Pattern
class MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 705, 1)
    _Documentation = None
MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57A_Type_Pattern._InitializeFacetMap(MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57A_Type_Pattern', MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57A_Type_Pattern)
_module_typeBindings.MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57A_Type_Pattern = MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57D_Type_Pattern
class MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 718, 1)
    _Documentation = None
MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57D_Type_Pattern._InitializeFacetMap(MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57D_Type_Pattern', MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57D_Type_Pattern)
_module_typeBindings.MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57D_Type_Pattern = MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57J_Type_Pattern
class MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 731, 1)
    _Documentation = None
MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57J_Type_Pattern._InitializeFacetMap(MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57J_Type_Pattern', MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57J_Type_Pattern)
_module_typeBindings.MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57J_Type_Pattern = MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58A_Type_Pattern
class MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 744, 1)
    _Documentation = None
MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58A_Type_Pattern._InitializeFacetMap(MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58A_Type_Pattern', MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58A_Type_Pattern)
_module_typeBindings.MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58A_Type_Pattern = MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58D_Type_Pattern
class MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 757, 1)
    _Documentation = None
MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58D_Type_Pattern._InitializeFacetMap(MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58D_Type_Pattern', MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58D_Type_Pattern)
_module_typeBindings.MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58D_Type_Pattern = MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58J_Type_Pattern
class MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 770, 1)
    _Documentation = None
MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58J_Type_Pattern._InitializeFacetMap(MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58J_Type_Pattern', MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58J_Type_Pattern)
_module_typeBindings.MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58J_Type_Pattern = MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53A_Type_Pattern
class MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 783, 1)
    _Documentation = None
MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53A_Type_Pattern._InitializeFacetMap(MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53A_Type_Pattern', MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53A_Type_Pattern)
_module_typeBindings.MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53A_Type_Pattern = MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53D_Type_Pattern
class MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 796, 1)
    _Documentation = None
MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53D_Type_Pattern._InitializeFacetMap(MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53D_Type_Pattern', MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53D_Type_Pattern)
_module_typeBindings.MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53D_Type_Pattern = MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53J_Type_Pattern
class MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 809, 1)
    _Documentation = None
MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53J_Type_Pattern._InitializeFacetMap(MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53J_Type_Pattern', MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53J_Type_Pattern)
_module_typeBindings.MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53J_Type_Pattern = MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86A_Type_Pattern
class MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 822, 1)
    _Documentation = None
MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86A_Type_Pattern._InitializeFacetMap(MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86A_Type_Pattern', MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86A_Type_Pattern)
_module_typeBindings.MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86A_Type_Pattern = MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86D_Type_Pattern
class MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 835, 1)
    _Documentation = None
MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86D_Type_Pattern._InitializeFacetMap(MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86D_Type_Pattern', MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86D_Type_Pattern)
_module_typeBindings.MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86D_Type_Pattern = MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86J_Type_Pattern
class MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 848, 1)
    _Documentation = None
MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86J_Type_Pattern._InitializeFacetMap(MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86J_Type_Pattern', MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86J_Type_Pattern)
_module_typeBindings.MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86J_Type_Pattern = MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56A_Type_Pattern
class MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 861, 1)
    _Documentation = None
MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56A_Type_Pattern._InitializeFacetMap(MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56A_Type_Pattern', MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56A_Type_Pattern)
_module_typeBindings.MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56A_Type_Pattern = MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56D_Type_Pattern
class MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 874, 1)
    _Documentation = None
MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56D_Type_Pattern._InitializeFacetMap(MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56D_Type_Pattern', MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56D_Type_Pattern)
_module_typeBindings.MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56D_Type_Pattern = MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56J_Type_Pattern
class MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 887, 1)
    _Documentation = None
MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56J_Type_Pattern._InitializeFacetMap(MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56J_Type_Pattern', MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56J_Type_Pattern)
_module_typeBindings.MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56J_Type_Pattern = MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57A_Type_Pattern
class MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 900, 1)
    _Documentation = None
MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57A_Type_Pattern._InitializeFacetMap(MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57A_Type_Pattern', MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57A_Type_Pattern)
_module_typeBindings.MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57A_Type_Pattern = MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57D_Type_Pattern
class MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 913, 1)
    _Documentation = None
MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57D_Type_Pattern._InitializeFacetMap(MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57D_Type_Pattern', MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57D_Type_Pattern)
_module_typeBindings.MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57D_Type_Pattern = MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57J_Type_Pattern
class MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 926, 1)
    _Documentation = None
MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57J_Type_Pattern._InitializeFacetMap(MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57J_Type_Pattern', MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57J_Type_Pattern)
_module_typeBindings.MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57J_Type_Pattern = MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58A_Type_Pattern
class MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 939, 1)
    _Documentation = None
MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58A_Type_Pattern._InitializeFacetMap(MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58A_Type_Pattern', MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58A_Type_Pattern)
_module_typeBindings.MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58A_Type_Pattern = MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58D_Type_Pattern
class MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 952, 1)
    _Documentation = None
MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58D_Type_Pattern._InitializeFacetMap(MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58D_Type_Pattern', MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58D_Type_Pattern)
_module_typeBindings.MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58D_Type_Pattern = MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58J_Type_Pattern
class MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 965, 1)
    _Documentation = None
MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58J_Type_Pattern._InitializeFacetMap(MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58J_Type_Pattern', MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58J_Type_Pattern)
_module_typeBindings.MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58J_Type_Pattern = MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53A_Type_Pattern
class MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 978, 1)
    _Documentation = None
MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53A_Type_Pattern._InitializeFacetMap(MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53A_Type_Pattern', MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53A_Type_Pattern)
_module_typeBindings.MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53A_Type_Pattern = MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53D_Type_Pattern
class MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 991, 1)
    _Documentation = None
MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53D_Type_Pattern._InitializeFacetMap(MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53D_Type_Pattern', MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53D_Type_Pattern)
_module_typeBindings.MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53D_Type_Pattern = MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53J_Type_Pattern
class MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1004, 1)
    _Documentation = None
MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53J_Type_Pattern._InitializeFacetMap(MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53J_Type_Pattern', MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53J_Type_Pattern)
_module_typeBindings.MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53J_Type_Pattern = MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86A_Type_Pattern
class MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1017, 1)
    _Documentation = None
MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86A_Type_Pattern._InitializeFacetMap(MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86A_Type_Pattern', MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86A_Type_Pattern)
_module_typeBindings.MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86A_Type_Pattern = MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86D_Type_Pattern
class MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1030, 1)
    _Documentation = None
MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86D_Type_Pattern._InitializeFacetMap(MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86D_Type_Pattern', MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86D_Type_Pattern)
_module_typeBindings.MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86D_Type_Pattern = MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86J_Type_Pattern
class MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1043, 1)
    _Documentation = None
MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86J_Type_Pattern._InitializeFacetMap(MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86J_Type_Pattern', MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86J_Type_Pattern)
_module_typeBindings.MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86J_Type_Pattern = MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56A_Type_Pattern
class MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1056, 1)
    _Documentation = None
MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56A_Type_Pattern._InitializeFacetMap(MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56A_Type_Pattern', MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56A_Type_Pattern)
_module_typeBindings.MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56A_Type_Pattern = MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56D_Type_Pattern
class MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1069, 1)
    _Documentation = None
MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56D_Type_Pattern._InitializeFacetMap(MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56D_Type_Pattern', MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56D_Type_Pattern)
_module_typeBindings.MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56D_Type_Pattern = MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56J_Type_Pattern
class MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1082, 1)
    _Documentation = None
MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56J_Type_Pattern._InitializeFacetMap(MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56J_Type_Pattern', MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56J_Type_Pattern)
_module_typeBindings.MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56J_Type_Pattern = MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57A_Type_Pattern
class MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1095, 1)
    _Documentation = None
MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57A_Type_Pattern._InitializeFacetMap(MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57A_Type_Pattern', MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57A_Type_Pattern)
_module_typeBindings.MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57A_Type_Pattern = MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57D_Type_Pattern
class MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1108, 1)
    _Documentation = None
MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57D_Type_Pattern._InitializeFacetMap(MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57D_Type_Pattern', MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57D_Type_Pattern)
_module_typeBindings.MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57D_Type_Pattern = MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57J_Type_Pattern
class MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1121, 1)
    _Documentation = None
MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57J_Type_Pattern._InitializeFacetMap(MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57J_Type_Pattern', MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57J_Type_Pattern)
_module_typeBindings.MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57J_Type_Pattern = MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58A_Type_Pattern
class MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1134, 1)
    _Documentation = None
MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58A_Type_Pattern._InitializeFacetMap(MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58A_Type_Pattern', MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58A_Type_Pattern)
_module_typeBindings.MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58A_Type_Pattern = MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58D_Type_Pattern
class MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1147, 1)
    _Documentation = None
MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58D_Type_Pattern._InitializeFacetMap(MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58D_Type_Pattern', MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58D_Type_Pattern)
_module_typeBindings.MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58D_Type_Pattern = MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58J_Type_Pattern
class MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1160, 1)
    _Documentation = None
MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58J_Type_Pattern._InitializeFacetMap(MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58J_Type_Pattern', MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58J_Type_Pattern)
_module_typeBindings.MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58J_Type_Pattern = MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceG_TaxInformation_37L_Type_Pattern
class MT320_SequenceG_TaxInformation_37L_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceG_TaxInformation_37L_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1173, 1)
    _Documentation = None
MT320_SequenceG_TaxInformation_37L_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceG_TaxInformation_37L_Type_Pattern._CF_pattern.addPattern(pattern='([0-9,(?0-9)]{1,12})')
MT320_SequenceG_TaxInformation_37L_Type_Pattern._InitializeFacetMap(MT320_SequenceG_TaxInformation_37L_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceG_TaxInformation_37L_Type_Pattern', MT320_SequenceG_TaxInformation_37L_Type_Pattern)
_module_typeBindings.MT320_SequenceG_TaxInformation_37L_Type_Pattern = MT320_SequenceG_TaxInformation_37L_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceG_TaxInformation_33B_Type_Pattern
class MT320_SequenceG_TaxInformation_33B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceG_TaxInformation_33B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1186, 1)
    _Documentation = None
MT320_SequenceG_TaxInformation_33B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceG_TaxInformation_33B_Type_Pattern._CF_pattern.addPattern(pattern='((AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})')
MT320_SequenceG_TaxInformation_33B_Type_Pattern._InitializeFacetMap(MT320_SequenceG_TaxInformation_33B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceG_TaxInformation_33B_Type_Pattern', MT320_SequenceG_TaxInformation_33B_Type_Pattern)
_module_typeBindings.MT320_SequenceG_TaxInformation_33B_Type_Pattern = MT320_SequenceG_TaxInformation_33B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceG_TaxInformation_36_Type_Pattern
class MT320_SequenceG_TaxInformation_36_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceG_TaxInformation_36_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1199, 1)
    _Documentation = None
MT320_SequenceG_TaxInformation_36_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceG_TaxInformation_36_Type_Pattern._CF_pattern.addPattern(pattern='([0-9,(?0-9)]{1,12})')
MT320_SequenceG_TaxInformation_36_Type_Pattern._InitializeFacetMap(MT320_SequenceG_TaxInformation_36_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceG_TaxInformation_36_Type_Pattern', MT320_SequenceG_TaxInformation_36_Type_Pattern)
_module_typeBindings.MT320_SequenceG_TaxInformation_36_Type_Pattern = MT320_SequenceG_TaxInformation_36_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceG_TaxInformation_33E_Type_Pattern
class MT320_SequenceG_TaxInformation_33E_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceG_TaxInformation_33E_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1212, 1)
    _Documentation = None
MT320_SequenceG_TaxInformation_33E_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceG_TaxInformation_33E_Type_Pattern._CF_pattern.addPattern(pattern='((AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})')
MT320_SequenceG_TaxInformation_33E_Type_Pattern._InitializeFacetMap(MT320_SequenceG_TaxInformation_33E_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceG_TaxInformation_33E_Type_Pattern', MT320_SequenceG_TaxInformation_33E_Type_Pattern)
_module_typeBindings.MT320_SequenceG_TaxInformation_33E_Type_Pattern = MT320_SequenceG_TaxInformation_33E_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceH_AdditionalInformation_29A_Type_Pattern
class MT320_SequenceH_AdditionalInformation_29A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceH_AdditionalInformation_29A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1225, 1)
    _Documentation = None
MT320_SequenceH_AdditionalInformation_29A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceH_AdditionalInformation_29A_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT320_SequenceH_AdditionalInformation_29A_Type_Pattern._InitializeFacetMap(MT320_SequenceH_AdditionalInformation_29A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceH_AdditionalInformation_29A_Type_Pattern', MT320_SequenceH_AdditionalInformation_29A_Type_Pattern)
_module_typeBindings.MT320_SequenceH_AdditionalInformation_29A_Type_Pattern = MT320_SequenceH_AdditionalInformation_29A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceH_AdditionalInformation_24D_Type_Pattern
class MT320_SequenceH_AdditionalInformation_24D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceH_AdditionalInformation_24D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1238, 1)
    _Documentation = None
MT320_SequenceH_AdditionalInformation_24D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceH_AdditionalInformation_24D_Type_Pattern._CF_pattern.addPattern(pattern="((BROK|ELEC|PHON)(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35})?)")
MT320_SequenceH_AdditionalInformation_24D_Type_Pattern._InitializeFacetMap(MT320_SequenceH_AdditionalInformation_24D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceH_AdditionalInformation_24D_Type_Pattern', MT320_SequenceH_AdditionalInformation_24D_Type_Pattern)
_module_typeBindings.MT320_SequenceH_AdditionalInformation_24D_Type_Pattern = MT320_SequenceH_AdditionalInformation_24D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceH_AdditionalInformation_84A_Type_Pattern
class MT320_SequenceH_AdditionalInformation_84A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceH_AdditionalInformation_84A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1251, 1)
    _Documentation = None
MT320_SequenceH_AdditionalInformation_84A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceH_AdditionalInformation_84A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT320_SequenceH_AdditionalInformation_84A_Type_Pattern._InitializeFacetMap(MT320_SequenceH_AdditionalInformation_84A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceH_AdditionalInformation_84A_Type_Pattern', MT320_SequenceH_AdditionalInformation_84A_Type_Pattern)
_module_typeBindings.MT320_SequenceH_AdditionalInformation_84A_Type_Pattern = MT320_SequenceH_AdditionalInformation_84A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceH_AdditionalInformation_84B_Type_Pattern
class MT320_SequenceH_AdditionalInformation_84B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceH_AdditionalInformation_84B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1264, 1)
    _Documentation = None
MT320_SequenceH_AdditionalInformation_84B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceH_AdditionalInformation_84B_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35})?)")
MT320_SequenceH_AdditionalInformation_84B_Type_Pattern._InitializeFacetMap(MT320_SequenceH_AdditionalInformation_84B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceH_AdditionalInformation_84B_Type_Pattern', MT320_SequenceH_AdditionalInformation_84B_Type_Pattern)
_module_typeBindings.MT320_SequenceH_AdditionalInformation_84B_Type_Pattern = MT320_SequenceH_AdditionalInformation_84B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceH_AdditionalInformation_84D_Type_Pattern
class MT320_SequenceH_AdditionalInformation_84D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceH_AdditionalInformation_84D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1277, 1)
    _Documentation = None
MT320_SequenceH_AdditionalInformation_84D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceH_AdditionalInformation_84D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT320_SequenceH_AdditionalInformation_84D_Type_Pattern._InitializeFacetMap(MT320_SequenceH_AdditionalInformation_84D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceH_AdditionalInformation_84D_Type_Pattern', MT320_SequenceH_AdditionalInformation_84D_Type_Pattern)
_module_typeBindings.MT320_SequenceH_AdditionalInformation_84D_Type_Pattern = MT320_SequenceH_AdditionalInformation_84D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceH_AdditionalInformation_84J_Type_Pattern
class MT320_SequenceH_AdditionalInformation_84J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceH_AdditionalInformation_84J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1290, 1)
    _Documentation = None
MT320_SequenceH_AdditionalInformation_84J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceH_AdditionalInformation_84J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT320_SequenceH_AdditionalInformation_84J_Type_Pattern._InitializeFacetMap(MT320_SequenceH_AdditionalInformation_84J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceH_AdditionalInformation_84J_Type_Pattern', MT320_SequenceH_AdditionalInformation_84J_Type_Pattern)
_module_typeBindings.MT320_SequenceH_AdditionalInformation_84J_Type_Pattern = MT320_SequenceH_AdditionalInformation_84J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceH_AdditionalInformation_85A_Type_Pattern
class MT320_SequenceH_AdditionalInformation_85A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceH_AdditionalInformation_85A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1303, 1)
    _Documentation = None
MT320_SequenceH_AdditionalInformation_85A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceH_AdditionalInformation_85A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT320_SequenceH_AdditionalInformation_85A_Type_Pattern._InitializeFacetMap(MT320_SequenceH_AdditionalInformation_85A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceH_AdditionalInformation_85A_Type_Pattern', MT320_SequenceH_AdditionalInformation_85A_Type_Pattern)
_module_typeBindings.MT320_SequenceH_AdditionalInformation_85A_Type_Pattern = MT320_SequenceH_AdditionalInformation_85A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceH_AdditionalInformation_85B_Type_Pattern
class MT320_SequenceH_AdditionalInformation_85B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceH_AdditionalInformation_85B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1316, 1)
    _Documentation = None
MT320_SequenceH_AdditionalInformation_85B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceH_AdditionalInformation_85B_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35})?)")
MT320_SequenceH_AdditionalInformation_85B_Type_Pattern._InitializeFacetMap(MT320_SequenceH_AdditionalInformation_85B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceH_AdditionalInformation_85B_Type_Pattern', MT320_SequenceH_AdditionalInformation_85B_Type_Pattern)
_module_typeBindings.MT320_SequenceH_AdditionalInformation_85B_Type_Pattern = MT320_SequenceH_AdditionalInformation_85B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceH_AdditionalInformation_85D_Type_Pattern
class MT320_SequenceH_AdditionalInformation_85D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceH_AdditionalInformation_85D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1329, 1)
    _Documentation = None
MT320_SequenceH_AdditionalInformation_85D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceH_AdditionalInformation_85D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT320_SequenceH_AdditionalInformation_85D_Type_Pattern._InitializeFacetMap(MT320_SequenceH_AdditionalInformation_85D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceH_AdditionalInformation_85D_Type_Pattern', MT320_SequenceH_AdditionalInformation_85D_Type_Pattern)
_module_typeBindings.MT320_SequenceH_AdditionalInformation_85D_Type_Pattern = MT320_SequenceH_AdditionalInformation_85D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceH_AdditionalInformation_85J_Type_Pattern
class MT320_SequenceH_AdditionalInformation_85J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceH_AdditionalInformation_85J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1342, 1)
    _Documentation = None
MT320_SequenceH_AdditionalInformation_85J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceH_AdditionalInformation_85J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT320_SequenceH_AdditionalInformation_85J_Type_Pattern._InitializeFacetMap(MT320_SequenceH_AdditionalInformation_85J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceH_AdditionalInformation_85J_Type_Pattern', MT320_SequenceH_AdditionalInformation_85J_Type_Pattern)
_module_typeBindings.MT320_SequenceH_AdditionalInformation_85J_Type_Pattern = MT320_SequenceH_AdditionalInformation_85J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceH_AdditionalInformation_88A_Type_Pattern
class MT320_SequenceH_AdditionalInformation_88A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceH_AdditionalInformation_88A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1355, 1)
    _Documentation = None
MT320_SequenceH_AdditionalInformation_88A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceH_AdditionalInformation_88A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT320_SequenceH_AdditionalInformation_88A_Type_Pattern._InitializeFacetMap(MT320_SequenceH_AdditionalInformation_88A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceH_AdditionalInformation_88A_Type_Pattern', MT320_SequenceH_AdditionalInformation_88A_Type_Pattern)
_module_typeBindings.MT320_SequenceH_AdditionalInformation_88A_Type_Pattern = MT320_SequenceH_AdditionalInformation_88A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceH_AdditionalInformation_88D_Type_Pattern
class MT320_SequenceH_AdditionalInformation_88D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceH_AdditionalInformation_88D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1368, 1)
    _Documentation = None
MT320_SequenceH_AdditionalInformation_88D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceH_AdditionalInformation_88D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT320_SequenceH_AdditionalInformation_88D_Type_Pattern._InitializeFacetMap(MT320_SequenceH_AdditionalInformation_88D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceH_AdditionalInformation_88D_Type_Pattern', MT320_SequenceH_AdditionalInformation_88D_Type_Pattern)
_module_typeBindings.MT320_SequenceH_AdditionalInformation_88D_Type_Pattern = MT320_SequenceH_AdditionalInformation_88D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceH_AdditionalInformation_88J_Type_Pattern
class MT320_SequenceH_AdditionalInformation_88J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceH_AdditionalInformation_88J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1381, 1)
    _Documentation = None
MT320_SequenceH_AdditionalInformation_88J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceH_AdditionalInformation_88J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT320_SequenceH_AdditionalInformation_88J_Type_Pattern._InitializeFacetMap(MT320_SequenceH_AdditionalInformation_88J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceH_AdditionalInformation_88J_Type_Pattern', MT320_SequenceH_AdditionalInformation_88J_Type_Pattern)
_module_typeBindings.MT320_SequenceH_AdditionalInformation_88J_Type_Pattern = MT320_SequenceH_AdditionalInformation_88J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceH_AdditionalInformation_71F_Type_Pattern
class MT320_SequenceH_AdditionalInformation_71F_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceH_AdditionalInformation_71F_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1394, 1)
    _Documentation = None
MT320_SequenceH_AdditionalInformation_71F_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceH_AdditionalInformation_71F_Type_Pattern._CF_pattern.addPattern(pattern='((AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})')
MT320_SequenceH_AdditionalInformation_71F_Type_Pattern._InitializeFacetMap(MT320_SequenceH_AdditionalInformation_71F_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceH_AdditionalInformation_71F_Type_Pattern', MT320_SequenceH_AdditionalInformation_71F_Type_Pattern)
_module_typeBindings.MT320_SequenceH_AdditionalInformation_71F_Type_Pattern = MT320_SequenceH_AdditionalInformation_71F_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceH_AdditionalInformation_26H_Type_Pattern
class MT320_SequenceH_AdditionalInformation_26H_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceH_AdditionalInformation_26H_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1407, 1)
    _Documentation = None
MT320_SequenceH_AdditionalInformation_26H_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceH_AdditionalInformation_26H_Type_Pattern._CF_pattern.addPattern(pattern="(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,16})")
MT320_SequenceH_AdditionalInformation_26H_Type_Pattern._InitializeFacetMap(MT320_SequenceH_AdditionalInformation_26H_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceH_AdditionalInformation_26H_Type_Pattern', MT320_SequenceH_AdditionalInformation_26H_Type_Pattern)
_module_typeBindings.MT320_SequenceH_AdditionalInformation_26H_Type_Pattern = MT320_SequenceH_AdditionalInformation_26H_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceH_AdditionalInformation_21G_Type_Pattern
class MT320_SequenceH_AdditionalInformation_21G_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceH_AdditionalInformation_21G_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1420, 1)
    _Documentation = None
MT320_SequenceH_AdditionalInformation_21G_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceH_AdditionalInformation_21G_Type_Pattern._CF_pattern.addPattern(pattern="([^/]([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,16}[^/])")
MT320_SequenceH_AdditionalInformation_21G_Type_Pattern._InitializeFacetMap(MT320_SequenceH_AdditionalInformation_21G_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceH_AdditionalInformation_21G_Type_Pattern', MT320_SequenceH_AdditionalInformation_21G_Type_Pattern)
_module_typeBindings.MT320_SequenceH_AdditionalInformation_21G_Type_Pattern = MT320_SequenceH_AdditionalInformation_21G_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceH_AdditionalInformation_34C_Type_Pattern
class MT320_SequenceH_AdditionalInformation_34C_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceH_AdditionalInformation_34C_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1433, 1)
    _Documentation = None
MT320_SequenceH_AdditionalInformation_34C_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceH_AdditionalInformation_34C_Type_Pattern._CF_pattern.addPattern(pattern='([A-Z0-9]{4}/(N)?(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})')
MT320_SequenceH_AdditionalInformation_34C_Type_Pattern._InitializeFacetMap(MT320_SequenceH_AdditionalInformation_34C_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceH_AdditionalInformation_34C_Type_Pattern', MT320_SequenceH_AdditionalInformation_34C_Type_Pattern)
_module_typeBindings.MT320_SequenceH_AdditionalInformation_34C_Type_Pattern = MT320_SequenceH_AdditionalInformation_34C_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceH_AdditionalInformation_72_Type_Pattern
class MT320_SequenceH_AdditionalInformation_72_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceH_AdditionalInformation_72_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1446, 1)
    _Documentation = None
MT320_SequenceH_AdditionalInformation_72_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceH_AdditionalInformation_72_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,6})")
MT320_SequenceH_AdditionalInformation_72_Type_Pattern._InitializeFacetMap(MT320_SequenceH_AdditionalInformation_72_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceH_AdditionalInformation_72_Type_Pattern', MT320_SequenceH_AdditionalInformation_72_Type_Pattern)
_module_typeBindings.MT320_SequenceH_AdditionalInformation_72_Type_Pattern = MT320_SequenceH_AdditionalInformation_72_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceI_AdditionalAmounts_18A_Type_Pattern
class MT320_SequenceI_AdditionalAmounts_18A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceI_AdditionalAmounts_18A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1459, 1)
    _Documentation = None
MT320_SequenceI_AdditionalAmounts_18A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceI_AdditionalAmounts_18A_Type_Pattern._CF_pattern.addPattern(pattern='([0-9]{1,5})')
MT320_SequenceI_AdditionalAmounts_18A_Type_Pattern._InitializeFacetMap(MT320_SequenceI_AdditionalAmounts_18A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceI_AdditionalAmounts_18A_Type_Pattern', MT320_SequenceI_AdditionalAmounts_18A_Type_Pattern)
_module_typeBindings.MT320_SequenceI_AdditionalAmounts_18A_Type_Pattern = MT320_SequenceI_AdditionalAmounts_18A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceI_AdditionalAmounts_AMOUNT_30F_Type_Pattern
class MT320_SequenceI_AdditionalAmounts_AMOUNT_30F_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceI_AdditionalAmounts_AMOUNT_30F_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1472, 1)
    _Documentation = None
MT320_SequenceI_AdditionalAmounts_AMOUNT_30F_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceI_AdditionalAmounts_AMOUNT_30F_Type_Pattern._CF_pattern.addPattern(pattern='([0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))')
MT320_SequenceI_AdditionalAmounts_AMOUNT_30F_Type_Pattern._InitializeFacetMap(MT320_SequenceI_AdditionalAmounts_AMOUNT_30F_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceI_AdditionalAmounts_AMOUNT_30F_Type_Pattern', MT320_SequenceI_AdditionalAmounts_AMOUNT_30F_Type_Pattern)
_module_typeBindings.MT320_SequenceI_AdditionalAmounts_AMOUNT_30F_Type_Pattern = MT320_SequenceI_AdditionalAmounts_AMOUNT_30F_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceI_AdditionalAmounts_AMOUNT_32H_Type_Pattern
class MT320_SequenceI_AdditionalAmounts_AMOUNT_32H_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceI_AdditionalAmounts_AMOUNT_32H_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1485, 1)
    _Documentation = None
MT320_SequenceI_AdditionalAmounts_AMOUNT_32H_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceI_AdditionalAmounts_AMOUNT_32H_Type_Pattern._CF_pattern.addPattern(pattern='((N)?(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})')
MT320_SequenceI_AdditionalAmounts_AMOUNT_32H_Type_Pattern._InitializeFacetMap(MT320_SequenceI_AdditionalAmounts_AMOUNT_32H_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceI_AdditionalAmounts_AMOUNT_32H_Type_Pattern', MT320_SequenceI_AdditionalAmounts_AMOUNT_32H_Type_Pattern)
_module_typeBindings.MT320_SequenceI_AdditionalAmounts_AMOUNT_32H_Type_Pattern = MT320_SequenceI_AdditionalAmounts_AMOUNT_32H_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceI_AdditionalAmounts_53A_Type_Pattern
class MT320_SequenceI_AdditionalAmounts_53A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceI_AdditionalAmounts_53A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1498, 1)
    _Documentation = None
MT320_SequenceI_AdditionalAmounts_53A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceI_AdditionalAmounts_53A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT320_SequenceI_AdditionalAmounts_53A_Type_Pattern._InitializeFacetMap(MT320_SequenceI_AdditionalAmounts_53A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceI_AdditionalAmounts_53A_Type_Pattern', MT320_SequenceI_AdditionalAmounts_53A_Type_Pattern)
_module_typeBindings.MT320_SequenceI_AdditionalAmounts_53A_Type_Pattern = MT320_SequenceI_AdditionalAmounts_53A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceI_AdditionalAmounts_53D_Type_Pattern
class MT320_SequenceI_AdditionalAmounts_53D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceI_AdditionalAmounts_53D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1511, 1)
    _Documentation = None
MT320_SequenceI_AdditionalAmounts_53D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceI_AdditionalAmounts_53D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT320_SequenceI_AdditionalAmounts_53D_Type_Pattern._InitializeFacetMap(MT320_SequenceI_AdditionalAmounts_53D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceI_AdditionalAmounts_53D_Type_Pattern', MT320_SequenceI_AdditionalAmounts_53D_Type_Pattern)
_module_typeBindings.MT320_SequenceI_AdditionalAmounts_53D_Type_Pattern = MT320_SequenceI_AdditionalAmounts_53D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceI_AdditionalAmounts_53J_Type_Pattern
class MT320_SequenceI_AdditionalAmounts_53J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceI_AdditionalAmounts_53J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1524, 1)
    _Documentation = None
MT320_SequenceI_AdditionalAmounts_53J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceI_AdditionalAmounts_53J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT320_SequenceI_AdditionalAmounts_53J_Type_Pattern._InitializeFacetMap(MT320_SequenceI_AdditionalAmounts_53J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceI_AdditionalAmounts_53J_Type_Pattern', MT320_SequenceI_AdditionalAmounts_53J_Type_Pattern)
_module_typeBindings.MT320_SequenceI_AdditionalAmounts_53J_Type_Pattern = MT320_SequenceI_AdditionalAmounts_53J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceI_AdditionalAmounts_86A_Type_Pattern
class MT320_SequenceI_AdditionalAmounts_86A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceI_AdditionalAmounts_86A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1537, 1)
    _Documentation = None
MT320_SequenceI_AdditionalAmounts_86A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceI_AdditionalAmounts_86A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT320_SequenceI_AdditionalAmounts_86A_Type_Pattern._InitializeFacetMap(MT320_SequenceI_AdditionalAmounts_86A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceI_AdditionalAmounts_86A_Type_Pattern', MT320_SequenceI_AdditionalAmounts_86A_Type_Pattern)
_module_typeBindings.MT320_SequenceI_AdditionalAmounts_86A_Type_Pattern = MT320_SequenceI_AdditionalAmounts_86A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceI_AdditionalAmounts_86D_Type_Pattern
class MT320_SequenceI_AdditionalAmounts_86D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceI_AdditionalAmounts_86D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1550, 1)
    _Documentation = None
MT320_SequenceI_AdditionalAmounts_86D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceI_AdditionalAmounts_86D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT320_SequenceI_AdditionalAmounts_86D_Type_Pattern._InitializeFacetMap(MT320_SequenceI_AdditionalAmounts_86D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceI_AdditionalAmounts_86D_Type_Pattern', MT320_SequenceI_AdditionalAmounts_86D_Type_Pattern)
_module_typeBindings.MT320_SequenceI_AdditionalAmounts_86D_Type_Pattern = MT320_SequenceI_AdditionalAmounts_86D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceI_AdditionalAmounts_86J_Type_Pattern
class MT320_SequenceI_AdditionalAmounts_86J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceI_AdditionalAmounts_86J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1563, 1)
    _Documentation = None
MT320_SequenceI_AdditionalAmounts_86J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceI_AdditionalAmounts_86J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT320_SequenceI_AdditionalAmounts_86J_Type_Pattern._InitializeFacetMap(MT320_SequenceI_AdditionalAmounts_86J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceI_AdditionalAmounts_86J_Type_Pattern', MT320_SequenceI_AdditionalAmounts_86J_Type_Pattern)
_module_typeBindings.MT320_SequenceI_AdditionalAmounts_86J_Type_Pattern = MT320_SequenceI_AdditionalAmounts_86J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceI_AdditionalAmounts_56A_Type_Pattern
class MT320_SequenceI_AdditionalAmounts_56A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceI_AdditionalAmounts_56A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1576, 1)
    _Documentation = None
MT320_SequenceI_AdditionalAmounts_56A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceI_AdditionalAmounts_56A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT320_SequenceI_AdditionalAmounts_56A_Type_Pattern._InitializeFacetMap(MT320_SequenceI_AdditionalAmounts_56A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceI_AdditionalAmounts_56A_Type_Pattern', MT320_SequenceI_AdditionalAmounts_56A_Type_Pattern)
_module_typeBindings.MT320_SequenceI_AdditionalAmounts_56A_Type_Pattern = MT320_SequenceI_AdditionalAmounts_56A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceI_AdditionalAmounts_56D_Type_Pattern
class MT320_SequenceI_AdditionalAmounts_56D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceI_AdditionalAmounts_56D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1589, 1)
    _Documentation = None
MT320_SequenceI_AdditionalAmounts_56D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceI_AdditionalAmounts_56D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT320_SequenceI_AdditionalAmounts_56D_Type_Pattern._InitializeFacetMap(MT320_SequenceI_AdditionalAmounts_56D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceI_AdditionalAmounts_56D_Type_Pattern', MT320_SequenceI_AdditionalAmounts_56D_Type_Pattern)
_module_typeBindings.MT320_SequenceI_AdditionalAmounts_56D_Type_Pattern = MT320_SequenceI_AdditionalAmounts_56D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceI_AdditionalAmounts_56J_Type_Pattern
class MT320_SequenceI_AdditionalAmounts_56J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceI_AdditionalAmounts_56J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1602, 1)
    _Documentation = None
MT320_SequenceI_AdditionalAmounts_56J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceI_AdditionalAmounts_56J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT320_SequenceI_AdditionalAmounts_56J_Type_Pattern._InitializeFacetMap(MT320_SequenceI_AdditionalAmounts_56J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceI_AdditionalAmounts_56J_Type_Pattern', MT320_SequenceI_AdditionalAmounts_56J_Type_Pattern)
_module_typeBindings.MT320_SequenceI_AdditionalAmounts_56J_Type_Pattern = MT320_SequenceI_AdditionalAmounts_56J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceI_AdditionalAmounts_57A_Type_Pattern
class MT320_SequenceI_AdditionalAmounts_57A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceI_AdditionalAmounts_57A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1615, 1)
    _Documentation = None
MT320_SequenceI_AdditionalAmounts_57A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceI_AdditionalAmounts_57A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT320_SequenceI_AdditionalAmounts_57A_Type_Pattern._InitializeFacetMap(MT320_SequenceI_AdditionalAmounts_57A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceI_AdditionalAmounts_57A_Type_Pattern', MT320_SequenceI_AdditionalAmounts_57A_Type_Pattern)
_module_typeBindings.MT320_SequenceI_AdditionalAmounts_57A_Type_Pattern = MT320_SequenceI_AdditionalAmounts_57A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceI_AdditionalAmounts_57D_Type_Pattern
class MT320_SequenceI_AdditionalAmounts_57D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceI_AdditionalAmounts_57D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1628, 1)
    _Documentation = None
MT320_SequenceI_AdditionalAmounts_57D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceI_AdditionalAmounts_57D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT320_SequenceI_AdditionalAmounts_57D_Type_Pattern._InitializeFacetMap(MT320_SequenceI_AdditionalAmounts_57D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceI_AdditionalAmounts_57D_Type_Pattern', MT320_SequenceI_AdditionalAmounts_57D_Type_Pattern)
_module_typeBindings.MT320_SequenceI_AdditionalAmounts_57D_Type_Pattern = MT320_SequenceI_AdditionalAmounts_57D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT320_SequenceI_AdditionalAmounts_57J_Type_Pattern
class MT320_SequenceI_AdditionalAmounts_57J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceI_AdditionalAmounts_57J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1641, 1)
    _Documentation = None
MT320_SequenceI_AdditionalAmounts_57J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT320_SequenceI_AdditionalAmounts_57J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT320_SequenceI_AdditionalAmounts_57J_Type_Pattern._InitializeFacetMap(MT320_SequenceI_AdditionalAmounts_57J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceI_AdditionalAmounts_57J_Type_Pattern', MT320_SequenceI_AdditionalAmounts_57J_Type_Pattern)
_module_typeBindings.MT320_SequenceI_AdditionalAmounts_57J_Type_Pattern = MT320_SequenceI_AdditionalAmounts_57J_Type_Pattern

# Complex type {http://www.w3schools.com}MT320_SequenceA_GeneralInformation with content type ELEMENT_ONLY
class MT320_SequenceA_GeneralInformation (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceA_GeneralInformation with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceA_GeneralInformation')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1654, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}SendersReference uses Python identifier SendersReference
    __SendersReference = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SendersReference'), 'SendersReference', '__httpwww_w3schools_com_MT320_SequenceA_GeneralInformation_httpwww_w3schools_comSendersReference', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1656, 3), )

    
    SendersReference = property(__SendersReference.value, __SendersReference.set, None, None)

    
    # Element {http://www.w3schools.com}RelatedReference uses Python identifier RelatedReference
    __RelatedReference = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'RelatedReference'), 'RelatedReference', '__httpwww_w3schools_com_MT320_SequenceA_GeneralInformation_httpwww_w3schools_comRelatedReference', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1657, 3), )

    
    RelatedReference = property(__RelatedReference.value, __RelatedReference.set, None, None)

    
    # Element {http://www.w3schools.com}TypeOfOperation uses Python identifier TypeOfOperation
    __TypeOfOperation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'TypeOfOperation'), 'TypeOfOperation', '__httpwww_w3schools_com_MT320_SequenceA_GeneralInformation_httpwww_w3schools_comTypeOfOperation', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1658, 3), )

    
    TypeOfOperation = property(__TypeOfOperation.value, __TypeOfOperation.set, None, None)

    
    # Element {http://www.w3schools.com}ScopeOfOperation uses Python identifier ScopeOfOperation
    __ScopeOfOperation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ScopeOfOperation'), 'ScopeOfOperation', '__httpwww_w3schools_com_MT320_SequenceA_GeneralInformation_httpwww_w3schools_comScopeOfOperation', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1659, 3), )

    
    ScopeOfOperation = property(__ScopeOfOperation.value, __ScopeOfOperation.set, None, None)

    
    # Element {http://www.w3schools.com}TypeOfEvent uses Python identifier TypeOfEvent
    __TypeOfEvent = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'TypeOfEvent'), 'TypeOfEvent', '__httpwww_w3schools_com_MT320_SequenceA_GeneralInformation_httpwww_w3schools_comTypeOfEvent', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1660, 3), )

    
    TypeOfEvent = property(__TypeOfEvent.value, __TypeOfEvent.set, None, None)

    
    # Element {http://www.w3schools.com}CommonReference uses Python identifier CommonReference
    __CommonReference = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CommonReference'), 'CommonReference', '__httpwww_w3schools_com_MT320_SequenceA_GeneralInformation_httpwww_w3schools_comCommonReference', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1661, 3), )

    
    CommonReference = property(__CommonReference.value, __CommonReference.set, None, None)

    
    # Element {http://www.w3schools.com}ContractNumberPartyA uses Python identifier ContractNumberPartyA
    __ContractNumberPartyA = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ContractNumberPartyA'), 'ContractNumberPartyA', '__httpwww_w3schools_com_MT320_SequenceA_GeneralInformation_httpwww_w3schools_comContractNumberPartyA', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1662, 3), )

    
    ContractNumberPartyA = property(__ContractNumberPartyA.value, __ContractNumberPartyA.set, None, None)

    
    # Element {http://www.w3schools.com}PartyA_A uses Python identifier PartyA_A
    __PartyA_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PartyA_A'), 'PartyA_A', '__httpwww_w3schools_com_MT320_SequenceA_GeneralInformation_httpwww_w3schools_comPartyA_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1664, 4), )

    
    PartyA_A = property(__PartyA_A.value, __PartyA_A.set, None, None)

    
    # Element {http://www.w3schools.com}PartyA_D uses Python identifier PartyA_D
    __PartyA_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PartyA_D'), 'PartyA_D', '__httpwww_w3schools_com_MT320_SequenceA_GeneralInformation_httpwww_w3schools_comPartyA_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1665, 4), )

    
    PartyA_D = property(__PartyA_D.value, __PartyA_D.set, None, None)

    
    # Element {http://www.w3schools.com}PartyA_J uses Python identifier PartyA_J
    __PartyA_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PartyA_J'), 'PartyA_J', '__httpwww_w3schools_com_MT320_SequenceA_GeneralInformation_httpwww_w3schools_comPartyA_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1666, 4), )

    
    PartyA_J = property(__PartyA_J.value, __PartyA_J.set, None, None)

    
    # Element {http://www.w3schools.com}PartyB_A uses Python identifier PartyB_A
    __PartyB_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PartyB_A'), 'PartyB_A', '__httpwww_w3schools_com_MT320_SequenceA_GeneralInformation_httpwww_w3schools_comPartyB_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1669, 4), )

    
    PartyB_A = property(__PartyB_A.value, __PartyB_A.set, None, None)

    
    # Element {http://www.w3schools.com}PartyB_D uses Python identifier PartyB_D
    __PartyB_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PartyB_D'), 'PartyB_D', '__httpwww_w3schools_com_MT320_SequenceA_GeneralInformation_httpwww_w3schools_comPartyB_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1670, 4), )

    
    PartyB_D = property(__PartyB_D.value, __PartyB_D.set, None, None)

    
    # Element {http://www.w3schools.com}PartyB_J uses Python identifier PartyB_J
    __PartyB_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PartyB_J'), 'PartyB_J', '__httpwww_w3schools_com_MT320_SequenceA_GeneralInformation_httpwww_w3schools_comPartyB_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1671, 4), )

    
    PartyB_J = property(__PartyB_J.value, __PartyB_J.set, None, None)

    
    # Element {http://www.w3schools.com}FundOrInstructingParty_A uses Python identifier FundOrInstructingParty_A
    __FundOrInstructingParty_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'FundOrInstructingParty_A'), 'FundOrInstructingParty_A', '__httpwww_w3schools_com_MT320_SequenceA_GeneralInformation_httpwww_w3schools_comFundOrInstructingParty_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1674, 4), )

    
    FundOrInstructingParty_A = property(__FundOrInstructingParty_A.value, __FundOrInstructingParty_A.set, None, None)

    
    # Element {http://www.w3schools.com}FundOrInstructingParty_D uses Python identifier FundOrInstructingParty_D
    __FundOrInstructingParty_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'FundOrInstructingParty_D'), 'FundOrInstructingParty_D', '__httpwww_w3schools_com_MT320_SequenceA_GeneralInformation_httpwww_w3schools_comFundOrInstructingParty_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1675, 4), )

    
    FundOrInstructingParty_D = property(__FundOrInstructingParty_D.value, __FundOrInstructingParty_D.set, None, None)

    
    # Element {http://www.w3schools.com}FundOrInstructingParty_J uses Python identifier FundOrInstructingParty_J
    __FundOrInstructingParty_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'FundOrInstructingParty_J'), 'FundOrInstructingParty_J', '__httpwww_w3schools_com_MT320_SequenceA_GeneralInformation_httpwww_w3schools_comFundOrInstructingParty_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1676, 4), )

    
    FundOrInstructingParty_J = property(__FundOrInstructingParty_J.value, __FundOrInstructingParty_J.set, None, None)

    
    # Element {http://www.w3schools.com}TermsAndConditions uses Python identifier TermsAndConditions
    __TermsAndConditions = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'TermsAndConditions'), 'TermsAndConditions', '__httpwww_w3schools_com_MT320_SequenceA_GeneralInformation_httpwww_w3schools_comTermsAndConditions', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1678, 3), )

    
    TermsAndConditions = property(__TermsAndConditions.value, __TermsAndConditions.set, None, None)

    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceA_GeneralInformation_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='15A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1680, 2)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1680, 2)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceA_GeneralInformation_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1681, 2)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1681, 2)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    
    # Attribute formatTag uses Python identifier formatTag
    __formatTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'formatTag'), 'formatTag', '__httpwww_w3schools_com_MT320_SequenceA_GeneralInformation_formatTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='False')
    __formatTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1682, 2)
    __formatTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1682, 2)
    
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
_module_typeBindings.MT320_SequenceA_GeneralInformation = MT320_SequenceA_GeneralInformation
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceA_GeneralInformation', MT320_SequenceA_GeneralInformation)


# Complex type {http://www.w3schools.com}MT320_SequenceB_TransactionDetails with content type ELEMENT_ONLY
class MT320_SequenceB_TransactionDetails (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceB_TransactionDetails with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceB_TransactionDetails')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1684, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}PartyAsRole uses Python identifier PartyAsRole
    __PartyAsRole = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PartyAsRole'), 'PartyAsRole', '__httpwww_w3schools_com_MT320_SequenceB_TransactionDetails_httpwww_w3schools_comPartyAsRole', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1686, 3), )

    
    PartyAsRole = property(__PartyAsRole.value, __PartyAsRole.set, None, None)

    
    # Element {http://www.w3schools.com}TradeDate uses Python identifier TradeDate
    __TradeDate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'TradeDate'), 'TradeDate', '__httpwww_w3schools_com_MT320_SequenceB_TransactionDetails_httpwww_w3schools_comTradeDate', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1687, 3), )

    
    TradeDate = property(__TradeDate.value, __TradeDate.set, None, None)

    
    # Element {http://www.w3schools.com}ValueDate uses Python identifier ValueDate
    __ValueDate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ValueDate'), 'ValueDate', '__httpwww_w3schools_com_MT320_SequenceB_TransactionDetails_httpwww_w3schools_comValueDate', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1688, 3), )

    
    ValueDate = property(__ValueDate.value, __ValueDate.set, None, None)

    
    # Element {http://www.w3schools.com}MaturityDate uses Python identifier MaturityDate
    __MaturityDate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'MaturityDate'), 'MaturityDate', '__httpwww_w3schools_com_MT320_SequenceB_TransactionDetails_httpwww_w3schools_comMaturityDate', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1689, 3), )

    
    MaturityDate = property(__MaturityDate.value, __MaturityDate.set, None, None)

    
    # Element {http://www.w3schools.com}CurrencyAndPrincipalAmount uses Python identifier CurrencyAndPrincipalAmount
    __CurrencyAndPrincipalAmount = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CurrencyAndPrincipalAmount'), 'CurrencyAndPrincipalAmount', '__httpwww_w3schools_com_MT320_SequenceB_TransactionDetails_httpwww_w3schools_comCurrencyAndPrincipalAmount', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1690, 3), )

    
    CurrencyAndPrincipalAmount = property(__CurrencyAndPrincipalAmount.value, __CurrencyAndPrincipalAmount.set, None, None)

    
    # Element {http://www.w3schools.com}AmountToBeSettled uses Python identifier AmountToBeSettled
    __AmountToBeSettled = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'AmountToBeSettled'), 'AmountToBeSettled', '__httpwww_w3schools_com_MT320_SequenceB_TransactionDetails_httpwww_w3schools_comAmountToBeSettled', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1691, 3), )

    
    AmountToBeSettled = property(__AmountToBeSettled.value, __AmountToBeSettled.set, None, None)

    
    # Element {http://www.w3schools.com}NextInterestDueDate uses Python identifier NextInterestDueDate
    __NextInterestDueDate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'NextInterestDueDate'), 'NextInterestDueDate', '__httpwww_w3schools_com_MT320_SequenceB_TransactionDetails_httpwww_w3schools_comNextInterestDueDate', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1692, 3), )

    
    NextInterestDueDate = property(__NextInterestDueDate.value, __NextInterestDueDate.set, None, None)

    
    # Element {http://www.w3schools.com}CurrencyAndInterestAmount uses Python identifier CurrencyAndInterestAmount
    __CurrencyAndInterestAmount = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CurrencyAndInterestAmount'), 'CurrencyAndInterestAmount', '__httpwww_w3schools_com_MT320_SequenceB_TransactionDetails_httpwww_w3schools_comCurrencyAndInterestAmount', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1693, 3), )

    
    CurrencyAndInterestAmount = property(__CurrencyAndInterestAmount.value, __CurrencyAndInterestAmount.set, None, None)

    
    # Element {http://www.w3schools.com}InterestRate uses Python identifier InterestRate
    __InterestRate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'InterestRate'), 'InterestRate', '__httpwww_w3schools_com_MT320_SequenceB_TransactionDetails_httpwww_w3schools_comInterestRate', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1694, 3), )

    
    InterestRate = property(__InterestRate.value, __InterestRate.set, None, None)

    
    # Element {http://www.w3schools.com}DayCountFraction uses Python identifier DayCountFraction
    __DayCountFraction = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DayCountFraction'), 'DayCountFraction', '__httpwww_w3schools_com_MT320_SequenceB_TransactionDetails_httpwww_w3schools_comDayCountFraction', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1695, 3), )

    
    DayCountFraction = property(__DayCountFraction.value, __DayCountFraction.set, None, None)

    
    # Element {http://www.w3schools.com}LastDayOfTheFirstInterestPeriod uses Python identifier LastDayOfTheFirstInterestPeriod
    __LastDayOfTheFirstInterestPeriod = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'LastDayOfTheFirstInterestPeriod'), 'LastDayOfTheFirstInterestPeriod', '__httpwww_w3schools_com_MT320_SequenceB_TransactionDetails_httpwww_w3schools_comLastDayOfTheFirstInterestPeriod', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1696, 3), )

    
    LastDayOfTheFirstInterestPeriod = property(__LastDayOfTheFirstInterestPeriod.value, __LastDayOfTheFirstInterestPeriod.set, None, None)

    
    # Element {http://www.w3schools.com}NumberOfDays uses Python identifier NumberOfDays
    __NumberOfDays = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'NumberOfDays'), 'NumberOfDays', '__httpwww_w3schools_com_MT320_SequenceB_TransactionDetails_httpwww_w3schools_comNumberOfDays', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1697, 3), )

    
    NumberOfDays = property(__NumberOfDays.value, __NumberOfDays.set, None, None)

    
    # Element {http://www.w3schools.com}PaymentClearingCentre uses Python identifier PaymentClearingCentre
    __PaymentClearingCentre = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PaymentClearingCentre'), 'PaymentClearingCentre', '__httpwww_w3schools_com_MT320_SequenceB_TransactionDetails_httpwww_w3schools_comPaymentClearingCentre', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1698, 3), )

    
    PaymentClearingCentre = property(__PaymentClearingCentre.value, __PaymentClearingCentre.set, None, None)

    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceB_TransactionDetails_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='15B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1700, 2)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1700, 2)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceB_TransactionDetails_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1701, 2)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1701, 2)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    
    # Attribute formatTag uses Python identifier formatTag
    __formatTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'formatTag'), 'formatTag', '__httpwww_w3schools_com_MT320_SequenceB_TransactionDetails_formatTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='False')
    __formatTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1702, 2)
    __formatTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1702, 2)
    
    formatTag = property(__formatTag.value, __formatTag.set, None, None)

    _ElementMap.update({
        __PartyAsRole.name() : __PartyAsRole,
        __TradeDate.name() : __TradeDate,
        __ValueDate.name() : __ValueDate,
        __MaturityDate.name() : __MaturityDate,
        __CurrencyAndPrincipalAmount.name() : __CurrencyAndPrincipalAmount,
        __AmountToBeSettled.name() : __AmountToBeSettled,
        __NextInterestDueDate.name() : __NextInterestDueDate,
        __CurrencyAndInterestAmount.name() : __CurrencyAndInterestAmount,
        __InterestRate.name() : __InterestRate,
        __DayCountFraction.name() : __DayCountFraction,
        __LastDayOfTheFirstInterestPeriod.name() : __LastDayOfTheFirstInterestPeriod,
        __NumberOfDays.name() : __NumberOfDays,
        __PaymentClearingCentre.name() : __PaymentClearingCentre
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory,
        __formatTag.name() : __formatTag
    })
_module_typeBindings.MT320_SequenceB_TransactionDetails = MT320_SequenceB_TransactionDetails
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceB_TransactionDetails', MT320_SequenceB_TransactionDetails)


# Complex type {http://www.w3schools.com}MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA with content type ELEMENT_ONLY
class MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1704, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}DeliveryAgent_A uses Python identifier DeliveryAgent_A
    __DeliveryAgent_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_A'), 'DeliveryAgent_A', '__httpwww_w3schools_com_MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_httpwww_w3schools_comDeliveryAgent_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1707, 4), )

    
    DeliveryAgent_A = property(__DeliveryAgent_A.value, __DeliveryAgent_A.set, None, None)

    
    # Element {http://www.w3schools.com}DeliveryAgent_D uses Python identifier DeliveryAgent_D
    __DeliveryAgent_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_D'), 'DeliveryAgent_D', '__httpwww_w3schools_com_MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_httpwww_w3schools_comDeliveryAgent_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1708, 4), )

    
    DeliveryAgent_D = property(__DeliveryAgent_D.value, __DeliveryAgent_D.set, None, None)

    
    # Element {http://www.w3schools.com}DeliveryAgent_J uses Python identifier DeliveryAgent_J
    __DeliveryAgent_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_J'), 'DeliveryAgent_J', '__httpwww_w3schools_com_MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_httpwww_w3schools_comDeliveryAgent_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1709, 4), )

    
    DeliveryAgent_J = property(__DeliveryAgent_J.value, __DeliveryAgent_J.set, None, None)

    
    # Element {http://www.w3schools.com}Intermediary2_A uses Python identifier Intermediary2_A
    __Intermediary2_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Intermediary2_A'), 'Intermediary2_A', '__httpwww_w3schools_com_MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_httpwww_w3schools_comIntermediary2_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1712, 4), )

    
    Intermediary2_A = property(__Intermediary2_A.value, __Intermediary2_A.set, None, None)

    
    # Element {http://www.w3schools.com}Intermediary2_D uses Python identifier Intermediary2_D
    __Intermediary2_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Intermediary2_D'), 'Intermediary2_D', '__httpwww_w3schools_com_MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_httpwww_w3schools_comIntermediary2_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1713, 4), )

    
    Intermediary2_D = property(__Intermediary2_D.value, __Intermediary2_D.set, None, None)

    
    # Element {http://www.w3schools.com}Intermediary2_J uses Python identifier Intermediary2_J
    __Intermediary2_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Intermediary2_J'), 'Intermediary2_J', '__httpwww_w3schools_com_MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_httpwww_w3schools_comIntermediary2_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1714, 4), )

    
    Intermediary2_J = property(__Intermediary2_J.value, __Intermediary2_J.set, None, None)

    
    # Element {http://www.w3schools.com}Intermediary_A uses Python identifier Intermediary_A
    __Intermediary_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_A'), 'Intermediary_A', '__httpwww_w3schools_com_MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_httpwww_w3schools_comIntermediary_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1717, 4), )

    
    Intermediary_A = property(__Intermediary_A.value, __Intermediary_A.set, None, None)

    
    # Element {http://www.w3schools.com}Intermediary_D uses Python identifier Intermediary_D
    __Intermediary_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_D'), 'Intermediary_D', '__httpwww_w3schools_com_MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_httpwww_w3schools_comIntermediary_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1718, 4), )

    
    Intermediary_D = property(__Intermediary_D.value, __Intermediary_D.set, None, None)

    
    # Element {http://www.w3schools.com}Intermediary_J uses Python identifier Intermediary_J
    __Intermediary_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_J'), 'Intermediary_J', '__httpwww_w3schools_com_MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_httpwww_w3schools_comIntermediary_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1719, 4), )

    
    Intermediary_J = property(__Intermediary_J.value, __Intermediary_J.set, None, None)

    
    # Element {http://www.w3schools.com}ReceivingAgent_A uses Python identifier ReceivingAgent_A
    __ReceivingAgent_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_A'), 'ReceivingAgent_A', '__httpwww_w3schools_com_MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_httpwww_w3schools_comReceivingAgent_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1722, 4), )

    
    ReceivingAgent_A = property(__ReceivingAgent_A.value, __ReceivingAgent_A.set, None, None)

    
    # Element {http://www.w3schools.com}ReceivingAgent_D uses Python identifier ReceivingAgent_D
    __ReceivingAgent_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_D'), 'ReceivingAgent_D', '__httpwww_w3schools_com_MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_httpwww_w3schools_comReceivingAgent_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1723, 4), )

    
    ReceivingAgent_D = property(__ReceivingAgent_D.value, __ReceivingAgent_D.set, None, None)

    
    # Element {http://www.w3schools.com}ReceivingAgent_J uses Python identifier ReceivingAgent_J
    __ReceivingAgent_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_J'), 'ReceivingAgent_J', '__httpwww_w3schools_com_MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_httpwww_w3schools_comReceivingAgent_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1724, 4), )

    
    ReceivingAgent_J = property(__ReceivingAgent_J.value, __ReceivingAgent_J.set, None, None)

    
    # Element {http://www.w3schools.com}BeneficiaryInstitution_A uses Python identifier BeneficiaryInstitution_A
    __BeneficiaryInstitution_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_A'), 'BeneficiaryInstitution_A', '__httpwww_w3schools_com_MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_httpwww_w3schools_comBeneficiaryInstitution_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1727, 4), )

    
    BeneficiaryInstitution_A = property(__BeneficiaryInstitution_A.value, __BeneficiaryInstitution_A.set, None, None)

    
    # Element {http://www.w3schools.com}BeneficiaryInstitution_D uses Python identifier BeneficiaryInstitution_D
    __BeneficiaryInstitution_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_D'), 'BeneficiaryInstitution_D', '__httpwww_w3schools_com_MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_httpwww_w3schools_comBeneficiaryInstitution_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1728, 4), )

    
    BeneficiaryInstitution_D = property(__BeneficiaryInstitution_D.value, __BeneficiaryInstitution_D.set, None, None)

    
    # Element {http://www.w3schools.com}BeneficiaryInstitution_J uses Python identifier BeneficiaryInstitution_J
    __BeneficiaryInstitution_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_J'), 'BeneficiaryInstitution_J', '__httpwww_w3schools_com_MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_httpwww_w3schools_comBeneficiaryInstitution_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1729, 4), )

    
    BeneficiaryInstitution_J = property(__BeneficiaryInstitution_J.value, __BeneficiaryInstitution_J.set, None, None)

    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='15C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1732, 2)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1732, 2)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1733, 2)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1733, 2)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    
    # Attribute formatTag uses Python identifier formatTag
    __formatTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'formatTag'), 'formatTag', '__httpwww_w3schools_com_MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_formatTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='False')
    __formatTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1734, 2)
    __formatTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1734, 2)
    
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
_module_typeBindings.MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA = MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA', MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA)


# Complex type {http://www.w3schools.com}MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB with content type ELEMENT_ONLY
class MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1736, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}DeliveryAgent_A uses Python identifier DeliveryAgent_A
    __DeliveryAgent_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_A'), 'DeliveryAgent_A', '__httpwww_w3schools_com_MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_httpwww_w3schools_comDeliveryAgent_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1739, 4), )

    
    DeliveryAgent_A = property(__DeliveryAgent_A.value, __DeliveryAgent_A.set, None, None)

    
    # Element {http://www.w3schools.com}DeliveryAgent_D uses Python identifier DeliveryAgent_D
    __DeliveryAgent_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_D'), 'DeliveryAgent_D', '__httpwww_w3schools_com_MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_httpwww_w3schools_comDeliveryAgent_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1740, 4), )

    
    DeliveryAgent_D = property(__DeliveryAgent_D.value, __DeliveryAgent_D.set, None, None)

    
    # Element {http://www.w3schools.com}DeliveryAgent_J uses Python identifier DeliveryAgent_J
    __DeliveryAgent_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_J'), 'DeliveryAgent_J', '__httpwww_w3schools_com_MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_httpwww_w3schools_comDeliveryAgent_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1741, 4), )

    
    DeliveryAgent_J = property(__DeliveryAgent_J.value, __DeliveryAgent_J.set, None, None)

    
    # Element {http://www.w3schools.com}Intermediary2_A uses Python identifier Intermediary2_A
    __Intermediary2_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Intermediary2_A'), 'Intermediary2_A', '__httpwww_w3schools_com_MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_httpwww_w3schools_comIntermediary2_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1744, 4), )

    
    Intermediary2_A = property(__Intermediary2_A.value, __Intermediary2_A.set, None, None)

    
    # Element {http://www.w3schools.com}Intermediary2_D uses Python identifier Intermediary2_D
    __Intermediary2_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Intermediary2_D'), 'Intermediary2_D', '__httpwww_w3schools_com_MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_httpwww_w3schools_comIntermediary2_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1745, 4), )

    
    Intermediary2_D = property(__Intermediary2_D.value, __Intermediary2_D.set, None, None)

    
    # Element {http://www.w3schools.com}Intermediary2_J uses Python identifier Intermediary2_J
    __Intermediary2_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Intermediary2_J'), 'Intermediary2_J', '__httpwww_w3schools_com_MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_httpwww_w3schools_comIntermediary2_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1746, 4), )

    
    Intermediary2_J = property(__Intermediary2_J.value, __Intermediary2_J.set, None, None)

    
    # Element {http://www.w3schools.com}Intermediary_A uses Python identifier Intermediary_A
    __Intermediary_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_A'), 'Intermediary_A', '__httpwww_w3schools_com_MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_httpwww_w3schools_comIntermediary_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1749, 4), )

    
    Intermediary_A = property(__Intermediary_A.value, __Intermediary_A.set, None, None)

    
    # Element {http://www.w3schools.com}Intermediary_D uses Python identifier Intermediary_D
    __Intermediary_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_D'), 'Intermediary_D', '__httpwww_w3schools_com_MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_httpwww_w3schools_comIntermediary_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1750, 4), )

    
    Intermediary_D = property(__Intermediary_D.value, __Intermediary_D.set, None, None)

    
    # Element {http://www.w3schools.com}Intermediary_J uses Python identifier Intermediary_J
    __Intermediary_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_J'), 'Intermediary_J', '__httpwww_w3schools_com_MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_httpwww_w3schools_comIntermediary_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1751, 4), )

    
    Intermediary_J = property(__Intermediary_J.value, __Intermediary_J.set, None, None)

    
    # Element {http://www.w3schools.com}ReceivingAgent_A uses Python identifier ReceivingAgent_A
    __ReceivingAgent_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_A'), 'ReceivingAgent_A', '__httpwww_w3schools_com_MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_httpwww_w3schools_comReceivingAgent_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1754, 4), )

    
    ReceivingAgent_A = property(__ReceivingAgent_A.value, __ReceivingAgent_A.set, None, None)

    
    # Element {http://www.w3schools.com}ReceivingAgent_D uses Python identifier ReceivingAgent_D
    __ReceivingAgent_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_D'), 'ReceivingAgent_D', '__httpwww_w3schools_com_MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_httpwww_w3schools_comReceivingAgent_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1755, 4), )

    
    ReceivingAgent_D = property(__ReceivingAgent_D.value, __ReceivingAgent_D.set, None, None)

    
    # Element {http://www.w3schools.com}ReceivingAgent_J uses Python identifier ReceivingAgent_J
    __ReceivingAgent_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_J'), 'ReceivingAgent_J', '__httpwww_w3schools_com_MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_httpwww_w3schools_comReceivingAgent_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1756, 4), )

    
    ReceivingAgent_J = property(__ReceivingAgent_J.value, __ReceivingAgent_J.set, None, None)

    
    # Element {http://www.w3schools.com}BeneficiaryInstitution_A uses Python identifier BeneficiaryInstitution_A
    __BeneficiaryInstitution_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_A'), 'BeneficiaryInstitution_A', '__httpwww_w3schools_com_MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_httpwww_w3schools_comBeneficiaryInstitution_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1759, 4), )

    
    BeneficiaryInstitution_A = property(__BeneficiaryInstitution_A.value, __BeneficiaryInstitution_A.set, None, None)

    
    # Element {http://www.w3schools.com}BeneficiaryInstitution_D uses Python identifier BeneficiaryInstitution_D
    __BeneficiaryInstitution_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_D'), 'BeneficiaryInstitution_D', '__httpwww_w3schools_com_MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_httpwww_w3schools_comBeneficiaryInstitution_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1760, 4), )

    
    BeneficiaryInstitution_D = property(__BeneficiaryInstitution_D.value, __BeneficiaryInstitution_D.set, None, None)

    
    # Element {http://www.w3schools.com}BeneficiaryInstitution_J uses Python identifier BeneficiaryInstitution_J
    __BeneficiaryInstitution_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_J'), 'BeneficiaryInstitution_J', '__httpwww_w3schools_com_MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_httpwww_w3schools_comBeneficiaryInstitution_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1761, 4), )

    
    BeneficiaryInstitution_J = property(__BeneficiaryInstitution_J.value, __BeneficiaryInstitution_J.set, None, None)

    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='15D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1764, 2)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1764, 2)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1765, 2)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1765, 2)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    
    # Attribute formatTag uses Python identifier formatTag
    __formatTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'formatTag'), 'formatTag', '__httpwww_w3schools_com_MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_formatTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='False')
    __formatTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1766, 2)
    __formatTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1766, 2)
    
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
_module_typeBindings.MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB = MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB', MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB)


# Complex type {http://www.w3schools.com}MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA with content type ELEMENT_ONLY
class MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1768, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}DeliveryAgent_A uses Python identifier DeliveryAgent_A
    __DeliveryAgent_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_A'), 'DeliveryAgent_A', '__httpwww_w3schools_com_MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_httpwww_w3schools_comDeliveryAgent_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1771, 4), )

    
    DeliveryAgent_A = property(__DeliveryAgent_A.value, __DeliveryAgent_A.set, None, None)

    
    # Element {http://www.w3schools.com}DeliveryAgent_D uses Python identifier DeliveryAgent_D
    __DeliveryAgent_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_D'), 'DeliveryAgent_D', '__httpwww_w3schools_com_MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_httpwww_w3schools_comDeliveryAgent_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1772, 4), )

    
    DeliveryAgent_D = property(__DeliveryAgent_D.value, __DeliveryAgent_D.set, None, None)

    
    # Element {http://www.w3schools.com}DeliveryAgent_J uses Python identifier DeliveryAgent_J
    __DeliveryAgent_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_J'), 'DeliveryAgent_J', '__httpwww_w3schools_com_MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_httpwww_w3schools_comDeliveryAgent_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1773, 4), )

    
    DeliveryAgent_J = property(__DeliveryAgent_J.value, __DeliveryAgent_J.set, None, None)

    
    # Element {http://www.w3schools.com}Intermediary2_A uses Python identifier Intermediary2_A
    __Intermediary2_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Intermediary2_A'), 'Intermediary2_A', '__httpwww_w3schools_com_MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_httpwww_w3schools_comIntermediary2_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1776, 4), )

    
    Intermediary2_A = property(__Intermediary2_A.value, __Intermediary2_A.set, None, None)

    
    # Element {http://www.w3schools.com}Intermediary2_D uses Python identifier Intermediary2_D
    __Intermediary2_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Intermediary2_D'), 'Intermediary2_D', '__httpwww_w3schools_com_MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_httpwww_w3schools_comIntermediary2_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1777, 4), )

    
    Intermediary2_D = property(__Intermediary2_D.value, __Intermediary2_D.set, None, None)

    
    # Element {http://www.w3schools.com}Intermediary2_J uses Python identifier Intermediary2_J
    __Intermediary2_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Intermediary2_J'), 'Intermediary2_J', '__httpwww_w3schools_com_MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_httpwww_w3schools_comIntermediary2_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1778, 4), )

    
    Intermediary2_J = property(__Intermediary2_J.value, __Intermediary2_J.set, None, None)

    
    # Element {http://www.w3schools.com}Intermediary_A uses Python identifier Intermediary_A
    __Intermediary_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_A'), 'Intermediary_A', '__httpwww_w3schools_com_MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_httpwww_w3schools_comIntermediary_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1781, 4), )

    
    Intermediary_A = property(__Intermediary_A.value, __Intermediary_A.set, None, None)

    
    # Element {http://www.w3schools.com}Intermediary_D uses Python identifier Intermediary_D
    __Intermediary_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_D'), 'Intermediary_D', '__httpwww_w3schools_com_MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_httpwww_w3schools_comIntermediary_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1782, 4), )

    
    Intermediary_D = property(__Intermediary_D.value, __Intermediary_D.set, None, None)

    
    # Element {http://www.w3schools.com}Intermediary_J uses Python identifier Intermediary_J
    __Intermediary_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_J'), 'Intermediary_J', '__httpwww_w3schools_com_MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_httpwww_w3schools_comIntermediary_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1783, 4), )

    
    Intermediary_J = property(__Intermediary_J.value, __Intermediary_J.set, None, None)

    
    # Element {http://www.w3schools.com}ReceivingAgent_A uses Python identifier ReceivingAgent_A
    __ReceivingAgent_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_A'), 'ReceivingAgent_A', '__httpwww_w3schools_com_MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_httpwww_w3schools_comReceivingAgent_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1786, 4), )

    
    ReceivingAgent_A = property(__ReceivingAgent_A.value, __ReceivingAgent_A.set, None, None)

    
    # Element {http://www.w3schools.com}ReceivingAgent_D uses Python identifier ReceivingAgent_D
    __ReceivingAgent_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_D'), 'ReceivingAgent_D', '__httpwww_w3schools_com_MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_httpwww_w3schools_comReceivingAgent_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1787, 4), )

    
    ReceivingAgent_D = property(__ReceivingAgent_D.value, __ReceivingAgent_D.set, None, None)

    
    # Element {http://www.w3schools.com}ReceivingAgent_J uses Python identifier ReceivingAgent_J
    __ReceivingAgent_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_J'), 'ReceivingAgent_J', '__httpwww_w3schools_com_MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_httpwww_w3schools_comReceivingAgent_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1788, 4), )

    
    ReceivingAgent_J = property(__ReceivingAgent_J.value, __ReceivingAgent_J.set, None, None)

    
    # Element {http://www.w3schools.com}BeneficiaryInstitution_A uses Python identifier BeneficiaryInstitution_A
    __BeneficiaryInstitution_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_A'), 'BeneficiaryInstitution_A', '__httpwww_w3schools_com_MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_httpwww_w3schools_comBeneficiaryInstitution_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1791, 4), )

    
    BeneficiaryInstitution_A = property(__BeneficiaryInstitution_A.value, __BeneficiaryInstitution_A.set, None, None)

    
    # Element {http://www.w3schools.com}BeneficiaryInstitution_D uses Python identifier BeneficiaryInstitution_D
    __BeneficiaryInstitution_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_D'), 'BeneficiaryInstitution_D', '__httpwww_w3schools_com_MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_httpwww_w3schools_comBeneficiaryInstitution_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1792, 4), )

    
    BeneficiaryInstitution_D = property(__BeneficiaryInstitution_D.value, __BeneficiaryInstitution_D.set, None, None)

    
    # Element {http://www.w3schools.com}BeneficiaryInstitution_J uses Python identifier BeneficiaryInstitution_J
    __BeneficiaryInstitution_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_J'), 'BeneficiaryInstitution_J', '__httpwww_w3schools_com_MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_httpwww_w3schools_comBeneficiaryInstitution_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1793, 4), )

    
    BeneficiaryInstitution_J = property(__BeneficiaryInstitution_J.value, __BeneficiaryInstitution_J.set, None, None)

    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='15E')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1796, 2)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1796, 2)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1797, 2)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1797, 2)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    
    # Attribute formatTag uses Python identifier formatTag
    __formatTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'formatTag'), 'formatTag', '__httpwww_w3schools_com_MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_formatTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='False')
    __formatTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1798, 2)
    __formatTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1798, 2)
    
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
_module_typeBindings.MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA = MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA', MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA)


# Complex type {http://www.w3schools.com}MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB with content type ELEMENT_ONLY
class MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1800, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}DeliveryAgent_A uses Python identifier DeliveryAgent_A
    __DeliveryAgent_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_A'), 'DeliveryAgent_A', '__httpwww_w3schools_com_MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_httpwww_w3schools_comDeliveryAgent_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1803, 4), )

    
    DeliveryAgent_A = property(__DeliveryAgent_A.value, __DeliveryAgent_A.set, None, None)

    
    # Element {http://www.w3schools.com}DeliveryAgent_D uses Python identifier DeliveryAgent_D
    __DeliveryAgent_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_D'), 'DeliveryAgent_D', '__httpwww_w3schools_com_MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_httpwww_w3schools_comDeliveryAgent_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1804, 4), )

    
    DeliveryAgent_D = property(__DeliveryAgent_D.value, __DeliveryAgent_D.set, None, None)

    
    # Element {http://www.w3schools.com}DeliveryAgent_J uses Python identifier DeliveryAgent_J
    __DeliveryAgent_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_J'), 'DeliveryAgent_J', '__httpwww_w3schools_com_MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_httpwww_w3schools_comDeliveryAgent_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1805, 4), )

    
    DeliveryAgent_J = property(__DeliveryAgent_J.value, __DeliveryAgent_J.set, None, None)

    
    # Element {http://www.w3schools.com}Intermediary2_A uses Python identifier Intermediary2_A
    __Intermediary2_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Intermediary2_A'), 'Intermediary2_A', '__httpwww_w3schools_com_MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_httpwww_w3schools_comIntermediary2_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1808, 4), )

    
    Intermediary2_A = property(__Intermediary2_A.value, __Intermediary2_A.set, None, None)

    
    # Element {http://www.w3schools.com}Intermediary2_D uses Python identifier Intermediary2_D
    __Intermediary2_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Intermediary2_D'), 'Intermediary2_D', '__httpwww_w3schools_com_MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_httpwww_w3schools_comIntermediary2_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1809, 4), )

    
    Intermediary2_D = property(__Intermediary2_D.value, __Intermediary2_D.set, None, None)

    
    # Element {http://www.w3schools.com}Intermediary2_J uses Python identifier Intermediary2_J
    __Intermediary2_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Intermediary2_J'), 'Intermediary2_J', '__httpwww_w3schools_com_MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_httpwww_w3schools_comIntermediary2_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1810, 4), )

    
    Intermediary2_J = property(__Intermediary2_J.value, __Intermediary2_J.set, None, None)

    
    # Element {http://www.w3schools.com}Intermediary_A uses Python identifier Intermediary_A
    __Intermediary_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_A'), 'Intermediary_A', '__httpwww_w3schools_com_MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_httpwww_w3schools_comIntermediary_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1813, 4), )

    
    Intermediary_A = property(__Intermediary_A.value, __Intermediary_A.set, None, None)

    
    # Element {http://www.w3schools.com}Intermediary_D uses Python identifier Intermediary_D
    __Intermediary_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_D'), 'Intermediary_D', '__httpwww_w3schools_com_MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_httpwww_w3schools_comIntermediary_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1814, 4), )

    
    Intermediary_D = property(__Intermediary_D.value, __Intermediary_D.set, None, None)

    
    # Element {http://www.w3schools.com}Intermediary_J uses Python identifier Intermediary_J
    __Intermediary_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_J'), 'Intermediary_J', '__httpwww_w3schools_com_MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_httpwww_w3schools_comIntermediary_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1815, 4), )

    
    Intermediary_J = property(__Intermediary_J.value, __Intermediary_J.set, None, None)

    
    # Element {http://www.w3schools.com}ReceivingAgent_A uses Python identifier ReceivingAgent_A
    __ReceivingAgent_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_A'), 'ReceivingAgent_A', '__httpwww_w3schools_com_MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_httpwww_w3schools_comReceivingAgent_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1818, 4), )

    
    ReceivingAgent_A = property(__ReceivingAgent_A.value, __ReceivingAgent_A.set, None, None)

    
    # Element {http://www.w3schools.com}ReceivingAgent_D uses Python identifier ReceivingAgent_D
    __ReceivingAgent_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_D'), 'ReceivingAgent_D', '__httpwww_w3schools_com_MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_httpwww_w3schools_comReceivingAgent_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1819, 4), )

    
    ReceivingAgent_D = property(__ReceivingAgent_D.value, __ReceivingAgent_D.set, None, None)

    
    # Element {http://www.w3schools.com}ReceivingAgent_J uses Python identifier ReceivingAgent_J
    __ReceivingAgent_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_J'), 'ReceivingAgent_J', '__httpwww_w3schools_com_MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_httpwww_w3schools_comReceivingAgent_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1820, 4), )

    
    ReceivingAgent_J = property(__ReceivingAgent_J.value, __ReceivingAgent_J.set, None, None)

    
    # Element {http://www.w3schools.com}BeneficiaryInstitution_A uses Python identifier BeneficiaryInstitution_A
    __BeneficiaryInstitution_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_A'), 'BeneficiaryInstitution_A', '__httpwww_w3schools_com_MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_httpwww_w3schools_comBeneficiaryInstitution_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1823, 4), )

    
    BeneficiaryInstitution_A = property(__BeneficiaryInstitution_A.value, __BeneficiaryInstitution_A.set, None, None)

    
    # Element {http://www.w3schools.com}BeneficiaryInstitution_D uses Python identifier BeneficiaryInstitution_D
    __BeneficiaryInstitution_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_D'), 'BeneficiaryInstitution_D', '__httpwww_w3schools_com_MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_httpwww_w3schools_comBeneficiaryInstitution_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1824, 4), )

    
    BeneficiaryInstitution_D = property(__BeneficiaryInstitution_D.value, __BeneficiaryInstitution_D.set, None, None)

    
    # Element {http://www.w3schools.com}BeneficiaryInstitution_J uses Python identifier BeneficiaryInstitution_J
    __BeneficiaryInstitution_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_J'), 'BeneficiaryInstitution_J', '__httpwww_w3schools_com_MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_httpwww_w3schools_comBeneficiaryInstitution_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1825, 4), )

    
    BeneficiaryInstitution_J = property(__BeneficiaryInstitution_J.value, __BeneficiaryInstitution_J.set, None, None)

    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='15F')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1828, 2)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1828, 2)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1829, 2)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1829, 2)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    
    # Attribute formatTag uses Python identifier formatTag
    __formatTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'formatTag'), 'formatTag', '__httpwww_w3schools_com_MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_formatTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='False')
    __formatTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1830, 2)
    __formatTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1830, 2)
    
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
_module_typeBindings.MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB = MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB', MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB)


# Complex type {http://www.w3schools.com}MT320_SequenceG_TaxInformation with content type ELEMENT_ONLY
class MT320_SequenceG_TaxInformation (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceG_TaxInformation with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceG_TaxInformation')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1832, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}TaxRate uses Python identifier TaxRate
    __TaxRate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'TaxRate'), 'TaxRate', '__httpwww_w3schools_com_MT320_SequenceG_TaxInformation_httpwww_w3schools_comTaxRate', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1834, 3), )

    
    TaxRate = property(__TaxRate.value, __TaxRate.set, None, None)

    
    # Element {http://www.w3schools.com}TransactionCurrencyAndNetInterestAmount uses Python identifier TransactionCurrencyAndNetInterestAmount
    __TransactionCurrencyAndNetInterestAmount = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'TransactionCurrencyAndNetInterestAmount'), 'TransactionCurrencyAndNetInterestAmount', '__httpwww_w3schools_com_MT320_SequenceG_TaxInformation_httpwww_w3schools_comTransactionCurrencyAndNetInterestAmount', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1835, 3), )

    
    TransactionCurrencyAndNetInterestAmount = property(__TransactionCurrencyAndNetInterestAmount.value, __TransactionCurrencyAndNetInterestAmount.set, None, None)

    
    # Element {http://www.w3schools.com}ExchangeRate uses Python identifier ExchangeRate
    __ExchangeRate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ExchangeRate'), 'ExchangeRate', '__httpwww_w3schools_com_MT320_SequenceG_TaxInformation_httpwww_w3schools_comExchangeRate', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1836, 3), )

    
    ExchangeRate = property(__ExchangeRate.value, __ExchangeRate.set, None, None)

    
    # Element {http://www.w3schools.com}ReportingCurrencyAndTaxAmount uses Python identifier ReportingCurrencyAndTaxAmount
    __ReportingCurrencyAndTaxAmount = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ReportingCurrencyAndTaxAmount'), 'ReportingCurrencyAndTaxAmount', '__httpwww_w3schools_com_MT320_SequenceG_TaxInformation_httpwww_w3schools_comReportingCurrencyAndTaxAmount', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1837, 3), )

    
    ReportingCurrencyAndTaxAmount = property(__ReportingCurrencyAndTaxAmount.value, __ReportingCurrencyAndTaxAmount.set, None, None)

    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceG_TaxInformation_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='15G')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1839, 2)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1839, 2)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceG_TaxInformation_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1840, 2)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1840, 2)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    
    # Attribute formatTag uses Python identifier formatTag
    __formatTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'formatTag'), 'formatTag', '__httpwww_w3schools_com_MT320_SequenceG_TaxInformation_formatTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='False')
    __formatTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1841, 2)
    __formatTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1841, 2)
    
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
_module_typeBindings.MT320_SequenceG_TaxInformation = MT320_SequenceG_TaxInformation
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceG_TaxInformation', MT320_SequenceG_TaxInformation)


# Complex type {http://www.w3schools.com}MT320_SequenceH_AdditionalInformation with content type ELEMENT_ONLY
class MT320_SequenceH_AdditionalInformation (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceH_AdditionalInformation with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceH_AdditionalInformation')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1843, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}ContactInformation uses Python identifier ContactInformation
    __ContactInformation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ContactInformation'), 'ContactInformation', '__httpwww_w3schools_com_MT320_SequenceH_AdditionalInformation_httpwww_w3schools_comContactInformation', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1845, 3), )

    
    ContactInformation = property(__ContactInformation.value, __ContactInformation.set, None, None)

    
    # Element {http://www.w3schools.com}DealingMethod uses Python identifier DealingMethod
    __DealingMethod = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DealingMethod'), 'DealingMethod', '__httpwww_w3schools_com_MT320_SequenceH_AdditionalInformation_httpwww_w3schools_comDealingMethod', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1846, 3), )

    
    DealingMethod = property(__DealingMethod.value, __DealingMethod.set, None, None)

    
    # Element {http://www.w3schools.com}DealingBranchPartyA_A uses Python identifier DealingBranchPartyA_A
    __DealingBranchPartyA_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DealingBranchPartyA_A'), 'DealingBranchPartyA_A', '__httpwww_w3schools_com_MT320_SequenceH_AdditionalInformation_httpwww_w3schools_comDealingBranchPartyA_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1848, 4), )

    
    DealingBranchPartyA_A = property(__DealingBranchPartyA_A.value, __DealingBranchPartyA_A.set, None, None)

    
    # Element {http://www.w3schools.com}DealingBranchPartyA_B uses Python identifier DealingBranchPartyA_B
    __DealingBranchPartyA_B = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DealingBranchPartyA_B'), 'DealingBranchPartyA_B', '__httpwww_w3schools_com_MT320_SequenceH_AdditionalInformation_httpwww_w3schools_comDealingBranchPartyA_B', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1849, 4), )

    
    DealingBranchPartyA_B = property(__DealingBranchPartyA_B.value, __DealingBranchPartyA_B.set, None, None)

    
    # Element {http://www.w3schools.com}DealingBranchPartyA_D uses Python identifier DealingBranchPartyA_D
    __DealingBranchPartyA_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DealingBranchPartyA_D'), 'DealingBranchPartyA_D', '__httpwww_w3schools_com_MT320_SequenceH_AdditionalInformation_httpwww_w3schools_comDealingBranchPartyA_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1850, 4), )

    
    DealingBranchPartyA_D = property(__DealingBranchPartyA_D.value, __DealingBranchPartyA_D.set, None, None)

    
    # Element {http://www.w3schools.com}DealingBranchPartyA_J uses Python identifier DealingBranchPartyA_J
    __DealingBranchPartyA_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DealingBranchPartyA_J'), 'DealingBranchPartyA_J', '__httpwww_w3schools_com_MT320_SequenceH_AdditionalInformation_httpwww_w3schools_comDealingBranchPartyA_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1851, 4), )

    
    DealingBranchPartyA_J = property(__DealingBranchPartyA_J.value, __DealingBranchPartyA_J.set, None, None)

    
    # Element {http://www.w3schools.com}DealingBranchPartyB_A uses Python identifier DealingBranchPartyB_A
    __DealingBranchPartyB_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DealingBranchPartyB_A'), 'DealingBranchPartyB_A', '__httpwww_w3schools_com_MT320_SequenceH_AdditionalInformation_httpwww_w3schools_comDealingBranchPartyB_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1854, 4), )

    
    DealingBranchPartyB_A = property(__DealingBranchPartyB_A.value, __DealingBranchPartyB_A.set, None, None)

    
    # Element {http://www.w3schools.com}DealingBranchPartyB_B uses Python identifier DealingBranchPartyB_B
    __DealingBranchPartyB_B = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DealingBranchPartyB_B'), 'DealingBranchPartyB_B', '__httpwww_w3schools_com_MT320_SequenceH_AdditionalInformation_httpwww_w3schools_comDealingBranchPartyB_B', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1855, 4), )

    
    DealingBranchPartyB_B = property(__DealingBranchPartyB_B.value, __DealingBranchPartyB_B.set, None, None)

    
    # Element {http://www.w3schools.com}DealingBranchPartyB_D uses Python identifier DealingBranchPartyB_D
    __DealingBranchPartyB_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DealingBranchPartyB_D'), 'DealingBranchPartyB_D', '__httpwww_w3schools_com_MT320_SequenceH_AdditionalInformation_httpwww_w3schools_comDealingBranchPartyB_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1856, 4), )

    
    DealingBranchPartyB_D = property(__DealingBranchPartyB_D.value, __DealingBranchPartyB_D.set, None, None)

    
    # Element {http://www.w3schools.com}DealingBranchPartyB_J uses Python identifier DealingBranchPartyB_J
    __DealingBranchPartyB_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DealingBranchPartyB_J'), 'DealingBranchPartyB_J', '__httpwww_w3schools_com_MT320_SequenceH_AdditionalInformation_httpwww_w3schools_comDealingBranchPartyB_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1857, 4), )

    
    DealingBranchPartyB_J = property(__DealingBranchPartyB_J.value, __DealingBranchPartyB_J.set, None, None)

    
    # Element {http://www.w3schools.com}BrokerIdentification_A uses Python identifier BrokerIdentification_A
    __BrokerIdentification_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'BrokerIdentification_A'), 'BrokerIdentification_A', '__httpwww_w3schools_com_MT320_SequenceH_AdditionalInformation_httpwww_w3schools_comBrokerIdentification_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1860, 4), )

    
    BrokerIdentification_A = property(__BrokerIdentification_A.value, __BrokerIdentification_A.set, None, None)

    
    # Element {http://www.w3schools.com}BrokerIdentification_D uses Python identifier BrokerIdentification_D
    __BrokerIdentification_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'BrokerIdentification_D'), 'BrokerIdentification_D', '__httpwww_w3schools_com_MT320_SequenceH_AdditionalInformation_httpwww_w3schools_comBrokerIdentification_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1861, 4), )

    
    BrokerIdentification_D = property(__BrokerIdentification_D.value, __BrokerIdentification_D.set, None, None)

    
    # Element {http://www.w3schools.com}BrokerIdentification_J uses Python identifier BrokerIdentification_J
    __BrokerIdentification_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'BrokerIdentification_J'), 'BrokerIdentification_J', '__httpwww_w3schools_com_MT320_SequenceH_AdditionalInformation_httpwww_w3schools_comBrokerIdentification_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1862, 4), )

    
    BrokerIdentification_J = property(__BrokerIdentification_J.value, __BrokerIdentification_J.set, None, None)

    
    # Element {http://www.w3schools.com}BrokersCommission uses Python identifier BrokersCommission
    __BrokersCommission = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'BrokersCommission'), 'BrokersCommission', '__httpwww_w3schools_com_MT320_SequenceH_AdditionalInformation_httpwww_w3schools_comBrokersCommission', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1864, 3), )

    
    BrokersCommission = property(__BrokersCommission.value, __BrokersCommission.set, None, None)

    
    # Element {http://www.w3schools.com}CounterpartysReference uses Python identifier CounterpartysReference
    __CounterpartysReference = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CounterpartysReference'), 'CounterpartysReference', '__httpwww_w3schools_com_MT320_SequenceH_AdditionalInformation_httpwww_w3schools_comCounterpartysReference', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1865, 3), )

    
    CounterpartysReference = property(__CounterpartysReference.value, __CounterpartysReference.set, None, None)

    
    # Element {http://www.w3schools.com}BrokersReference uses Python identifier BrokersReference
    __BrokersReference = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'BrokersReference'), 'BrokersReference', '__httpwww_w3schools_com_MT320_SequenceH_AdditionalInformation_httpwww_w3schools_comBrokersReference', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1866, 3), )

    
    BrokersReference = property(__BrokersReference.value, __BrokersReference.set, None, None)

    
    # Element {http://www.w3schools.com}CommissionAndFees uses Python identifier CommissionAndFees
    __CommissionAndFees = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CommissionAndFees'), 'CommissionAndFees', '__httpwww_w3schools_com_MT320_SequenceH_AdditionalInformation_httpwww_w3schools_comCommissionAndFees', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1867, 3), )

    
    CommissionAndFees = property(__CommissionAndFees.value, __CommissionAndFees.set, None, None)

    
    # Element {http://www.w3schools.com}SenderToReceiverInformation uses Python identifier SenderToReceiverInformation
    __SenderToReceiverInformation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SenderToReceiverInformation'), 'SenderToReceiverInformation', '__httpwww_w3schools_com_MT320_SequenceH_AdditionalInformation_httpwww_w3schools_comSenderToReceiverInformation', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1868, 3), )

    
    SenderToReceiverInformation = property(__SenderToReceiverInformation.value, __SenderToReceiverInformation.set, None, None)

    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceH_AdditionalInformation_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='15H')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1870, 2)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1870, 2)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceH_AdditionalInformation_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1871, 2)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1871, 2)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    
    # Attribute formatTag uses Python identifier formatTag
    __formatTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'formatTag'), 'formatTag', '__httpwww_w3schools_com_MT320_SequenceH_AdditionalInformation_formatTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='False')
    __formatTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1872, 2)
    __formatTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1872, 2)
    
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
        __BrokerIdentification_A.name() : __BrokerIdentification_A,
        __BrokerIdentification_D.name() : __BrokerIdentification_D,
        __BrokerIdentification_J.name() : __BrokerIdentification_J,
        __BrokersCommission.name() : __BrokersCommission,
        __CounterpartysReference.name() : __CounterpartysReference,
        __BrokersReference.name() : __BrokersReference,
        __CommissionAndFees.name() : __CommissionAndFees,
        __SenderToReceiverInformation.name() : __SenderToReceiverInformation
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory,
        __formatTag.name() : __formatTag
    })
_module_typeBindings.MT320_SequenceH_AdditionalInformation = MT320_SequenceH_AdditionalInformation
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceH_AdditionalInformation', MT320_SequenceH_AdditionalInformation)


# Complex type {http://www.w3schools.com}MT320_SequenceI_AdditionalAmounts with content type ELEMENT_ONLY
class MT320_SequenceI_AdditionalAmounts (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceI_AdditionalAmounts with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceI_AdditionalAmounts')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1874, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}NumberOfRepetitions uses Python identifier NumberOfRepetitions
    __NumberOfRepetitions = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'NumberOfRepetitions'), 'NumberOfRepetitions', '__httpwww_w3schools_com_MT320_SequenceI_AdditionalAmounts_httpwww_w3schools_comNumberOfRepetitions', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1876, 3), )

    
    NumberOfRepetitions = property(__NumberOfRepetitions.value, __NumberOfRepetitions.set, None, None)

    
    # Element {http://www.w3schools.com}AMOUNT uses Python identifier AMOUNT
    __AMOUNT = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'AMOUNT'), 'AMOUNT', '__httpwww_w3schools_com_MT320_SequenceI_AdditionalAmounts_httpwww_w3schools_comAMOUNT', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1877, 3), )

    
    AMOUNT = property(__AMOUNT.value, __AMOUNT.set, None, None)

    
    # Element {http://www.w3schools.com}DeliveryAgent_A uses Python identifier DeliveryAgent_A
    __DeliveryAgent_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_A'), 'DeliveryAgent_A', '__httpwww_w3schools_com_MT320_SequenceI_AdditionalAmounts_httpwww_w3schools_comDeliveryAgent_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1879, 4), )

    
    DeliveryAgent_A = property(__DeliveryAgent_A.value, __DeliveryAgent_A.set, None, None)

    
    # Element {http://www.w3schools.com}DeliveryAgent_D uses Python identifier DeliveryAgent_D
    __DeliveryAgent_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_D'), 'DeliveryAgent_D', '__httpwww_w3schools_com_MT320_SequenceI_AdditionalAmounts_httpwww_w3schools_comDeliveryAgent_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1880, 4), )

    
    DeliveryAgent_D = property(__DeliveryAgent_D.value, __DeliveryAgent_D.set, None, None)

    
    # Element {http://www.w3schools.com}DeliveryAgent_J uses Python identifier DeliveryAgent_J
    __DeliveryAgent_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_J'), 'DeliveryAgent_J', '__httpwww_w3schools_com_MT320_SequenceI_AdditionalAmounts_httpwww_w3schools_comDeliveryAgent_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1881, 4), )

    
    DeliveryAgent_J = property(__DeliveryAgent_J.value, __DeliveryAgent_J.set, None, None)

    
    # Element {http://www.w3schools.com}Intermediary2_A uses Python identifier Intermediary2_A
    __Intermediary2_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Intermediary2_A'), 'Intermediary2_A', '__httpwww_w3schools_com_MT320_SequenceI_AdditionalAmounts_httpwww_w3schools_comIntermediary2_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1884, 4), )

    
    Intermediary2_A = property(__Intermediary2_A.value, __Intermediary2_A.set, None, None)

    
    # Element {http://www.w3schools.com}Intermediary2_D uses Python identifier Intermediary2_D
    __Intermediary2_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Intermediary2_D'), 'Intermediary2_D', '__httpwww_w3schools_com_MT320_SequenceI_AdditionalAmounts_httpwww_w3schools_comIntermediary2_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1885, 4), )

    
    Intermediary2_D = property(__Intermediary2_D.value, __Intermediary2_D.set, None, None)

    
    # Element {http://www.w3schools.com}Intermediary2_J uses Python identifier Intermediary2_J
    __Intermediary2_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Intermediary2_J'), 'Intermediary2_J', '__httpwww_w3schools_com_MT320_SequenceI_AdditionalAmounts_httpwww_w3schools_comIntermediary2_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1886, 4), )

    
    Intermediary2_J = property(__Intermediary2_J.value, __Intermediary2_J.set, None, None)

    
    # Element {http://www.w3schools.com}Intermediary_A uses Python identifier Intermediary_A
    __Intermediary_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_A'), 'Intermediary_A', '__httpwww_w3schools_com_MT320_SequenceI_AdditionalAmounts_httpwww_w3schools_comIntermediary_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1889, 4), )

    
    Intermediary_A = property(__Intermediary_A.value, __Intermediary_A.set, None, None)

    
    # Element {http://www.w3schools.com}Intermediary_D uses Python identifier Intermediary_D
    __Intermediary_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_D'), 'Intermediary_D', '__httpwww_w3schools_com_MT320_SequenceI_AdditionalAmounts_httpwww_w3schools_comIntermediary_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1890, 4), )

    
    Intermediary_D = property(__Intermediary_D.value, __Intermediary_D.set, None, None)

    
    # Element {http://www.w3schools.com}Intermediary_J uses Python identifier Intermediary_J
    __Intermediary_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_J'), 'Intermediary_J', '__httpwww_w3schools_com_MT320_SequenceI_AdditionalAmounts_httpwww_w3schools_comIntermediary_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1891, 4), )

    
    Intermediary_J = property(__Intermediary_J.value, __Intermediary_J.set, None, None)

    
    # Element {http://www.w3schools.com}ReceivingAgent_A uses Python identifier ReceivingAgent_A
    __ReceivingAgent_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_A'), 'ReceivingAgent_A', '__httpwww_w3schools_com_MT320_SequenceI_AdditionalAmounts_httpwww_w3schools_comReceivingAgent_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1894, 4), )

    
    ReceivingAgent_A = property(__ReceivingAgent_A.value, __ReceivingAgent_A.set, None, None)

    
    # Element {http://www.w3schools.com}ReceivingAgent_D uses Python identifier ReceivingAgent_D
    __ReceivingAgent_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_D'), 'ReceivingAgent_D', '__httpwww_w3schools_com_MT320_SequenceI_AdditionalAmounts_httpwww_w3schools_comReceivingAgent_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1895, 4), )

    
    ReceivingAgent_D = property(__ReceivingAgent_D.value, __ReceivingAgent_D.set, None, None)

    
    # Element {http://www.w3schools.com}ReceivingAgent_J uses Python identifier ReceivingAgent_J
    __ReceivingAgent_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_J'), 'ReceivingAgent_J', '__httpwww_w3schools_com_MT320_SequenceI_AdditionalAmounts_httpwww_w3schools_comReceivingAgent_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1896, 4), )

    
    ReceivingAgent_J = property(__ReceivingAgent_J.value, __ReceivingAgent_J.set, None, None)

    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceI_AdditionalAmounts_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='15I')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1899, 2)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1899, 2)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceI_AdditionalAmounts_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1900, 2)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1900, 2)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    
    # Attribute formatTag uses Python identifier formatTag
    __formatTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'formatTag'), 'formatTag', '__httpwww_w3schools_com_MT320_SequenceI_AdditionalAmounts_formatTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='False')
    __formatTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1901, 2)
    __formatTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1901, 2)
    
    formatTag = property(__formatTag.value, __formatTag.set, None, None)

    _ElementMap.update({
        __NumberOfRepetitions.name() : __NumberOfRepetitions,
        __AMOUNT.name() : __AMOUNT,
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
        __ReceivingAgent_J.name() : __ReceivingAgent_J
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory,
        __formatTag.name() : __formatTag
    })
_module_typeBindings.MT320_SequenceI_AdditionalAmounts = MT320_SequenceI_AdditionalAmounts
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceI_AdditionalAmounts', MT320_SequenceI_AdditionalAmounts)


# Complex type {http://www.w3schools.com}MT320_SequenceI_AdditionalAmounts_AMOUNT with content type ELEMENT_ONLY
class MT320_SequenceI_AdditionalAmounts_AMOUNT (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceI_AdditionalAmounts_AMOUNT with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceI_AdditionalAmounts_AMOUNT')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1903, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}PaymentDate uses Python identifier PaymentDate
    __PaymentDate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PaymentDate'), 'PaymentDate', '__httpwww_w3schools_com_MT320_SequenceI_AdditionalAmounts_AMOUNT_httpwww_w3schools_comPaymentDate', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1905, 3), )

    
    PaymentDate = property(__PaymentDate.value, __PaymentDate.set, None, None)

    
    # Element {http://www.w3schools.com}CurrencyPaymentAmount uses Python identifier CurrencyPaymentAmount
    __CurrencyPaymentAmount = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CurrencyPaymentAmount'), 'CurrencyPaymentAmount', '__httpwww_w3schools_com_MT320_SequenceI_AdditionalAmounts_AMOUNT_httpwww_w3schools_comCurrencyPaymentAmount', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1906, 3), )

    
    CurrencyPaymentAmount = property(__CurrencyPaymentAmount.value, __CurrencyPaymentAmount.set, None, None)

    _ElementMap.update({
        __PaymentDate.name() : __PaymentDate,
        __CurrencyPaymentAmount.name() : __CurrencyPaymentAmount
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.MT320_SequenceI_AdditionalAmounts_AMOUNT = MT320_SequenceI_AdditionalAmounts_AMOUNT
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceI_AdditionalAmounts_AMOUNT', MT320_SequenceI_AdditionalAmounts_AMOUNT)


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1910, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}SequenceA_GeneralInformation uses Python identifier SequenceA_GeneralInformation
    __SequenceA_GeneralInformation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SequenceA_GeneralInformation'), 'SequenceA_GeneralInformation', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comSequenceA_GeneralInformation', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1912, 4), )

    
    SequenceA_GeneralInformation = property(__SequenceA_GeneralInformation.value, __SequenceA_GeneralInformation.set, None, None)

    
    # Element {http://www.w3schools.com}SequenceB_TransactionDetails uses Python identifier SequenceB_TransactionDetails
    __SequenceB_TransactionDetails = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SequenceB_TransactionDetails'), 'SequenceB_TransactionDetails', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comSequenceB_TransactionDetails', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1913, 4), )

    
    SequenceB_TransactionDetails = property(__SequenceB_TransactionDetails.value, __SequenceB_TransactionDetails.set, None, None)

    
    # Element {http://www.w3schools.com}SequenceC_SettlementInstructionsforAmountsPayablebyPartyA uses Python identifier SequenceC_SettlementInstructionsforAmountsPayablebyPartyA
    __SequenceC_SettlementInstructionsforAmountsPayablebyPartyA = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SequenceC_SettlementInstructionsforAmountsPayablebyPartyA'), 'SequenceC_SettlementInstructionsforAmountsPayablebyPartyA', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comSequenceC_SettlementInstructionsforAmountsPayablebyPartyA', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1914, 4), )

    
    SequenceC_SettlementInstructionsforAmountsPayablebyPartyA = property(__SequenceC_SettlementInstructionsforAmountsPayablebyPartyA.value, __SequenceC_SettlementInstructionsforAmountsPayablebyPartyA.set, None, None)

    
    # Element {http://www.w3schools.com}SequenceD_SettlementInstructionsforAmountsPayablebyPartyB uses Python identifier SequenceD_SettlementInstructionsforAmountsPayablebyPartyB
    __SequenceD_SettlementInstructionsforAmountsPayablebyPartyB = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SequenceD_SettlementInstructionsforAmountsPayablebyPartyB'), 'SequenceD_SettlementInstructionsforAmountsPayablebyPartyB', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comSequenceD_SettlementInstructionsforAmountsPayablebyPartyB', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1915, 4), )

    
    SequenceD_SettlementInstructionsforAmountsPayablebyPartyB = property(__SequenceD_SettlementInstructionsforAmountsPayablebyPartyB.value, __SequenceD_SettlementInstructionsforAmountsPayablebyPartyB.set, None, None)

    
    # Element {http://www.w3schools.com}SequenceE_SettlementInstructionsforInterestsPayablebyPartyA uses Python identifier SequenceE_SettlementInstructionsforInterestsPayablebyPartyA
    __SequenceE_SettlementInstructionsforInterestsPayablebyPartyA = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SequenceE_SettlementInstructionsforInterestsPayablebyPartyA'), 'SequenceE_SettlementInstructionsforInterestsPayablebyPartyA', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comSequenceE_SettlementInstructionsforInterestsPayablebyPartyA', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1916, 4), )

    
    SequenceE_SettlementInstructionsforInterestsPayablebyPartyA = property(__SequenceE_SettlementInstructionsforInterestsPayablebyPartyA.value, __SequenceE_SettlementInstructionsforInterestsPayablebyPartyA.set, None, None)

    
    # Element {http://www.w3schools.com}SequenceF_SettlementInstructionsforInterestsPayablebyPartyB uses Python identifier SequenceF_SettlementInstructionsforInterestsPayablebyPartyB
    __SequenceF_SettlementInstructionsforInterestsPayablebyPartyB = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SequenceF_SettlementInstructionsforInterestsPayablebyPartyB'), 'SequenceF_SettlementInstructionsforInterestsPayablebyPartyB', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comSequenceF_SettlementInstructionsforInterestsPayablebyPartyB', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1917, 4), )

    
    SequenceF_SettlementInstructionsforInterestsPayablebyPartyB = property(__SequenceF_SettlementInstructionsforInterestsPayablebyPartyB.value, __SequenceF_SettlementInstructionsforInterestsPayablebyPartyB.set, None, None)

    
    # Element {http://www.w3schools.com}SequenceG_TaxInformation uses Python identifier SequenceG_TaxInformation
    __SequenceG_TaxInformation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SequenceG_TaxInformation'), 'SequenceG_TaxInformation', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comSequenceG_TaxInformation', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1918, 4), )

    
    SequenceG_TaxInformation = property(__SequenceG_TaxInformation.value, __SequenceG_TaxInformation.set, None, None)

    
    # Element {http://www.w3schools.com}SequenceH_AdditionalInformation uses Python identifier SequenceH_AdditionalInformation
    __SequenceH_AdditionalInformation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SequenceH_AdditionalInformation'), 'SequenceH_AdditionalInformation', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comSequenceH_AdditionalInformation', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1919, 4), )

    
    SequenceH_AdditionalInformation = property(__SequenceH_AdditionalInformation.value, __SequenceH_AdditionalInformation.set, None, None)

    
    # Element {http://www.w3schools.com}SequenceI_AdditionalAmounts uses Python identifier SequenceI_AdditionalAmounts
    __SequenceI_AdditionalAmounts = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SequenceI_AdditionalAmounts'), 'SequenceI_AdditionalAmounts', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comSequenceI_AdditionalAmounts', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1920, 4), )

    
    SequenceI_AdditionalAmounts = property(__SequenceI_AdditionalAmounts.value, __SequenceI_AdditionalAmounts.set, None, None)

    _ElementMap.update({
        __SequenceA_GeneralInformation.name() : __SequenceA_GeneralInformation,
        __SequenceB_TransactionDetails.name() : __SequenceB_TransactionDetails,
        __SequenceC_SettlementInstructionsforAmountsPayablebyPartyA.name() : __SequenceC_SettlementInstructionsforAmountsPayablebyPartyA,
        __SequenceD_SettlementInstructionsforAmountsPayablebyPartyB.name() : __SequenceD_SettlementInstructionsforAmountsPayablebyPartyB,
        __SequenceE_SettlementInstructionsforInterestsPayablebyPartyA.name() : __SequenceE_SettlementInstructionsforInterestsPayablebyPartyA,
        __SequenceF_SettlementInstructionsforInterestsPayablebyPartyB.name() : __SequenceF_SettlementInstructionsforInterestsPayablebyPartyB,
        __SequenceG_TaxInformation.name() : __SequenceG_TaxInformation,
        __SequenceH_AdditionalInformation.name() : __SequenceH_AdditionalInformation,
        __SequenceI_AdditionalAmounts.name() : __SequenceI_AdditionalAmounts
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON = CTD_ANON


# Complex type {http://www.w3schools.com}MT320_SequenceA_GeneralInformation_20_Type with content type SIMPLE
class MT320_SequenceA_GeneralInformation_20_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceA_GeneralInformation_20_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceA_GeneralInformation_20_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceA_GeneralInformation_20_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 8, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceA_GeneralInformation_20_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceA_GeneralInformation_20_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='20')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 11, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 11, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceA_GeneralInformation_20_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 12, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 12, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceA_GeneralInformation_20_Type = MT320_SequenceA_GeneralInformation_20_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceA_GeneralInformation_20_Type', MT320_SequenceA_GeneralInformation_20_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceA_GeneralInformation_21_Type with content type SIMPLE
class MT320_SequenceA_GeneralInformation_21_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceA_GeneralInformation_21_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceA_GeneralInformation_21_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceA_GeneralInformation_21_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 21, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceA_GeneralInformation_21_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceA_GeneralInformation_21_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='21')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 24, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 24, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceA_GeneralInformation_21_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 25, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 25, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceA_GeneralInformation_21_Type = MT320_SequenceA_GeneralInformation_21_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceA_GeneralInformation_21_Type', MT320_SequenceA_GeneralInformation_21_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceA_GeneralInformation_22A_Type with content type SIMPLE
class MT320_SequenceA_GeneralInformation_22A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceA_GeneralInformation_22A_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceA_GeneralInformation_22A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceA_GeneralInformation_22A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 34, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceA_GeneralInformation_22A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceA_GeneralInformation_22A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='22A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 37, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 37, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceA_GeneralInformation_22A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 38, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 38, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceA_GeneralInformation_22A_Type = MT320_SequenceA_GeneralInformation_22A_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceA_GeneralInformation_22A_Type', MT320_SequenceA_GeneralInformation_22A_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceA_GeneralInformation_94A_Type with content type SIMPLE
class MT320_SequenceA_GeneralInformation_94A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceA_GeneralInformation_94A_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceA_GeneralInformation_94A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceA_GeneralInformation_94A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 47, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceA_GeneralInformation_94A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceA_GeneralInformation_94A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='94A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 50, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 50, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceA_GeneralInformation_94A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 51, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 51, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceA_GeneralInformation_94A_Type = MT320_SequenceA_GeneralInformation_94A_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceA_GeneralInformation_94A_Type', MT320_SequenceA_GeneralInformation_94A_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceA_GeneralInformation_22B_Type with content type SIMPLE
class MT320_SequenceA_GeneralInformation_22B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceA_GeneralInformation_22B_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceA_GeneralInformation_22B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceA_GeneralInformation_22B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 60, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceA_GeneralInformation_22B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceA_GeneralInformation_22B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='22B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 63, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 63, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceA_GeneralInformation_22B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 64, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 64, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceA_GeneralInformation_22B_Type = MT320_SequenceA_GeneralInformation_22B_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceA_GeneralInformation_22B_Type', MT320_SequenceA_GeneralInformation_22B_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceA_GeneralInformation_22C_Type with content type SIMPLE
class MT320_SequenceA_GeneralInformation_22C_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceA_GeneralInformation_22C_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceA_GeneralInformation_22C_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceA_GeneralInformation_22C_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 73, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceA_GeneralInformation_22C_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceA_GeneralInformation_22C_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='22C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 76, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 76, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceA_GeneralInformation_22C_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 77, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 77, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceA_GeneralInformation_22C_Type = MT320_SequenceA_GeneralInformation_22C_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceA_GeneralInformation_22C_Type', MT320_SequenceA_GeneralInformation_22C_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceA_GeneralInformation_21N_Type with content type SIMPLE
class MT320_SequenceA_GeneralInformation_21N_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceA_GeneralInformation_21N_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceA_GeneralInformation_21N_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceA_GeneralInformation_21N_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 86, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceA_GeneralInformation_21N_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceA_GeneralInformation_21N_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='21N')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 89, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 89, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceA_GeneralInformation_21N_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 90, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 90, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceA_GeneralInformation_21N_Type = MT320_SequenceA_GeneralInformation_21N_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceA_GeneralInformation_21N_Type', MT320_SequenceA_GeneralInformation_21N_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceA_GeneralInformation_82A_Type with content type SIMPLE
class MT320_SequenceA_GeneralInformation_82A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceA_GeneralInformation_82A_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceA_GeneralInformation_82A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceA_GeneralInformation_82A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 99, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceA_GeneralInformation_82A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceA_GeneralInformation_82A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='82A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 102, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 102, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceA_GeneralInformation_82A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 103, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 103, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceA_GeneralInformation_82A_Type = MT320_SequenceA_GeneralInformation_82A_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceA_GeneralInformation_82A_Type', MT320_SequenceA_GeneralInformation_82A_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceA_GeneralInformation_82D_Type with content type SIMPLE
class MT320_SequenceA_GeneralInformation_82D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceA_GeneralInformation_82D_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceA_GeneralInformation_82D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceA_GeneralInformation_82D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 112, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceA_GeneralInformation_82D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceA_GeneralInformation_82D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='82D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 115, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 115, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceA_GeneralInformation_82D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 116, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 116, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceA_GeneralInformation_82D_Type = MT320_SequenceA_GeneralInformation_82D_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceA_GeneralInformation_82D_Type', MT320_SequenceA_GeneralInformation_82D_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceA_GeneralInformation_82J_Type with content type SIMPLE
class MT320_SequenceA_GeneralInformation_82J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceA_GeneralInformation_82J_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceA_GeneralInformation_82J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceA_GeneralInformation_82J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 125, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceA_GeneralInformation_82J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceA_GeneralInformation_82J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='82J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 128, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 128, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceA_GeneralInformation_82J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 129, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 129, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceA_GeneralInformation_82J_Type = MT320_SequenceA_GeneralInformation_82J_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceA_GeneralInformation_82J_Type', MT320_SequenceA_GeneralInformation_82J_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceA_GeneralInformation_87A_Type with content type SIMPLE
class MT320_SequenceA_GeneralInformation_87A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceA_GeneralInformation_87A_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceA_GeneralInformation_87A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceA_GeneralInformation_87A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 138, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceA_GeneralInformation_87A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceA_GeneralInformation_87A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='87A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 141, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 141, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceA_GeneralInformation_87A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 142, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 142, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceA_GeneralInformation_87A_Type = MT320_SequenceA_GeneralInformation_87A_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceA_GeneralInformation_87A_Type', MT320_SequenceA_GeneralInformation_87A_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceA_GeneralInformation_87D_Type with content type SIMPLE
class MT320_SequenceA_GeneralInformation_87D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceA_GeneralInformation_87D_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceA_GeneralInformation_87D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceA_GeneralInformation_87D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 151, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceA_GeneralInformation_87D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceA_GeneralInformation_87D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='87D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 154, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 154, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceA_GeneralInformation_87D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 155, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 155, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceA_GeneralInformation_87D_Type = MT320_SequenceA_GeneralInformation_87D_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceA_GeneralInformation_87D_Type', MT320_SequenceA_GeneralInformation_87D_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceA_GeneralInformation_87J_Type with content type SIMPLE
class MT320_SequenceA_GeneralInformation_87J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceA_GeneralInformation_87J_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceA_GeneralInformation_87J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceA_GeneralInformation_87J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 164, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceA_GeneralInformation_87J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceA_GeneralInformation_87J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='87J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 167, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 167, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceA_GeneralInformation_87J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 168, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 168, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceA_GeneralInformation_87J_Type = MT320_SequenceA_GeneralInformation_87J_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceA_GeneralInformation_87J_Type', MT320_SequenceA_GeneralInformation_87J_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceA_GeneralInformation_83A_Type with content type SIMPLE
class MT320_SequenceA_GeneralInformation_83A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceA_GeneralInformation_83A_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceA_GeneralInformation_83A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceA_GeneralInformation_83A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 177, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceA_GeneralInformation_83A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceA_GeneralInformation_83A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='83A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 180, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 180, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceA_GeneralInformation_83A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 181, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 181, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceA_GeneralInformation_83A_Type = MT320_SequenceA_GeneralInformation_83A_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceA_GeneralInformation_83A_Type', MT320_SequenceA_GeneralInformation_83A_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceA_GeneralInformation_83D_Type with content type SIMPLE
class MT320_SequenceA_GeneralInformation_83D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceA_GeneralInformation_83D_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceA_GeneralInformation_83D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceA_GeneralInformation_83D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 190, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceA_GeneralInformation_83D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceA_GeneralInformation_83D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='83D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 193, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 193, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceA_GeneralInformation_83D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 194, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 194, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceA_GeneralInformation_83D_Type = MT320_SequenceA_GeneralInformation_83D_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceA_GeneralInformation_83D_Type', MT320_SequenceA_GeneralInformation_83D_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceA_GeneralInformation_83J_Type with content type SIMPLE
class MT320_SequenceA_GeneralInformation_83J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceA_GeneralInformation_83J_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceA_GeneralInformation_83J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceA_GeneralInformation_83J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 203, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceA_GeneralInformation_83J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceA_GeneralInformation_83J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='83J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 206, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 206, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceA_GeneralInformation_83J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 207, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 207, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceA_GeneralInformation_83J_Type = MT320_SequenceA_GeneralInformation_83J_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceA_GeneralInformation_83J_Type', MT320_SequenceA_GeneralInformation_83J_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceA_GeneralInformation_77D_Type with content type SIMPLE
class MT320_SequenceA_GeneralInformation_77D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceA_GeneralInformation_77D_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceA_GeneralInformation_77D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceA_GeneralInformation_77D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 216, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceA_GeneralInformation_77D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceA_GeneralInformation_77D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='77D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 219, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 219, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceA_GeneralInformation_77D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 220, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 220, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceA_GeneralInformation_77D_Type = MT320_SequenceA_GeneralInformation_77D_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceA_GeneralInformation_77D_Type', MT320_SequenceA_GeneralInformation_77D_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceB_TransactionDetails_17R_Type with content type SIMPLE
class MT320_SequenceB_TransactionDetails_17R_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceB_TransactionDetails_17R_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceB_TransactionDetails_17R_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceB_TransactionDetails_17R_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 229, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceB_TransactionDetails_17R_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceB_TransactionDetails_17R_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='17R')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 232, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 232, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceB_TransactionDetails_17R_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 233, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 233, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceB_TransactionDetails_17R_Type = MT320_SequenceB_TransactionDetails_17R_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceB_TransactionDetails_17R_Type', MT320_SequenceB_TransactionDetails_17R_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceB_TransactionDetails_30T_Type with content type SIMPLE
class MT320_SequenceB_TransactionDetails_30T_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceB_TransactionDetails_30T_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceB_TransactionDetails_30T_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceB_TransactionDetails_30T_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 242, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceB_TransactionDetails_30T_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceB_TransactionDetails_30T_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='30T')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 245, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 245, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceB_TransactionDetails_30T_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 246, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 246, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceB_TransactionDetails_30T_Type = MT320_SequenceB_TransactionDetails_30T_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceB_TransactionDetails_30T_Type', MT320_SequenceB_TransactionDetails_30T_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceB_TransactionDetails_30V_Type with content type SIMPLE
class MT320_SequenceB_TransactionDetails_30V_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceB_TransactionDetails_30V_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceB_TransactionDetails_30V_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceB_TransactionDetails_30V_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 255, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceB_TransactionDetails_30V_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceB_TransactionDetails_30V_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='30V')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 258, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 258, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceB_TransactionDetails_30V_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 259, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 259, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceB_TransactionDetails_30V_Type = MT320_SequenceB_TransactionDetails_30V_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceB_TransactionDetails_30V_Type', MT320_SequenceB_TransactionDetails_30V_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceB_TransactionDetails_30P_Type with content type SIMPLE
class MT320_SequenceB_TransactionDetails_30P_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceB_TransactionDetails_30P_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceB_TransactionDetails_30P_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceB_TransactionDetails_30P_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 268, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceB_TransactionDetails_30P_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceB_TransactionDetails_30P_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='30P')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 271, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 271, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceB_TransactionDetails_30P_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 272, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 272, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceB_TransactionDetails_30P_Type = MT320_SequenceB_TransactionDetails_30P_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceB_TransactionDetails_30P_Type', MT320_SequenceB_TransactionDetails_30P_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceB_TransactionDetails_32B_Type with content type SIMPLE
class MT320_SequenceB_TransactionDetails_32B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceB_TransactionDetails_32B_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceB_TransactionDetails_32B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceB_TransactionDetails_32B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 281, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceB_TransactionDetails_32B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceB_TransactionDetails_32B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='32B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 284, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 284, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceB_TransactionDetails_32B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 285, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 285, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceB_TransactionDetails_32B_Type = MT320_SequenceB_TransactionDetails_32B_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceB_TransactionDetails_32B_Type', MT320_SequenceB_TransactionDetails_32B_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceB_TransactionDetails_32H_Type with content type SIMPLE
class MT320_SequenceB_TransactionDetails_32H_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceB_TransactionDetails_32H_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceB_TransactionDetails_32H_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceB_TransactionDetails_32H_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 294, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceB_TransactionDetails_32H_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceB_TransactionDetails_32H_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='32H')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 297, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 297, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceB_TransactionDetails_32H_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 298, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 298, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceB_TransactionDetails_32H_Type = MT320_SequenceB_TransactionDetails_32H_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceB_TransactionDetails_32H_Type', MT320_SequenceB_TransactionDetails_32H_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceB_TransactionDetails_30X_Type with content type SIMPLE
class MT320_SequenceB_TransactionDetails_30X_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceB_TransactionDetails_30X_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceB_TransactionDetails_30X_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceB_TransactionDetails_30X_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 307, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceB_TransactionDetails_30X_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceB_TransactionDetails_30X_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='30X')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 310, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 310, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceB_TransactionDetails_30X_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 311, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 311, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceB_TransactionDetails_30X_Type = MT320_SequenceB_TransactionDetails_30X_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceB_TransactionDetails_30X_Type', MT320_SequenceB_TransactionDetails_30X_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceB_TransactionDetails_34E_Type with content type SIMPLE
class MT320_SequenceB_TransactionDetails_34E_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceB_TransactionDetails_34E_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceB_TransactionDetails_34E_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceB_TransactionDetails_34E_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 320, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceB_TransactionDetails_34E_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceB_TransactionDetails_34E_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='34E')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 323, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 323, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceB_TransactionDetails_34E_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 324, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 324, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceB_TransactionDetails_34E_Type = MT320_SequenceB_TransactionDetails_34E_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceB_TransactionDetails_34E_Type', MT320_SequenceB_TransactionDetails_34E_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceB_TransactionDetails_37G_Type with content type SIMPLE
class MT320_SequenceB_TransactionDetails_37G_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceB_TransactionDetails_37G_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceB_TransactionDetails_37G_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceB_TransactionDetails_37G_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 333, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceB_TransactionDetails_37G_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceB_TransactionDetails_37G_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='37G')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 336, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 336, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceB_TransactionDetails_37G_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 337, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 337, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceB_TransactionDetails_37G_Type = MT320_SequenceB_TransactionDetails_37G_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceB_TransactionDetails_37G_Type', MT320_SequenceB_TransactionDetails_37G_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceB_TransactionDetails_14D_Type with content type SIMPLE
class MT320_SequenceB_TransactionDetails_14D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceB_TransactionDetails_14D_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceB_TransactionDetails_14D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceB_TransactionDetails_14D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 346, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceB_TransactionDetails_14D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceB_TransactionDetails_14D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='14D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 349, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 349, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceB_TransactionDetails_14D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 350, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 350, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceB_TransactionDetails_14D_Type = MT320_SequenceB_TransactionDetails_14D_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceB_TransactionDetails_14D_Type', MT320_SequenceB_TransactionDetails_14D_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceB_TransactionDetails_30F_Type with content type SIMPLE
class MT320_SequenceB_TransactionDetails_30F_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceB_TransactionDetails_30F_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceB_TransactionDetails_30F_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceB_TransactionDetails_30F_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 359, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceB_TransactionDetails_30F_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceB_TransactionDetails_30F_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='30F')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 362, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 362, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceB_TransactionDetails_30F_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 363, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 363, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceB_TransactionDetails_30F_Type = MT320_SequenceB_TransactionDetails_30F_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceB_TransactionDetails_30F_Type', MT320_SequenceB_TransactionDetails_30F_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceB_TransactionDetails_38J_Type with content type SIMPLE
class MT320_SequenceB_TransactionDetails_38J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceB_TransactionDetails_38J_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceB_TransactionDetails_38J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceB_TransactionDetails_38J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 372, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceB_TransactionDetails_38J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceB_TransactionDetails_38J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='38J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 375, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 375, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceB_TransactionDetails_38J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 376, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 376, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceB_TransactionDetails_38J_Type = MT320_SequenceB_TransactionDetails_38J_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceB_TransactionDetails_38J_Type', MT320_SequenceB_TransactionDetails_38J_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceB_TransactionDetails_39M_Type with content type SIMPLE
class MT320_SequenceB_TransactionDetails_39M_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceB_TransactionDetails_39M_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceB_TransactionDetails_39M_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceB_TransactionDetails_39M_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 385, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceB_TransactionDetails_39M_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceB_TransactionDetails_39M_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='39M')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 388, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 388, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceB_TransactionDetails_39M_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 389, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 389, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceB_TransactionDetails_39M_Type = MT320_SequenceB_TransactionDetails_39M_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceB_TransactionDetails_39M_Type', MT320_SequenceB_TransactionDetails_39M_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53A_Type with content type SIMPLE
class MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53A_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 398, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='53A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 401, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 401, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 402, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 402, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53A_Type = MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53A_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53A_Type', MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53A_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53D_Type with content type SIMPLE
class MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53D_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 411, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='53D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 414, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 414, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 415, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 415, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53D_Type = MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53D_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53D_Type', MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53D_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53J_Type with content type SIMPLE
class MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53J_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 424, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='53J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 427, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 427, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 428, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 428, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53J_Type = MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53J_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53J_Type', MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53J_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86A_Type with content type SIMPLE
class MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86A_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 437, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='86A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 440, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 440, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 441, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 441, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86A_Type = MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86A_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86A_Type', MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86A_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86D_Type with content type SIMPLE
class MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86D_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 450, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='86D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 453, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 453, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 454, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 454, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86D_Type = MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86D_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86D_Type', MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86D_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86J_Type with content type SIMPLE
class MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86J_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 463, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='86J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 466, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 466, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 467, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 467, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86J_Type = MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86J_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86J_Type', MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86J_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56A_Type with content type SIMPLE
class MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56A_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 476, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='56A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 479, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 479, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 480, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 480, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56A_Type = MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56A_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56A_Type', MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56A_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56D_Type with content type SIMPLE
class MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56D_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 489, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='56D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 492, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 492, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 493, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 493, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56D_Type = MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56D_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56D_Type', MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56D_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56J_Type with content type SIMPLE
class MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56J_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 502, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='56J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 505, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 505, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 506, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 506, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56J_Type = MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56J_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56J_Type', MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56J_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57A_Type with content type SIMPLE
class MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57A_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 515, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='57A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 518, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 518, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 519, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 519, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57A_Type = MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57A_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57A_Type', MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57A_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57D_Type with content type SIMPLE
class MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57D_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 528, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='57D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 531, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 531, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 532, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 532, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57D_Type = MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57D_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57D_Type', MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57D_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57J_Type with content type SIMPLE
class MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57J_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 541, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='57J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 544, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 544, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 545, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 545, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57J_Type = MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57J_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57J_Type', MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57J_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58A_Type with content type SIMPLE
class MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58A_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 554, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='58A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 557, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 557, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 558, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 558, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58A_Type = MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58A_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58A_Type', MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58A_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58D_Type with content type SIMPLE
class MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58D_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 567, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='58D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 570, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 570, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 571, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 571, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58D_Type = MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58D_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58D_Type', MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58D_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58J_Type with content type SIMPLE
class MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58J_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 580, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='58J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 583, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 583, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 584, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 584, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58J_Type = MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58J_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58J_Type', MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58J_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53A_Type with content type SIMPLE
class MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53A_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 593, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='53A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 596, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 596, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 597, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 597, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53A_Type = MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53A_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53A_Type', MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53A_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53D_Type with content type SIMPLE
class MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53D_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 606, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='53D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 609, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 609, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 610, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 610, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53D_Type = MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53D_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53D_Type', MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53D_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53J_Type with content type SIMPLE
class MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53J_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 619, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='53J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 622, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 622, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 623, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 623, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53J_Type = MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53J_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53J_Type', MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53J_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86A_Type with content type SIMPLE
class MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86A_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 632, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='86A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 635, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 635, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 636, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 636, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86A_Type = MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86A_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86A_Type', MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86A_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86D_Type with content type SIMPLE
class MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86D_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 645, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='86D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 648, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 648, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 649, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 649, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86D_Type = MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86D_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86D_Type', MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86D_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86J_Type with content type SIMPLE
class MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86J_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 658, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='86J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 661, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 661, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 662, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 662, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86J_Type = MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86J_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86J_Type', MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86J_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56A_Type with content type SIMPLE
class MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56A_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 671, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='56A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 674, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 674, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 675, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 675, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56A_Type = MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56A_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56A_Type', MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56A_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56D_Type with content type SIMPLE
class MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56D_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 684, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='56D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 687, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 687, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 688, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 688, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56D_Type = MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56D_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56D_Type', MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56D_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56J_Type with content type SIMPLE
class MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56J_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 697, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='56J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 700, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 700, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 701, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 701, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56J_Type = MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56J_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56J_Type', MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56J_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57A_Type with content type SIMPLE
class MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57A_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 710, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='57A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 713, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 713, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 714, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 714, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57A_Type = MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57A_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57A_Type', MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57A_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57D_Type with content type SIMPLE
class MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57D_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 723, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='57D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 726, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 726, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 727, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 727, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57D_Type = MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57D_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57D_Type', MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57D_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57J_Type with content type SIMPLE
class MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57J_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 736, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='57J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 739, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 739, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 740, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 740, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57J_Type = MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57J_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57J_Type', MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57J_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58A_Type with content type SIMPLE
class MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58A_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 749, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='58A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 752, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 752, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 753, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 753, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58A_Type = MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58A_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58A_Type', MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58A_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58D_Type with content type SIMPLE
class MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58D_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 762, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='58D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 765, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 765, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 766, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 766, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58D_Type = MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58D_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58D_Type', MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58D_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58J_Type with content type SIMPLE
class MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58J_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 775, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='58J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 778, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 778, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 779, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 779, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58J_Type = MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58J_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58J_Type', MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58J_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53A_Type with content type SIMPLE
class MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53A_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 788, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='53A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 791, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 791, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 792, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 792, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53A_Type = MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53A_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53A_Type', MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53A_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53D_Type with content type SIMPLE
class MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53D_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 801, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='53D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 804, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 804, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 805, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 805, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53D_Type = MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53D_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53D_Type', MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53D_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53J_Type with content type SIMPLE
class MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53J_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 814, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='53J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 817, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 817, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 818, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 818, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53J_Type = MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53J_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53J_Type', MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53J_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86A_Type with content type SIMPLE
class MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86A_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 827, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='86A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 830, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 830, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 831, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 831, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86A_Type = MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86A_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86A_Type', MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86A_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86D_Type with content type SIMPLE
class MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86D_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 840, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='86D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 843, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 843, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 844, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 844, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86D_Type = MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86D_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86D_Type', MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86D_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86J_Type with content type SIMPLE
class MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86J_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 853, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='86J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 856, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 856, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 857, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 857, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86J_Type = MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86J_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86J_Type', MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86J_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56A_Type with content type SIMPLE
class MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56A_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 866, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='56A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 869, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 869, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 870, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 870, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56A_Type = MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56A_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56A_Type', MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56A_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56D_Type with content type SIMPLE
class MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56D_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 879, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='56D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 882, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 882, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 883, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 883, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56D_Type = MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56D_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56D_Type', MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56D_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56J_Type with content type SIMPLE
class MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56J_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 892, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='56J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 895, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 895, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 896, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 896, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56J_Type = MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56J_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56J_Type', MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56J_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57A_Type with content type SIMPLE
class MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57A_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 905, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='57A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 908, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 908, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 909, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 909, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57A_Type = MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57A_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57A_Type', MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57A_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57D_Type with content type SIMPLE
class MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57D_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 918, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='57D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 921, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 921, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 922, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 922, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57D_Type = MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57D_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57D_Type', MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57D_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57J_Type with content type SIMPLE
class MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57J_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 931, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='57J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 934, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 934, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 935, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 935, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57J_Type = MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57J_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57J_Type', MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57J_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58A_Type with content type SIMPLE
class MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58A_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 944, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='58A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 947, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 947, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 948, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 948, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58A_Type = MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58A_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58A_Type', MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58A_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58D_Type with content type SIMPLE
class MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58D_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 957, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='58D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 960, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 960, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 961, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 961, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58D_Type = MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58D_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58D_Type', MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58D_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58J_Type with content type SIMPLE
class MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58J_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 970, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='58J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 973, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 973, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 974, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 974, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58J_Type = MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58J_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58J_Type', MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58J_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53A_Type with content type SIMPLE
class MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53A_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 983, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='53A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 986, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 986, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 987, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 987, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53A_Type = MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53A_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53A_Type', MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53A_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53D_Type with content type SIMPLE
class MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53D_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 996, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='53D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 999, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 999, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1000, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1000, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53D_Type = MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53D_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53D_Type', MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53D_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53J_Type with content type SIMPLE
class MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53J_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1009, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='53J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1012, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1012, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1013, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1013, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53J_Type = MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53J_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53J_Type', MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53J_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86A_Type with content type SIMPLE
class MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86A_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1022, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='86A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1025, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1025, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1026, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1026, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86A_Type = MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86A_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86A_Type', MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86A_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86D_Type with content type SIMPLE
class MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86D_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1035, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='86D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1038, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1038, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1039, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1039, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86D_Type = MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86D_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86D_Type', MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86D_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86J_Type with content type SIMPLE
class MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86J_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1048, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='86J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1051, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1051, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1052, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1052, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86J_Type = MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86J_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86J_Type', MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86J_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56A_Type with content type SIMPLE
class MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56A_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1061, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='56A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1064, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1064, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1065, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1065, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56A_Type = MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56A_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56A_Type', MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56A_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56D_Type with content type SIMPLE
class MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56D_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1074, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='56D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1077, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1077, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1078, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1078, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56D_Type = MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56D_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56D_Type', MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56D_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56J_Type with content type SIMPLE
class MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56J_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1087, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='56J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1090, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1090, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1091, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1091, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56J_Type = MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56J_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56J_Type', MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56J_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57A_Type with content type SIMPLE
class MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57A_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1100, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='57A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1103, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1103, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1104, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1104, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57A_Type = MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57A_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57A_Type', MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57A_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57D_Type with content type SIMPLE
class MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57D_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1113, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='57D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1116, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1116, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1117, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1117, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57D_Type = MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57D_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57D_Type', MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57D_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57J_Type with content type SIMPLE
class MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57J_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1126, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='57J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1129, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1129, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1130, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1130, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57J_Type = MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57J_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57J_Type', MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57J_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58A_Type with content type SIMPLE
class MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58A_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1139, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='58A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1142, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1142, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1143, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1143, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58A_Type = MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58A_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58A_Type', MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58A_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58D_Type with content type SIMPLE
class MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58D_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1152, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='58D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1155, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1155, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1156, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1156, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58D_Type = MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58D_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58D_Type', MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58D_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58J_Type with content type SIMPLE
class MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58J_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1165, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='58J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1168, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1168, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1169, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1169, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58J_Type = MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58J_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58J_Type', MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58J_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceG_TaxInformation_37L_Type with content type SIMPLE
class MT320_SequenceG_TaxInformation_37L_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceG_TaxInformation_37L_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceG_TaxInformation_37L_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceG_TaxInformation_37L_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1178, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceG_TaxInformation_37L_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceG_TaxInformation_37L_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='37L')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1181, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1181, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceG_TaxInformation_37L_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1182, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1182, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceG_TaxInformation_37L_Type = MT320_SequenceG_TaxInformation_37L_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceG_TaxInformation_37L_Type', MT320_SequenceG_TaxInformation_37L_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceG_TaxInformation_33B_Type with content type SIMPLE
class MT320_SequenceG_TaxInformation_33B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceG_TaxInformation_33B_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceG_TaxInformation_33B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceG_TaxInformation_33B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1191, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceG_TaxInformation_33B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceG_TaxInformation_33B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='33B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1194, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1194, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceG_TaxInformation_33B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1195, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1195, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceG_TaxInformation_33B_Type = MT320_SequenceG_TaxInformation_33B_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceG_TaxInformation_33B_Type', MT320_SequenceG_TaxInformation_33B_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceG_TaxInformation_36_Type with content type SIMPLE
class MT320_SequenceG_TaxInformation_36_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceG_TaxInformation_36_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceG_TaxInformation_36_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceG_TaxInformation_36_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1204, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceG_TaxInformation_36_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceG_TaxInformation_36_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='36')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1207, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1207, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceG_TaxInformation_36_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1208, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1208, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceG_TaxInformation_36_Type = MT320_SequenceG_TaxInformation_36_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceG_TaxInformation_36_Type', MT320_SequenceG_TaxInformation_36_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceG_TaxInformation_33E_Type with content type SIMPLE
class MT320_SequenceG_TaxInformation_33E_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceG_TaxInformation_33E_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceG_TaxInformation_33E_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceG_TaxInformation_33E_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1217, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceG_TaxInformation_33E_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceG_TaxInformation_33E_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='33E')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1220, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1220, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceG_TaxInformation_33E_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1221, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1221, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceG_TaxInformation_33E_Type = MT320_SequenceG_TaxInformation_33E_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceG_TaxInformation_33E_Type', MT320_SequenceG_TaxInformation_33E_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceH_AdditionalInformation_29A_Type with content type SIMPLE
class MT320_SequenceH_AdditionalInformation_29A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceH_AdditionalInformation_29A_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceH_AdditionalInformation_29A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceH_AdditionalInformation_29A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1230, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceH_AdditionalInformation_29A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceH_AdditionalInformation_29A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='29A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1233, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1233, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceH_AdditionalInformation_29A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1234, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1234, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceH_AdditionalInformation_29A_Type = MT320_SequenceH_AdditionalInformation_29A_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceH_AdditionalInformation_29A_Type', MT320_SequenceH_AdditionalInformation_29A_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceH_AdditionalInformation_24D_Type with content type SIMPLE
class MT320_SequenceH_AdditionalInformation_24D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceH_AdditionalInformation_24D_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceH_AdditionalInformation_24D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceH_AdditionalInformation_24D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1243, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceH_AdditionalInformation_24D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceH_AdditionalInformation_24D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='24D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1246, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1246, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceH_AdditionalInformation_24D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1247, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1247, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceH_AdditionalInformation_24D_Type = MT320_SequenceH_AdditionalInformation_24D_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceH_AdditionalInformation_24D_Type', MT320_SequenceH_AdditionalInformation_24D_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceH_AdditionalInformation_84A_Type with content type SIMPLE
class MT320_SequenceH_AdditionalInformation_84A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceH_AdditionalInformation_84A_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceH_AdditionalInformation_84A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceH_AdditionalInformation_84A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1256, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceH_AdditionalInformation_84A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceH_AdditionalInformation_84A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='84A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1259, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1259, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceH_AdditionalInformation_84A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1260, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1260, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceH_AdditionalInformation_84A_Type = MT320_SequenceH_AdditionalInformation_84A_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceH_AdditionalInformation_84A_Type', MT320_SequenceH_AdditionalInformation_84A_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceH_AdditionalInformation_84B_Type with content type SIMPLE
class MT320_SequenceH_AdditionalInformation_84B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceH_AdditionalInformation_84B_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceH_AdditionalInformation_84B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceH_AdditionalInformation_84B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1269, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceH_AdditionalInformation_84B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceH_AdditionalInformation_84B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='84B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1272, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1272, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceH_AdditionalInformation_84B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1273, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1273, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceH_AdditionalInformation_84B_Type = MT320_SequenceH_AdditionalInformation_84B_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceH_AdditionalInformation_84B_Type', MT320_SequenceH_AdditionalInformation_84B_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceH_AdditionalInformation_84D_Type with content type SIMPLE
class MT320_SequenceH_AdditionalInformation_84D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceH_AdditionalInformation_84D_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceH_AdditionalInformation_84D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceH_AdditionalInformation_84D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1282, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceH_AdditionalInformation_84D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceH_AdditionalInformation_84D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='84D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1285, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1285, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceH_AdditionalInformation_84D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1286, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1286, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceH_AdditionalInformation_84D_Type = MT320_SequenceH_AdditionalInformation_84D_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceH_AdditionalInformation_84D_Type', MT320_SequenceH_AdditionalInformation_84D_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceH_AdditionalInformation_84J_Type with content type SIMPLE
class MT320_SequenceH_AdditionalInformation_84J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceH_AdditionalInformation_84J_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceH_AdditionalInformation_84J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceH_AdditionalInformation_84J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1295, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceH_AdditionalInformation_84J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceH_AdditionalInformation_84J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='84J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1298, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1298, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceH_AdditionalInformation_84J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1299, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1299, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceH_AdditionalInformation_84J_Type = MT320_SequenceH_AdditionalInformation_84J_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceH_AdditionalInformation_84J_Type', MT320_SequenceH_AdditionalInformation_84J_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceH_AdditionalInformation_85A_Type with content type SIMPLE
class MT320_SequenceH_AdditionalInformation_85A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceH_AdditionalInformation_85A_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceH_AdditionalInformation_85A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceH_AdditionalInformation_85A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1308, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceH_AdditionalInformation_85A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceH_AdditionalInformation_85A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='85A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1311, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1311, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceH_AdditionalInformation_85A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1312, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1312, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceH_AdditionalInformation_85A_Type = MT320_SequenceH_AdditionalInformation_85A_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceH_AdditionalInformation_85A_Type', MT320_SequenceH_AdditionalInformation_85A_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceH_AdditionalInformation_85B_Type with content type SIMPLE
class MT320_SequenceH_AdditionalInformation_85B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceH_AdditionalInformation_85B_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceH_AdditionalInformation_85B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceH_AdditionalInformation_85B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1321, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceH_AdditionalInformation_85B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceH_AdditionalInformation_85B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='85B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1324, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1324, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceH_AdditionalInformation_85B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1325, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1325, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceH_AdditionalInformation_85B_Type = MT320_SequenceH_AdditionalInformation_85B_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceH_AdditionalInformation_85B_Type', MT320_SequenceH_AdditionalInformation_85B_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceH_AdditionalInformation_85D_Type with content type SIMPLE
class MT320_SequenceH_AdditionalInformation_85D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceH_AdditionalInformation_85D_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceH_AdditionalInformation_85D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceH_AdditionalInformation_85D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1334, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceH_AdditionalInformation_85D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceH_AdditionalInformation_85D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='85D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1337, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1337, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceH_AdditionalInformation_85D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1338, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1338, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceH_AdditionalInformation_85D_Type = MT320_SequenceH_AdditionalInformation_85D_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceH_AdditionalInformation_85D_Type', MT320_SequenceH_AdditionalInformation_85D_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceH_AdditionalInformation_85J_Type with content type SIMPLE
class MT320_SequenceH_AdditionalInformation_85J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceH_AdditionalInformation_85J_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceH_AdditionalInformation_85J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceH_AdditionalInformation_85J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1347, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceH_AdditionalInformation_85J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceH_AdditionalInformation_85J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='85J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1350, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1350, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceH_AdditionalInformation_85J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1351, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1351, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceH_AdditionalInformation_85J_Type = MT320_SequenceH_AdditionalInformation_85J_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceH_AdditionalInformation_85J_Type', MT320_SequenceH_AdditionalInformation_85J_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceH_AdditionalInformation_88A_Type with content type SIMPLE
class MT320_SequenceH_AdditionalInformation_88A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceH_AdditionalInformation_88A_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceH_AdditionalInformation_88A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceH_AdditionalInformation_88A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1360, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceH_AdditionalInformation_88A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceH_AdditionalInformation_88A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='88A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1363, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1363, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceH_AdditionalInformation_88A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1364, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1364, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceH_AdditionalInformation_88A_Type = MT320_SequenceH_AdditionalInformation_88A_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceH_AdditionalInformation_88A_Type', MT320_SequenceH_AdditionalInformation_88A_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceH_AdditionalInformation_88D_Type with content type SIMPLE
class MT320_SequenceH_AdditionalInformation_88D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceH_AdditionalInformation_88D_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceH_AdditionalInformation_88D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceH_AdditionalInformation_88D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1373, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceH_AdditionalInformation_88D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceH_AdditionalInformation_88D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='88D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1376, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1376, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceH_AdditionalInformation_88D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1377, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1377, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceH_AdditionalInformation_88D_Type = MT320_SequenceH_AdditionalInformation_88D_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceH_AdditionalInformation_88D_Type', MT320_SequenceH_AdditionalInformation_88D_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceH_AdditionalInformation_88J_Type with content type SIMPLE
class MT320_SequenceH_AdditionalInformation_88J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceH_AdditionalInformation_88J_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceH_AdditionalInformation_88J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceH_AdditionalInformation_88J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1386, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceH_AdditionalInformation_88J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceH_AdditionalInformation_88J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='88J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1389, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1389, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceH_AdditionalInformation_88J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1390, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1390, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceH_AdditionalInformation_88J_Type = MT320_SequenceH_AdditionalInformation_88J_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceH_AdditionalInformation_88J_Type', MT320_SequenceH_AdditionalInformation_88J_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceH_AdditionalInformation_71F_Type with content type SIMPLE
class MT320_SequenceH_AdditionalInformation_71F_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceH_AdditionalInformation_71F_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceH_AdditionalInformation_71F_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceH_AdditionalInformation_71F_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1399, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceH_AdditionalInformation_71F_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceH_AdditionalInformation_71F_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='71F')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1402, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1402, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceH_AdditionalInformation_71F_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1403, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1403, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceH_AdditionalInformation_71F_Type = MT320_SequenceH_AdditionalInformation_71F_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceH_AdditionalInformation_71F_Type', MT320_SequenceH_AdditionalInformation_71F_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceH_AdditionalInformation_26H_Type with content type SIMPLE
class MT320_SequenceH_AdditionalInformation_26H_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceH_AdditionalInformation_26H_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceH_AdditionalInformation_26H_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceH_AdditionalInformation_26H_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1412, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceH_AdditionalInformation_26H_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceH_AdditionalInformation_26H_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='26H')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1415, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1415, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceH_AdditionalInformation_26H_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1416, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1416, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceH_AdditionalInformation_26H_Type = MT320_SequenceH_AdditionalInformation_26H_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceH_AdditionalInformation_26H_Type', MT320_SequenceH_AdditionalInformation_26H_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceH_AdditionalInformation_21G_Type with content type SIMPLE
class MT320_SequenceH_AdditionalInformation_21G_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceH_AdditionalInformation_21G_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceH_AdditionalInformation_21G_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceH_AdditionalInformation_21G_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1425, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceH_AdditionalInformation_21G_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceH_AdditionalInformation_21G_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='21G')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1428, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1428, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceH_AdditionalInformation_21G_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1429, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1429, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceH_AdditionalInformation_21G_Type = MT320_SequenceH_AdditionalInformation_21G_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceH_AdditionalInformation_21G_Type', MT320_SequenceH_AdditionalInformation_21G_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceH_AdditionalInformation_34C_Type with content type SIMPLE
class MT320_SequenceH_AdditionalInformation_34C_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceH_AdditionalInformation_34C_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceH_AdditionalInformation_34C_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceH_AdditionalInformation_34C_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1438, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceH_AdditionalInformation_34C_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceH_AdditionalInformation_34C_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='34C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1441, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1441, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceH_AdditionalInformation_34C_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1442, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1442, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceH_AdditionalInformation_34C_Type = MT320_SequenceH_AdditionalInformation_34C_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceH_AdditionalInformation_34C_Type', MT320_SequenceH_AdditionalInformation_34C_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceH_AdditionalInformation_72_Type with content type SIMPLE
class MT320_SequenceH_AdditionalInformation_72_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceH_AdditionalInformation_72_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceH_AdditionalInformation_72_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceH_AdditionalInformation_72_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1451, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceH_AdditionalInformation_72_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceH_AdditionalInformation_72_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='72')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1454, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1454, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceH_AdditionalInformation_72_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1455, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1455, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceH_AdditionalInformation_72_Type = MT320_SequenceH_AdditionalInformation_72_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceH_AdditionalInformation_72_Type', MT320_SequenceH_AdditionalInformation_72_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceI_AdditionalAmounts_18A_Type with content type SIMPLE
class MT320_SequenceI_AdditionalAmounts_18A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceI_AdditionalAmounts_18A_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceI_AdditionalAmounts_18A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceI_AdditionalAmounts_18A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1464, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceI_AdditionalAmounts_18A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceI_AdditionalAmounts_18A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='18A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1467, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1467, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceI_AdditionalAmounts_18A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1468, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1468, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceI_AdditionalAmounts_18A_Type = MT320_SequenceI_AdditionalAmounts_18A_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceI_AdditionalAmounts_18A_Type', MT320_SequenceI_AdditionalAmounts_18A_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceI_AdditionalAmounts_AMOUNT_30F_Type with content type SIMPLE
class MT320_SequenceI_AdditionalAmounts_AMOUNT_30F_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceI_AdditionalAmounts_AMOUNT_30F_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceI_AdditionalAmounts_AMOUNT_30F_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceI_AdditionalAmounts_AMOUNT_30F_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1477, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceI_AdditionalAmounts_AMOUNT_30F_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceI_AdditionalAmounts_AMOUNT_30F_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='30F')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1480, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1480, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceI_AdditionalAmounts_AMOUNT_30F_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1481, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1481, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceI_AdditionalAmounts_AMOUNT_30F_Type = MT320_SequenceI_AdditionalAmounts_AMOUNT_30F_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceI_AdditionalAmounts_AMOUNT_30F_Type', MT320_SequenceI_AdditionalAmounts_AMOUNT_30F_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceI_AdditionalAmounts_AMOUNT_32H_Type with content type SIMPLE
class MT320_SequenceI_AdditionalAmounts_AMOUNT_32H_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceI_AdditionalAmounts_AMOUNT_32H_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceI_AdditionalAmounts_AMOUNT_32H_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceI_AdditionalAmounts_AMOUNT_32H_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1490, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceI_AdditionalAmounts_AMOUNT_32H_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceI_AdditionalAmounts_AMOUNT_32H_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='32H')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1493, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1493, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceI_AdditionalAmounts_AMOUNT_32H_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1494, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1494, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceI_AdditionalAmounts_AMOUNT_32H_Type = MT320_SequenceI_AdditionalAmounts_AMOUNT_32H_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceI_AdditionalAmounts_AMOUNT_32H_Type', MT320_SequenceI_AdditionalAmounts_AMOUNT_32H_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceI_AdditionalAmounts_53A_Type with content type SIMPLE
class MT320_SequenceI_AdditionalAmounts_53A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceI_AdditionalAmounts_53A_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceI_AdditionalAmounts_53A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceI_AdditionalAmounts_53A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1503, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceI_AdditionalAmounts_53A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceI_AdditionalAmounts_53A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='53A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1506, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1506, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceI_AdditionalAmounts_53A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1507, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1507, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceI_AdditionalAmounts_53A_Type = MT320_SequenceI_AdditionalAmounts_53A_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceI_AdditionalAmounts_53A_Type', MT320_SequenceI_AdditionalAmounts_53A_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceI_AdditionalAmounts_53D_Type with content type SIMPLE
class MT320_SequenceI_AdditionalAmounts_53D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceI_AdditionalAmounts_53D_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceI_AdditionalAmounts_53D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceI_AdditionalAmounts_53D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1516, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceI_AdditionalAmounts_53D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceI_AdditionalAmounts_53D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='53D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1519, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1519, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceI_AdditionalAmounts_53D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1520, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1520, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceI_AdditionalAmounts_53D_Type = MT320_SequenceI_AdditionalAmounts_53D_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceI_AdditionalAmounts_53D_Type', MT320_SequenceI_AdditionalAmounts_53D_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceI_AdditionalAmounts_53J_Type with content type SIMPLE
class MT320_SequenceI_AdditionalAmounts_53J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceI_AdditionalAmounts_53J_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceI_AdditionalAmounts_53J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceI_AdditionalAmounts_53J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1529, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceI_AdditionalAmounts_53J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceI_AdditionalAmounts_53J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='53J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1532, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1532, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceI_AdditionalAmounts_53J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1533, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1533, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceI_AdditionalAmounts_53J_Type = MT320_SequenceI_AdditionalAmounts_53J_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceI_AdditionalAmounts_53J_Type', MT320_SequenceI_AdditionalAmounts_53J_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceI_AdditionalAmounts_86A_Type with content type SIMPLE
class MT320_SequenceI_AdditionalAmounts_86A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceI_AdditionalAmounts_86A_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceI_AdditionalAmounts_86A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceI_AdditionalAmounts_86A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1542, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceI_AdditionalAmounts_86A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceI_AdditionalAmounts_86A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='86A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1545, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1545, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceI_AdditionalAmounts_86A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1546, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1546, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceI_AdditionalAmounts_86A_Type = MT320_SequenceI_AdditionalAmounts_86A_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceI_AdditionalAmounts_86A_Type', MT320_SequenceI_AdditionalAmounts_86A_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceI_AdditionalAmounts_86D_Type with content type SIMPLE
class MT320_SequenceI_AdditionalAmounts_86D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceI_AdditionalAmounts_86D_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceI_AdditionalAmounts_86D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceI_AdditionalAmounts_86D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1555, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceI_AdditionalAmounts_86D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceI_AdditionalAmounts_86D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='86D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1558, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1558, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceI_AdditionalAmounts_86D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1559, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1559, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceI_AdditionalAmounts_86D_Type = MT320_SequenceI_AdditionalAmounts_86D_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceI_AdditionalAmounts_86D_Type', MT320_SequenceI_AdditionalAmounts_86D_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceI_AdditionalAmounts_86J_Type with content type SIMPLE
class MT320_SequenceI_AdditionalAmounts_86J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceI_AdditionalAmounts_86J_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceI_AdditionalAmounts_86J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceI_AdditionalAmounts_86J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1568, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceI_AdditionalAmounts_86J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceI_AdditionalAmounts_86J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='86J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1571, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1571, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceI_AdditionalAmounts_86J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1572, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1572, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceI_AdditionalAmounts_86J_Type = MT320_SequenceI_AdditionalAmounts_86J_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceI_AdditionalAmounts_86J_Type', MT320_SequenceI_AdditionalAmounts_86J_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceI_AdditionalAmounts_56A_Type with content type SIMPLE
class MT320_SequenceI_AdditionalAmounts_56A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceI_AdditionalAmounts_56A_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceI_AdditionalAmounts_56A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceI_AdditionalAmounts_56A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1581, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceI_AdditionalAmounts_56A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceI_AdditionalAmounts_56A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='56A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1584, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1584, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceI_AdditionalAmounts_56A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1585, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1585, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceI_AdditionalAmounts_56A_Type = MT320_SequenceI_AdditionalAmounts_56A_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceI_AdditionalAmounts_56A_Type', MT320_SequenceI_AdditionalAmounts_56A_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceI_AdditionalAmounts_56D_Type with content type SIMPLE
class MT320_SequenceI_AdditionalAmounts_56D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceI_AdditionalAmounts_56D_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceI_AdditionalAmounts_56D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceI_AdditionalAmounts_56D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1594, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceI_AdditionalAmounts_56D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceI_AdditionalAmounts_56D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='56D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1597, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1597, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceI_AdditionalAmounts_56D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1598, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1598, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceI_AdditionalAmounts_56D_Type = MT320_SequenceI_AdditionalAmounts_56D_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceI_AdditionalAmounts_56D_Type', MT320_SequenceI_AdditionalAmounts_56D_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceI_AdditionalAmounts_56J_Type with content type SIMPLE
class MT320_SequenceI_AdditionalAmounts_56J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceI_AdditionalAmounts_56J_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceI_AdditionalAmounts_56J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceI_AdditionalAmounts_56J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1607, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceI_AdditionalAmounts_56J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceI_AdditionalAmounts_56J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='56J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1610, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1610, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceI_AdditionalAmounts_56J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1611, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1611, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceI_AdditionalAmounts_56J_Type = MT320_SequenceI_AdditionalAmounts_56J_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceI_AdditionalAmounts_56J_Type', MT320_SequenceI_AdditionalAmounts_56J_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceI_AdditionalAmounts_57A_Type with content type SIMPLE
class MT320_SequenceI_AdditionalAmounts_57A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceI_AdditionalAmounts_57A_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceI_AdditionalAmounts_57A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceI_AdditionalAmounts_57A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1620, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceI_AdditionalAmounts_57A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceI_AdditionalAmounts_57A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='57A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1623, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1623, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceI_AdditionalAmounts_57A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1624, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1624, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceI_AdditionalAmounts_57A_Type = MT320_SequenceI_AdditionalAmounts_57A_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceI_AdditionalAmounts_57A_Type', MT320_SequenceI_AdditionalAmounts_57A_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceI_AdditionalAmounts_57D_Type with content type SIMPLE
class MT320_SequenceI_AdditionalAmounts_57D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceI_AdditionalAmounts_57D_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceI_AdditionalAmounts_57D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceI_AdditionalAmounts_57D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1633, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceI_AdditionalAmounts_57D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceI_AdditionalAmounts_57D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='57D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1636, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1636, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceI_AdditionalAmounts_57D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1637, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1637, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceI_AdditionalAmounts_57D_Type = MT320_SequenceI_AdditionalAmounts_57D_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceI_AdditionalAmounts_57D_Type', MT320_SequenceI_AdditionalAmounts_57D_Type)


# Complex type {http://www.w3schools.com}MT320_SequenceI_AdditionalAmounts_57J_Type with content type SIMPLE
class MT320_SequenceI_AdditionalAmounts_57J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT320_SequenceI_AdditionalAmounts_57J_Type with content type SIMPLE"""
    _TypeDefinition = MT320_SequenceI_AdditionalAmounts_57J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT320_SequenceI_AdditionalAmounts_57J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1646, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT320_SequenceI_AdditionalAmounts_57J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT320_SequenceI_AdditionalAmounts_57J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='57J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1649, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1649, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT320_SequenceI_AdditionalAmounts_57J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1650, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1650, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT320_SequenceI_AdditionalAmounts_57J_Type = MT320_SequenceI_AdditionalAmounts_57J_Type
Namespace.addCategoryObject('typeBinding', 'MT320_SequenceI_AdditionalAmounts_57J_Type', MT320_SequenceI_AdditionalAmounts_57J_Type)


MT320 = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'MT320'), CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1909, 1))
Namespace.addCategoryObject('elementBinding', MT320.name().localName(), MT320)



MT320_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SendersReference'), MT320_SequenceA_GeneralInformation_20_Type, scope=MT320_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1656, 3)))

MT320_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'RelatedReference'), MT320_SequenceA_GeneralInformation_21_Type, scope=MT320_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1657, 3)))

MT320_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TypeOfOperation'), MT320_SequenceA_GeneralInformation_22A_Type, scope=MT320_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1658, 3)))

MT320_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ScopeOfOperation'), MT320_SequenceA_GeneralInformation_94A_Type, scope=MT320_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1659, 3)))

MT320_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TypeOfEvent'), MT320_SequenceA_GeneralInformation_22B_Type, scope=MT320_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1660, 3)))

MT320_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CommonReference'), MT320_SequenceA_GeneralInformation_22C_Type, scope=MT320_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1661, 3)))

MT320_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ContractNumberPartyA'), MT320_SequenceA_GeneralInformation_21N_Type, scope=MT320_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1662, 3)))

MT320_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PartyA_A'), MT320_SequenceA_GeneralInformation_82A_Type, scope=MT320_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1664, 4)))

MT320_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PartyA_D'), MT320_SequenceA_GeneralInformation_82D_Type, scope=MT320_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1665, 4)))

MT320_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PartyA_J'), MT320_SequenceA_GeneralInformation_82J_Type, scope=MT320_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1666, 4)))

MT320_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PartyB_A'), MT320_SequenceA_GeneralInformation_87A_Type, scope=MT320_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1669, 4)))

MT320_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PartyB_D'), MT320_SequenceA_GeneralInformation_87D_Type, scope=MT320_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1670, 4)))

MT320_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PartyB_J'), MT320_SequenceA_GeneralInformation_87J_Type, scope=MT320_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1671, 4)))

MT320_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'FundOrInstructingParty_A'), MT320_SequenceA_GeneralInformation_83A_Type, scope=MT320_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1674, 4)))

MT320_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'FundOrInstructingParty_D'), MT320_SequenceA_GeneralInformation_83D_Type, scope=MT320_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1675, 4)))

MT320_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'FundOrInstructingParty_J'), MT320_SequenceA_GeneralInformation_83J_Type, scope=MT320_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1676, 4)))

MT320_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TermsAndConditions'), MT320_SequenceA_GeneralInformation_77D_Type, scope=MT320_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1678, 3)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1657, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1659, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1662, 3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1673, 3))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1674, 4))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1675, 4))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1676, 4))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1678, 3))
    counters.add(cc_7)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SendersReference')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1656, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'RelatedReference')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1657, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'TypeOfOperation')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1658, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ScopeOfOperation')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1659, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'TypeOfEvent')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1660, 3))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CommonReference')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1661, 3))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ContractNumberPartyA')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1662, 3))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PartyA_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1664, 4))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PartyA_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1665, 4))
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PartyA_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1666, 4))
    st_9 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PartyB_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1669, 4))
    st_10 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PartyB_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1670, 4))
    st_11 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PartyB_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1671, 4))
    st_12 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_12)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'FundOrInstructingParty_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1674, 4))
    st_13 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_13)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'FundOrInstructingParty_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1675, 4))
    st_14 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_14)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    final_update.add(fac.UpdateInstruction(cc_6, False))
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'FundOrInstructingParty_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1676, 4))
    st_15 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_15)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_7, False))
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'TermsAndConditions')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1678, 3))
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
MT320_SequenceA_GeneralInformation._Automaton = _BuildAutomaton()




MT320_SequenceB_TransactionDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PartyAsRole'), MT320_SequenceB_TransactionDetails_17R_Type, scope=MT320_SequenceB_TransactionDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1686, 3)))

MT320_SequenceB_TransactionDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TradeDate'), MT320_SequenceB_TransactionDetails_30T_Type, scope=MT320_SequenceB_TransactionDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1687, 3)))

MT320_SequenceB_TransactionDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ValueDate'), MT320_SequenceB_TransactionDetails_30V_Type, scope=MT320_SequenceB_TransactionDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1688, 3)))

MT320_SequenceB_TransactionDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'MaturityDate'), MT320_SequenceB_TransactionDetails_30P_Type, scope=MT320_SequenceB_TransactionDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1689, 3)))

MT320_SequenceB_TransactionDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CurrencyAndPrincipalAmount'), MT320_SequenceB_TransactionDetails_32B_Type, scope=MT320_SequenceB_TransactionDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1690, 3)))

MT320_SequenceB_TransactionDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'AmountToBeSettled'), MT320_SequenceB_TransactionDetails_32H_Type, scope=MT320_SequenceB_TransactionDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1691, 3)))

MT320_SequenceB_TransactionDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'NextInterestDueDate'), MT320_SequenceB_TransactionDetails_30X_Type, scope=MT320_SequenceB_TransactionDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1692, 3)))

MT320_SequenceB_TransactionDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CurrencyAndInterestAmount'), MT320_SequenceB_TransactionDetails_34E_Type, scope=MT320_SequenceB_TransactionDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1693, 3)))

MT320_SequenceB_TransactionDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'InterestRate'), MT320_SequenceB_TransactionDetails_37G_Type, scope=MT320_SequenceB_TransactionDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1694, 3)))

MT320_SequenceB_TransactionDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DayCountFraction'), MT320_SequenceB_TransactionDetails_14D_Type, scope=MT320_SequenceB_TransactionDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1695, 3)))

MT320_SequenceB_TransactionDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'LastDayOfTheFirstInterestPeriod'), MT320_SequenceB_TransactionDetails_30F_Type, scope=MT320_SequenceB_TransactionDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1696, 3)))

MT320_SequenceB_TransactionDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'NumberOfDays'), MT320_SequenceB_TransactionDetails_38J_Type, scope=MT320_SequenceB_TransactionDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1697, 3)))

MT320_SequenceB_TransactionDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PaymentClearingCentre'), MT320_SequenceB_TransactionDetails_39M_Type, scope=MT320_SequenceB_TransactionDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1698, 3)))

def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1691, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1692, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1696, 3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1697, 3))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1698, 3))
    counters.add(cc_4)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceB_TransactionDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PartyAsRole')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1686, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceB_TransactionDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'TradeDate')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1687, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceB_TransactionDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ValueDate')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1688, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceB_TransactionDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'MaturityDate')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1689, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceB_TransactionDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CurrencyAndPrincipalAmount')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1690, 3))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceB_TransactionDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'AmountToBeSettled')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1691, 3))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceB_TransactionDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'NextInterestDueDate')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1692, 3))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceB_TransactionDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CurrencyAndInterestAmount')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1693, 3))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceB_TransactionDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'InterestRate')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1694, 3))
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceB_TransactionDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DayCountFraction')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1695, 3))
    st_9 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceB_TransactionDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'LastDayOfTheFirstInterestPeriod')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1696, 3))
    st_10 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceB_TransactionDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'NumberOfDays')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1697, 3))
    st_11 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceB_TransactionDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PaymentClearingCentre')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1698, 3))
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
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
         ]))
    transitions.append(fac.Transition(st_6, [
         ]))
    transitions.append(fac.Transition(st_7, [
         ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
         ]))
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
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_10._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_11._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_4, True) ]))
    st_12._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
MT320_SequenceB_TransactionDetails._Automaton = _BuildAutomaton_()




MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_A'), MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53A_Type, scope=MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1707, 4)))

MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_D'), MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53D_Type, scope=MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1708, 4)))

MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_J'), MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53J_Type, scope=MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1709, 4)))

MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Intermediary2_A'), MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86A_Type, scope=MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1712, 4)))

MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Intermediary2_D'), MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86D_Type, scope=MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1713, 4)))

MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Intermediary2_J'), MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_86J_Type, scope=MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1714, 4)))

MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_A'), MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56A_Type, scope=MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1717, 4)))

MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_D'), MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56D_Type, scope=MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1718, 4)))

MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_J'), MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56J_Type, scope=MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1719, 4)))

MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_A'), MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57A_Type, scope=MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1722, 4)))

MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_D'), MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57D_Type, scope=MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1723, 4)))

MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_J'), MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57J_Type, scope=MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1724, 4)))

MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_A'), MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58A_Type, scope=MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1727, 4)))

MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_D'), MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58D_Type, scope=MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1728, 4)))

MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_J'), MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_58J_Type, scope=MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1729, 4)))

def _BuildAutomaton_2 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_2
    del _BuildAutomaton_2
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1706, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1707, 4))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1708, 4))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1709, 4))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1711, 3))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1712, 4))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1713, 4))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1714, 4))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1716, 3))
    counters.add(cc_8)
    cc_9 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1717, 4))
    counters.add(cc_9)
    cc_10 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1718, 4))
    counters.add(cc_10)
    cc_11 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1719, 4))
    counters.add(cc_11)
    cc_12 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1726, 3))
    counters.add(cc_12)
    cc_13 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1727, 4))
    counters.add(cc_13)
    cc_14 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1728, 4))
    counters.add(cc_14)
    cc_15 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1729, 4))
    counters.add(cc_15)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1707, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1708, 4))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1709, 4))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Intermediary2_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1712, 4))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Intermediary2_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1713, 4))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Intermediary2_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1714, 4))
    st_5 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1717, 4))
    st_6 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1718, 4))
    st_7 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1719, 4))
    st_8 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1722, 4))
    st_9 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1723, 4))
    st_10 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1724, 4))
    st_11 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_12, False))
    final_update.add(fac.UpdateInstruction(cc_13, False))
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1727, 4))
    st_12 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_12)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_12, False))
    final_update.add(fac.UpdateInstruction(cc_14, False))
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1728, 4))
    st_13 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_13)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_12, False))
    final_update.add(fac.UpdateInstruction(cc_15, False))
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1729, 4))
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
MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA._Automaton = _BuildAutomaton_2()




MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_A'), MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53A_Type, scope=MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1739, 4)))

MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_D'), MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53D_Type, scope=MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1740, 4)))

MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_J'), MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_53J_Type, scope=MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1741, 4)))

MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Intermediary2_A'), MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86A_Type, scope=MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1744, 4)))

MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Intermediary2_D'), MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86D_Type, scope=MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1745, 4)))

MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Intermediary2_J'), MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_86J_Type, scope=MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1746, 4)))

MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_A'), MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56A_Type, scope=MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1749, 4)))

MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_D'), MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56D_Type, scope=MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1750, 4)))

MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_J'), MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56J_Type, scope=MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1751, 4)))

MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_A'), MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57A_Type, scope=MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1754, 4)))

MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_D'), MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57D_Type, scope=MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1755, 4)))

MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_J'), MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57J_Type, scope=MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1756, 4)))

MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_A'), MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58A_Type, scope=MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1759, 4)))

MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_D'), MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58D_Type, scope=MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1760, 4)))

MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_J'), MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_58J_Type, scope=MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1761, 4)))

def _BuildAutomaton_3 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_3
    del _BuildAutomaton_3
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1738, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1739, 4))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1740, 4))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1741, 4))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1743, 3))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1744, 4))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1745, 4))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1746, 4))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1748, 3))
    counters.add(cc_8)
    cc_9 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1749, 4))
    counters.add(cc_9)
    cc_10 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1750, 4))
    counters.add(cc_10)
    cc_11 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1751, 4))
    counters.add(cc_11)
    cc_12 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1758, 3))
    counters.add(cc_12)
    cc_13 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1759, 4))
    counters.add(cc_13)
    cc_14 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1760, 4))
    counters.add(cc_14)
    cc_15 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1761, 4))
    counters.add(cc_15)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1739, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1740, 4))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1741, 4))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Intermediary2_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1744, 4))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Intermediary2_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1745, 4))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Intermediary2_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1746, 4))
    st_5 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1749, 4))
    st_6 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1750, 4))
    st_7 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1751, 4))
    st_8 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1754, 4))
    st_9 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1755, 4))
    st_10 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1756, 4))
    st_11 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_12, False))
    final_update.add(fac.UpdateInstruction(cc_13, False))
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1759, 4))
    st_12 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_12)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_12, False))
    final_update.add(fac.UpdateInstruction(cc_14, False))
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1760, 4))
    st_13 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_13)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_12, False))
    final_update.add(fac.UpdateInstruction(cc_15, False))
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1761, 4))
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
MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB._Automaton = _BuildAutomaton_3()




MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_A'), MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53A_Type, scope=MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1771, 4)))

MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_D'), MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53D_Type, scope=MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1772, 4)))

MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_J'), MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_53J_Type, scope=MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1773, 4)))

MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Intermediary2_A'), MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86A_Type, scope=MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1776, 4)))

MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Intermediary2_D'), MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86D_Type, scope=MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1777, 4)))

MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Intermediary2_J'), MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_86J_Type, scope=MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1778, 4)))

MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_A'), MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56A_Type, scope=MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1781, 4)))

MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_D'), MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56D_Type, scope=MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1782, 4)))

MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_J'), MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_56J_Type, scope=MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1783, 4)))

MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_A'), MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57A_Type, scope=MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1786, 4)))

MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_D'), MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57D_Type, scope=MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1787, 4)))

MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_J'), MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_57J_Type, scope=MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1788, 4)))

MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_A'), MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58A_Type, scope=MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1791, 4)))

MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_D'), MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58D_Type, scope=MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1792, 4)))

MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_J'), MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA_58J_Type, scope=MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1793, 4)))

def _BuildAutomaton_4 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_4
    del _BuildAutomaton_4
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1770, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1771, 4))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1772, 4))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1773, 4))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1775, 3))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1776, 4))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1777, 4))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1778, 4))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1780, 3))
    counters.add(cc_8)
    cc_9 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1781, 4))
    counters.add(cc_9)
    cc_10 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1782, 4))
    counters.add(cc_10)
    cc_11 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1783, 4))
    counters.add(cc_11)
    cc_12 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1790, 3))
    counters.add(cc_12)
    cc_13 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1791, 4))
    counters.add(cc_13)
    cc_14 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1792, 4))
    counters.add(cc_14)
    cc_15 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1793, 4))
    counters.add(cc_15)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1771, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1772, 4))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1773, 4))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Intermediary2_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1776, 4))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Intermediary2_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1777, 4))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Intermediary2_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1778, 4))
    st_5 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1781, 4))
    st_6 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1782, 4))
    st_7 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1783, 4))
    st_8 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1786, 4))
    st_9 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1787, 4))
    st_10 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1788, 4))
    st_11 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_12, False))
    final_update.add(fac.UpdateInstruction(cc_13, False))
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1791, 4))
    st_12 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_12)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_12, False))
    final_update.add(fac.UpdateInstruction(cc_14, False))
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1792, 4))
    st_13 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_13)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_12, False))
    final_update.add(fac.UpdateInstruction(cc_15, False))
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1793, 4))
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
MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA._Automaton = _BuildAutomaton_4()




MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_A'), MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53A_Type, scope=MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1803, 4)))

MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_D'), MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53D_Type, scope=MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1804, 4)))

MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_J'), MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_53J_Type, scope=MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1805, 4)))

MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Intermediary2_A'), MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86A_Type, scope=MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1808, 4)))

MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Intermediary2_D'), MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86D_Type, scope=MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1809, 4)))

MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Intermediary2_J'), MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_86J_Type, scope=MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1810, 4)))

MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_A'), MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56A_Type, scope=MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1813, 4)))

MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_D'), MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56D_Type, scope=MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1814, 4)))

MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_J'), MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_56J_Type, scope=MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1815, 4)))

MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_A'), MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57A_Type, scope=MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1818, 4)))

MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_D'), MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57D_Type, scope=MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1819, 4)))

MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_J'), MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_57J_Type, scope=MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1820, 4)))

MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_A'), MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58A_Type, scope=MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1823, 4)))

MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_D'), MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58D_Type, scope=MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1824, 4)))

MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_J'), MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB_58J_Type, scope=MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1825, 4)))

def _BuildAutomaton_5 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_5
    del _BuildAutomaton_5
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1802, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1803, 4))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1804, 4))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1805, 4))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1807, 3))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1808, 4))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1809, 4))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1810, 4))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1812, 3))
    counters.add(cc_8)
    cc_9 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1813, 4))
    counters.add(cc_9)
    cc_10 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1814, 4))
    counters.add(cc_10)
    cc_11 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1815, 4))
    counters.add(cc_11)
    cc_12 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1822, 3))
    counters.add(cc_12)
    cc_13 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1823, 4))
    counters.add(cc_13)
    cc_14 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1824, 4))
    counters.add(cc_14)
    cc_15 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1825, 4))
    counters.add(cc_15)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1803, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1804, 4))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1805, 4))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Intermediary2_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1808, 4))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Intermediary2_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1809, 4))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Intermediary2_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1810, 4))
    st_5 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1813, 4))
    st_6 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1814, 4))
    st_7 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1815, 4))
    st_8 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1818, 4))
    st_9 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1819, 4))
    st_10 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1820, 4))
    st_11 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_12, False))
    final_update.add(fac.UpdateInstruction(cc_13, False))
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1823, 4))
    st_12 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_12)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_12, False))
    final_update.add(fac.UpdateInstruction(cc_14, False))
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1824, 4))
    st_13 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_13)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_12, False))
    final_update.add(fac.UpdateInstruction(cc_15, False))
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1825, 4))
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
MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB._Automaton = _BuildAutomaton_5()




MT320_SequenceG_TaxInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TaxRate'), MT320_SequenceG_TaxInformation_37L_Type, scope=MT320_SequenceG_TaxInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1834, 3)))

MT320_SequenceG_TaxInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TransactionCurrencyAndNetInterestAmount'), MT320_SequenceG_TaxInformation_33B_Type, scope=MT320_SequenceG_TaxInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1835, 3)))

MT320_SequenceG_TaxInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ExchangeRate'), MT320_SequenceG_TaxInformation_36_Type, scope=MT320_SequenceG_TaxInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1836, 3)))

MT320_SequenceG_TaxInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ReportingCurrencyAndTaxAmount'), MT320_SequenceG_TaxInformation_33E_Type, scope=MT320_SequenceG_TaxInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1837, 3)))

def _BuildAutomaton_6 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_6
    del _BuildAutomaton_6
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1836, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1837, 3))
    counters.add(cc_1)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceG_TaxInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'TaxRate')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1834, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceG_TaxInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'TransactionCurrencyAndNetInterestAmount')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1835, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceG_TaxInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ExchangeRate')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1836, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceG_TaxInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ReportingCurrencyAndTaxAmount')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1837, 3))
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
MT320_SequenceG_TaxInformation._Automaton = _BuildAutomaton_6()




MT320_SequenceH_AdditionalInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ContactInformation'), MT320_SequenceH_AdditionalInformation_29A_Type, scope=MT320_SequenceH_AdditionalInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1845, 3)))

MT320_SequenceH_AdditionalInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DealingMethod'), MT320_SequenceH_AdditionalInformation_24D_Type, scope=MT320_SequenceH_AdditionalInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1846, 3)))

MT320_SequenceH_AdditionalInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DealingBranchPartyA_A'), MT320_SequenceH_AdditionalInformation_84A_Type, scope=MT320_SequenceH_AdditionalInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1848, 4)))

MT320_SequenceH_AdditionalInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DealingBranchPartyA_B'), MT320_SequenceH_AdditionalInformation_84B_Type, scope=MT320_SequenceH_AdditionalInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1849, 4)))

MT320_SequenceH_AdditionalInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DealingBranchPartyA_D'), MT320_SequenceH_AdditionalInformation_84D_Type, scope=MT320_SequenceH_AdditionalInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1850, 4)))

MT320_SequenceH_AdditionalInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DealingBranchPartyA_J'), MT320_SequenceH_AdditionalInformation_84J_Type, scope=MT320_SequenceH_AdditionalInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1851, 4)))

MT320_SequenceH_AdditionalInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DealingBranchPartyB_A'), MT320_SequenceH_AdditionalInformation_85A_Type, scope=MT320_SequenceH_AdditionalInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1854, 4)))

MT320_SequenceH_AdditionalInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DealingBranchPartyB_B'), MT320_SequenceH_AdditionalInformation_85B_Type, scope=MT320_SequenceH_AdditionalInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1855, 4)))

MT320_SequenceH_AdditionalInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DealingBranchPartyB_D'), MT320_SequenceH_AdditionalInformation_85D_Type, scope=MT320_SequenceH_AdditionalInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1856, 4)))

MT320_SequenceH_AdditionalInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DealingBranchPartyB_J'), MT320_SequenceH_AdditionalInformation_85J_Type, scope=MT320_SequenceH_AdditionalInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1857, 4)))

MT320_SequenceH_AdditionalInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'BrokerIdentification_A'), MT320_SequenceH_AdditionalInformation_88A_Type, scope=MT320_SequenceH_AdditionalInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1860, 4)))

MT320_SequenceH_AdditionalInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'BrokerIdentification_D'), MT320_SequenceH_AdditionalInformation_88D_Type, scope=MT320_SequenceH_AdditionalInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1861, 4)))

MT320_SequenceH_AdditionalInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'BrokerIdentification_J'), MT320_SequenceH_AdditionalInformation_88J_Type, scope=MT320_SequenceH_AdditionalInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1862, 4)))

MT320_SequenceH_AdditionalInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'BrokersCommission'), MT320_SequenceH_AdditionalInformation_71F_Type, scope=MT320_SequenceH_AdditionalInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1864, 3)))

MT320_SequenceH_AdditionalInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CounterpartysReference'), MT320_SequenceH_AdditionalInformation_26H_Type, scope=MT320_SequenceH_AdditionalInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1865, 3)))

MT320_SequenceH_AdditionalInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'BrokersReference'), MT320_SequenceH_AdditionalInformation_21G_Type, scope=MT320_SequenceH_AdditionalInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1866, 3)))

MT320_SequenceH_AdditionalInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CommissionAndFees'), MT320_SequenceH_AdditionalInformation_34C_Type, scope=MT320_SequenceH_AdditionalInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1867, 3)))

MT320_SequenceH_AdditionalInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SenderToReceiverInformation'), MT320_SequenceH_AdditionalInformation_72_Type, scope=MT320_SequenceH_AdditionalInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1868, 3)))

def _BuildAutomaton_7 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_7
    del _BuildAutomaton_7
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1845, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1846, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1847, 3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1848, 4))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1849, 4))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1850, 4))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1851, 4))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1853, 3))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1854, 4))
    counters.add(cc_8)
    cc_9 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1855, 4))
    counters.add(cc_9)
    cc_10 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1856, 4))
    counters.add(cc_10)
    cc_11 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1857, 4))
    counters.add(cc_11)
    cc_12 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1859, 3))
    counters.add(cc_12)
    cc_13 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1860, 4))
    counters.add(cc_13)
    cc_14 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1861, 4))
    counters.add(cc_14)
    cc_15 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1862, 4))
    counters.add(cc_15)
    cc_16 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1864, 3))
    counters.add(cc_16)
    cc_17 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1865, 3))
    counters.add(cc_17)
    cc_18 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1866, 3))
    counters.add(cc_18)
    cc_19 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1867, 3))
    counters.add(cc_19)
    cc_20 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1868, 3))
    counters.add(cc_20)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceH_AdditionalInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ContactInformation')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1845, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceH_AdditionalInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DealingMethod')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1846, 3))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceH_AdditionalInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DealingBranchPartyA_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1848, 4))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceH_AdditionalInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DealingBranchPartyA_B')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1849, 4))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceH_AdditionalInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DealingBranchPartyA_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1850, 4))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    final_update.add(fac.UpdateInstruction(cc_6, False))
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceH_AdditionalInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DealingBranchPartyA_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1851, 4))
    st_5 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_7, False))
    final_update.add(fac.UpdateInstruction(cc_8, False))
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceH_AdditionalInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DealingBranchPartyB_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1854, 4))
    st_6 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_7, False))
    final_update.add(fac.UpdateInstruction(cc_9, False))
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceH_AdditionalInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DealingBranchPartyB_B')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1855, 4))
    st_7 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_7, False))
    final_update.add(fac.UpdateInstruction(cc_10, False))
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceH_AdditionalInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DealingBranchPartyB_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1856, 4))
    st_8 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_7, False))
    final_update.add(fac.UpdateInstruction(cc_11, False))
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceH_AdditionalInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DealingBranchPartyB_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1857, 4))
    st_9 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_12, False))
    final_update.add(fac.UpdateInstruction(cc_13, False))
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceH_AdditionalInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'BrokerIdentification_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1860, 4))
    st_10 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_12, False))
    final_update.add(fac.UpdateInstruction(cc_14, False))
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceH_AdditionalInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'BrokerIdentification_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1861, 4))
    st_11 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_12, False))
    final_update.add(fac.UpdateInstruction(cc_15, False))
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceH_AdditionalInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'BrokerIdentification_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1862, 4))
    st_12 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_12)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_16, False))
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceH_AdditionalInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'BrokersCommission')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1864, 3))
    st_13 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_13)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_17, False))
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceH_AdditionalInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CounterpartysReference')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1865, 3))
    st_14 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_14)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_18, False))
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceH_AdditionalInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'BrokersReference')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1866, 3))
    st_15 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_15)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_19, False))
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceH_AdditionalInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CommissionAndFees')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1867, 3))
    st_16 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_16)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_20, False))
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceH_AdditionalInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SenderToReceiverInformation')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1868, 3))
    st_17 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_17)
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
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_17, [
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
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_2, False),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_2, False),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_2, False),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_2, False),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_17, [
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
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_2, False),
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_2, False),
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_2, False),
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_2, False),
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_17, [
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
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_2, False),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_2, False),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_2, False),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_2, False),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_17, [
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
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_2, False),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_2, False),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_2, False),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_2, False),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_17, [
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
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_7, False),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_7, False),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_7, False),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_7, False),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_17, [
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
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_7, False),
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_7, False),
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_7, False),
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_7, False),
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_17, [
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
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_7, False),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_7, False),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_7, False),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_7, False),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_17, [
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
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_7, False),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_7, False),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_7, False),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_7, False),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_7, False),
        fac.UpdateInstruction(cc_11, False) ]))
    st_9._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_12, True),
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_13, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_12, True),
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_12, True),
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_12, False),
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
    st_10._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_12, True),
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_12, True),
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_14, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_12, True),
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_12, False),
        fac.UpdateInstruction(cc_14, False) ]))
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
    st_11._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_12, True),
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_12, True),
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_12, True),
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_15, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_12, False),
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_12, False),
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_12, False),
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_12, False),
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_12, False),
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
    st_14._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_18, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_18, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_18, False) ]))
    st_15._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_19, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_19, False) ]))
    st_16._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_20, True) ]))
    st_17._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
MT320_SequenceH_AdditionalInformation._Automaton = _BuildAutomaton_7()




MT320_SequenceI_AdditionalAmounts._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'NumberOfRepetitions'), MT320_SequenceI_AdditionalAmounts_18A_Type, scope=MT320_SequenceI_AdditionalAmounts, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1876, 3)))

MT320_SequenceI_AdditionalAmounts._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'AMOUNT'), MT320_SequenceI_AdditionalAmounts_AMOUNT, scope=MT320_SequenceI_AdditionalAmounts, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1877, 3)))

MT320_SequenceI_AdditionalAmounts._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_A'), MT320_SequenceI_AdditionalAmounts_53A_Type, scope=MT320_SequenceI_AdditionalAmounts, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1879, 4)))

MT320_SequenceI_AdditionalAmounts._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_D'), MT320_SequenceI_AdditionalAmounts_53D_Type, scope=MT320_SequenceI_AdditionalAmounts, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1880, 4)))

MT320_SequenceI_AdditionalAmounts._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_J'), MT320_SequenceI_AdditionalAmounts_53J_Type, scope=MT320_SequenceI_AdditionalAmounts, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1881, 4)))

MT320_SequenceI_AdditionalAmounts._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Intermediary2_A'), MT320_SequenceI_AdditionalAmounts_86A_Type, scope=MT320_SequenceI_AdditionalAmounts, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1884, 4)))

MT320_SequenceI_AdditionalAmounts._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Intermediary2_D'), MT320_SequenceI_AdditionalAmounts_86D_Type, scope=MT320_SequenceI_AdditionalAmounts, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1885, 4)))

MT320_SequenceI_AdditionalAmounts._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Intermediary2_J'), MT320_SequenceI_AdditionalAmounts_86J_Type, scope=MT320_SequenceI_AdditionalAmounts, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1886, 4)))

MT320_SequenceI_AdditionalAmounts._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_A'), MT320_SequenceI_AdditionalAmounts_56A_Type, scope=MT320_SequenceI_AdditionalAmounts, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1889, 4)))

MT320_SequenceI_AdditionalAmounts._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_D'), MT320_SequenceI_AdditionalAmounts_56D_Type, scope=MT320_SequenceI_AdditionalAmounts, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1890, 4)))

MT320_SequenceI_AdditionalAmounts._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_J'), MT320_SequenceI_AdditionalAmounts_56J_Type, scope=MT320_SequenceI_AdditionalAmounts, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1891, 4)))

MT320_SequenceI_AdditionalAmounts._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_A'), MT320_SequenceI_AdditionalAmounts_57A_Type, scope=MT320_SequenceI_AdditionalAmounts, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1894, 4)))

MT320_SequenceI_AdditionalAmounts._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_D'), MT320_SequenceI_AdditionalAmounts_57D_Type, scope=MT320_SequenceI_AdditionalAmounts, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1895, 4)))

MT320_SequenceI_AdditionalAmounts._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_J'), MT320_SequenceI_AdditionalAmounts_57J_Type, scope=MT320_SequenceI_AdditionalAmounts, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1896, 4)))

def _BuildAutomaton_8 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_8
    del _BuildAutomaton_8
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1878, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1879, 4))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1880, 4))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1881, 4))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1883, 3))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1884, 4))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1885, 4))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1886, 4))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1888, 3))
    counters.add(cc_8)
    cc_9 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1889, 4))
    counters.add(cc_9)
    cc_10 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1890, 4))
    counters.add(cc_10)
    cc_11 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1891, 4))
    counters.add(cc_11)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceI_AdditionalAmounts._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'NumberOfRepetitions')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1876, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceI_AdditionalAmounts._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'AMOUNT')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1877, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceI_AdditionalAmounts._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1879, 4))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceI_AdditionalAmounts._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1880, 4))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceI_AdditionalAmounts._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1881, 4))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceI_AdditionalAmounts._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Intermediary2_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1884, 4))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceI_AdditionalAmounts._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Intermediary2_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1885, 4))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceI_AdditionalAmounts._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Intermediary2_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1886, 4))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceI_AdditionalAmounts._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1889, 4))
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceI_AdditionalAmounts._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1890, 4))
    st_9 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceI_AdditionalAmounts._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1891, 4))
    st_10 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceI_AdditionalAmounts._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1894, 4))
    st_11 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceI_AdditionalAmounts._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1895, 4))
    st_12 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_12)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceI_AdditionalAmounts._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1896, 4))
    st_13 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_13)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
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
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_13, [
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
        fac.UpdateInstruction(cc_4, True),
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
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_13, [
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
        fac.UpdateInstruction(cc_4, True),
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
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_6, False) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_4, True),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_4, True),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_4, True),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_7, True) ]))
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
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_7, False) ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_8, True),
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_9, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_8, True),
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_8, True),
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_9, False) ]))
    st_8._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_8, True),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_8, True),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_10, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_8, True),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_10, False) ]))
    st_9._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_8, True),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_8, True),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_8, True),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_11, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_11, False) ]))
    st_10._set_transitionSet(transitions)
    transitions = []
    st_11._set_transitionSet(transitions)
    transitions = []
    st_12._set_transitionSet(transitions)
    transitions = []
    st_13._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
MT320_SequenceI_AdditionalAmounts._Automaton = _BuildAutomaton_8()




MT320_SequenceI_AdditionalAmounts_AMOUNT._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PaymentDate'), MT320_SequenceI_AdditionalAmounts_AMOUNT_30F_Type, scope=MT320_SequenceI_AdditionalAmounts_AMOUNT, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1905, 3)))

MT320_SequenceI_AdditionalAmounts_AMOUNT._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CurrencyPaymentAmount'), MT320_SequenceI_AdditionalAmounts_AMOUNT_32H_Type, scope=MT320_SequenceI_AdditionalAmounts_AMOUNT, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1906, 3)))

def _BuildAutomaton_9 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_9
    del _BuildAutomaton_9
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceI_AdditionalAmounts_AMOUNT._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PaymentDate')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1905, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT320_SequenceI_AdditionalAmounts_AMOUNT._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CurrencyPaymentAmount')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1906, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
MT320_SequenceI_AdditionalAmounts_AMOUNT._Automaton = _BuildAutomaton_9()




CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SequenceA_GeneralInformation'), MT320_SequenceA_GeneralInformation, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1912, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SequenceB_TransactionDetails'), MT320_SequenceB_TransactionDetails, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1913, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SequenceC_SettlementInstructionsforAmountsPayablebyPartyA'), MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1914, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SequenceD_SettlementInstructionsforAmountsPayablebyPartyB'), MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1915, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SequenceE_SettlementInstructionsforInterestsPayablebyPartyA'), MT320_SequenceE_SettlementInstructionsforInterestsPayablebyPartyA, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1916, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SequenceF_SettlementInstructionsforInterestsPayablebyPartyB'), MT320_SequenceF_SettlementInstructionsforInterestsPayablebyPartyB, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1917, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SequenceG_TaxInformation'), MT320_SequenceG_TaxInformation, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1918, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SequenceH_AdditionalInformation'), MT320_SequenceH_AdditionalInformation, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1919, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SequenceI_AdditionalAmounts'), MT320_SequenceI_AdditionalAmounts, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1920, 4)))

def _BuildAutomaton_10 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_10
    del _BuildAutomaton_10
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1916, 4))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1917, 4))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1918, 4))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1919, 4))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1920, 4))
    counters.add(cc_4)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SequenceA_GeneralInformation')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1912, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SequenceB_TransactionDetails')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1913, 4))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SequenceC_SettlementInstructionsforAmountsPayablebyPartyA')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1914, 4))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SequenceD_SettlementInstructionsforAmountsPayablebyPartyB')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1915, 4))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SequenceE_SettlementInstructionsforInterestsPayablebyPartyA')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1916, 4))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SequenceF_SettlementInstructionsforInterestsPayablebyPartyB')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1917, 4))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SequenceG_TaxInformation')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1918, 4))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SequenceH_AdditionalInformation')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1919, 4))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SequenceI_AdditionalAmounts')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT320.xsd', 1920, 4))
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
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
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_4, True) ]))
    st_8._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON._Automaton = _BuildAutomaton_10()


